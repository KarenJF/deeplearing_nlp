import logging
import json
import datetime
import pytz
import os
import re


#################
# GENERAL COMMON FUNCTIONS#
#################

def initLogging():
    # https://docs.python.org/3/howto/logging.html#logging-basic-tutorial
    logging.basicConfig(level=logging.DEBUG)
    return


def getCurrentPacificTime():

    # https://stackoverflow.com/questions/13866926/is-there-a-list-of-pytz-timezones
    pacificTimezone = pytz.timezone('US/Pacific')
    currentPST = datetime.datetime.now(pacificTimezone).isoformat()
    logging.info('current time = ' + currentPST)

    return currentPST



#################
# CASE_LAW COMMON FUNCTIONS START#
#################

#def getCaseLawCursorValueForNextPull(jurisdictionUsed):
def getTagForNextPull(
        jurisdictionUsed
):

    if jurisdictionUsed=='cal':
        PULL_RECORD_FILE_PATH = '../../data/downloaded/caselaw/pull_records_cal.json'
    else:
        PULL_RECORD_FILE_PATH = '../../data/downloaded/caselaw/pull_records_ill.json'

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

            # go to last record (latest pull) and find cursor
            # will use cursor in upcoming data pull
            cursor = pullRecords[pullRecordsCount - 1].get('next_cursor')

            logging.info('cursor = ' + cursor)

        else:
            logging.error('array length is NOT valid')

    else:
        logging.error('pull record file DOES NOT EXIST')

    return cursor


def recordCaseLawData(
        responseJsonObj,
        searchTermUsed='',
        jurisdictionUsed=''
):

    #currentDirectory = os.getcwd()
    #logging.info('currentDirectory = ' + currentDirectory)

    # create file named with current timestamp
    currentPST = getCurrentPacificTime()

    # SAMPLE data have jurisdictionUsed and searchTermUsed as BLANK, goes to IF clause
    # REAL data goes to ELSE clause
    if (jurisdictionUsed=='') & (searchTermUsed==''):

        destinationPath = '../../data/downloaded/testing'
        filename = currentPST + '.json'

    else:

        #separate folders for cal (has token rate limit) vs ill (free)

        if jurisdictionUsed == 'cal':
            destinationPath = '../../data/downloaded/caselaw/raw/cal'
        else:
            destinationPath = '../../data/downloaded/caselaw/raw/ill'

        filename = searchTermUsed + '-' + jurisdictionUsed + '-' + currentPST + '.json'

    # write/save data
    with open(
            os.path.join(
                destinationPath,
                filename
            ),
            'w'
    ) as outfile:
        json.dump(responseJsonObj, outfile, indent=4)
        #json.dump(responseJsonObj, outfile)

    return currentPST, filename



def updateCaseLawPullRecords(
        currentPST,
        filename,
        searchTermUsed,
        jurisdictionUsed,
        responseJsonObj
):
    if jurisdictionUsed=='cal':
        PULL_RECORD_FILE_PATH = '../../data/downloaded/caselaw/pull_records_cal.json'
        pullRecordFilename = 'pull_records_cal.json'
    else:
        PULL_RECORD_FILE_PATH = '../../data/downloaded/caselaw/pull_records_ill.json'
        pullRecordFilename = 'pull_records_ill.json'


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
        #TODO: fix regular expression to be more dynamic, not rely on checking "decision_date_max"
        nextCursor = re.search('&cursor=(.*)&decision_date_max', nextURL).group(1)

        if nextCursor:

            logging.info("nextCursor = " + nextCursor)

            pullRecords.append(
                {
                    "timestamp": currentPST,
                    "file_name": filename,
                    "count": len(responseJsonObj['results']),
                    "search_term": searchTermUsed,
                    "jurisdiction": jurisdictionUsed,
                    "next_cursor": nextCursor
                }
            )

            logging.info("AFTER - pull_records = " + json.dumps(pullRecords))

            # write/save data
            with open(
                    os.path.join(
                        '../../data/downloaded/caselaw',
                        pullRecordFilename
                    ),
                    'w'
            ) as outfile:
                json.dump(pullRecordsJsonObj, outfile, indent=4)

        else:
            logging.error('cursor DOES NOT EXIST')

    else:
        logging.error('pull record file DOES NOT EXIST')

    return

#################
# CASE_LAW COMMON FUNCTIONS END#
#################



#################
# REDDIT COMMON FUNCTIONS START#
#################

def recordRedditData(
        responseJsonObj
):
    # create file named with current timestamp
    currentPST = getCurrentPacificTime()

    destinationPath = '../../data/downloaded/reddit/raw/'
    filename = 'legaladvice-' + currentPST + '.json'

    # write/save data
    with open(
            os.path.join(
                destinationPath,
                filename
            ),
            'w'
    ) as outfile:
        json.dump(responseJsonObj, outfile, indent=4)

    return currentPST, filename



def updateRedditPullRecords(
        currentPST,
        filename,
        responseJsonObj
):

    PULL_RECORD_FILE_PATH = '../../data/downloaded/reddit/pull_records_reddit.json'
    pullRecordFilename = 'pull_records_reddit.json'


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


        afterTag = responseJsonObj['data']['after']
        logging.info("afterTag = " + (afterTag if afterTag else 'NULL'))

        beforeTag = responseJsonObj['data']['before']
        logging.info("beforeTag = " + (beforeTag if beforeTag else 'NULL'))

        # IMPORTANT:
        # title, selftext, id
        # the property 'kind' has a value of 't3' means a reddit thread
        # append: "kind" and "id" for an easy unique identifier (full name is reddit doc)
        # example: t3_p53sq3

        pullRecords.append(
            {
                "timestamp": currentPST,
                "file_name": filename,
                "count": responseJsonObj['data']['dist'],
                "subreddit": 'r/legaladvice',
                "after_tag": afterTag,
                "before_tag": beforeTag
            }
        )

        logging.info("AFTER - pull_records = " + json.dumps(pullRecords))

        # write/save data
        with open(
                os.path.join(
                    '../../data/downloaded/reddit',
                    pullRecordFilename
                ),
                'w'
        ) as outfile:
            json.dump(pullRecordsJsonObj, outfile, indent=4)

    else:
        logging.error('pull record file DOES NOT EXIST')

    return


#################
# REDDIT COMMON FUNCTIONS END#
#################



#################
# TOKEN COMMON FUNCTIONS START#
#################

def getTokenFromJsonFile(
        serviceType,
        tokenKey,
        tokenType='web_app'
):
    # this function is used to retrieve TOKENs to log into systems to backhaul data
    # example systems are: Reddit, CaseLaw

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

            # see tokens.json for details
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

#################
# TOKEN COMMON FUNCTIONS END#
#################