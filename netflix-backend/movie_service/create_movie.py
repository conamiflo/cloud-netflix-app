import base64
import json
import boto3

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

def post_movie(event, context):
    
    movies_table = dynamodb.Table('movie-table')
    s3_bucket = 'movie-bucket'

    try:
        body = json.loads(event['body'])
        movie_id = int(body['movie_id'])
        title = body['title']
        genres = body['genres']
        actors = body['actors']
        directors = body['directors']
        movie = body['movie']

        movies_table.put_item(
            Item={
                'movie_id': movie_id,
                'title': title,
                'genres': genres,
                'actors': actors,
                'directors': directors,
            }
        )

        encoded_movie = base64.b64decode(movie)
        s3.put_object(Bucket=s3_bucket, Key=str(movie_id), Body=encoded_movie, ContentType='video/mp4')

        return {
            'statusCode': 200,
            'body': json.dumps({'message': "Successfully added movie!"})
        }

    except Exception as e:
        return{
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    

def post_movie_mp4(event, context):
    s3_bucket = 'movie-bucket'

    try:
        body = json.loads(event['body'])
        movie_id = int(body['movie_id'])
        movie = body['movie']

        encoded_movie = base64.b64decode(movie)
        s3.put_object(Bucket=s3_bucket, Key=str(movie_id), Body=encoded_movie, ContentType='video/mp4')

        return {
            'statusCode': 200,
            'body': json.dumps({'message': "Successfully added movie MP4!"})
        }

    except Exception as e:
        return{
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }