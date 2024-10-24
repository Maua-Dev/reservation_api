from typing import List
from src.shared.domain.entities.court import Court
from src.shared.domain.enums.status_enum import STATUS
from src.shared.domain.repositories.reservation_repository_interface import IReservationRepository


class ReservationRepositoryMock(IReservationRepository):
    courts: List[Court]

    def __init__(self):
        self.courts = [
            Court(
                number=1,
                status=STATUS.AVAILABLE,
                is_field=False,
                photo='https://www.linkedin.com/in/giovanna-albuquerque-16917a245/'
            ),

            Court(
                number=2,
                status=STATUS.AVAILABLE,
                is_field=False,
                photo='https://www.linkedin.com/in/giovanna-albuquerque-16917a245/'
            ),

            Court(
                number=3,
                status=STATUS.UNAVAILABLE,
                is_field=False,
                photo='https://super.abril.com.br/mundo-estranho/os-poneis-sao-cavalos-anoes'
            ),

            Court(
                number = 4,
                status = STATUS.MAINTENANCE,
                is_field = True,
                photo = None
            ),

            Court(
                number = 5,
                status = STATUS.AVAILABLE,
                is_field = False,
                photo = 'https://www.linkedin.com/in/vinicius-berti-a80354209/'
            ),                                                                                                              

        ]

    def create_court(self, court: Court):
        self.courts.append(court)
        return court

    def update_court(self,
                     number: int,
                     status: STATUS = None,
                     photo: str = None):

        court = self.get_court(number)

        if court is None:
            return None

        if status is not None:
            court.status = status
        if photo is not None:
            court.photo = photo

        return court

    def get_court(self, number: int):
        for court in self.courts:
            if court.number == number:
                return court
        return None
    
    def delete_court(self, number: str) -> Court:
        for i in range(len(self.courts)):
            if self.courts[i].number == number:
                return self.courts.pop(i)
        return None
    
    def get_all_courts(self):
        return self.courts

#Eh o brancas
