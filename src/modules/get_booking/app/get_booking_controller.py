from .get_booking_viewmodel import GetBookingViewmodel
from .get_booking_usecase import GetBookingUseCase
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter, AuthorizerError
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import BadRequest, OK, NotFound, InternalServerError


class GetBookingController:
    def __init__(self, usecase: GetBookingUseCase):
        self.usecase = usecase

    def __call__(self, request: IRequest):
        try:
            user = request.data.get('user_from_authorizer')
            if user is None:
                raise AuthorizerError()

            if request.data.get('booking_id') is None:
                raise MissingParameters('booking_id')

            booking_id = request.data.get('booking_id')

            if type(booking_id) is not str:
                raise WrongTypeParameter(
                    'booking_id',
                    'str',
                    (type(booking_id)).__name__
                )

            result = self.usecase(
                booking_id=booking_id,
                requester_role=user.get('role')
            )
            booking_viewmodel = GetBookingViewmodel(result['booking'], result['owner'])
            return OK(booking_viewmodel.to_dict())

        except MissingParameters as err:
            return BadRequest(body=err.message)

        except AuthorizerError as err:
            return BadRequest(body=err.message)

        except EntityError as err:
            return BadRequest(body=err.message)

        except NoItemsFound as err:
            return NotFound(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)

        except Exception as err:
            return InternalServerError(body=err.args[0])
