from src.shared.domain.entities.booking import Booking
from src.shared.domain.repositories.booking_repository_interface import IBookingRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound

class GetBookingUseCase:
    repo: IBookingRepository

    def __init__(self, repo: IBookingRepository):
        self.repo = repo
    
    def __call__(self, booking_id: str):
        if not Booking.validate_booking_id(booking_id=booking_id):
            raise EntityError('Invalid booking id')
        
        booking = self.repo.get_booking(booking_id=booking_id)
        if booking is None:
            raise NoItemsFound('booking id')
        
        return booking