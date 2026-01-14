import os
import random
from locust import HttpUser, task, between, events

class CodeSnapUser(HttpUser):
    wait_time = between(1, 5)
    
    def on_start(self):
        """Authenticate user on start to get JWT token."""
        self.username = "admin" # Defaulting to admin or a known test user
        self.password = "admin" # Defaulting to admin password or known test password
        self.token = self.login()

    def login(self):
        """
        Logins to Keycloak to retrieve a token.
        Assumes Keycloak is reachable at the service name 'keycloak' or configured URL.
        """
        # We need to hit the Keycloak token endpoint.
        # Inside the docker network, keycloak is at http://keycloak:8080
        keycloak_url = os.environ.get("KEYCLOAK_URL", "http://keycloak:8080")
        realm = os.environ.get("KEYCLOAK_REALM", "codesnap")
        client_id = os.environ.get("KEYCLOAK_CLIENT_ID", "codesnap-client")
        
        url = f"{keycloak_url}/realms/{realm}/protocol/openid-connect/token"
        data = {
            "client_id": client_id,
            "username": self.username,
            "password": self.password,
            "grant_type": "password"
        }
        
        try:
            # We use a separate session for auth so it doesn't mess with metrics if we don't want it to
            # Or we can just use self.client.post if we want to track auth time
            response = self.client.post(url, data=data, name="/login (Keycloak)")
            if response.status_code == 200:
                return response.json().get("access_token")
            else:
                print(f"Login failed: {response.text}")
                return None
        except Exception as e:
            print(f"Login exception: {e}")
            return None

    @property
    def headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    @task(3)
    def view_profile(self):
        if self.token:
            self.client.get("/users/me", headers=self.headers, name="/users/me")

    @task(5)
    def list_exercises(self):
        if self.token:
            self.client.get("/exercises/", headers=self.headers, name="/exercises/")

    @task(1)
    def view_history(self):
        if self.token:
            self.client.get("/attempts/my-history", headers=self.headers, name="/attempts/my-history")
            
    # CRITICAL: Do NOT add tasks for /ai endpoints to avoid usage limits.
