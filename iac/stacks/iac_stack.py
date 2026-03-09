from aws_cdk import (
    Stack, aws_iam
)
from constructs import Construct
from aws_cdk.aws_apigateway import RestApi, Cors
import os

from .bucket_stack import BucketStack
from .lambda_stack import LambdaStack
from .dynamo_stack import DynamoStack


class IacStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        self.github_ref = os.environ.get('GITHUB_REF_NAME')
        stage = ''
        if 'prod' in self.github_ref:
            stage = 'PROD'
        elif 'homolog' in self.github_ref:
            stage = 'HOMOLOG'
        else:
            stage = 'DEV'

        self.aws_region = os.environ.get("AWS_REGION")
        stack_name = os.environ.get("STACK_NAME")

        self.rest_api = RestApi(
            self, f"{stack_name}_RestApi_{stage}",
            rest_api_name=f"{stack_name}_RestApi_{stage}",
            description="This is the Maua Reservation RestApi",
            default_cors_preflight_options= 
            {
                "allow_origins": Cors.ALL_ORIGINS,
                "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": Cors.DEFAULT_HEADERS
            }
        )

        api_gateway_resource = self.rest_api.root.add_resource(
            "reservation-api", 
            default_cors_preflight_options= 
            {
                "allow_origins": Cors.ALL_ORIGINS,
                "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": Cors.DEFAULT_HEADERS
            }
        )

        self.dynamo_table = DynamoStack(self)
        self.s3_bucket = BucketStack(self)

        ENVIRONMENT_VARIABLES = {
            "STAGE": stage,
            "DYNAMO_TABLE_NAME": self.dynamo_table.table.table_name,
            "DYNAMO_PARTITION_KEY": "PK",
            "DYNAMO_SORT_KEY": "SK",
            "REGION": self.aws_region,
            "USER_API_URL": os.environ.get("USER_API_URL"),
            "S3_BUCKET_NAME": self.s3_bucket.bucket.bucket_name,
            "FROM_EMAIL": os.environ.get("FROM_EMAIL"),
            "HIDDEN_COPY": os.environ.get("HIDDEN_COPY"),
            "S3_ASSETS_CDN": os.environ.get("S3_ASSETS_CDN")
        }



        self.lambda_stack = LambdaStack(self, api_gateway_resource=api_gateway_resource,
                                        environment_variables=ENVIRONMENT_VARIABLES)

        for function in self.lambda_stack.functions_that_need_dynamo_permissions:
            self.dynamo_table.table.grant_read_write_data(function)

        for function in self.lambda_stack.functions_that_need_s3_permissions:
            self.s3_bucket.bucket.grant_read_write(function)

        ses_admin_policy = aws_iam.PolicyStatement(
            effect=aws_iam.Effect.ALLOW,
            actions=[
                "ses:*",
            ],
            resources=[
                "*"
            ]
        )

        functions_that_need_ses_permissions = [
            self.lambda_stack.delete_booking
        ]

        for f in functions_that_need_ses_permissions:
            f.add_environment("HIDDEN_COPY", os.environ.get("HIDDEN_COPY"))
            f.add_environment("FROM_EMAIL", os.environ.get("FROM_EMAIL"))
            f.add_environment("REPLY_TO_EMAIL", os.environ.get("REPLY_TO_EMAIL"))
            f.add_to_role_policy(ses_admin_policy)
        
