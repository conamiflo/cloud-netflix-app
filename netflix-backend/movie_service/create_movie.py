import base64
import os
import json
import boto3
from botocore import client
import subprocess

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
movies_table = dynamodb.Table('movies-dbtable2')
s3_bucket = 'movie-bucket3'
sqs = boto3.client('sqs')
feed_update_queue_url = os.environ['FEED_UPDATE_QUEUE_URL']


def post_movie(event, context):
    # try:
    body = json.loads(event['body'])
    title = body['title']
    genres = body['genres']
    actors = body['actors']
    directors = body['directors']
    description = body['description']
    series = body.get('series', '')
    movie = body['movie']

    movie_id = str(get_last_movie_id() + 1)
    encoded_movie = base64.b64decode(movie)

    resolutions = {
        '360p': '360',
        '480p': '480',
        '720p': '720'
    }

    # for resolution, folder in resolutions.items():
    #     print(f'Starting transcoding for resolution: {resolution}')
    #
    #     output_key = f"{folder}/{movie_id}"
    #     print(f'Output key for {resolution}: {output_key}')
    #
    #     output_path = f"/tmp/{movie_id}_{resolution}.mp4"
    #     print(f'Output path for {resolution}: {output_path}')
    #
    #     ffmpeg_command = [
    #         '/opt/python/lib/python3.11/site-packages/ffmpeg', '-i', 'pipe:', '-vf', f'scale=-2:{resolution}',
    #         '-pix_fmt', 'yuv420p', output_path
    #     ]
    #     print(f'FFmpeg command for {resolution}: {" ".join(ffmpeg_command)}')
    #
    #     ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, stderr=subprocess.PIPE,
    #                                       stdout=subprocess.PIPE)
    #     stdout, stderr = ffmpeg_process.communicate(input=encoded_movie)
    #
    #     if ffmpeg_process.returncode != 0:
    #         error_message = f'FFmpeg error: {stderr.decode()}'
    #         print(error_message)
    #         raise RuntimeError(error_message)
    #
    #     with open(output_path, 'rb') as f:
    #         transcoded_movie = f.read()
    #
    #     print(f'Transcoding successful for resolution: {resolution}')
    #
    #     s3.put_object(Bucket=s3_bucket, Key=output_key, Body=transcoded_movie, ContentType='video/mp4')
    #     print(f'Uploaded transcoded movie for resolution: {resolution} to S3')
    #
    #     os.remove(output_path)
    #     print(f'Removed temporary file for resolution: {resolution}')

    metadata = s3.head_object(Bucket=s3_bucket, Key=f"720/{movie_id}")
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
            'series': series,
            'search_data': generate_search_key(title, description, actors, directors, genres)
        }
    )

    sqs.send_message(
        QueueUrl=feed_update_queue_url,
        MessageBody=json.dumps({'event': 'new_movie'})
    )

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps({'message': f"Successfully added movie with id: {movie_id}!"})
    }
    # except Exception as e:
    #     return {
    #         'statusCode': 500,
    #         'headers': {
    #             'Access-Control-Allow-Origin': '*',
    #         },
    #         'body': json.dumps({'error': str(e)})
    #     }


def get_last_movie_id():
    response = movies_table.scan(
        ProjectionExpression="movie_id"
    )

    last_movie_id = 0
    if 'Items' in response:
        movie_ids = [int(item['movie_id']) for item in response['Items'] if 'movie_id' in item]
        if movie_ids:
            last_movie_id = max(movie_ids)

    return last_movie_id


def generate_search_key(title, description, actors, directors, genres):
    return f"{title}_{description}_{actors}_{directors}_{genres}"
