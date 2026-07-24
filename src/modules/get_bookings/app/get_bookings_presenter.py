import json

from .get_bookings_controller import GetBookingsController
from .get_bookings_usecase import GetBookingsUseCase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse


def _build_controller():
    repo = Environments.get_booking_repo()()
    usecase = GetBookingsUseCase(repo=repo)
    return GetBookingsController(usecase=usecase)


def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)

    user_info = event.get('requestContext', {}).get('authorizer', {}).get('user')
    if isinstance(user_info, str):
        try:
            user_info = json.loads(user_info)
        except json.JSONDecodeError:
            user_info = None
    elif not isinstance(user_info, dict):
        user_info = None

    httpRequest.data['user_from_authorizer'] = user_info

    controller = _build_controller()
    response = controller(request=httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()
