import requests
import json
import os

BASE_URL = "https://intellihack-backend-rcbmvyttca-uc.a.run.app"
BASE_URL_LOCAL = "http://127.0.0.1:8000"
CREDENTIALS_FILE = "credentials.json"

class IntelliBotAPI:
    def __init__(self):
        self.access_token = None
        self.user_id = None
        self.username = None
        self.load_credentials()

    def load_credentials(self):
        if os.path.exists(CREDENTIALS_FILE):
            with open(CREDENTIALS_FILE, 'r') as file:
                credentials = json.load(file)
                self.access_token = credentials.get('access_token')
                self.user_id = credentials.get('user_id')
                self.username = credentials.get('username')

    def save_credentials(self, credentials):
        with open(CREDENTIALS_FILE, 'w') as file:
            json.dump(credentials, file)

    def connect(self, username, password):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"username": username, "password": password}
        response = requests.post(BASE_URL + "/login", data=data, headers=headers)
        if response.status_code == 200:
            auth_data = response.json()
            self.access_token = auth_data["access_token"]
            self.user_id = auth_data["id"]
            self.username = auth_data["email"]
            self.save_credentials({
                "access_token": self.access_token,
                "user_id": self.user_id,
                "username": self.username,
            })
        return response

    def get_active_user_details(self):
        if not self.access_token or not self.user_id:
            raise Exception("User not authenticated. Please connect first.")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        response = requests.get(BASE_URL + f"/user/{self.user_id}", headers=headers)
        return response

    def chat(self, message, history=None):
        if not self.access_token or not self.user_id or not self.username:
            raise Exception("User not authenticated. Please connect first.")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        json_data = {
            "user_id": self.user_id,
            "username": self.username,
            "message": message,
            "history": history if history else "",
        }
        return requests.post(BASE_URL + "/query/chat", json=json_data, headers=headers)

    def initialize_crew(self, config_data):
        if not self.access_token or not self.user_id:
            raise Exception("User not authenticated. Please connect first.")

        config_data['user_id'] = self.user_id

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }

        response = requests.post(
            BASE_URL_LOCAL + f"/agentConfiguration/",
            json=config_data,
            headers=headers,
        )
        return response

    def get_active_projects(self):
        if not self.access_token or not self.user_id:
            raise Exception("User not authenticated. Please connect first.")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        response = requests.get(
            f"{BASE_URL_LOCAL}/agentConfiguration/projects/{self.user_id}",
            headers=headers,
        )
        return response

    def execute_project(self, project_name):
        if not self.access_token:
            raise Exception("User not authenticated. Please connect first.")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        response = requests.get(
            f"{BASE_URL_LOCAL}/agentConfiguration/execute/{project_name}",
            headers=headers,
        )
        return response
