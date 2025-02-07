import pytest

from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.sport import SPORT
from src.shared.helpers.errors.domain_errors import EntityError


class TestBooking:

    def test_booking(self):

        booking = Booking(
            start_date= 1738940138,
            end_date= 1838940138,
            court_number= 1,
            sport= SPORT.FOOTBALL,
            user_id= "d3b07384-d9a1-4e8a-b3ef-4f1d2a87c6f5",
            booking_id= "a1f5e2c3-7d8b-4c9e-b012-34f6a789d0e1",
            materials= ["ball"]
        )

        assert type(booking) == Booking
        assert booking.start_date == 1738940138
        assert booking.end_date == 1838940138
        assert booking.court_number == 1
        assert booking.sport == SPORT.FOOTBALL
        assert booking.user_id == "d3b07384-d9a1-4e8a-b3ef-4f1d2a87c6f5"
        assert booking.booking_id == "a1f5e2c3-7d8b-4c9e-b012-34f6a789d0e1"
        assert booking.materials == ["ball"]

    def test_invalid_dates(self):
        with pytest.raises(EntityError):
            Booking(
                start_date= 1838940138,
                end_date= 1738940138,
                court_number= 1,
                sport= SPORT.FOOTBALL,
                user_id= "d3b07384-d9a1-4e8a-b3ef-4f1d2a87c6f5",
                booking_id= "a1f5e2c3-7d8b-4c9e-b012-34f6a789d0e1",
                materials= ["ball"]
            )

    def test_invalid_dates2(self):
        with pytest.raises(EntityError):
            Booking(
                start_date= 'a',
                end_date= 'b',
                court_number= 1,
                sport= SPORT.FOOTBALL,
                user_id= "d3b07384-d9a1-4e8a-b3ef-4f1d2a87c6f5",
                booking_id= "a1f5e2c3-7d8b-4c9e-b012-34f6a789d0e1",
                materials= ["ball"]
            )

    def test_invalid_court_number(self):
        with pytest.raises(EntityError):
            Booking(
                start_date= 1738940138,
                end_date= 1838940138,
                court_number= 'a',
                sport= SPORT.FOOTBALL,
                user_id= "d3b07384-d9a1-4e8a-b3ef-4f1d2a87c6f5",
                booking_id= "a1f5e2c3-7d8b-4c9e-b012-34f6a789d0e1",
                materials= ["ball"]
            )

    def test_invalid_sport(self):
        with pytest.raises(EntityError):
            Booking(
                start_date= 1738940138,
                end_date= 1838940138,
                court_number= 1,
                sport= "football",
                user_id= "d3b07384-d9a1-4e8a-b3ef-4f1d2a87c6f5",
                booking_id= "a1f5e2c3-7d8b-4c9e-b012-34f6a789d0e1",
                materials= ["ball"]
            )

    def test_invalid_user_id(self):
        with pytest.raises(EntityError):
            Booking(
                start_date= 1738940138,
                end_date= 1838940138,
                court_number= 1,
                sport= SPORT.FOOTBALL,
                user_id= "123",
                booking_id= "a1f5e2c3-7d8b-4c9e-b012-34f6a789d0e1",
                materials= ["ball"]
            )

    def test_invalid_booking_id(self):
        with pytest.raises(EntityError):
            Booking(
                start_date= 1738940138,
                end_date= 1838940138,
                court_number= 1,
                sport= SPORT.FOOTBALL,
                user_id= "d3b07384-d9a1-4e8a-b3ef-4f1d2a87c6f5",
                booking_id= "123",
                materials= ["ball"]
            )

    def test_invalid_materials(self):
        with pytest.raises(EntityError):
            Booking(
                start_date= 1738940138,
                end_date= 1838940138,
                court_number= 1,
                sport= SPORT.FOOTBALL,
                user_id= "d3b07384-d9a1-4e8a-b3ef-4f1d2a87c6f5",
                booking_id= "a1f5e2c3-7d8b-4c9e-b012-34f6a789d0e1",
                materials= "ball"
            )

    def test_invalid_materials2(self):
        with pytest.raises(EntityError):
            Booking(
                start_date= 1738940138,
                end_date= 1838940138,
                court_number= 1,
                sport= SPORT.FOOTBALL,
                user_id= "d3b07384-d9a1-4e8a-b3ef-4f1d2a87c6f5",
                booking_id= "a1f5e2c3-7d8b-4c9e-b012-34f6a789d0e1",
                materials= [1]
            )

    def test_invalid_materials3(self):
        with pytest.raises(EntityError):
            Booking(
                start_date= 1738940138,
                end_date= 1838940138,
                court_number= 1,
                sport= SPORT.FOOTBALL,
                user_id= "d3b07384-d9a1-4e8a-b3ef-4f1d2a87c6f5",
                booking_id= "a1f5e2c3-7d8b-4c9e-b012-34f6a789d0e1",
                materials= ["ball", 2]
            )

    def test_booking_to_dict(self):

        booking = Booking(
            start_date= 1738940138,
            end_date= 1838940138,
            court_number= 1,
            sport= SPORT.FOOTBALL,
            user_id= "d3b07384-d9a1-4e8a-b3ef-4f1d2a87c6f5",
            booking_id= "a1f5e2c3-7d8b-4c9e-b012-34f6a789d0e1",
            materials= ["ball"]
        )

        expected = {
            "start_date": 1738940138,
            "end_date": 1838940138,
            "court_number": 1,
            "sport": "Football",
            "user_id": "d3b07384-d9a1-4e8a-b3ef-4f1d2a87c6f5",
            "booking_id": "a1f5e2c3-7d8b-4c9e-b012-34f6a789d0e1",
            "materials": ["ball"]
        }

        assert booking.to_dict() == expected