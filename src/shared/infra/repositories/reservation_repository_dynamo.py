from src.shared.domain.entities.court import Court
from src.shared.domain.repositories.reservation_repository_interface import IReservationRepository
from src.shared.environments import Environments
from src.shared.infra.dto.court_dynamo_dto import CourtDynamoDTO
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource
from src.shared.domain.enums.status_enum import STATUS
from boto3.dynamodb.conditions import Key

class ReservationRepositoryDynamo(IReservationRepository):
    @staticmethod
    def court_partition_key_format(number: int) -> str:
        return f'court'
    
    @staticmethod
    def court_sort_key_format(number: int) -> str:
        return f'court#{number}'
    

    def __init__(self):
        self.dynamo = DynamoDatasource(
            endpoint_url=Environments.get_envs().endpoint_url,
            dynamo_table_name=Environments.get_envs().dynamo_table_name,
            region=Environments.get_envs().region,
            partition_key=Environments.get_envs().dynamo_partition_key,
            sort_key=Environments.get_envs().dynamo_sort_key,
            gsi_partition_key=Environments.get_envs().dynamo_gsi_1_partition_key,
            gsi_sort_key=Environments.get_envs().dynamo_gsi_1_sort_key,
        )

    def create_court(self, court: Court) -> Court:
        item = CourtDynamoDTO.from_entity(court).to_dynamo()
        resp = self.dynamo.put_item(item, partition_key=self.court_partition_key_format(court.number), sort_key=self.court_sort_key_format(court.number))

        return Court