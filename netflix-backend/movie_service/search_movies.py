import base64
import json
import boto3
from botocore import client
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3', region_name='eu-central-1', config=client.Config(signature_version='s3v4'))

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def generate_search_key(title, description, actors, directors, genres):
    return f"{title}_{description}_{actors}_{directors}_{genres}"

def search_movies(event, context):
    movies_table = dynamodb.Table('movies-dbtable2')
    try:
        query_params = event.get('queryStringParameters', {})
        title = query_params.get('title', '')
        description = query_params.get('description', '')
        actors = query_params.get('actors', '')
        directors = query_params.get('directors', '')
        genres = query_params.get('genres', '')

        search_key = generate_search_key(title, description, actors, directors, genres).strip()

        if title and description and actors and directors and genres:
            response = movies_table.query(
                IndexName='SearchIndex',
                KeyConditionExpression=boto3.dynamodb.conditions.Key('search_data').eq(search_key)
            )
        else:
            filter_expression = []
            expression_attribute_values = {}
            if title:
                filter_expression.append("contains(title, :title)")
                expression_attribute_values[":title"] = title
            if description:
                filter_expression.append("contains(description, :description)")
                expression_attribute_values[":description"] = description
            if actors:
                filter_expression.append("contains(actors, :actors)")
                expression_attribute_values[":actors"] = actors
            if directors:
                filter_expression.append("contains(directors, :directors)")
                expression_attribute_values[":directors"] = directors
            if genres:
                filter_expression.append("contains(genres, :genres)")
                expression_attribute_values[":genres"] = genres

            filter_expression = " AND ".join(filter_expression)

            response = movies_table.scan(
                FilterExpression=filter_expression,
                ExpressionAttributeValues=expression_attribute_values
            )

        movies = response.get('Items', [])

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
