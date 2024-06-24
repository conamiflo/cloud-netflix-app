import base64
import json
import boto3
from botocore import client

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
movies_table = dynamodb.Table('movies-dbtable2')
s3_bucket = 'movie-bucket3'


def post_movie(event, context):
    
    try:
        body = json.loads(event['body'])
        movie_id = body['movie_id']
        title = body['title']
        genres = body['genres']
        actors = body['actors']
        directors = body['directors']
        description = body['description']
        movie = body['movie']
        
        encoded_movie = base64.b64decode(movie)
        s3.put_object(Bucket=s3_bucket, Key=movie_id, Body=encoded_movie, ContentType='video/mp4')
        
        metadata = s3.head_object(Bucket=s3_bucket, Key=movie_id)
        file_type = metadata['ContentType']
        movie_size = metadata['ContentLength']
        movie_modified = metadata['LastModified'].isoformat()
        

        movies_table.put_item(
            Item={
                'movie_id': movie_id,
                'title': title,
                'genres': genres,
                'actors': actors,
                'directors': directors,
                'description': description,
                'file_type': file_type,
                'movie_size': movie_size,
                'movie_modified': movie_modified,
            }
        )  

        return {
            'statusCode': 200,
            'body': json.dumps({'message': "Successfully added movie!"})
        }
    except Exception as e:
        return{
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    
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