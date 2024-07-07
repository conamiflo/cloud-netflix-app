import json
import os
import boto3
from botocore.exceptions import ClientError


dynamodb = boto3.resource('dynamodb')
subscription_table = dynamodb.Table('subscription-table')
sqs = boto3.client('sqs')
feed_update_queue_url = os.environ['FEED_UPDATE_QUEUE_URL']

def unsubscribe(event, context):
    try:
        subscription_id = event['queryStringParameters']['subscription_id']
        username = event['queryStringParameters']['username']

        response = subscription_table.delete_item(
            Key={
                'subscription_id': subscription_id,
                'username': username
            },
            ConditionExpression="attribute_exists(subscription_id)"
        )

        sqs.send_message(
            QueueUrl=feed_update_queue_url,
            MessageBody=json.dumps({
                'event': 'user_unsubscribe',
                'username': username
            })
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'message': f"Successfully deleted subscription with id: {subscription_id} for user: {username}!"})
        }
    except KeyError as e:

        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'error': 'Missing subscription_id or username parameter in query string'})
        }
    except ClientError as e:

        error_code = e.response['Error']['Code']
        if error_code == 'ConditionalCheckFailedException':
            return {
                'statusCode': 404,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({'error': f"Subscription with id {subscription_id} for user {username} not found!"})
            }
        else:
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({'error': str(e)})
            }
    except Exception as e:
        
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'error': str(e)})
        }
