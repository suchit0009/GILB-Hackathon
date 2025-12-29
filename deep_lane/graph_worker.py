import time
import random
from neo4j import GraphDatabase
# import redis

# Mock Redis for MVP
class MockRedis:
    def set(self, key, value):
        print(f"[Redis] SET {key} = {value}")

redis_client = MockRedis()

class GraphWorker:
    """
    Sentinel Deep Path Worker
    Asynchronously traverses the transaction graph to detect complex fraud patterns.
    """
    def __init__(self, uri, auth):
        self.driver = GraphDatabase.driver(uri, auth=auth)

    def close(self):
        self.driver.close()

    def process_transaction(self, txn_id, sender_id):
        """
        Triggered by Kafka message (Async).
        Run deep graph traversal to update risk profile for FUTURE transactions.
        """
        print(f"Analyzing Graph for Txn: {txn_id} (Sender: {sender_id})...")
        
        with self.driver.session() as session:
            # Check for Smurfing (Fan-In)
            fan_in_count = session.execute_read(self._count_fan_in, sender_id)
            
            # Check for Circular Loop
            has_loop = session.execute_read(self._detect_loop, sender_id)
            
            risk_score = 0.0
            if fan_in_count > 10:
                risk_score += 0.5
            if has_loop:
                risk_score += 0.4
                
            if risk_score > 0:
                print(f"!!! DEEP FRAUD DETECTED (Score: {risk_score})")
                # Update Feature Store so FAST PATH blocks next attempt
                redis_client.set(f"risk:{sender_id}", risk_score)
                
                # If high risk, Trigger Hunter Agent
                if risk_score > 0.8:
                    return "TRIGGER_HUNTER"
            
        return "OK"

    @staticmethod
    def _count_fan_in(tx, node_id):
        # Cypher: Find number of distinct SENDERS to this account in last 24h
        query = (
            "MATCH (a:Account)-[:SENT]->(b:Account {id: $id}) "
            "RETURN count(a) as fan_in"
        )
        # Mock result for MVP without live DB
        return random.randint(0, 50) # Simulate varied network

    @staticmethod
    def _detect_loop(tx, node_id):
        # Cypher: Find path back to self length 3..6
        query = (
            "MATCH path = (a:Account {id: $id})-[:SENT*3..6]->(a) "
            "RETURN count(path) > 0 as loop_exists"
        )
        # Mock result
        return random.choice([True, False])

if __name__ == "__main__":
    # Example Usage
    worker = GraphWorker("bolt://localhost:7687", ("neo4j", "test"))
    worker.process_transaction("TXN_123", "ACC_999")
    worker.close()
