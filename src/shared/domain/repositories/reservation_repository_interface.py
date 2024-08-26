from abc import ABC, abstractmethod
from src.shared.domain.entities.court import Court


class IReservationRepository(ABC):

    @abstractmethod
    def create_court(self, court: Court) -> Court:
        '''
        If court does not exist, creates it and returns it
        '''
        pass

    @abstractmethod
    def get_court(self, number: int):
        '''
        If the court exists, returns it, else returns None
        '''
        pass
      
    @abstractmethod
    def delete_court(self, number: int):
        '''
        If courts exists, deletes it and returns it
        else returns None
        '''
        pass