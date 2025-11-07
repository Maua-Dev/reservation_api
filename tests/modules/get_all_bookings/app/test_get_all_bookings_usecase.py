from src.modules.get_all_bookings.app.get_all_bookings_usecase import GetAllBookingsUsecase
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock
from src.shared.domain.enums.sport import SPORT
from src.shared.domain.entities.booking import Booking
import pytest

class TestGetAllBookingsUsecase:
    def test_get_all_bookings_usecase(self):
        repo = BookingRepositoryMock()
        usecase = GetAllBookingsUsecase(repo = repo)
        bookings = usecase()
        
        assert len(bookings) == 8
        assert bookings[0].court_number == 1
        assert bookings[0].start_date == 1634576165000
        assert bookings[0].end_date == 1634583365000
        assert bookings[0].sport == SPORT.TENNIS
        assert bookings[0].user_id == '1f25448b-3429-4c19-8287-d9e64f17bc3a'
        assert bookings[0].booking_id == 'b1d3bebf-dc0d-4fc1-861c-506a40cc2925'
        assert bookings[0].materials == ['Raquete', 'Bola', 'Rede', 'Tenis']