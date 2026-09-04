from src.modules.get_booking.app.get_booking_controller import GetBookingController
from src.modules.get_booking.app.get_booking_usecase import GetBookingUseCase
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock
from src.shared.helpers.external_interfaces.http_models import HttpRequest


class _UserClientFake:
    def __init__(self, name=None, network_id=None):
        self._name = name
        self._network_id = network_id

    def get_user_name(self, user_id):
        return self._name

    def get_user_network_id(self, user_id):
        return self._network_id


STUDENT = {"user_id": "some-student", "role": "STUDENT", "email": "23.00847-4@maua.br", "name": "Aluno"}
ADMIN = {"user_id": "some-admin", "role": "ADMIN", "email": "nome.sobrenome@maua.br", "name": "Admin"}


class TestGetBookingController:
    def test_get_booking_controller_non_admin(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingUseCase(repo=repo)
        controller = GetBookingController(usecase=usecase)
        request = HttpRequest(
            body={'user_from_authorizer': STUDENT},
            query_params={'booking_id': 'b2d3bebf-dc0d-4fc1-861c-506a40cc2925'},
        )
        response = controller(request)

        assert response.status_code == 200
        assert response.body['booking']['booking_id'] == 'b2d3bebf-dc0d-4fc1-861c-506a40cc2925'
        assert response.body['booking']['start_date'] == 1634563800000
        assert response.body['booking']['end_date'] == 1634567400000
        assert response.body['booking']['court_number'] == 2
        assert response.body['booking']['sport'] == 'Football'
        assert response.body['booking']['materials'] == ['Bola', 'Chuteira']
        assert 'owner_name' not in response.body['booking']
        assert 'owner_network_id' not in response.body['booking']

    def test_get_booking_controller_admin_enriches(self):
        repo = BookingRepositoryMock()
        user_client = _UserClientFake(name="GUSTAVO ALVES GOMES", network_id="23.00847-4")
        usecase = GetBookingUseCase(repo=repo, user_client=user_client)
        controller = GetBookingController(usecase=usecase)
        request = HttpRequest(
            body={'user_from_authorizer': ADMIN},
            query_params={'booking_id': 'b2d3bebf-dc0d-4fc1-861c-506a40cc2925'},
        )
        response = controller(request)

        assert response.status_code == 200
        assert response.body['booking']['owner_name'] == 'GUSTAVO ALVES GOMES'
        assert response.body['booking']['owner_network_id'] == '23.00847-4'

    def test_get_booking_controller_missing_authorizer(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingUseCase(repo=repo)
        controller = GetBookingController(usecase=usecase)
        request = HttpRequest(query_params={'booking_id': 'b2d3bebf-dc0d-4fc1-861c-506a40cc2925'})
        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'User was not returned from authorizer'

    def test_get_booking_controller_missing_booking_id(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingUseCase(repo=repo)
        controller = GetBookingController(usecase=usecase)
        request = HttpRequest(body={'user_from_authorizer': STUDENT}, query_params={})
        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Field booking_id is missing'

    def test_get_booking_controller_wrong_type_booking_id(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingUseCase(repo=repo)
        controller = GetBookingController(usecase=usecase)
        request = HttpRequest(body={'user_from_authorizer': STUDENT, 'booking_id': 123})
        response = controller(request)

        assert response.status_code == 400
        assert "Field booking_id isn't in the right type." in response.body
        assert "Received: int." in response.body
        assert "Expected: str" in response.body

    def test_get_booking_controller_booking_not_found(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingUseCase(repo=repo)
        controller = GetBookingController(usecase=usecase)
        request = HttpRequest(
            body={'user_from_authorizer': STUDENT},
            query_params={'booking_id': 'b2d3bebf-dc0d-4fc1-861c-506a40cc2943'},
        )
        response = controller(request)

        assert response.status_code == 404
        assert response.body == 'No items found for booking_id'
