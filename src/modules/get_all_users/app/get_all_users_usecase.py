from src.shared.domain.repositories.booking_repository_interface import IBookingRepository
from dotenv import load_dotenv
import os
import requests

load_dotenv()

class GetAllUsersUseCase:
    def __init__(self, repo: IBookingRepository):
        self.repo = repo

    def __call__(self):
        users_id_by_booking = self.repo.get_all_users()
        if not users_id_by_booking:
            return "nenhum usuário encontrado"

        users_id_by_booking = list(set(users_id_by_booking))

        users_data = call_other_microservice()
        if not users_data:
            print("nenhum dado de usuário foi retornado pelo microserviço.")

        valid_users_data = [
            {
                "user_id": user["user_id"],
                "name": user["name"]
            }
            for user in users_data
            if isinstance(user, dict) and "user_id" in user and "name" in user
        ]
        
        if len(valid_users_data) != len(users_data):
            print("dados invalidos/incompletos foram retornados pelo microserviço.")

        user_id_to_name = {user["user_id"]: user["name"] for user in valid_users_data}

        users_with_names = [
            {"user_id": user_id, "name": user_id_to_name.get(user_id)}
            for user_id in users_id_by_booking #verificao se o user_id existe no booking e assim faz a troca
            if user_id_to_name.get(user_id) is not None
        ]

        users_with_names.sort(key=lambda user: user["name"]) # Ordena os nomes dos usuarios por ordem alfabetica
        #feito desta forma pois, o set() não garante a ordem dos elementos 

        return users_with_names

def call_other_microservice():

    load_dotenv()

    url = os.getenv("GET_ALL_USERS_API_URL")

    payload={}
    headers = {
        'User-Agent': os.getenv("GET_ALL_USERS_USER_AGENT"),
        'Authorization': os.getenv("GET_ALL_USERS_AUTHORIZATION_TOKEN"),
        'Accept': '*/*',
        'Host': os.getenv("GET_ALL_USERS_HOST"),
        'Connection': 'keep-alive'
    }

    try:
        response = requests.get(url, headers=headers, data=payload)
        response.raise_for_status()  
        
        data = response.json()
        if not isinstance(data, dict) or "users" not in data:
            print("Erro: Resposta inesperada do microserviço.")
            return []

        return data.get("users", [])
    except Exception as e:
        print(f"Erro ao processar a resposta do serviço: {e}")
        return []