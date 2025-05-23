import pytest
from src.modules.get_all_users.app.get_all_users_usecase import GetAllUsersUseCase
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock  

class Test_GetAllUsersUsecase:
    @pytest.mark.skip("Can't run test in github actions") 
    def test_get_all_users_usecase(self):
        repo = BookingRepositoryMock()

        usecase = GetAllUsersUseCase(repo)

        result = usecase()

        assert len(result) == 3  
        assert result[0]["user_id"] == "1f25448b-3429-4c19-8287-d9e64f17bc3a"