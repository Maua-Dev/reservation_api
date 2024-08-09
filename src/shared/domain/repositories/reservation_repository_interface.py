from abc import ABC, abstractmethod


class IReservationRepository(ABC):

    @abstractmethod
    def create_court(self):
        pass