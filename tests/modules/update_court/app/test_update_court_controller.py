from src.shared.infra.repositories.reservation_repository_mock import ReservationRepositoryMock
from src.modules.update_court.app.update_court_controller import UpdateCourtController
from src.modules.update_court.app.update_court_usecase import UpdateCourtUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.domain.entities.court import Court


class TestUpdateCourtController:
    def test_update_court_controller(self):
        repo = ReservationRepositoryMock()
        usecase = UpdateCourtUsecase(repo=repo)
        controller = UpdateCourtController(usecase=usecase)
        court_number = 1

        mock_court = repo.get_court(court_number)
        prev_court = Court(mock_court.number,
                           mock_court.status,
                           mock_court.is_field,
                           mock_court.photo)

        request = HttpRequest(body={
            "number": court_number,
            "status": "MAINTENANCE",
            "is_field": True,
            "photo": "https://www.linkedin.com/in/leonardo-iorio-b83360279/"
        })

        response = controller(request)

        assert response.status_code == 200
        assert response.body['message'] == "the court was updated"
        assert response.body['updated_court']['number'] == court_number

        assert response.body['updated_court']['status'] != prev_court.status.value
        assert response.body['updated_court']['status'] == "MAINTENANCE"

        assert response.body['updated_court']['is_field'] != prev_court.is_field
        assert response.body['updated_court']['is_field'] == True

        assert response.body['updated_court']['photo'] != prev_court.photo
        assert response.body['updated_court']['photo'] == "https://www.linkedin.com/in/leonardo-iorio-b83360279/"

    def test_update_court_controller_missing_number(self):
        repo = ReservationRepositoryMock()
        usecase = UpdateCourtUsecase(repo=repo)
        controller = UpdateCourtController(usecase=usecase)
        request = HttpRequest(body={
            "status": "AVAILABLE",
            "is_field": False,
            "photo": "https://www.linkedin.com/in/vinicius-berti-a80354209/"
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Field number is missing'

    def test_update_court_controller_wrong_type_number(self):
        repo = ReservationRepositoryMock()
        usecase = UpdateCourtUsecase(repo=repo)
        controller = UpdateCourtController(usecase=usecase)
        request = HttpRequest(body={
            "number": "cavalo",
            "status": "AVAILABLE",
            "is_field": False,
            "photo": "https://www.linkedin.com/in/vinicius-berti-a80354209/"
        })

        reponse = controller(request)

        assert reponse.status_code == 400
        assert reponse.body == "Field number isn\'t in the right type.\n Received: <class 'str'>.\n Expected: <class 'int'>"

    def test_update_court_controller_with_wrong_type_status(self):
        repo = ReservationRepositoryMock()
        usecase = UpdateCourtUsecase(repo= repo)
        controller = UpdateCourtController(usecase=usecase)
        request = HttpRequest(body={
            "number": 7,
            "status": 123,
            "is_field": False,
            "photo": "https://www.linkedin.com/in/vinicius-berti-a80354209/"
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Field status is not valid'

    def test_update_court_controller_status_entity_error(self):
        repo = ReservationRepositoryMock()
        usecase = UpdateCourtUsecase(repo=repo)
        controller = UpdateCourtController(usecase=usecase)
        request = HttpRequest(body={
            "number": 7,
            "status": "INVALID",
            "is_field": False,
            "photo": "https://www.linkedin.com/in/vinicius-berti-a80354209/"
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Field status is not valid"

    def test_update_court_controller_is_field_type_error_int(self):
        repo = ReservationRepositoryMock()
        usecase = UpdateCourtUsecase(repo=repo)
        controller = UpdateCourtController(usecase=usecase)
        request = HttpRequest(body={
            "number": 7,
            "status": "AVAILABLE",
            "is_field": 1,
            "photo": "https://www.linkedin.com/in/vinicius-berti-a80354209/"
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Field is_field isn\'t in the right type.\n Received: <class 'int'>.\n Expected: <class 'bool'>"

    def test_update_court_controller_is_field_type_error_string(self):
        repo = ReservationRepositoryMock()
        usecase = UpdateCourtUsecase(repo=repo)
        controller = UpdateCourtController(usecase=usecase)
        request = HttpRequest(body={
            "number": 7,
            "status": "AVAILABLE",
            "is_field": 'False',
            "photo": "https://www.linkedin.com/in/vinicius-berti-a80354209/"
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Field is_field isn\'t in the right type.\n Received: <class 'str'>.\n Expected: <class 'bool'>"

    def test_update_court_controller_photo_type_error(self):
        repo = ReservationRepositoryMock()
        usecase = UpdateCourtUsecase(repo=repo)
        controller = UpdateCourtController(usecase=usecase)
        request = HttpRequest(body={
            "number": 7,
            "status": "AVAILABLE",
            "is_field": False,
            "photo": 1337
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Field photo isn\'t in the right type.\n Received: <class 'int'>.\n Expected: <class 'str'>"

