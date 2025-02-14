from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.sport import SPORT
from src.shared.domain.repositories.booking_repository_interface import IBookingRepository
from src.shared.environments import Environments
from src.shared.infra.dto.booking_dynamo_dto import BookingDynamoDTO
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource


class BookingRepositoryDynamo(IBookingRepository):

    @staticmethod
    def booking_partition_key_format() -> str:
        return f'Booking'

    @staticmethod
    def booking_sort_key_format(time: int) -> str:
        return f'booking@{time}'

    def __init__(self):
        self.dynamo = DynamoDatasource(
            endpoint_url=Environments.get_envs().endpoint_url,
            dynamo_table_name=Environments.get_envs().dynamo_table_name,
            region=Environments.get_envs().region,
            partition_key=Environments.get_envs().dynamo_partition_key,
            sort_key=Environments.get_envs().dynamo_sort_key,
        )


    def create_booking(self, booking: Booking) -> Booking:

        item = BookingDynamoDTO.from_entity(booking).to_dynamo()

        resp = self.dynamo.put_item(item,
                                    partition_key=self.booking_partition_key_format(),
                                    sort_key=self.booking_sort_key_format(booking.start_date))

        return booking

    def update_booking(self, start_date: int, end_date: int, court_number: int, sport: SPORT) -> Booking:
        pass

    def get_booking(self, booking_id: int):
        pass

    def delete_booking(self, booking_id: int):
        pass

    def get_all_bookings(self):

        all_bookings = []
        all_items = self.dynamo.get_all_items().get('Items')

        for item in all_items:
            if item.get('entity') == 'booking':
                all_bookings.append(BookingDynamoDTO.from_dynamo(item).to_entity())

        return all_bookings

