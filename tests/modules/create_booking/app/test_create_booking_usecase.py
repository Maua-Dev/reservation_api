import pytest

from src.modules.create_booking.app.create_booking_usecase import CreateBookingUsecase
from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.sport import SPORT
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock


class TestCreateBookingUsecase:

    def test_create_booking_usecase(self):

        booking = Booking(
            start_date=1634576165000,
            end_date=1634583365000,
            court_number=1,
            sport=SPORT.TENNIS,
            user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
            booking_id='e1d3bebf-dc0d-4fc1-861c-506a40cc2925',
            materials=['Raquete', 'Bola', 'Rede', 'Tenis']
        )

        booking_repository = BookingRepositoryMock()

        usecase = CreateBookingUsecase(booking_repository)

        response = usecase(
            start_date=1634576165000,
            end_date=1634583365000,
            court_number=1,
            sport="Tennis",
            user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
            booking_id='e1d3bebf-dc0d-4fc1-861c-506a40cc2925',
            materials=['Raquete', 'Bola', 'Rede', 'Tenis']
        )

        assert booking == response

    def test_create_booking_usecase_invalid_sport(self):

        with pytest.raises(ValueError) as e:

            booking_repository = BookingRepositoryMock()

            usecase = CreateBookingUsecase(booking_repository)

            response = usecase(
                start_date=1634576165000,
                end_date=1634583365000,
                court_number=1,
                sport="Invalid sport but string",
                user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
                booking_id='e1d3bebf-dc0d-4fc1-861c-506a40cc2925',
                materials=['Raquete', 'Bola', 'Rede', 'Tenis']
            )

    def test_create_booking_usecase_invalid_materials(self):

        with pytest.raises(ValueError) as e:

            booking_repository = BookingRepositoryMock()

            usecase = CreateBookingUsecase(booking_repository)

            response = usecase(
                start_date=1634576165000,
                end_date=1634583365000,
                court_number=1,
                sport="Tennis",
                user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
                booking_id='e1d3bebf-dc0d-4fc1-861c-506a40cc2925',
                materials=[1, 2, 3]
            )

