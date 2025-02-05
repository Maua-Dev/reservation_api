import abc
from typing import Optional
from datetime import datetime
from src.shared.helpers.errors.domain_errors import EntityError

class Booking(abc.ABC):
    start_date: datetime
    end_date: datetime
    court: int
    sport: str
    user_id: str
    ra: Optional[str]
    booking_id: str
    materials: str


    def __init__(self, start_date: datetime, end_date: datetime, court: int, sport: str, user_id: str, ra: Optional[str], booking_id: str, materials: str):
        if not Booking.validate_dates(start_date, end_date):
            raise EntityError("dates")
        self.start_date = start_date
        self.end_date = end_date

        if not Booking.validate_court(court):
            raise EntityError("court")
        self.court = court

        if not Booking.validate_sport(sport):
            raise EntityError("sport")
        self.sport = sport

        if not Booking.validate_user_id(user_id):
            raise EntityError("user_id")
        self.user_id = user_id

        if not Booking.validate_ra(ra):
            raise EntityError("ra")
        self.ra = ra

        if not Booking.validate_booking_id(booking_id):
            raise EntityError("booking_id")
        self.booking_id = booking_id

        if not Booking.validate_materials(materials):
            raise EntityError("materials")
        self.materials = materials






    @staticmethod
    def validate_dates(start_date: datetime, end_date: datetime) -> bool:
        if not isinstance(start_date, datetime) or not isinstance(end_date, datetime) or start_date >= end_date:
            return False
        return True

    @staticmethod
    def validate_court(court: int) -> bool:
        if not isinstance(court, int) or court < 1 or court > 10:
            return False
        return True

    @staticmethod
    def validate_sport(sport: str) -> bool:
        if not isinstance(sport, str):
            return False
        return True
        

    @staticmethod
    def validate_user_id(user_id: str) -> bool:
        if not isinstance(user_id, str):
            return False
        return True

    @staticmethod
    def validate_ra(ra: Optional[str]) -> bool:
        if ra is not None and not isinstance(ra, str):
            return False
        return True

    @staticmethod   
    def validate_booking_id(booking_id: str) -> bool:
        if not isinstance(booking_id, str):
            return False
        return True

    @staticmethod
    def validate_materials(materials: str) -> bool:
        if not isinstance(materials, str):
            return False
        return True
    
    def to_dict(self):
        return {
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "court": self.court,
            "sport": self.sport,
            "user_id": self.user_id,
            "ra": self.ra,
            "booking_id": self.booking_id,
            "materials": self.materials
        }