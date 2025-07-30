import json

from src.modules.create_booking.app.create_booking_presenter import lambda_handler


class TestCreateBookingPresenter:

    def test_create_booking_presenter(self):

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
                            "user_id": "c8435c66-13a4-4641-9d54-773b4b8ccc98",
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
            "body": '{"start_date": 1610617200, "end_date": 1610620800, "court_number": 1, "sport": "Tennis", "materials": ["ball", "racket"]}',
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event, None)

        print(response)
        assert response['statusCode'] == 201
        assert json.loads(response['body'])['message'] == 'Booking created successfully'