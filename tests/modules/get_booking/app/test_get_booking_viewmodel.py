from src.modules.get_booking.app.get_booking_viewmodel import GetBookingViewmodel
from src.modules.get_booking.app.get_booking_usecase import GetBookingUseCase
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock


class Test_GetBookingViewModel:
    def test_get_booking_viewmodel_without_owner(self):
        repo = BookingRepositoryMock()
        usecase = GetBookingUseCase(repo)
        result = usecase(booking_id=repo.bookings[0].booking_id)

        viewmodel = GetBookingViewmodel(result["booking"], result["owner"]).to_dict()

        expected = {
            'booking': {
                'start_date': 1634576165000,
                'end_date': 1634583365000,
                'court_number': 1,
                'sport': 'Tennis',
                'booking_id': 'b1d3bebf-dc0d-4fc1-861c-506a40cc2925',
                'materials': ['Raquete', 'Bola', 'Rede', 'Tenis'],
                'type': 'Training'
            },
            'message': 'the booking was retrieved'
        }

        assert viewmodel == expected

    def test_get_booking_viewmodel_with_owner(self):
        repo = BookingRepositoryMock()
        booking = repo.bookings[0]
        owner = {"name": "GUSTAVO ALVES GOMES", "network_id": "23.00847-4"}

        viewmodel = GetBookingViewmodel(booking, owner).to_dict()

        expected = {
            'booking': {
                'start_date': 1634576165000,
                'end_date': 1634583365000,
                'court_number': 1,
                'sport': 'Tennis',
                'booking_id': 'b1d3bebf-dc0d-4fc1-861c-506a40cc2925',
                'materials': ['Raquete', 'Bola', 'Rede', 'Tenis'],
                'type': 'Training',
                'owner_name': 'GUSTAVO ALVES GOMES',
                'owner_network_id': '23.00847-4'
            },
            'message': 'the booking was retrieved'
        }

        assert viewmodel == expected

    def test_get_booking_viewmodel_with_owner_null_fields(self):
        repo = BookingRepositoryMock()
        booking = repo.bookings[0]
        owner = {"name": None, "network_id": None}

        viewmodel = GetBookingViewmodel(booking, owner).to_dict()

        assert viewmodel['booking']['owner_name'] is None
        assert viewmodel['booking']['owner_network_id'] is None
