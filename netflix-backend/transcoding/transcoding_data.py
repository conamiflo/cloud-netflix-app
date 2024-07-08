import json

def handler(event, context):
    movie_id = event['movie_id']

    return {
        'movie_id': movie_id,
    }