from typing import List
from src.shared.domain.entities.court import Court
from src.shared.domain.enums.status_enum import STATUS
from src.shared.domain.repositories.reservation_repository_interface import IReservationRepository


class ReservationRepositoryMock(IReservationRepository):
    courts: List[Court]

    def __init__(self):
        self.courts = [
            Court(
                number = 1,
                status = STATUS.AVAILABLE,
                is_field = False,
                photo = 'https://www.linkedin.com/in/giovanna-albuquerque-16917a245/'
            ),
           
            Court(
                number = 2,
                status = STATUS.AVAILABLE,
                is_field = False,
                photo = 'https://www.linkedin.com/in/giovanna-albuquerque-16917a245/'
            ),

            Court(
                number = 3,
                status = STATUS.UNAVAILABLE,
                is_field = False,
                photo = 'https://super.abril.com.br/mundo-estranho/os-poneis-sao-cavalos-anoes'
            )  ,

            Court(
                number = 4,
                status = STATUS.MAINTENANCE,
                is_field = True,
                photo = None
            )                                                                                                             
        ]

    def create_court(self, court: Court):
        self.courts.append(court)
        return court
    
    def get_court(self, number: int):
        for court in self.courts:
            if court.number == number:
                return court
        return None