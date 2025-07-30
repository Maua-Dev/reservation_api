from .create_booking_controller import CreateBookingController
from .create_booking_usecase import CreateBookingUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo = Environments.get_booking_repo()()
usecase = CreateBookingUsecase(repo)
controller = CreateBookingController(usecase)

def lambda_handler(event, context):
    
    print(event)
    
    httpRequest = LambdaHttpRequest(data=event)
    httpRequest.data['user_from_authorizer'] = event.get('requestContext', {}).get('authorizer', {}).get('user', None)
    response = controller(request=httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()