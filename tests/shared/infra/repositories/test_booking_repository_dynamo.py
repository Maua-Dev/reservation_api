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
        assert len(dynamo_bookings) == len(mock_bookings)


    @pytest.mark.skip("Can't run test in github actions")
    def test_dynamo_get_booking(self):
        dynamo_repo = BookingRepositoryDynamo()
        resp= dynamo_repo.get_booking('b1d3bebf-dc0d-4fc1-861c-506a40cc2925')
        assert resp.booking_id == 'b1d3bebf-dc0d-4fc1-861c-506a40cc2925'


    @pytest.mark.skip("Can't run test in github actions")
    def test_dynamo_get_bookings_sport(self):
        dynamo_repo = BookingRepositoryDynamo()
        mock_repo = BookingRepositoryMock()

        dynamo_bookings = dynamo_repo.get_bookings(sport=SPORT.TENNIS.value)
        mock_bookings = mock_repo.get_bookings(sport=SPORT.TENNIS.value)

        assert len(dynamo_bookings) == len(mock_bookings)

        for d_booking, m_booking in zip(dynamo_bookings, mock_bookings):
            assert d_booking.start_date == m_booking.start_date
            assert d_booking.end_date == m_booking.end_date
            assert d_booking.court_number == m_booking.court_number
            assert d_booking.sport == m_booking.sport
            assert d_booking.user_id == m_booking.user_id
            assert d_booking.booking_id == m_booking.booking_id
            assert d_booking.materials == m_booking.materials


    @pytest.mark.skip("Can't run test in github actions")
    def test_get_bookings_by_user_id(self):
        dynamo_repo = BookingRepositoryDynamo()
        mock_repo = BookingRepositoryMock()
        
        all_mock_bookings = mock_repo.get_all_bookings()
        test_user_id = all_mock_bookings[0].user_id
        
        dynamo_bookings = dynamo_repo.get_bookings(user_id=test_user_id)
        mock_bookings = mock_repo.get_bookings(user_id=test_user_id)
        
        assert len(dynamo_bookings) == len(mock_bookings)
        
        for booking in dynamo_bookings:
            assert booking.user_id == test_user_id

    
    @pytest.mark.skip("Can't run test in github actions")
    def test_get_bookings_by_court_number(self):
        dynamo_repo = BookingRepositoryDynamo()
        mock_repo = BookingRepositoryMock()
        
        for court_number in [1, 2, 3]:
            dynamo_bookings = dynamo_repo.get_bookings(court_number=court_number)
            mock_bookings = mock_repo.get_bookings(court_number=court_number)
            
            assert len(dynamo_bookings) == len(mock_bookings)
            
            for booking in dynamo_bookings:
                assert booking.court_number == court_number


    @pytest.mark.skip("Can't run test in github actions")
    def test_get_bookings_by_booking_id(self):
        dynamo_repo = BookingRepositoryDynamo()
        mock_repo = BookingRepositoryMock()
        
        test_booking_id = 'b1d3bebf-dc0d-4fc1-861c-506a40cc2925'
        
        dynamo_bookings = dynamo_repo.get_bookings(booking_id=test_booking_id)
        mock_bookings = mock_repo.get_bookings(booking_id=test_booking_id)
        
        assert len(dynamo_bookings) == len(mock_bookings)
        assert len(dynamo_bookings) == 1
        assert dynamo_bookings[0].booking_id == test_booking_id


    @pytest.mark.skip("Can't run test in github actions")
    def test_get_bookings_by_sport_and_court(self):
        dynamo_repo = BookingRepositoryDynamo()
        mock_repo = BookingRepositoryMock()
        
        test_combinations = [
            (SPORT.TENNIS, 1),
            (SPORT.FOOTBALL, 2),
            (SPORT.BASKETBALL, 3)
        ]
        
        for sport, court_number in test_combinations:
            dynamo_bookings = dynamo_repo.get_bookings(sport=sport.value, court_number=court_number)
            mock_bookings = mock_repo.get_bookings(sport=sport.value, court_number=court_number)
            
            assert len(dynamo_bookings) == len(mock_bookings)
            
            for booking in dynamo_bookings:
                assert booking.sport == sport
                assert booking.court_number == court_number


    @pytest.mark.skip("Can't run test in github actions")
    def test_get_bookings_by_sport_and_user(self):
        dynamo_repo = BookingRepositoryDynamo()
        mock_repo = BookingRepositoryMock()
        
        all_mock_bookings = mock_repo.get_all_bookings()
        test_user_id = all_mock_bookings[0].user_id
        
        for sport in SPORT:
            dynamo_bookings = dynamo_repo.get_bookings(sport=sport.value, user_id=test_user_id)
            mock_bookings = mock_repo.get_bookings(sport=sport.value, user_id=test_user_id)
            
            assert len(dynamo_bookings) == len(mock_bookings)
            
            for booking in dynamo_bookings:
                assert booking.sport == sport
                assert booking.user_id == test_user_id


    @pytest.mark.skip("Can't run test in github actions")
    def test_get_bookings_by_user_and_court(self):
        dynamo_repo = BookingRepositoryDynamo()
        mock_repo = BookingRepositoryMock()
        
        all_mock_bookings = mock_repo.get_all_bookings()
        test_user_id = all_mock_bookings[0].user_id
        
        for court_number in [1, 2, 3]:
            dynamo_bookings = dynamo_repo.get_bookings(user_id=test_user_id, court_number=court_number)
            mock_bookings = mock_repo.get_bookings(user_id=test_user_id, court_number=court_number)
            
            assert len(dynamo_bookings) == len(mock_bookings)
            
            for booking in dynamo_bookings:
                assert booking.user_id == test_user_id
                assert booking.court_number == court_number


    @pytest.mark.skip("Can't run test in github actions")
    def test_get_bookings_by_three_filters(self):
        dynamo_repo = BookingRepositoryDynamo()
        mock_repo = BookingRepositoryMock()
        
        all_mock_bookings = mock_repo.get_all_bookings()
        test_user_id = all_mock_bookings[0].user_id
        
        test_combinations = [
            (SPORT.TENNIS, 1, test_user_id),
            (SPORT.FOOTBALL, 2, test_user_id)
        ]
        
        for sport, court_number, user_id in test_combinations:
            dynamo_bookings = dynamo_repo.get_bookings(
                sport=sport.value, 
                court_number=court_number, 
                user_id=user_id
            )
            mock_bookings = mock_repo.get_bookings(
                sport=sport.value, 
                court_number=court_number, 
                user_id=user_id
            )
            
            assert len(dynamo_bookings) == len(mock_bookings)
            
            for booking in dynamo_bookings:
                assert booking.sport == sport
                assert booking.court_number == court_number
                assert booking.user_id == user_id


    @pytest.mark.skip("Can't run test in github actions")
    def test_get_bookings_by_date_range(self):
        dynamo_repo = BookingRepositoryDynamo()
        mock_repo = BookingRepositoryMock()
        
        start_date = 1634400000000
        end_date = 1634700000000
        
        dynamo_bookings = dynamo_repo.get_bookings(start_date=start_date, end_date=end_date)
        mock_bookings = mock_repo.get_bookings(start_date=start_date, end_date=end_date)
        
        assert len(dynamo_bookings) == len(mock_bookings)
        
        for booking in dynamo_bookings:
            assert booking.start_date >= start_date
            assert booking.end_date <= end_date


    @pytest.mark.skip("Can't run test in github actions")
    def test_get_bookings_by_sport_and_date_range(self):
        dynamo_repo = BookingRepositoryDynamo()
        mock_repo = BookingRepositoryMock()
        
        start_date = 1634400000000
        end_date = 1634700000000
        
        for sport in SPORT:
            dynamo_bookings = dynamo_repo.get_bookings(
                sport=sport.value, 
                start_date=start_date, 
                end_date=end_date
            )
            mock_bookings = mock_repo.get_bookings(
                sport=sport.value, 
                start_date=start_date, 
                end_date=end_date
            )
            
            assert len(dynamo_bookings) == len(mock_bookings)
            
            for booking in dynamo_bookings:
                assert booking.sport == sport
                assert booking.start_date >= start_date
                assert booking.end_date <= end_date


    @pytest.mark.skip("Can't run test in github actions")    
    def test_dynamo_update_booking(self):
        dynamo_repo = BookingRepositoryDynamo()
        booking_id = 'b1d3bebf-dc0d-4fc1-861c-506a40cc2925'
        updated_booking = dynamo_repo.update_booking(
            booking_id=booking_id,
            start_date=1234567890,  
            court_number=2,
            sport=SPORT.TENNIS.value      
        )


        assert updated_booking is not None
        assert updated_booking.booking_id == booking_id
        assert updated_booking.start_date == 1234567890
        assert updated_booking.court_number == 2
        assert updated_booking.sport == SPORT.TENNIS

        
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

        dynamo_repo.delete_booking(new_booking.booking_id)


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


