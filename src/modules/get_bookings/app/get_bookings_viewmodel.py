from typing import List
from src.shared.domain.entities.booking import Booking


class GetBookingsViewmodel:
    bookings: List[Booking]

    def __init__(self, bookings: list, owner_list: list = None):
        if isinstance(bookings, dict):
            data = bookings
            self.bookings = data.get('bookings', [])
            self.owner_list = data.get('owner', [])
        else:
            self.bookings = bookings or []
            self.owner_list = owner_list or []

    def to_dict(self):
        bookings_response = []

        for index, booking in enumerate(self.bookings):
            booking_dict = {
                k: v for k, v in booking.to_dict().items() if k != 'user_id'
            }

            if index < len(self.owner_list):
                owner = self.owner_list[index]
                booking_dict['owner_name'] = owner.get('name')
                booking_dict['owner_network_id'] = owner.get('network_id')

            bookings_response.append(booking_dict)

        return {
            'bookings': bookings_response,
            'message': 'the bookings were retrieved'
        }
