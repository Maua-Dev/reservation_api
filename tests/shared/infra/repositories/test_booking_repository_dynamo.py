import pytest
from src.shared.infra.repositories.booking_repository_dynamo import BookingRepositoryDynamo
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock
from src.shared.domain.enums.sport import SPORT
from src.shared.domain.entities.booking import Booking

class TestBookingRepositoryDynamo:

    @pytest.mark.skip("Can't run test in github actions")
    def test_dynamo_get_all_bookings(self):
        dynamo_repo = BookingRepositoryDynamo()
        mock_repo = BookingRepositoryMock()
        dynamo_bookings = dynamo_repo.get_all_bookings()
        mock_bookings = mock_repo.get_all_bookings()
        assert len(dynamo_bookings) == len(mock_bookings) + 1
        for d_booking, m_booking in zip(dynamo_bookings, mock_bookings):
            assert d_booking.start_date == m_booking.start_date
            assert d_booking.end_date == m_booking.end_date
            assert d_booking.court_number == m_booking.court_number
            assert d_booking.sport == m_booking.sport
            assert d_booking.user_id == m_booking.user_id
            assert d_booking.booking_id == m_booking.booking_id
            assert d_booking.materials == m_booking.materials

    @pytest.mark.skip("Can't run test in github actions")
    def test_dynamo_delete_booking(self):
        dynamo_repo = BookingRepositoryDynamo()
        mock_repo = BookingRepositoryMock()
        booking = mock_repo.get_booking('b5d3bebf-dc0d-4fc1-861c-506a40cc2925')
        deleted_booking = dynamo_repo.delete_booking(booking.booking_id)
        retrieved_booking = dynamo_repo.get_booking(booking.booking_id)
        assert retrieved_booking is None
        assert deleted_booking.booking_id == booking.booking_id

    @pytest.mark.skip("Can't run test in github actions")
    def test_dynamo_delete_booking_not_found(self):
        dynamo_repo = BookingRepositoryDynamo()
        deleted_booking = dynamo_repo.delete_booking('bau3bebf-dc0d-4fc1-861c-506a40cc2997')
        assert deleted_booking is None

    @pytest.mark.skip("Can't run test in github actions")
    def test_dynamo_get_booking(self):
        dynamo_repo = BookingRepositoryDynamo()
        resp= dynamo_repo.get_booking('b1d3bebf-dc0d-4fc1-861c-506a40cc2925')
        assert resp.booking_id == 'b1d3bebf-dc0d-4fc1-861c-506a40cc2925'
        assert resp.sport == SPORT.TENNIS

    @pytest.mark.skip("Can't run test in github actions")
    def test_dynamo_update_booking(self):
        dynamo_repo = BookingRepositoryDynamo()
        booking_id = 'b1d3bebf-dc0d-4fc1-861c-506a40cc2925'
        updated_booking = dynamo_repo.update_booking(
            booking_id=booking_id,
            start_date=1234567890,  
            court_number=2,
            sport=SPORT.BASKETBALL 
        )


        assert updated_booking is not None
        assert updated_booking.booking_id == booking_id
        assert updated_booking.start_date == 1234567890
        assert updated_booking.court_number == 2
        assert updated_booking.sport == SPORT.BASKETBALL

    @pytest.mark.skip("Can't run test in github actions")
    def test_dynamo_create_booking(self):
        dynamo_repo = BookingRepositoryDynamo()
        new_booking = Booking(
            start_date=1634563800000,
            end_date=1634567400000,
            court_number=2,
            sport=SPORT.FOOTBALL,
            user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
            booking_id='b9d3bebf-dc0d-4fc1-861c-506a40cc2935',
            materials=['Bola', 'Chuteira']
        )

        created_booking = dynamo_repo.create_booking(new_booking)
        
        assert created_booking.start_date == new_booking.start_date
        assert created_booking.end_date == new_booking.end_date
        assert created_booking.court_number == new_booking.court_number
        assert created_booking.sport == new_booking.sport
        assert created_booking.user_id == new_booking.user_id
        assert created_booking.booking_id == new_booking.booking_id
        assert created_booking.materials == new_booking.materials

        retrieved_booking = dynamo_repo.get_booking(new_booking.booking_id)
        
        assert retrieved_booking.start_date == new_booking.start_date
        assert retrieved_booking.end_date == new_booking.end_date
        assert retrieved_booking.court_number == new_booking.court_number
        assert retrieved_booking.sport == new_booking.sport
        assert retrieved_booking.user_id == new_booking.user_id
        assert retrieved_booking.booking_id == new_booking.booking_id
        assert retrieved_booking.materials == new_booking.materials