from src.modules.get_court.app.get_court_controller import GetCourtController
from src.modules.get_court.app.get_court_usecase import GetCourtUsecase
from src.shared.infra.repositories.reservation_repository_mock import ReservationRepositoryMock
from src.shared.helpers.external_interfaces.http_models import HttpRequest


class TestGetCourtController:
    def test_get_court_controller(self):

        repo = ReservationRepositoryMock()
        usecase = GetCourtUsecase(repo=repo)
        controller = GetCourtController(usecase=usecase)
        request = HttpRequest(body={
            "number": 2,
            "status": "AVAILABLE",
            "is_field": False,
            "photo": "https://www.linkedin.com/in/giovanna-albuquerque-16917a245/"
        })

        response = controller(request)
        
        assert response.status_code == 200
        assert response.body['court']['number'] == 2
        assert response.body['court']['status'] == "AVAILABLE"
        assert response.body['court']['is_field'] == False
        assert response.body['court']['photo'] == "https://www.linkedin.com/in/giovanna-albuquerque-16917a245/"


    def test_get_court_controller_missing_number(self):
        repo = ReservationRepositoryMock()
        usecase = GetCourtUsecase(repo=repo)
        controller = GetCourtController(usecase=usecase)
        request = HttpRequest(body={
            "status": "AVAILABLE",
            "is_field": False,
            "photo": "https://www.linkedin.com/in/giovanna-albuquerque-16917a245/"
        })

        response = controller(request)
        assert response.status_code == 400
        assert response.body == 'Field number is missing'



    def test_get_court_controller_wrong_type_parameters(self):
        repo = ReservationRepositoryMock()
        usecase = GetCourtUsecase(repo=repo)
        controller = GetCourtController(usecase=usecase)
        request = HttpRequest(body={
            "number": "cavalo",
            "status": "AVAILABLE",
            "is_field": False,
            "photo": "https://www.linkedin.com/in/giovanna-albuquerque-16917a245/"
        })

        response = controller(request)
        assert response.status_code == 400
        assert "Field number isn't in the right type." in response.body
        assert "Received: str." in response.body
        assert "Expected: int" in response.body

  
    def test_get_court_controller_court_not_found(self):
        repo = ReservationRepositoryMock()
        usecase = GetCourtUsecase(repo=repo)
        controller = GetCourtController(usecase=usecase)
        request = HttpRequest(body={
            "number": 10,
            "status": "AVAILABLE",
            "is_field": False,
            "photo": "https://www.linkedin.com/in/giovanna-albuquerque-16917a245/"
        })

        response = controller(request)
        assert response.status_code == 404
        assert response.body == 'No items found for number'

