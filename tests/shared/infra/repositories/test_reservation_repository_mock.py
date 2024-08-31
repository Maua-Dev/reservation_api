from src.shared.infra.repositories.reservation_repository_mock import ReservationRepositoryMock
from src.shared.domain.enums.status_enum import STATUS
from src.shared.domain.entities.court import Court


class TestReservationRepositoryMock:
    def test_create_court(self):
        repo_mock = ReservationRepositoryMock()
        new_court = Court(number=6, status=STATUS.MAINTENANCE, is_field=False, photo=None)
        len_before = len(repo_mock.courts)

        response = repo_mock.create_court(new_court)
        assert len(repo_mock.courts) == len_before + 1
        assert response == new_court

    def test_update_court(self):
        court_number = 1

        repo_mock = ReservationRepositoryMock()

        court = repo_mock.update_court(number=court_number,
                                        status=STATUS.UNAVAILABLE,
                                        photo='test string1')

        assert repo_mock.get_court(court_number).number == court.number
        assert repo_mock.get_court(court_number).status == court.status
        assert repo_mock.get_court(court_number).is_field == court.is_field
        assert repo_mock.get_court(court_number).photo == court.photo

    def test_get_court(self):
        repo_mock = ReservationRepositoryMock()
        court_number = 1
        court = repo_mock.get_court(court_number)
        
    def test_get_all_courts(self):
        repo = ReservationRepositoryMock()
        courts = repo.get_all_courts()

        assert len(courts) == 5


        assert court.number == court_number
        assert court.status == STATUS.AVAILABLE
        assert court.is_field == False
        assert court.photo == 'https://www.linkedin.com/in/giovanna-albuquerque-16917a245/'
