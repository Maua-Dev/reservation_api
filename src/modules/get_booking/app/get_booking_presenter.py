from .get_booking_controller import GetBookingController
from .get_booking_usecase import GetBookingUseCase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock
import json

repo = Environments.get_booking_repo()()
usecase = GetBookingUseCase(repo=repo)
controller = GetBookingController(usecase=usecase)

def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data= event)

    user_info_string = event.get('requestContext', {}).get('authorizer', {}).get('user')

    if user_info_string:
        httpRequest.data['user_from_authorizer'] = json.loads(user_info_string).get('user')
    else:
        httpRequest.data['user_from_authorizer'] = None

    response = controller(request = httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()