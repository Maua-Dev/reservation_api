import pytest

from src.modules.create_booking.app.create_booking_usecase import CreateBookingUsecase
from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.sport import SPORT
from src.shared.helpers.errors.usecase_errors import InvalidSchedule
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock


class TestCreateBookingUsecase:

    def test_create_booking_usecase(self):

        booking = Booking(
            start_date=1234576165000,
            end_date=1234583365000,
            court_number=1,
            sport=SPORT.TENNIS,
            user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
            booking_id='e1d3bebf-dc0d-4fc1-861c-506a40cc2925',
            materials=['Raquete', 'Bola', 'Rede', 'Tenis']
        )

        booking_repository = BookingRepositoryMock()

        usecase = CreateBookingUsecase(booking_repository)

        response = usecase(
            start_date=1234576165000,
            end_date=1234583365000,
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
                materials=["colete"]
            )

            assert e.value == "Court is already booked for the selected time slot or has to have 15 min tolerance"
            

    def test_create_booking_usecase_invalid_schedule_15min(self):

        with pytest.raises(InvalidSchedule) as e:

            booking_repository = BookingRepositoryMock()

            usecase = CreateBookingUsecase(repo=booking_repository)

            booking_repository.create_booking(
                booking=Booking(
                    start_date=20000000,
                    end_date=30000000,
                    court_number=5,
                    sport=SPORT.FUTSAL,
                    user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
                    materials=['Bola', 'Chuteira'],
                    booking_id='ddd35c66-13a4-4641-9d54-773b4b8ccc98'
                )
            )

            response = usecase(
                start_date=10000000,
                end_date=19100001, #15 minutos de intolerância na criação
                court_number=5,
                sport=SPORT.FUTSAL,
                user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
                materials=['Bola', 'Chuteira']
            )

            assert e.value == "Court is already booked for the selected time slot or has to have 15 min tolerance"

            with pytest.raises(InvalidSchedule) as e2: 


                response2 = usecase(
                    start_date=30899999, # 15 minutos de intolerância na criação
                    end_date=40000000,
                    court_number=5,
                    sport=SPORT.FUTSAL,
                    user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
                    materials=['Bola', 'Chuteira']
                )

                assert e2.value == "Court is already booked for the selected time slot or has to have 15 min tolerance"
