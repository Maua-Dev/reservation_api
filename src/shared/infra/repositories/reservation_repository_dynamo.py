from src.shared.domain.entities.court import Court
from src.shared.domain.repositories.reservation_repository_interface import IReservationRepository
from src.shared.environments import Environments
from src.shared.infra.dto.court_dynamo_dto import CourtDynamoDTO
from typing import List, Optional
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
        )

    def create_court(self, court: Court) -> Court:
        item = CourtDynamoDTO.from_entity(court).to_dynamo()
        resp = self.dynamo.put_item(item, partition_key=self.court_partition_key_format(court.number),
                                    sort_key=self.court_sort_key_format(court.number))

        return court

    def get_court(self, number: int):
        court = self.dynamo.get_item(partition_key=self.court_partition_key_format(number),
                                     sort_key=self.court_sort_key_format(number))

        if "Item" not in court:
            return None

        court_dto = CourtDynamoDTO.from_dynamo(court['Item'])
        return court_dto.to_entity()

    def get_all_courts(self) -> list[Court]:

        all_courts = []
        all_items = self.dynamo.get_all_items().get('Items')

        for item in all_items:
            all_courts.append(CourtDynamoDTO.from_dynamo(item).to_entity())

        return all_courts

    def delete_court(self, number: int):
        delete_court = self.dynamo.delete_item(partition_key=self.court_partition_key_format(number),
                                               sort_key=self.court_sort_key_format(number))
        if "Attributes" not in delete_court:
            return None
        attributes = delete_court["Attributes"]
        attributes["number"] = int(attributes["number"])
        return CourtDynamoDTO.from_dynamo(delete_court["Attributes"]).to_entity()

    def update_court(self, number: int, new_status: Optional[STATUS] = None, new_photo: Optional[str] = None) -> Court:
        court_to_update = self.get_court(number=number)

        if court_to_update is None:
            return None

        if new_status is not None:
            court_to_update.status = new_status
        if new_photo is not None:
            court_to_update.photo = new_photo

        update_dict = {
            "status": court_to_update.status.value,
            "photo": court_to_update.photo
        }

        resp = self.dynamo.update_item(partition_key=self.court_partition_key_format(court_to_update),
                                       sort_key=self.court_sort_key_format(court_to_update.number),
                                       update_dict=update_dict)

        if "Attributes" not in resp:
            return None

        return CourtDynamoDTO.from_dynamo(resp["Attributes"]).to_entity()
