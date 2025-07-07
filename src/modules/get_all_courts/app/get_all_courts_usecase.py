from typing import Any
from src.shared.domain.repositories.reservation_repository_interface import IReservationRepository
from src.shared.domain.entities.court import Court

class GetAllCourtsUsecase:
    def __init__(self, repo: IReservationRepository):
        self.repo = repo

    def __call__(self):

        courts = self.repo.get_all_courts()
        
        return courts