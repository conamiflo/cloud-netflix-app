import base64
import json
import boto3
from botocore import client

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
movies_table = dynamodb.Table('movies-dbtable2')
s3_bucket = 'movie-bucket3'


def post_movie(event, context):
    
    try:
        body = json.loads(event['body'])
        title = body['title']
        genres = body['genres']
        actors = body['actors']
        directors = body['directors']
        description = body['description']
        movie = body['movie']
        
        movie_id = str(get_last_movie_id() + 1)
        
        encoded_movie = base64.b64decode(movie)
        s3.put_object(Bucket=s3_bucket, Key=movie_id, Body=encoded_movie, ContentType='video/mp4')
        
        metadata = s3.head_object(Bucket=s3_bucket, Key=movie_id)
        file_type = metadata['ContentType']
        movie_size = metadata['ContentLength']
        movie_modified = metadata['LastModified'].isoformat()
        

        movies_table.put_item(
            Item={
                'movie_id': movie_id,
                'title': title,
                'genres': genres,
                'actors': actors,
                'directors': directors,
                'description': description,
                'file_type': file_type,
                'movie_size': movie_size,
                'movie_modified': movie_modified,
            }
        )  

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'message': f"Successfully added movie with id: {movie_id}!"})
        }
    except Exception as e:
        return{
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'error': str(e)})
        }


def get_last_movie_id():
    paginator = s3.get_paginator("list_objects_v2")
    page_iterator = paginator.paginate(Bucket="movie-bucket3")

    last_movie_id = 0
    for page in page_iterator:
        if "Contents" in page:
            keys = [int(obj['Key']) for obj in page['Contents']]
            if keys:
                last_movie_id = max(keys)
    
    return last_movie_id