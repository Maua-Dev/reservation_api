from typing import List, Optional
from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.sport import SPORT
from src.shared.domain.enums.type import BOOKING_TYPE
from src.shared.domain.repositories.booking_repository_interface import IBookingRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction


class BookingRepositoryMock(IBookingRepository):
    bookings: List[Booking]

    def __init__(self):
        self.bookings = [
            Booking(
                start_date=1634576165000,
                end_date=1634583365000,
                court_number=1,
                sport=SPORT.TENNIS,
                user_id='1f25448b-3429-4c19-8287-d9e64f17bc3a',
                booking_id='b1d3bebf-dc0d-4fc1-861c-506a40cc2925',
                materials=['Raquete', 'Bola', 'Rede', 'Tenis'], 
                booking_type=BOOKING_TYPE.TRAINING
            ),

            Booking(
                start_date=1634563800000,
                end_date=1634567400000,
                court_number=2,
                sport=SPORT.FOOTBALL,
                user_id='c07e0862-3c07-4227-ab0f-511a267cb7ff',
                booking_id='b2d3bebf-dc0d-4fc1-861c-506a40cc2925',
                materials=['Bola', 'Chuteira'], 
                booking_type=BOOKING_TYPE.TRAINING
            ),

            Booking(
                start_date=1634569200000,
                end_date=1634571000000,
                court_number=3,
                sport=SPORT.BASKETBALL,
                user_id='d351a9b1-937f-423c-a9d1-9929b5795be1',
                booking_id='b3d3bebf-dc0d-4fc1-861c-506a40cc2925',
                materials=['Bola'], 
                booking_type=BOOKING_TYPE.COMMON
            ),

            Booking(
                start_date=1634574600000,
                end_date=1634578200000,
                court_number=4,
                sport=SPORT.VOLLEYBALL,
                user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
                booking_id='b4d3bebf-dc0d-4fc1-861c-506a40cc2925',
                materials=['Bola', 'Rede'], 
                booking_type=BOOKING_TYPE.COMMON
            ),

            Booking(
                start_date=1634580000000,
                end_date=1634581800000,
                court_number=5,
                sport=SPORT.HANDBALL,
                user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
                booking_id='b5d3bebf-dc0d-4fc1-861c-506a40cc2925',
                materials=['Bola'], 
                booking_type=BOOKING_TYPE.TRAINING
            ),

            Booking(
                start_date=1634583600000,
                end_date=1634585400000,
                court_number=5,
                sport=SPORT.FUTSAL,
                user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
                booking_id='b6d3bebf-dc0d-4fc1-861c-506a40cc2925',
                materials=['Bola', 'Chuteira'], 
                booking_type=BOOKING_TYPE.TRAINING
            ),

            Booking(
                start_date=1634587200000,
                end_date=1634589000000,
                court_number=5,
                sport=SPORT.RUGBY,
                user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
                booking_id='b7d3bebf-dc0d-4fc1-861c-506a40cc2925',
                materials=['Bola', 'Tenis', 'Capacete'], 
                booking_type=BOOKING_TYPE.TRAINING
            ),

            Booking(
                start_date=1634590800000,
                end_date=1634592600000,
                court_number=5,
                sport=SPORT.PING_PONG,
                user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
                booking_id='b8d3bebf-dc0d-4fc1-861c-506a40cc2925',
                materials=['Raquete', 'Bola'], 
                booking_type=BOOKING_TYPE.TRAINING
            ),
        ]

    def create_booking(self, booking: Booking) -> Booking:
        self.bookings.append(booking)
        return booking

    def update_booking(self,
                       booking_id: str,
                       start_date: int = None,
                       end_date: int = None,
                       court_number: int = None,
                       sport: SPORT = None,
                       materials: List[str] = None,
                       booking_type: BOOKING_TYPE = None
                       ) -> Booking:

        booking = self.get_booking(booking_id)

        if booking is None:
            raise ValueError("Booking not found")

        if start_date is not None:
            booking.start_date = start_date
        if end_date is not None:
            booking.end_date = end_date
        if court_number is not None:
            booking.court_number = court_number
        if sport is not None:
            booking.sport = sport
        if materials is not None:
            booking.materials = materials
        if booking_type is not None:
            booking.booking_type = booking_type
        return booking

    def get_booking(self, booking_id: str):
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                return booking
        return None
    
    def get_bookings(self,
                     booking_id: Optional[str] = None,
                     user_id: Optional[str] = None,
                     sport: Optional[str] = None,
                     court_number: Optional[int] = None,
                     end_date: Optional[int] = None,
                     start_date: Optional[int] = None,
                     booking_type: Optional[str] = None) -> List[Optional[Booking]]:

        filters = locals().copy()
        filters.pop('self')
        filters.pop('end_date')
        filters.pop('start_date')

        filters = {k: v for k, v in filters.items() if v is not None}

        bookings = []

        for booking in self.bookings:
            booking_dict = booking.__dict__
            if start_date and end_date:
                if all(
                    booking_dict.get(key) == value for key, value in filters.items()
                ) and booking.start_date >= start_date and booking.end_date <= end_date:
                    bookings.append(booking)
            else:
                if all(
                    booking_dict.get(key) == value for key, value in filters.items()
                ):
                    bookings.append(booking)

        return bookings

    def delete_booking(self, booking_id: str, user):
        booking = self.get_booking(booking_id)

        user_role = user.get('role')

        if booking is not None:

            if user_role == 'ADMIN':
                self.bookings.remove(booking)
                return booking

            elif user_role == 'STUDENT':

                if booking.user_id == user.get('user_id'):

                    self.bookings.remove(booking)
                    return booking
                
                else:
                    raise ForbiddenAction('user id')

        return None

    def get_all_bookings(self) -> List[Booking]:
        return self.bookings

    def get_all_bookings_by_date_range(self, initial_date, final_date):

        all_bookings = []
        for booking in self.bookings:
            if initial_date <= booking.start_date <= final_date:
                all_bookings.append(booking)

        return all_bookings
    
    def get_all_users(self) -> List[str]:
        users_id = list(set([booking.user_id for booking in self.bookings]))
        return users_id
    
    def send_user_email(self, user) -> bool:
        print('ENVIAR E-MAIL PARA O USUÁRIO')

        return True
