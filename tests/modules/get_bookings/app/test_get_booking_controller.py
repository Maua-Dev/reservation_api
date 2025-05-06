from src.modules.get_bookings.app.get_bookings_controller import GetBookingsController
from src.modules.get_bookings.app.get_bookings_usecase import GetBookingsUseCase
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock
from src.shared.helpers.external_interfaces.http_models import HttpRequest

class TestGetBookingsController:
    def test_get_bookings_controller(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingsUseCase(repo=repo)
        controller = GetBookingsController(usecase=usecase)
        request = HttpRequest(query_params={
            'booking_id': 'b2d3bebf-dc0d-4fc1-861c-506a40cc2925',
        })
        response = controller(request)

        assert response.status_code == 200
        assert response.body['bookings'][0]['booking_id'] == 'b2d3bebf-dc0d-4fc1-861c-506a40cc2925'
        assert response.body['bookings'][0]['start_date'] == 1634563800000
        assert response.body['bookings'][0]['end_date'] == 1634567400000
        assert response.body['bookings'][0]['court_number'] == 2
        assert response.body['bookings'][0]['sport'] == 'Football'
        assert response.body['bookings'][0]['user_id'] == 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
        assert response.body['bookings'][0]['materials'] == ['Bola', 'Chuteira']

    def test_get_bookings_controller_missing_booking_id(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingsUseCase(repo=repo)
        controller = GetBookingsController(usecase=usecase)
        request = HttpRequest(query_params={
        })
        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Empty query parameters: At least one of the filters must be provided: booking_id, user_id, sport, court_number, end_date, start_date'
    
    def test_get_bookings_controller_wrong_type_booking_id(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingsUseCase(repo=repo)
        controller = GetBookingsController(usecase=usecase)
        request = HttpRequest(query_params={
            'booking_id': 123,
        })
        response = controller(request)

        assert response.status_code == 400
        assert "Field booking_id isn't in the right type." in response.body
        assert "Received: int." in response.body
        assert "Expected: str" in response.body


    def test_get_bookings_controller_booking_not_found(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingsUseCase(repo=repo)
        controller = GetBookingsController(usecase=usecase)
        request = HttpRequest(query_params={
            'booking_id': 'b2d3bebf-dc0d-4fc1-861c-506a40cc2943',
        })

        response = controller(request)
        assert response.status_code == 404
        assert response.body == 'No items found for booking_id'
       