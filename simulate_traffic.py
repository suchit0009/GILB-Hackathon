import time
import random
import json
from fast_lane.inference import FastPathEngine

# Mock Data
NAMES = ["Ramesh", "Sita", "Hari", "Gita", "CryptoKing", "BetMaster", "Mule_1", "Mule_2"]
TYPES = ["CASH_IN", "CASH_OUT", "TRANSFER", "PAYMENT"]

def generate_transaction():
    src = random.choice(NAMES)
    dest = random.choice([n for n in NAMES if n != src])
    type_tx = random.choice(TYPES)
    amount = random.expovariate(1/5000) # Mostly small, some huge
    # Simulate Balances
    oldbalanceOrg = amount + random.uniform(0, 10000)
    newbalanceOrig = oldbalanceOrg - amount
    oldbalanceDest = random.uniform(0, 10000)
    newbalanceDest = oldbalanceDest + amount
    
    # --- INJECT FRAUD PATTERN (15% Chance) ---
    is_forced_fraud = random.random() < 0.15
    if is_forced_fraud and type_tx in ['TRANSFER', 'CASH_OUT']:
        # Fraud Pattern 1: Emptying the account (common in PaySim)
        # The 'newbalanceOrig' becomes 0 even if amount != oldbalanceOrg locally (errorBalance)
        newbalanceOrig = 0.0 
        # Fraud Pattern 2: Destination receives nothing (money laundering sink)
        newbalanceDest = oldbalanceDest 
        
        # Increase amount to trigger model sensitivity if needed
        if random.random() > 0.5:
            amount = amount * 10
            
    return {
        "id": f"TX-{random.randint(10000, 99999)}",
        "timestamp": time.time(),
        "amount": round(amount, 2),
        "nameOrig": src,
        "nameDest": dest,
        "type": type_tx,
        "oldbalanceOrg": round(oldbalanceOrg, 2),
        "newbalanceOrig": round(newbalanceOrig, 2),
        "oldbalanceDest": round(oldbalanceDest, 2),
        "newbalanceDest": round(newbalanceDest, 2)
    }

def simulate():
    print(">>> STARTING SENTINEL TRAFFIC SIMULATOR (MOCK MODE) <<<")
    print("---------------------------------------------------------")
    
    engine = FastPathEngine()
    
    try:
        while True:
            txn = generate_transaction()
            
            # 1. Edge: Biometrics (Mock)
            bio_score = random.random()
            txn['liveness_score'] = bio_score
            
            # 2. Fast Path Inference
            decision = engine.process_transaction(txn)
            
            # Output
            symbol = "✅" if decision['decision'] == 'ALLOW' else "🛑"
            
            print(f"{symbol} [TXN {txn['id']}] {txn['nameOrig']} -> {txn['nameDest']} | NPR {txn['amount']:.2f}")
            print(f"   Risk: {decision['risk_score']:.2f} | Latency: {decision['latency_ms']:.1f}ms | Breaker: {decision.get('circuit_breaker_triggered', False)}")
            
            # --- DASHBOARD INTEGRATION ---
            # Write latest state to JSON for Dashboard polling
            dash_data = {
                "tps": random.randint(3200, 4800), # Simulated system load
                "latency": int(decision['latency_ms']),
                "health": 99.9,
                "latest_threat": {
                    "id": txn['id'],
                    "time": time.strftime("%H:%M:%S"),
                    "type": txn['type'],
                    "amount": txn['amount'],
                    "risk": decision['risk_score']
                } if decision['risk_score'] > 0.5 else None
            }
            try:
                # Atomic write (mostly) to avoid read conflicts
                with open("dashboard/public/live_data.json", "w") as f:
                    json.dump(dash_data, f)
            except Exception:
                pass 

            # Simulate "Hundi" detection occasionally
            if decision['decision'] == 'BLOCK':
                print(f"   🚨 ALERT: Hundi Pattern / High Risk Detected!")
            
            print("-" * 60)
            time.sleep(1.0) # Slower loop to allow UI to catch up
            
    except KeyboardInterrupt:
        print("\nStopping Simulator...")

if __name__ == "__main__":
    simulate()
