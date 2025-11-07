from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.sport import SPORT
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.domain.repositories.booking_repository_interface import IBookingRepository

class DeleteBookingUsecase:
    def __init__(self, repo:IBookingRepository):
        self.repo = repo
    
    def __call__(self, booking_id: int, user):    
        if user.get('user_id') is None:
            raise EntityError('user id')
        
        if user.get('name') is None:
            raise EntityError('user id')

        if user.get('email') is None:
            raise EntityError('user email')
        
        if user.get('role') is None: 
            raise EntityError('user role')

        if not Booking.validate_booking_id(booking_id):
            raise EntityError('booking_id')
        
        booking = self.repo.delete_booking(booking_id=booking_id, user=user)
        
        if booking is None:
            raise NoItemsFound('booking')
        
        if booking is None:
            raise NoItemsFound('booking')
        
        return booking