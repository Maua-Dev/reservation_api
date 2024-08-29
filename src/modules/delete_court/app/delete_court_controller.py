from typing import Any
from src.shared.domain.entities.court import Court
from .delete_court_usecase import DeleteCourtUsecase
from .delete_court_viewmodel import DeleteCourtViewModel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Created, InternalServerError, NotFound
from src.shared.domain.enums.status_enum import STATUS

class DeleteCourtController:
    
    def __init__(self, usecase:  DeleteCourtUsecase):
        self.usecase = usecase
        
    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('number') is None:
                raise MissingParameters('number')
            
            court = self.usecase(number=request.data.get('number'))
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
        
        except Exception as err:
            return InternalServerError(body=err.args[0])