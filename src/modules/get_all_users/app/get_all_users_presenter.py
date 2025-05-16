from src.modules.get_all_users.app.get_all_users_controller import GetAllUsersController
from src.modules.get_all_users.app.get_all_users_usecase import GetAllUsersUseCase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock

repo = BookingRepositoryMock()
usecase = GetAllUsersUseCase(repo)
controller = GetAllUsersController(usecase)

def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data = event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body)

    return httpResponse.toDict()