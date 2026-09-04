from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.sport import SPORT

class BookingViewmodel:
    start_date: int
    end_date: int
    court_number: int
    sport: SPORT
    booking_id: str
    materials: list

    def __init__(self, booking: Booking, owner: dict = None):
        self.start_date = booking.start_date
        self.end_date = booking.end_date
        self.court_number = booking.court_number
        self.sport = booking.sport
        self.booking_id = booking.booking_id
        self.materials = booking.materials
        self.booking_type = booking.booking_type
        self.owner = owner

    def to_dict(self):
        booking_dict = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'court_number': self.court_number,
            'sport': self.sport.value,
            'booking_id': self.booking_id,
            'materials': self.materials,
            "type": self.booking_type.value
        }

        if self.owner is not None:
            booking_dict['owner_name'] = self.owner.get('name')
            booking_dict['owner_network_id'] = self.owner.get('network_id')

        return booking_dict

class GetBookingViewmodel:
    booking_viewmodel: BookingViewmodel

    def __init__(self, booking: Booking, owner: dict = None):
        self.booking = BookingViewmodel(booking, owner)

    def to_dict(self):
        return{
            'booking': self.booking.to_dict(),
            'message': 'the booking was retrieved'
        }
