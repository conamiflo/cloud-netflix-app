import boto3
from botocore.exceptions import ClientError

client = boto3.client('cognito-idp')

def handler(event, context):
    user_pool_id = event['userPoolId']
    user_attributes = event['request']['userAttributes']
    email = user_attributes['email']

    try:
        response = client.list_users(
            UserPoolId=user_pool_id,
            Filter=f'email = "{email}"'
        )
        users = response['Users']

        if users and len(users) > 0:
            raise Exception("Email already in use")
    except ClientError as e:
        print(f"Error listing users: {e}")

    return event
