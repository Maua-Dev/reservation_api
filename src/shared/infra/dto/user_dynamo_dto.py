from decimal import Decimal

from src.shared.domain.enums.status_enum import STATUS
from src.shared.domain.entities.court import Court

class CourtDynamoDTO:
    number: int
    status: STATUS
    is_field: bool
    photo: str = None
    MIN_PHOTO_LENGTH = 3


    def __init__(self, number: int, status: STATUS, is_field: bool, photo: str = None):
        self.number = number
        self.status = status
        self.is_field = is_field
        self.photo = photo

    @staticmethod
    def from_entity(court: Court) -> "CourtDynamoDTO":
        """
        Parse data from User to CourtDynamoDTO
        """
        return CourtDynamoDTO(
            number=court.number,
            status=court.status,
            is_field=court.is_field,
            photo=court.photo
        )

    def to_dynamo(self) -> dict:
        """
        Parse data from CourtDynamoDTO to dict
        """
        return {
            "entity": "Court",
            "number": self.number,
            "status": self.status.value,
            "is_field": self.is_field,
            "state": self.state.value
        }

    @staticmethod
    def from_dynamo(court_data: dict) -> "CourtDynamoDTO":
        """
        Parse data from DynamoDB to CourtDynamoDTO
        @param court_data: dict from DynamoDB
        """
        return CourtDynamoDTO(
            number=court_data["number"],
            status=STATUS(court_data["status"]),
            is_field=bool(court_data["is_field"]),
            photo=court_data["state"]
        )

    def to_entity(self) -> Court:
        """
        Parse data from CourtDynamoDTO to User
        """
        return Court(
            number=self.number,
            status=self.status,
            is_field=self.is_field,
            photo=self.photo
        )

    def __repr__(self):
        return f"CourtDynamoDto(number={self.number}, status={self.status}, is_field={self.is_field}, photo={self.photo})"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
