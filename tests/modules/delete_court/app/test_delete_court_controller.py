from src.modules.delete_court.app.delete_court_controller import DeleteCourtController
from src.modules.delete_court.app.delete_court_usecase import DeleteCourtUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.reservation_repository_mock import ReservationRepositoryMock

class TestDeleteCourtController:
    def test_delete_court_controller(self):
        repo = ReservationRepositoryMock()
        usecase = DeleteCourtUsecase(repo= repo)
        controller = DeleteCourtController(usecase=usecase)
        request = HttpRequest(body= {
            "number": 2,
            "user_from_authorizer": {
                "name": "Dummy",
                "email": "admin@maua.br",
                "user_id": "user_id",
                "ra": None,
                "role": "ADMIN",
                "confirm_user": False
            }
        })

        response = controller(request)
        assert response.status_code == 200
        assert response.body['message'] == "the court was deleted"  
        assert response.body['court']['number'] == 2

    def test_delete_court_controller_missing_number(self):
        repo = ReservationRepositoryMock()
        usecase = DeleteCourtUsecase(repo= repo)
        controller = DeleteCourtController(usecase=usecase)
        request = HttpRequest(body={
            "number": None,
            "user_from_authorizer": {
                "name": "Dummy",
                "email": "admin@maua.br",
                "user_id": "user_id",
                "ra": None,
                "role": "ADMIN",
                "confirm_user": False
            }
        })

        response = controller(request)
        assert response.status_code == 400
        assert response.body == 'Field number is missing'

    def test_delete_court_controller_number_entity_error(self):
        repo = ReservationRepositoryMock()
        usecase = DeleteCourtUsecase(repo= repo)
        controller = DeleteCourtController(usecase=usecase)
        request = HttpRequest(body={
            "number": 0,
            "user_from_authorizer": {
                "name": "Dummy",
                "email": "admin@maua.br",
                "user_id": "user_id",
                "ra": None,
                "role": "ADMIN",
                "confirm_user": False
            }
        })
        
        reponse = controller(request)
        assert reponse.status_code == 400
        assert reponse.body == "Field number is not valid"

    def test_delete_court_controller_wrong_type_parameter(self):
        repo = ReservationRepositoryMock()
        usecase = DeleteCourtUsecase(repo=repo)
        controller = DeleteCourtController(usecase=usecase)
        request = HttpRequest(body={
            "number": "wrong_type",
            "user_from_authorizer": {
                "name": "Dummy",
                "email": "admin@maua.br",
                "user_id": "user_id",
                "ra": None,
                "role": "ADMIN",
                "confirm_user": False
            }
        })

        response = controller(request)
        assert response.status_code == 400
        assert "Field number isn't in the right type" in response.body

    def test_delete_court_controller_not_found(self):
        repo = ReservationRepositoryMock()
        usecase = DeleteCourtUsecase(repo=repo)
        controller = DeleteCourtController(usecase=usecase)
        request = HttpRequest(body={
            "number": 10,
            "user_from_authorizer": {
                "name": "Dummy",
                "email": "admin@maua.br",
                "user_id": "user_id",
                "ra": None,
                "role": "ADMIN",
                "confirm_user": False
            }
        })

        response = controller(request)
        assert response.status_code == 404
        assert response.body == "No items found for court"