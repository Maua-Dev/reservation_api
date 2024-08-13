import abc
from src.shared.domain.enums.status_enum import STATUS
from typing import Optional
from src.shared.helpers.errors.domain_errors import EntityError

# COURT (quadras + campo terao um ENUM status, AVAILABLE  MAINTENANCE)
# number -> int (no minimo 1 no maximo 4)
# status -> enum
# photo -> optional[String]
# is_field -> bool (false pra number de court 1 a 3 e true pra number 4, verificar na entidade)

class Court(abc.ABC):
    number: int
    status: STATUS
    is_field: bool
    photo: Optional[str] = None
    MIN_PHOTO_LENGTH = 3

    def __init__(self, number: int, status: STATUS, is_field: bool, photo: Optional[str] = None):
        #validações da entidade
        if not self.validate_number(number):
            raise EntityError('number')
        self.number = number

        if type(status) != STATUS:
            raise EntityError('status')
        self.status = status
        
        if type(is_field) != bool:
            raise EntityError('is_field')
        self.is_field = is_field

        if not self.validate_photo(photo):
            raise EntityError('photo')
        self.photo = photo
    
    
    @staticmethod
    def validate_number(number: int):
        if type(number) != int or number < 1 or number > 4:
            return False
        return True
    
    
    @staticmethod
    def validade_status(status: STATUS):
        if not isinstance(status, STATUS):
            return False
        return True
    
    @staticmethod
    def determin_is_field(is_field, number) -> bool:
       if is_field and number == 4:
           return True
       return False

    @staticmethod
    def validate_photo(photo: str)->bool:
        if photo is None: return True
        if type(photo) != str: return False
        if len(photo) <= Court.MIN_PHOTO_LENGTH:
            return False
        return True

