import base64
import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
subscription_table = dynamodb.Table('subscription-table')


def subscribe(event, context):
    try:
        body = json.loads(event['body'])
        username = body['username']
        subscription_type = body['type']
        value = body['value']

        # Check for existing subscription
        if check_existing_subscription(username, subscription_type, value):
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({'message': f"Subscription already exists for user {username} with type {subscription_type} and value {value}!"})
            }

        subscription_id = str(get_last_subscription_id() + 1)

        subscription_table.put_item(
            Item={
                'subscription_id': subscription_id,
                'username': username,
                'type': subscription_type,
                'value': value
            }
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'message': f"Successfully added subscription with id: {subscription_id}!"})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'error': str(e)})
        }


def get_last_subscription_id():
    try:
        response = subscription_table.scan()
        items = response['Items']

        if not items:
            return 0

        latest_item = max(items, key=lambda x: int(x['subscription_id']))

        return int(latest_item['subscription_id'])
    except ClientError as e:
        print(e.response['Error']['Message'])
        return 0
    except Exception as e:
        print(str(e))
        return 0


def check_existing_subscription(username, subscription_type, value):
    try:
        response = subscription_table.scan(
            FilterExpression=Attr('username').eq(username) & Attr('type').eq(subscription_type) & Attr('value').eq(value)
        )

        if response['Items']:
            return True
        return False
    except ClientError as e:
        print(e.response['Error']['Message'])
        return False
    except Exception as e:
        print(str(e))
        return False
