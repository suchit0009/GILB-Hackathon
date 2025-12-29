from kafka import KafkaConsumer, KafkaProducer
import json

class ShadowRouter:
    """
    Shadow Mode Router
    Duplicates live traffic to a 'Challenger' topic for asynchronous model evaluation.
    """
    def __init__(self, bootstrap_servers='localhost:9092'):
        self.consumer = KafkaConsumer(
            'tx-raw',
            bootstrap_servers=bootstrap_servers,
            group_id='shadow-router-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )

    def start(self):
        print("Shadow Router Started...")
        for message in self.consumer:
            txn = message.value
            
            # 1. Verification: Ensure we don't modify the data
            # 2. Routing: Send to Challenger Topic
            self.producer.send('tx-challenger', value=txn)
            
            # Optional: Log sample rate
            if hash(str(txn)) % 100 == 0:
                print(f"[SHADOW] Routed Txn {txn.get('id', '?')} to Challenge Lane")

if __name__ == "__main__":
    router = ShadowRouter()
    router.start()
