from src.modules.get_all_courts.app.get_all_courts_usecase import GetAllCourtsUsecase
from src.shared.infra.repositories.reservation_repository_mock import ReservationRepositoryMock
from src.shared.domain.entities.court import Court
import pytest

class Test_GetAllCourtsUsecase:
    def test_get_all_courts_usecase(self):
        repo = ReservationRepositoryMock()
        usecase = GetAllCourtsUsecase(repo = repo)
        courts = usecase()
        
        assert len(courts) == 5
        assert courts[0].number == 1