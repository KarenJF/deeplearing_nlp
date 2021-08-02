import requests
import logging
from pandas import json_normalize
import json
from datetime import date
import datetime
import re

#################
# Set Parameter #
#################
today = date.today()
today_str = today.strftime("%Y%m%d")
yesterday = today - datetime.timedelta(days=1)
yesterday_str = yesterday.strftime("%Y%m%d")

# set karen's token_id
token_id = 'Token f643c4cfb329a249febbecca90efa2736acf39ce'
#outputDir = '../../data/downloaded/caselaw/output'
outputDir = '/data/downloaded/caselaw/output'
searchTerm = 'small+claims'


def getDataFromCaseLaw(
        token_id,
        next_cursor,
        page_size='50',
        search='small+claims',
        full_case='true',
        jurisdiction='ill',
        decision_date_min='1930-01-01',
        decision_date_max='2020-12-31'
    ):

    # get url
    url = 'https://api.case.law/v1/cases/?' +\
          'page_size=' + page_size + \
          '&jurisdiction=' + jurisdiction
           #'&cursor=' + next_cursor

    #print('url = ' + url)
    logging.info('url = ' + url.__str__())

    response = requests.get(
        url
        #, headers={'Authorization': token_id}
    )

    #print('response = ' + response.content)
    logging.info('response = ' + response.content.__str__())

    return response


'''
def getCursorFromData():

    # load yesterday json cursor
    with open(outputDir + yesterday_str + '.json') as f:
        prior_case = json.load(f)

    # get the cursor value
    next_str = prior_case['next']
    cursor_str = re.search('&cursor=(.*)&decision_date_max', next_str).group(1)

    return cursor_str
'''


def writeDataToFile(response):

    # write data to today's json
    #with open(outputDir + today_str + '.json', 'wb') as outf:
    with open('data.json', 'wb') as outf:
        outf.write(response.content)

    return


def initLogging():
    # https://docs.python.org/3/howto/logging.html#logging-basic-tutorial
    logging.basicConfig(level=logging.DEBUG)
    return



if __name__ == "__main__":
    initLogging()
    logging.info("-----start-----")

    #cursor = getCursorFromData()
    cursor = "123"

    logging.debug('data pull -- start')
    response = getDataFromCaseLaw(token_id,
              next_cursor=cursor,
              page_size='50',
              search=searchTerm,
              full_case='false',
              jurisdiction='ill',
              decision_date_min='1930-01-01',
              decision_date_max='2020-12-31'
              )
    logging.debug('data pull -- end')

    logging.warning('writing to file -- start')
    writeDataToFile(response)
    logging.error('writing to file -- end')

    logging.info("-----end-----")
