from typing import Any, Optional
from src.shared.domain.enums.status_enum import STATUS
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.domain.repositories.reservation_repository_interface import IReservationRepository


class UpdateCourtUsecase:
    def __init__(self, repo: IReservationRepository):
        self.repo = repo

    def __call__(self,
                 number: int,
                 status: STATUS = None,
                 is_field: bool = None,
                 photo: str = None):

        if self.repo.get_court(number) is None:
            raise NoItemsFound(f'court number: {number} was not found')

        court = self.repo.update_court(number=number,
                                       status=status,
                                       is_field=is_field,
                                       photo=photo)

        return court
