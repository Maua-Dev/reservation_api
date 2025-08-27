from src.shared.domain.repositories.booking_repository_interface import IBookingRepository
from src.shared.clients.user_api_client import UserAPIClient
from src.shared.helpers.errors.usecase_errors import *

class GetAllAdminBookingsUsecase:
    
    def __init__(self, repo: IBookingRepository):
        
        self.repo = repo
        self.user_client = UserAPIClient()
        
    def __call__(self):
        
        all_users = self.user_client.all_users
        admin_user = None
        
        for item in all_users:
            
            if item.get("role") == "ADMIN" and item.get("email") == "dev@maua.br":
                
                admin_user = item
                
        if admin_user == None:
            
            raise NoAdminFound()
                
        all_bookings = self.repo.get_all_bookings()
        admin_bookings = []
        
        for item in all_bookings:
            
            if item.user_id == admin_user.get("user_id", None):
                
                admin_bookings.append(item)
                
        if not admin_bookings:
            
            raise NoAdminBookingsFound()
                
        return admin_bookings