###############################################################
# Fuctions in this script is used to assign user input value  # 
# to the data dictionary in order to fill the i-821D Form.    #
###############################################################
# import library
import datetime

# helper function
def check_date(val):
    month, day, year = val.split('/')
    
    isValidDate = True
    try:
        datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        isValidDate = False

    if(isValidDate == False):
        raise KeyError(f"Your most recent DACA expiration date {val} is not valid.")


# i-821D Form, Page 1
# Select this box if Form G-28 is attached to represetn the requestor
def get_attorney_info(data_dict):
    lines = '''To begin, are you an attorney represeting the requestor? 
    (Yes/No)
    '''
    g28_answer = input(lines)
    
    if g28_answer in ['Yes','y','Y','yes']:
        # check the g-28 checkbox
        data_dict["form1[0].#subform[0].G28_Attached[0]"]= True
        
        # get the attorney state bar number
        bar_num = input("Enter your Attorney State Bar Number: ")
        data_dict["form1[0].#subform[0].#area[0].AttyLicenseNum[0]"] = bar_num
        
    else: 
        data_dict["form1[0].#subform[0].G28_Attached[0]"]= False
        data_dict["form1[0].#subform[0].#area[0].AttyLicenseNum[0]"] = ""
        
    return data_dict

# Part1, question 1 and 2: initial request or renewal request
def get_initial_renewal(data_dict):
    request_type = input('''Are you requesting Initial Request or Renewal? 
    (Initial/Renewal)''')
    
    if request_type in ['Initial','initial','I','i']:
        data_dict["form1[0].#subform[0].P1_Line1_2a_Checkbox[0]"] = True
        data_dict["form1[0].#subform[0].P1_Line2b_Date[0]"] = ""
        
    elif request_type in ['Renewal','Renew', 'renewal','renew','R','r']:
        daca_expire_date = input('''When is your most recent period of DACA expiration date? 
        (mm/dd/yyyy)''')
        # unit test
        check_date(daca_expire_date)
        
        data_dict["form1[0].#subform[0].P1_Line1_2a_Checkbox[1]"] = True
        data_dict["form1[0].#subform[0].P1_Line2b_Date[0]"] = daca_expire_date
        
    else: 
        raise KeyError(f"i-821D form is for Initial or Renewal Request. Please check if this is the right form for you")
    return data_dict

# Part 1, section 3, Full Legal Name
def get_legal_name(data_dict):
    lname = input("Enter your Last Name")
    fname = input("Enter your First Name")
    mname = input('''Enter your Middle Name. 
    Press ENTER to escapte.''')
    
    data_dict["form1[0].#subform[0].P1_Line3a_Name[0]"] = lname
    data_dict["form1[0].#subform[0].P1_Line3b_Name[0]"] = fname
    data_dict["form1[0].#subform[0].P1_Line3c_Name[0]"] = mname
    
    return data_dict

# Part1, Item 4: Mailing Address
def get_mail_address(data_dict):
    incare_name = input('''Enter the In Care of Name. 
    Press ENTER to escape if not applicable''')
    data_dict["form1[0].#subform[0].P1_Line4a_Name[0]"] = incare_name
    
    str_name = input("Enter Street Number and Name")
    data_dict["form1[0].#subform[0].P1_Line4b_Street[0]"] = str_name
    
    apt_ste_flr = input('''Is it an apartment, suite or floor? 
    (Apt./Ste./Flr.) Press Enter to continue''')
    
    if apt_ste_flr in ['apt','apt.','Apt','Apt.']:
        data_dict["form1[0].#subform[0].P1_Line4c_Unit[2]"] = True
        data_dict["form1[0].#subform[0].P1_Line4c_Unit[1]"] = False
        data_dict["form1[0].#subform[0].P1_Line4c_Unit[0]"] = False
        
    elif apt_ste_flr in ['suite','Suite','Ste.', 'Ste','ste','ste.']:
        data_dict["form1[0].#subform[0].P1_Line4c_Unit[1]"] = True
        data_dict["form1[0].#subform[0].P1_Line4c_Unit[2]"] = False
        data_dict["form1[0].#subform[0].P1_Line4c_Unit[0]"] = False
        
    elif apt_ste_flr in ['Floor','floor','Flr.','flr.', 'Flr','flr','Fl.','Fl','fl.', 'fl']:
        data_dict["form1[0].#subform[0].P1_Line4c_Unit[0]"] = True
        data_dict["form1[0].#subform[0].P1_Line4c_Unit[2]"] = False
        data_dict["form1[0].#subform[0].P1_Line4c_Unit[1]"] = False
        
    else:
        data_dict["form1[0].#subform[0].P1_Line4c_Unit[0]"] = False
        data_dict["form1[0].#subform[0].P1_Line4c_Unit[2]"] = False
        data_dict["form1[0].#subform[0].P1_Line4c_Unit[1]"] = False
    
    if len(apt_ste_flr)>0: 
        apt_ste_flr_num = input("Enter Apartment, Suite or Floor No. ")
        data_dict["form1[0].#subform[0].P1_Line4c_Number[0]"] = apt_ste_flr_num
    else:
        data_dict["form1[0].#subform[0].P1_Line4c_Number[0]"] = ""
    
    city_nm = input("Enter the City or Town:")
    data_dict["form1[0].#subform[0].P1_Line4d_City[0]"] = city_nm
    
    state_nm = input("Enter the State Abbriviation: (eg. CA)")
    data_dict["form1[0].#subform[0].P1_Line4e_State[0]"] = state_nm.upper()
        
    zipcode_nm = input("Enter the zipcode: ")
    data_dict["form1[0].#subform[0].P1_Line4f_ZipCode[0]"] = zipcode_nm
    
    return data_dict

