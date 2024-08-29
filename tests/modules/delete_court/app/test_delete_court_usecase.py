import pytest
from typing import Any, Optional
from src.shared.domain.entities.court import Court
from src.shared.domain.enums.status_enum import STATUS
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.helpers.errors.domain_errors import EntityError
from src.modules.delete_court.app.delete_court_usecase import DeleteCourtUsecase
from src.shared.infra.repositories.reservation_repository_mock import ReservationRepositoryMock
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.domain.repositories.reservation_repository_interface import IReservationRepository

class Test_DeleteCourtUsecase:
    def test_delete_court_usecase(self):
        repo = ReservationRepositoryMock()
        usecase = DeleteCourtUsecase(repo=repo)
        len_before = len(repo.courts)
        
        court = usecase(number=1)
        assert len(repo.courts) == len_before - 1
        assert court.number == 1

    def test_delete_court_usecase_no_items_found(self):
        repo = ReservationRepositoryMock()
        usecase = DeleteCourtUsecase(repo=repo)
        with pytest.raises(NoItemsFound):
            court = usecase(number=10)

    def test_delete_court_usecase_invalid_number(self):
        repo = ReservationRepositoryMock()
        usecase = DeleteCourtUsecase(repo=repo)
    
        with pytest.raises(EntityError):
            usecase(number=-1)
    
        with pytest.raises(EntityError):
            usecase(number=None)

    