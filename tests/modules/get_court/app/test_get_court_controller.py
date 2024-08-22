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
        assert response.body.to_dict()['court']['number'] == 2
        assert response.body.to_dict()['court']['status'] == "AVAILABLE"
        assert response.body.to_dict()['court']['is_field'] == False
        assert response.body.to_dict()['court']['photo'] == "https://www.linkedin.com/in/giovanna-albuquerque-16917a245/"


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



    def test_get_controller_wrong_type_parameters(self):
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
        assert response.body == 'Field number is not valid'


    def test_get_court_controller_entity_error(self):
        repo = ReservationRepositoryMock()
        usecase = GetCourtUsecase(repo=repo)
        controller = GetCourtController(usecase=usecase)
        request = HttpRequest(body={
            "number": 7,
            "status": "AVAILABLE",
            "is_field": False,
            "photo": "https://www.linkedin.com/in/giovanna-albuquerque-16917a245/"
        })

        response = controller(request)
        assert response.status_code == 404
        assert response.body == 'No items found for court'