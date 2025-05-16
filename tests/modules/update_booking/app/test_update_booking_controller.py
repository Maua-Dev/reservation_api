import pytest
import uuid

from src.modules.update_booking.app.update_booking_controller import UpdateBookingController
from src.modules.update_booking.app.update_booking_usecase import UpdateBookingUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock


class Test_UpdateBookingController:
    def test_update_booking_controller(self):
        booking_repo = BookingRepositoryMock()
        usecase = UpdateBookingUsecase(booking_repo=booking_repo)
        controller = UpdateBookingController(update_booking_use_case=usecase)

        request = HttpRequest(body={
            "booking_id":  booking_repo.bookings[0].booking_id,
            "start_date": booking_repo.bookings[0].start_date,
            "end_date": booking_repo.bookings[0].end_date,
            "court_number": 1,
            "sport": "Tennis",
            "materials": ['Raquete', 'Bola', 'Rede', 'Tenis']
        })

        response = controller(request)

        assert response.status_code == 200
        assert response.body['message'] == "the booking was retrieved"

    def test_update_booking_controller_booking_id_missing(self):
        booking_repo = BookingRepositoryMock()
        usecase = UpdateBookingUsecase(booking_repo=booking_repo)
        controller = UpdateBookingController(update_booking_use_case=usecase)

        request = HttpRequest(body={
            "start_date": booking_repo.bookings[0].start_date,
            "end_date": booking_repo.bookings[0].end_date,
            "court_number": 1,
            "sport": "Tennis",
            "materials": ['Raquete', 'Bola', 'Rede', 'Tenis']
        })        

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Field booking_id is missing"

    def test_update_booking_controller_booking_id_wrong_type(self):
        booking_repo = BookingRepositoryMock()
        usecase = UpdateBookingUsecase(booking_repo=booking_repo)
        controller = UpdateBookingController(update_booking_use_case=usecase)

        request = HttpRequest(body={
            "booking_id": 123,  
            "start_date": booking_repo.bookings[0].start_date,
            "end_date": booking_repo.bookings[0].end_date,
            "court_number": 1,
            "sport": "Tennis",
            "materials": ['Raquete', 'Bola', 'Rede', 'Tenis']
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Field booking_id is not valid"

    def test_update_booking_controller_start_date_wrong_type(self):
        booking_repo = BookingRepositoryMock()
        usecase = UpdateBookingUsecase(booking_repo=booking_repo)
        controller = UpdateBookingController(update_booking_use_case=usecase)

        request = HttpRequest(body={
            "booking_id": booking_repo.bookings[0].booking_id,
            "start_date": "123",  
            "end_date": booking_repo.bookings[0].end_date,
            "court_number": 1,
            "sport": "Tennis",
            "materials": ['Raquete', 'Bola', 'Rede', 'Tenis']
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Field date is not valid"

    def test_update_booking_controller_end_date_wrong_type(self):
        booking_repo = BookingRepositoryMock()
        usecase = UpdateBookingUsecase(booking_repo=booking_repo)
        controller = UpdateBookingController(update_booking_use_case=usecase)

        request = HttpRequest(body={
            "booking_id": booking_repo.bookings[0].booking_id,
            "start_date": booking_repo.bookings[0].start_date,
            "end_date": "123", 
            "court_number": 1,
            "sport": "Tennis",
            "materials": ['Raquete', 'Bola', 'Rede', 'Tenis']
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Field date is not valid"

    def test_update_booking_controller_court_number_wrong_type(self):
        booking_repo = BookingRepositoryMock()
        usecase = UpdateBookingUsecase(booking_repo=booking_repo)
        controller = UpdateBookingController(update_booking_use_case=usecase)

        request = HttpRequest(body={
            "booking_id": booking_repo.bookings[0].booking_id,
            "start_date": booking_repo.bookings[0].start_date,
            "end_date": booking_repo.bookings[0].end_date,
            "court_number": "1",  
            "sport": "Tennis",
            "materials": ['Raquete', 'Bola', 'Rede', 'Tenis']
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Field court_number is not valid"

    def test_update_booking_controller_sport_wrong_type(self):
        booking_repo = BookingRepositoryMock()
        usecase = UpdateBookingUsecase(booking_repo=booking_repo)
        controller = UpdateBookingController(update_booking_use_case=usecase)

        request = HttpRequest(body={
            "booking_id": booking_repo.bookings[0].booking_id,
            "start_date": booking_repo.bookings[0].start_date,
            "end_date": booking_repo.bookings[0].end_date,
            "court_number": 1,
            "sport": 123,  
            "materials": ['Raquete', 'Bola', 'Rede', 'Tenis']
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Field sport is not valid"

    def test_update_booking_controller_materials_wrong_type(self):
        booking_repo = BookingRepositoryMock()
        usecase = UpdateBookingUsecase(booking_repo=booking_repo)
        controller = UpdateBookingController(update_booking_use_case=usecase)

        request = HttpRequest(body={
            "booking_id": booking_repo.bookings[0].booking_id,
            "start_date": booking_repo.bookings[0].start_date,
            "end_date": booking_repo.bookings[0].end_date,
            "court_number": 1,
            "sport": "Tennis",
            "materials": "Raquete, Bola, Rede, Tenis"  
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Field materials is not valid"

    def test_update_booking_controller_only_booking_id(self):
        booking_repo = BookingRepositoryMock()
        usecase = UpdateBookingUsecase(booking_repo=booking_repo)
        controller = UpdateBookingController(update_booking_use_case=usecase)
        
        original_booking = booking_repo.bookings[0]
        booking_id = original_booking.booking_id
        
        request = HttpRequest(body={
            "booking_id": booking_id
        })
        
        response = controller(request)
        
        assert response.status_code == 200
        assert response.body['booking']['booking_id'] == booking_id

    def test_update_booking_controller_user_id_ignored(self):
        booking_repo = BookingRepositoryMock()
        usecase = UpdateBookingUsecase(booking_repo=booking_repo)
        controller = UpdateBookingController(update_booking_use_case=usecase)
        
        original_booking = booking_repo.bookings[0]
        original_user_id = original_booking.user_id
        new_user_id = "novo-user-id-que-nao-deve-ser-usado"
        
        request = HttpRequest(body={
            "booking_id": original_booking.booking_id,
            "start_date": original_booking.start_date,
            "end_date": original_booking.end_date,
            "court_number": 1,
            "sport": "Tennis",
            "materials": ['Raquete', 'Bola', 'Rede', 'Tenis'],
            "user_id": new_user_id  
        })
        
        response = controller(request)
        
        assert response.status_code == 200
        assert response.body['booking']['user_id'] == original_user_id
        assert response.body['booking']['user_id'] != new_user_id

    def test_update_booking_controller_booking_not_found(self):
        booking_repo = BookingRepositoryMock()
        usecase = UpdateBookingUsecase(booking_repo=booking_repo)
        controller = UpdateBookingController(update_booking_use_case=usecase)
        
        non_existent_booking_id = str(uuid.uuid4())

        original_get_booking = booking_repo.get_booking
        
        def get_booking_mock(booking_id):
            if booking_id == non_existent_booking_id:
                return None
            return original_get_booking(booking_id)
        
        booking_repo.get_booking = get_booking_mock
        
        request = HttpRequest(body={
            "booking_id": non_existent_booking_id,
            "start_date": 1634576165000,
            "end_date": 1634583365000,
            "court_number": 1,
            "sport": "Tennis",
            "materials": ['Raquete', 'Bola', 'Rede', 'Tenis']
        })
        
        response = controller(request)
        booking_repo.get_booking = original_get_booking

        assert response.status_code == 404
        assert "not found" in response.body.lower()