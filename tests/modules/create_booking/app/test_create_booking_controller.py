from src.modules.create_booking.app.create_booking_controller import CreateBookingController
from src.modules.create_booking.app.create_booking_usecase import CreateBookingUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock


class TestCreateBookingController:

    def test_create_booking_controller(self):
        repo = BookingRepositoryMock()
        usecase = CreateBookingUsecase(repo)
        controller = CreateBookingController(usecase)

        request = HttpRequest(
            body={
                "start_date": 1630000000,
                "end_date": 1630003600,
                "court_number": 1,
                "sport": "Tennis",
                "materials": ["racket", "balls"]
            },
            headers={
                "user_from_authorizer": {
                    "displayName": 'Lebron James',
                    "mail": 'lbj@maua.br',
                    "id": 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
                }
            }
        )

        response = controller(request)

        assert response.status_code == 201

    def test_create_booking_controller_missing_start_date(self):
        repo = BookingRepositoryMock()
        usecase = CreateBookingUsecase(repo)
        controller = CreateBookingController(usecase)

        request = HttpRequest(
            body={
                "end_date": 1630003600,
                "court_number": 1,
                "sport": "Tennis",
                "materials": ["racket", "balls"]
            },
            headers={
                "user_from_authorizer": {
                    "displayName": 'Lebron James',
                    "mail": 'lbj@maua.br',
                    "id": 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
                }
            })

        response = controller(request)

        assert response.body == "Field start_date is missing"
        assert response.status_code == 400

    def test_create_booking_controller_wrong_type_start_date(self):
        repo = BookingRepositoryMock()
        usecase = CreateBookingUsecase(repo)
        controller = CreateBookingController(usecase)

        request = HttpRequest(body={
            "start_date": "1630000000",
            "end_date": 1630003600,
            "court_number": 1,
            "sport": "Tennis",
            "materials": ["racket", "balls"]
        }, headers={
            "user_from_authorizer": {
                "displayName": 'Lebron James',
                "mail": 'lbj@maua.br',
                "id": 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
            }
        })

        response = controller(request)

        assert response.body == "Field start_date isn't in the right type.\n Received: str.\n Expected: int"
        assert response.status_code == 400

    def test_create_booking_controller_missing_end_date(self):
        repo = BookingRepositoryMock()
        usecase = CreateBookingUsecase(repo)
        controller = CreateBookingController(usecase)

        request = HttpRequest(body={
            "start_date": 1630000000,
            "court_number": 1,
            "sport": "Tennis",
            "materials": ["racket", "balls"]
        }, headers={
            "user_from_authorizer": {
                "displayName": 'Lebron James',
                "mail": 'lbj@maua.br',
                "id": 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
            }
        })

        response = controller(request)

        assert response.body == "Field end_date is missing"
        assert response.status_code == 400

    def test_create_booking_controller_wrong_type_end_date(self):
        repo = BookingRepositoryMock()
        usecase = CreateBookingUsecase(repo)
        controller = CreateBookingController(usecase)

        request = HttpRequest(body={
            "start_date": 1630000000,
            "end_date": "1630003600",
            "court_number": 1,
            "sport": "Tennis",
            "materials": ["racket", "balls"]
        }, headers={
            "user_from_authorizer": {
                "displayName": 'Lebron James',
                "mail": 'lbj@maua.br',
                "id": 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
            }
        })

        response = controller(request)

        assert response.body == "Field end_date isn't in the right type.\n Received: str.\n Expected: int"
        assert response.status_code == 400

    def test_create_booking_wrong_type_court_number(self):
        repo = BookingRepositoryMock()
        usecase = CreateBookingUsecase(repo)
        controller = CreateBookingController(usecase)

        request = HttpRequest(body={
            "start_date": 1630000000,
            "end_date": 1630003600,
            "court_number": "1",
            "sport": "Tennis",
            "materials": ["racket", "balls"]
        }, headers={
            "user_from_authorizer": {
                "displayName": 'Lebron James',
                "mail": 'lbj@maua.br',
                "id": 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
            }
        })

        response = controller(request)

        assert response.body == "Field court_number isn't in the right type.\n Received: str.\n Expected: int"
        assert response.status_code == 400

    def test_create_booking_controller_missing_court_number(self):
        repo = BookingRepositoryMock()
        usecase = CreateBookingUsecase(repo)
        controller = CreateBookingController(usecase)

        request = HttpRequest(body={
            "start_date": 1630000000,
            "end_date": 1630003600,
            "sport": "Tennis",
            "materials": ["racket", "balls"]
        }, headers={
            "user_from_authorizer": {
                "displayName": 'Lebron James',
                "mail": 'lbj@maua.br',
                "id": 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
            }
        })

        response = controller(request)

        assert response.body == "Field court_number is missing"
        assert response.status_code == 400

    def test_create_booking_controller_missing_sport(self):
        repo = BookingRepositoryMock()
        usecase = CreateBookingUsecase(repo)
        controller = CreateBookingController(usecase)

        request = HttpRequest(body={
            "start_date": 1630000000,
            "end_date": 1630003600,
            "court_number": 1,
            "materials": ["racket", "balls"]
        }, headers={
            "user_from_authorizer": {
                "displayName": 'Lebron James',
                "mail": 'lbj@maua.br',
                "id": 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
            }
        })

        response = controller(request)

        assert response.body == "Field sport is missing"
        assert response.status_code == 400

    def test_create_booking_controller_wrong_type_sport(self):
        repo = BookingRepositoryMock()
        usecase = CreateBookingUsecase(repo)
        controller = CreateBookingController(usecase)

        request = HttpRequest(body={
            "start_date": 1630000000,
            "end_date": 1630003600,
            "court_number": 1,
            "sport": 1,
            "materials": ["racket", "balls"]
        }, headers={
            "user_from_authorizer": {
                "displayName": 'Lebron James',
                "mail": 'lbj@maua.br',
                "id": 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
            }
        })

        response = controller(request)

        assert response.body == "Field sport isn't in the right type.\n Received: int.\n Expected: str"
        assert response.status_code == 400

    def test_create_booking_controller_missing_materials(self):
        repo = BookingRepositoryMock()
        usecase = CreateBookingUsecase(repo)
        controller = CreateBookingController(usecase)

        request = HttpRequest(body={
            "start_date": 1630000000,
            "end_date": 1630003600,
            "court_number": 1,
            "sport": "Tennis",
        }, headers={
            "user_from_authorizer": {
                "displayName": 'Lebron James',
                "mail": 'lbj@maua.br',
                "id": 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
            }
        })

        response = controller(request)

        assert response.body == "Field materials is missing"
        assert response.status_code == 400

    def test_create_booking_controller_wrong_type_materials(self):
        repo = BookingRepositoryMock()
        usecase = CreateBookingUsecase(repo)
        controller = CreateBookingController(usecase)

        request = HttpRequest(body={
            "start_date": 1630000000,
            "end_date": 1630003600,
            "court_number": 1,
            "sport": "Tennis",
            "materials": "racket"
        }, headers={
            "user_from_authorizer": {
                "displayName": 'Lebron James',
                "mail": 'lbj@maua.br',
                "id": 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
            }
        })

        response = controller(request)

        assert response.body == "Field materials isn't in the right type.\n Received: str.\n Expected: list"
        assert response.status_code == 400

    def test_create_booking_controller_wrong_type_inside_list(self):
        repo = BookingRepositoryMock()
        usecase = CreateBookingUsecase(repo)
        controller = CreateBookingController(usecase)

        request = HttpRequest(body={
            "start_date": 1630000000,
            "end_date": 1630003600,
            "court_number": 1,
            "sport": "Tennis",
            "materials": ["racket", 1]
        }, headers={
            "user_from_authorizer": {
                "displayName": 'Lebron James',
                "mail": 'lbj@maua.br',
                "id": 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
            }
        })

        response = controller(request)

        assert response.body == "Invalid material type"
        assert response.status_code == 400

