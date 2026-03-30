from aws_cdk import (
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    RemovalPolicy,
)
from constructs import Construct
import os

class S3Construct(Construct):

    def __init__(
        self, 
        scope: Construct,
        construct_id: str,
        stage: str, 
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # deixei aqui como um legacy para o ID stackname para o bucket nao ser recriado. no futuro quando forem atualizar
        # esse stackname mesmo que seja no CD, o bucket terá de ser recriado apesar de ter o mesmo nome (creio eu)

        self.stack_name = os.environ.get("STACK_NAME")

        stage = stage.capitalize()

        self.bucket = s3.Bucket(
            self, f"RESERVATION_BACK_S3_BUCKET_{stage}",
            bucket_name=f"{self.stack_name}-bucket-{stage}".lower(),
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY if not (stage == 'Prod') else RemovalPolicy.RETAIN,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )
        
        self.distribution = cloudfront.Distribution(
            self, f"ReservationBucketDistribution{stage}",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(self.bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
            default_root_object=None  # não obrigatório, mas evita erro se não tiver index.html
        )
