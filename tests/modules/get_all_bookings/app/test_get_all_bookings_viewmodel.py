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
                        'sport': 'Tenis Mesa',
                        'booking_id': 'b8d3bebf-dc0d-4fc1-861c-506a40cc2925',
                        'materials': ['Raquete', 'Bola'],
                        'type': 'Training'
                    }
                }
            ],
            'message': 'the bookings were retrieved'
        }


        assert viewmodel == expected