# Part 1, item 5: Removal Proceedings Information
def get_removal_proceeding(data_dict):
    q5lines = '''Are you Now or have you EVER been in removal proceedings, 
    or do you have a removal order issued in other context?"
    (Yes/No)
    '''
    removal_ind = input(q5lines)
    if removal_ind in ['No','no','N','n']:
        data_dict["form1[0].#subform[0].P1_Line5_Checkbox[1]"] = True
        data_dict["form1[0].#subform[0].P1_Line5_Checkbox[0]"] = False
        
        data_dict["form1[0].#subform[0].P1_Line5a_Checkbox[0]"] = False
        data_dict["form1[0].#subform[0].P1_Line5b_Checkbox[0]"] = False
        data_dict["form1[0].#subform[0].P1_Line5c_Checkbox[0]"] = False
        data_dict["form1[0].#subform[0].P1_Line5d_Checkbox[0]"] = False
        data_dict["form1[0].#subform[0].P1_Line5e_Checkbox[0]"] = False
        
        data_dict["form1[0].#subform[0].P1_Line5f_Date[0]"] = ""
        data_dict["form1[0].#subform[0].P1_Line5g_Location[0]"] = ""
        
    elif removal_ind in ['Yes','yes','Y','y']:
        data_dict["form1[0].#subform[0].P1_Line5_Checkbox[0]"] = True
        data_dict["form1[0].#subform[0].P1_Line5_Checkbox[1]"] = False
        
        lines = '''If you answered "Yes", you must select one of the below
        indicating your current status or outcome of your removal proceedings.
        
        Enter one of the following code if applicable: 
        - Currently in Proceedings: Enter 5a
        - Currently in Proceedings: Enter 5b
        - Terminated: Enter 5c
        - Subject to a Final Order: Enter 5d
        - Other: Enter 5e
        '''
        removal_reason = input(lines)
        if removal_reason == '5a':
            data_dict["form1[0].#subform[0].P1_Line5a_Checkbox[0]"] = True
            data_dict["form1[0].#subform[0].P1_Line5b_Checkbox[0]"] = False
            data_dict["form1[0].#subform[0].P1_Line5c_Checkbox[0]"] = False
            data_dict["form1[0].#subform[0].P1_Line5d_Checkbox[0]"] = False
            data_dict["form1[0].#subform[0].P1_Line5e_Checkbox[0]"] = False
        elif removal_reason == '5b':
            data_dict["form1[0].#subform[0].P1_Line5a_Checkbox[0]"] = False
            data_dict["form1[0].#subform[0].P1_Line5b_Checkbox[0]"] = True
            data_dict["form1[0].#subform[0].P1_Line5c_Checkbox[0]"] = False
            data_dict["form1[0].#subform[0].P1_Line5d_Checkbox[0]"] = False
            data_dict["form1[0].#subform[0].P1_Line5e_Checkbox[0]"] = False
        elif removal_reason == '5c':
            data_dict["form1[0].#subform[0].P1_Line5a_Checkbox[0]"] = False
            data_dict["form1[0].#subform[0].P1_Line5b_Checkbox[0]"] = False
            data_dict["form1[0].#subform[0].P1_Line5c_Checkbox[0]"] = True
            data_dict["form1[0].#subform[0].P1_Line5d_Checkbox[0]"] = False
            data_dict["form1[0].#subform[0].P1_Line5e_Checkbox[0]"] = False  
        elif removal_reason == '5d':
            data_dict["form1[0].#subform[0].P1_Line5a_Checkbox[0]"] = False
            data_dict["form1[0].#subform[0].P1_Line5b_Checkbox[0]"] = False
            data_dict["form1[0].#subform[0].P1_Line5c_Checkbox[0]"] = False
            data_dict["form1[0].#subform[0].P1_Line5d_Checkbox[0]"] = True
            data_dict["form1[0].#subform[0].P1_Line5e_Checkbox[0]"] = False
        elif removal_reason == '5e':
            data_dict["form1[0].#subform[0].P1_Line5a_Checkbox[0]"] = False
            data_dict["form1[0].#subform[0].P1_Line5b_Checkbox[0]"] = False
            data_dict["form1[0].#subform[0].P1_Line5c_Checkbox[0]"] = False
            data_dict["form1[0].#subform[0].P1_Line5d_Checkbox[0]"] = False
            data_dict["form1[0].#subform[0].P1_Line5e_Checkbox[0]"] = True            
        else: 
            raise KeyError(f"You must select one of the status")
            
        proceed_date = input('''Enter the Most Recent Date of Proceedings. 
        (mm/dd/yyyy)''')
        # unit test
        check_date(proceed_date)
        data_dict["form1[0].#subform[0].P1_Line5f_Date[0]"] = proceed_date
        
        proceed_loc = input("Location of Proceedings")
        data_dict["form1[0].#subform[0].P1_Line5g_Location[0]"] = proceed_loc
    
    return data_dict