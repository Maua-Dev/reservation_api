from src.shared.domain.repositories.booking_repository_interface import IBookingRepository

class GetAllBookingsUsecase:
    def __init__(self, repo: IBookingRepository):
        self.repo = repo

    def __call__(self):

        bookings = self.repo.get_all_bookings()
        
        return bookings