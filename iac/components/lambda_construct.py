from aws_cdk import (
    aws_lambda as lambda_,
    Duration,
    aws_apigateway as apigw
)
from constructs import Construct
from aws_cdk.aws_apigateway import Resource, LambdaIntegration
from aws_cdk.aws_events import Rule, Schedule, EventField, RuleTargetInput
from aws_cdk.aws_events_targets import LambdaFunction 

class LambdaConstruct(Construct):
    functions_that_need_dynamo_permissions = []
    functions_that_need_s3_permissions = []

    def create_lambda_api_gateway_integration(
        self, 
        module_name: str,
        method: str,
        api_resource: Resource,
        environment_variables: dict = {"STAGE": "TEST"}, 
        authorizer=None
    ):
        
        function = lambda_.Function(
            self, module_name.title(),
            code=lambda_.Code.from_asset(f"../src/modules/{module_name}"),
            handler=f"app.{module_name}_presenter.lambda_handler",
            runtime=lambda_.Runtime("python3.13"),
            layers=[self.lambda_layer],
            environment=environment_variables,
            timeout=Duration.seconds(15)
        )

        api_resource.add_resource(
            module_name.replace("_", "-")
        ).add_method(
            method,
            integration=LambdaIntegration(
                function
            ),
            authorizer=authorizer
        )
        return function

    def create_lambda_event_bridge_integration(
        self,
        module_name: str,
        cron_schedule: Schedule.cron,
        environment_variables: dict = {"STAGE": "TEST"}
    ):
        
        function = lambda_.Function(
            self,
            module_name.title(),
            code=lambda_.Code.from_asset(f"../src/modules/{module_name}"),
            handler=f"app.{module_name}_presenter.lambda_handler",
            runtime=lambda_.Runtime("python3.13"),
            layers=[self.lambda_layer],
            environment=environment_variables,
            timeout=Duration.seconds(15)
        )

        rule = Rule(
            self, f"{module_name.title()}EventRuleForWeeklyUpload",
            schedule=cron_schedule
        )

        input_transformer = RuleTargetInput.from_object({
            "current_date": EventField.time,
            "message": "weekly report trigger!"
        })

        rule.add_target(LambdaFunction(function, event=input_transformer))

        return function

    def __init__(
        self, 
        scope: Construct,
        construct_id: str,
        stage: str,
        api_gateway_resource: Resource,
        environment_variables: dict
    ) -> None:
    
        stage = stage.capitalize()

        super().__init__(scope, f"ReservationApi_LambdaConstruct_{stage}")

        self.lambda_layer = lambda_.LayerVersion(
            self, 
            id=f"ReservationApi_LambdaLayer_{stage}",
            # a pasta .build foi obtida do adjust layer directory, certifique-se de que a configuração da pasta layer gerada la esta igual
            code=lambda_.Code.from_asset("./build"),
            compatible_runtimes=[lambda_.Runtime("python3.13")]
        )
        
        authorizer_lambda = lambda_.Function(
            self, "AuthorizerUserMssReservationApiLambda",
            code=lambda_.Code.from_asset("../src/shared/authorizer"),
            handler="user_mss_authorizer.lambda_handler",
            runtime=lambda_.Runtime("python3.13"),
            layers=[self.lambda_layer],
            environment=environment_variables,
            timeout=Duration.seconds(15)
        )

        token_authorizer_lambda = apigw.TokenAuthorizer(
            self, "TokenAuthorizerReservationApi",
            handler=authorizer_lambda,
            identity_source=apigw.IdentitySource.header("Authorization"),
            authorizer_name="AuthorizerUserMssReservationMssAlertLambda",
            results_cache_ttl=Duration.seconds(0)
        )

        self.create_booking = self.create_lambda_api_gateway_integration(
            module_name="create_booking",
            method="POST",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=token_authorizer_lambda
        )

        self.update_booking = self.create_lambda_api_gateway_integration(
            module_name="update_booking",
            method="PUT",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=token_authorizer_lambda
        )

        self.get_booking = self.create_lambda_api_gateway_integration(
            module_name="get_booking",
            method="GET",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables
        )

        self.get_bookings = self.create_lambda_api_gateway_integration(
            module_name="get_bookings",
            method="GET",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
        )

        self.delete_booking = self.create_lambda_api_gateway_integration(
            module_name="delete_booking",
            method="DELETE",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=token_authorizer_lambda
        )

        self.get_all_bookings = self.create_lambda_api_gateway_integration(
            module_name="get_all_bookings",
            method="GET",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables
        )

        self.create_court = self.create_lambda_api_gateway_integration(
            module_name="create_court",
            method="POST",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=token_authorizer_lambda
        )

        self.get_court = self.create_lambda_api_gateway_integration(
            module_name="get_court",
            method="GET",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables
        )

        self.update_court = self.create_lambda_api_gateway_integration(
            module_name="update_court",
            method="PUT",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=token_authorizer_lambda
        )

        #TODO implementar lógica de deletar foto do bucket ao excluir a quadra pelo s3_client
        # @43 ;)
        self.delete_court = self.create_lambda_api_gateway_integration(
            module_name="delete_court",
            method="DELETE",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=token_authorizer_lambda
        )

        self.get_all_courts = self.create_lambda_api_gateway_integration(
            module_name="get_all_courts",
            method="GET",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables
        )

        self.health_check = self.create_lambda_api_gateway_integration(
            module_name="health_check",
            method="GET",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables
        )

        #does not need auth / not a route
        self.generate_report = self.create_lambda_event_bridge_integration(
            module_name="generate_report",
            cron_schedule=Schedule.cron(minute="30", hour="11", week_day="FRI"),
            environment_variables=environment_variables
        )
        
        self.get_all_admin_bookings = self.create_lambda_api_gateway_integration(
            module_name="get_all_admin_bookings",
            method="GET",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables
        )

        self.get_all_bookings_grouped_by_role = self.create_lambda_api_gateway_integration(
            module_name="get_all_bookings_grouped_by_role",
            method="GET",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables
        )

        self.functions_that_need_dynamo_permissions = [
            self.create_court,
            self.get_court,
            self.update_court,
            self.delete_court,
            self.get_all_courts,
            self.create_booking,
            self.get_booking,
            self.update_booking,
            self.delete_booking,
            self.get_all_bookings,
            self.get_bookings,
            self.generate_report,
            self.get_all_admin_bookings,
            self.get_all_bookings_grouped_by_role
        ]

        self.functions_that_need_s3_permissions = [
            self.create_court,
            self.update_court,
            self.delete_court,
            self.generate_report
        ]
