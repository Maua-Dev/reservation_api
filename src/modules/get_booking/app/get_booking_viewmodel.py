from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.sport import SPORT

class BookingViewmodel:
    start_date: int
    end_date: int
    court_number: int
    sport: SPORT
    user_id: str
    booking_id: str
    materials: list

    def __init__(self, booking: Booking):
        self.start_date = booking.start_date
        self.end_date = booking.end_date
        self.court_number = booking.court_number
        self.sport = booking.sport
        self.user_id = booking.user_id
        self.booking_id = booking.booking_id
        self.materials = booking.materials

    def to_dict(self):
        return {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'court_number': self.court_number,
            'sport': self.sport.value,
            'user_id': self.user_id,
            'booking_id': self.booking_id,
            'materials': self.materials
        }
        
class GetBookingViewmodel:
    booking_viewmodel: BookingViewmodel

    def __init__(self, booking: Booking):
        self.booking = BookingViewmodel(booking)

    def to_dict(self):
        return{
            'booking': self.booking.to_dict(),
            'message': 'the booking was retrieved'
        }
