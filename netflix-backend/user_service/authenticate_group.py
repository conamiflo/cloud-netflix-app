import boto3
import json
import os
import cognitojwt

mapGroupsToPaths = {
    '/testiranje': {
        'GET': 'Users'
    },
    '/movies':{
        "GET":['Users','Admins'],
        "POST":'Admins',
        "PUT":"Admins",
        "DELETE":"Admins"
    },
    '/series':{
        "GET":['Users','Admins'],
    },
    '/search':{
        "GET":['Users','Admins'],
    },
    '/subscriptions':{
        "GET":['Users','Admins'],
        "POST":['Users','Admins'],
        "DELETE":['Users','Admins']
    },'/reviews':{
        "GET":['Users','Admins'],
        "POST":['Users','Admins'],
    },'/feed':{
        "GET":['Users','Admins'],
    },'/history':{
        "POST":['Users','Admins'],
    },'/transcode':{
        "PUT":'Admins',
    },
    '/download':{
        "GET":['Users','Admins'],
    },
}

userpool_id= os.environ.get('USERPOOL_ID')
app_client_id =os.environ.get('WEB_CLIENT_ID')
region = boto3.Session().region_name

# Fetch the signing key using the JWKS URL

def handler(event, context):

    try:

        headers = event.get('headers', {})
        token = headers.get('authorizationtoken')
        http_method = event['httpMethod']
        resource=event['resource']
    except Exception as e:
        raise Exception('Invalid params')

    try:


        claims: dict = cognitojwt.decode(
            token,
            region,
            userpool_id,
            app_client_id=app_client_id,  # Optional
            testmode=False  # Disable token expiration check for testing purposes
        )

    except Exception as e:
        raise Exception('Non valid jwt')

    user_groups = claims.get('cognito:groups', [])

    try:

        if user_groups[0] not in mapGroupsToPaths[resource][http_method]:
            raise Exception('User is not authorized to perform this action')

    except Exception as e:
        raise Exception('err')



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

