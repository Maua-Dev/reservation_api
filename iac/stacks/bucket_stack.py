from aws_cdk import (
    aws_s3 as s3,
    aws_iam as iam,
    RemovalPolicy,
    Stack,
)
from constructs import Construct
import os
import random

class BucketStack(Construct):

    def __init__(self, scope: Construct, **kwargs) -> None:
        super().__init__(scope,  "BucketStack", **kwargs)

        self.github_ref = os.environ.get('GITHUB_REF_NAME')
        self.stack_name = os.environ.get("STACK_NAME")

        stage = ''
        if 'prod' in self.github_ref:
            stage = 'PROD'
        elif 'homolog' in self.github_ref:
            stage = 'HOMOLOG'
        else:
            stage = 'DEV'

        self.bucket = s3.Bucket(
            self, f"BACK_S3_REPORT_BUCKET_{stage}",
            # TODO remover isso quando voltar pra conta nova ou tentar deletar o bucket criado la com power user
            bucket_name=f"{self.stack_name}-report-bucket{stage}-{random.randint(1000,9999)}".lower(),
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY if not (stage == 'PROD') else RemovalPolicy.RETAIN,
        )
