import os
import requests
import logging
import datetime
import pytz
import json


#################
# Set Parameter #
#################


def getSampleDataFromCaseLaw(
        token_id='TokenHere',
        cursor='CursorHere',
        page_size='50',
        search='small+claims',
        full_case='false',
        jurisdiction='ill',
        decision_date_min='1930-01-01',
        decision_date_max='2020-12-31'
    ):

    # get url
    url = 'https://api.case.law/v1/cases/?' +\
          'page_size=' + page_size + \
          '&jurisdiction=' + jurisdiction
           #'&cursor=' + next_cursor

    logging.info('url = ' + url.__str__())

    #CASE_LAW_AUTH_TOKEN = getAuthToken()

    response = requests.get(
        url
        #, headers={'Authorization': 'TOKEN ' + CASE_LAW_AUTH_TOKEN}
    )

    logging.info('response = ' + response.content.__str__())

    return response



def getAuthToken(
        service_type='case_law'
):

    TOKEN_FILE_PATH = '../../utils/tokens.json'

    token = ''

    # check if TOKEN_FILE actually exists
    tokenFileExists = os.path.exists(TOKEN_FILE_PATH)
    if tokenFileExists:
        logging.debug('token file EXISTS')

        # Opening JSON file
        tokenFile = open(TOKEN_FILE_PATH, )

        # returns JSON
        tokenJsonObj = json.load(tokenFile)

        tokensArray = tokenJsonObj[service_type]['tokens']

        if len(tokensArray) > 0:
            logging.debug('array length is valid')

            token = tokensArray[0]['token']
            #logging.info('TOKEN = ' + token)

        else:
            logging.error('array length is NOT valid')

    else:
        logging.error('token file DOES NOT EXIST')

    return token



def writeDataToFile(response):

    #currentDirectory = os.getcwd()
    #logging.info('currentDirectory = ' + currentDirectory)

    # create file named with current timestamp
    # https://stackoverflow.com/questions/13866926/is-there-a-list-of-pytz-timezones

    pacificTimezone = pytz.timezone('US/Pacific')
    currentPST = datetime.datetime.now(pacificTimezone).isoformat()
    logging.info('current time = ' + currentPST)


    # write/save data
    with open(
            os.path.join(
                # destination of file
                '../../data/downloaded/testing',
                # name of file
                currentPST + '.json'
            ),
            # write file as binary
            'wb'
    ) as output:
        output.write(response.content)

    return


def initLogging():
    # https://docs.python.org/3/howto/logging.html#logging-basic-tutorial
    logging.basicConfig(level=logging.DEBUG)
    return



if __name__ == "__main__":
    initLogging()
    logging.info("-----start GetSampleDataFromCaseLaw-----")


    logging.debug('data pull -- start')
    response = getSampleDataFromCaseLaw(
        #getAuthToken(),
        page_size='50',
        jurisdiction='ill',
    )
    logging.debug('data pull -- end')


    logging.debug('writing to file -- start')
    writeDataToFile(response)
    #getAuthToken()
    logging.debug('writing to file -- end')

    logging.info("-----end GetSampleDataFromCaseLaw-----")
