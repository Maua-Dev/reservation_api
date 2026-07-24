import pytest

from src.modules.get_bookings.app.get_bookings_usecase import GetBookingsUseCase
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound

class TestGetBookingsUseCase:
    def test_get_bookings_usecase(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingsUseCase(repo=repo)
        booking_id = repo.bookings[0].booking_id
        response = usecase(booking_id=booking_id)

        assert response['bookings'][0] == repo.bookings[0]
        assert response['owner'] == []
    
    def test_get_bookings_usecase_invalid_id(self):
        with pytest.raises(EntityError):
            repo = BookingRepositoryMock()
            usecase = GetBookingsUseCase(repo=repo)
            usecase(booking_id='invalid_id')
    
    def test_get_bookings_usecase_no_items_found(self):
        with pytest.raises(NoItemsFound):
            repo = BookingRepositoryMock()
            usecase = GetBookingsUseCase(repo=repo)
            usecase(booking_id='b3d3b3b3-dc0d-4fc1-861c-506a40cc2925')