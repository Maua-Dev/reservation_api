from src.modules.create_court.app.create_court_viewmodel import CreateCourtViewmodel
from src.shared.domain.entities.court import Court
from src.shared.domain.enums.status_enum import STATUS

class Test_CreateCourtViewModel:
    def test_create_court_viewmodel(self):
        court = Court(
            number = 9,
            status= STATUS.AVAILABLE,
            is_field = False,
            photo = "https://super.abril.com.br/mundo-estranho/os-poneis-sao-cavalos-anoes"
        )

        courtViewmodel = CreateCourtViewmodel(court=court).to_dict()
        expected = {
            "court": {
                'number' : 9,
                'status' :'AVAILABLE',
                'is_field' :False,
                'photo' : "https://super.abril.com.br/mundo-estranho/os-poneis-sao-cavalos-anoes"
            },
            'message': 'the court was created'
        }

    def test_create_court_viewmodel_without_photos(self):
        court = Court(
            number = 8,
            status= STATUS.AVAILABLE,
            is_field = False,
            photo = None
        )

        viewmodel = CreateCourtViewmodel(court).to_dict()
        expected = {
            'court':{
                'number' : 8,
                'status' : STATUS.AVAILABLE,
                'is_field' : False,
                'photo' : None
            },
            'message':'the court was created'
            }

        assert viewmodel == expected
        
