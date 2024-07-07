import base64
import os
import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
subscription_table = dynamodb.Table('subscription-table')
sqs = boto3.client('sqs')
feed_update_queue_url = os.environ['FEED_UPDATE_QUEUE_URL']
sns = boto3.client('sns')
cognito = boto3.client('cognito-idp')
user_pool_id = os.environ['USER_POOL_ID']

def subscribe(event, context):
    try:
        body = json.loads(event['body'])
        username = body['username']
        subscription_type = body['type']
        value = body['value']

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
        
        topic_arn = create_or_find_sns_topic(subscription_type, value)

        if topic_arn:
            sns.subscribe(
                TopicArn=topic_arn,
                Protocol='email',
                Endpoint=get_user_email(username)
            )
        

        sqs.send_message(
            QueueUrl=feed_update_queue_url,
            MessageBody=json.dumps({
                'event': 'user_subscription',
                'username': username
            })
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


def create_or_find_sns_topic(subscription_type, value):
    try:
        topic_name = f"{subscription_type}-{value}"
        topic_arn = ""

        topics = sns.list_topics()['Topics']
        existing_topic = next((topic for topic in topics if topic_name in topic['TopicArn']), None)

        if existing_topic:
            topic_arn = existing_topic['TopicArn']
        else:
            response = sns.create_topic(Name=topic_name)
            topic_arn = response['TopicArn']

        return topic_arn
    except Exception as e:
        print(f"Error creating or finding SNS topic: {str(e)}")
        return None


def get_user_email(username):
    try:
        response = cognito.admin_get_user(
            UserPoolId=user_pool_id,
            Username=username
        )
        for attr in response['UserAttributes']:
            if attr['Name'] == 'email':
                return attr['Value']
        return None
    except cognito.exceptions.UserNotFoundException as e:
        print(f"User with username '{username}' not found.")
        return None
    except Exception as e:
        print(f"Error fetching user email: {str(e)}")
        return None

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
