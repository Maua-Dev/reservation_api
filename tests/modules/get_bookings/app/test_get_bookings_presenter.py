import json
from src.modules.get_bookings.app.get_bookings_presenter import lambda_handler
from src.shared.infra.repositories.booking_repository_mock import BookingRepositoryMock

class Test_GetBookingPresenter:

    def test_get_bookings_presenter(self):
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
                "booking_id": "b1d3bebf-dc0d-4fc1-861c-506a40cc2925",
                "user_id": "",
                "sport": "",
                "court_number": "",
                "end_date": "",
                "start_date": ""
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {
                    "user": {
                        "id": "c8435c66-13a4-4641-9d54-773b4b8ccc98",
                        "displayName": "User",
                        "mail": "lbj@maua.br"
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
            "body": {},
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }
        

        response = lambda_handler(event, None)
        assert response['statusCode'] == 200
        assert json.loads(response['body'])['message'] == 'the bookings were retrieved'
        assert json.loads(response['body'])['bookings'][0]['booking_id'] == 'b1d3bebf-dc0d-4fc1-861c-506a40cc2925'
        assert json.loads(response['body'])['bookings'][0]['start_date'] == 1634576165000
        assert json.loads(response['body'])['bookings'][0]['end_date'] == 1634583365000
        assert json.loads(response['body'])['bookings'][0]['court_number'] == 1
        assert json.loads(response['body'])['bookings'][0]['sport'] == 'Tennis'
        assert json.loads(response['body'])['bookings'][0]['user_id'] == 'c8435c66-13a4-4641-9d54-773b4b8ccc98'
        assert json.loads(response['body'])['bookings'][0]['materials'] == ['Raquete', 'Bola', 'Rede', 'Tenis']


    def test_get_bookings_presenter_missing_parameters(self):
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
                    "user": {
                        "id": "c8435c66-13a4-4641-9d54-773b4b8ccc98",
                        "displayName": "User",
                        "mail": "lbj@maua.br"
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
            "body": {},
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }
        
        response = lambda_handler(event, None)
        assert response['statusCode'] == 400
        assert json.loads(response['body']) == 'Empty query parameters: At least one of the filters must be provided: booking_id, user_id, sport, court_number, end_date, start_date'

    def test_get_bookings_presenter_entity_error(self):
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
                "booking_id":'teste'
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {
                    "user": {
                        "id": "c8435c66-13a4-4641-9d54-773b4b8ccc98",
                        "displayName": "User",
                        "mail": "lbj@maua.br"
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
            "body": {},
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event, None)

        assert response['statusCode'] == 400
        assert json.loads(response['body']) == 'Field booking_id is not valid'


    def test_get_bookings_presenter_wrong_type_parameter(self):
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
                "booking_id": '10'
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {
                    "user": {
                        "id": "c8435c66-13a4-4641-9d54-773b4b8ccc98",
                        "displayName": "User",
                        "mail": "lbj@maua.br"
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
            "body": {},
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event, None)

        assert response['statusCode'] == 400
        assert json.loads(response['body']) == 'Field booking_id is not valid'


    def test_get_bookings_presenter_entity_not_found(self):
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
                "booking_id": 'b1d3bebf-dc0d-4fc1-861c-506a40cc2989'
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {
                    "user": {
                        "id": "c8435c66-13a4-4641-9d54-773b4b8ccc98",
                        "displayName": "User",
                        "mail": "lbj@maua.br"
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
            "body": {},
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event, None)

        assert response['statusCode'] == 404
        assert json.loads(response['body']) == 'No items found for booking filters passed'

        





        
