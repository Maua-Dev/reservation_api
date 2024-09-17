import os
from inspect import stack

from aws_cdk import (
    aws_lambda as lambda_,
    NestedStack, Duration,
)
from constructs import Construct
from aws_cdk.aws_apigateway import Resource, LambdaIntegration

from iac.app import stack_name
from iac.get_stage import get_stage_env


class LambdaStack(Construct):
    functions_that_need_dynamo_permissions = []

    def create_lambda_api_gateway_integration(self, module_name: str, method: str, mss_student_api_resource: Resource,
                                              environment_variables: dict = {"STAGE": "TEST"}):
        stack_name = os.environ.get("STACK_NAME")
        stage = get_stage_env()

        function = lambda_.Function(
            self, 
            function_name=f"{stack_name}_{module_name.title()}_{stage}",
            code=lambda_.Code.from_asset(f"../src/modules/{module_name}"),
            handler=f"app.{module_name}_presenter.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            layers=[self.lambda_layer],
            environment=environment_variables,
            timeout=Duration.seconds(15)
        )

        mss_student_api_resource.add_resource(module_name.replace("_", "-")).add_method(method,
                                                                                        integration=LambdaIntegration(
                                                                                            function))

        return function

    def __init__(self, scope: Construct, api_gateway_resource: Resource, environment_variables: dict) -> None:
        self.stack_name = os.environ.get("STACK_NAME")
        stage = get_stage_env()
        
        super().__init__(scope, f"{self.stack_name}_LambdaStack_{stage}")

        self.lambda_layer = lambda_.LayerVersion(self, f"{self.stack_name}_Lambda_Layer_{stage}",
                                                 code=lambda_.Code.from_asset("./copied_shared"),
                                                 compatible_runtimes=[lambda_.Runtime.PYTHON_3_9]
                                                 )


        # self.create_court = self.create_lambda_api_gateway_integration(
        #     module_name="create_court",
        #     method="POST",
        #     mss_student_api_resource=api_gateway_resource,
        #     environment_variables=environment_variables
        # )
        
        # self.get_court = self.create_lambda_api_gateway_integration(
        #     module_name="get_court",
        #     method="GET",
        #     mss_student_api_resource=api_gateway_resource,
        #     environment_variables=environment_variables
        # )
        
        # self.update_court = self.create_lambda_api_gateway_integration(
        #     module_name="update_court",
        #     method="PUT",
        #     mss_student_api_resource=api_gateway_resource,
        #     environment_variables=environment_variables
        # )
        
        # self.delete_court = self.create_lambda_api_gateway_integration(
        #     module_name="delete_court",
        #     method="DELETE",
        #     mss_student_api_resource=api_gateway_resource,
        #     environment_variables=environment_variables
        # )
        
        # self.get_all_courts = self.create_lambda_api_gateway_integration(
        #     module_name="get_all_courts",
        #     method="GET",
        #     mss_student_api_resource=api_gateway_resource,
        #     environment_variables=environment_variables
        # )
        
        self.health_check = self.create_lambda_api_gateway_integration(
            module_name="health_check",
            method="GET",
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables
        )

        # self.functions_that_need_dynamo_permissions = [self.get_user_function, self.create_user_function,
                                                #   self.delete_user_function, self.update_user_function]
