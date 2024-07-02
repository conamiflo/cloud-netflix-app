import boto3

def handler(event, context):
    client = boto3.client('cognito-idp')

    params = {
        'GroupName': 'Users',  # The name of the group in your Cognito user pool that you want to add the user to
        'UserPoolId': event['userPoolId'],
        'Username': event['userName']
    }

    # Some minimal checks to make sure the user was properly confirmed
    if not (event['request']['userAttributes']['cognito:user_status'] == "CONFIRMED" and event['request']['userAttributes']['email_verified'] == "true"):
        return {
            'statusCode': 400,
            'body': 'User was not properly confirmed and/or email not verified'
        }

    try:
        response = client.admin_add_user_to_group(**params)
        return event  # Return the event object as required by Cognito
    except Exception as e:
        print(f"Error adding user to group: {str(e)}")
        raise e
