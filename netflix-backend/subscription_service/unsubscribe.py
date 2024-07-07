import json
import os
import boto3
from botocore.exceptions import ClientError


dynamodb = boto3.resource('dynamodb')
subscription_table = dynamodb.Table('subscription-table')
sqs = boto3.client('sqs')
feed_update_queue_url = os.environ['FEED_UPDATE_QUEUE_URL']
sns = boto3.client('sns')
cognito = boto3.client('cognito-idp')
user_pool_id = os.environ['USER_POOL_ID']

def unsubscribe(event, context):
    try:
        subscription_id = event['queryStringParameters']['subscription_id']
        username = event['queryStringParameters']['username']
        
        response1 = subscription_table.get_item(Key={'subscription_id': subscription_id, 'username': username})
        item = response1['Item']
        
        subscription_type = item['type']
        value = item['value']

        response = subscription_table.delete_item(
            Key={
                'subscription_id': subscription_id,
                'username': username
            },
            ConditionExpression="attribute_exists(subscription_id)"
        )
        
        topic_arn = create_or_find_sns_topic(subscription_type, value)
        unsubscribe_from_sns(topic_arn,get_user_email(username))

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
    
def unsubscribe_from_sns(topic_arn, email):
    subscriptions = sns.list_subscriptions_by_topic(TopicArn=topic_arn)['Subscriptions']
    for subscription in subscriptions:
        if subscription['Endpoint'] == email and subscription['Protocol'] == 'email':
            sns.unsubscribe(SubscriptionArn=subscription['SubscriptionArn'])
            break


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