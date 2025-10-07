import os
from typing import Optional, List

import boto3
from boto3.dynamodb.conditions import Key

from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.sport import SPORT
from src.shared.domain.enums.type import BOOKING_TYPE
from src.shared.domain.repositories.booking_repository_interface import IBookingRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import ForbiddenAction
from src.shared.helpers.functions.compose_delete_booking_email import compose_deleted_user_email
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
                       materials: List[str] = None,
                       booking_type: BOOKING_TYPE = None) -> Optional[Booking]:

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
            "booking_type": booking_type.value if booking_type is not None else booking_to_update.booking_type.value
        }

        resp = self.dynamo.update_item(update_dict=update_dict,
                                       partition_key=self.booking_partition_key_format(),
                                       sort_key=self.booking_sort_key_format(booking_id))

        if resp.get('ResponseMetadata').get('HTTPStatusCode') != 200:
            return None

        return BookingDynamoDTO.from_dynamo(resp['Attributes']).to_entity()

    def get_bookings(self,
                     booking_id: Optional[str] = None,
                     user_id: Optional[str] = None,
                     sport: Optional[str] = None,
                     court_number: Optional[int] = None,
                     booking_type: Optional[str] = None,
                     end_date: Optional[int] = None,
                     start_date: Optional[int] = None
                     ) -> List[Optional[Booking]]:

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

        dynamo_object = self.dynamo.get_item(partition_key=self.booking_partition_key_format(),
                                           sort_key=self.booking_sort_key_format(booking_id))

        if "Item" not in dynamo_object:
            return None

        return BookingDynamoDTO.from_dynamo(dynamo_object['Item']).to_entity()

    def delete_booking(self, booking_id: str, user) -> Optional[Booking]:

        booking = self.get_booking(booking_id)
        user_role = user.get('role')
        user_id = user.get('user_id')

        if not booking:
            return None

        is_admin = user_role == 'ADMIN'
        is_owner = user_role == 'STUDENT' and booking.user_id == user_id

        if is_admin or is_owner:
            deleted = self.dynamo.delete_item(
                partition_key=self.booking_partition_key_format(),
                sort_key=self.booking_sort_key_format(booking_id)
            )

            self.send_user_email(user, deleted)

            return BookingDynamoDTO.from_dynamo(deleted['Attributes']).to_entity()

        if user_role == 'STUDENT':
            raise ForbiddenAction('user id')

        return None
 

    def get_all_bookings(self) -> Optional[List[Booking]]:

        all_bookings = []
        all_items = self.dynamo.get_all_items().get('Items') or []

        for item in all_items:
            if item.get('entity') == 'booking':
                all_bookings.append(BookingDynamoDTO.from_dynamo(item).to_entity())
        
        return all_bookings

    def get_all_bookings_by_date_range(self, initial_date: int, final_date: int) -> Optional[List[Booking]]:

        all_bookings = []
        all_items = self.dynamo.get_all_items().get('Items') or []

        for item in all_items:
            if item.get('entity') == 'booking':
                booking = BookingDynamoDTO.from_dynamo(item).to_entity()
                if initial_date <= booking.start_date/1000 <= final_date:
                    all_bookings.append(booking)

        return all_bookings
    
    def get_all_users(self):
        return super().get_all_users()
    

    def send_user_email(self, user, deleted_booking: Booking) -> bool:
        try:

            client_ses = boto3.client('ses', region_name=os.environ.get('AWS_REGION'))
            email_to_send = compose_deleted_user_email(user, deleted_booking)

            response = client_ses.send_email(
                Destination={
                    'ToAddresses': [
                        user.get('email'),
                    ],
                    'BccAddresses':
                        [
                            Environments.hidden_copy
                        ]
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': "UTF-8",
                            'Data': email_to_send,
                        },
                    },
                    'Subject': {
                        'Charset': "UTF-8",
                        'Data': 'Mauá Reservation - Reserva Cancelada',
                    },
                },
                Source = Environments.from_email,
            )

            

            return True
        except Exception as err:
            print(err)
            return False



