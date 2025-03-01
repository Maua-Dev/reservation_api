from src.modules.get_all_bookings.app.get_all_bookings_usecase import GetAllBookingsUsecase
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock
from src.shared.domain.entities.booking import Booking
import pytest

class Test_GetAllBookingsUsecase:
    def test_get_all_bookings_usecase(self):
        repo = BookingRepositoryMock()
        usecase = GetAllBookingsUsecase(repo = repo)
        bookings = usecase()
        
        assert len(bookings) == 8
        assert bookings[0].court_number == 1