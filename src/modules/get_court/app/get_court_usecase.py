from src.shared.domain.entities.court import Court
from src.shared.domain.repositories.reservation_repository_interface import IReservationRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class GetCourtUsecase:
    repo: IReservationRepository

    def __init__(self, repo: IReservationRepository):
        self.repo = repo
    
    def __call__ (self, number: int):
        if not Court.validate_number(number):
            raise EntityError('number')
        
        court = self.repo.get_court(number = number)

        if court is None:
            raise NoItemsFound('court not found')
        
        return court