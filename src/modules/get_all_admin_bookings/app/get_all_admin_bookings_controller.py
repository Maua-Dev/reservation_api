from .get_all_admin_bookings_usecase import GetAllAdminBookingsUsecase
from .get_all_admin_bookings_viewmodel import GetAllAdminBookingsViewmodel
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import *
from src.shared.helpers.errors.domain_errors import *
from src.shared.helpers.errors.usecase_errors import *



class GetAllAdminBookingsController:
    
    def __init__(self, usecase: GetAllAdminBookingsUsecase):
        
        self.usecase = usecase
        
    def __call__(self, request: IRequest) -> IResponse:
        
        try:
            
            response = self.usecase()
            
            return OK(GetAllAdminBookingsViewmodel(bookings=response).to_dict())
        
        except EntityError as err:
            return BadRequest(body=err.message)
        
        except NoItemsFound as err:
            return BadRequest(body=err.message)
        
        except NoAdminFound as err:
            return BadRequest(body=err.message)
        
        except NoAdminBookingsFound as err:
            return BadRequest(body=err.message)
        
        except Exception as err:
            return InternalServerError(body=err.args[0])