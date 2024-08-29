import pytest
from src.modules.update_court.app.update_court_usecase import UpdateCourtUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.infra.repositories.reservation_repository_mock import ReservationRepositoryMock
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.domain.enums.status_enum import STATUS


class TestUpdateCourtUsecase:
    def test_update_court_usecase(self):
        repo = ReservationRepositoryMock()
        usecase = UpdateCourtUsecase(repo=repo)

        court_number = 1

        court = usecase(
            number=court_number,
            status=STATUS.MAINTENANCE,
            photo="https://super.abril.com.br/mundo-estranho/os-poneis-sao-cavalos-anoes"
        )

        assert repo.get_court(court_number).number == court.number
        assert repo.get_court(court_number).status == court.status
        assert repo.get_court(court_number).photo == court.photo

    def test_update_court_usecase_not_found_number(self):

        repo = ReservationRepositoryMock()
        usecase = UpdateCourtUsecase(repo=repo)

        with pytest.raises(NoItemsFound):
            court = usecase(
                number=9,
                status=STATUS.MAINTENANCE,
                photo="http://foto"
            )

    def test_update_court_usecase_invalid_court_number(self):

        repo = ReservationRepositoryMock()
        usecase = UpdateCourtUsecase(repo=repo)

        with pytest.raises(EntityError):
            court = usecase(
                number=-999,
                status=STATUS.MAINTENANCE,
                photo="https://super.abril.com.br/mundo-estranho/os-poneis-sao-cavalos-anoes"
            )
