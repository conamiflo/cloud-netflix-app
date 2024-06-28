import datetime
import math
import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')
feed_table = dynamodb.Table('feed-table')
review_table = dynamodb.Table('review-table2')
subscription_table = dynamodb.Table('subscription-table')
movies_table = dynamodb.Table('movies-dbtable2')
download_history_table = dynamodb.Table('download-history-table')

def exponential_approach(date):
    current_datetime = datetime.datetime.now()
    delta = (date - current_datetime).total_seconds()
    decay_rate = 0.0000004
    #sa ovim decay rateom nakon mesec dana filmovi vec krecu da imaju dosta manju relevantnost: 0.3545875486 npr a nakon nedelju su i dalje relevantni dosta 0.7851189846
    # a nakon 2 meseca 0.1257323296

    if delta <= 0:
        return 1.0

    return math.exp(-decay_rate * delta)

def update_users_feed(event, context):
    try:
        body = json.loads(event['body'])
        username = body.get('username')

        if not username:
            raise ValueError("Username is required")

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
                        #genres = movie_item.get('genres', [])
                        #ovo vratiti kada se popravi tabela usera

                        genres = movie_item.get('genres', "")
                        actors = movie_item.get('actors', [])
                        directors = movie_item.get('directors', [])
                        # for genre in genres:
                        #     if genre not in genres_dict:
                        #         genres_dict[genre] = 0
                        #     genres_dict[genre] += value
                        # ovo vratiti kada se popravi tabela usera

                        if genres not in genres_dict:
                            genres_dict[genres] = 0
                        genres_dict[genres] += value

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
                if 'movie_id' in item and 'download_date' in item:
                    movie_id = item['movie_id']
                    download_date = item['download_date']

                    download_datetime = datetime.datetime.fromisoformat(download_date)
                    value = exponential_approach(download_datetime)

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

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Feed updated successfully', 'feed': top_movie_ids})
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }