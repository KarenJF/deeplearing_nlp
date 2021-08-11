import requests.auth
import logging
import json

from utils import Utils

if __name__ == "__main__":
    Utils.initLogging()
    logging.info("-----start GetSampleDataFromReddit-----")

    # TUTORIAL
    # https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c

    # REDDIT API DOC
    # https://www.reddit.com/dev/api/
    # https://www.reddit.com/dev/api/#GET_best (use LISTING section)
    # https://www.reddit.com/wiki/api
    # https://github.com/reddit-archive/reddit/wiki/OAuth2 (reddit auth)
    # https://github.com/reddit-archive/reddit/wiki/JSON (reddit JSON schema)

    SERVICE_TYPE = 'reddit'
    #TOKEN_TYPE = 'web_app'
    TOKEN_TYPE = 'personal_script'


    CLIENT_ID  = Utils.getTokenFromJsonFile(
        SERVICE_TYPE,
        TOKEN_TYPE,
        'client_id'
    )
    #logging.info("CLIENT_ID = " + CLIENT_ID)

    SECRET_TOKEN = Utils.getTokenFromJsonFile(
        SERVICE_TYPE,
        TOKEN_TYPE,
        'secret'
    )
    #logging.info("SECRET_TOKEN = " + SECRET_TOKEN)

    # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_TOKEN)


    # example
    # https://www.reddit.com/api/v1/authorize?client_id=DngWGr4tz0MOGHbQTLdyxA&response_type=code&state=1230&duration=temporary&scope=read&redirect_uri=https://www.reddit.com/user/patrickchho
    # https://www.reddit.com/user/patrickchho?state=random123&code=P8sGp7lgSuMduRvYQ3uwilrZQOs2Wg#_
    # https://www.reddit.com/user/patrickchho?state=1230&code=u6vE_IIVJK-9Ch1LTLi3akUxkWtZHw#_
    # in RESPONSE...
    # &code is ONE-TIME use
    # &state should match random string

    # FOR WEB_APP tokens
    '''
    data = {
        'grant_type': 'authorization_code',
        'code': 'kZBz8jEWljgXsDuLSKzSfYw5R9_kuw#_',
        'redirect_uri': 'https://www.reddit.com/user/patrickchho'
    }
    '''

    with open('redditPW.txt', 'r') as file:
        redditPassword = file.read()
    #logging.info("redditPassword = " + redditPassword)


    # here we pass our login method (password), username, and password
    data = {
        'grant_type': 'password',
        'username': 'patrickchho',
        'password': redditPassword
    }


    # setup our header info, which gives reddit a brief description of our app
    headers = {'User-Agent': 'Reddit-API/0.1'}

    # send our request for an OAuth token
    response = requests.post(
        'https://www.reddit.com/api/v1/access_token',
        auth=auth,
        data=data,
        headers=headers
    )

    responseJsonObj = response.json()

    # TODO add error handling
    #if responseJsonObj['error']:

    # reddit JSON = {"message": "Unauthorized", "error": 401}
    # reddit JSON = {"access_token": "57301248-GNBaM2M83Toi_0hPRpADLpow2xZjAQ", "token_type": "bearer", "expires_in": 3600, "scope": "*"}


    logging.info("reddit JSON = " + json.dumps(responseJsonObj))

    # convert response to JSON and pull access_token value
    TOKEN = responseJsonObj['access_token']





    # add authorization to our headers dictionary
    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

    # while the token is valid (~2 hours) we just add headers=headers to our requests
    requests.get(
        'https://oauth.reddit.com/api/v1/me',
        headers=headers
    )

    response2 = requests.get(
        "https://oauth.reddit.com/r/legaladvice/hot",
        headers=headers
    )

    # TODO add error handling
    response2JsonObj = response2.json()
    logging.info("reddit JSON = " + json.dumps(response2JsonObj))