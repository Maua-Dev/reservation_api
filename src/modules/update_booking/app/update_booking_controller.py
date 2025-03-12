from src.modules.update_booking.app.update_booking_usecase import UpdateBookingUsecase

from src.modules.update_booking.app.update_booking_viewmodel import UpdateBookingViewmodel
from src.shared.domain.enums.sport import SPORT
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError

class UpdateBookingController: 
    def __init__(self, update_booking_use_case: UpdateBookingUsecase):
        self.UpdateBookingUsecase = update_booking_use_case

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('booking_id') is None:
                raise MissingParameters('booking_id')
                        
            if request.data.get('start_date') is None:
                raise MissingParameters('start_date')
            
            if request.data.get('end_date') is None:
                raise MissingParameters('end_date')
            
            if request.data.get('court_number') is None:
                raise MissingParameters('court_number')
            
            if request.data.get('sport') is None:
                raise MissingParameters('sport')
            
            sport = request.data.get('sport')

            if sport not in [sport_type.value for sport_type in SPORT]:
                raise EntityError('sport')
            
            if request.data.get('materials') is None:
                raise MissingParameters('materials')
            
            booking = self.UpdateBookingUsecase(booking_id=request.data.get('booking_id'),
                                                start_date=request.data.get('start_date'),
                                                end_date=request.data.get('end_date'),
                                                court_number=request.data.get('court_number'),
                                                sport=SPORT(sport),
                                                materials=request.data.get('materials'))
            
            viewmodel = UpdateBookingViewmodel(booking=booking)
            
            return OK(viewmodel.to_dict())

        except MissingParameters as err:
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)

        except EntityError as err:
            return BadRequest(body=err.message)
        
        except Exception as err:
            return InternalServerError(body=err.args[0])