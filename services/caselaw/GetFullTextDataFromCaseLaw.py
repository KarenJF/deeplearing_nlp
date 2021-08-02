import os
import re

import requests
import logging
import datetime
import pytz
import json


#################
# Set Parameter Start#
#################
defaultSearchTerm='small+claims'
defaultJurisdiction='ill'

searchTermUsed=''
jurisdictionUsed=''

def getSearchTermUsed():
    return searchTermUsed

def setSearchTermUsed(value):
    global searchTermUsed
    searchTermUsed = value
    return searchTermUsed

def getJurisdictionUsed():
    return jurisdictionUsed

def setJurisdictionUsed(value):
    global jurisdictionUsed
    jurisdictionUsed = value
    return jurisdictionUsed
#################
# Set Parameter End#
#################




def getFullTextDataFromCaseLaw(
        # required, no default values
        authToken,
        cursor,

        # default values below
        pageSize='1',
        searchTerm=defaultSearchTerm,
        fullCaseText='true',
        jurisdiction=defaultJurisdiction,
        minDecisionDate='1930-01-01',
        maxDecisionDate='2020-12-31'
    ):


    # start constructing URL
    url = 'https://api.case.law/v1/cases/?' + \
          'page_size=' + pageSize + \
          '&jurisdiction=' + jurisdiction + \
          '&search=' + searchTerm + \
          '&full_case=' + fullCaseText + \
          '&decision_date_min=' + minDecisionDate + \
          '&decision_date_max=' + maxDecisionDate + \
          '&body_format=text&ordering=relevance'


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

    responseJsonObj = response.json()

    logging.info('response = ' + json.dumps(responseJsonObj))

    return responseJsonObj


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



def recordCaseLawData(responseJsonObj):

    #currentDirectory = os.getcwd()
    #logging.info('currentDirectory = ' + currentDirectory)

    # create file named with current timestamp
    # https://stackoverflow.com/questions/13866926/is-there-a-list-of-pytz-timezones

    pacificTimezone = pytz.timezone('US/Pacific')
    currentPST = datetime.datetime.now(pacificTimezone).isoformat()
    logging.info('current time = ' + currentPST)

    filename = getSearchTermUsed() + '-' + getJurisdictionUsed() + '-' + currentPST + '.json'

    # write/save data
    with open(
            os.path.join(
                # destination of file
                '../../data/downloaded/caselaw/raw',
                # name of file
                filename
            ),
            'w'
    ) as outfile:
        json.dump(responseJsonObj, outfile)


    '''
    # write/save data
    with open(
            os.path.join(
                # destination of file
                '../../data/downloaded/caselaw/raw',
                # name of file
                filename
            ),
            # write file as binary
            'wb'
    ) as output:
        output.write(response.content)
    '''

    return currentPST, filename



def updatePullRecords(
        currentPST,
        filename,
        responseJsonObj
):

    PULL_RECORD_FILE_PATH = '../../data/downloaded/caselaw/pull_records.json'

    # check if PULL_RECORD_FILE actually exists
    pullRecordFileExists = os.path.exists(PULL_RECORD_FILE_PATH)
    if pullRecordFileExists:
        logging.debug('pull record file EXISTS')

        # Opening JSON file
        pullRecordsJsonFile = open(PULL_RECORD_FILE_PATH, )

        # returns JSON
        pullRecordsJsonObj = json.load(pullRecordsJsonFile)

        pullRecords = pullRecordsJsonObj['pull_records']
        logging.info("BEFORE - pull_records = " + json.dumps(pullRecords))


        nextURL = responseJsonObj['next']
        #TODO: fix regular expression later
        nextCursor = re.search('&cursor=(.*)&decision_date_max', nextURL).group(1)

        if nextCursor:

            logging.info("nextCursor = " + nextCursor)

            pullRecords.append(
                {
                    "timestamp": currentPST,
                    "file_name": filename,
                    "search_term": getSearchTermUsed(),
                    "jurisdiction": getJurisdictionUsed(),
                    "next_cursor": nextCursor
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
                json.dump(pullRecordsJsonObj, outfile)

        else:
            logging.error('cursor DOES NOT EXIST')

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

    if authToken:
        logging.debug('authToken = ' + authToken)

        logging.debug('data pull -- start')

        setSearchTermUsed(defaultSearchTerm)
        setJurisdictionUsed('ill')

        responseJsonObj = getFullTextDataFromCaseLaw(
            authToken=authToken,
            cursor=getCursorValue(),
            pageSize='1',
            jurisdiction=getJurisdictionUsed(),
            searchTerm=getSearchTermUsed(),
            fullCaseText='true'
        )
        logging.debug('data pull -- end')


        logging.debug('writing to file -- start')
        currentPST, filename = recordCaseLawData(responseJsonObj)
        logging.debug('writing to file -- end')


        logging.debug('updating pull record -- start')
        updatePullRecords(
            currentPST,
            filename,
            responseJsonObj
        )
        logging.debug('updating pull record -- end')

    else:
        logging.debug('authToken is NULL')


    # outside
    logging.info("-----end GetFullTextDataFromCaseLaw-----")
