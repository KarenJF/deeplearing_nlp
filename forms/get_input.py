import os
import re

import pdfrw
import subprocess
import os.path
import sys
import json
from importlib import reload 
from helper_function import get_page1_input
# only use to reload the helper function
#reload(get_page1_input)

## Goal: Asking User input to update the data dictionary
def get_page1(data_dict):
    # Question: To be completed by an Attorney?
    data_dict = get_page1_input.get_attorney_info(data_dict)

    # Part 1-1,1-2
    data_dict = get_page1_input.get_initial_renewal(data_dict)
        
    # Part1, Item 3: Full Legal Name
    data_dict = get_page1_input.get_legal_name(data_dict)

    # Part1, Item 4: Mailing Address
    data_dict = get_page1_input.get_mail_address(data_dict)

    # Part1, Item 5: Removal Proceedings
    data_dict = get_page1_input.get_removal_proceeding(data_dict)

    return data_dict

if __name__ == '__main__':
    # Step 1: Create empty dictionary
    data_dict = dict()
    
    # Step 2: Start asking questions 
    print("Thank you for using FillMeForms! Let's begin to fill out the DACA form")
    data_dict = get_page1(data_dict)
    
    # Step 3: Save the data dictionary
    with open('data_dict.json', 'w') as f:
        json.dump(data_dict, f,  indent=4)