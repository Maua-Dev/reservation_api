from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.sport import SPORT
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.domain.repositories.reservation_repository_interface import IReservationRepository

class DeleteBookingUsecase:
    def __init__(self, repo:IReservationRepository):
        self.repo = repo
    
    def __call__(self, booking_id: int):    
        
        if not Booking.validate_booking_id(booking_id):
            raise EntityError('booking_id')
        
        booking = self.repo.delete_booking(booking_id=booking_id)
        
        if booking is None:
            raise NoItemsFound('booking')
        
        return booking