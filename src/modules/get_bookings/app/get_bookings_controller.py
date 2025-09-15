import json

from .get_bookings_viewmodel import GetBookingsViewmodel
from .get_bookings_usecase import GetBookingsUseCase
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter, EmptyQueryParameters, \
    AuthorizerError
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
            booking_type = request.data.get('type', None)

            booking_id = booking_id if booking_id != "" else None
            user_id = user_id if user_id != "" else None
            sport = sport if sport != "" else None
            court_number = court_number if court_number != "" else None
            end_date = end_date if end_date != "" else None
            start_date = start_date if start_date != "" else None
            booking_type = booking_type if booking_type != "" else None

            if not booking_id and not user_id and not sport and not court_number and not end_date and not start_date:
                raise EmptyQueryParameters(
                    'At least one of the filters must be provided: booking_id, user_id, sport, court_number, end_date, start_date')

            if court_number is not None:
                try:
                    court_number = int(court_number)
                except ValueError:
                    raise WrongTypeParameter(fieldName='court_number',
                                             fieldTypeExpected='int',
                                             fieldTypeReceived=court_number)

            if end_date is not None:
                try:
                    end_date = int(end_date)
                except ValueError:
                    raise WrongTypeParameter(fieldName='end_date',
                                             fieldTypeExpected='int',
                                             fieldTypeReceived=end_date)

            if start_date is not None:
                try:
                    start_date = int(start_date)
                except ValueError:
                    raise WrongTypeParameter(fieldName='start_date',
                                             fieldTypeExpected='int',
                                             fieldTypeReceived=start_date)

            booking = self.usecase(
                booking_id=booking_id,
                user_id=user_id,
                sport=sport,
                court_number=court_number,
                end_date=end_date,
                start_date=start_date,
                booking_type=booking_type
            )
            booking_viewmodel = GetBookingsViewmodel(booking)
            return OK(booking_viewmodel.to_dict())

        except AuthorizerError as err:
            return BadRequest(body=err.message)

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
