import json

def handler(event, context):
    movie_id = event['movie_id']
    resolutions = ['360', '480', '720']

    return {
        'movie_id': movie_id,
        'resolutions': resolutions
    }