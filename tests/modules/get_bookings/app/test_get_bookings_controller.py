import pytest

from src.modules.get_bookings.app.get_bookings_controller import GetBookingsController
from src.modules.get_bookings.app.get_bookings_usecase import GetBookingsUseCase
from src.shared.helpers.errors.usecase_errors import DependantFilter
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock
from src.shared.helpers.external_interfaces.http_models import HttpRequest

class TestGetBookingsController:
    def setup_method(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingsUseCase(repo=repo)
        self.controller = GetBookingsController(usecase=usecase)

    def test_get_bookings_controller(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingsUseCase(repo=repo)
        controller = GetBookingsController(usecase=usecase)
        request = HttpRequest(query_params={
            'booking_id': 'b2d3bebf-dc0d-4fc1-861c-506a40cc2925',
            'user_id': 'false'
        }, headers={
            "user_from_authorizer": {
                "displayName": "John Doe",
                "mail": "JD@maua.br",
                "id": "c8435c66-13a4-4641-9d54-773b4b8ccc98"
            }
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

    def test_get_bookings_controller_empty_query(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingsUseCase(repo=repo)
        controller = GetBookingsController(usecase=usecase)
        request = HttpRequest(query_params={
        }, headers={
            "user_from_authorizer": {
                "displayName": 'Lebron James',
                "mail": 'lbj@maua.br',
                "id": 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
            }
        })
        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Empty query parameters: At least one of the filters must be provided: booking_id, user_id, sport, court_number, end_date, start_date'

    def test_get_bookings_controller_wrong_type_booking_id(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingsUseCase(repo=repo)
        controller = GetBookingsController(usecase=usecase)
        request = HttpRequest(query_params={
            'booking_id': '123',
        }, headers={
            "user_from_authorizer": {
                "displayName": 'Lebron James',
                "mail": 'lbj@maua.br',
                "id": 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
            }
        })
        response = controller(request)

        assert response.status_code == 400
        assert "Field booking_id is not valid" in response.body

    def test_get_bookings_controller_booking_not_found(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingsUseCase(repo=repo)
        controller = GetBookingsController(usecase=usecase)
        request = HttpRequest(query_params={
            'booking_id': 'b2d3bebf-dc0d-4fc1-861c-506a40cc2943',
        }, headers={
            "user_from_authorizer": {
                "displayName": 'Lebron James',
                "mail": 'lbj@maua.br',
                "id": 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
            }
        })

        response = controller(request)
        assert response.status_code == 404
        assert response.body == 'No items found for booking_id'

    def test_get_bookings_controller_sport(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingsUseCase(repo=repo)
        controller = GetBookingsController(usecase=usecase)
        request = HttpRequest(query_params={
            'sport': 'Tennis',
        }, headers={
            "user_from_authorizer": {
                "displayName": 'Lebron James',
                "mail": 'lbj@maua.br',
                "id": 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
            }
        })
        response = controller(request)

        assert response.status_code == 200

        for booking in response.body['bookings']:
            assert booking['sport'] == 'Tennis'

    def test_get_bookings_controller_court_number(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingsUseCase(repo=repo)
        controller = GetBookingsController(usecase=usecase)
        request = HttpRequest(query_params={
            'court_number': '1',
        }, headers={
            'user_from_authorizer': {
                "displayName": 'Lebron James',
                "mail": "lbj@maua.br",
                "id": 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
            }
        })
        response = controller(request)

        assert response.status_code == 200

        for booking in response.body['bookings']:
            assert booking['court_number'] == 1

    def test_get_bookings_controller_user_id(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingsUseCase(repo=repo)
        controller = GetBookingsController(usecase=usecase)
        request = HttpRequest(query_params={
            'user_id': 'true',
        },  headers={
            "user_from_authorizer": {
                "displayName": 'Lebron James',
                "mail": 'lbj@maua.br',
                "id": 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
            }
        })
        response = controller(request)

        assert response.status_code == 200

        for booking in response.body['bookings']:
            assert booking['user_id'] == 'c8435c66-13a4-4641-9d54-773b4b8ccc98'

    def test_get_bookings_controller_start_date_error(self):

        repo = BookingRepositoryMock()
        usecase = GetBookingsUseCase(repo=repo)
        controller = GetBookingsController(usecase=usecase)
        request = HttpRequest(query_params={
            'start_date': '1634563800000',
        }, headers={
            "user_from_authorizer": {
                "displayName": 'Lebron James',
                "mail": 'lbj@maua.br',
                "id": 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
            }
        })
        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Filters have to be provided together: start_date and end_date"

    def test_get_bookings_controller_end_date_error(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingsUseCase(repo=repo)
        controller = GetBookingsController(usecase=usecase)
        request = HttpRequest(query_params={
            'end_date': '1634567400000',
        }, headers={
            "user_from_authorizer": {
                "displayName": 'Lebron James',
                "mail": 'lbj@maua.br',
                "id": 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
            }
        })
        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Filters have to be provided together: start_date and end_date"

    def test_get_bookings_controller_start_date_end_date(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingsUseCase(repo=repo)
        controller = GetBookingsController(usecase=usecase)
        request = HttpRequest(query_params={
            'start_date': '1634563800000',
            'end_date': '16345674000000',
        }, headers={
            "user_from_authorizer": {
                "displayName": 'Lebron James',
                "mail": 'lbj@maua.br',
                "id": 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
            }
        })
        response = controller(request)

        assert response.status_code == 200

        for booking in response.body['bookings']:
            assert booking['start_date'] >= 1634563800000
            assert booking['end_date'] <= 16345674000000

    def test_get_bookings_controller_five_filters(self):
        # booking_id + user_id + sport + court_number + date_range
        start = '1634583600000'
        end = '1634585400000'
        request = HttpRequest(query_params={
            'booking_id': 'b6d3bebf-dc0d-4fc1-861c-506a40cc2925',
            'user_id': 'true',
            'sport': 'Futsal',
            'court_number': 5,
            'start_date': start,
            'end_date': end
        }, headers={
            "user_from_authorizer": {
                "displayName": 'Lebron James',
                "mail": 'lbj@maua.br',
                "id": 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
            }
        })
        response = self.controller(request)
        assert response.status_code == 200
        bookings = response.body['bookings']
        assert len(bookings) == 1
        b = bookings[0]
        assert b['booking_id'] == 'b6d3bebf-dc0d-4fc1-861c-506a40cc2925'
        assert b['user_id'] == 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
        assert b['sport'] == 'Futsal'
        assert b['court_number'] == 5
        assert b['start_date'] >= int(start) and b['end_date'] <= int(end)

    def test_get_bookings_controller_four_filters(self):
        # user_id + sport + court_number + date_range
        start = '1634574600000'
        end = '1634578200000'
        request = HttpRequest(query_params={
            'user_id': 'true',
            'sport': 'Volleyball',
            'court_number': 4,
            'start_date': start,
            'end_date': end
        }, headers={
            "user_from_authorizer": {
                "displayName": 'Lebron James',
                "mail": 'lbj@maua.br',
                "id": 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
            }
        })
        response = self.controller(request)
        assert response.status_code == 200
        bookings = response.body['bookings']
        assert len(bookings) == 1
        b = bookings[0]
        assert b['user_id'] == 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
        assert b['sport'] == 'Volleyball'
        assert b['court_number'] == 4
        assert b['start_date'] >= int(start) and b['end_date'] <= int(end)

    def test_get_bookings_controller_three_filters(self):
        # sport + court_number + user_id
        request = HttpRequest(query_params={
            'sport': 'Rugby',
            'court_number': 5,
            'user_id': 'true'
        }, headers={
            "user_from_authorizer": {
                "displayName": 'Lebron James',
                "mail": 'lbj@maua.br',
                "id": 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
            }
        })
        response = self.controller(request)
        assert response.status_code == 200
        bookings = response.body['bookings']
        assert len(bookings) == 1
        b = bookings[0]
        assert b['sport'] == 'Rugby'
        assert b['court_number'] == 5
        assert b['user_id'] == 'c8435c66-13a4-4641-9d54-773b4b8ccc98'

    def test_get_bookings_user_id_not_valid(self):
        request = HttpRequest(query_params={
            'user_id': '1'
        }, headers={
            "user_from_authorizer": {
                "displayName": 'Lebron James',
                "mail": 'lbj@maua.br',
                "id": 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
            }
        })
        response = self.controller(request)
        assert response.status_code == 400

