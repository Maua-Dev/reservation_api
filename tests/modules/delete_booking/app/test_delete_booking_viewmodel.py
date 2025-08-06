from src.modules.delete_booking.app.delete_booking_viewmodel import DeleteBookingViewModel
from src.modules.delete_booking.app.delete_booking_usecase import DeleteBookingUsecase
from src.shared.domain.entities.booking import Booking
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock


class Test_DeleteBookingViewModel:
    def test_delete_booking_viewmodel(self):
        repo = BookingRepositoryMock()
        usecase = DeleteBookingUsecase(repo=repo)
        user = {
            'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
            'name': 'Nome',
            'email': 'user@email.com',
            'role': 'STUDENT'
        }
        booking = usecase(booking_id=repo.bookings[0].booking_id, user=user)
        viewmodel = DeleteBookingViewModel(booking=booking).to_dict()

        expected = {
            'booking': {
                'start_date': 1634576165000,
                'end_date': 1634583365000,
                'court_number': 1,
                'sport': 'Tennis',
                'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
                'booking_id': 'b1d3bebf-dc0d-4fc1-861c-506a40cc2925',
                'materials': ['Raquete', 'Bola', 'Rede', 'Tenis']
            },
            'message': 'the booking was deleted'
        }

        assert viewmodel == expected