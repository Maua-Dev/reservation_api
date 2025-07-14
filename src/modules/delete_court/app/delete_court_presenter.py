from .delete_court_controller import DeleteCourtController
from .delete_court_usecase import DeleteCourtUsecase
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.environments import Environments

repo = Environments.get_reservation_repo()()
usecase = DeleteCourtUsecase(repo)
controller = DeleteCourtController(usecase)


def delete_court_presenter(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    httpRequest.data['user_from_authorizer'] = event.get('requestContext', {}).get('authorizer', {}).get('user', None)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()


def lambda_handler(event, context):
    response = delete_court_presenter(event, context)

    return response
