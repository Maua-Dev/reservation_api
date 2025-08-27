from src.modules.get_all_admin_bookings.app.get_all_admin_bookings_controller import GetAllAdminBookingsController
from src.modules.get_all_admin_bookings.app.get_all_admin_bookings_usecase import GetAllAdminBookingsUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock

class TestGetAllAdminBookingsController:
    
    def test_get_all_admin_bookings_controller(self):
        
        repo = BookingRepositoryMock()
        usecase = GetAllAdminBookingsUsecase(repo = repo)
        controller = GetAllAdminBookingsController(usecase=usecase)
        request = HttpRequest()
        response = controller(request)