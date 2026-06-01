import random
from locust import HttpUser, task, between

class P2PUserLoadTest(HttpUser):
    wait_time = between(0.1, 1.0) 

    @task
    def search_stress_test(self):
        algos = ["flooding", "informed_flooding", "random_walk", "informed_random_walk"]
        
        node_id = f"n{random.randint(1, 12)}"
        resource_id = f"r{random.randint(1, 10)}"
        ttl = random.randint(2, 5)
        algo = random.choice(algos)

        payload = {
            "node_id": node_id,
            "resource_id": resource_id,
            "ttl": ttl,
            "algo": algo
        }

        self.client.post("/search", json=payload)