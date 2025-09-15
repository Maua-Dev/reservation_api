from src.shared.domain.enums.type import BOOKING_TYPE
from .update_booking_usecase import UpdateBookingUsecase
from .update_booking_viewmodel import UpdateBookingViewmodel
from src.shared.domain.enums.sport import SPORT
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Forbidden, InternalServerError, NotFound
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound

class UpdateBookingController: 
    def __init__(self, update_booking_use_case: UpdateBookingUsecase):
        self.UpdateBookingUsecase = update_booking_use_case

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('booking_id') is None:
                raise MissingParameters('booking_id')
            
            if request.data.get('user_from_authorizer') is None:
                raise MissingParameters('user authorizer')  
            
            booking_id = request.data.get('booking_id')
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')
            court_number = request.data.get('court_number')
            sport_value = request.data.get('sport')
            materials = request.data.get('materials')
            booking_type = request.data.get('type')
            user = request.data.get('user_from_authorizer')

            if not isinstance(booking_id, str):
                raise WrongTypeParameter('booking_id', 'str', type(booking_id).__name__)

            if start_date is not None and not isinstance(start_date, int):
                raise WrongTypeParameter('start_date', 'int', type(start_date).__name__)

            if end_date is not None and not isinstance(end_date, int):
                raise WrongTypeParameter('end_date', 'int', type(end_date).__name__)

            if court_number is not None and not isinstance(court_number, int):
                raise WrongTypeParameter('court_number', 'int', type(court_number).__name__)

            sport = None
            if sport_value is not None:
                if not isinstance(sport_value, str):
                    raise WrongTypeParameter('sport', 'str', type(sport_value).__name__)
                
                if sport_value not in [sport_type.value for sport_type in SPORT]:
                    raise EntityError('sport')
                
                sport = SPORT(sport_value)

            if booking_type is not None:
                if not isinstance(booking_type, str):
                    raise WrongTypeParameter('type', 'str', type(booking_type).__name__)
                if booking_type not in [type.value for type in BOOKING_TYPE]:
                    raise EntityError('type')
                
                booking_type = BOOKING_TYPE(booking_type)

            
            if materials is not None and not isinstance(materials, list):
                raise WrongTypeParameter('materials', 'list', type(materials).__name__)
          
            
            booking = self.UpdateBookingUsecase(
                booking_id=booking_id,
                user=user,
                start_date=start_date,
                end_date=end_date,
                court_number=court_number,
                sport=sport,
                materials=materials,
                booking_type=booking_type
            )
            
            viewmodel = UpdateBookingViewmodel(booking=booking)
            
            return OK(viewmodel.to_dict())

        except MissingParameters as err:
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)

        except EntityError as err:
            return BadRequest(body=err.message)
        
        except NoItemsFound as err:
            return NotFound(body=f"Booking not found: {err.message}")
        
        except ForbiddenAction as err:
            return Forbidden(body=err.message)
        
        except Exception as err:
            return InternalServerError(body=err.args[0])