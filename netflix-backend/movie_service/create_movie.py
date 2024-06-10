import base64
import json
import boto3
from botocore import client

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
movies_table = dynamodb.Table('movie-table2')
s3_bucket = 'movie-bucket'


def post_movie(event, context):
    
    try:
        body = json.loads(event['body'])
        movie_id = int(body['movie_id'])
        title = body['title']
        genres = body['genres']
        actors = body['actors']
        directors = body['directors']
        movie = body['movie']

        movies_table.put_item(
            Item={
                'movie_id': movie_id,
                'title': title,
                'genres': genres,
                'actors': actors,
                'directors': directors,
            }
        )  

        # try:

        #     presigned_url = s3.generate_presigned_url(
        #             'put_object',
        #             Params={'Bucket': 'movie-bucket', 'Key': f"{movie_id}"},
        #             ExpiresIn=3600
        #         )
            
        #     return {
        #         'statusCode': 200,
        #         'headers': {
        #             'Access-Control-Allow-Origin': '*',
        #         },
        #         'body': json.dumps({
        #             'message': 'Successfully added a movie!',
        #             'upload_url': presigned_url
        #         })
        #     }
        # except Exception as e:
        #     return {
        #         'statusCode': 404,
        #         'body': json.dumps({'message': str(e)})
        #     }

        encoded_movie = base64.b64decode(movie)
        s3.put_object(Bucket=s3_bucket, Key=str(movie_id), Body=encoded_movie, ContentType='video/mp4')

        return {
            'statusCode': 200,
            'body': json.dumps({'message': "Successfully added movie!"})
        }
    except Exception as e:
        return{
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    
