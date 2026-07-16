import pytest

from src.modules.get_booking.app.get_booking_usecase import GetBookingUseCase
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class _UserClientFake:
    def __init__(self, name=None, network_id=None):
        self._name = name
        self._network_id = network_id

    def get_user_name(self, user_id):
        return self._name

    def get_user_network_id(self, user_id):
        return self._network_id


class TestGetBookingUseCase:
    def test_get_booking_usecase_non_admin_returns_no_owner(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingUseCase(repo=repo)
        booking_id = repo.bookings[0].booking_id

        result = usecase(booking_id=booking_id, requester_role="STUDENT")

        assert result["booking"] == repo.bookings[0]
        assert result["owner"] is None

    def test_get_booking_usecase_no_role_returns_no_owner(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingUseCase(repo=repo)
        booking_id = repo.bookings[0].booking_id

        result = usecase(booking_id=booking_id)

        assert result["booking"] == repo.bookings[0]
        assert result["owner"] is None

    def test_get_booking_usecase_admin_enriches_owner(self):
        repo = BookingRepositoryMock()
        user_client = _UserClientFake(name="GUSTAVO ALVES GOMES", network_id="23.00847-4")
        usecase = GetBookingUseCase(repo=repo, user_client=user_client)
        booking_id = repo.bookings[0].booking_id

        result = usecase(booking_id=booking_id, requester_role="ADMIN")

        assert result["booking"] == repo.bookings[0]
        assert result["owner"] == {"name": "GUSTAVO ALVES GOMES", "network_id": "23.00847-4"}

    def test_get_booking_usecase_admin_owner_not_found(self):
        repo = BookingRepositoryMock()
        user_client = _UserClientFake(name=None, network_id=None)
        usecase = GetBookingUseCase(repo=repo, user_client=user_client)
        booking_id = repo.bookings[0].booking_id

        result = usecase(booking_id=booking_id, requester_role="ADMIN")

        assert result["booking"] == repo.bookings[0]
        assert result["owner"] == {"name": None, "network_id": None}

    def test_get_booking_usecase_invalid_id(self):
        with pytest.raises(EntityError):
            repo = BookingRepositoryMock()
            usecase = GetBookingUseCase(repo=repo)
            usecase("invalid_id")

    def test_get_booking_usecase_no_items_found(self):
        with pytest.raises(NoItemsFound):
            repo = BookingRepositoryMock()
            usecase = GetBookingUseCase(repo=repo)
            usecase("b3d3b3b3-dc0d-4fc1-861c-506a40cc2925")
