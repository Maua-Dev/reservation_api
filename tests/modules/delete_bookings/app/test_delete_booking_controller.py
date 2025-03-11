from src.modules.delete_booking.app.delete_booking_controller import DeleteBookingController
from src.modules.delete_booking.app.delete_booking_usecase import DeleteBookingUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock

class TestDeleteBookingController:
    def test_delete_booking_controller(self):
        repo = BookingRepositoryMock()
        usecase = DeleteBookingUsecase(repo= repo)
        controller = DeleteBookingController(usecase=usecase)
        request = HttpRequest(body= {
            "booking_id": 'b1d3bebf-dc0d-4fc1-861c-506a40cc2925'
        })

        response = controller(request)
        assert response.status_code == 200
        assert response.body['message'] == "the booking was deleted"

    def test_delete_booking_controller_missing_booking_id(self):
        repo = BookingRepositoryMock()
        usecase = DeleteBookingUsecase(repo= repo)
        controller = DeleteBookingController(usecase=usecase)
        request = HttpRequest(body={
            "booking_id": None
        })

        response = controller(request)
        assert response.status_code == 400
        assert response.body == 'Field booking_id is missing'

    def test_delete_booking_controller_booking_id_entity_error(self):
        repo = BookingRepositoryMock()
        usecase = DeleteBookingUsecase(repo= repo)
        controller = DeleteBookingController(usecase=usecase)
        request = HttpRequest(body={
            "booking_id": 0
        })
        
        reponse = controller(request)
        assert reponse.status_code == 400
        assert reponse.body == "Field booking_id is not valid"

    def test_delete_booking_controller_wrong_type_parameter(self):
        repo = BookingRepositoryMock()
        usecase = DeleteBookingUsecase(repo=repo)
        controller = DeleteBookingController(usecase=usecase)
        request = HttpRequest(body={
            "booking_id": "wrong_type"  
        })

        response = controller(request)
        assert response.status_code == 400
        assert response.body == "Field booking_id is not valid"

    def test_delete_booking_controller_not_found(self):
        repo = BookingRepositoryMock()
        usecase = DeleteBookingUsecase(repo=repo)
        controller = DeleteBookingController(usecase=usecase)
        request = HttpRequest(body={
            "booking_id": 'b1d3bebf-dc0d-4fc1-861c-506a40cc2926'
        })

        response = controller(request)
        assert response.status_code == 404
        assert response.body == "No items found for booking"