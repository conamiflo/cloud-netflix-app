import json
import boto3

s3 = boto3.client('s3')
bucket_name = 'movie-bucket3'

def handler(event, context):
    movie_id = event['movie_id']
    target_resolution = event['target_resolution']

    print(f'{movie_id}, {target_resolution}')

    return {
        'statusCode': 200,
        'body': json.dumps('Transcoding process initiated successfully')
    }