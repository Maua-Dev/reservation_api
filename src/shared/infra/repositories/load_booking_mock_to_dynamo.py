import boto3
from src.shared.infra.repositories.booking_repository_dynamo import BookingRepositoryDynamo
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock


def setup_dynamo_table():
    print("Setting up dynamo table")
    dynamo_client = boto3.client('dynamodb', endpoint_url='http://localhost:8000', region_name='sa-east-1')
    tables = dynamo_client.list_tables()['TableNames']
    table_name = "local_reservation_api_table"
    gsi_name = "booking_id-index"

    if not table_name in tables:
        print("Creating table")
        dynamo_client.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'PK',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'SK',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'PK',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'SK',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'booking_id',
                    'AttributeType': 'S'
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': gsi_name,
                    'KeySchema': [
                        {
                            'AttributeName': 'booking_id',
                            'KeyType': 'HASH'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    }
                }
            ],
            BillingMode='PAY_PER_REQUEST',

        )
        print('Table "local_reservation_api_table" created!\n')
    else:
        print('Table already exists!\n')


def load_mock_to_local_dynamo():
    repo_dynamo = BookingRepositoryDynamo()
    repo_mock = BookingRepositoryMock()

    print('Loading mock data to dynamo...')

    print('Loading bookings...')

    booking_count = 0
    for booking in repo_mock.bookings:
        print(f'Loading booking {booking.booking_id}...')
        repo_dynamo.create_booking(booking=booking)
        booking_count += 1
    print(f'{booking_count} bookings loaded\n')

    print("Done!")


def load_mock_to_real_dynamo():
    repo_dynamo = BookingRepositoryDynamo()
    repo_mock = BookingRepositoryMock()

    print('Loading mock data to dynamo...')

    print('Loading users...')

    booking_count = 0
    for booking in repo_mock.bookings:
        print(f'Loading booking {booking.booking_id}...')
        repo_dynamo.create_booking(booking=booking)
        booking_count += 1
    print(f'{booking_count} bookings loaded\n')

    print("Done!")


if __name__ == '__main__':
    setup_dynamo_table()
    load_mock_to_local_dynamo()
