from urllib.parse import urlparse

import boto3
from jwt import decode
import json
from jwt import exceptions as jwt_exceptions
from botocore.exceptions import ClientError
import os

cognito_client = boto3.client('cognito-idp')
ssm_client = boto3.client('ssm')

mapGroupsToPaths = {
    '/testiranje': {
        'GET': 'Users'
    }
}



userpool_id= os.environ.get('USERPOOL_ID')
app_client_id =os.environ.get('WEB_CLIENT_ID')
region = boto3.Session().region_name

def handler(event, context):

    headers = event.get('headers', {})
    token = headers.get('authorizationToken')
    http_method = event['httpMethod']
    resource=event['resource']


    try:
        claims = decode(token, options={"verify_signature": False})

        user_groups = claims.get('cognito:groups', [])


        if mapGroupsToPaths[resource][http_method]  not in user_groups:
            raise Exception('User is not authorized to perform this action')


    except jwt_exceptions.DecodeError as e:
        raise Exception('Unauthorized')
    except jwt_exceptions.InvalidTokenError as e:
        raise Exception('Unauthorized')
    except ClientError as e:
        raise Exception('Unauthorized')

    response = generateAllow('me', "*")
    print('authorized')
    return json.loads(response)

def generatePolicy(principalId, effect, resource):
    authResponse = {}
    authResponse['principalId'] = principalId
    if (effect and resource):
        policyDocument = {}
        policyDocument['Version'] = '2012-10-17'
        policyDocument['Statement'] = []
        statementOne = {}
        statementOne['Action'] = 'execute-api:Invoke'
        statementOne['Effect'] = effect
        statementOne['Resource'] = resource
        policyDocument['Statement'] = [statementOne]
        authResponse['policyDocument'] = policyDocument

    authResponse['context'] = {
        "stringKey": "stringval",
        "numberKey": 123,
        "booleanKey": True
    }

    authResponse_JSON = json.dumps(authResponse)

    return authResponse_JSON


def generateAllow(principalId, resource):
    return generatePolicy(principalId, 'Allow', resource)


