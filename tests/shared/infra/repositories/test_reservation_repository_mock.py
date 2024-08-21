from src.shared.infra.repositories.reservation_repository_mock import ReservationRepositoryMock
from src.shared.domain.enums.status_enum import STATUS
from src.shared.domain.entities.court import Court

class TestReservationRepositoryMock:
    def test_create_court(self):
        repo_mock = ReservationRepositoryMock()
        new_court = Court(number = 6, status = STATUS.MAINTENANCE, is_field= False, photo = None)
        len_before = len(repo_mock.courts)

        response = repo_mock.create_court(new_court)
        assert len(repo_mock.courts) == len_before + 1
        assert response == new_court



    