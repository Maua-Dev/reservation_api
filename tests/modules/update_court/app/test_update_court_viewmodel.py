from src.modules.update_court.app.update_court_viewmodel import UpdateCourtViewmodel
from src.shared.domain.entities.court import Court
from src.shared.domain.enums.status_enum import STATUS
from src.shared.infra.repositories.reservation_repository_mock import ReservationRepositoryMock


class TestUpdateCourtViewModel:

    def test_update_court_viewmodel(self):
        court_number = 1
        repo = ReservationRepositoryMock()

        court = repo.get_court(court_number)

        viewmodel = UpdateCourtViewmodel(court=court)

        expected = {
            'updated_court': {
                'number': court.number,
                'status': court.status.value,
                'is_field': court.is_field,
                'photo': court.photo
            },
            'message': 'the court was updated'
        }

        assert viewmodel.to_dict() == expected
