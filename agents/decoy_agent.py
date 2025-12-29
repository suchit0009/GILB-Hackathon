import random

class DecoyAgent:
    """
    Active Defense Unit: Decoy
    Injects disinformation when probing is detected on the API.
    """
    def __init__(self):
        self.decoy_profiles = [
            {"id": "ACC_DECOY_1", "balance": 5000, "status": "ACTIVE"},
            {"id": "ACC_DECOY_2", "balance": 120000, "status": "LOCKED"}, # Honey pot
            {"id": "ACC_DECOY_3", "balance": 0, "status": "ACTIVE"},
        ]

    def intercept_probe(self, request_metadata):
        """
        Analyze request for Reconnaissance patterns (e.g., enumeration).
        """
        # Logic: If 404s > 10 in 1 minute from same IP -> It's a Probe.
        is_probe = True # Simplified trigger
        
        if is_probe:
            return self._generate_poison_pill()
        
        return None

    def _generate_poison_pill(self):
        """
        Returns a valid-schema response with fake data.
        """
        pill = random.choice(self.decoy_profiles)
        print(f"[DECOY] 💊 Injecting Poison Pill: {pill['id']}")
        return pill

if __name__ == "__main__":
    decoy = DecoyAgent()
    print(decoy.intercept_probe({"ip": "192.168.1.50"}))
