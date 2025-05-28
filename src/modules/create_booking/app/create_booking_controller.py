import json

from .create_booking_usecase import CreateBookingUsecase
from .create_booking_viewmodel import CreateBookingViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter, AuthorizerError
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, InvalidSchedule
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import Created, BadRequest, InternalServerError


class CreateBookingController:

    def __init__(self, create_booking_use_case: CreateBookingUsecase):
        self.create_booking_use_case = create_booking_use_case

    def __call__(self, request: IRequest):

        user_from_authorizer = request.data.get('user_from_authorizer', None)

        if not isinstance(request.data.get('user_from_authorizer'), dict):

            user_from_authorizer = json.loads(request.data.get('user_from_authorizer'))

        if user_from_authorizer is None:
            raise AuthorizerError()

        start_date = request.data.get('start_date', None)
        end_date = request.data.get('end_date', None)
        court_number = request.data.get('court_number', None)
        sport = request.data.get('sport', None)
        user_id = user_from_authorizer.get('id', None)
        materials = request.data.get('materials', None)

        try:

            if start_date is None:
                raise MissingParameters('start_date')
            if not isinstance(start_date, int):
                raise WrongTypeParameter(fieldName='start_date',
                                         fieldTypeExpected='int',
                                         fieldTypeReceived=type(start_date).__name__)

            if end_date is None:
                raise MissingParameters('end_date')
            if not isinstance(end_date, int):
                raise WrongTypeParameter(fieldName='end_date',
                                         fieldTypeExpected='int',
                                         fieldTypeReceived=type(end_date).__name__)

            if court_number is None:
                raise MissingParameters('court_number')
            if not isinstance(court_number, int):
                raise WrongTypeParameter(fieldName='court_number',
                                         fieldTypeExpected='int',
                                         fieldTypeReceived=type(court_number).__name__)

            if sport is None:
                raise MissingParameters('sport')
            if not isinstance(sport, str):
                raise WrongTypeParameter(fieldName='sport',
                                         fieldTypeExpected='str',
                                         fieldTypeReceived=type(sport).__name__)

            if user_id is None:
                raise MissingParameters('user_id')
            if not isinstance(user_id, str):
                raise WrongTypeParameter(fieldName='user_id',
                                         fieldTypeExpected='str',
                                         fieldTypeReceived=type(user_id).__name__)

            if materials is None:
                raise MissingParameters('materials')
            if not isinstance(materials, list):
                raise WrongTypeParameter(fieldName='materials',
                                         fieldTypeExpected='list',
                                         fieldTypeReceived=type(materials).__name__)

            booking = self.create_booking_use_case(
                start_date=start_date,
                end_date=end_date,
                court_number=court_number,
                sport=sport,
                user_id=user_id,
                materials=materials
            )

            viewmodel = CreateBookingViewmodel(booking=booking)

            return Created(viewmodel.to_dict())

        except InvalidSchedule as err:
            return BadRequest(body=err.message)

        except MissingParameters as err:
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)

        except DuplicatedItem as err:
            return BadRequest(body=err.message)

        except EntityError as err:
            return BadRequest(body=err.message)

        except ValueError as err:
            return BadRequest(body=err.args[0])

        except Exception as err:
            return InternalServerError(body=err.args[0])
