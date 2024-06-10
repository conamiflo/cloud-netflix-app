import base64
import json
import boto3

dynamodb = boto3.resource('dynamodb')
# s3 = boto3.client('s3')
s3 = boto3.client('s3', region_name='eu-central-1')

def download_movie(event, context):
    movies_table = dynamodb.Table('movie-table2')
    s3_bucket = 'movie-bucket'


    id = event['pathParameters']['id']
    
    response = movies_table.get_item(
        Key={
            'movie_id': int(id)
        }
    )