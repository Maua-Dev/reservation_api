import pytest

from src.modules.create_booking.app.create_booking_usecase import CreateBookingUsecase
from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.sport import SPORT
from src.shared.domain.enums.type import BOOKING_TYPE
from src.shared.helpers.errors.usecase_errors import InvalidSchedule, InvalidSchedulePeriod
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock


class TestCreateBookingUsecase:

    def test_create_booking_usecase(self):

        booking = Booking(
            start_date=1234576165000,
            end_date=1234583365000,
            court_number=1,
            sport=SPORT.TENNIS,
            user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
            materials=['Raquete', 'Bola', 'Rede', 'Tenis'],
            booking_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
            booking_type=BOOKING_TYPE.TRAINING
        )

        booking_repository = BookingRepositoryMock()

        usecase = CreateBookingUsecase(booking_repository)

        response = usecase(
            start_date=1234576165000,
            end_date=1234583365000,
            court_number=1,
            sport="Tennis",
            user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
            materials=['Raquete', 'Bola', 'Rede', 'Tenis'],
            booking_type='Training'
        )

        assert response is not None
        assert response.start_date == booking.start_date
        assert response.end_date == booking.end_date
        assert response.court_number == booking.court_number
        assert response.sport == booking.sport
        assert response.user_id == booking.user_id
        assert response.booking_id != booking.booking_id
        assert response.booking_type == booking.booking_type

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
                materials=['Raquete', 'Bola', 'Rede', 'Tenis'],
                booking_type='Training'
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
                materials=[1, 2, 3],
                booking_type='Training'
            )

    def test_create_booking_usecase_invalid_schedule_period(self):
        
        with pytest.raises(InvalidSchedulePeriod) as e:
            
            booking_repository = BookingRepositoryMock()

            usecase = CreateBookingUsecase(booking_repository)
            
            response = usecase(
                start_date=1771897236000,
                end_date=1781897236000,
                court_number=1,
                sport="Tennis",
                user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
                materials=['Raquete', 'Bola', 'Rede', 'Tenis'],
                booking_type='Training'
            )

        assert e.value.message == 'The scheduling period must not exceed 3 months'

    def test_create_booking_usecase_invalid_schedule_overlap(self):

        with pytest.raises(InvalidSchedule) as e:

            booking_repository = BookingRepositoryMock()

            usecase = CreateBookingUsecase(booking_repository)

            response = usecase(
                start_date=1634576165000,
                end_date=1634583365000,
                court_number=1,
                sport="Tennis",
                user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
                materials=["colete"],
                booking_type='Training'
            )

            assert e.value == "Court is already booked for the selected time slot"
            

    