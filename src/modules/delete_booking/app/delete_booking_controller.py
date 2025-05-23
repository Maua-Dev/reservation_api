from typing import Any
from src.shared.domain.entities.booking import Booking
from .delete_booking_usecase import DeleteBookingUsecase
from .delete_booking_viewmodel import DeleteBookingViewModel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Created, InternalServerError, NotFound
from src.shared.domain.enums.sport import SPORT

class DeleteBookingController:
    
    def __init__(self, usecase:  DeleteBookingUsecase):
        self.usecase = usecase
        
    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('booking_id') is None:
                raise MissingParameters('booking_id')
            booking = self.usecase(booking_id=request.data.get('booking_id'))
            viewmodel = DeleteBookingViewModel(booking)
            
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