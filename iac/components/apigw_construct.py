from aws_cdk import Resource, aws_apigateway as apigateway
from constructs import Construct
from aws_cdk.aws_apigateway import RestApi, Cors, CorsOptions, GatewayResponse, ResponseType


class ApigwConstruct(Construct):
    rest_api: RestApi
    api_gateway_resource: Resource
    
    def __init__(
        self, 
        scope: Construct, 
        construct_id: str, 
        stage: str, 
        **kwargs
    ):
        
        stage = stage.capitalize()
        
        super().__init__(scope, construct_id, **kwargs)
        
        cors_options = CorsOptions(
            allow_origins =
                [
                    "https://reservation.maua.br",
                    "https://reservation.devmaua.com"
                ] 
            if stage == 'Prod'
            else 
                [
                    "https://reservation.hml.devmaua.com",
                    "https://reservation.dev.devmaua.com",
                    "https://localhost:3000",
                    "http://localhost:3000"
                ],
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=Cors.DEFAULT_HEADERS
        )

        self.rest_api = RestApi(
            self, f"ReservationApi_RestApi_{stage}",
            rest_api_name=f"ReservationApi_RestApi_{stage}",
            description="This is the Maua Reservation RestApi",
            deploy_options=apigateway.StageOptions(
                stage_name=stage.lower(),
                logging_level=apigateway.MethodLoggingLevel.INFO,
                data_trace_enabled=False,
                metrics_enabled=True,
            ),
            default_cors_preflight_options=cors_options
        )
        
        GatewayResponse(
            self,
            "AuthorizerDenyResponse",
            rest_api=self.rest_api,
            type=ResponseType.ACCESS_DENIED,
            response_headers={
                "Access-Control-Allow-Origin": "'*'",
                "Access-Control-Allow-Headers": "'*'",
                "Access-Control-Allow-Methods": "'*'",
            },
            status_code="403"
        )
        
        GatewayResponse(
            self,
            "AuthorizerUnauthorizedResponse",
            rest_api=self.rest_api,
            type=ResponseType.UNAUTHORIZED,
            response_headers={
                "Access-Control-Allow-Origin": "'*'",
                "Access-Control-Allow-Headers": "'*'",
                "Access-Control-Allow-Methods": "'*'",
            },
            status_code="401"
        )

        self.api_gateway_resource = self.rest_api.root.add_resource(
            "reservation-api",
            default_cors_preflight_options=cors_options
        )