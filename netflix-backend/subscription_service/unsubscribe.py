import json
import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB resource and table
dynamodb = boto3.resource('dynamodb')
subscription_table = dynamodb.Table('subscription-table')

def unsubscribe(event, context):
    try:
        # Retrieve subscription_id and username from query string parameters
        subscription_id = event['queryStringParameters']['subscription_id']
        username = event['queryStringParameters']['username']  # Assuming username is also passed

        # Delete item from DynamoDB table
        response = subscription_table.delete_item(
            Key={
                'subscription_id': subscription_id,
                'username': username
            },
            ConditionExpression="attribute_exists(subscription_id)"
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': f"Successfully deleted subscription with id: {subscription_id} for user: {username}!"})
        }
    except KeyError as e:
        # Handle missing subscription_id or username parameter in query string
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing subscription_id or username parameter in query string'})
        }
    except ClientError as e:
        # Handle specific DynamoDB errors
        error_code = e.response['Error']['Code']
        if error_code == 'ConditionalCheckFailedException':
            return {
                'statusCode': 404,
                'body': json.dumps({'error': f"Subscription with id {subscription_id} for user {username} not found!"})
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }
    except Exception as e:
        # Handle any other unexpected errors
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
