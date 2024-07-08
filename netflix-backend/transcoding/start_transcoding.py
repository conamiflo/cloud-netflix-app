import json
import os
import boto3

client = boto3.client('stepfunctions')
state_machine_arn = os.environ['STATE_MACHINE_ARN']

def handler(event, context):
    try:
        body = json.loads(event['body'])
        sm_input = json.dumps({"movie_id": body['movie_id']})

        response = client.start_execution(
            stateMachineArn=state_machine_arn,
            input=sm_input
        )
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'response': response}, default=str)
        }
    except Exception as e:
        return{
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'error': str(e)})
        }
