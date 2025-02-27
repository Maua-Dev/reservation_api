import pytest

from src.modules.update_booking.app.update_booking_usecase import UpdateBookingUsecase
from src.shared.domain.enums.sport import SPORT
from src.shared.helpers.errors.domain_errors import EntityError, EntityParameterOrderDatesError, EntityParameterTimeError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock


class Test_UpdateBookingUsecase:
    def test_update_booking_usecase(self):
        booking_repo = BookingRepositoryMock()
        usecase = UpdateBookingUsecase(booking_repo=booking_repo)

        booking_id = booking_repo.bookings[0].booking_id

        booking = usecase(booking_id=booking_id, 
                          court_number=2, 
                          start_date=1634576165000, 
                          end_date=1634583365000, 
                          sport=SPORT.TENNIS, 
                          materials=['Raquete', 'Bola', 'Rede', 'Tenis']
                        )
        
        assert booking_id == booking.booking_id
        assert booking_repo.bookings[0].court_number == booking.court_number
        assert booking_repo.bookings[0].start_date == booking.start_date
        assert booking_repo.bookings[0].end_date == booking.end_date
        assert booking_repo.bookings[0].sport == booking.sport
        assert booking_repo.bookings[0].materials == booking.materials

    def test_update_booking_usecase_invalid_booking_id(self):
        booking_repo = BookingRepositoryMock()
        usecase = UpdateBookingUsecase(booking_repo=booking_repo)

        with pytest.raises(EntityError):
            booking = usecase(booking_id=111, 
                              court_number=2, 
                              start_date=1634576165000, 
                              end_date=1634583365000, 
                              sport=SPORT.TENNIS, 
                              materials=['Raquete', 'Bola', 'Rede', 'Tenis']
            )

    def test_update_booking_usecase_invalid_dates(self):
        booking_repo = BookingRepositoryMock()
        usecase = UpdateBookingUsecase(booking_repo=booking_repo)

        with pytest.raises(EntityError):
            booking = usecase(booking_id=booking_repo.bookings[0].booking_id, 
                              court_number=2, 
                              start_date="1634583365000", 
                              end_date="1634576165000", 
                              sport=SPORT.TENNIS, 
                              materials=['Raquete', 'Bola', 'Rede', 'Tenis']
            )
            
    def test_update_booking_usecase_invalid_sport(self):
        booking_repo = BookingRepositoryMock()
        usecase = UpdateBookingUsecase(booking_repo=booking_repo)

        with pytest.raises(EntityError):
            booking = usecase(booking_id=booking_repo.bookings[0].booking_id, 
                              court_number=2, 
                              start_date=1634576165000, 
                              end_date=1634583365000, 
                              sport='BADMINTON', 
                              materials=['Raquete', 'Bola', 'Rede', 'Tenis']
            )
    
    def test_update_booking_usecase_invalid_materials(self):
        booking_repo = BookingRepositoryMock()
        usecase = UpdateBookingUsecase(booking_repo=booking_repo)

        with pytest.raises(EntityError):
            booking = usecase(booking_id=booking_repo.bookings[0].booking_id, 
                              court_number=2, 
                              start_date=1634576165000, 
                              end_date=1634583365000, 
                              sport=SPORT.TENNIS, 
                              materials='Raquete'
            )
    
    def test_update_booking_usecase_none_booking_id(self):
        booking_repo = BookingRepositoryMock()
        usecase = UpdateBookingUsecase(booking_repo=booking_repo)

        with pytest.raises(EntityError):
            booking = usecase(booking_id=None, 
                              court_number=2, 
                              start_date=1634576165000, 
                              end_date=1634583365000, 
                              sport=SPORT.TENNIS, 
                              materials=['Raquete', 'Bola', 'Rede', 'Tenis']
            )     

    def test_update_booking_usecase_none_court_number(self):
        booking_repo = BookingRepositoryMock()
        usecase = UpdateBookingUsecase(booking_repo=booking_repo)

        with pytest.raises(EntityError):
            booking = usecase(booking_id=booking_repo.bookings[0].booking_id, 
                              court_number=None, 
                              start_date=1634576165000, 
                              end_date=1634583365000, 
                              sport=SPORT.TENNIS, 
                              materials=['Raquete', 'Bola', 'Rede', 'Tenis']
            ) 
    
    def test_update_booking_usecase_none_start_date(self):
        booking_repo = BookingRepositoryMock()
        usecase = UpdateBookingUsecase(booking_repo=booking_repo)

        with pytest.raises(EntityError):
            booking = usecase(booking_id=booking_repo.bookings[0].booking_id, 
                              court_number=2, 
                              start_date=None, 
                              end_date=1634583365000, 
                              sport=SPORT.TENNIS, 
                              materials=['Raquete', 'Bola', 'Rede', 'Tenis']
            )

    def test_update_booking_usecase_none_end_date(self):
        booking_repo = BookingRepositoryMock()
        usecase = UpdateBookingUsecase(booking_repo=booking_repo)

        with pytest.raises(EntityError):
            booking = usecase(booking_id=booking_repo.bookings[0].booking_id, 
                              court_number=2, 
                              start_date=1634576165000, 
                              end_date=None, 
                              sport=SPORT.TENNIS, 
                              materials=['Raquete', 'Bola', 'Rede', 'Tenis']
            )
        
    def test_update_booking_usecase_order_dates_incorrect(self):
        booking_repo = BookingRepositoryMock()
        usecase = UpdateBookingUsecase(booking_repo=booking_repo)

        with pytest.raises(EntityParameterOrderDatesError):
            booking = usecase(booking_id=booking_repo.bookings[0].booking_id, 
                              court_number=2, 
                              start_date=1634583365000, 
                              end_date=1634576165000, 
                              sport=SPORT.TENNIS, 
                              materials=['Raquete', 'Bola', 'Rede', 'Tenis']
            )
    
    def test_update_booking_usecase_none_sport(self):
        booking_repo = BookingRepositoryMock()
        usecase = UpdateBookingUsecase(booking_repo=booking_repo)

        with pytest.raises(EntityError):
            booking = usecase(booking_id=booking_repo.bookings[0].booking_id, 
                              court_number=2, 
                              start_date=1634576165000, 
                              end_date=1634583365000, 
                              sport=None, 
                              materials=['Raquete', 'Bola', 'Rede', 'Tenis']
            )

    def test_update_booking_usecase_none_materials(self):
        booking_repo = BookingRepositoryMock()
        usecase = UpdateBookingUsecase(booking_repo=booking_repo)

        with pytest.raises(EntityError):
            booking = usecase(booking_id=booking_repo.bookings[0].booking_id, 
                              court_number=2, 
                              start_date=1634576165000, 
                              end_date=1634583365000, 
                              sport=SPORT.TENNIS, 
                              materials=None
            )