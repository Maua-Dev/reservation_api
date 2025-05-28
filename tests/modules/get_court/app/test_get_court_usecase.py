import pytest

from src.modules.get_court.app.get_court_usecase import GetCourtUsecase
from src.shared.infra.repositories.reservation_repository_mock import ReservationRepositoryMock
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.errors.domain_errors import EntityError




class TestGetCourtUseCase:
    
    def test_get_court_usecase(self):
        repo = ReservationRepositoryMock()
        usecase = GetCourtUsecase(repo=repo)
        first_court = repo.courts[0].number
        response = usecase(first_court)

        assert response == repo.courts[0]

    def test_get_court_usecase_invalid_number(self):
        with pytest.raises(EntityError):
            repo = ReservationRepositoryMock()
            usecase = GetCourtUsecase(repo = repo)
            response =  usecase(1000)

    def test_get_court_usecase_no_items_found(self):
        with pytest.raises(NoItemsFound):
            repo = ReservationRepositoryMock()
            usecase = GetCourtUsecase(repo = repo)
            response = usecase(9)
            
            
            


        


        










