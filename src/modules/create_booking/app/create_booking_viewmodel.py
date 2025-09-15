from typing import List

from src.shared.domain.enums.sport import SPORT
from src.shared.domain.enums.type import BOOKING_TYPE


class CreateBookingViewmodel:

    start_date: int
    end_date: int
    court_number: int
    sport: SPORT
    user_id: str
    booking_id: str
    materials: List[str]
    booking_type: BOOKING_TYPE

    def __init__(self, booking):
        self.start_date = booking.start_date
        self.end_date = booking.end_date
        self.court_number = booking.court_number
        self.sport = booking.sport
        self.user_id = booking.user_id
        self.booking_id = booking.booking_id
        self.materials = booking.materials
        self.booking_type = booking.booking_type

    def to_dict(self):

        return {
            "booking": {
                "start_date": self.start_date,
                "end_date": self.end_date,
                "court_number": self.court_number,
                "sport": self.sport.value,
                "user_id": self.user_id,
                "booking_id": self.booking_id,
                "materials": self.materials,
                "type": self.booking_type.value
            },
            "message": "Booking created successfully"
        }
