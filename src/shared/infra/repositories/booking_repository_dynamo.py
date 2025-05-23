from typing import Optional, List

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
    def booking_sort_key_format(booking_id: str) -> str:
        return f'booking#{booking_id}'

    def __init__(self):
        self.dynamo = DynamoDatasource(
            endpoint_url=Environments.get_envs().endpoint_url,
            dynamo_table_name=Environments.get_envs().dynamo_table_name,
            region=Environments.get_envs().region,
            partition_key=Environments.get_envs().dynamo_partition_key,
            sort_key=Environments.get_envs().dynamo_sort_key,
        )

    def create_booking(self, booking: Booking) -> Optional[Booking]:

        item = BookingDynamoDTO.from_entity(booking).to_dynamo()

        resp = self.dynamo.put_item(item,
                                    partition_key=self.booking_partition_key_format(),
                                    sort_key=self.booking_sort_key_format(booking.booking_id))

        if resp.get('ResponseMetadata').get('HTTPStatusCode') != 200:
            return None

        return booking

    def update_booking(self,
                       booking_id: str,
                       start_date: int = None,
                       end_date: int = None,
                       court_number: int = None,
                       sport: SPORT = None,
                       materials: List[str] = None) -> Optional[Booking]:

        booking_to_update = self.get_booking(booking_id)

        if booking_to_update is None:
            return None

        update_dict = {
            "start_date": start_date if start_date is not None else booking_to_update.start_date,
            "end_date": end_date if end_date is not None else booking_to_update.end_date,
            "court_number": court_number if court_number is not None else booking_to_update.court_number,
            "sport": sport if sport is not None else booking_to_update.sport,
            "materials": materials if materials is not None else booking_to_update.materials
        }

        resp = self.dynamo.update_item(update_dict=update_dict,
                                       partition_key=self.booking_partition_key_format(),
                                       sort_key=self.booking_sort_key_format(booking_id))

        if resp.get('ResponseMetadata').get('HTTPStatusCode') != 200:
            return None

        return BookingDynamoDTO.from_dynamo(resp['Attributes']).to_entity()

    def get_booking(self, booking_id: str) -> Optional[Booking]:

        dynamo_object = self.dynamo.get_item(partition_key=self.booking_partition_key_format(),
                                           sort_key=self.booking_sort_key_format(booking_id))

        if "Item" not in dynamo_object:
            return None

        return BookingDynamoDTO.from_dynamo(dynamo_object['Item']).to_entity()

    def delete_booking(self, booking_id: str) -> Optional[Booking]:

        delete_booking = self.dynamo.delete_item(partition_key=self.booking_partition_key_format(),
                                                 sort_key=self.booking_sort_key_format(booking_id))
        if "Attributes" not in delete_booking:
            return None

        return BookingDynamoDTO.from_dynamo(delete_booking['Attributes']).to_entity()

    def get_all_bookings(self) -> Optional[List[Booking]]:

        all_bookings = []
        all_items = self.dynamo.get_all_items().get('Items')

        for item in all_items:
            if item.get('entity') == 'booking':
                all_bookings.append(BookingDynamoDTO.from_dynamo(item).to_entity())

    def get_all_bookings_by_date_range(self, initial_date: int, final_date: int) -> Optional[List[Booking]]:

        all_bookings = []
        all_items = self.dynamo.get_all_items().get('Items')

        for item in all_items:
            if item.get('entity') == 'booking':
                booking = BookingDynamoDTO.from_dynamo(item).to_entity()
                if initial_date <= booking.start_date/1000 <= final_date:
                    all_bookings.append(booking)

        return all_bookings
    
    def get_all_users(self):
        return super().get_all_users()

