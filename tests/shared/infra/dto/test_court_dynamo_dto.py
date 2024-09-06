from src.shared.domain.entities.court import Court
from src.shared.domain.enums.status_enum import STATUS
from src.shared.infra.dto.court_dynamo_dto import CourtDynamoDTO
from src.shared.infra.repositories.reservation_repository_mock import ReservationRepositoryMock


class Test_CourtDynamoDto:
    def test_from_entity(self):
        repo = ReservationRepositoryMock()

        court_dto = CourtDynamoDTO.from_entity(court=repo.get_court(1))

        expected_court_dto = CourtDynamoDTO(
            number = repo.get_court(1).number,
            status = repo.get_court(1).status,
            is_field = repo.get_court(1).is_field,
            photo = repo.get_court(1).photo

        )

        assert court_dto == expected_court_dto

    def test_to_dynamo(self):
        repo = ReservationRepositoryMock()

        court_dto = CourtDynamoDTO(
            number = repo.get_court(2).number,
            status = repo.get_court(2).status,
            is_field = repo.get_court(2).is_field,
            photo = repo.get_court(2).photo
        )

        court_dynamo = court_dto.to_dynamo()

        expected_dict = {
            "number": repo.get_court(2).number,
            "status": repo.get_court(2).status.value,
            "is_field": repo.get_court(2).is_field,
            "photo": repo.get_court(2).photo,
            "entity": "Court"
        }

        assert court_dynamo == expected_dict

    def test_to_dynamo_photo_none(self):
        repo = ReservationRepositoryMock()

        court_dto = CourtDynamoDTO(
            number = repo.get_court(4).number,
            status = repo.get_court(4).status,
            is_field = repo.get_court(4).is_field,
            photo = None
        )

        user_dynamo = court_dto.to_dynamo()

        expected_dict = {
            "entity": "Court",
            "number": repo.get_court(4).number,
            "status": repo.get_court(4).status.value,
            "is_field": repo.get_court(4).is_field,
            "photo": None
        }

        assert user_dynamo == expected_dict

    def test_from_entity_to_dynamo(self):
        repo = ReservationRepositoryMock()

        court_dto = CourtDynamoDTO.from_entity(court=repo.get_court(3))

        court_dynamo = court_dto.to_dynamo()

        expected_dict = {
            "entity": "Court",
            "number": repo.get_court(3).number,
            "status": repo.get_court(3).status.value,
            "is_field": repo.get_court(3).is_field,
            "photo": repo.get_court(3).photo,
        }

        assert court_dynamo == expected_dict

    def test_from_dynamo_photo_none(self):
        dynamo_dict = {'Item': {'number': 4,
                                'status': 'MAINTENANCE',
                                'is_field': True,
                                'photo': None},
                       'ResponseMetadata': {'RequestId': 'aa6a5e5e-943f-4452-8c1f-4e5441ee6042',
                                            'HTTPStatusCode': 200,
                                            'HTTPHeaders': {'date': 'Fri, 16 Dec 2022 15:40:29 GMT',
                                                            'content-type': 'application/x-amz-json-1.0',
                                                            'x-amz-crc32': '3909675734',
                                                            'x-amzn-requestid': 'aa6a5e5e-943f-4452-8c1f-4e5441ee6042',
                                                            'content-length': '174',
                                                            'server': 'Jetty(9.4.48.v20220622)'},
                                            'RetryAttempts': 0}}

        court_dto = CourtDynamoDTO.from_dynamo(court_data=dynamo_dict["Item"])

        expected_court_dto = CourtDynamoDTO(
            number = 4,
            status = STATUS.MAINTENANCE,
            is_field = True,
            photo = None
        )

        assert court_dto == expected_court_dto

    def test_from_dynamo(self):
        dynamo_dict = {'Item': {'number': 2,
                                'status': 'AVAILABLE',
                                'is_field': False,
                                'photo': 'https://www.linkedin.com/in/giovanna-albuquerque-16917a245/'},
                       'ResponseMetadata': {'RequestId': 'aa6a5e5e-943f-4452-8c1f-4e5441ee6042',
                                            'HTTPStatusCode': 200,
                                            'HTTPHeaders': {'date': 'Fri, 16 Dec 2022 15:40:29 GMT',
                                                            'content-type': 'application/x-amz-json-1.0',
                                                            'x-amz-crc32': '3909675734',
                                                            'x-amzn-requestid': 'aa6a5e5e-943f-4452-8c1f-4e5441ee6042',
                                                            'content-length': '174',
                                                            'server': 'Jetty(9.4.48.v20220622)'},
                                            'RetryAttempts': 0}}

        court_dto = CourtDynamoDTO.from_dynamo(court_data=dynamo_dict["Item"])

        expected_court_dto = CourtDynamoDTO(
            number = 2,
            status = STATUS.AVAILABLE,
            is_field = False,
            photo = 'https://www.linkedin.com/in/giovanna-albuquerque-16917a245/'
        )

        assert court_dto == expected_court_dto

    def test_to_entity(self):
        repo = ReservationRepositoryMock()

        court_dto = CourtDynamoDTO(
            number=repo.get_court(5).number,
            status=repo.get_court(5).status,
            is_field=repo.get_court(5).is_field,
            photo=repo.get_court(5).photo
    )

        court = court_dto.to_entity()

        assert court_dto == court

    def test_from_dynamo_to_entity(self):
        dynamo_item = {'Item': {'number': 2,
                                'status': 'AVAILABLE',
                                'is_field': False,
                                'photo': 'https://www.linkedin.com/in/giovanna-albuquerque-16917a245/'},
                                }

        court_dto = CourtDynamoDTO.from_dynamo(court_data=dynamo_item["Item"])

        court = court_dto.to_entity()

        expected_court = Court(
            number=2,
            status=STATUS.AVAILABLE,    
            is_field=False,
            photo='https://www.linkedin.com/in/giovanna-albuquerque-16917a245/'
        )

        assert court.number == expected_court.number
        assert court.status == expected_court.status
        assert court.is_field == expected_court.is_field
        assert court.photo == expected_court.photo
       
       