from typing import Any, Optional
from src.shared.domain.enums.status_enum import STATUS
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.domain.repositories.reservation_repository_interface import IReservationRepository


class UpdateCourtUsecase:
    def __init__(self, repo: IReservationRepository):
        self.repo = repo

    def __call__(self,
                 number: int,
                 status: STATUS = None,
                 photo: str = None):

        if number < 0 or number > 10:
            raise EntityError('number')

        if self.repo.get_court(number) is None:
            raise NoItemsFound(f'number: {number}')

        court = self.repo.update_court(number=number,
                                       status=status,
                                       photo=photo)

        return court
