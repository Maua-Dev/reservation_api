from typing import List
from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.sport import SPORT


class BookingViewmodel:

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
            'materials': self.booking.materials,
            'type': self.booking.booking_type.value
        }
    
class UpdateBookingViewmodel:

    def __init__(self, booking: Booking):
        self.booking = BookingViewmodel(booking)

    def to_dict(self):
        return{
            'booking' : self.booking.to_dict(),
            'message': 'the booking was retrieved'
        }