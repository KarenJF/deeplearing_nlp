import requests
import logging
import json

from utils import Utils

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

    logging.info('url = ' + url.__str__())

    response = requests.get(
        url
        #, headers={'Authorization': 'TOKEN ' + CASE_LAW_AUTH_TOKEN}
    )

    logging.info('response = ' + json.dumps(response.json()))

    return response



if __name__ == "__main__":
    Utils.initLogging()
    logging.info("-----start GetSampleDataFromCaseLaw-----")


    logging.debug('data pull -- start')
    response = getSampleDataFromCaseLaw(
        page_size='50',
        jurisdiction='ill',
    )
    logging.debug('data pull -- end')


    logging.debug('writing to file -- start')
    Utils.recordCaseLawData(response.json())
    logging.debug('writing to file -- end')

    logging.info("-----end GetSampleDataFromCaseLaw-----")
