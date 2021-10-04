###############################################################
# Fuctions in this script is used to assign user input value  # 
# to the data dictionary in order to fill the i-821D Form.    #
# This is Part 5 INPUT                                        #
###############################################################
from datetime import datetime

def get_language_assist(data_dict): 
    qlines = '''
    Can you read and understand English, and have read and 
    understand each and every question and instruction 
    on this form, as well as your answer to each question.
    (Yes/No)
    '''
    read_english = input(qlines)
    if read_english in ['Yes','yes','Y','y']: 
        data_dict["form1[0].#subform[4].P6_Line1a_1b_Checkbox[1]"] = True
        data_dict["form1[0].#subform[4].P6_Line1a_1b_Checkbox[0]"] = False
    else: 
        qlines = '''
        Has an interpreter read to you each and 
        every question and instruction on this form, 
        as well as your answer to each questions? (Yes/No)
        '''
        need_interpreter = input(qlines)
        if need_interpreter in ['Yes','yes','Y','y']: 
            data_dict["form1[0].#subform[4].P6_Line1a_1b_Checkbox[1]"] = False
            data_dict["form1[0].#subform[4].P6_Line1a_1b_Checkbox[0]"] = True
            
            language = input("What language the interpreter read to you?")
            data_dict["form1[0].#subform[4].P6_Line1b_Language[0]"] = language
        else: 
            raise KeyError(f"Language selection is invalid.")
            
    return data_dict

def get_requestor_info(data_dict): 
    sign_date = datetime.today().strftime("%m/%d/%Y")
    data_dict["form1[0].#subform[4].P6_Line2b_Date[0]"] = sign_date
    
    phone_num = input("Enter Requestor's Daytime Telephone Number")
    data_dict["form1[0].#subform[4].P6_Line3_DayPhone[0]"] = phone_num
    
    mobile_num = input("Enter Requestor's Mobile Telephone Number")
    data_dict["form1[0].#subform[4].P6_Line4_MobilePhone[0]"] = mobile_num
    
    email_address = input("Enter Requestor's Email Address")
    data_dict["form1[0].#subform[4].P6_Line5_Email[0]"] = email_address
    
    return data_dict
