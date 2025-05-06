from abc import ABC, abstractmethod

from typing import Optional, List

from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.sport import SPORT


class IBookingRepository(ABC):

    @abstractmethod
    def create_booking(self, booking: Booking) -> Optional[Booking]:
        '''
        If booking does not exist, creates it and returns it
        '''
        pass

    @abstractmethod
    def update_booking(self,
                       booking_id: str,
                       start_date: int = None,
                       end_date: int = None,
                       court_number: int = None,
                       sport: SPORT = None,
                       materials: List[str] = None) -> Optional[Booking]:
        '''
        If booking exists, updates it and returns it
        '''
        pass

    @abstractmethod
    def get_booking(self,
                    booking_id: str) -> Optional[Booking]:
        '''
        If the booking exists, returns it, else returns None
        '''
        pass

    @abstractmethod
    def get_bookings(self,
                     booking_id: Optional[str] = None,
                     user_id: Optional[str] = None,
                     sport: Optional[str] = None,
                     court_number: Optional[int] = None,
                     end_date: Optional[int] = None,
                     start_date: Optional[int] = None) -> List[Optional[Booking]]:
        '''
        If the booking exists, returns it, else returns None
        '''
        pass

    @abstractmethod
    def delete_booking(self, booking_id: int) -> Optional[Booking]:
        '''
        If booking exists, deletes it and returns it
        else returns None
        '''
        pass

    @abstractmethod
    def get_all_bookings(self):
        '''
        Returns all bookings
        '''
        pass
