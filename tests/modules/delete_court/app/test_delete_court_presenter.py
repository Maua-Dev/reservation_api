import json
from src.modules.delete_court.app.delete_court_presenter import lambda_handler


class TestDeleteCourtPresenter:
    def test_delete_court_presenter(self):
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
            "queryStringParameters": {
                "number": "1"
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {
                    "user": json.dumps({
                        "user": {
                            'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
                            'name': 'Nome',
                            'email': 'user@email.com',
                            'role': 'ADMIN'
                        },
                        "message": "the user was retrieved"
                    })
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
            "body": {},
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }
         
        response = lambda_handler(event, None)
        assert response['statusCode'] == 200
        assert json.loads(response['body'])['message'] == 'the court was deleted'
        assert json.loads(response['body'])['court']['number'] == 1
         
    def test_delete_court_presenter_missing_number(self):
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
            "queryStringParameters": {
                "parameter1": "1"
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {
                    "user": json.dumps({
                        "user": {
                            'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
                            'name': 'Nome',
                            'email': 'user@email.com',
                            'role': 'ADMIN'
                        },
                        "message": "the user was retrieved"
                    })
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
            "body": {},
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }
    
        response = lambda_handler(event, None)

        assert response['statusCode'] == 400
        assert json.loads(response['body']) == 'Field number is missing'

    def test_delete_court_not_found(self):
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
            "queryStringParameters": {
                "number": "10"
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {
                    "user": json.dumps({
                        "user": {
                            'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
                            'name': 'Nome',
                            'email': 'user@email.com',
                            'role': 'ADMIN'
                        },
                        "message": "the user was retrieved"
                    })
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
            "body": {},
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }
    
        response = lambda_handler(event, None)

        assert response['statusCode'] == 404
        assert json.loads(response['body']) == 'No items found for court'

    def test_delete_court_wrong_type(self):
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
            "queryStringParameters": {
                "number": "wrong_type"
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {
                    "user": json.dumps({
                        "user": {
                            'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
                            'name': 'Nome',
                            'email': 'user@email.com',
                            'role': 'ADMIN'
                        },
                        "message": "the user was retrieved"
                    })
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
            "body": {},
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }
    
        response = lambda_handler(event, None)

        assert response['statusCode'] == 400
        assert "Field number isn't in the right type" in json.loads(response['body'])