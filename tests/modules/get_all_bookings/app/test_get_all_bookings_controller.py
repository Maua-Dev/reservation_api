from src.modules.get_all_bookings.app.get_all_bookings_usecase import GetAllBookingsUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock
from src.shared.domain.entities.booking import Booking
from src.modules.get_all_bookings.app.get_all_bookings_controller import GetAllBookingsController

class Test_GetAllBookingsController:
    def test_get_all_bookings_controller(self):
        repo = BookingRepositoryMock()
        usecase = GetAllBookingsUsecase(repo = repo)
        controller = GetAllBookingsController(usecase=usecase)
        request = HttpRequest()
        response = controller(request)
        assert response.status_code == 200
        assert response.body['message'] == 'the bookings were retrieved'