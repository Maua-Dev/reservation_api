from typing import Optional

from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.sport import SPORT
from src.shared.domain.enums.type import BOOKING_TYPE
from src.shared.domain.repositories.booking_repository_interface import IBookingRepository
import os
from src.shared.clients.user_api_client import UserAPIClient
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, DependantFilter

class GetBookingsUseCase:
    repo: IBookingRepository

    def __init__(self, repo: IBookingRepository, user_client=None):
        self.repo = repo
        self.user_client = user_client

    
    def __call__(self,
                 booking_id: Optional[str] = None,
                 user_id: Optional[str] = None,
                 sport: Optional[str] = None,
                 court_number: Optional[int] = None,
                 end_date: Optional[int] = None,
                 start_date: Optional[int] = None,
                 booking_type: Optional[str] = None,
                 requester_role: str = None):

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
        
        if booking_type:
            if not Booking.validate_booking_type(BOOKING_TYPE(booking_type)):
                raise EntityError('type')
        
        bookings = self.repo.get_bookings(
            booking_id=booking_id if booking_id else None,
            user_id=user_id if user_id else None,
            sport=SPORT(sport) if sport else None,
            court_number=court_number if court_number else None,
            end_date=end_date if end_date else None,
            start_date=start_date if start_date else None,
            booking_type=BOOKING_TYPE(booking_type) if booking_type else None)
        if bookings is None or bookings == []:
            raise NoItemsFound('booking filters passed')
        
        owner_list = []
        
        for booking in bookings:
            if requester_role == 'ADMIN':
                client = self.user_client or UserAPIClient()
                try:
                    owner = {
                        'name': client.get_user_name(booking.user_id),
                        'network_id': client.get_user_network_id(booking.user_id),
                    }
                except Exception as e:
                    print(f"ERRO NA API DE USER: {e}")
                    owner = {
                        'name': 'Erro de integração',
                        'network_id': 'Erro de integração',
                    }
                owner_list.append(owner)

        return {'bookings': bookings, 'owner': owner_list}
