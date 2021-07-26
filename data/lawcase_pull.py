import requests
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

def pull_data(token_id, 
              next_cursor,
              page_size='500', 
              search='car+accident',
              full_case='true',
              jurisdiction = 'ill',
              decision_date_min='1930-01-01',
              decision_date_max='2020-12-31'):
    
    # get url
    url = 'https://api.case.law/v1/cases/?page_size='+page_size+\
    '&search='+search+'&full_case='+full_case+'&jurisdiction='+jurisdiction+\
    '&cursor='+next_cursor +\
    '&decision_date_min='+decision_date_min +\
    '&decision_date_max='+decision_date_max +\
    '&body_format=text&ordering=relevance'    
    
    print(url)
    
    response = requests.get(url,headers={'Authorization': token_id})
    
    return response

def load_today_json(token_id, yesterday_str,today_str, search_term, state_name, min_date,max_date):
    # load yesterday json cursor
    with open('./data/car_accident_'+yesterday_str+'.json') as f:
        prior_case = json.load(f)

    # get the cursor value 
    next_str = prior_case['next']
    next_cursor_str = re.search('&cursor=(.*)&decision_date_max', next_str).group(1)
    
    # set next_url, max page = 500, full_case = true
    response = pull_data(token_id,
                     next_cursor=next_cursor_str,
                     page_size='500',search=search_term,
                     full_case='true',
                     jurisdiction = state_name,
                     decision_date_min=min_date,
                     decision_date_max=max_date)

    # write data to today's json
    with open('./data/car_accident_'+today_str+'.json', 'wb') as outf:
        outf.write(response.content)
    
    return
    

if __name__ == "__main__":
    load_today_json(token_id, yesterday_str,today_str, search_term='car+accident', state_name='cal', min_date='1930-01-01',max_date='2020-12-31')
    
