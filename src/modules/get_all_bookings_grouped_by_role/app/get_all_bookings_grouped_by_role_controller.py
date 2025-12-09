from .get_all_bookings_grouped_by_role_usecase import GetAllBookingsGroupedByRoleUsecase
from .get_all_bookings_grouped_by_role_viewmodel import GetAllBookingsGroupedByRoleViewmodel
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError, NotFound


class GetAllBookingsGroupedByRoleController:

    def __init__(self, usecase: GetAllBookingsGroupedByRoleUsecase):
        
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        
        try:

            response = self.usecase()

            return OK(GetAllBookingsGroupedByRoleViewmodel(response).to_dict())
        
        except NoItemsFound as err:
            return NotFound(body=err.message)
        except Exception as err:
            return InternalServerError(body=err.args[0])