import requests.auth
import logging
import json

from utils import HelperUtils


defaultHeaders = {'User-Agent': 'Reddit-API/0.1'}
headers = {}

isBackHaul = False
#isBackHaul = True

def getHeaders():
    return headers

def setHeaders(value):
    global headers
    headers = value
    return headers

defaultPullCount = '50'
pullCount = '50'

def getPullCount():
    return pullCount

def setPullCount(value):
    global pullCount
    pullCount = value
    return pullCount




def getRedditAccessToken(
        tokenType
):

    redditAccessToken = ''

    CLIENT_ID  = HelperUtils.getTokenFromJsonFile(
        serviceType=SERVICE_TYPE,
        tokenKey='client_id',
        tokenType=tokenType
    )
    #logging.info("CLIENT_ID = " + CLIENT_ID)

    SECRET_TOKEN = HelperUtils.getTokenFromJsonFile(
        serviceType=SERVICE_TYPE,
        tokenKey='secret',
        tokenType=tokenType
    )
    #logging.info("SECRET_TOKEN = " + SECRET_TOKEN)

    # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_TOKEN)

    logging.info("tokenType = " + tokenType)

    if tokenType == 'personal_script':

        with open('redditPW.txt', 'r') as file:
            redditPassword = file.read()
        # logging.info("redditPassword = " + redditPassword)

        # here we pass our login method (password), username, and password
        data = {
            'grant_type': 'password',
            'username': 'patrickchho',
            'password': redditPassword
        }

    elif tokenType == 'web_app':

        # example
        # https://www.reddit.com/api/v1/authorize?client_id=DngWGr4tz0MOGHbQTLdyxA&response_type=code&state=1230&duration=temporary&scope=read&redirect_uri=https://www.reddit.com/user/patrickchho
        # https://www.reddit.com/user/patrickchho?state=random123&code=P8sGp7lgSuMduRvYQ3uwilrZQOs2Wg#_
        # https://www.reddit.com/user/patrickchho?state=1230&code=u6vE_IIVJK-9Ch1LTLi3akUxkWtZHw#_
        # in RESPONSE...
        # &code is ONE-TIME use
        # &state should match random string

        # FOR WEB_APP tokens
        data = {
            'grant_type': 'authorization_code',
            'code': 'kZBz8jEWljgXsDuLSKzSfYw5R9_kuw#_',
            'redirect_uri': 'https://www.reddit.com/user/patrickchho'
        }

    else:

        logging.error("tokenType = " + tokenType)

        data = {

        }

    # send our request for an OAuth token
    response = requests.post(
        'https://www.reddit.com/api/v1/access_token',
        auth=auth,
        data=data,
        headers=getHeaders()
    )

    accessResponseJsonObj = response.json()

    # TODO add error handling
    #if responseJsonObj['error']:
    # reddit JSON = {"message": "Unauthorized", "error": 401}
    # reddit JSON = {"access_token": "57301248-GNBaM2M83Toi_0hPRpADLpow2xZjAQ", "token_type": "bearer", "expires_in": 3600, "scope": "*"}

    logging.info("accessResponseJsonObj = " + json.dumps(accessResponseJsonObj))

    # convert response to JSON and pull access_token value
    redditAccessToken = accessResponseJsonObj['access_token']

    return redditAccessToken



def getContentDataFromReddit(
        redditAccessToken
):

    # add authorization to our headers dictionary
    setHeaders({**headers, **{'Authorization': f"bearer {redditAccessToken}"}})

    '''
    # while the token is valid (~2 hours) we just add headers=headers to our requests
    responseX = requests.get(
        'https://oauth.reddit.com/api/v1/me',
        headers=getHeaders()
    )
    tempJsonObj = responseX.json()
    logging.info("tempJsonObj = " + json.dumps(tempJsonObj))
    '''


    params = {
        'limit': getPullCount()
    }

    retrievedCursor = HelperUtils.getTagForNextPull('reddit')
    logging.info("retrievedCursor = " + retrievedCursor)

    if isBackHaul & len(retrievedCursor)>0:
        params = {**params,
                  **{'after': {retrievedCursor}}
                  }
        logging.info("params = " + str(params))



    # other endpoints:
    # ~.../hot
    # ~.../best
    # ~.../new
    # https://www.reddit.com/dev/api/#section_listings

    # Confusingly, AFTER means further back in time, whereas BEFORE means more recently in time.
    # The limit is set to 25 by default. We can pump this up to a maximum value of 100 items

    response = requests.get(
        "https://oauth.reddit.com/r/legaladvice/hot",
        headers=getHeaders(),
        params=params
    )

    # TODO add error handling
    responseJsonObj = response.json()
    logging.info("responseJsonObj = " + json.dumps(responseJsonObj))

    return responseJsonObj




if __name__ == "__main__":
    HelperUtils.initLogging()
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

    setHeaders(defaultHeaders)
    setPullCount(defaultPullCount)

    logging.debug('reddit access token -- start')
    redditAccessToken = getRedditAccessToken(
        TOKEN_TYPE
    )
    logging.debug('reddit access token -- end')



    logging.debug('data pull -- start')
    responseJsonObj = getContentDataFromReddit(
        redditAccessToken
    )
    logging.debug('data pull -- end')


    logging.debug('writing to file -- start')
    currentPST, filename = HelperUtils.recordRedditData(
        responseJsonObj
    )
    logging.debug('writing to file -- end')


    logging.debug('updating pull record -- start')
    HelperUtils.updateRedditPullRecords(
        currentPST=currentPST,
        filename=filename,
        responseJsonObj=responseJsonObj
    )
    logging.debug('updating pull record -- end')


    logging.info("-----end GetSampleDataFromReddit-----")

