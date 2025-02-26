from src.modules.update_booking.app.update_booking_viewmodel import UpdateBookingViewmodel
from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.sport import SPORT


class Test_UpdateBookingViewmodel:

    def test_update_booking_view_model(self):
        booking = Booking(start_date=1634576165000, 
                          end_date=1634583365000, 
                          court_number=1, 
                          sport=SPORT.FOOTBALL, 
                          user_id='c8435c66-13a4-4641-9d54-773b4b8ccc98', 
                          booking_id='b1d3bebf-dc0d-4fc1-861c-506a40cc2925', 
                          materials=['Bola'])

        viewmodel = UpdateBookingViewmodel(booking=booking).to_dict()

        expected = {
            'booking': {
                'start_date': 1634576165000,
                'end_date': 1634583365000,
                'court_number': 1,
                'sport': 'Football',
                'user_id': 'c8435c66-13a4-4641-9d54-773b4b8ccc98',
                'booking_id': 'b1d3bebf-dc0d-4fc1-861c-506a40cc2925',
                'materials': ['Bola']
            },
            'message': 'the booking was retrieved'
        }

        assert expected == viewmodel