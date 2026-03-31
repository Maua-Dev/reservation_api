from aws_cdk import (
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    RemovalPolicy,
    Aws
)
from constructs import Construct

class S3Construct(Construct):

    def __init__(
        self, 
        scope: Construct,
        construct_id: str,
        stage: str,
        stack_name: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        stage = stage.capitalize()

        self.bucket_spreadsheets = s3.Bucket(
            self, 
            id=f"ReservationApi_Bucket_Back_{stage}",
            bucket_name=f"reservationapi-spreadsheets-{stage.lower()}-{Aws.ACCOUNT_ID}-{Aws.REGION}",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY if not (stage == 'Prod') else RemovalPolicy.RETAIN,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )
        
        self.distribution = cloudfront.Distribution(
            self, f"ReservationApiSpreadsheetsBucketDistribution{stage}",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(self.bucket_spreadsheets),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
            default_root_object=None  # não obrigatório, mas evita erro se não tiver index.html
        )
