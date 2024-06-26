import datetime
import math
import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')
feed_table = dynamodb.Table('feed-table')
movies_table = dynamodb.Table('movies-dbtable2')


def get_feed(event, context):
    try:
        username = event['queryStringParameters']['username']

        # Query the table for items with the specified username
        response = feed_table.get_item(
            Key={'username': username}
        )

        feed_item = response.get('Item')

        if not feed_item or 'feed' not in feed_item:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': f"No feed found for user {username}."})
            }

        feed_movie_ids = feed_item['feed']

        movies = []
        for movie_id in feed_movie_ids:
            response = movies_table.get_item(
                Key={'movie_id': movie_id}
            )
            movie_item = response.get('Item')
            if movie_item:
                movies.append(movie_item)

        return {
            'statusCode': 200,
            'body': json.dumps({'movies': movies})
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


