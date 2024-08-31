from src.modules.get_court.app.get_court_viewmodel import GetCourtViewmodel
from src.modules.get_court.app.get_court_usecase import GetCourtUsecase
from src.shared.infra.repositories.reservation_repository_mock import ReservationRepositoryMock


class Test_GetCourtViewModel:
    def test_get_court_viewmodel(self):
        repo = ReservationRepositoryMock()
        usecase = GetCourtUsecase(repo=repo)
        court = usecase(number=repo.courts[0].number)
        viewmodel = GetCourtViewmodel(court=court).to_dict()

        expected = {
            'court': {
                'number': 1,
                'status': 'AVAILABLE',
                'is_field': False,
                'photo': 'https://www.linkedin.com/in/giovanna-albuquerque-16917a245/'
            },
            'message': 'the court was retrieved'
        }

        assert viewmodel == expected