from typing import Any, Optional
from src.shared.domain.entities.court import Court
from src.shared.domain.enums.status_enum import STATUS
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.domain.repositories.reservation_repository_interface import IReservationRepository

class DeleteCourtUsecase:
    def __init__(self, repo:IReservationRepository):
        self.repo = repo
    
    def __call__(self, number: int):    
        
        if not Court.validate_number(number):
            raise EntityError('number')
        
        court = self.repo.delete_court(number=number)
        
        if court is None:
            raise NoItemsFound('court')
        
        return court