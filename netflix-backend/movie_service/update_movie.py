import base64
import os
import json
import boto3
from botocore import client
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
movies_table = dynamodb.Table('movies-dbtable2')
s3_bucket = 'movie-bucket3'
sqs = boto3.client('sqs')
feed_update_queue_url = os.environ['FEED_UPDATE_QUEUE_URL']

def update_movie(event, context):
    
    # try:
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

            
        if 'movie' in body and body['movie'] is not None:
            movie = body['movie']
            encoded_movie = base64.b64decode(movie)
            s3.put_object(Bucket=s3_bucket, Key=movie_id, Body=encoded_movie, ContentType='video/mp4')

            metadata = s3.head_object(Bucket=s3_bucket, Key=movie_id)
            body['file_type'] = metadata['ContentType']
            body['movie_size'] = metadata['ContentLength']
            body['movie_modified'] = metadata['LastModified'].isoformat()
            del body['movie']

        for key in item:
            if key not in body and key != 'movie' and key != 'movieFile':
                body[key] = item[key]
                
                
        movies_table.delete_item(Key={'movie_id': movie_id, 'title': old_title})

        body['title'] = new_title
        body['search_data'] = generate_search_key(body['title'],body['description'],body['actors'],body['directors'],body['genres'])
        movies_table.put_item(Item=body)

        sqs.send_message(
            QueueUrl=feed_update_queue_url,
            MessageBody=json.dumps({
                'event': 'update_movie'
            })
        )

        return {
            'statusCode': 200,
            'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
            'body': json.dumps({'message': "Successfully updated movie!"})
        }
    # except Exception as e:
    #     return {
    #         'statusCode': 500,
    #         'headers': {
    #             'Access-Control-Allow-Origin': '*',
    #         },
    #         'body': json.dumps({'error': str(e)})
    #     }


def generate_search_key(title, description, actors, directors, genres):
    return f"{title}_{description}_{actors}_{directors}_{genres}"