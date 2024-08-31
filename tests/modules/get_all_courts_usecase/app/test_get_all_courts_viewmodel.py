from src.modules.get_all_courts.app.get_all_courts_usecase import GetAllCourtsUsecase
from src.modules.get_all_courts.app.get_all_courts_viewmodel import GetAllCourtsViewModel
from src.shared.infra.repositories.reservation_repository_mock import ReservationRepositoryMock
from src.shared.domain.entities.court import Court

class Test_GetAllCourtsViewmodel:
    def test_get_all_courts_viewmodel(self):
        repo = ReservationRepositoryMock()
        usecase = GetAllCourtsUsecase(repo = repo)
        courts = usecase()
        viewmodel = GetAllCourtsViewModel(courts).to_dict()
        
        excepted = {
            'courts': [
                {
                    'number': 1,
                    'status': 'AVAILABLE',
                    'is_field': False,
                    'photo': 'https://www.linkedin.com/in/giovanna-albuquerque-16917a245/'
                },
                {
                    'number': 2,
                    'status': 'AVAILABLE',
                    'is_field': False,
                    'photo': 'https://www.linkedin.com/in/giovanna-albuquerque-16917a245/'
                },
                {
                    'number': 3,
                    'status': 'UNAVAILABLE',
                    'is_field': False,
                    'photo': 'https://super.abril.com.br/mundo-estranho/os-poneis-sao-cavalos-anoes'
                },
                {
                    'number': 4,
                    'status': 'MAINTENANCE',
                    'is_field': True,
                    'photo': None
                },
                {
                    'number': 5,
                    'status': 'AVAILABLE',
                    'is_field': False,
                    'photo': 'https://www.linkedin.com/in/vinicius-berti-a80354209/'
                }
            ],
            'message': 'the courts were retrieved'

        }
        
