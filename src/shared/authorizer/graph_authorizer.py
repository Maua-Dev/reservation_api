import os
import re
import json
import urllib3

from src.shared.environments import Environments


def lambda_handler(event, context):
    """
    This function is used to authorize the user to access the API Gateway.
    It uses the Microsoft Graph API to fetch the user information and check if the user is from Maua.

    Args:
        event (dict): The event data passed to the Lambda function.
        context (object): The context object representing the current invocation.

    Returns:
        dict: The response object containing the policy document.
    """

    try:
        # Fetching the Microsoft Graph endpoint from the environment variables
        GRAPH_MICROSOFT_ENDPOINT = os.environ.get("GRAPH_MICROSOFT_ENDPOINT", None)
        if not GRAPH_MICROSOFT_ENDPOINT:
            raise Exception("MS_GRAPH_ENDPOINT environment variable not set")

        # Creating a HTTP client
        http = urllib3.PoolManager()

        # Extracting the token from the event data
        token = event["authorizationToken"].replace("Bearer ", "")

        print(f"token: {token}")
        print(f"graph_endpoint: {GRAPH_MICROSOFT_ENDPOINT}")

        # Fetching the user information from the Microsoft Graph API
        graph_endpoint = GRAPH_MICROSOFT_ENDPOINT
        methodArn = event["methodArn"]
        headers = {"Authorization": f"Bearer {token}"}
        response = http.request("GET", graph_endpoint, headers=headers)

        # Checking if the request was successful
        if response.status != 200:
            raise Exception("Failed to fetch user information")

        # Parsing the user data
        user_data = json.loads(response.data.decode("utf-8"))

        print("CHECK BEFORE REGEX")
        print(user_data)

        # Checking if the user is from Maua
        email_regex = r"(^\d{2}\.\d{5}-\d@maua\.br$)|(^[a-zA-Z]+\.[a-zA-Z]+@maua\.br$)"  # Regex to match the Maua email
        if not re.match(email_regex, user_data.get("mail", "")):
            return generate_policy("user", "Deny", methodArn)


        # TODO -> implementar o método de get user, pode ser pelo e-mail ou pelo user_id, usando o Repositorio

        print("USER_ID: ", user_data.get("id", "did not find id"))

        user_repo = Environments.get_user_repo()()
        user = user_repo.get_user(user_id=user_data.get("id"))

        print("CHECK PASSED REGEX AND GET USER")

        policy = generate_policy(
            user_data.get("id", "user"), "Allow", methodArn, {"user": json.dumps(user_data)}
        )

        print(policy)

        return policy

    # Handling exceptions
    except Exception as e:
        print(f"Error: {e}")
        methodArn = event["methodArn"]
        return generate_policy("user", "Deny", methodArn)


def generate_policy(principal_id, effect, method_arn, context=None):
    '''
    This function generates the policy document based on the principal ID, effect, method ARN, and context.

    Args:
        principal_id (str): The principal ID.
        effect (str): The effect (Allow or Deny).
        method_arn (str): The method ARN.
        context (dict): The context object.

    Returns:
        dict: The policy document.
    '''

    # Generating the policy document
    auth_response = {"principalId": principal_id}

    if effect:
        policy_document = {
            "Version": "2012-10-17",  # Version of the policy
            "Statement": [
                {
                    "Action": "execute-api:Invoke",  # Action to allow
                    "Effect": effect,  # Effect (Allow or Deny)
                    "Resource": method_arn,  # Resource path
                }
            ],
        }
        auth_response["policyDocument"] = policy_document

    if context:
        auth_response["context"] = context  # Adding the context to the response

    print("PASSED AUTH RESPONSE")

    return auth_response