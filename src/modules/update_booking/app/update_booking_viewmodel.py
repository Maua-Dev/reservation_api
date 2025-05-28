from typing import List
from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.sport import SPORT


class BookingViewmodel:
    start_date: int
    end_date: int
    court_number: int
    sport: SPORT
    user_id: str
    booking_id: str
    materials: List[str]

    def __init__(self, booking: Booking):
        self.booking = booking

    def to_dict(self) -> Booking:
        return {
            'start_date': self.booking.start_date,
            'end_date': self.booking.end_date,
            'court_number': self.booking.court_number,
            'sport': self.booking.sport.value,
            'user_id': self.booking.user_id,
            'booking_id': self.booking.booking_id,
            'materials': self.booking.materials
        }
    
class UpdateBookingViewmodel:

    def __init__(self, booking: Booking):
        self.booking = BookingViewmodel(booking)

    def to_dict(self):
        return{
            'booking' : self.booking.to_dict(),
            'message': 'the booking was retrieved'
        }