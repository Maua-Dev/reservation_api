import pytest

from src.modules.get_bookings.app.get_bookings_usecase import GetBookingsUseCase
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound

class FakeUserClient:
    def get_user_name(self, user_id):
        return 'CEAF MAUA'

    def get_user_network_id(self, user_id):
        return 'ceaf'


class TestGetBookingsUseCase:
    def test_get_bookings_usecase(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingsUseCase(repo=repo)
        booking_id = repo.bookings[0].booking_id
        response = usecase(booking_id=booking_id)

        assert response['bookings'][0] == repo.bookings[0]
        assert response['owner'] == []

    def test_get_bookings_usecase_admin_returns_owner_metadata(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingsUseCase(repo=repo)
        usecase.user_client = FakeUserClient()
        booking_id = repo.bookings[0].booking_id

        response = usecase(booking_id=booking_id, requester_role='ADMIN')

        assert response['bookings'][0] == repo.bookings[0]
        assert response['owner'] == [{'name': 'CEAF MAUA', 'network_id': 'ceaf'}]
    
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

    def test_get_bookings_usecase_admin_builds_user_client_once(self, monkeypatch):
        class CountingUserClient:
            instances = 0

            def __init__(self):
                CountingUserClient.instances += 1

            def get_user_name(self, user_id):
                return 'CEAF MAUA'

            def get_user_network_id(self, user_id):
                return 'ceaf'

        monkeypatch.setattr(
            'src.modules.get_bookings.app.get_bookings_usecase.UserAPIClient',
            CountingUserClient,
        )

        repo = BookingRepositoryMock()
        usecase = GetBookingsUseCase(repo=repo)

        response = usecase(user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98', requester_role='ADMIN')

        assert len(response['bookings']) > 1
        assert len(response['owner']) == len(response['bookings'])
        assert CountingUserClient.instances == 1