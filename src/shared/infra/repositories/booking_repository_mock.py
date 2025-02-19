from typing import List
from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.sport import SPORT
from src.shared.domain.repositories.booking_repository_interface import IBookingRepository


class BookingRepositoryMock(IBookingRepository):
    bookings: List[Booking]

    def __init__(self):
        self.bookings = [
            Booking(
                start_date=1634576165000,
                end_date=1634583365000,
                court_number=1,
                sport=SPORT.TENNIS,
                user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
                booking_id='c2d3bebf-dc0d-4fc1-861c-506a40cc2925',
                materials=['Raquete', 'Bola', 'Rede', 'Tenis']
            ),

            Booking(
                start_date=1634563800000,
                end_date=1634567400000,
                court_number=2,
                sport=SPORT.FOOTBALL,
                user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
                booking_id='c2d3bebf-dc0d-4fc1-861c-506a40cc2925',
                materials=['Bola', 'Chuteira']
            ),

            Booking(
                start_date=1634569200000,
                end_date=1634571000000,
                court_number=3,
                sport=SPORT.BASKETBALL,
                user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
                booking_id='c2d3bebf-dc0d-4fc1-861c-506a40cc2925',
                materials=['Bola']
            ),

            Booking(
                start_date=1634574600000,
                end_date=1634578200000,
                court_number=4,
                sport=SPORT.VOLLEYBALL,
                user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
                booking_id='c2d3bebf-dc0d-4fc1-861c-506a40cc2925',
                materials=['Bola', 'Rede']
            ),

            Booking(
                start_date=1634580000000,
                end_date=1634581800000,
                court_number=5,
                sport=SPORT.HANDBALL,
                user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
                booking_id='c2d3bebf-dc0d-4fc1-861c-506a40cc2925',
                materials=['Bola']
            ),

            Booking(
                start_date=1634583600000,
                end_date=1634585400000,
                court_number=5,
                sport=SPORT.FUTSAL,
                user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
                booking_id='c2d3bebf-dc0d-4fc1-861c-506a40cc2925',
                materials=['Bola', 'Chuteira']
            ),

            Booking(
                start_date=1634587200000,
                end_date=1634589000000,
                court_number=5,
                sport=SPORT.RUGBY,
                user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
                booking_id='c2d3bebf-dc0d-4fc1-861c-506a40cc2925',
                materials=['Bola', 'Tenis', 'Capacete']
            ),

            Booking(
                start_date=1634590800000,
                end_date=1634592600000,
                court_number=5,
                sport=SPORT.PING_PONG,
                user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
                booking_id='c2d3bebf-dc0d-4fc1-861c-506a40cc2925',
                materials=['Raquete', 'Bola']
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
                       materials: List[str] = None
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

        return booking

    def get_booking(self, booking_id: str):
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                return booking
        return None

    def delete_booking(self, booking_id: str):
        booking = self.get_booking(booking_id)
        if booking is not None:
            self.bookings.remove(booking)
            return booking
        return None

    def get_all_bookings(self) -> List[Booking]:
        return self.bookings
