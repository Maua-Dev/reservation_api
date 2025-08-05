import pytest
<<<<<<< HEAD:tests/modules/delete_bookings/app/test_delete_booking_usecase.py
from typing import Any, Optional
from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.status_enum import STATUS
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, ForbiddenAction
=======
>>>>>>> parent of 86c13e0 (Merge pull request #20 from Maua-Dev/user-on-generate-report):tests/modules/delete_booking/app/test_delete_booking_usecase.py
from src.shared.helpers.errors.domain_errors import EntityError
from src.modules.delete_booking.app.delete_booking_usecase import DeleteBookingUsecase
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock
from src.shared.helpers.errors.usecase_errors import NoItemsFound

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
        
<<<<<<< HEAD:tests/modules/delete_bookings/app/test_delete_booking_usecase.py
        booking = usecase(booking_id='b1d3bebf-dc0d-4fc1-861c-506a40cc2925', user=user)
=======
        booking = usecase(booking_id='b1d3bebf-dc0d-4fc1-861c-506a40cc2925',
                          user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98')
>>>>>>> parent of 86c13e0 (Merge pull request #20 from Maua-Dev/user-on-generate-report):tests/modules/delete_booking/app/test_delete_booking_usecase.py
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
<<<<<<< HEAD:tests/modules/delete_bookings/app/test_delete_booking_usecase.py
            booking = usecase(booking_id='b1d3bebf-dc0d-4fc1-861c-506a40cc2926', user = user)
=======
            booking = usecase(booking_id='b1d3bebf-dc0d-4fc1-861c-506a40cc2926',
                              user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98')
>>>>>>> parent of 86c13e0 (Merge pull request #20 from Maua-Dev/user-on-generate-report):tests/modules/delete_booking/app/test_delete_booking_usecase.py

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
<<<<<<< HEAD:tests/modules/delete_bookings/app/test_delete_booking_usecase.py
            usecase(booking_id=-1, user=user)
    
        with pytest.raises(EntityError):
            usecase(booking_id=None,user=user)
=======
            usecase(booking_id=-1,
                    user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98')
    
        with pytest.raises(EntityError):
            usecase(booking_id=None,
                    user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98')
>>>>>>> parent of 86c13e0 (Merge pull request #20 from Maua-Dev/user-on-generate-report):tests/modules/delete_booking/app/test_delete_booking_usecase.py
