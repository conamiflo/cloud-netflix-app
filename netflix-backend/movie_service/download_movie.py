import base64
import json
import boto3
from botocore import client

dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3', region_name='eu-central-1', config=client.Config(signature_version='s3v4'))

def download_movie(event, context):
    movies_table = dynamodb.Table('movies-dbtable')
    s3_bucket = 'movie-bucket3'

    try:

        movie_id = event['queryStringParameters']['movie_id']
        response = movies_table.get_item(Key={'movie_id': movie_id})

        if 'Item' in response:

            url = s3_client.generate_presigned_url('get_object', Params={'Bucket': s3_bucket, 'Key': movie_id}, ExpiresIn=3600)

            item = response['Item']
            item['download_url'] = url

            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps(item)
            }

        else:
            return {
                'statusCode': 404,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({'message': 'Movie not found'})
            }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'error': str(e)})
        }

