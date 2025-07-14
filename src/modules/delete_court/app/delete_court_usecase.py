from src.shared.domain.entities.court import Court
from src.shared.domain.enums.status_enum import STATUS
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction
from src.shared.domain.repositories.reservation_repository_interface import IReservationRepository

class DeleteCourtUsecase:
    def __init__(self, repo:IReservationRepository):
        self.repo = repo
    
    def __call__(self, number: int, role: str):    
        
        if not Court.validate_number(number):
            raise EntityError('number')
        
        if role != "ADMIN":
            raise ForbiddenAction("user, only admin can delete courts")
        
        court = self.repo.delete_court(number=number)
        
        if court is None:
            raise NoItemsFound('court')
        
        return court