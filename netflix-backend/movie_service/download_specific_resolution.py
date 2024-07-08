import base64
import json
import boto3
from botocore import client
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3', region_name='eu-central-1', config=client.Config(signature_version='s3v4'))

def download_specific_resolution(event, context):
    movies_table = dynamodb.Table('movies-dbtable2')
    s3_bucket = 'movie-bucket3'

    try:
        query_params = event.get('queryStringParameters', {})
        movie_id = query_params.get('movie_id')
        resolution = query_params.get('resolution')
        
        
        s3_key = f'{resolution}/{movie_id}'

        presigned_url = s3_client.generate_presigned_url('get_object', 
                                                         Params={'Bucket': s3_bucket, 'Key': s3_key,'ResponseContentDisposition': 'attachment'},
                                                         ExpiresIn=3600)
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps(presigned_url)
        }
       
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'error': str(e)})
        }
