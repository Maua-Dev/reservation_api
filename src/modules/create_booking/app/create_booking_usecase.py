from typing import List

from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.sport import SPORT
from src.shared.domain.repositories.booking_repository_interface import IBookingRepository
from src.shared.helpers.errors.usecase_errors import DuplicatedItem


class CreateBookingUsecase:
    start_date: int
    end_date: int
    court_number: int
    sport: SPORT
    user_id: str
    booking_id: str
    materials: List[str]

    def __init__(self, repo: IBookingRepository):
        self.repo = repo

    def __call__(self,
                 start_date: int,
                 end_date: int,
                 court_number: int,
                 sport: str,
                 user_id: str,
                 booking_id: str,
                 materials: List[str]
                 ) -> Booking:

        if self.repo.get_booking(booking_id):
            raise DuplicatedItem("Booking already exists")

        try:
            self.sport = SPORT(sport)
        except ValueError:
            raise ValueError("Invalid sport enum value")

        for material in materials:
            if not isinstance(material, str):
                raise ValueError("Invalid material type")

        resp = self.repo.create_booking(Booking(start_date, end_date, court_number, self.sport, user_id, booking_id, materials))

        return resp



