import base64
import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
review_table = dynamodb.Table('review-table')


def review(event, context):
    try:
        body = json.loads(event['body'])
        username = body['username']
        movie_id = body['movie_id']
        review_type = body['type']
        description = body['description']
        value = body['value']

        # Check for existing subscription
        if check_existing_reviews(username, review_type, movie_id):
            return {
                'statusCode': 400,
                'body': json.dumps({'message': f"Review already exists from user {username} for movie with id {movie_id} with type {review_type}"})
            }

        review_id = str(get_last_review_id() + 1)

        review_table.put_item(
            Item={
                'review_id': review_id,
                'username': username,
                'movie_id': movie_id,
                'type': review_type,
                'description': description,
                'value': value
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': f"Successfully added review with id: {review_id}!"})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


def get_last_review_id():
    try:
        response = review_table.scan()
        items = response['Items']

        if not items:
            return 0

        latest_item = max(items, key=lambda x: int(x['review_id']))

        return int(latest_item['review_id'])
    except ClientError as e:
        print(e.response['Error']['Message'])
        return 0
    except Exception as e:
        print(str(e))
        return 0


def check_existing_reviews(username, review_type, movie_id):
    try:
        response = review_table.scan(
            FilterExpression=Attr('username').eq(username) & Attr('type').eq(review_type) & Attr('movie_id').eq(movie_id)
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
