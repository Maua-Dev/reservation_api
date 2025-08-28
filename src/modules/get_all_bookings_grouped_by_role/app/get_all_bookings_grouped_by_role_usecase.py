from src.shared.clients.user_api_client import UserAPIClient
from src.shared.domain.repositories.booking_repository_interface import IBookingRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class GetAllBookingsGroupedByRoleUsecase:

    def __init__(self, repo: IBookingRepository):
        self.repo = repo
        self.user_client = UserAPIClient()

    def __call__(self):
        all_users = self.user_client.all_users
        
        all_bookings = self.repo.get_all_bookings()

        if all_bookings is None:
            raise NoItemsFound('all_bookings')

        all_bookings_by_role = {
            'UNKNOWN': []
        }

        for user in all_users:

            user_role = user.get('role', None)
            user_id = user.get('user_id', None)

            if user_role is not None:

                if user_role not in all_bookings_by_role:
                    all_bookings_by_role[user_role] = []

            user_bookings = [booking for booking in all_bookings if booking.user_id == user_id]

            all_bookings_by_role[user_role if user_role is not None else 'UNKNOWN'].extend(user_bookings)

        return all_bookings_by_role


        