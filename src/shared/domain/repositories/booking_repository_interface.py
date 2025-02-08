from abc import ABC, abstractmethod

from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.sport import SPORT

class IBookingRepository(ABC):

    @abstractmethod
    def create_booking(self, booking: Booking) -> Booking:
        '''
        If booking does not exist, creates it and returns it
        '''
        pass

    @abstractmethod
    def update_booking(self,
                     start_date: int,
                     end_date: int,
                     court_number: int,
                     sport: SPORT
                     ) -> Booking:
        '''
        If booking exists, updates it and returns it
        '''
        pass

    @abstractmethod
    def get_booking(self, booking_id: int):
        '''
        If the booking exists, returns it, else returns None
        '''
        pass
      
    @abstractmethod
    def delete_booking(self, booking_id: int):
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