from src.modules.update_booking.app.update_booking_controller import UpdateBookingController
from src.modules.update_booking.app.update_booking_usecase import UpdateBookingUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse


repo = Environments.get_booking_repo()()
usecase = UpdateBookingUsecase(repo)
controller = UpdateBookingController(usecase)

def update_booking_presenter(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(request=httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    
    return httpResponse.toDict()

def lambda_handler(event, context):

    response = update_booking_presenter(event, context)

    return response