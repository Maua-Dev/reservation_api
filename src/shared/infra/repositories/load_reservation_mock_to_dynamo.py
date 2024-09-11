import boto3
from src.shared.infra.repositories.reservation_repository_mock import ReservationRepositoryMock
from src.shared.infra.repositories.reservation_repository_dynamo import ReservationRepositoryDynamo

def setup_dynamo_table():
    print("Setting up dynamo table")
    dynamo_client = boto3.client('dynamodb', endpoint_url='http://localhost:8000', region_name='sa-east-1')
    tables = dynamo_client.list_tables()['TableNames']
    table_name = "reservation_api_table"

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
                }
            ],
            BillingMode='PAY_PER_REQUEST',

        )
        print('Table "port_mss_action-table" created!\n')
    else:
        print('Table already exists!\n')

def load_mock_to_local_dynamo():
    repo_dynamo = ReservationRepositoryDynamo()
    repo_mock = ReservationRepositoryMock()

    print('Loading mock to data to dynamo...')

    print("Loading courts")
    count = 0
    for court in repo_mock.courts:
        print(f'Loading court {court.number}...')
        repo_dynamo.create_court(court=court)
        count += 1
        print(court)
    print(f'{count} courts loaded\n')

    print("Done!")

def load_mock_to_real_dynamo():
    repo_dynamo = ReservationRepositoryDynamo()
    repo_mock = ReservationRepositoryMock()

    print('Loading mock data to dynamo...')

    print("Loading courts")
    count = 0
    for court in repo_mock.courts:
        print(f'Loading court {court.number}...')
        repo_dynamo.create_court(court=court)
        count += 1
        print(court)
    print(f'{count} courts loaded\n')

    print("Done!")


if __name__ == '__main__':
    setup_dynamo_table()
    load_mock_to_local_dynamo()