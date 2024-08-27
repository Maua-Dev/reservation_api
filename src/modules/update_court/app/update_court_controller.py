from typing import Any
from .update_court_usecase import UpdateCourtUsecase
from .update_court_viewmodel import UpdateCourtViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import BadRequest, OK, InternalServerError
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

            if status_str not in [status_type.value for status_type in STATUS]:
                raise EntityError('status')
            status = STATUS[status_str]

            if type(request.data.get('is_field')) is not bool:
                raise WrongTypeParameter(fieldName='is_field', fieldTypeExpected=bool,
                                         fieldTypeReceived=type(request.data.get('is_field')))

            if type(request.data.get('photo')) is not str:
                raise WrongTypeParameter(fieldName='photo', fieldTypeExpected=str,
                                         fieldTypeReceived=type(request.data.get('photo')))

            court = self.usecase(
                number=request.data.get('number'),
                status=status,
                is_field=request.data.get('is_field'),
                photo=request.data.get('photo')
            )

            viewmodel = UpdateCourtViewmodel(court=court)

            return OK(viewmodel.to_dict())

        except MissingParameters as err:
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)

        except EntityError as err:
            return BadRequest(body=err.message)

        except Exception as err:
            return InternalServerError(body=err.args[0])
