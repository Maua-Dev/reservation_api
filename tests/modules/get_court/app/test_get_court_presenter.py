import json
from src.modules.get_court.app.get_court_presenter import lambda_handler
from src.shared.infra.repositories.reservation_repository_mock import ReservationRepositoryMock


first_court = ReservationRepositoryMock().get_court(1)

class Test_GetCourtPresenter:

    def test_get_court_presenter(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "parameter1=value1&parameter1=value2&parameter2=value",
            "cookies": [
                "cookie1",
                "cookie2"
            ],
            "headers": {
                "header1": "value1",
                "header2": "value1,value2"
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {
                    "claims":
                        {
                            "number": first_court.number,
                            "status": first_court.status,
                            "is_field": first_court.is_field,
                            "photo": first_court.photo
                        }
                },
                "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
                "domainPrefix": "<url-id>",
                "external_interfaces": {
                    "method": "POST",
                    "path": "/my/path",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "agent"
                },
                "requestId": "id",
                "routeKey": "$default",
                "stage": "$default",
                "time": "12/Mar/2020:19:03:58 +0000",
                "timeEpoch": 1583348638390
            },
            "body": "Hello from client!",
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event, None)
        assert response["statusCode"] == 400



    def test_get_court_presenter_invalid_number(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "parameter1=value1&parameter1=value2&parameter2=value",
            "cookies": [
                "cookie1",
                "cookie2"
            ],
            "headers": {
                "header1": "value1",
                "header2": "value1,value2"
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {
                    "claims":
                        {
                            "number": "Um number invalido",
                            "status": first_court.status,
                            "is_field": first_court.is_field,
                            "photo": first_court.photo
                        }
                },
                "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
                "domainPrefix": "<url-id>",
                "external_interfaces": {
                    "method": "POST",
                    "path": "/my/path",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "agent"
                },
                "requestId": "id",
                "routeKey": "$default",
                "stage": "$default",
                "time": "12/Mar/2020:19:03:58 +0000",
                "timeEpoch": 1583348638390
            },
            "body": "Hello from client!",
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event, None)
        assert response["statusCode"] == 400

    def test_get_enrollment_presenter_nonexistent_number(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "parameter1=value1&parameter1=value2&parameter2=value",
            "cookies": [
                "cookie1",
                "cookie2"
            ],
            "headers": {
                "header1": "value1",
                "header2": "value1,value2"
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {
                    "claims":
                        {
                            "number": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                            "status": first_court.status,
                            "is_field": first_court.is_field,
                            "photo": first_court.photo
                        }
                },
                "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
                "domainPrefix": "<url-id>",
                "external_interfaces": {
                    "method": "POST",
                    "path": "/my/path",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "agent"
                },
                "requestId": "id",
                "routeKey": "$default",
                "stage": "$default",
                "time": "12/Mar/2020:19:03:58 +0000",
                "timeEpoch": 1583348638390
            },
            "body": "Hello from client!",
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event, None)
        assert response["statusCode"] == 400