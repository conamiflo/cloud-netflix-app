import json
import os
import boto3

client = boto3.client('stepfunctions')


def handler(event, context):
    state_machine_arn = os.environ['STATE_MACHINE_ARN']
    body = json.loads(event['body'])
    movie_id = body['movie_id']
    input_payload = json.dumps({"movie_id": movie_id})

    response = client.start_execution(
        stateMachineArn=state_machine_arn,
        input=input_payload
    )
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps({'response': response}, default=str)
    }
