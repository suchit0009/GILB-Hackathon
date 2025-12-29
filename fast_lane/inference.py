import random
import time
import xgboost as xgb
import pandas as pd
import os
from .circuit_breaker import CircuitBreaker

MODEL_PATH = "fast_lane/sentinel_xgboost.model"

class FastPathEngine:
    def __init__(self):
        self.breaker = CircuitBreaker(timeout_ms=200)
        self.model = None
        self._load_model()

    def _load_model(self):
        """Loads the trained XGBoost model if available."""
        if os.path.exists(MODEL_PATH):
            try:
                self.model = xgb.Booster()
                self.model.load_model(MODEL_PATH)
                print(f"✅ FastPathEngine: Loaded Real Model from {MODEL_PATH}")
            except Exception as e:
                print(f"❌ FastPathEngine: Failed to load model: {e}")
        else:
            print("⚠️  FastPathEngine: Model not found. Running in MOCK MODE.")

    def _xgboost_predict(self, txn_data):
        """
        Runs Real XGBoost Inference if model exists, else Logic Mock.
        """
        start_time = time.time()
        
        # 1. Feature Engineering (Must match training logic!)
        if self.model:
            try:
                # Type Encoding
                t_type = 0 if txn_data['type'] == 'TRANSFER' else (1 if txn_data['type'] == 'CASH_OUT' else -1)
                
                # Check if it's a relevant type (Transfer/Cashout only)
                if t_type == -1:
                     # Payment/Debit usually low risk in this specific model context
                    risk_score = 0.01 
                else:
                    # Calc Errors
                    errorBalanceOrig = txn_data['newbalanceOrig'] + txn_data['amount'] - txn_data['oldbalanceOrg']
                    errorBalanceDest = txn_data['oldbalanceDest'] + txn_data['amount'] - txn_data['newbalanceDest']

                    features = pd.DataFrame([{
                        'type': t_type,
                        'amount': txn_data['amount'],
                        'oldbalanceOrg': txn_data['oldbalanceOrg'],
                        'newbalanceOrig': txn_data['newbalanceOrig'],
                        'errorBalanceOrig': errorBalanceOrig,
                        'errorBalanceDest': errorBalanceDest
                    }])
                    
                    # Convert to DMatrix
                    dtest = xgb.DMatrix(features)
                    
                    # Predict
                    risk_score = float(self.model.predict(dtest)[0])
            except Exception as e:
                print(f"Prediction Error: {e}")
                risk_score = 0.5 # Fallback
        else:
            # --- MOCK LOGIC FALLBACK ---
            time.sleep(0.05) # Simulate latency
            risk_score = 0.1
            if txn_data.get('amount', 0) > 100000:
                risk_score += 0.8

        latency_ms = (time.time() - start_time) * 1000
        
        return {
            "decision": "BLOCK" if risk_score > 0.8 else "ALLOW",
            "risk_score": risk_score,
            "latency_ms": latency_ms
        }

    def process_transaction(self, txn_data):
        """
        Main entry point for the Fast Path.
        """
        return self.breaker.execute(txn_data, self._xgboost_predict)
