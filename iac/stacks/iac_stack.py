from aws_cdk import (
    Stack,
)
from constructs import Construct
from aws_cdk.aws_apigateway import RestApi, Cors
import os

from .lambda_stack import LambdaStack
from .dynamo_stack import DynamoStack
from iac.get_stage import get_stage_env


class IacStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        stage = get_stage_env()
        self.aws_region = os.environ.get("AWS_REGION")
        stack_name = os.environ.get("STACK_NAME")
        region = os.environ.get("AWS_REGION")

        self.rest_api = RestApi(self, f"{stack_name}_RestApi_{stage}",
                                    rest_api_name=f"{stack_name}_RestApi_{stage}",
                                    description="This is the Maua Reservation RestApi",
                                    default_cors_preflight_options=
                                    {
                                        "allow_origins": Cors.ALL_ORIGINS,
                                        "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                                        "allow_headers": ["*"]
                                    },
                                )

        api_gateway_resource = self.rest_api.root.add_resource("mss-reservation", default_cors_preflight_options=
        {
            "allow_origins": Cors.ALL_ORIGINS,
            "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": Cors.DEFAULT_HEADERS
        }
                                                               )

        self.dynamo_table = DynamoStack(self, f"{stack_name}_DynamoStack_{stage}")

        ENVIRONMENT_VARIABLES = {
            "STAGE": stage,
            "DYNAMO_TABLE_NAME": self.dynamo_table.table.table_name,
            "DYNAMO_PARTITION_KEY": "PK",
            "DYNAMO_SORT_KEY": "SK",
            "REGION": region,
        }



        self.lambda_stack = LambdaStack(self, api_gateway_resource=api_gateway_resource,
                                        environment_variables=ENVIRONMENT_VARIABLES)

        # for function in self.lambda_stack.functions_that_need_dynamo_permissions:
        #     self.dynamo_table.table.grant_read_write_data(function)

        