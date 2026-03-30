from aws_cdk import (
    Stack, aws_iam
)
from constructs import Construct
import os

from components.apigw_construct import ApigwConstruct
from components.s3_construct import S3Construct
from components.dynamo_construct import DynamoConstruct
from components.lambda_construct import LambdaConstruct
from components.ssm_construct import SsmConstruct


class IacStack(Stack):

    def __init__(
        self, 
        scope: Construct, 
        stack_id: str, 
        **kwargs
    ) -> None:
        
        super().__init__(scope, stack_id, **kwargs)
        
        self.github_ref = os.environ.get('GITHUB_REF_NAME')
        stage = ''
        if 'prod' in self.github_ref:
            stage = 'PROD'
        elif 'homolog' in self.github_ref:
            stage = 'HOMOLOG'
        else:
            stage = 'DEV'
            
        stage = stage.capitalize()

        self.aws_region = os.environ.get("AWS_REGION")
        
        self.apigw_construct = ApigwConstruct(
            self,
            construct_id="ReservationApiApigw",
            stage=stage,
        )
        
        self.dynamo_construct = DynamoConstruct(
            self,
            construct_id="ReservationApiDynamo",
            stage=stage
        )

        self.s3_construct = S3Construct(
            self,
            # aqui deixei como bucket stack mesmo para não mexer nos ids lógicos e ter que recriar o bucket
            # para mais explicação cheque dentro da classe
            construct_id="BucketStack",
            stage=stage
        )
        
        self.ssm_construct = SsmConstruct(
            self,
            construct_id="ReservationApiSsm",
            stage=stage,
            # atenção para esse próximo parâmetro. de preferencia deixe tudo minusculo sem _
            # isso deve corresponder ao prefixo de caminho passado no CD dos outros mss (inclusive front)
            # que acessam os parametros no ssm.
            mss_name_identification_for_path="reservationapi",
            api=self.apigw_construct.rest_api,
            api_gateway_resource=self.apigw_construct.api_gateway_resource
        )

        ENVIRONMENT_VARIABLES = {
            "STAGE": stage,
            "DYNAMO_TABLE_NAME": self.dynamo_construct.table.table_name,
            "DYNAMO_PARTITION_KEY": "PK",
            "DYNAMO_SORT_KEY": "SK",
            "REGION": self.aws_region,
            "USER_API_URL": os.environ.get("USER_API_URL"),
            "S3_BUCKET_NAME": self.s3_construct.bucket.bucket_name,
            "FROM_EMAIL": os.environ.get("FROM_EMAIL"),
            "HIDDEN_COPY": os.environ.get("HIDDEN_COPY"),
            "S3_ASSETS_CDN": os.environ.get("S3_ASSETS_CDN")
        }

        self.lambda_construct = LambdaConstruct(
            self, 
            construct_id="ReservationApiLambda",
            stage=stage,
            api_gateway_resource=self.apigw_construct.api_gateway_resource,
            environment_variables=ENVIRONMENT_VARIABLES
        )

        for function in self.lambda_construct.functions_that_need_dynamo_permissions:
            self.dynamo_construct.table.grant_read_write_data(function)

        for function in self.lambda_construct.functions_that_need_s3_permissions:
            self.s3_construct.bucket.grant_read_write(function)

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
        
