import abc
import uuid
from typing import Optional, List
from src.shared.domain.entities.court import Court
from src.shared.domain.enums.sport import SPORT
from src.shared.helpers.errors.domain_errors import EntityError

class Booking(abc.ABC):
    start_date: int
    end_date: int
    court_number: int
    sport: SPORT
    user_id: str
    booking_id: str
    materials: List[str]


    def __init__(self, start_date: int, end_date: int, court_number: int, sport: SPORT, user_id: str, booking_id: str, materials: List[str]):
        if not Booking.validate_dates(start_date, end_date):
            raise EntityError("dates")
        self.start_date = start_date
        self.end_date = end_date

        if not Booking.validate_court(court_number):
            raise EntityError("court")
        self.court_number = court_number

        if not Booking.validate_sport(sport):
            raise EntityError("sport")
        self.sport = sport

        if not Booking.validate_user_id(user_id):
            raise EntityError("user_id")
        self.user_id = user_id

        if not Booking.validate_booking_id(booking_id):
            raise EntityError("booking_id")
        self.booking_id = booking_id

        if not Booking.validate_materials(materials):
            raise EntityError("materials")
        self.materials = materials


    @staticmethod
    def validate_dates(start_date: int, end_date: int) -> bool:
        if not isinstance(start_date, int) or not isinstance(end_date, int) or start_date >= end_date:
            return False
        return True

    @staticmethod
    def validate_court(court_number: int) -> bool:
        if not isinstance(court_number, int):
            return False
        return True

    @staticmethod
    def validate_sport(sport: SPORT) -> bool:
        if not isinstance(sport, SPORT):
            return False
        return True

    @staticmethod
    def validate_user_id(user_id: str) -> bool:
        if not isinstance(user_id, str):
            return False
        try:
            val = uuid.UUID(user_id, version=4)
        except ValueError:
            return False
        return True

    @staticmethod   
    def validate_booking_id(booking_id: str) -> bool:
        if not isinstance(booking_id, str):
            return False
        try:
            val = uuid.UUID(booking_id, version=4)
        except ValueError:
            return False
        return True

    @staticmethod
    def validate_materials(materials: List[str]) -> bool:
        if not isinstance(materials, list) or not all(isinstance(item, str) for item in materials) or materials == []:
            return False
        return True
    
    def to_dict(self):
        return {
            "start_date": self.start_date,
            "end_date": self.end_date,
            "court_number": self.court_number,
            "sport": self.sport.value,
            "user_id": self.user_id,
            "booking_id": self.booking_id,
            "materials": self.materials
        }