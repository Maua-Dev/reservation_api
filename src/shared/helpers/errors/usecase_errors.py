from src.shared.helpers.errors.base_error import BaseError

class NoItemsFound(BaseError):
    def __init__(self, message: str):
        super().__init__(f'No items found for {message}')

class DuplicatedItem(BaseError):
    def __init__(self, message: str):
        super().__init__(f'The item alredy exists for this {message}')
        
class ForbiddenAction(BaseError):
    def __init__(self, message: str):
        super().__init__(f'That action is forbidden for this {message}')

class DynamoDBBaseError(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Error extracting bookings from dynamo: {message}')

class InvalidSchedule(BaseError):
    def __init__(self):
        super().__init__('Court is already booked for the selected time slot or has to have 15 min tolerance')
