from .get_all_courts_controller import GetAllCourtsController
from .get_all_courts_usecase import GetAllCourtsUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo = Environments.get_reservation_repo()()
usecase = GetAllCourtsUsecase(repo)
controller = GetAllCourtsController(usecase)

def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(request=httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    
    return httpResponse.toDict()