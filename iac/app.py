import os

import aws_cdk as cdk
from adjust_layer_directory import adjust_layer_directory

from stack.iac_stack import IacStack



print("Starting the CDK")

print("Adjusting the layer directory")
adjust_layer_directory()
print("Finished adjusting the layer directory")


app = cdk.App()

aws_region = os.environ.get("AWS_REGION")
aws_account_id = os.environ.get("AWS_ACCOUNT_ID")
stack_name = os.environ.get("STACK_NAME")

# CD ja checa se esta dentro do branch name dev, hmlg, prod
# É ideal manter o CD como capitalize para seguir no mesmo esquema do stackname
stage = os.environ.get("GITHUB_REF_NAME").capitalize()

tags = {
    'project': 'Reservation Api MSS',
    'stage': stage,
    'stack': stack_name,
    'owner': 'DevCommunity'
}

IacStack(
    app, 
    stack_id=stack_name,
    stack_name=stack_name,
    stage=stage,
    env=cdk.Environment(
        account=aws_account_id, 
        region=aws_region
    ), 
    tags=tags
)


app.synth()
