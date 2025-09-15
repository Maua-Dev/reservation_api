from src.modules.get_booking.app.get_booking_viewmodel import GetBookingViewmodel
from src.modules.get_booking.app.get_booking_usecase import GetBookingUseCase
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock

class Test_GetBookingViewModel:
    def test_get_booking_viewmodel(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingUseCase(repo)
        booking = usecase(booking_id= repo.bookings[0].booking_id)

        viewmodel = GetBookingViewmodel(booking = booking).to_dict()

        expected = {
            'booking': {
                'start_date': 1634576165000,
                'end_date': 1634583365000,
                'court_number': 1,
                'sport': 'Tennis',
                'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
                'booking_id': 'b1d3bebf-dc0d-4fc1-861c-506a40cc2925',
                'materials': ['Raquete', 'Bola', 'Rede', 'Tenis'],
                'type': 'Training'
            },
            'message': 'the booking was retrieved'  
        }

        assert viewmodel == expected