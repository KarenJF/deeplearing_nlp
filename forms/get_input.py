import os
import re

import pdfrw
import subprocess
import os.path
import sys
import json
from importlib import reload 
from helper_function import get_part1_input
from helper_function import get_part2_input
from helper_function import get_part4_input
from helper_function import get_part5_input
from helper_function import get_part6_input
from helper_function import get_part7_input
# only use to reload the helper function
reload(get_part1_input)


## Goal: Asking User input to update the data dictionary
def get_part1(data_dict):
    # Question: To be completed by an Attorney?
    data_dict = get_part1_input.get_attorney_info(data_dict)

    # Part 1-1,1-2
    data_dict = get_part1_input.get_initial_renewal(data_dict)
        
    # Part1, Item 3: Full Legal Name
    data_dict = get_part1_input.get_legal_name(data_dict)

    # Part1, Item 4: Mailing Address
    data_dict = get_part1_input.get_mail_address(data_dict)

    # Part1, Item 5: Removal Proceedings
    data_dict = get_part1_input.get_removal_proceeding(data_dict)
    
    # Part1, Other_info
    data_dict = get_part1_input.get_other_info(data_dict)

    # Part1, other name
    data_dict = get_part1_input.get_other_names(data_dict)
    
    # Part1, Processing Info
    data_dict = get_part1_input.processing_info(data_dict)
    
    return data_dict

def get_part2(data_dict):
    # Part 2, Residing status
    data_dict = get_part2_input.get_residing(data_dict)
    
    # Part 2, Present Address
    data_dict, present_from_date = get_part2_input.get_present_address(data_dict)
    
    # Part 2, Privious Address 1
    data_dict, prior1_from_date = get_part2_input.get_prior_address1(data_dict,present_from_date)
    
    # Part 2, Privious Address 2
    data_dict, prior2_from_date = get_part2_input.get_prior_address2(data_dict,prior1_from_date)
    
    # Part 2, Previous Address 3
    data_dict, prior3_from_date = get_part2_input.get_prior_address3(data_dict, prior2_from_date)
    
    # Part 2, Departure 1
    data_dict = get_part2_input.get_travel1(data_dict)
    
    # Part 2, Departure 2
    data_dict = get_part2_input.get_travel2(data_dict)
    
    # Part 2, No Advance Parole status
    data_dict = get_part2_input.get_without_advance_parole(data_dict)
    
    # Part 2, Passport Number
    data_dict = get_part2_input.get_passport(data_dict)
    
    # Part 2, border crossing card
    data_dict = get_part2_input.get_border_card_num(data_dict)
    
    return data_dict
    
def get_part4(data_dict):
    # Part 4, arrested
    data_dict = get_part4_input.get_arrested_felony(data_dict)
    
    # Part 4, crime outside US
    data_dict = get_part4_input.get_crime_outside(data_dict)
    
    # Part 4, engaged in terrorist
    data_dict = get_part4_input.get_engage_terrorist(data_dict)
    
    # Part 4, gang member
    data_dict = get_part4_input.get_gang(data_dict)
    
    # Part 4, engaged activities
    data_dict = get_part4_input.get_activities_5a(data_dict)
    data_dict = get_part4_input.get_activities_5b(data_dict)
    data_dict = get_part4_input.get_activities_5c(data_dict)
    data_dict = get_part4_input.get_activities_5d(data_dict)
    data_dict = get_part4_input.get_activities_6(data_dict)
    data_dict = get_part4_input.get_activities_7(data_dict)
    
    return data_dict

def get_part5(data_dict): 
    # Part 5 read and understand English
    data_dict = get_part5_input.get_language_assist(data_dict)

    # Part 5, Requestor's certification
    data_dict = get_part5_input.get_requestor_info(data_dict)
    
    return data_dict
    
def get_part6(data_dict): 
    # Part 6, interpreter name
    data_dict = get_part6_input.get_interpreter_name(data_dict)
    
    # Part 6, interpreter mailing address
    data_dict = get_part6_input.get_interpreter_mail_address(data_dict)
    
    # Part 6, interpreter contact
    data_dict = get_part6_input.get_interpreter_contact(data_dict)
    
    # Part 6, interpreter's certification
    data_dict = get_part6_input.get_interpreter_cert(data_dict)
    
    return data_dict

def get_part7(data_dict): 
    data_dict, status = get_part7_input.get_preparer_status(data_dict)
    
    if status == True: # continue to fill out if it's true
        # Part 7, preparer's full name
        data_dict = get_part7_input.get_preparer_name(data_dict)
        
        # Part 7, Preparer's Mailing Address
        data_dict = get_part7_input.get_preparer_mail_address(data_dict)
        
        # Part 7, Preparer's Contact Information
        data_dict = get_part7_input.get_preparer_contact(data_dict)
        
        # Part 7, Preparer's Declaration
        data_dict = get_part7_input.get_preparer_cert(data_dict)
        
    return data_dict
    
    
if __name__ == '__main__':
    # Step 1: Create empty dictionary
    data_dict = dict()
    
    # Step 2: Get Part 1 Input
    print("Thank you for using FillMeForms! Let's begin to fill out the DACA form")
    data_dict = get_part1(data_dict)
    
    # Step 3: Get Part 2 Input
    data_dict = get_part2(data_dict)
    
    # Step 4: Get Part 4 Input
    data_dict = get_part4(data_dict)
    
    # Step 5: Get Part 5 Input
    data_dict = get_part5(data_dict)
    
    # Step 6: Get Part 6 Input
    data_dict = get_part6(data_dict)
    
    # Step 7: Get Part 7 Input
    data_dict = get_part7(data_dict)
    
    # Step 8: Save the data dictionary
    with open('data_dict.json', 'w') as f:
        json.dump(data_dict, f,  indent=4)