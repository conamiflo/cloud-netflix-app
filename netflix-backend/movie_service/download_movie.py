import base64
import json
import boto3

dynamodb = boto3.resource('dynamodb')
# s3 = boto3.client('s3')
s3_client = boto3.client('s3', region_name='eu-central-1')

def download_movie(event, context):
    movies_table = dynamodb.Table('movie-table2')
    s3_bucket = 'movie-bucket'

    try:

        movie_id = int(event['queryStringParameters']['movie_id'])

        response = movies_table.get_item(
            Key={
                'movie_id': movie_id
            }
        )

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

