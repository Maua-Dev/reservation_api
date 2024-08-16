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



