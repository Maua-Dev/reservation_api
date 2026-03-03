from typing import List
from src.shared.domain.entities.booking import Booking
from src.shared.domain.enums.sport import SPORT
from src.shared.domain.enums.type import BOOKING_TYPE
from src.shared.domain.repositories.booking_repository_interface import IBookingRepository
from src.shared.helpers.errors.domain_errors import EntityError, EntityParameterOrderDatesError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound, InvalidSchedule, InvalidSchedulePeriod
from datetime import timedelta

class UpdateBookingUsecase:
    def __init__(self, booking_repo: IBookingRepository):
        self.booking_repo = booking_repo

    def __call__(self, 
                booking_id: str, 
                user: dict,
                start_date: int = None, 
                end_date: int = None, 
                court_number: int = None, 
                sport: SPORT = None, 
                materials: List[str] = None,
                new_user_id: str = None,
                booking_type: BOOKING_TYPE = None):
        
        user_id = user.get('user_id')
        user_role = user.get('role') 

        if Booking.validate_booking_id(booking_id) is False: 
            raise EntityError('booking_id')
        
        existing_booking = self.booking_repo.get_booking(booking_id)
        if existing_booking is None:
            raise NoItemsFound('booking')
        
        if user_role != 'ADMIN':

            booking_user_id = existing_booking.user_id
            if booking_user_id != user_id:
                raise ForbiddenAction('user id')
        
        start_date = start_date if start_date is not None else existing_booking.start_date
        end_date = end_date if end_date is not None else existing_booking.end_date
        court_number = court_number if court_number is not None else existing_booking.court_number
        sport = sport if sport is not None else existing_booking.sport
        materials = materials if materials is not None else existing_booking.materials
        booking_type = booking_type if booking_type is not None else existing_booking.booking_type
        
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
        
        if Booking.validate_booking_type(booking_type) is False:
            raise EntityError("type")
            
        maxtime = start_date + (timedelta(weeks=12).total_seconds()*1000)
        if(end_date > maxtime):
            raise InvalidSchedulePeriod()
        
        
        all_bookings = self.booking_repo.get_all_bookings()

        for booking in all_bookings:
            if (
                (booking.booking_id != booking_id)
                and (
                    (
                        booking.start_date < end_date + (15 * 60 * 1000) #15 minutes in mseconds
                        and booking.end_date > start_date - (15 * 60 * 1000) #15 minutes in mseconds
                        and booking.court_number == court_number
                    )
                )
            ):
                raise InvalidSchedule()

        booking = self.booking_repo.update_booking(
            booking_id=booking_id,
            start_date=start_date,
            end_date=end_date,
            court_number=court_number,
            sport=sport,
            materials=materials,
            booking_type=booking_type
        )
        
        if booking.user_id != existing_booking.user_id:
            booking.user_id = existing_booking.user_id
        
        return booking