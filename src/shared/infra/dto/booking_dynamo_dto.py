from typing import List

from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.sport import SPORT


class BookingDynamoDTO:
    start_date: int
    end_date: int
    court_number: int
    sport: SPORT
    user_id: str
    booking_id: str
    materials: List[str]

    def __init__(self, start_date: int, end_date: int, court_number: int, sport: SPORT, user_id: str, booking_id: str, materials: List[str]):
        self.start_date = start_date
        self.end_date = end_date
        self.court_number = court_number
        self.sport = sport
        self.user_id = user_id
        self.booking_id = booking_id
        self.materials = materials

    @staticmethod
    def from_entity(booking: Booking) -> 'BookingDynamoDTO':
        '''
        Converts a Booking entity to a BookingDynamoDTO
        '''
        return BookingDynamoDTO(
            start_date = booking.start_date,
            end_date = booking.end_date,
            court_number = booking.court_number,
            sport = booking.sport,
            user_id = booking.user_id,
            booking_id = booking.booking_id,
            materials = booking.materials
        )

    def to_dynamo(self) -> dict:
        """
        Converts a BookingDynamoDTO to a dynamo item
        """
        data = {
            "entity": "booking",
            "start_date": self.start_date,
            "end_date": self.end_date,
            "court_number": self.court_number,
            "sport": self.sport.value,
            "user_id": self.user_id,
            "booking_id": self.booking_id,
            "materials": self.materials
        }

        booking_without_none_values = {k: v for k, v in data.items() if v is not None}

        return booking_without_none_values
    
    @staticmethod
    def from_dynamo(booking_data: dict) -> "BookingDynamoDTO":
        """
        Converts a dynamo item to a BookingDynamoDTO
        """
        return BookingDynamoDTO(
            start_date = int(booking_data["start_date"]),
            end_date = int(booking_data["end_date"]),
            court_number = int(booking_data["court_number"]),
            sport = SPORT(booking_data["sport"]),
            user_id = booking_data["user_id"],
            booking_id = booking_data["booking_id"],
            materials = booking_data["materials"]
        )
    
    def to_entity(self) -> Booking:
        """
        Parse a BookingDynamoDTO to a Booking entity
        """
        return Booking(
            start_date=self.start_date,
            end_date=self.end_date,
            court_number=self.court_number,
            sport=self.sport,
            user_id=self.user_id,
            booking_id=self.booking_id,
            materials=self.materials
        )
    
    def __repr__(self):
        return f"BookingDynamoDTO(start_date={self.start_date}, end_date={self.end_date}, court_number={self.court_number}, sport={self.sport}, user_id={self.user_id}, booking_id={self.booking_id}, materials={self.materials})"
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
