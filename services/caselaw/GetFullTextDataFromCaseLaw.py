import os
import requests
import logging
import datetime
import pytz
import json


def getFullTextDataFromCaseLaw(
        # required, no default values
        authToken,
        cursor,

        # default values below
        pageSize='50',
        searchTerm='small+claims',
        fullCaseText='false',
        jurisdiction='ill',
        minDecisionDate='1930-01-01',
        maxDecisionDate='2020-12-31'
    ):

    url = 'https://api.case.law/v1/cases/?' + \
          'page_size=' + pageSize + \
          '&jurisdiction=' + jurisdiction

    if cursor:
        logging.debug('cursor = ' + cursor)
        url = url + '&cursor=' + cursor
    else:
        logging.debug('cursor is NULL')


    logging.info('url = ' + url)

    response = requests.get(
        url,
        headers={'Authorization':'TOKEN ' + authToken}
    )

    logging.info('response = ' + response.content.__str__())

    return response


def getCursorValue():

    PULL_RECORD_FILE_PATH = '../../data/downloaded/caselaw/pull_records.json'
    cursor = ''

    # check if PULL_RECORD_FILE actually exists
    pullRecordFileExists = os.path.exists(PULL_RECORD_FILE_PATH)
    if pullRecordFileExists:
        logging.debug('pull record file EXISTS')

        # Opening JSON file
        jsonFile = open(PULL_RECORD_FILE_PATH, )

        # returns JSON
        jsonObj = json.load(jsonFile)

        pullRecords = jsonObj['pull_records']
        pullRecordsCount = len(pullRecords)

        if pullRecordsCount > 0:
            logging.debug('array length is valid')

            #'next_cursor' in pullRecords[pullRecordsCount-1]
            #pullRecords[pullRecordsCount-1].get('next_cursor')

            # go to last record (latest pull) and find cursor
            # will use cursor in upcoming data pull
            cursor = pullRecords[pullRecordsCount - 1].get('next_cursor')

            logging.info('cursor = ' + cursor)

        else:
            logging.error('array length is NOT valid')

    else:
        logging.error('pull record file DOES NOT EXIST')


    return cursor


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



def downloadCaseLawData(response):

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
                '../../data/downloaded/caselaw/raw',
                # name of file
                currentPST + '.json'
            ),
            # write file as binary
            'wb'
    ) as output:
        output.write(response.content)

    return



def updatePullRecords():

    PULL_RECORD_FILE_PATH = '../../data/downloaded/caselaw/pull_records.json'

    # check if PULL_RECORD_FILE actually exists
    pullRecordFileExists = os.path.exists(PULL_RECORD_FILE_PATH)
    if pullRecordFileExists:
        logging.debug('pull record file EXISTS')

        # Opening JSON file
        jsonFile = open(PULL_RECORD_FILE_PATH, )

        # returns JSON
        jsonObj = json.load(jsonFile)

        pullRecords = jsonObj['pull_records']
        logging.info("BEFORE - pull_records = " + json.dumps(pullRecords))

        pullRecords.append(
            {
                "timestamp": "value-112",
                "file_name": "value-212",
                "search_term": "value-312",
                "jurisdiction": "value-412",
                "next_cursor": "value-512"
            }
        )

        logging.info("AFTER - pull_records = " + json.dumps(pullRecords))

        # write/save data
        with open(
                os.path.join(
                    # destination of file
                    '../../data/downloaded/caselaw',
                    # name of file
                    'pull_records.json'
                ),
                'w'
        ) as outfile:
            json.dump(jsonObj, outfile)

    else:
        logging.error('pull record file DOES NOT EXIST')

    return



def initLogging():
    # https://docs.python.org/3/howto/logging.html#logging-basic-tutorial
    logging.basicConfig(level=logging.DEBUG)
    return



if __name__ == "__main__":
    initLogging()
    logging.info("-----start GetFullTextDataFromCaseLaw-----")

    authToken = getAuthToken(service_type='case_law')
    #authToken = 'abc'

    if authToken:
        logging.debug('authToken = ' + authToken)

        logging.debug('data pull -- start')

        response = getFullTextDataFromCaseLaw(
            authToken=authToken,
            cursor=getCursorValue(),
            pageSize='1',
            jurisdiction='cal',
            fullCaseText='true'
        )
        logging.debug('data pull -- end')


        logging.debug('writing to file -- start')
        downloadCaseLawData(response)
        logging.debug('writing to file -- end')


        logging.debug('GET cursor value -- start')
        getCursorValue()
        logging.debug('GET cursor value -- end')


        logging.debug('updating pull record -- start')
        updatePullRecords()
        logging.debug('updating pull record -- end')
    else:
        logging.debug('authToken is NULL')


    # outside
    logging.info("-----end GetFullTextDataFromCaseLaw-----")
