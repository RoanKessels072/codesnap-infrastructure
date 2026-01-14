import os
import requests
from locust import HttpUser, task, between, events
import logging

class CodeSnapUser(HttpUser):
    wait_time = between(1, 5)
    
    def on_start(self):
        """Authenticate EACH user on start to load test Keycloak."""
        self.keycloak_url = os.environ.get("KEYCLOAK_URL", "http://keycloak:8080")
        self.realm = os.environ.get("KEYCLOAK_REALM", "codesnap")
        self.client_id = os.environ.get("KEYCLOAK_CLIENT_ID", "codesnap-client")
        
        self.username = os.environ.get("KEYCLOAK_USERNAME", "testuser")
        self.password = os.environ.get("KEYCLOAK_PASSWORD", "password")
        
        self.token = self.login()

    def login(self):
        url = f"{self.keycloak_url}/realms/{self.realm}/protocol/openid-connect/token"
        data = {
            "client_id": self.client_id,
            "username": self.username,
            "password": self.password,
            "grant_type": "password"
        }
        
        try:
            # name argument groups this request in Locust UI
            with self.client.post(url, data=data, name="/login (Keycloak)", catch_response=True) as response:
                if response.status_code == 200:
                    return response.json().get("access_token")
                else:
                    response.failure(f"Login failed: {response.text}")
                    logging.error(f"Login failed for {self.username}: {response.text}")
                    return None
        except Exception as e:
            logging.error(f"Login exception: {e}")
            return None

    @property
    def headers(self):
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    @task(3)
    def view_profile(self):
        if self.token:
            with self.client.get("/users/me", headers=self.headers, catch_response=True, name="/users/me") as response:
                if response.status_code == 401:
                    response.failure("Unauthorized - Refreshing token not implemented")

    @task(5)
    def list_exercises(self):
        if self.token:
            with self.client.get("/exercises/", headers=self.headers, catch_response=True, name="/exercises/") as response:
                if response.status_code == 401:
                    response.failure("Unauthorized")

    @task(1)
    def view_history(self):
        if self.token:
             with self.client.get("/attempts/my-history", headers=self.headers, catch_response=True, name="/attempts/my-history") as response:
                if response.status_code == 401:
                     response.failure("Unauthorized")