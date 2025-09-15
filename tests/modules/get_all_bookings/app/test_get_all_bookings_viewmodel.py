from src.modules.get_all_bookings.app.get_all_bookings_usecase import GetAllBookingsUsecase
from src.modules.get_all_bookings.app.get_all_bookings_viewmodel import GetAllBookingsViewModel
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock
from src.shared.domain.entities.booking import Booking

class Test_GetAllBookingsViewmodel:
    def test_get_all_bookings_viewmodel(self):
        repo = BookingRepositoryMock()
        usecase = GetAllBookingsUsecase(repo = repo)
        bookings = usecase()
        viewmodel = GetAllBookingsViewModel(bookings).to_dict()
        
        expected = {
            'bookings': [
                {
                    'booking': {
                        'start_date': 1634576165000,
                        'end_date': 1634583365000,
                        'court_number': 1,
                        'sport': 'Tennis',
                        'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
                        'booking_id': 'b1d3bebf-dc0d-4fc1-861c-506a40cc2925',
                        'materials': ['Raquete', 'Bola', 'Rede', 'Tenis'],
                        'type': 'Training'
                    }
                },
                {
                    'booking': {
                        'start_date': 1634563800000,
                        'end_date': 1634567400000,
                        'court_number': 2,
                        'sport': 'Football',
                        'user_id': 'c07e0862-3c07-4227-ab0f-511a267cb7ff',
                        'booking_id': 'b2d3bebf-dc0d-4fc1-861c-506a40cc2925',
                        'materials': ['Bola', 'Chuteira'],
                        'type': 'Training'
                    }
                },
                {
                    'booking': {
                        'start_date': 1634569200000,
                        'end_date': 1634571000000,
                        'court_number': 3,
                        'sport': 'Basketball',
                        'user_id': 'd351a9b1-937f-423c-a9d1-9929b5795be1',
                        'booking_id': 'b3d3bebf-dc0d-4fc1-861c-506a40cc2925',
                        'materials': ['Bola'],
                        'type': 'Common'
                    }
                },
                {
                    'booking': {
                        'start_date': 1634574600000,
                        'end_date': 1634578200000,
                        'court_number': 4,
                        'sport': 'Volleyball',
                        'user_id': 'c8435c66-13a4-4641-9d54-773b4b8ccc98',
                        'booking_id': 'b4d3bebf-dc0d-4fc1-861c-506a40cc2925',
                        'materials': ['Bola', 'Rede'],
                        'type': 'Common'
                    }
                },
                {
                    'booking': {
                        'start_date': 1634580000000,
                        'end_date': 1634581800000,
                        'court_number': 5,
                        'sport': 'Handball',
                        'user_id': 'c8435c66-13a4-4641-9d54-773b4b8ccc98',
                        'booking_id': 'b5d3bebf-dc0d-4fc1-861c-506a40cc2925',
                        'materials': ['Bola'],
                        'type': 'Training'
                    }
                },
                {
                    'booking': {
                        'start_date': 1634583600000,
                        'end_date': 1634585400000,
                        'court_number': 5,
                        'sport': 'Futsal',
                        'user_id': 'c8435c66-13a4-4641-9d54-773b4b8ccc98',
                        'booking_id': 'b6d3bebf-dc0d-4fc1-861c-506a40cc2925',
                        'materials': ['Bola', 'Chuteira'],
                        'type': 'Training'
                    }
                },
                {
                    'booking': {
                        'start_date': 1634587200000,
                        'end_date': 1634589000000,
                        'court_number': 5,
                        'sport': 'Rugby',
                        'user_id': 'c8435c66-13a4-4641-9d54-773b4b8ccc98',
                        'booking_id': 'b7d3bebf-dc0d-4fc1-861c-506a40cc2925',
                        'materials': ['Bola', 'Tenis', 'Capacete'],
                        'type': 'Training'
                    }
                },
                {
                    'booking': {
                        'start_date': 1634590800000,
                        'end_date': 1634592600000,
                        'court_number': 5,
                        'sport': 'Ping Pong',
                        'user_id': 'c8435c66-13a4-4641-9d54-773b4b8ccc98',
                        'booking_id': 'b8d3bebf-dc0d-4fc1-861c-506a40cc2925',
                        'materials': ['Raquete', 'Bola'],
                        'type': 'Training'
                    }
                }
            ],
            'message': 'the bookings were retrieved'
        }


        assert viewmodel == expected
