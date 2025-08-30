from typing import List
from src.shared.domain.entities.booking import Booking


class GetBookingsViewmodel:
    bookings: List[Booking]

    def __init__(self, bookings: list):
        self.bookings = bookings

    def to_dict(self):
        return {
            'bookings': [
                {k: v for k, v in booking.to_dict().items() if k != 'user_id'}
                for booking in self.bookings
            ],
            'message': 'the bookings were retrieved'
        }
