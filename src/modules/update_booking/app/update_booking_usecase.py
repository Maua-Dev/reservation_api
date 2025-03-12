from typing import List
from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.sport import SPORT
from src.shared.domain.repositories.booking_repository_interface import IBookingRepository
from src.shared.helpers.errors.domain_errors import EntityError, EntityParameterOrderDatesError, EntityParameterTimeError
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class UpdateBookingUsecase:
    def __init__(self, booking_repo: IBookingRepository):
        self.booking_repo = booking_repo

    def __call__(self, 
                 booking_id: str, 
                 start_date: int, 
                 end_date: int, 
                 court_number: int, 
                 sport: SPORT, 
                 materials: List[str] = None):

        if Booking.validate_booking_id(booking_id) is False: 
            raise EntityError('booking_id')
        
        if Booking.validate_dates(start_date, end_date) is False:
            raise EntityError("date")
        
        if Booking.validate_order_dates(start_date, end_date) is False:
            raise EntityParameterOrderDatesError(start_date, end_date)

        if Booking.validate_court(court_number) is False:
            raise EntityError("court_number")
             
        if Booking.validate_sport(sport) is False:
            raise EntityError("sport")
            
        if Booking.validate_materials(materials) is False:
            raise EntityError("materials")
            
        booking = self.booking_repo.update_booking(booking_id=booking_id,
                                                   start_date=start_date,
                                                   end_date=end_date,
                                                   court_number=court_number,
                                                   sport=sport,
                                                   materials=materials)
        
        return booking
        
            
             
        
        

