from src.shared.domain.entities.court import Court
from src.shared.domain.enums.status_enum import STATUS


class CourtViewmodel:
    number: int
    status: STATUS
    is_field: bool
    photo: str

    def __init__(self, court: Court):
        self.number = court.number
        self.status = court.status
        self.is_field = court.is_field
        self.photo = court.photo
        
    def to_dict(self):
        return {
            'number': self.number,
            'status': self.status,
            'is_field': self.is_field,
            'photo': self.photo
        }
class CreateCourtViewmodel:
    court:Court

    def __init__(self, court: Court):
        self.court = court
        
    def to_dict(self) -> dict:
        return {
            'court' : CourtViewmodel(self.court).to_dict(),
            'message': 'the court was created'
        }