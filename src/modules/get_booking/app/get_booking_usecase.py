from src.shared.domain.entities.booking import Booking
from src.shared.domain.repositories.booking_repository_interface import IBookingRepository
from src.shared.clients.user_api_client import UserAPIClient
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class GetBookingUseCase:
    repo: IBookingRepository

    def __init__(self, repo: IBookingRepository, user_client=None):
        self.repo = repo
        self.user_client = user_client

    def __call__(self, booking_id: str, requester_role: str = None):
        if not Booking.validate_booking_id(booking_id=booking_id):
            raise EntityError('booking_id')

        booking = self.repo.get_booking(booking_id=booking_id)
        if booking is None:
            raise NoItemsFound('booking_id')

        owner = None
        if requester_role == 'ADMIN':
            client = self.user_client or UserAPIClient()
            try:
                owner = {
                    'name': client.get_user_name(booking.user_id),
                    'network_id': client.get_user_network_id(booking.user_id),
                }
            except Exception as e:
        
                print(f"ERRO NA API DE USER: {e}")
                owner = {
                    'name': 'Erro de integração',
                    'network_id': 'Erro de integração',
                }

        return {'booking': booking, 'owner': owner}
