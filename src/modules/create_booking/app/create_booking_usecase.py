from datetime import timedelta
import uuid
from typing import List

from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.sport import SPORT
from src.shared.domain.enums.type import BOOKING_TYPE
from src.shared.domain.repositories.booking_repository_interface import IBookingRepository
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, InvalidSchedule, InvalidSchedulePeriod


class CreateBookingUsecase:
    start_date: int
    end_date: int
    court_number: int
    sport: SPORT
    user_id: str
    booking_id: str
    materials: List[str]
    booking_type: BOOKING_TYPE

    def __init__(self, repo: IBookingRepository):
        self.repo = repo

    def __call__(self,
                 start_date: int,
                 end_date: int,
                 court_number: int,
                 sport: str,
                 user_id: str,
                 materials: List[str],
                 booking_type: str
                 ) -> Booking:

        booking_id = str(uuid.uuid4())

        if self.repo.get_booking(booking_id):
            raise DuplicatedItem("Booking already exists")

        try:
            self.sport = SPORT(sport)
        except ValueError:
            raise ValueError("Invalid sport enum value")

        for material in materials:
            if not isinstance(material, str):
                raise ValueError("Invalid material type")
        
        
        if booking_type not in [type.value for type in BOOKING_TYPE]:
            raise ValueError("Invalid type enum value")

        self.booking_type = BOOKING_TYPE(booking_type)

        maxtime = start_date + (timedelta(weeks=12).total_seconds()*1000)
        if(end_date > maxtime):
            raise InvalidSchedulePeriod()

        all_bookings = self.repo.get_all_bookings()

        for booking in all_bookings:
            if (
                booking.court_number == court_number
                and not (end_date <= booking.start_date or start_date >= booking.end_date)
            ):
                raise InvalidSchedule()

        resp = self.repo.create_booking(Booking(start_date,
                                                end_date,
                                                court_number,
                                                self.sport,
                                                user_id,
                                                booking_id,
                                                materials,
                                                self.booking_type))

        return resp



