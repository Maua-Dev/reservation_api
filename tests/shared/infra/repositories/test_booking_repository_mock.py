from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock
from src.shared.domain.enums.sport import SPORT
from src.shared.domain.entities.booking import Booking


class TestBookingRepositoryMock:
    def test_create_booking(self):
        repo_mock = BookingRepositoryMock()
        new_booking = Booking(start_date=1634576165000, end_date=1634583365000, court_number=1,sport=SPORT.TENNIS, user_id='c8435c66-13a4-4641-9d54-773b4b8ccd09', booking_id='c2d3bebf-dc0d-4fc1-861c-506a40cc2036', materials=['Raquete', 'Bola', 'Rede', 'Tenis'])
        len_before = len(repo_mock.bookings)

        response = repo_mock.create_booking(new_booking)
        assert len(repo_mock.bookings) == len_before + 1
        assert response == new_booking

    def test_update_booking(self):
        booking_id = 'c2d3bebf-dc0d-4fc1-861c-506a40cc2925'

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
        booking_id = 'c2d3bebf-dc0d-4fc1-861c-506a40cc2925'

        booking = repo_mock.get_booking(booking_id)

        assert booking is not None
        assert booking.booking_id == booking_id
        assert booking.user_id == 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
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