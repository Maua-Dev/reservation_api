from .get_all_booking_controller import GetAllBookingsController
from .get_all_booking_usecase import GetAllBookingsUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo = Environments.get_booking_repo()()
usecase = GetAllBookingsUsecase(repo)
controller = GetAllBookingsController(usecase)

def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(request=httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    
    return httpResponse.toDict()