from .delete_court_usecase import DeleteCourtUsecase
from .delete_court_viewmodel import DeleteCourtViewModel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, NotFound

class DeleteCourtController:
    
    def __init__(self, usecase:  DeleteCourtUsecase):
        self.usecase = usecase
        
    def __call__(self, request: IRequest) -> IResponse:
        try:
            
            user = request.data.get("user_from_authorizer")
            number = request.data.get("number")
            
            if user is None:
                raise MissingParameters('user')
            
            if number is not None:
                try:
                    number = int(number)
                except ValueError:
                    raise WrongTypeParameter(fieldName="number",
                                             fieldTypeExpected="int",
                                             fieldTypeReceived=type(number).__name__)
            else:
                raise MissingParameters("number")
            
            court = self.usecase(number=number, role=user.get("role"))
            viewmodel = DeleteCourtViewModel(court)
            
            return OK(viewmodel.to_dict())

        except MissingParameters as err:
            return BadRequest(body=err.message)
        
        except WrongTypeParameter as err:
            return BadRequest(body=err.message)
        
        except NoItemsFound as err:
            return NotFound(body=err.message)
        
        except EntityError as err:
            return BadRequest(body=err.message)
        
        except ForbiddenAction as err:
            return BadRequest(body=err.message)
        
        except Exception as err:
            return InternalServerError(body=err.args[0])