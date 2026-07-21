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

    def get_user_network_id(self, user_id):
        user = next((user for user in self.all_users if user["user_id"] == user_id), None)
        if user is None:
            return None
        email = user.get("email")
        if not email or "@" not in email:
            return None
        return email.split("@")[0]

    def authenticate_user(self, token):
        return self._auth_user(token=token)

    @staticmethod
    def retrieve_users():

        api_url= os.environ.get("USER_API_URL")
        try:
            response = requests.get(api_url + '/reservation-mss-user/get-all-users')
            
            response.raise_for_status()
            
            users = response.json().get("users")
            
            if users == None:
                users = []
                
            return users
        except:
            raise Exception('Couldn\'t retrieve users')
        
    #TODO adciionar os parametros nas request, testar se funciona mesmo
        
    @staticmethod
    def _auth_user(token):
        
        '''
        UNUSED AND DEPRECATED DO NOT USE
        '''
        
        #this will only get the user info if the user is already created in db, else it will delete the user shortly after
        
        #UNUSED DO NOT USE THIS, ITS DEPRECATED 
        
        api_url = os.environ.get("USER_API_URL")
        
        #untested funtion
        def delete_user(token):
            
            try:
                
                headers = {
                    "Authorization": f"Bearer{token}"
                }
                
                response = requests.delete(api_url + 'reservation-mss-user/delete-user', headers=headers)
                
                return response.json().get("message")
                
            except:
                
                raise Exception('Could not delete user')
        
        try:
            
            headers = {
                "Authorization": f"Bearer {token}"
            }
            
            response = requests.get(api_url + 'reservation-mss-user/auth-user', headers=headers)
            
            user = response.json().get("user")
            
            identifier = user.get("message", None)
            
            #TODO test this part
            
            if identifier == "the user was created successfully":
                
                #untested funtion
                delete_user(token=token)
                
                raise Exception('User was not registered')
            
            return user
            
        except:
            raise Exception('Could not authenticate user')
        
