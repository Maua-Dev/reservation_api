from .get_bookings_controller import GetBookingsController
from .get_bookings_usecase import GetBookingsUseCase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock

repo = Environments.get_booking_repo()()
usecase = GetBookingsUseCase(repo=repo)
controller = GetBookingsController(usecase=usecase)


def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(request=httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()
