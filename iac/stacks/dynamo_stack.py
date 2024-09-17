from aws_cdk import (
    aws_dynamodb as dynamodb, RemovalPolicy,
)
from constructs import Construct
import os

class DynamoStack(Construct):
    table: dynamodb.Table

    def __init__(self, scope: Construct, **kwargs) -> None:
        super().__init__(scope, **kwargs)

        self.github_ref = os.environ.get('GITHUB_REF_NAME')
        self.stack_name = os.environ.get("STACK_NAME")

        stage = ''
        if 'prod' in self.github_ref:
            stage = 'PROD'
        elif 'homolog' in self.github_ref:
            stage = 'HOMOLOG'
        else:
            stage = 'DEV'

        self.table = dynamodb.Table(
            self, f"{self.stack_name}_DynamoTable_{stage}",
            partition_key=dynamodb.Attribute(
                name="PK",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="SK",
                type=dynamodb.AttributeType.STRING
            ), 
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )
        
    


