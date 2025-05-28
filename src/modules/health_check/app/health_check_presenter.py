from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .health_check_controller import HealthCheckController

controller = HealthCheckController()

def lambda_handler(event, context):
  httpRequest = LambdaHttpRequest(data = event)
  response = controller(req=httpRequest)
  httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
  
  return httpResponse.toDict()


