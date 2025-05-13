from .get_bookings_viewmodel import GetBookingsViewmodel
from .get_bookings_usecase import GetBookingsUseCase
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter, EmptyQueryParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, DependantFilter
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import BadRequest, OK, NotFound, InternalServerError


class GetBookingsController:
    def __init__(self, usecase: GetBookingsUseCase):
        self.usecase = usecase

    def __call__(self, request: IRequest):
        try:

            booking_id = request.data.get('booking_id', None)
            user_id = request.data.get('user_id', None)
            sport = request.data.get('sport', None)
            court_number = request.data.get('court_number', None)
            end_date = request.data.get('end_date', None)
            start_date = request.data.get('start_date', None)

            booking_id = booking_id if booking_id != "" else None
            user_id = user_id if user_id != "" else None
            sport = sport if sport != "" else None
            court_number = court_number if court_number != "" else None
            end_date = end_date if end_date != "" else None
            start_date = start_date if start_date != "" else None

            if not booking_id and not user_id and not sport and not court_number and not end_date and not start_date:
                raise EmptyQueryParameters('At least one of the filters must be provided: booking_id, user_id, sport, court_number, end_date, start_date')

            if booking_id is not None:
                if not isinstance(booking_id, str):
                    raise WrongTypeParameter('booking_id',
                                             fieldTypeReceived=type(booking_id).__name__,
                                             fieldTypeExpected='str')

            if user_id is not None:
                if not isinstance(user_id, str):
                    raise WrongTypeParameter('user_id',
                                             fieldTypeReceived=type(user_id).__name__,
                                             fieldTypeExpected='str')

            if sport is not None:
                if not isinstance(sport, str):
                    raise WrongTypeParameter('sport',
                                             fieldTypeReceived=type(sport).__name__,
                                             fieldTypeExpected='str')

            if court_number is not None:
                if not isinstance(court_number, int):
                    raise WrongTypeParameter('court_number',
                                             fieldTypeReceived=type(court_number).__name__,
                                             fieldTypeExpected='int')

            if end_date is not None:
                if not isinstance(end_date, int):
                    raise WrongTypeParameter('end_date',
                                             fieldTypeReceived=type(end_date).__name__,
                                             fieldTypeExpected='int')

            if start_date is not None:
                if not isinstance(start_date, int):
                    raise WrongTypeParameter('start_date',
                                             fieldTypeReceived=type(start_date).__name__,
                                             fieldTypeExpected='int')
                
            booking = self.usecase(
                booking_id=booking_id,
                user_id=user_id,
                sport=sport,
                court_number=court_number,
                end_date=end_date,
                start_date=start_date
            )
            booking_viewmodel = GetBookingsViewmodel(booking)
            return OK(booking_viewmodel.to_dict())
        
        except EmptyQueryParameters as err:
            return BadRequest(body=err.message)

        except DependantFilter as err:
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