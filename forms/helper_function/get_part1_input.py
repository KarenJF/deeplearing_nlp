###############################################################
# Fuctions in this script is used to assign user input value  # 
# to the data dictionary in order to fill the i-821D Form.    #
# This is Part 1 INPUT                                        #
###############################################################
# import library
import datetime
import sys
from helper_function import unit_test

# i-821D Form, Part 1
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
        unit_test.check_date(daca_expire_date)
        
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
        unit_test.check_date(proceed_date)
        data_dict["form1[0].#subform[0].P1_Line5f_Date[0]"] = proceed_date
        
        proceed_loc = input("Location of Proceedings")
        data_dict["form1[0].#subform[0].P1_Line5g_Location[0]"] = proceed_loc
    
    return data_dict

# Part 1, item 6
def get_other_info(data_dict):
    
    anum = input('''Enter Alien Registration Number (if any)
    Press ENTER to escape''' )
    data_dict["form1[0].#subform[1].Line4_ANumber[0].P1_Line6_ANumber[0]"] = anum
    
    ssn_num = input('''Enter U.S SSN (if any)
    Press ENTER to escape''')
    data_dict["form1[0].#subform[1].P1_Line7_SSN[0]"] = ssn_num
    
    dob_num = input('''Enter Date of Birth 
    (mm/dd/yyyy)''')
    # unit test
    unit_test.check_date(dob_num)
    data_dict["form1[0].#subform[1].P1_Line9_DOB[0]"] = dob_num
    
    gender = input('''What's your gender?
    (Male/Female)''')
    if gender in ['Male','M','male','m']:
        data_dict["form1[0].#subform[1].P1_Line10_Gender[0]"] = True
        data_dict["form1[0].#subform[1].P1_Line10_Gender[1]"] = False
    elif gender in ['Female','female','F','f']:
        data_dict["form1[0].#subform[1].P1_Line10_Gender[1]"] = True
        data_dict["form1[0].#subform[1].P1_Line10_Gender[0]"] = False
    else:
        data_dict["form1[0].#subform[1].P1_Line10_Gender[0]"] = False
        data_dict["form1[0].#subform[1].P1_Line10_Gender[1]"] = False
        
    birthplace = input("Enter the name of your City/Town/Village of Birth")
    data_dict["form1[0].#subform[1].P1_Line11a_CityBirth[0]"] = birthplace
    
    birthcountry = input("Enter Country of Birth")
    data_dict["form1[0].#subform[1].P1_Line11b_CountryBirth[0]"] = birthcountry
    
    curr_resident = input("Enter current country of residence")
    data_dict["form1[0].#subform[1].P1_Line12_CountryRes[0]"] = curr_resident
    
    nationality = input("Enter Country of Citizenship or Nationality")
    data_dict["form1[0].#subform[1].P1_Line13_CountryCitz[0]"] = nationality
    
    maritial = input('''Marital Status
    (Married/Widowed/Single/Divorced''')
    
    if maritial in ['Married','married','M','m','marry','Marry']:
        data_dict["form1[0].#subform[1].P1_Line14_MaritalStatus[1]"] = True
        data_dict["form1[0].#subform[1].P1_Line14_MaritalStatus[3]"] = False
        data_dict["form1[0].#subform[1].P1_Line14_MaritalStatus[0]"] = False
        data_dict["form1[0].#subform[1].P1_Line14_MaritalStatus[2]"] = False
        
    elif maritial in ['Widowed','widowed','W','w']:
        data_dict["form1[0].#subform[1].P1_Line14_MaritalStatus[3]"] = True
        data_dict["form1[0].#subform[1].P1_Line14_MaritalStatus[1]"] = False
        data_dict["form1[0].#subform[1].P1_Line14_MaritalStatus[0]"] = False
        data_dict["form1[0].#subform[1].P1_Line14_MaritalStatus[2]"] = False
        
    elif maritial in ['Single','single','s','S']:
        data_dict["form1[0].#subform[1].P1_Line14_MaritalStatus[0]"] = True
        data_dict["form1[0].#subform[1].P1_Line14_MaritalStatus[1]"] = False
        data_dict["form1[0].#subform[1].P1_Line14_MaritalStatus[3]"] = False 
        data_dict["form1[0].#subform[1].P1_Line14_MaritalStatus[2]"] = False
        
    elif maritial in ['Divorced','divorced','D','d','Divorce','divorce']:
        data_dict["form1[0].#subform[1].P1_Line14_MaritalStatus[2]"] = True
        data_dict["form1[0].#subform[1].P1_Line14_MaritalStatus[1]"] = False
        data_dict["form1[0].#subform[1].P1_Line14_MaritalStatus[3]"] = False
        data_dict["form1[0].#subform[1].P1_Line14_MaritalStatus[0]"] = False
        
    else:
        data_dict["form1[0].#subform[1].P1_Line14_MaritalStatus[0]"] = False
        data_dict["form1[0].#subform[1].P1_Line14_MaritalStatus[1]"] = False
        data_dict["form1[0].#subform[1].P1_Line14_MaritalStatus[2]"] = False
        data_dict["form1[0].#subform[1].P1_Line14_MaritalStatus[3]"] = False
        
    return data_dict

