import pytest
from src.shared.infra.repositories.reservation_repository_mock import ReservationRepositoryMock
from src.shared.infra.repositories.reservation_repository_dynamo import ReservationRepositoryDynamo



class Test_ReservationRepositoryMock:
    def test_get_court(self):
        repo = ReservationRepositoryDynamo()

        resp = repo.get_court(3)

        assert resp.number == 3

