import base64
import os
import datetime
import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
download_history_table = dynamodb.Table('download-history-table')
sqs = boto3.client('sqs')
feed_update_queue_url = os.environ['FEED_UPDATE_QUEUE_URL']
def create_download_history(event, context):
    try:
        body = json.loads(event['body'])
        username = body['username']
        movie_id = body['movie_id']
        timestamp = datetime.datetime.now().isoformat()
        download_id = str(get_last_download_id() + 1)

        download_history_table.put_item(
            Item={
                'download_id': download_id,
                'username': username,
                'movie_id': movie_id,
                'timestamp': timestamp
            }
        )

        sqs.send_message(
            QueueUrl=feed_update_queue_url,
            MessageBody=json.dumps({
                'event': 'user_download_movie',
                'username': username
            })
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'message': f"Successfully added download history with id: {download_id}!"})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'error': str(e)})
        }


def get_last_download_id():
    try:
        response = download_history_table.scan()
        items = response['Items']

        if not items:
            return 0

        latest_item = max(items, key=lambda x: int(x['download_id']))

        return int(latest_item['download_id'])
    except ClientError as e:
        print(e.response['Error']['Message'])
        return 0
    except Exception as e:
        print(str(e))
        return 0
