import json
import os
import requests

from src.shared.environments import Environments

class UserAPIClient:

    def __init__(self):
        self.all_users = self.retrieve_users()

    def get_user_name(self, user_id):
        user = next((user for user in self.all_users if user["user_id"] == user_id), None)
        return user["name"] if user is not None else None

    @staticmethod
    def retrieve_users():

        api_url= os.environ.get("USER_API_URL")
        try:
            response = requests.get(api_url)
            users = response.json().get("users")
            return users
        except:
            raise Exception('Couldn\'t retrieve users')
