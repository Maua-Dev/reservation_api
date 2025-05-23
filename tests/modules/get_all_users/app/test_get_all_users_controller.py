import pytest
from src.modules.get_all_users.app.get_all_users_usecase import GetAllUsersUseCase
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock
from src.modules.get_all_users.app.get_all_users_controller import GetAllUsersController
from src.shared.helpers.external_interfaces.http_models import HttpRequest

class Test_GetAllUsersController:
    @pytest.mark.skip("Can't run test in github actions") 
    def test_get_all_users_controller(self):

        repo = BookingRepositoryMock()
        usecase = GetAllUsersUseCase(repo=repo)
        controller = GetAllUsersController(usecase=usecase)
        request = HttpRequest()
        response = controller(request)

        assert response.status_code == 200
        assert len(response.body['users']) == 3
        assert response.body['message'] == 'the users were retrieved'
        assert response.body['users'][0]['user_id'] == '1f25448b-3429-4c19-8287-d9e64f17bc3a'