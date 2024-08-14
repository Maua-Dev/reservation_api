import pytest
from src.modules.create_court.app.create_court_usecase import CreateCourtUsecase
from src.shared.infra.repositories.reservation_repository_mock import ReservationRepositoryMock
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.domain.enums.status_enum import STATUS

class TestCreateCourtUsecase:
    def test_create_court_usecase(self):
        repo = ReservationRepositoryMock()
        usecase = CreateCourtUsecase(repo=repo)
        
        court  = usecase(
            number= 8,
            status= STATUS.AVAILABLE, 
            is_field= False,
            photo = "https://super.abril.com.br/mundo-estranho/os-poneis-sao-cavalos-anoes"
        )

        assert repo.courts[-1] == court
        assert court.photo == "https://super.abril.com.br/mundo-estranho/os-poneis-sao-cavalos-anoes"
        assert court.number == 8
        assert court.status == STATUS.AVAILABLE
        assert court.is_field == False

        
    def test_create_court_usecase_duplicated_item(self):
        repo = ReservationRepositoryMock()
        usecase = CreateCourtUsecase(repo=repo)

        with pytest.raises(DuplicatedItem):
            court = usecase(number= 2, status= STATUS.AVAILABLE, is_field= False, photo = None)

    def test_create_court_usecase_no_photo(self):
        repo = ReservationRepositoryMock()
        Usecase = CreateCourtUsecase(repo=repo)
        
        court = Usecase(
            number= 7, 
            status= STATUS.UNAVAILABLE, 
            is_field = False, 
            photo = None 
        )
        assert court.photo is None
        assert repo.courts[-1] == court
        assert court.number == 7
        
        
        