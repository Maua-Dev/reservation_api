import pytest
from typing import Any, Optional
from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.status_enum import STATUS
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.helpers.errors.domain_errors import EntityError
from src.modules.delete_booking.app.delete_booking_usecase import DeleteBookingUsecase
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.domain.repositories.booking_repository_interface import IBookingRepository

class Test_DeleteBookingUsecase:
    def test_delete_booking_usecase(self):
        repo = BookingRepositoryMock()
        usecase = DeleteBookingUsecase(repo=repo)
        len_before = len(repo.bookings)
        
        booking = usecase(booking_id='b1d3bebf-dc0d-4fc1-861c-506a40cc2925')
        assert len(repo.bookings) == len_before - 1

    def test_delete_booking_usecase_no_items_found(self):
        repo = BookingRepositoryMock()
        usecase = DeleteBookingUsecase(repo=repo)
        with pytest.raises(NoItemsFound):
            booking = usecase(booking_id='b1d3bebf-dc0d-4fc1-861c-506a40cc2926')

    def test_delete_booking_usecase_invalid_booking_id(self):
        repo = BookingRepositoryMock()
        usecase = DeleteBookingUsecase(repo=repo)
    
        with pytest.raises(EntityError):
            usecase(booking_id=-1)
    
        with pytest.raises(EntityError):
            usecase(booking_id=None)