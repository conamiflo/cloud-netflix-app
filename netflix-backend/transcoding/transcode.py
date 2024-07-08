import json
import boto3

s3 = boto3.client('s3')
bucket_name = 'movie-bucket3'

def lambda_handler(event, context):
    # Extract movie_id and title from the event input
    movie_id = event['movie_id']
    title = event['title']

    # Perform any processing or transcoding logic here
    # For demonstration, just print out the received inputs
    print(f"Transcoding movie with ID: {movie_id}, Title: {title}")

    # Return a response if necessary
    return {
        'statusCode': 200,
        'body': json.dumps('Transcoding process initiated successfully')
    }