

def lambda_handler(event, context):
    """
    Lambda handler function for the make_calendar module
    """
    print("IM ALIVE!! LAMBDA TRIGGERED BY EVENTBRIDGE")
    print('event: ', event)
    print('context', context)