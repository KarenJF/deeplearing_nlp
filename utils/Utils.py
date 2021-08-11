import logging
import os
import json


def initLogging():
    # https://docs.python.org/3/howto/logging.html#logging-basic-tutorial
    logging.basicConfig(level=logging.DEBUG)
    return



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


def getTokenFromJsonFile(
        serviceType,
        tokenType,
        tokenKey
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

        tokensArray = tokenJsonObj[serviceType]['tokens']

        if len(tokensArray) > 0:
            logging.debug('array length is valid')

            index = 0
            if tokenType == 'web_app':
                index = 0
            elif tokenType == 'personal_script':
                index = 1
            else:
                index = 0


            # find index by tokenType
            token = tokensArray[index][tokenKey]
            logging.info('TOKEN = ' + token)

        else:
            logging.error('array length is NOT valid')

    else:
        logging.error('token file DOES NOT EXIST')

    return token