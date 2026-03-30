from aws_cdk import (
    aws_dynamodb as dynamodb, RemovalPolicy,
)
from constructs import Construct

class DynamoConstruct(Construct):
    table: dynamodb.Table

    def __init__(
        self, 
        scope: Construct,
        construct_id: str,
        stage: str, 
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stage = stage.capitalize()
        
        # deixei aqui como um stackname explicito (ReservationApi) pq o vindo do CD é todo mal formatado e muitas vezes quem vem
        # programar infra aqui pela primeira vez mal sabe de onde essa variável vem
        
        # SE for trocar de volta pra um stackname vindo do CD aqui, provavelmente a tabela vai ser recriada (atenção à prod)

        self.table = dynamodb.Table(
            self, 
            id=f"ReservationApi_DynamoTable_{stage}",
            table_name=f"ReservationApi_DynamoTable_{stage}",
            partition_key=dynamodb.Attribute(
                name="PK",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="SK",
                type=dynamodb.AttributeType.STRING
            ), 
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.RETAIN if stage == "Prod" else RemovalPolicy.DESTROY
        )
        
    


