import json
from src.modules.delete_booking.app.delete_booking_presenter import lambda_handler


class TestDeleteBookingPresenter:
    def test_delete_booking_presenter(self):
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
                            'role': 'STUDENT'
                        },
                        "message": "the user was retrieved"
                    })
                },
                "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
                "domainPrefix": "<url-id>",
                "external_interfaces": {
                    "method": "DELETE",
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
            "body": {
                "booking_id": "b1d3bebf-dc0d-4fc1-861c-506a40cc2925"
            },
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }
         
        response = lambda_handler(event, None)

        print(response)
        assert response['statusCode'] == 200
        assert json.loads(response['body'])['message'] == 'the booking was deleted'
         
    def test_delete_booking_presenter_missing_booking_id(self):
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
                            'role': 'STUDENT'
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
            "body": '{}',
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }
    
        response = lambda_handler(event, None)

        assert response['statusCode'] == 400
        assert json.loads(response['body']) == 'Field booking_id is missing'

    def test_delete_booking_not_found(self):
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
                            'role': 'STUDENT'
                        },
                        "message": "the user was retrieved"
                    })
                },
                "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
                "domainPrefix": "<url-id>",
                "external_interfaces": {
                    "method": "DELETE",
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
            "body": '{"booking_id": "b1d3bebf-dc0d-4fc1-861c-506a40cc2926"}',   
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }
    
        response = lambda_handler(event, None)
        print(response)
        assert response['statusCode'] == 404
        assert json.loads(response['body']) == 'No items found for booking'

    def test_delete_booking_wrong_type(self):
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
                            'role': 'STUDENT'
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
            "body": '{"booking_id": "wrong_type"}',
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }
    
        response = lambda_handler(event, None)

        assert response['statusCode'] == 400
        assert json.loads(response['body']) == 'Field booking_id is not valid'