import pytest
from src.modules.generate_report.app.user_api_client import UserAPIClient


class TestUserAPIClient:

    @pytest.mark.skip("Can't run test in gh actions")
    def test_get_user(self):

        user_client = UserAPIClient()
        user_name = user_client.get_user_name('1f25448b-3429-4c19-8287-d9e64f17bc3a')

        assert user_name == 'GUSTAVO ALVES GOMES'