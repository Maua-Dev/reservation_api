from src.shared.domain.repositories.reservation_repository_interface import IReservationRepository

class GetAllCourtsUsecase:
    def __init__(self, repo: IReservationRepository):
        self.repo = repo

    def __call__(self):

        courts = self.repo.get_all_courts()
        
        return courts