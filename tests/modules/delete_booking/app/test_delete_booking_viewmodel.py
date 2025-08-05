from src.modules.delete_booking.app.delete_booking_viewmodel import DeleteBookingViewModel
from src.modules.delete_booking.app.delete_booking_usecase import DeleteBookingUsecase
from src.shared.domain.entities.booking import Booking
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock


class Test_DeleteBookingViewModel:
    def test_delete_booking_viewmodel(self):
        repo = BookingRepositoryMock()
        usecase = DeleteBookingUsecase(repo=repo)
<<<<<<< HEAD:tests/modules/delete_bookings/app/test_delete_booking_viewmodel.py
        user = {
            'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
            'name': 'Nome',
            'email': 'user@email.com',
            'role': 'STUDENT'
        }
        booking = usecase(booking_id=repo.bookings[0].booking_id, user=user)
=======
        booking = usecase(booking_id=repo.bookings[0].booking_id,
                          user_id=repo.bookings[0].user_id)
>>>>>>> parent of 86c13e0 (Merge pull request #20 from Maua-Dev/user-on-generate-report):tests/modules/delete_booking/app/test_delete_booking_viewmodel.py
        viewmodel = DeleteBookingViewModel(booking=booking).to_dict()

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
            'message': 'the booking was deleted'
        }

        assert viewmodel == expected