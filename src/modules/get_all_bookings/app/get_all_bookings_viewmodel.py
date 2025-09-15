from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.sport import SPORT
from typing import List

class BookingViewModel:
    start_date: int
    end_date: int
    court_number: int
    sport: SPORT
    booking_id: str
    materials: List[str]

    def __init__(self, booking: Booking):
        self.start_date = booking.start_date
        self.end_date = booking.end_date
        self.court_number = booking.court_number
        self.sport = booking.sport
        self.booking_id = booking.booking_id
        self.materials = booking.materials
        self.booking_type = booking.booking_type

    def to_dict(self):
        return {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'court_number': self.court_number,
            'sport': self.sport.value,
            'booking_id': self.booking_id,
            'materials': self.materials,
            "type": self.booking_type.value
        }
class GetBookingViewModel:
    booking: Booking
    
    def __init__(self, booking: Booking):
        self.booking_viewmodel = BookingViewModel(booking)

    def to_dict(self):
        return{
            'booking' : self.booking_viewmodel.to_dict()
        }

class GetAllBookingsViewModel:
    bookings: List[GetBookingViewModel]

    def __init__(self, bookings: list):
        self.bookings = [GetBookingViewModel(booking) for booking in bookings]

    def to_dict(self):
        return {
            'bookings': [booking.to_dict() for booking in self.bookings],
            'message': 'the bookings were retrieved'
        }