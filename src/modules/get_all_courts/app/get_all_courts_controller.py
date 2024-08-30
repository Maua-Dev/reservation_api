from typing import Any
from .get_all_courts_usecase import GetAllCourtsUsecase
from .get_all_courts_viewmodel import GetAllCourtsViewModel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import BadRequest, OK, InternalServerError


class GetAllCourtsController:

    def __init__(self, usecase: GetAllCourtsUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest):
        try:
            courts = self.usecase()
            viewmodel = GetAllCourtsViewModel(courts).to_dict()
            return OK(viewmodel)
        except EntityError as err:
            return BadRequest(body=err.message)
        
        except Exception as err:
            return InternalServerError(body=err.args[0])