import pytest
from src.shared.helpers.errors.domain_errors import EntityError
from src.modules.delete_booking.app.delete_booking_usecase import DeleteBookingUsecase
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock
from src.shared.helpers.errors.usecase_errors import NoItemsFound

class Test_DeleteBookingUsecase:
    def test_delete_booking_usecase(self):
        repo = BookingRepositoryMock()
        usecase = DeleteBookingUsecase(repo=repo)
        len_before = len(repo.bookings)
        
        booking = usecase(booking_id='b1d3bebf-dc0d-4fc1-861c-506a40cc2925',
                          user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98')
        assert len(repo.bookings) == len_before - 1

    def test_delete_booking_usecase_no_items_found(self):
        repo = BookingRepositoryMock()
        usecase = DeleteBookingUsecase(repo=repo)
        with pytest.raises(NoItemsFound):
            booking = usecase(booking_id='b1d3bebf-dc0d-4fc1-861c-506a40cc2926',
                              user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98')

    def test_delete_booking_usecase_invalid_booking_id(self):
        repo = BookingRepositoryMock()
        usecase = DeleteBookingUsecase(repo=repo)
    
        with pytest.raises(EntityError):
            usecase(booking_id=-1,
                    user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98')
    
        with pytest.raises(EntityError):
            usecase(booking_id=None,
                    user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98')