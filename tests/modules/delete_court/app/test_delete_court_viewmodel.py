from src.modules.delete_court.app.delete_court_viewmodel import DeleteCourtViewModel
from src.modules.delete_court.app.delete_court_usecase import DeleteCourtUsecase
from src.shared.domain.entities.court import Court
from src.shared.infra.repositories.reservation_repository_mock import ReservationRepositoryMock


class Test_DeleteCourtViewModel:
    def test_delete_court_viewmodel(self):
        repo = ReservationRepositoryMock()
        usecase = DeleteCourtUsecase(repo=repo)
        court = usecase(number=repo.courts[0].number)
        viewmodel = DeleteCourtViewModel(court=court).to_dict()

        expected = {
            'court': {
                'number': 1,
                'status': 'AVAILABLE',
                'is_field': False,
                'photo': 'https://www.linkedin.com/in/giovanna-albuquerque-16917a245/'
            },
            'message': 'the court was deleted'
        }

        assert viewmodel == expected