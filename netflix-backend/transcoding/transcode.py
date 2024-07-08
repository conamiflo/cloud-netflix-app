import json
import boto3
import subprocess
import os

s3 = boto3.client('s3')
bucket_name = 'movie-bucket3'

def handler(event, context):
    movie_id = event['movie_id']
    target_resolution = event['resolution']

    resolution_map = {
        '360': '640:360',
        '480': '854:480',
        '720': '1280:720'
    }

    if target_resolution not in resolution_map:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid resolution specified')
        }

    local_movie_path = f'/tmp/{movie_id}.mp4'

    try:
        s3.download_file(bucket_name, movie_id, local_movie_path)
    except Exception as e:
        return {
            'statusCode': 501,
            'body': json.dumps(f'Error downloading movie from S3: {str(e)}')
        }

    output_path = f'/tmp/{movie_id}_{target_resolution}.mp4'

    ffmpeg_command = f'/opt/ffmpeg -y -i {local_movie_path} -codec:v mpeg4 -vf scale={resolution_map[target_resolution]} -c:a copy {output_path}'
    try:
        subprocess.run(ffmpeg_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        return {
            'statusCode': 502,
            'body': json.dumps(f'Error transcoding movie: {str(e)}')
        }

    output_s3_key = f'{target_resolution}/{movie_id}'
    try:
        with open(output_path, "rb") as f:
            s3.put_object(Bucket=bucket_name, Key=output_s3_key, Body=f, ContentType='video/mp4')
    except Exception as e:
        return {
            'statusCode': 503,
            'body': json.dumps(f'Error uploading transcoded movie to S3: {str(e)}')
        }

    os.remove(local_movie_path)
    os.remove(output_path)

    return {
        'statusCode': 200,
        'body': json.dumps('Transcoding process initiated successfully')
    }