import pytest
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, ForbiddenAction
from src.modules.delete_booking.app.delete_booking_usecase import DeleteBookingUsecase
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.errors.domain_errors import EntityError

class Test_DeleteBookingUsecase:
    def test_delete_booking_usecase(self):
        repo = BookingRepositoryMock()
        usecase = DeleteBookingUsecase(repo=repo)
        len_before = len(repo.bookings)
        user = {
            'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
            'name': 'Nome',
            'email': 'user@email.com',
            'role': 'STUDENT'
        }
    
        booking = usecase(booking_id='b1d3bebf-dc0d-4fc1-861c-506a40cc2925',
                          user=user)
        
        assert len(repo.bookings) == len_before - 1

    def test_delete_booking_usecase_admin(self):
        repo = BookingRepositoryMock()
        usecase = DeleteBookingUsecase(repo=repo)
        len_before = len(repo.bookings)
        user = {
            'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
            'name': 'Nome',
            'email': 'user@email.com',
            'role': 'STUDENT'
        }
        
        booking = usecase(booking_id='b1d3bebf-dc0d-4fc1-861c-506a40cc2925', user=user)
        assert len(repo.bookings) == len_before - 1

    def test_delete_booking_usecase_invalid_student(self):
        repo = BookingRepositoryMock()
        usecase = DeleteBookingUsecase(repo=repo)
        user = {
            'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
            'name': 'Nome',
            'email': 'user@email.com',
            'role': 'STUDENT'
        }
        
        with pytest.raises(ForbiddenAction):
            usecase(booking_id='b2d3bebf-dc0d-4fc1-861c-506a40cc2925', user=user)

    def test_delete_booking_usecase_no_items_found(self):
        repo = BookingRepositoryMock()
        usecase = DeleteBookingUsecase(repo=repo)
        user = {
            'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
            'name': 'Nome',
            'email': 'user@email.com',
            'role': 'STUDENT'
        }
        with pytest.raises(NoItemsFound):
            booking = usecase(booking_id='b1d3bebf-dc0d-4fc1-861c-506a40cc2926', user = user)
            
    def test_delete_booking_usecase_invalid_booking_id(self):
        repo = BookingRepositoryMock()
        usecase = DeleteBookingUsecase(repo=repo)
        user = {
            'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
            'name': 'Nome',
            'email': 'user@email.com',
            'role': 'STUDENT'
        }
    
        with pytest.raises(EntityError):
            usecase(booking_id=-1, user=user)
    