# Part 1 other names used
def get_other_names(data_dict):
    other_ln = input('''Other Family Name (if any)
               Prese ENTER to escape''')
    data_dict["form1[0].#subform[1].P1_Line15a_Name[0]"] = other_ln
    
    other_fn = input('''Other First Name (if any)
                     Press ENTER to escape''')
    data_dict["form1[0].#subform[1].P1_Line15b_Name[0]"] = other_fn
    
    other_mn = input('''Other Middle Name (if any)
                     Press ENTER to escap''')
    data_dict["form1[0].#subform[1].P1_Line15c_Name[0]"] = other_mn
    
    return data_dict
    
# Part 1 Processing Information
def processing_info(data_dict):
    ethnicity = input('''What's your Ethnicity? (Select only one)
                      - Hispanic or Latino: Enter 1
                      - Not Hispanic or Latino: Enter 2''')
    if len(ethnicity) == 1: 
        if int(ethnicity) == 1:
            data_dict["form1[0].#subform[1].P2_Line1_Checkbox[1]"] = True
            data_dict["form1[0].#subform[1].P2_Line1_Checkbox[0]"] = False
        elif int(ethnicity) == 2:
            data_dict["form1[0].#subform[1].P2_Line1_Checkbox[0]"] = True
            data_dict["form1[0].#subform[1].P2_Line1_Checkbox[1]"] = False
        else:
            data_dict["form1[0].#subform[1].P2_Line1_Checkbox[1]"] = False
            data_dict["form1[0].#subform[1].P2_Line1_Checkbox[0]"] = False
    else: 
        raise KeyError(f"You must select ONLY one of the status")
        
    race = input('''Enter Race (all applicable, seperate by ,)
    - White: Enter 1
    - Asian: Enter 2
    - Black or African American: Enter 3
    - American Indian or Alaska Native: Enter 4
    - Native Hawaiian or Other Pacific Islander: Enter 5''')
    race_list = race.split(",")
    for i in race_list:
        if int(i) == 1:
            data_dict["form1[0].#subform[1].P2_Line2_Race_White[0]"] = True
        if int(i) == 2:
            data_dict["form1[0].#subform[1].P2_Line2_Race_Asian[0]"] = True
        if int(i) == 3:
            data_dict["form1[0].#subform[1].P2_Line2_Race_Black[0]"] = True
        if int(i) == 4:
            data_dict["form1[0].#subform[1].P2_Line2_Race_AmIndian[0]"] = True
        if int(i) == 5:
            data_dict["form1[0].#subform[1].P2_Line2_Race_NativeHaw[0]"] = True
    
    height_feet = input("Enter Feet")
    data_dict["form1[0].#subform[1].P2_Line3_Height-Ft[0]"] = height_feet
    
    height_inch = input("Enter inches")
    data_dict["form1[0].#subform[1].P2_Line3_Height-In[0]"] = height_inch
    
    weight = input("Enter weight")
    weight_num = round(float(weight))
    weight_str = str(weight_num)
    
    position = 0
    if len(weight_str) == 3:
        for i in weight_str:
            if position == 0: 
                data_dict["form1[0].#subform[1].P2_Line4_Weight[0]"] = i
                position+=1
            elif position == 1:
                data_dict["form1[0].#subform[1].P2_Line4_Weight[1]"] = i
                position+=1
            else:
                data_dict["form1[0].#subform[1].P2_Line4_Weight[2]"] = i

    if len(weight_str) == 2:
        data_dict["form1[0].#subform[1].P2_Line4_Weight[0]"] = ""
        for i in weight_str:
            if positin == 0:
                data_dict["form1[0].#subform[1].P2_Line4_Weight[1]"] = i
                position+=1
            else:
                data_dict["form1[0].#subform[1].P2_Line4_Weight[2]"] = i
    
    eyecolor = input('''Enter Eye Color (Only one)
    - Black: Enter 1
    - Blue: Enter 2
    - Brown: Enter 3
    - Grey: Enter 4
    - Green: Enter 5
    - Hazel: Enter 6
    - Maroon: Enter 7
    - Pink: Enter 8
    - Unknown/Other: Enter 9''')
    
    if len(eyecolor) == 1: 
        if int(eyecolor) == 1:
            data_dict["form1[0].#subform[1].P2_Line5_Checkbox[7]"] = True
        if int(eyecolor) == 2:
            data_dict["form1[0].#subform[1].P2_Line5_Checkbox[0]"] = True
        if int(eyecolor) == 3:
            data_dict["form1[0].#subform[1].P2_Line5_Checkbox[6]"] = True
        if int(eyecolor) == 4:
            data_dict["form1[0].#subform[1].P2_Line5_Checkbox[1]"] = True
        if int(eyecolor) == 5:
            data_dict["form1[0].#subform[1].P2_Line5_Checkbox[5]"] = True
        if int(eyecolor) == 6: 
            data_dict["form1[0].#subform[1].P2_Line5_Checkbox[2]"] = True
        if int(eyecolor) == 7: 
            data_dict["form1[0].#subform[1].P2_Line5_Checkbox[4]"] = True
        if int(eyecolor) == 8: 
            data_dict["form1[0].#subform[1].P2_Line5_Checkbox[3]"] = True
        if int(eyecolor) == 9: 
            data_dict["form1[0].#subform[1].P2_Line5_Checkbox[8]"] = True
    else: 
        raise KeyError(f"You must select ONLY one of the status")
        
    haircolor = input('''Enter Hair Color (Only one)
    - Bald (No hair): Enter 1
    - Black: enter 2
    - Blond: enter 3
    - Brown: enter 4
    - Grey: enter 5
    - Red: enter 6
    - Sandy: enter 7
    - White: enter 8
    - Unknown/Other: enter 9''')
    
    if len(haircolor) == 1: 
        if int(haircolor) == 1:
            data_dict["form1[0].#subform[1].P2_Line6_Checkbox[0]"] = True
        if int(haircolor) == 2: 
            data_dict["form1[0].#subform[1].P2_Line6_Checkbox[8]"] = True
        if int(haircolor) == 3: 
            data_dict["form1[0].#subform[1].P2_Line6_Checkbox[1]"] = True
        if int(haircolor) == 4: 
            data_dict["form1[0].#subform[1].P2_Line6_Checkbox[7]"] = True
        if int(haircolor) == 5: 
            data_dict["form1[0].#subform[1].P2_Line6_Checkbox[2]"] = True
        if int(haircolor) == 6: 
            data_dict["form1[0].#subform[1].P2_Line6_Checkbox[6]"] = True
        if int(haircolor) == 7: 
            data_dict["form1[0].#subform[1].P2_Line6_Checkbox[3]"] = True
        if int(haircolor) == 8: 
            data_dict["form1[0].#subform[1].P2_Line6_Checkbox[5]"] = True
        if int(haircolor) == 9: 
            data_dict["form1[0].#subform[1].P2_Line6_Checkbox[4]"] = True
    else: 
        raise KeyError(f"You must select ONLY one of the status")
    
    return data_dict
    
    
    