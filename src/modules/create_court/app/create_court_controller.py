from typing import Any
from .create_court_usecase import CreateCourtUsecase
from .create_court_viewmodel import CreateCourtViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import BadRequest, Created, InternalServerError
from src.shared.domain.enums.status_enum import STATUS


class CreateCourtController:

    def __init__(self, usecase: CreateCourtUsecase):
        self.usecase = usecase


    def __call__(self, request: IRequest):
        try:
            if  request.data.get('number') is None:
                raise MissingParameters('number')
            
            if request.data.get('status') is None:
                raise MissingParameters('status')
            
            if request.data.get('is_field') is None:
                raise MissingParameters('is_field')
            
            if type(request.data.get('number')) is not int:
                raise WrongTypeParameter(fieldName = 'number', fieldTypeExpected = int, fieldTypeReceived = type(request.data.get('number')))

            status_str = request.data.get('status')
            if status_str not in [status_type.value for status_type in STATUS]:
                raise EntityError('status')
            status = STATUS[status_str]

            if type(request.data.get('is_field')) is not bool:
                raise WrongTypeParameter(fieldName='is_field', fieldTypeExpected= bool, fieldTypeReceived=type(request.data.get('is_field')))
            
            if request.data.get('photo') is not None and type(request.data.get('photo')) is not str:
                raise WrongTypeParameter(fieldName= 'photo', fieldTypeExpected= str, fieldTypeReceived= type(request.data.get('photo')))
            
            court = self.usecase(
                number= request.data.get('number'),
                status= status,
                is_field= request.data.get('is_field'),
                photo= request.data.get('photo')
            )

            viewmodel = CreateCourtViewmodel(court= court)

            return Created(viewmodel.to_dict())

        except MissingParameters as err:
            return BadRequest(body=err.message)
        
        except WrongTypeParameter as err:
            return BadRequest(body=err.message)
        
        except DuplicatedItem as err:
            return BadRequest(body=err.message)
        
        except EntityError as err:
            return BadRequest(body=err.message)
        
        except Exception as err:
            return InternalServerError(body=err.args[0])
        
        
        