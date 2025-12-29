import sys
import os
import pytest
import time
import torch

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fast_lane.inference import FastPathEngine
from fast_lane.circuit_breaker import CircuitBreaker
import deep_lane.graph_analytics as ga

# --- FAST PATH TESTS ---

def test_xgboost_model_loaded():
    """Verify that FastPathEngine successfully loads the trained XGBoost model."""
    engine = FastPathEngine()
    assert engine.model is not None, "❌ XGBoost Model failed to load! (Is it trained?)"
    print("\n✅ XGBoost Model Loaded Successfully")

def test_inference_execution():
    """Verify the engine produces a valid prediction structure for a PaySim-like transaction."""
    engine = FastPathEngine()
    
    # Synthetic Transaction (High Value Transfer)
    tx = {
        "id": "TEST-TXN-001",
        "amount": 250000.0,
        "nameOrig": "C_TEST_ORIG",
        "nameDest": "C_TEST_DEST",
        "type": "TRANSFER",
        "oldbalanceOrg": 300000.0,
        "newbalanceOrig": 50000.0,
        "oldbalanceDest": 0.0,
        "newbalanceDest": 250000.0
    }
    
    result = engine.process_transaction(tx)
    
    assert "decision" in result
    assert "risk_score" in result
    assert "latency_ms" in result
    assert 0.0 <= result["risk_score"] <= 1.0
    assert result["decision"] in ["ALLOW", "BLOCK"]
    print(f"\n✅ Inference Test Passed: {result}")

def test_circuit_breaker_stability():
    """Verify Circuit Breaker doesn't crash on execution."""
    breaker = CircuitBreaker(timeout_ms=500)
    
    def dummy_task(data):
        return "SUCCESS"
        
    res = breaker.execute({}, dummy_task)
    assert res == "SUCCESS"
    print("\n✅ Circuit Breaker Stability Verified")

# --- DEEP PATH TESTS ---

def test_gnn_model_artifact():
    """Verify the GNN model file exists on disk."""
    model_path = "deep_lane/sentinel_gnn.pt"
    assert os.path.exists(model_path), f"❌ GNN Model not found at {model_path}"
    print("\n✅ GNN Model Artifact Found")

def test_graph_analytics_import():
    """Verify Graph Analytics module can be instantiated."""
    try:
        intel = ga.GraphIntel()
        assert intel.G is None
        print("\n✅ Graph Analytics Module Importable")
    except Exception as e:
        pytest.fail(f"Graph Analytics Import Failed: {e}")

if __name__ == "__main__":
    sys.exit(pytest.main(["-v", __file__]))
