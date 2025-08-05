from src.modules.get_all_bookings.app.get_all_bookings_usecase import GetAllBookingsUsecase
from src.modules.get_all_bookings.app.get_all_bookings_viewmodel import GetAllBookingsViewModel
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock
from src.shared.domain.entities.booking import Booking

class Test_GetAllBookingsViewmodel:
    def test_get_all_bookings_viewmodel(self):
        repo = BookingRepositoryMock()
        usecase = GetAllBookingsUsecase(repo = repo)
        courts = usecase()
        viewmodel = GetAllBookingsViewModel(courts).to_dict()
        
        excepted = {
            'courts': [
                {
                    'start_date': 1634576165000,
                    'end_date': 1634583365000,
                    'court_number': 1,
                    'sport': 'TENNIS',
                    'user_id': 'c8435c66-13a4-4641-9d54-773b4b8ccc98',
                    'booking_id': 'b1d3bebf-dc0d-4fc1-861c-506a40cc2925',
                    'materials': ['Raquete', 'Bola', 'Rede', 'Tenis']
                },
                {
                    'start_date': 1634563800000,
                    'end_date': 1634567400000,
                    'court_number': 2,
                    'sport': 'FOOTBALL',
                    'user_id': 'c8435c66-13a4-4641-9d54-773b4b8ccc98',
                    'booking_id': 'b2d3bebf-dc0d-4fc1-861c-506a40cc2925',
                    'materials': ['Bola', 'Chuteira']
                },
                {
                    'start_date': 1634569200000,
                    'end_date': 1634571000000,
                    'court_number': 3,
                    'sport': 'BASKETBALL',
                    'user_id': 'c8435c66-13a4-4641-9d54-773b4b8ccc98',
                    'booking_id': 'b3d3bebf-dc0d-4fc1-861c-506a40cc2925',
                    'materials': ['Bola']
                },
                {
                    'start_date': 1634574600000,
                    'end_date': 1634578200000,
                    'court_number': 4,
                    'sport': 'VOLLEYBALL',
                    'user_id': 'c8435c66-13a4-4641-9d54-773b4b8ccc98',
                    'booking_id': 'b4d3bebf-dc0d-4fc1-861c-506a40cc2925',
                    'materials': ['Bola', 'Rede']
                },
                {
                    'start_date': 1634580000000,
                    'end_date': 1634581800000,
                    'court_number': 5,
                    'sport': 'HANDBALL',
                    'user_id': 'c8435c66-13a4-4641-9d54-773b4b8ccc98',
                    'booking_id': 'b5d3bebf-dc0d-4fc1-861c-506a40cc2925',
                    'materials': ['Bola']
                }
            ],
            'message': 'the bookings were retrieved'

        }