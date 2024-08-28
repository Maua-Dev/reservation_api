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
        courtAnumber = 1
        courtBnumber = 2
        repo_mock = ReservationRepositoryMock()

        courtA = repo_mock.update_court(number=courtAnumber,
                                        status=STATUS.UNAVAILABLE,
                                        photo='test string1')

        assert repo_mock.get_court(courtAnumber).number == courtA.number
        assert repo_mock.get_court(courtAnumber).status == courtA.status
        assert repo_mock.get_court(courtAnumber).is_field == courtA.is_field
        assert repo_mock.get_court(courtAnumber).photo == courtA.photo

        courtB = repo_mock.update_court(number=courtBnumber,
                                        status=STATUS.MAINTENANCE,
                                        photo='test string')

        assert repo_mock.get_court(courtBnumber).number == courtB.number
        assert repo_mock.get_court(courtBnumber).status == courtB.status
        assert repo_mock.get_court(courtBnumber).is_field == courtB.is_field
        assert repo_mock.get_court(courtBnumber).photo == courtB.photo
