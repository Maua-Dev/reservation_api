from src.modules.get_all_users.app.get_all_users_usecase import GetAllUsersUseCase
from src.modules.get_all_users.app.get_all_users_viewmodel import GetAllUsersViewModel
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError


class GetAllUsersController:
    def __init__(self, usecase: GetAllUsersUseCase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:

        try:
            users = self.usecase()
            viewmodel = GetAllUsersViewModel(users)

            return OK(viewmodel.to_dict())
        
        except EntityError as e:
            return BadRequest(body=e.message)
        
        except MissingParameters as err:
            return BadRequest(body=err.message)
        
        except Exception as err:
            return InternalServerError(body=str(err))