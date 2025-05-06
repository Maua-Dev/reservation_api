from typing import List
from src.shared.domain.entities.booking import Booking


class GetBookingsViewmodel:
    bookings: List[Booking]

    def __init__(self, bookings: list):
        self.bookings = bookings

    def to_dict(self):
        return {
            'bookings': [booking.to_dict() for booking in self.bookings],
            'message': 'the bookings were retrieved'
        }

