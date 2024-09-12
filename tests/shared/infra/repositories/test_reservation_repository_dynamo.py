import pytest

from src.shared.domain.entities.court import Court
from src.shared.domain.repositories.reservation_repository_interface import IReservationRepository
from src.shared.environments import Environments
from src.shared.infra.dto.court_dynamo_dto import CourtDynamoDTO
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource
from src.shared.domain.enums.status_enum import STATUS
from boto3.dynamodb.conditions import Key

from src.shared.infra.repositories.reservation_repository_dynamo import ReservationRepositoryDynamo
from src.shared.infra.repositories.reservation_repository_mock import ReservationRepositoryMock


class TestReservationRepositoryDynamo:

    # descomentar dps q tiver o delete

    # @pytest.mark.skip("Github Skip")
    # def test_dynamo_create_court(self):
    #     dynamo_repo = ReservationRepositoryDynamo()
    #     new_court = Court(number=6, status=STATUS.MAINTENANCE, is_field=False, photo=None)
    #     size = len(dynamo_repo.get_all_courts())
    #
    #     assert new_court == dynamo_repo.create_court(new_court)
    #     assert dynamo_repo.get_all_courts()[size] == new_court ----> mudar pro get_court tlvez?

    #     dynamo_repo.delete_court(new_court)
    #     deletar a court dps de testar se nao o proximo teste vai falhar

    @pytest.mark.skip("Github Skip")
    def test_dynamo_get_all_courts(self):
        mock_repo = ReservationRepositoryMock()
        dynamo_repo = ReservationRepositoryDynamo()

        dynamo_courts = dynamo_repo.get_all_courts()
        mock_courts = mock_repo.get_all_courts()

        assert len(dynamo_courts) == len(mock_courts)

        for d_court, m_court in zip(dynamo_courts, mock_courts):
            assert d_court.__dict__.items() == m_court.__dict__.items()
