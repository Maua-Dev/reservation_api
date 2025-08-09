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
            "materials": ['Raquete', 'Bola', 'Rede', 'Tenis'],
            "user_from_authorizer": {
                'user_id': 'qualquer-id',
                'name': 'Nome',
                'email': 'user@email.com',
                'role': 'ADMIN'
             }
       })

       response = controller(request)

       assert response.status_code == 200
       assert response.body['message'] == "the booking was retrieved"


    def test_update_booking_controller_with_invalid_user_id(self):
       booking_repo = BookingRepositoryMock()
       usecase = UpdateBookingUsecase(booking_repo=booking_repo)
       controller = UpdateBookingController(update_booking_use_case=usecase)

       request = HttpRequest(body={
            "booking_id":  booking_repo.bookings[0].booking_id,
            "start_date": booking_repo.bookings[0].start_date,
            "end_date": booking_repo.bookings[0].end_date,
            "court_number": 1,
            "sport": "Tennis",
            "materials": ['Raquete', 'Bola', 'Rede', 'Tenis'],
            "user_from_authorizer": {
                'user_id': 'invalid',
                'name': 'Nome',
                'email': 'user@email.com',
                'role': 'STUDENT'
             }
       })

       response = controller(request)

       assert response.status_code == 403
       assert response.body == "That action is forbidden for this user id"


    def test_update_booking_controller_booking_id_missing(self):
       booking_repo = BookingRepositoryMock()
       usecase = UpdateBookingUsecase(booking_repo=booking_repo)
       controller = UpdateBookingController(update_booking_use_case=usecase)

       request = HttpRequest(body={
            "start_date": booking_repo.bookings[0].start_date,
            "end_date": booking_repo.bookings[0].end_date,
            "court_number": 1,
            "sport": "Tennis",
            "materials": ['Raquete', 'Bola', 'Rede', 'Tenis'],
            "user_from_authorizer": {
                'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
                'name': 'Nome',
                'email': 'user@email.com',
                'role': 'STUDENT'
             }
           
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
            "materials": ['Raquete', 'Bola', 'Rede', 'Tenis'],
            "user_from_authorizer": {
                'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
                'name': 'Nome',
                'email': 'user@email.com',
                'role': 'STUDENT'
             }

       })

       response = controller(request)

       assert response.status_code == 400
       assert "booking_id" in response.body
       assert "str" in response.body

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
            "materials": ['Raquete', 'Bola', 'Rede', 'Tenis'],
            "user_from_authorizer": {
                'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
                'name': 'Nome',
                'email': 'user@email.com',
                'role': 'STUDENT'
             }
       })

       response = controller(request)

       assert response.status_code == 400
       assert "start_date" in response.body
       assert "int" in response.body

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
            "materials": ['Raquete', 'Bola', 'Rede', 'Tenis'],
            "user_from_authorizer": {
                'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
                'name': 'Nome',
                'email': 'user@email.com',
                'role': 'STUDENT'
             }
       })

       response = controller(request)

       assert response.status_code == 400
       assert "end_date" in response.body
       assert "int" in response.body

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
            "materials": ['Raquete', 'Bola', 'Rede', 'Tenis'],
            "user_from_authorizer": {
                'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
                'name': 'Nome',
                'email': 'user@email.com',
                'role': 'STUDENT'
             }
       })

       response = controller(request)

       assert response.status_code == 400
       assert "court_number" in response.body
       assert "int" in response.body

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
            "materials": ['Raquete', 'Bola', 'Rede', 'Tenis'],
            "user_from_authorizer": {
                'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
                'name': 'Nome',
                'email': 'user@email.com',
                'role': 'STUDENT'
             }
       })

       response = controller(request)

       assert response.status_code == 400
       assert "sport" in response.body
       assert "str" in response.body

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
            "materials": "Raquete, Bola, Rede, Tenis",
            "user_from_authorizer": {
                'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
                'name': 'Nome',
                'email': 'user@email.com',
                'role': 'STUDENT'
             }
       })

       response = controller(request)

       assert response.status_code == 400
       assert "materials" in response.body
       assert "list" in response.body

    def test_update_booking_controller_only_booking_id(self):
       booking_repo = BookingRepositoryMock()
       usecase = UpdateBookingUsecase(booking_repo=booking_repo)
       controller = UpdateBookingController(update_booking_use_case=usecase)
       
       original_booking = booking_repo.bookings[0]
       booking_id = original_booking.booking_id
       
       request = HttpRequest(body={
            "booking_id": booking_id,
            "user_from_authorizer": {
                'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
                'name': 'Nome',
                'email': 'user@email.com',
                'role': 'STUDENT'
             }
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
            "user_id": new_user_id,
            "user_from_authorizer": {
                'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
                'name': 'Nome',
                'email': 'user@email.com',
                'role': 'STUDENT'
             }
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
            "materials": ['Raquete', 'Bola', 'Rede', 'Tenis'],
            "user_from_authorizer": {
                'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
                'name': 'Nome',
                'email': 'user@email.com',
                'role': 'STUDENT'
             }
       })
       
       response = controller(request)
       booking_repo.get_booking = original_get_booking

       assert response.status_code == 404
       assert "not found" in response.body.lower()


    def test_update_booking_controller_partial_update(self):
        booking_repo = BookingRepositoryMock()
        usecase = UpdateBookingUsecase(booking_repo=booking_repo)
        controller = UpdateBookingController(update_booking_use_case=usecase)
        
        original_booking = booking_repo.bookings[0]
        booking_id = original_booking.booking_id
        original_court_number = original_booking.court_number
        new_court_number = original_court_number + 1  
        
        request = HttpRequest(body={
            "booking_id": booking_id,
            "court_number": new_court_number,
            "user_from_authorizer": {
                'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
                'name': 'Nome',
                'email': 'user@email.com',
                'role': 'STUDENT'
             }
        })
        
        response = controller(request)
        
        assert response.status_code == 200
        assert response.body['booking']['court_number'] == new_court_number
        assert response.body['booking']['start_date'] == original_booking.start_date
        assert response.body['booking']['end_date'] == original_booking.end_date
        assert response.body['booking']['sport'] == original_booking.sport.value
        assert response.body['booking']['materials'] == original_booking.materials