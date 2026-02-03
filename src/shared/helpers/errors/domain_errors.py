from src.shared.helpers.errors.base_error import BaseError


class EntityError(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Field {message} is not valid')

class EntityParameterTypeError(EntityError):
    def __init__(self, message: str):
        super().__init__(message)
        self.__message = message

    @property
    def message(self):
        return self.__message
    
class EntitySchedulePeriodError(BaseError):
    def __init__(self):
        super().__init__(f'The scheduling period must not exceed 3 months')
        
class EntityParameterOrderDatesError(EntityError):
    def __init__(self, start_date: int, end_date: int):
        super().__init__(f'Initial date {start_date} must be less than or equal to end date {end_date}')

class EntityParameterError(EntityError):
    def __init__(self, message: str):
        super().__init__(message)
        self.__message = message

    @property
    def message(self):
        return self.__message

class EntityParameterTimeError(BaseError):
    def __init__(self, start_Date: int, end_date: int):
        super().__init__(f'Initial time {start_Date} must be less than or equal to end time {end_date}')

