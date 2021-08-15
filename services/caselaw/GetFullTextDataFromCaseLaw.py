import requests
import logging
import json

from utils import Utils

#################
# Set Parameter Start#
#################

defaultSearchTerm='small+claims'
defaultJurisdiction='ill'
#defaultJurisdiction='cal'
defaultPageSize='5'
#defaultPageSize=500

searchTermUsed=''
jurisdictionUsed=''
pageSizeUsed='1'

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

def getPageSizeUsed():
    return pageSizeUsed

def setPageSizeUsed(value):
    global pageSizeUsed
    pageSizeUsed = value
    return pageSizeUsed

#################
# Set Parameter End#
#################


def getFullTextDataFromCaseLaw(
        # required, no default values
        authToken,
        cursor,

        # default values below
        pageSize=defaultPageSize,
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






if __name__ == "__main__":
    Utils.initLogging()
    logging.info("-----start GetFullTextDataFromCaseLaw-----")

    SERVICE_TYPE = 'case_law'

    authToken = Utils.getTokenFromJsonFile(
        serviceType='case_law',
        tokenKey='token'
    )

    if authToken:
        logging.debug('authToken = ' + authToken)

        logging.debug('data pull -- start')

        setSearchTermUsed(defaultSearchTerm)
        setJurisdictionUsed(defaultJurisdiction)
        setPageSizeUsed(defaultPageSize)

        retrievedCursor = Utils.getTagForNextPull(
            getJurisdictionUsed()
        )

        responseJsonObj = getFullTextDataFromCaseLaw(
            authToken=authToken,
            cursor=retrievedCursor,
            pageSize=getPageSizeUsed(),
            jurisdiction=getJurisdictionUsed(),
            searchTerm=getSearchTermUsed(),
            fullCaseText='true'
        )
        logging.debug('data pull -- end')


        logging.debug('writing to file -- start')
        currentPST, filename = Utils.recordCaseLawData(
            responseJsonObj,
            getSearchTermUsed(),
            getJurisdictionUsed()
        )
        logging.debug('writing to file -- end')


        logging.debug('updating pull record -- start')
        Utils.updateCaseLawPullRecords(
            currentPST=currentPST,
            filename=filename,
            searchTermUsed=getSearchTermUsed(),
            jurisdictionUsed=getJurisdictionUsed(),
            responseJsonObj=responseJsonObj
        )
        logging.debug('updating pull record -- end')

    else:
        logging.debug('authToken is NULL')


    # outside
    logging.info("-----end GetFullTextDataFromCaseLaw-----")
