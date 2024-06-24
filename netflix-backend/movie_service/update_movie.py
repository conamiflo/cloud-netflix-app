import base64
import json
import boto3
from botocore import client
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
movies_table = dynamodb.Table('movies-dbtable2')
s3_bucket = 'movie-bucket3'

def update_movie(event, context):
    
    try:
        body = json.loads(event['body'])
        movie_id = body['movie_id']
        new_title = body['title']
        
        # old_title = body.get('old_title')
        # new_title = body['title']
        # response = movies_table.get_item(Key={'movie_id': movie_id, 'title': old_title})

        response = movies_table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('movie_id').eq(movie_id)
        )
    
        if response['Items']:
            item = response['Items'][0]
            old_title = item['title']
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Movie not found'})
            }

        if 'movie' in body:
            movie = body['movie']
            encoded_movie = base64.b64decode(movie)
            s3.put_object(Bucket=s3_bucket, Key=movie_id, Body=encoded_movie, ContentType='video/mp4')

            metadata = s3.head_object(Bucket=s3_bucket, Key=movie_id)
            body['file_type'] = metadata['ContentType']
            body['movie_size'] = metadata['ContentLength']
            body['movie_modified'] = metadata['LastModified'].isoformat()
            del body['movie']

        for key in item:
            if key not in body:
                body[key] = item[key]

        movies_table.delete_item(Key={'movie_id': movie_id, 'title': old_title})

        body['title'] = new_title
        movies_table.put_item(Item=body)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': "Successfully updated movie!"})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
