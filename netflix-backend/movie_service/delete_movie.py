import json
import os
import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

movie_table = dynamodb.Table('movies-dbtable2')
review_table = dynamodb.Table('review-table2')
download_history_table = dynamodb.Table('download-history-table')
s3_bucket = 'movie-bucket3'

def delete_movie(event, context):
    query_params = event.get('queryStringParameters', {})
    movie_id = query_params.get('movie_id')
    movie_title = query_params.get('title')
    try:
        movie_table.delete_item(
            Key={
                'movie_id': movie_id,
                'title': movie_title
            },
            ConditionExpression="attribute_exists(movie_id)"
        )
        
        s3.delete_object(Bucket=s3_bucket, Key=movie_id)

        reviews_to_delete = review_table.scan(
            FilterExpression=Attr('movie_id').eq(movie_id)
        )
        with review_table.batch_writer() as batch:
            for each in reviews_to_delete['Items']:
                batch.delete_item(
                    Key={
                        'review_id': each['review_id'],
                        'username': each['username']
                    }
                )

        downloads_to_delete = download_history_table.scan(
            FilterExpression=Attr('movie_id').eq(movie_id)
        )
        with download_history_table.batch_writer() as batch:
            for each in downloads_to_delete['Items']:
                batch.delete_item(
                    Key={
                        'download_id': each['download_id'],
                        'username': each['username']
                    }
                )
        
        return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps({'message': f'Successfully deleted movie {movie_id} and its related reviews, download history, and S3 file'})
    }
    except Exception as e:
        return {
            'statusCode': 404,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': f'Movie with ID {movie_id} and title {movie_title} not found.'
        }
        