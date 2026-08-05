import os
import json
import urllib3

from src.shared.environments import Environments


def _get_authorization_header(headers):
    '''
    Extracts the Authorization header from a REQUEST authorizer event, case-insensitively.

    Args:
        headers (dict): The headers received in the event.

    Returns:
        str | None: The raw header value, or None when it is not present.
    '''

    if not headers:
        return None

    for key, value in headers.items():
        if key.lower() == "authorization":
            return value

    return None


def _fetch_user_data(token):
    '''
    Fetches the user information from the user mss using the given token.

    Args:
        token (str): The bearer token, already stripped of the "Bearer " prefix.

    Returns:
        dict: The user data returned by the user mss.

    Raises:
        Exception: When USER_API_URL is not set or the user mss does not answer with 200.
    '''

    # Fetch the User Mss enpoint from the environment variables
    MSS_USER_API_ENDPOINT = os.environ.get("USER_API_URL")
    if not MSS_USER_API_ENDPOINT:
        raise Exception("MSS_USER_ENDPOINT environment variable not set")

    # Creating a HTTP client
    http = urllib3.PoolManager()

    # Fetching the user information from the user mss
    headers = {"Authorization": f"Bearer {token}"}
    response = http.request("GET", MSS_USER_API_ENDPOINT + "get-user", headers=headers)

    # Checking if the request was successful
    if response.status != 200:
        raise Exception("Failed to fetch user information")

    # Parsing the user data
    return json.loads(response.data.decode("utf-8"))


def lambda_handler(event, context):
    """
    TOKEN authorizer. Requires a valid Bearer token — used by every protected route.

    Args:
        event (dict): The event data passed to the Lambda function.
        context (object): The context object representing the current invocation.

    Returns:
        dict: The response object containing the policy document.
    """

    method_arn = event["methodArn"]

    try:
        token = event["authorizationToken"].replace("Bearer ", "")
        user_data = _fetch_user_data(token)

        return generate_policy(
            user_data.get("id", "user"), "Allow", method_arn, {"user": json.dumps(user_data)}
        )

    # Handling exceptions
    except Exception as e:
        print(f"Error: {e}")
        return generate_policy("user", "Deny", method_arn)


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