from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import OK

class HealthCheckController:
  def __call__(self, req: IRequest):
    return OK("I'm alive")