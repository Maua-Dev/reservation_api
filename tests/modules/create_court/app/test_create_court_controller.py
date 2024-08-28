from src.modules.create_court.app.create_court_controller import CreateCourtController
from src.modules.create_court.app.create_court_usecase import CreateCourtUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.reservation_repository_mock import ReservationRepositoryMock

class TestCreateCourtController:
    def test_create_court_controller(self):
        repo = ReservationRepositoryMock()
        usecase = CreateCourtUsecase(repo= repo)
        controller = CreateCourtController(usecase=usecase)
        request = HttpRequest(body= {
            "number": 7,
            "status": "AVAILABLE",
            "is_field": False,
            "photo": "https://www.linkedin.com/in/vinicius-berti-a80354209/"
        })

        response = controller(request)
        assert response.status_code == 201
        assert response.body['message'] == "the court was created"  
        assert response.body['court']['number'] == 7
        assert response.body['court']['status'] == "AVAILABLE"
        assert response.body['court']['is_field'] == False
        assert response.body['court']['photo'] == "https://www.linkedin.com/in/vinicius-berti-a80354209/"

    def test_create_court_controller_missing_number(self):
        repo = ReservationRepositoryMock()
        usecase = CreateCourtUsecase(repo= repo)
        controller = CreateCourtController(usecase=usecase)
        request = HttpRequest(body= {
            "status": "AVAILABLE",
            "is_field": False,
            "photo": "https://www.linkedin.com/in/vinicius-berti-a80354209/"
        })

        response = controller(request)
        assert response.status_code == 400
        assert response.body == "Field number is missing"

    def test_create_court_controller_wrong_type_number(self):
        repo = ReservationRepositoryMock()
        usecase = CreateCourtUsecase(repo= repo)
        controller = CreateCourtController(usecase=usecase)
        request = HttpRequest(body= {
            "number": "a",
            "status": "AVAILABLE",
            "is_field": False,
            "photo": "https://www.linkedin.com/in/vinicius-berti-a80354209/"
        })

        response = controller(request)
        assert response.status_code == 400
        assert response.body == "Field number isn\'t in the right type.\n Received: <class 'str'>.\n Expected: <class 'int'>"


    def test_create_court_controller_invalid_number(self):
        repo = ReservationRepositoryMock()
        usecase = CreateCourtUsecase(repo= repo)
        controller = CreateCourtController(usecase=usecase)
        request = HttpRequest(body= {
            "number": 0,
            "status": "AVAILABLE",
            "is_field": False,
            "photo": "https://www.linkedin.com/in/vinicius-berti-a80354209/"
        })

        response = controller(request)
        assert response.status_code == 400
        assert response.body == "Field number is not valid"
    
    def test_create_court_controller_missing_status(self):
        repo = ReservationRepositoryMock()
        usecase = CreateCourtUsecase(repo= repo)
        controller = CreateCourtController(usecase=usecase)
        request = HttpRequest(body= {
            "number": 7,
            "is_field": False,
            "photo": "https://www.linkedin.com/in/vinicius-berti-a80354209/"
        })

        response = controller(request)
        assert response.status_code == 400
        assert response.body == "Field status is missing"

    def test_create_court_controller_invalid_status(self):
        repo = ReservationRepositoryMock()
        usecase = CreateCourtUsecase(repo= repo)
        controller = CreateCourtController(usecase=usecase)
        request = HttpRequest(body= {
            "number": 7,
            "status": "INVALID",
            "is_field": False,
            "photo": "https://www.linkedin.com/in/vinicius-berti-a80354209/"
        })

        response = controller(request)
        assert response.status_code == 400
        assert response.body == "Field status is not valid"

    def test_create_court_controller_missing_is_field(self):
        repo = ReservationRepositoryMock()
        usecase = CreateCourtUsecase(repo= repo)
        controller = CreateCourtController(usecase=usecase)
        request = HttpRequest(body= {
            "number": 7,
            "status": "AVAILABLE",
            "photo": "https://www.linkedin.com/in/vinicius-berti-a80354209/"
        })

        response = controller(request)
        assert response.status_code == 400
        assert response.body == "Field is_field is missing"

    def test_create_court_controller_is_field_not_valid(self):
        repo = ReservationRepositoryMock()
        usecase = CreateCourtUsecase(repo= repo)
        controller = CreateCourtController(usecase=usecase)
        request = HttpRequest(body= {
            "number": 7,
            "status": "AVAILABLE",
            "is_field": True,
            "photo": "https://www.linkedin.com/in/vinicius-berti-a80354209/"
        })

        response = controller(request)
        assert response.status_code == 400
        assert response.body == "Field is_field is not valid"

