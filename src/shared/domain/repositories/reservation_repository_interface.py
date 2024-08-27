from abc import ABC, abstractmethod
from src.shared.domain.entities.court import Court
from src.shared.domain.enums.status_enum import STATUS


class IReservationRepository(ABC):

    @abstractmethod
    def create_court(self, court: Court) -> Court:
        '''
        If court does not exist, creates it and returns it
        '''
        pass

    def update_court(self,
                     number: int,
                     status: STATUS = None,
                     is_field: bool = None,
                     photo: str = None) -> Court:
        '''
        If court exists, updates it and returns it
        '''
        pass

    @abstractmethod
    def get_court(self, number: int):
        '''
        If the court exists, returns it, else returns None
        '''
        pass
      
    @abstractmethod
    def delete_court(self):
        '''
        If courts exists, deletes it and returns it
        else returns None
        '''
        pass