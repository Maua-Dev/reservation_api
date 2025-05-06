from src.modules.get_bookings.app.get_bookings_viewmodel import GetBookingsViewmodel
from src.modules.get_bookings.app.get_bookings_usecase import GetBookingsUseCase
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock

class Test_GetBookingsViewModel:
    def test_get_bookings_viewmodel(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingsUseCase(repo)
        booking = usecase(booking_id= repo.bookings[0].booking_id)

        viewmodel = GetBookingsViewmodel(booking = booking).to_dict()

        expected = {
            'booking': {
                'start_date': 1634576165000,
                'end_date': 1634583365000,
                'court_number': 1,
                'sport': 'Tennis',
                'user_id': 'c8435c66-13a4-4641-9d54-773b4b8ccc98',
                'booking_id': 'b1d3bebf-dc0d-4fc1-861c-506a40cc2925',
                'materials': ['Raquete', 'Bola', 'Rede', 'Tenis']
            },
            'message': 'the booking was retrieved'  
        }

        assert viewmodel == expected