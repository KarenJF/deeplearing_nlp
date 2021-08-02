import os
import requests
import logging
import datetime
import pytz


#################
# Set Parameter #
#################

# set karen's token_id
token_id = 'Token f643c4cfb329a249febbecca90efa2736acf39ce'


def getDataFromCaseLaw(
        token_id,
        cursor='abc',
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

    response = requests.get(
        url
        #, headers={'Authorization': token_id}
    )

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

    currentDirectory = os.getcwd()
    logging.info('currentDirectory = ' + currentDirectory)

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
    logging.info("-----start GetDataFromCaseLaw-----")


    logging.debug('data pull -- start')
    response = getDataFromCaseLaw(
        token_id,
        page_size='50',
        jurisdiction='ill',
    )
    logging.debug('data pull -- end')


    logging.debug('writing to file -- start')
    writeDataToFile(response)
    logging.debug('writing to file -- end')

    logging.info("-----end GetDataFromCaseLaw-----")
