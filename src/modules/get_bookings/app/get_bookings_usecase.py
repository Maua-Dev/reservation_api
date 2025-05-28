from typing import Optional

from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.sport import SPORT
from src.shared.domain.repositories.booking_repository_interface import IBookingRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, DependantFilter

class GetBookingsUseCase:
    repo: IBookingRepository

    def __init__(self, repo: IBookingRepository):
        self.repo = repo
    
    def __call__(self,
                 booking_id: Optional[str] = None,
                 user_id: Optional[str] = None,
                 sport: Optional[str] = None,
                 court_number: Optional[int] = None,
                 end_date: Optional[int] = None,
                 start_date: Optional[int] = None):

        if booking_id:
            if not Booking.validate_booking_id(booking_id):
                raise EntityError('booking_id')
        if user_id:
            if not Booking.validate_user_id(user_id):
                raise EntityError('user_id')
        if sport:
            if not Booking.validate_sport(SPORT(sport)):
                raise EntityError('sport')
        if court_number:
            if not Booking.validate_court(court_number):
                raise EntityError('court_number')
        if end_date and start_date:
            if not Booking.validate_dates(end_date, start_date):
                raise EntityError('end_date or start_date')

        if (start_date and not end_date) or (end_date and not start_date):
            raise DependantFilter('start_date and end_date')
        
        bookings = self.repo.get_bookings(
            booking_id=booking_id if booking_id else None,
            user_id=user_id if user_id else None,
            sport=SPORT(sport) if sport else None,
            court_number=court_number if court_number else None,
            end_date=end_date if end_date else None,
            start_date=start_date if start_date else None)
        if bookings is None or bookings == []:
            raise NoItemsFound('booking filters passed')
        
        return bookings
