from src.shared.domain.repositories.booking_repository_interface import IBookingRepository
from src.shared.helpers.errors.usecase_errors import DynamoDBBaseError


class GenerateReportExtractor:

    def __init__(self, booking_repository: IBookingRepository):
        self.booking_repository = booking_repository

    def __call__(self, initial_date, final_date):

        try:

            #TODO Add method to interface
            bookings = self.booking_repository.get_all_bookings_by_date_range(initial_date, final_date)

        except:
            raise DynamoDBBaseError("Error extracting bookings from dynamo")

        return bookings
