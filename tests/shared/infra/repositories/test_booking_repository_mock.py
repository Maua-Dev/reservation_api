from src.shared.domain.enums.type import BOOKING_TYPE
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock
from src.shared.domain.enums.sport import SPORT
from src.shared.domain.entities.booking import Booking


class TestBookingRepositoryMock:
    def test_create_booking(self):
        repo_mock = BookingRepositoryMock()
        new_booking = Booking(start_date=1634576165000, end_date=1634583365000, court_number=1,sport=SPORT.TENNIS, user_id='c8435c66-13a4-4641-9d54-773b4b8ccd09', booking_id='c2d3bebf-dc0d-4fc1-861c-506a40cc2036', materials=['Raquete', 'Bola', 'Rede', 'Tenis'], booking_type=BOOKING_TYPE.TRAINING)
        len_before = len(repo_mock.bookings)

        response = repo_mock.create_booking(new_booking)
        assert len(repo_mock.bookings) == len_before + 1
        assert response == new_booking

    def test_update_booking(self):
        booking_id = 'b1d3bebf-dc0d-4fc1-861c-506a40cc2925'

        repo_mock = BookingRepositoryMock()

        updated_booking = repo_mock.update_booking(
            booking_id=booking_id,
            start_date=1634600000000,  
            end_date=1634603600000,  
            court_number=10,  
            sport=SPORT.BASKETBALL  
        )

        assert updated_booking is not None
        assert repo_mock.get_booking(booking_id).start_date == updated_booking.start_date
        assert repo_mock.get_booking(booking_id).end_date == updated_booking.end_date
        assert repo_mock.get_booking(booking_id).court_number == updated_booking.court_number
        assert repo_mock.get_booking(booking_id).sport == updated_booking.sport

    def test_get_booking(self):
        repo_mock = BookingRepositoryMock()
        booking_id = 'b1d3bebf-dc0d-4fc1-861c-506a40cc2925'

        booking = repo_mock.get_booking(booking_id)

        assert booking is not None
        assert booking.booking_id == booking_id
        assert booking.user_id == '1f25448b-3429-4c19-8287-d9e64f17bc3a'
        assert booking.sport == SPORT.TENNIS
        assert booking.court_number == 1
        assert booking.start_date == 1634576165000
        assert booking.end_date == 1634583365000
        assert booking.materials == ['Raquete', 'Bola', 'Rede', 'Tenis']
        
    def test_get_all_bookings(self):
        repo_mock = BookingRepositoryMock()
        bookings = repo_mock.get_all_bookings()

        assert len(bookings) == len(repo_mock.bookings)
        assert isinstance(bookings, list)
        assert all(isinstance(booking, Booking) for booking in bookings)

    def test_delete_booking(self):
        repo_mock = BookingRepositoryMock()
        booking_id = 'b1d3bebf-dc0d-4fc1-861c-506a40cc2925'
        user = {
            'user_id': 'd351a9b1-937f-423c-a9d1-9929b5795be1',
            'email': 'user@email.com',
            'role': 'ADMIN'
        }

        len_before = len(repo_mock.bookings)
        deleted_booking = repo_mock.delete_booking(booking_id, user)
        len_after = len(repo_mock.bookings)

        assert deleted_booking is not None
        assert len_after == len_before - 1
        assert repo_mock.get_booking(booking_id) is None
