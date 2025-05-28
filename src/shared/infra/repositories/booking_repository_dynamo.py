from typing import Optional, List

from boto3.dynamodb.conditions import Key

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
    def booking_sort_key_format(booking_start_date: int) -> str:
        #for better sorting and query with get methods
        return f'start_date@{booking_start_date}'

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
                                    sort_key=self.booking_sort_key_format(booking.start_date))

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
            "sport": sport.value if sport is not None else booking_to_update.sport.value,
            "materials": materials if materials is not None else booking_to_update.materials,
            "user_id": booking_to_update.user_id,
            "booking_id": booking_to_update.booking_id,
        }

        resp = self.dynamo.update_item(update_dict=update_dict,
                                       partition_key=self.booking_partition_key_format(),
                                       sort_key=self.booking_sort_key_format(start_date))

        if resp.get('ResponseMetadata').get('HTTPStatusCode') != 200:
            return None

        return BookingDynamoDTO.from_dynamo(resp['Attributes']).to_entity()

    def get_bookings(self,
                     booking_id: Optional[str] = None,
                     user_id: Optional[str] = None,
                     sport: Optional[SPORT] = None,
                     court_number: Optional[int] = None,
                     end_date: Optional[int] = None,
                     start_date: Optional[int] = None) -> List[Optional[Booking]]:

        filters = locals().copy()
        filters.pop('self')
        filters.pop('end_date')
        filters.pop('start_date')

        filters = {k: v for k, v in filters.items() if v is not None}

        all_bookings = self.get_all_bookings()

        bookings = []

        for booking in all_bookings:
            booking_dict = booking.__dict__
            if start_date and end_date:
                if all(
                    booking_dict.get(key) == value for key, value in filters.items()
                ) and booking.start_date >= start_date and booking.end_date <= end_date:
                    bookings.append(booking)
            else:
                if all(
                    booking_dict.get(key) == value for key, value in filters.items()
                ):
                    bookings.append(booking)

        return bookings

    def get_booking(self, booking_id: str) -> Optional[Booking]:

        response = self.dynamo.query(
            IndexName="booking_id-index", #hard coded for now, this should be a variable at somewhere, maybe at gh variables?
            key_condition_expression=Key("booking_id").eq(booking_id),
        )

        items = response.get('Items', [])

        if not items:
            return None

        booking_data_from_dynamo = items[0]

        print(f"Item encontrado no GSI: {booking_data_from_dynamo}")

        return BookingDynamoDTO.from_dynamo(booking_data_from_dynamo).to_entity()


    def delete_booking(self, booking_id: str) -> Optional[Booking]:

        gsi_response = self.dynamo.query(
            IndexName="booking_id-index",
            key_condition_expression=Key("booking_id").eq(booking_id),
        )

        print(gsi_response)

        item_from_gsi = gsi_response.get('Items', [])

        if not item_from_gsi:
            return None

        item_to_delete_info = item_from_gsi[0]

        start_date_ts_ddb_value = item_to_delete_info.get("start_date", None)

        actual_start_date_ts = int(start_date_ts_ddb_value)

        delete_item_response = self.dynamo.delete_item(
            partition_key=self.booking_partition_key_format(),
            sort_key=self.booking_sort_key_format(actual_start_date_ts)
        )

        if "Attributes" not in delete_item_response:
            return None

        return BookingDynamoDTO.from_dynamo(delete_item_response['Attributes']).to_entity()

    def get_all_bookings(self) -> Optional[List[Booking]]:

        all_bookings = []
        all_items = self.dynamo.get_all_items().get('Items')

        for item in all_items:
            if item.get('entity') == 'booking':
                all_bookings.append(BookingDynamoDTO.from_dynamo(item).to_entity())

        return all_bookings

