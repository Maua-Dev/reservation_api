from typing import Any, Optional
from src.shared.domain.entities.court import Court
from src.shared.domain.enums.status_enum import STATUS
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.domain.repositories.reservation_repository_interface import IReservationRepository

class CreateCourtUsecase:
    def __init__(self, repo: IReservationRepository):
        self.repo = repo

    def __call__(self, number: int, status: STATUS, is_field: bool, photo: Optional[str] = None):

        if self.repo.get_court(number) is not None:
            raise DuplicatedItem('number')

        court = Court(
            number = number,
            status = status,
            is_field = is_field,
            photo = photo
        )

        return self.repo.create_court(court)
        