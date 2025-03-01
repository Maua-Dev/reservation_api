from src.modules.create_booking.app.create_booking_viewmodel import CreateBookingViewmodel
from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.sport import SPORT


class TestCreateBookingViewmodel:

    def test_create_booking_viewmodel(self):

        booking = Booking(
            start_date=1634576165000,
            end_date=1634583365000,
            court_number=1,
            sport=SPORT.TENNIS,
            user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98',
            booking_id='b1d3bebf-dc0d-4fc1-861c-506a40cc2925',
            materials=['Raquete', 'Bola', 'Rede', 'Tenis']
        )

        expected = {
            "booking": {
                "start_date": 1634576165000,
                "end_date": 1634583365000,
                "court_number": 1,
                "sport": "Tennis",
                "user_id": "c8435c66-13a4-4641-9d54-773b4b8ccc98",
                "booking_id": "b1d3bebf-dc0d-4fc1-861c-506a40cc2925",
                "materials": ["Raquete", "Bola", "Rede", "Tenis"]
            },
            "message": "Booking created successfully"
        }
        viewmodel = CreateBookingViewmodel(booking)

        assert viewmodel.to_dict() == expected


