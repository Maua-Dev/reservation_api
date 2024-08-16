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
        request = HttpRequest(body={
            "status": "AVAILABLE",
            "is_field": False,
            "photo": "https://www.linkedin.com/in/vinicius-berti-a80354209/"
        })

        response = controller(request)
        assert response.status_code == 400
        assert response.body == 'Field number is missing'

        
    def test_create_court_controller_with_missing_status(self):
        repo = ReservationRepositoryMock()
        usecase = CreateCourtUsecase(repo= repo)
        controller = CreateCourtController(usecase=usecase)
        request = HttpRequest(body={
            "number": 7,
            "is_field": False,
            "photo": "https://www.linkedin.com/in/vinicius-berti-a80354209/"
        })

        response = controller(request)
        assert response.status_code == 400
        assert response.body == 'Field status is missing'

    def test_create_court_controller_wrong_type_number(self):
        repo = ReservationRepositoryMock()
        usecase = CreateCourtUsecase(repo= repo)
        controller = CreateCourtController(usecase=usecase)
        request = HttpRequest(body={
            "number": "cavalo",
            "status": "AVAILABLE",
            "is_field": False,
            "photo": "https://www.linkedin.com/in/vinicius-berti-a80354209/"
        })        
        
        reponse = controller(request)
        assert reponse.status_code == 400
        assert reponse.body == "Field number isn\'t in the right type.\n Received: <class 'str'>.\n Expected: <class 'int'>"

        
    def test_create_court_controller_with_wrong_type_status(self):
        repo = ReservationRepositoryMock()
        usecase = CreateCourtUsecase(repo= repo)
        controller = CreateCourtController(usecase=usecase)
        request = HttpRequest(body={
            "number": 7,
            "status": 123,
            "is_field": False,
            "photo": "https://www.linkedin.com/in/vinicius-berti-a80354209/"
        })

        response = controller(request)
        assert response.status_code == 400
        assert response.body == "Field status isn\'t in the right type.\n Received: <class 'int'>.\n Expected: <class 'str'>"


    def test_create_court_controllerwith_duplicated_item(self):
        repo = ReservationRepositoryMock()
        usecase = CreateCourtUsecase(repo= repo)
        controller = CreateCourtController(usecase=usecase)
        request = HttpRequest(body= {
            "number": 1,
            "status": "AVAILABLE",
            "is_field": False,
            "photo": "https://www.linkedin.com/in/vinicius-berti-a80354209/"
        })

        response = controller(request)
        assert response.status_code == 400
        assert response.body == "The item alredy exists for this number" 
    

    def test_create_court_controller_number_entity_error(self):
        repo = ReservationRepositoryMock()
        usecase = CreateCourtUsecase(repo= repo)
        controller = CreateCourtController(usecase=usecase)
        request = HttpRequest(body={
            "number": 0,
            "status": "AVAILABLE",  
            "is_field": False,
            "photo": "https://www.linkedin.com/in/vinicius-berti-a80354209/"
        })
        
        reponse = controller(request)
        assert reponse.status_code == 400
        assert reponse.body == "Field number is not valid"

        
    def test_create_court_controller_status_entity_error(self):
        repo = ReservationRepositoryMock()
        usecase = CreateCourtUsecase(repo= repo)
        controller = CreateCourtController(usecase=usecase)
        request = HttpRequest(body={
            "number": 7,
            "status": "INVALID",
            "is_field": False,
            "photo": "https://www.linkedin.com/in/vinicius-berti-a80354209/"
        })

        response = controller(request)
        assert response.status_code == 400
        assert response.body == "Field status is not valid"   
        
    