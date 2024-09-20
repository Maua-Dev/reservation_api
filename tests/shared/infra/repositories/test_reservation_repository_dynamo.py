import pytest
from src.shared.infra.repositories.reservation_repository_mock import ReservationRepositoryMock
from src.shared.infra.repositories.reservation_repository_dynamo import ReservationRepositoryDynamo
from src.shared.domain.entities.court import Court
from src.shared.environments import Environments
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource
from src.shared.domain.enums.status_enum import STATUS
from src.shared.infra.repositories.reservation_repository_dynamo import ReservationRepositoryDynamo
from src.shared.infra.repositories.reservation_repository_mock import ReservationRepositoryMock


class TestReservationRepositoryDynamo:

    @pytest.mark.skip("Can't run test in github actions")
    def test_dynamo_delete_court(self):
        dynamo_repo = ReservationRepositoryDynamo()
        mock_repo = ReservationRepositoryMock()
        court = mock_repo.get_court(3)
        deleted_court = dynamo_repo.delete_court(court.number)
        retrieved_court = dynamo_repo.get_court(court.number)
        assert retrieved_court is None
        assert deleted_court.number == court.number

    @pytest.mark.skip("Can't run test in github actions")
    def test_dynamo_delete_court_not_found(self):
        dynamo_repo = ReservationRepositoryDynamo()
        mock_repo = ReservationRepositoryMock()
        deleted_court = dynamo_repo.delete_court(999)
        assert deleted_court is None

    @pytest.mark.skip("Can't run test in github actions")
    def test_update_court(self):
        repo = ReservationRepositoryDynamo()
        resp = repo.update_court(number=3, new_photo="https://www.linkedin.com/in/giovanna-albuquerque-16917a245/")

        assert resp.number == 3
        assert resp.photo == "https://www.linkedin.com/in/giovanna-albuquerque-16917a245/"

    @pytest.mark.skip("Can't run test in github actions")    
    def test_get_court(self):
        repo = ReservationRepositoryDynamo()

        resp = repo.get_court(3)

        assert resp.number == 3

    @pytest.mark.skip("Github Skip")
    def test_dynamo_create_court(self):
        dynamo_repo = ReservationRepositoryDynamo()
        new_court = Court(number=6, status=STATUS.MAINTENANCE, is_field=False, photo=None)
        size = len(dynamo_repo.get_all_courts())
    
        assert new_court == dynamo_repo.create_court(new_court)
        assert dynamo_repo.get_court(6)== new_court 

        dynamo_repo.delete_court(new_court)

    @pytest.mark.skip("Github Skip")
    def test_dynamo_get_all_courts(self):
        mock_repo = ReservationRepositoryMock()
        dynamo_repo = ReservationRepositoryDynamo()

        dynamo_courts = dynamo_repo.get_all_courts()
        mock_courts = mock_repo.get_all_courts()

        assert len(dynamo_courts) == len(mock_courts)

        for d_court, m_court in zip(dynamo_courts, mock_courts):
            assert d_court.__dict__.items() == m_court.__dict__.items()