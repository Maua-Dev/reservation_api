from .get_court_viewmodel import GetCourtViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from .get_court_usecase import GetCourtUsecase
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import BadRequest, OK, NotFound, InternalServerError


class GetCourtController:
    def __init__(self, usecase: GetCourtUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest):
        try:
            if request.data.get('number') is None:
                raise MissingParameters('number')
            
            court  = self.usecase(
                number= request.data.get('number')
            )       
            court_viewmodel = GetCourtViewmodel(court= court)

            return OK(court_viewmodel)


        except MissingParameters as err:
            return BadRequest(body=err.message)
        
        except EntityError as err:
            return BadRequest(body=err.message)

        except NoItemsFound as err:
            return NotFound(body=err.message)
        
        except Exception as err:
            return InternalServerError(body=err.message) 

       