import pytest
from src.shared.domain.entities.court import Court
from src.shared.domain.enums.status_enum import STATUS
from src.shared.helpers.errors.domain_errors import EntityError

class TestCourt:
    
    def test_court(self):
        court = Court(
            number= 1,
            status= STATUS.AVAILABLE,
            is_field= False, 
            photo = 'https://www.linkedin.com/in/rafael-rubio-carnes-b2561b212/'
        )

        assert type(court) == Court
        assert court.number == 1
        assert court.status == STATUS.AVAILABLE
        assert court.is_field == False
        assert court.photo == "https://www.linkedin.com/in/rafael-rubio-carnes-b2561b212/"

    def test_invalid_number(self):
        with pytest.raises(EntityError):
            Court(
            number= 11,
            status= STATUS.AVAILABLE,
            is_field= False, 
            photo = 'https://www.linkedin.com/in/rafael-rubio-carnes-b2561b212/'
        )
    
    def test_none_photo(self):
        court = Court(
            number= 1,
            status= STATUS.AVAILABLE,
            is_field= False
        )

        assert type(court) == Court
        assert court.number == 1
        assert court.status == STATUS.AVAILABLE
        assert court.is_field == False

    def test_status_not_valid(self):
        with pytest.raises(EntityError):
            Court(
            number= 1,
            status= "a",
            is_field= False, 
            photo = 'https://www.linkedin.com/in/rafael-rubio-carnes-b2561b212/'
        )

    def test_is_field_not_bool(self):
        with pytest.raises(EntityError):
            Court(
            number= 1,
            status= STATUS.AVAILABLE,
            is_field= 1, 
            photo = 'https://www.linkedin.com/in/rafael-rubio-carnes-b2561b212/'
        )
    
    def test_wrong_type_number(self):
        with pytest.raises(EntityError):
            Court(
            number ="string", 
            status=STATUS.AVAILABLE,
            is_field=False, 
            photo="photo.jpg" 
            )

    def test_invalid_photo_type(self):
        with pytest.raises(EntityError):
            Court(
            number= 4,
            status= STATUS.AVAILABLE,
            is_field= False, 
            photo = 7
        )
    

    def test_invalid_photo_lenght(self):
        with pytest.raises(EntityError):
            Court(
            number= 4,
            status= STATUS.AVAILABLE,
            is_field= False, 
            photo = "ta"
        )