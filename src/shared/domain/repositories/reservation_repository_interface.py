from abc import ABC, abstractmethod


class IReservationRepository(ABC):

    @abstractmethod
    def create_court(self):
        pass

    @abstractmethod
    def delete_court(self):
        '''
        If courts exists, deletes it and returns it
        else returns None
        '''
        pass