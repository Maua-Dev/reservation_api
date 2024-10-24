from typing import Any
from .update_court_usecase import UpdateCourtUsecase
from .update_court_viewmodel import UpdateCourtViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import BadRequest, OK, InternalServerError, NotFound
from src.shared.domain.enums.status_enum import STATUS


class UpdateCourtController:

    def __init__(self, usecase: UpdateCourtUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest):
        try:
            if request.data.get('number') is None:
                raise MissingParameters('number')

            if type(request.data.get('number')) is not int:
                raise WrongTypeParameter(fieldName='number', fieldTypeExpected=int,
                                         fieldTypeReceived=type(request.data.get('number')))

            status_str = request.data.get('status')

            if status_str:
                if status_str not in [status_type.value for status_type in STATUS]:
                    raise EntityError('status')

            photo_str = request.data.get('photo')

            if photo_str:
                if type(photo_str) is not str:
                    raise WrongTypeParameter(fieldName='photo', fieldTypeExpected=str,
                                             fieldTypeReceived=type(request.data.get('photo')))

            court = self.usecase(
                number=request.data.get('number'),
                status=STATUS[status_str] if status_str is not None else None,
                photo=photo_str
            )

            viewmodel = UpdateCourtViewmodel(court=court)

            return OK(viewmodel.to_dict())

        except NoItemsFound as err:
            return NotFound(body=err.message)

        except MissingParameters as err:
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)

        except EntityError as err:
            return BadRequest(body=err.message)

        except Exception as err:
            return InternalServerError(body=err.args[0])