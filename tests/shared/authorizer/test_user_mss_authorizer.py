import json

import pytest

from src.shared.authorizer import user_mss_authorizer
from src.shared.authorizer.user_mss_authorizer import generate_policy, lambda_handler

METHOD_ARN = 'arn:aws:execute-api:sa-east-1:123456789012:abcdef/DEV/GET/get-bookings'


class FakeResponse:
    def __init__(self, status, payload):
        self.status = status
        self.data = json.dumps(payload).encode('utf-8')


class FakePoolManager:
    """Substitui urllib3.PoolManager. Registra as chamadas feitas em `calls`."""

    calls = []

    def __init__(self, status=200, payload=None):
        self.status = status
        self.payload = payload if payload is not None else {
            'id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
            'name': 'CEAF MAUA',
            'role': 'ADMIN',
        }

    def request(self, method, url, headers=None):
        FakePoolManager.calls.append({'method': method, 'url': url, 'headers': headers})
        return FakeResponse(self.status, self.payload)


def install_pool_manager(monkeypatch, status=200, payload=None):
    FakePoolManager.calls = []
    monkeypatch.setattr(
        user_mss_authorizer.urllib3,
        'PoolManager',
        lambda *args, **kwargs: FakePoolManager(status=status, payload=payload),
    )


class TestGeneratePolicy:
    def test_generate_policy_allow_with_context(self):
        policy = generate_policy('user-1', 'Allow', METHOD_ARN, {'user': '{"a": 1}'})

        assert policy['principalId'] == 'user-1'
        assert policy['policyDocument']['Statement'][0]['Effect'] == 'Allow'
        assert policy['policyDocument']['Statement'][0]['Resource'] == METHOD_ARN
        assert policy['context'] == {'user': '{"a": 1}'}

    def test_generate_policy_deny_without_context(self):
        policy = generate_policy('user', 'Deny', METHOD_ARN)

        assert policy['principalId'] == 'user'
        assert policy['policyDocument']['Statement'][0]['Effect'] == 'Deny'
        assert 'context' not in policy


class TestLambdaHandler:
    def test_lambda_handler_valid_token_returns_allow_with_user_context(self, monkeypatch):
        monkeypatch.setenv('USER_API_URL', 'http://fake-user-api/')
        install_pool_manager(monkeypatch)

        event = {'authorizationToken': 'Bearer valid-token', 'methodArn': METHOD_ARN}
        policy = lambda_handler(event, None)

        assert policy['principalId'] == '1f25448b-3429-4c19-8287-d9e64f17bc3a'
        assert policy['policyDocument']['Statement'][0]['Effect'] == 'Allow'
        assert json.loads(policy['context']['user'])['role'] == 'ADMIN'
        assert FakePoolManager.calls[0]['url'] == 'http://fake-user-api/get-user'
        assert FakePoolManager.calls[0]['headers'] == {'Authorization': 'Bearer valid-token'}

    def test_lambda_handler_non_200_returns_deny(self, monkeypatch):
        monkeypatch.setenv('USER_API_URL', 'http://fake-user-api/')
        install_pool_manager(monkeypatch, status=401)

        event = {'authorizationToken': 'Bearer expired-token', 'methodArn': METHOD_ARN}
        policy = lambda_handler(event, None)

        assert policy['principalId'] == 'user'
        assert policy['policyDocument']['Statement'][0]['Effect'] == 'Deny'
        assert 'context' not in policy

    def test_lambda_handler_missing_env_var_returns_deny(self, monkeypatch):
        monkeypatch.delenv('USER_API_URL', raising=False)
        install_pool_manager(monkeypatch)

        event = {'authorizationToken': 'Bearer valid-token', 'methodArn': METHOD_ARN}
        policy = lambda_handler(event, None)

        assert policy['policyDocument']['Statement'][0]['Effect'] == 'Deny'

    def test_lambda_handler_missing_authorization_token_returns_deny(self, monkeypatch):
        monkeypatch.setenv('USER_API_URL', 'http://fake-user-api/')
        install_pool_manager(monkeypatch)

        event = {'methodArn': METHOD_ARN}
        policy = lambda_handler(event, None)

        assert policy['policyDocument']['Statement'][0]['Effect'] == 'Deny'


class TestGetAuthorizationHeader:
    def test_get_authorization_header_exact_case(self):
        headers = {'Authorization': 'Bearer abc', 'Content-Type': 'application/json'}
        assert user_mss_authorizer._get_authorization_header(headers) == 'Bearer abc'

    def test_get_authorization_header_lowercase(self):
        headers = {'authorization': 'Bearer abc'}
        assert user_mss_authorizer._get_authorization_header(headers) == 'Bearer abc'

    def test_get_authorization_header_absent(self):
        assert user_mss_authorizer._get_authorization_header({'Content-Type': 'application/json'}) is None

    def test_get_authorization_header_none_headers(self):
        assert user_mss_authorizer._get_authorization_header(None) is None


class TestFetchUserData:
    def test_fetch_user_data_returns_parsed_json(self, monkeypatch):
        monkeypatch.setenv('USER_API_URL', 'http://fake-user-api/')
        install_pool_manager(monkeypatch, payload={'id': 'u-1', 'role': 'STUDENT'})

        assert user_mss_authorizer._fetch_user_data('valid-token') == {'id': 'u-1', 'role': 'STUDENT'}

    def test_fetch_user_data_raises_without_env_var(self, monkeypatch):
        monkeypatch.delenv('USER_API_URL', raising=False)
        install_pool_manager(monkeypatch)

        with pytest.raises(Exception):
            user_mss_authorizer._fetch_user_data('valid-token')

    def test_fetch_user_data_raises_on_non_200(self, monkeypatch):
        monkeypatch.setenv('USER_API_URL', 'http://fake-user-api/')
        install_pool_manager(monkeypatch, status=500)

        with pytest.raises(Exception):
            user_mss_authorizer._fetch_user_data('valid-token')
