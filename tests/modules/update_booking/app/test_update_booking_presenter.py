import pytest
import json

from src.modules.update_booking.app.update_booking_presenter import lambda_handler

class Test_UpdateBookingPresenter:
    def test_lambda_handler(self):
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
            },
            "body": {
                "booking_id": "b1d3bebf-dc0d-4fc1-861c-506a40cc2925",
                "start_date": 1634576165000,
                "end_date": 1634583365000,
                "court_number": 1,
                "sport": "Tennis",
                "materials": ['Raquete', 'Bola', 'Rede', 'Tenis']
            },
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        assert json.loads(response['body'])['message'] == 'the booking was retrieved'