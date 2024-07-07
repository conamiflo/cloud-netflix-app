import json
import boto3
from botocore import client
from decimal import Decimal
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3', region_name='eu-central-1', config=client.Config(signature_version='s3v4'))

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def get_series(event, context):
    movies_table = dynamodb.Table('movies-dbtable2')

    try:
        query_params = event.get('queryStringParameters', {})
        series_value = query_params.get('series')
        exclude_movie_id = query_params.get('exclude_movie_id')


        response = movies_table.scan(
            FilterExpression=Attr('series').eq(series_value) & Attr('movie_id').ne(exclude_movie_id)
        )

        movies = response.get('Items')
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps(movies, cls=DecimalEncoder)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'error': str(e)})
        }
