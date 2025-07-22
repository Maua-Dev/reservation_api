from .delete_booking_controller import DeleteBookingController
from .delete_booking_usecase import DeleteBookingUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo = Environments.get_booking_repo()()
usecase = DeleteBookingUsecase(repo)
controller = DeleteBookingController(usecase)

def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    print(event)
    print("PRINT DO EVENT TA AQUI")
    httpRequest.data['user_from_authorizer'] = event.get('requestContext', {}).get('authorizer', {}).get('user', None)
    response = controller(request=httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    
    return httpResponse.toDict()