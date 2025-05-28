from src.modules.get_all_courts.app.get_all_courts_usecase import GetAllCourtsUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.reservation_repository_mock import ReservationRepositoryMock
from src.shared.domain.entities.court import Court
from src.modules.get_all_courts.app.get_all_courts_controller import GetAllCourtsController

class Test_GetAllCourtsController:
    def test_get_all_courts_controller(self):
        repo = ReservationRepositoryMock()
        usecase = GetAllCourtsUsecase(repo = repo)
        controller = GetAllCourtsController(usecase=usecase)
        request = HttpRequest()
        response = controller(request)
        assert response.status_code == 200
        assert response.body['message'] == 'the courts were retrieved'
        assert len(response.body['courts']) == 5
        
    