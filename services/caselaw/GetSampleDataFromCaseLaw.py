import os

import requests
import logging
import json

#sys.path.append('../utils')
#sys.path.append('/utils')
#sys.path.insert(1, '/utils')
#import HelperUtils
import sys
#sys.path.append('/Users/pho/Documents/workspace/legalTech')
#sys.path.append("../..")

root_dir = sys.path[1]
helper_dir = root_dir + '/utils'
sys.path.append(helper_dir)
from utils import HelperUtils
#from utils import HelperUtils

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
    HelperUtils.initLogging()
    logging.info("-----start GetSampleDataFromCaseLaw-----")

    sysPath = sys.path
    print(sysPath)
    # [
    # '/Users/pho/Documents/workspace/legalTech/services/caselaw',
    # '/Users/pho/Documents/workspace/legalTech',
    # '/usr/local/Cellar/python@3.9/3.9.6/Frameworks/Python.framework/Versions/3.9/lib/python39.zip',
    # '/usr/local/Cellar/python@3.9/3.9.6/Frameworks/Python.framework/Versions/3.9/lib/python3.9',
    # '/usr/local/Cellar/python@3.9/3.9.6/Frameworks/Python.framework/Versions/3.9/lib/python3.9/lib-dynload',
    # '/usr/local/lib/python3.9/site-packages'
    # ]

    osPath = os.getcwd()
    logging.info('osPath = ' + osPath)
    # osPath = /Users/pho/Documents/workspace/legalTech/services/caselaw

    logging.debug('data pull -- start')
    response = getSampleDataFromCaseLaw(
        page_size='50',
        jurisdiction='ill',
    )
    logging.debug('data pull -- end')


    logging.debug('writing to file -- start')
    HelperUtils.recordCaseLawData(response.json())
    logging.debug('writing to file -- end')

    logging.info("-----end GetSampleDataFromCaseLaw-----")
