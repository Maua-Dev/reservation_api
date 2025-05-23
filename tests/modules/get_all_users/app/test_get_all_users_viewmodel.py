import pytest
from src.modules.get_all_users.app.get_all_users_usecase import GetAllUsersUseCase
from src.modules.get_all_users.app.get_all_users_viewmodel import GetAllUsersViewModel
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock


class Test_GetAllUsersViewModel:
    @pytest.mark.skip("Can't run test in github actions") 
    def test_get_all_users_viewmodel(self):
        repo = BookingRepositoryMock()
        usecase = GetAllUsersUseCase(repo)

        user_list = usecase()

        viewmodel = GetAllUsersViewModel(user_list)

        assert viewmodel.to_dict() == {
            'users': [
                {
                    'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
                    'name': 'GUSTAVO ALVES GOMES'
                },
                {
                    'user_id': 'd351a9b1-937f-423c-a9d1-9929b5795be1',
                    'name': 'LEONARDO LUIZ SEIXAS IORIO'
                },
                {
                    'user_id': 'c07e0862-3c07-4227-ab0f-511a267cb7ff',
                    'name': 'VICTOR AUGUSTO DE GASPERI'
                }
            ],
            'message': 'the users were retrieved'
        }
