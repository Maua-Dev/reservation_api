from typing import Dict, List
from src.shared.domain.entities.booking import Booking


class GetAllBookingsGroupedByRoleViewmodel:

    def __init__(self, all_bookings_by_role: Dict[str, List[Booking]]):
        
        self.all_bookings_by_role = all_bookings_by_role

    def to_dict(self):

        return {
            'bookings': self.all_bookings_by_role,
            'message': "The bookings grouped by roles were retrieved."
        }