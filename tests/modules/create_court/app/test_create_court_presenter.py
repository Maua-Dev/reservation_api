import json
from src.modules.create_court.app.create_court_presenter import lambda_handler


class TestCreateCourtPresenter:
    def test_create_court_presenter(self):
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
            "body": '{"number": 7, "status": "AVAILABLE", "is_field": false, "photo": "photo"}',
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }
         
        response = lambda_handler(event, None)
        print(response)
        assert response['statusCode'] == 201
        assert json.loads(response['body'])['message'] == 'the court was created'
        assert json.loads(response['body'])['court']['number'] == 7
        assert json.loads(response['body'])['court']['status'] == 'AVAILABLE'
        assert json.loads(response['body'])['court']['is_field'] == False
        assert json.loads(response['body'])['court']['photo'] == 'photo'
         
    def test_create_court_presenter_missing_number(self):
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
            "body": '{"status": "AVAILABLE", "is_field": false, "photo": "photo"}',
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }
    
        response = lambda_handler(event, None)

        assert response['statusCode'] == 400
        assert json.loads(response['body']) == 'Field number is missing'