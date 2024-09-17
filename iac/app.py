import os

import aws_cdk as cdk
from adjust_layer_directory import adjust_layer_directory
import get_stage

from stacks.iac_stack import IacStack



print("Starting the CDK")

print("Adjusting the layer directory")
adjust_layer_directory(shared_dir_name="shared", destination="copied_shared")
print("Finished adjusting the layer directory")


app = cdk.App()

aws_region = os.environ.get("AWS_REGION")
aws_account_id = os.environ.get("AWS_ACCOUNT_ID")
stack_name = os.environ.get("STACK_NAME")

stage = get_stage.get_stage_env()

tags = {
    'project': 'Reservation Courts and Schedule MSS',
    'stage': stage,
    'stack': 'BACK',
    'owner': 'DevCommunity'
}

IacStack(app, construct_id=f"{stack_name}_IacStack_{stage}", stack_name=stack_name, env=cdk.Environment(account=aws_account_id, region=aws_region), tags=tags)


app.synth()
