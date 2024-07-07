import datetime
import math
import json
import boto3
from decimal import Decimal, ROUND_DOWN
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr
import os

client = boto3.client('cognito-idp')

dynamodb = boto3.resource('dynamodb')
feed_table = dynamodb.Table('feed-table')
review_table = dynamodb.Table('review-table2')
subscription_table = dynamodb.Table('subscription-table')
movies_table = dynamodb.Table('movies-dbtable2')
download_history_table = dynamodb.Table('download-history-table')
user_pool_id = os.environ['USER_POOL_ID']

def exponential_approach(date):
    current_datetime = datetime.datetime.now()
    delta = (current_datetime - date).total_seconds()
    decay_rate = Decimal('0.0000004')

    if delta <= 0:
        return Decimal('1.0')

    result = Decimal(math.exp(-float(decay_rate * Decimal(delta))))
    result = result.quantize(Decimal('0.001'), rounding=ROUND_DOWN)
    return result


def lambda_handler(event, context):
    try:
        for record in event['Records']:
            message = json.loads(record['body'])
            event_type = message['event']
            username = message.get('username', '')

            if event_type == 'new_movie' or event_type == 'update_movie':
                update_all_users_feed()
            elif event_type in ['user_subscription', 'user_review', 'user_download_movie']:
                update_users_feed(username)

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps('Feed updated successfully.')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'error': str(e)})
        }


def update_all_users_feed():
    try:
        response = client.list_users(
            UserPoolId=user_pool_id,
        )
        for user in response['Users']:
            username = user['Username']
            top_movie_ids = get_top_movies(username)
            existing_feed = feed_table.get_item(Key={'username': username})

            if 'Item' in existing_feed:
                feed_table.update_item(
                    Key={'username': username},
                    UpdateExpression='SET #f = :feed',
                    ExpressionAttributeNames={'#f': 'feed'},
                    ExpressionAttributeValues={':feed': top_movie_ids}
                )
            else:
                feed_table.put_item(
                    Item={
                        'username': username,
                        'feed': top_movie_ids
                    }
                )
    except ClientError as e:
        print(f"ClientError: {e}")
    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"Exception: {e}")


def update_users_feed(username):
    try:
        top_movie_ids = get_top_movies(username)

        existing_feed = feed_table.get_item(Key={'username': username})

        if 'Item' in existing_feed:
            feed_table.update_item(
                Key={'username': username},
                UpdateExpression='SET #f = :feed',
                ExpressionAttributeNames={'#f': 'feed'},
                ExpressionAttributeValues={':feed': top_movie_ids}
            )
        else:
            feed_table.put_item(
                Item={
                    'username': username,
                    'feed': top_movie_ids
                }
            )

    except ClientError as e:
        print(f"ClientError: {e}")
    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"Exception: {e}")

def get_top_movies(username):
    genres_dict = {}
    actors_dict = {}
    directors_dict = {}

    reviews = review_table.scan(
        FilterExpression=Attr('username').eq(username)
    )

    if 'Items' in reviews:
        for item in reviews['Items']:
            if 'movie_id' in item:
                movie_id = item['movie_id']

                value = item.get('value', 1)
                value -= 2
                value = value / 2

                response = movies_table.query(
                    KeyConditionExpression=boto3.dynamodb.conditions.Key('movie_id').eq(movie_id)
                )

                movie_items = response.get('Items', [])
                for movie_item in movie_items:
                    genres = movie_item.get('genres', [])
                    actors = movie_item.get('actors', [])
                    directors = movie_item.get('directors', [])

                    for genre in genres:
                        if genre not in genres_dict:
                            genres_dict[genre] = 0
                        genres_dict[genre] += value

                    for actor in actors:
                        if actor not in actors_dict:
                            actors_dict[actor] = 0
                        actors_dict[actor] += value

                    for director in directors:
                        if director not in directors_dict:
                            directors_dict[director] = 0
                        directors_dict[director] += value

    subscriptions = subscription_table.scan(
        FilterExpression=Attr('username').eq(username)
    )

    if 'Items' in subscriptions:
        for item in subscriptions['Items']:
            if 'type' in item and 'value' in item:
                type = item['type']
                value = item['value']

                if type == 'actor':
                    if value not in actors_dict:
                        actors_dict[value] = 0
                    actors_dict[value] += 1

                elif type == 'genre':
                    if value not in genres_dict:
                        genres_dict[value] = 0
                    genres_dict[value] += 1

                elif type == 'director':
                    if value not in directors_dict:
                        directors_dict[value] = 0
                    directors_dict[value] += 1

    downloads = download_history_table.scan(
        FilterExpression=Attr('username').eq(username)
    )

    if 'Items' in downloads:
        for item in downloads['Items']:
            if 'movie_id' in item and 'timestamp' in item:
                movie_id = item['movie_id']
                timestamp = item['timestamp']

                download_datetime = datetime.datetime.fromisoformat(timestamp)
                value = exponential_approach(download_datetime)
                print(value)
                response = movies_table.query(
                    KeyConditionExpression=boto3.dynamodb.conditions.Key('movie_id').eq(movie_id)
                )
                movie_items = response.get('Items', [])
                for movie_item in movie_items:
                    genres = movie_item.get('genres', [])
                    actors = movie_item.get('actors', [])
                    directors = movie_item.get('directors', [])

                    for genre in genres:
                        if genre not in genres_dict:
                            genres_dict[genre] = 0
                        genres_dict[genre] += value

                    for actor in actors:
                        if actor not in actors_dict:
                            actors_dict[actor] = 0
                        actors_dict[actor] += value

                    for director in directors:
                        if director not in directors_dict:
                            directors_dict[director] = 0
                        directors_dict[director] += value

    movie_weights = {}

    response = movies_table.scan()
    movies = response['Items']

    for movie in movies:
        movie_id = movie['movie_id']
        genres = movie.get('genres', [])
        actors = movie.get('actors', [])
        directors = movie.get('directors', [])

        weight = 0

        for genre in genres:
            if genre in genres_dict:
                weight += genres_dict[genre]

        for actor in actors:
            if actor in actors_dict:
                weight += actors_dict[actor]

        for director in directors:
            if director in directors_dict:
                weight += directors_dict[director]

        movie_weights[movie_id] = weight
    print(genres_dict)
    print(directors_dict)
    print(actors_dict)
    print(movie_weights)
    sorted_movies = sorted(movie_weights.items(), key=lambda x: x[1], reverse=True)
    top_movie_ids = [movie_id for movie_id, weight in sorted_movies[:9]]
    return top_movie_ids
