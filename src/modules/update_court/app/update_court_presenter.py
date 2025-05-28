from .update_court_controller import UpdateCourtController
from .update_court_usecase import UpdateCourtUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo = Environments.get_reservation_repo()()
usecase = UpdateCourtUsecase(repo)
controller = UpdateCourtController(usecase)


def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(request=httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()