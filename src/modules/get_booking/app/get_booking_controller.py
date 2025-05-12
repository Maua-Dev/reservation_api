from .get_booking_viewmodel import GetBookingViewmodel
from .get_booking_usecase import GetBookingUseCase
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter, EmptyQueryParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import BadRequest, OK, NotFound, InternalServerError


class GetBookingController:
    def __init__(self, usecase: GetBookingUseCase):
        self.usecase = usecase

    def __call__(self, request: IRequest):
        try:

            booking_id = request.data.get('booking_id', None)

            if booking_id is not None:
                if not isinstance(booking_id, str):
                    raise WrongTypeParameter('booking_id',
                                             fieldTypeReceived=type(booking_id).__name__,
                                             fieldTypeExpected='str')
            else:
                raise MissingParameters('booking_id')
                
            booking = self.usecase(
                booking_id=booking_id
            )
            booking_viewmodel = GetBookingViewmodel(booking)
            return OK(booking_viewmodel.to_dict())
        
        except EmptyQueryParameters as err:
            return BadRequest(body=err.message)

        except MissingParameters as err:
            return BadRequest(body=err.message)
        
        except EntityError as err:
            return BadRequest(body=err.message)

        except NoItemsFound as err:
            return NotFound(body=err.message)
        
        except WrongTypeParameter as err:
            return BadRequest(body=err.message)

        except Exception as err:
            return InternalServerError(body=err.args[0])