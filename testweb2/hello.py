from django.http import HttpResponse
import requests
import json
import logging
import jwt
from django.conf import settings

def hello_world(request):

    logger = logging.getLogger(__name__)

    # Define the endpoint URL
    host = 'http://localhost:8080/auth'
    realm = 'myrealm'
    url = host + '/realms/' + realm + '/protocol/openid-connect/token'
    logger.info('url: ' + url)

    # Define the data to be sent in the request
    client_id = 'testclient'
    client_secret = 'a15b42df-b1fc-48de-8369-68f40323ef99'
    username = 'myuser'
    password = 'P455w0rd!'
    data = 'grant_type=password&scope=openid&client_id=' + client_id + '&client_secret=' + client_secret + '&username=' + username + '&password=' + password
    logger.info('data: ' + data)

    # Set the content type of the request to JSON
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    # Send the POST request
    logger.info('Begin sending POST')
    response = requests.post(url, data=data, headers=headers)
    logger.info('Finish sending POST')

    # Check if the request was successful
    if response.status_code == 200:
        # Request was successful, do something with the response
        logger.info('response.status_code: ' + str(response.status_code))
        
        response_str = response.content.decode('utf-8')
        response_obj = json.loads(response_str)
        access_token = response_obj['access_token']
        # decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
        decoded_token = jwt.decode(access_token, options={"verify_signature": False})
        roles = decoded_token['resource_access']['account']['roles']

        return HttpResponse(roles)
    else:
        # Request failed, handle the error
        logger.error('response.status_code: ', str(response.status_code))
        return HttpResponse(response, response.status_code)

#   return HttpResponse("Hello, " + request.user.username + '!')