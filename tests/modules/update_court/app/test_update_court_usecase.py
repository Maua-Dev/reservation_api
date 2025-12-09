import pytest
from src.modules.update_court.app.update_court_usecase import UpdateCourtUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.infra.repositories.reservation_repository_mock import ReservationRepositoryMock
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction
from src.shared.domain.enums.status_enum import STATUS


class TestUpdateCourtUsecase:
    def test_update_court_usecase(self):
        repo = ReservationRepositoryMock()
        usecase = UpdateCourtUsecase(repo=repo)

        court_number = 1

        court = usecase(
            number=court_number,
            status=STATUS.MAINTENANCE,
            photo="https://super.abril.com.br/mundo-estranho/os-poneis-sao-cavalos-anoes",
            role="ADMIN"
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
                photo="http://foto",
                role="ADMIN"   
            )

    def test_update_court_usecase_invalid_court_number(self):

        repo = ReservationRepositoryMock()
        usecase = UpdateCourtUsecase(repo=repo)

        with pytest.raises(EntityError):
            court = usecase(
                number=-999,
                status=STATUS.MAINTENANCE,
                photo="https://super.abril.com.br/mundo-estranho/os-poneis-sao-cavalos-anoes",
                role="ADMIN" 
            )

    def test_update_court_usecase_court_number_not_found(self):

        repo = ReservationRepositoryMock()
        usecase = UpdateCourtUsecase(repo=repo)

        with pytest.raises(NoItemsFound):
            court = usecase(
                number=9,
                status=STATUS.MAINTENANCE,
                photo="https://super.abril.com.br/mundo-estranho/os-poneis-sao-cavalos-anoes",
                role="ADMIN" 
            )
            
    def test_update_court_usecase_not_admin(self):
        
        repo = ReservationRepositoryMock()
        usecase = UpdateCourtUsecase(repo=repo)
        
        with pytest.raises(ForbiddenAction):
            court = usecase(
                number=1,
                status=STATUS.MAINTENANCE,
                photo="https://super.abril.com.br/mundo-estranho/os-poneis-sao-cavalos-anoes",
                role="STUDENT" 
            )
