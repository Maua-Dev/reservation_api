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
            'status': self.status.value,
            'is_field': self.is_field,
            'photo': self.photo
        }

class DeleteCourtViewModel:
    court: Court
    
    def __init__(self, court: Court):
        self.court_viewmodel = CourtViewmodel(court)

    def to_dict(self):
        return{
            'court' : self.court_viewmodel.to_dict(),
            'message': 'the court was deleted'
        }