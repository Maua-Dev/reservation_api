from typing import Any
from .get_all_booking_usecase import GetAllBookingsUsecase
from .get_all_booking_viewmodel import GetAllBookingViewModel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import BadRequest, OK, InternalServerError


class GetAllBookingsController:

    def __init__(self, usecase: GetAllBookingsUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest):
        try:
            bookings = self.usecase()
            viewmodel = GetAllBookingViewModel(bookings).to_dict()
            return OK(viewmodel)
        except EntityError as err:
            return BadRequest(body=err.message)
        
        except Exception as err:
            return InternalServerError(body=err.args[0])