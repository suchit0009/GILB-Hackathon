import time
from typing import Callable, Any, Dict

class CircuitBreaker:
    """
    Sentinel Circuit Breaker
    Enforces Fail-Open vs Fail-Closed logic based on transaction value and system latency.
    """
    def __init__(self, timeout_ms: int = 150):
        self.timeout_ms = timeout_ms
        self.FAIL_OPEN_THRESHOLD = 500.0  # NPR

    def execute(self, txn_data: Dict, inference_func: Callable) -> Dict:
        """
        Wraps the inference call with a timeout/resilience check.
        """
        start_time = time.time()
        
        try:
            # Simulate strict timeout enforcement (in production this would be async/threaded)
            # For this MVP python wrapper, we assume inference_func checks its own time or we measure after.
            result = inference_func(txn_data)
            
            elapsed_ms = (time.time() - start_time) * 1000
            
            if elapsed_ms > self.timeout_ms:
                # Latency Breach - Trigger Fail-Safe Logic
                return self._fallback_decision(txn_data, reason=f"Latency Breach: {elapsed_ms:.2f}ms", latency=elapsed_ms)
            
            return result

        except Exception as e:
            # Error / Crash - Trigger Fail-Safe Logic
            return self._fallback_decision(txn_data, reason=f"System Error: {str(e)}", latency=0.0)

    def _fallback_decision(self, txn_data: Dict, reason: str, latency: float) -> Dict:
        """
        Decides whether to ALLOW or BLOCK when the system fails/stalls.
        """
        amount = float(txn_data.get('amount', 0))
        
        if amount < self.FAIL_OPEN_THRESHOLD:
            # Fail-Open: Allow low value transactions to preserve UX
            return {
                "decision": "ALLOW",
                "risk_score": 0.0,
                "reason": f"FAIL-OPEN: {reason}",
                "circuit_breaker_triggered": True,
                "latency_ms": latency
            }
        else:
            # Fail-Closed: Block high value transactions to preserve funds
            return {
                "decision": "BLOCK",
                "risk_score": 1.0,
                "reason": f"FAIL-CLOSED: {reason}",
                "circuit_breaker_triggered": True,
                "latency_ms": latency
            }
