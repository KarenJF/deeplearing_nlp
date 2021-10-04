###############################################################
# Fuctions in this script is used to assign user input value  # 
# to the data dictionary in order to fill the i-821D Form.    #
# This is Part 2 INPUT                                        #
###############################################################
from helper_function import unit_test

# i-821D Form, Part 2
def get_residing(data_dict): 
    reside_ind = input('''Have you been continuously residing in the US
    since at least June 15, 2007,
    up to the present time. (Yes/No)''')

    if reside_ind in ['Yes','yes','Y','y']:
        data_dict["form1[0].#subform[1].P3_Line1b_checkbox[0]"] = True
        data_dict["form1[0].#subform[1].P3_Line1b_checkbox[1]"] = False
    elif reside_ind in ['No','no','N','n']:
        data_dict["form1[0].#subform[1].P3_Line1b_checkbox[1]"] = True
        data_dict["form1[0].#subform[1].P3_Line1b_checkbox[0]"] = False
    else: 
        data_dict["form1[0].#subform[1].P3_Line1b_checkbox[0]"] = False
        data_dict["form1[0].#subform[1].P3_Line1b_checkbox[1]"] = False
        
    return data_dict

def get_present_address(data_dict):
    present_from_date = input('''When you start living in this residence?
    (mm//dd/yyyy)''')
    unit_test.check_date(present_from_date)
    data_dict["form1[0].#subform[2].P3_Line2a_Date_From[0]"] = present_from_date
    
    present_str_name = input("Enter Street Number and Name")
    data_dict["form1[0].#subform[2].P3_Line2b_Street[0]"] = present_str_name
    
    present_apt_ste_flr = input('''Is it an apartment, suite or floor? 
    (Apt./Ste./Flr.) Press Enter to continue''')
    if present_apt_ste_flr in ['apt','apt.','Apt','Apt.']:
        data_dict["form1[0].#subform[2].P3_Line2c_Unit[2]"] = True
        data_dict["form1[0].#subform[2].P3_Line2c_Unit[1]"] = False
        data_dict["form1[0].#subform[2].P3_Line2c_Unit[0]"] = False
    elif present_apt_ste_flr in ['suite','Suite','Ste.', 'Ste','ste','ste.']:
        data_dict["form1[0].#subform[2].P3_Line2c_Unit[1]"] = True
        data_dict["form1[0].#subform[2].P3_Line2c_Unit[2]"] = False
        data_dict["form1[0].#subform[2].P3_Line2c_Unit[0]"] = False
    elif present_apt_ste_flr in ['Floor','floor','Flr.','flr.', 'Flr','flr','Fl.','Fl','fl.', 'fl']: 
        data_dict["form1[0].#subform[2].P3_Line2c_Unit[0]"] = True
        data_dict["form1[0].#subform[2].P3_Line2c_Unit[1]"] = False
        data_dict["form1[0].#subform[2].P3_Line2c_Unit[2]"] = False
    else: 
        data_dict["form1[0].#subform[2].P3_Line2c_Unit[0]"] = False
        data_dict["form1[0].#subform[2].P3_Line2c_Unit[1]"] = False
        data_dict["form1[0].#subform[2].P3_Line2c_Unit[2]"] = False
        
    if len(present_apt_ste_flr)>0: 
        present_apt_ste_flr_num = input("Enter Apartment, Suite or Floor No. ")
        data_dict["form1[0].#subform[2].P3_Line2c_Number[0]"] = present_apt_ste_flr_num
        
    present_city_nm = input("Enter Present City or Town:")
    data_dict["form1[0].#subform[2].P3_Line2d_City[0]"] = present_city_nm
    
    present_state_nm = input("Enter the State Abbriviation: (eg. CA)") 
    data_dict["form1[0].#subform[2].P3_Line2e_State[0]"] = present_state_nm
    
    present_zipcode_nm = input("Enter Present zipcode: ") 
    data_dict["form1[0].#subform[2].Pt2Line2f_ZipCode[0]"] = present_zipcode_nm
    
    return data_dict, present_from_date

def get_prior_address1(data_dict, present_from_date):
    prior1_from_date = input('''Previous Address 1: From date at this residence.
    (mm//dd/yyyy)''')
    # if there is a previous address, do the following
    if len(prior1_from_date)>0:
        unit_test.check_date(prior1_from_date)
        data_dict["form1[0].#subform[2].P3_Line3a_Date_From[0]"] = prior1_from_date
    
        prior1_to_date = present_from_date
        unit_test.check_date(prior1_to_date)
        data_dict["form1[0].#subform[2].P3_Line3a_Date_To[0]"] = prior1_to_date
    
        prior1_str_name = input("Enter Street Number and Name")
        data_dict["form1[0].#subform[2].P3_Line3b_Street[0]"] = prior1_str_name
    
        prior1_apt_ste_flr = input('''Is it an apartment, suite or floor? 
        (Apt./Ste./Flr.) Press Enter to continue''')
        if prior1_apt_ste_flr in ['apt','apt.','Apt','Apt.']:
            data_dict["form1[0].#subform[2].P3_Line3c_Unit[2]"] = True
            data_dict["form1[0].#subform[2].P3_Line3c_Unit[1]"] = False
            data_dict["form1[0].#subform[2].P3_Line3c_Unit[0]"] = False
        elif prior1_apt_ste_flr in ['suite','Suite','Ste.', 'Ste','ste','ste.']:
            data_dict["form1[0].#subform[2].P3_Line3c_Unit[1]"] = True
            data_dict["form1[0].#subform[2].P3_Line3c_Unit[2]"] = False
            data_dict["form1[0].#subform[2].P3_Line3c_Unit[0]"] = False
        elif prior1_apt_ste_flr in ['Floor','floor','Flr.','flr.', 'Flr','flr','Fl.','Fl','fl.', 'fl']: 
            data_dict["form1[0].#subform[2].P3_Line3c_Unit[0]"] = True
            data_dict["form1[0].#subform[2].P3_Line3c_Unit[1]"] = False
            data_dict["form1[0].#subform[2].P3_Line3c_Unit[2]"] = False
        else: 
            data_dict["form1[0].#subform[2].P3_Line3c_Unit[0]"] = False
            data_dict["form1[0].#subform[2].P3_Line3c_Unit[1]"] = False
            data_dict["form1[0].#subform[2].P3_Line3c_Unit[2]"] = False
        
        if len(prior1_apt_ste_flr)>0: 
            prior1_apt_ste_flr_num = input("Enter Apartment, Suite or Floor No. ")
            data_dict["form1[0].#subform[2].P3_Line3c_Number[0]"] = prior1_apt_ste_flr_num
        
        prior1_city_nm = input("Enter City or Town:")
        data_dict["form1[0].#subform[2].P3_Line3d_City[0]"] = prior1_city_nm
    
        prior1_state_nm = input("Enter the State Abbriviation: (eg. CA)") 
        data_dict["form1[0].#subform[2].P3_Line3e_State[0]"] = prior1_state_nm
    
        prior1_zipcode_nm = input("Enter zipcode: ") 
        data_dict["form1[0].#subform[2].Pt2Line3f_ZipCode[0]"] = prior1_zipcode_nm
    
    return data_dict, prior1_from_date

def get_prior_address2(data_dict, prior1_from_date):
    prior2_from_date = input('''Previous Address 2: Enter From date at this residence.
    (mm//dd/yyyy)''')
    # if there is a previous address, do the following
    if len(prior2_from_date)>0: 
        unit_test.check_date(prior2_from_date)
        data_dict["form1[0].#subform[2].P3_Line4a_Date_From[0]"] = prior2_from_date
    
        prior2_to_date = prior1_from_date
        unit_test.check_date(prior2_to_date)
        data_dict["form1[0].#subform[2].P3_Line4a_Date_To[0]"] = prior2_to_date
    
        prior2_str_name = input("Enter Street Number and Name")
        data_dict["form1[0].#subform[2].P3_Line4b_Street[0]"] = prior2_str_name
    
        prior2_apt_ste_flr = input('''Is it an apartment, suite or floor? 
        (Apt./Ste./Flr.) Press Enter to continue''')
        if prior2_apt_ste_flr in ['apt','apt.','Apt','Apt.']:
            data_dict["form1[0].#subform[2].P3_Line4c_Unit[2]"] = True
            data_dict["form1[0].#subform[2].P3_Line4c_Unit[1]"] = False
            data_dict["form1[0].#subform[2].P3_Line4c_Unit[0]"] = False
        elif prior2_apt_ste_flr in ['suite','Suite','Ste.', 'Ste','ste','ste.']:
            data_dict["form1[0].#subform[2].P3_Line4c_Unit[1]"] = True
            data_dict["form1[0].#subform[2].P3_Line4c_Unit[2]"] = False
            data_dict["form1[0].#subform[2].P3_Line4c_Unit[0]"] = False
        elif prior2_apt_ste_flr in ['Floor','floor','Flr.','flr.', 'Flr','flr','Fl.','Fl','fl.', 'fl']: 
            data_dict["form1[0].#subform[2].P3_Line4c_Unit[0]"] = True
            data_dict["form1[0].#subform[2].P3_Line4c_Unit[1]"] = False
            data_dict["form1[0].#subform[2].P3_Line4c_Unit[2]"] = False
        else: 
            data_dict["form1[0].#subform[2].P3_Line4c_Unit[0]"] = False
            data_dict["form1[0].#subform[2].P3_Line4c_Unit[1]"] = False
            data_dict["form1[0].#subform[2].P3_Line4c_Unit[2]"] = False
        
        if len(prior2_apt_ste_flr)>0: 
            prior2_apt_ste_flr_num = input("Enter Apartment, Suite or Floor No. ")
            data_dict["form1[0].#subform[2].P3_Line4c_Number[0]"] = prior2_apt_ste_flr_num
        
        prior2_city_nm = input("Enter City or Town:")
        data_dict["form1[0].#subform[2].P3_Line4d_City[0]"] = prior2_city_nm
    
        prior2_state_nm = input("Enter the State Abbriviation: (eg. CA)") 
        data_dict["form1[0].#subform[2].P3_Line4e_State[0]"] = prior2_state_nm
    
        prior2_zipcode_nm = input("Enter zipcode: ") 
        data_dict["form1[0].#subform[2].Pt2Line4f_ZipCode[0]"] = prior2_zipcode_nm
    
    return data_dict, prior2_from_date
        
def get_prior_address3(data_dict, prior2_from_date):
    prior3_from_date = input('''Previous Address 3: Enter From date at this residence.
    (mm//dd/yyyy)''')
    # if there is a previous address, do the following
    if len(prior3_from_date)>0: 
        unit_test.check_date(prior3_from_date)
        data_dict["form1[0].#subform[2].P3_Line5a_Date_From[0]"] = prior3_from_date
    
        prior3_to_date = prior2_from_date
        unit_test.check_date(prior3_to_date)
        data_dict["form1[0].#subform[2].P3_Line5a_Date_To[0]"] = prior3_to_date
    
        prior3_str_name = input("Enter Street Number and Name")
        data_dict["form1[0].#subform[2].P3_Line5b_Street[0]"] = prior3_str_name
    
        prior3_apt_ste_flr = input('''Is it an apartment, suite or floor? 
        (Apt./Ste./Flr.) Press Enter to continue''')
        if prior3_apt_ste_flr in ['apt','apt.','Apt','Apt.']:
            data_dict["form1[0].#subform[2].P3_Line5c_Unit[2]"] = True
            data_dict["form1[0].#subform[2].P3_Line5c_Unit[1]"] = False
            data_dict["form1[0].#subform[2].P3_Line5c_Unit[0]"] = False
        elif prior3_apt_ste_flr in ['suite','Suite','Ste.', 'Ste','ste','ste.']:
            data_dict["form1[0].#subform[2].P3_Line5c_Unit[1]"] = True
            data_dict["form1[0].#subform[2].P3_Line5c_Unit[2]"] = False
            data_dict["form1[0].#subform[2].P3_Line5c_Unit[0]"] = False
        elif prior3_apt_ste_flr in ['Floor','floor','Flr.','flr.', 'Flr','flr','Fl.','Fl','fl.', 'fl']: 
            data_dict["form1[0].#subform[2].P3_Line5c_Unit[0]"] = True
            data_dict["form1[0].#subform[2].P3_Line5c_Unit[1]"] = False
            data_dict["form1[0].#subform[2].P3_Line5c_Unit[2]"] = False
        else: 
            data_dict["form1[0].#subform[2].P3_Line5c_Unit[0]"] = False
            data_dict["form1[0].#subform[2].P3_Line5c_Unit[1]"] = False
            data_dict["form1[0].#subform[2].P3_Line5c_Unit[2]"] = False
        
        if len(prior3_apt_ste_flr)>0: 
            prior3_apt_ste_flr_num = input("Enter Apartment, Suite or Floor No. ")
            data_dict["form1[0].#subform[2].P3_Line5c_Number[0]"] = prior3_apt_ste_flr_num
        
        prior3_city_nm = input("Enter City or Town:")
        data_dict["form1[0].#subform[2].P3_Line5d_City[0]"] = prior3_city_nm
    
        prior3_state_nm = input("Enter the State Abbriviation: (eg. CA)") 
        data_dict["form1[0].#subform[2].P3_Line5e_State[0]"] = prior3_state_nm
    
        prior3_zipcode_nm = input("Enter zipcode: ") 
        data_dict["form1[0].#subform[2].Pt2Line5f_ZipCode[0]"] = prior3_zipcode_nm
    
    return data_dict, prior3_from_date

def get_travel1(data_dict):
    depart_date1 = input("Depart 1: Departure Date (mm/dd/yyyy)")
    # if travel, do following
    if len(depart_date1) > 0: 
        unit_test.check_date(depart_date1)
        data_dict["form1[0].#subform[2].P4_Line1a_DepDate[0]"] = depart_date1
    
        return_date1 = input("Reture Date (mm/dd/yyyy)")
        unit_test.check_date(return_date1)
        data_dict["form1[0].#subform[2].P4_Line1b_RetDate[0]"] = return_date1
    
        depart_reason1 = input("Reason for Departure")
        data_dict["form1[0].#subform[2].P4_Line1c_Reason[0]"] = depart_reason1
    
    return data_dict

def get_travel2(data_dict):
    depart_date2 = input("Depart 2: Departure Date (mm/dd/yyyy)")
    # if travel, do following
    if len(depart_date2) > 0: 
        unit_test.check_date(depart_date2)
        data_dict["form1[0].#subform[2].P4_Line2a_DeptDate[0]"] = depart_date2
    
        return_date2 = input("Reture Date (mm/dd/yyyy)")
        unit_test.check_date(return_date2)
        data_dict["form1[0].#subform[2].P4_Line2b_RetDate[0]"] = return_date2
    
        depart_reason2 = input("Reason for Departure")
        data_dict["form1[0].#subform[2].P4_Line2c_Reason[0]"] = depart_reason2
    
    return data_dict

def get_without_advance_parole(data_dict):
    no_advance_parole = input('''Have you left the United States
    without advance parole on or after 8/15/2021
    (Yes/No)''')
    if no_advance_parole in ['Yes','yes','Y','y']:
        data_dict["form1[0].#subform[2].P4_Line3_Checkbox[0]"] = True
    elif no_advance_parole in ['No','no','N','n']:
        data_dict["form1[0].#subform[2].P4_Line3_Checkbox[1]"] = True
    else: 
        data_dict["form1[0].#subform[2].P4_Line3_Checkbox[0]"] = False
        data_dict["form1[0].#subform[2].P4_Line3_Checkbox[1]"] = False
        
    return data_dict

def get_passport(data_dict):
    passport_country = input("What country issued your last passport?")
    data_dict["form1[0].#subform[2].P4_Line4a_Country[0]"] = passport_country
    
    passport_num = input("Passport Number")
    data_dict["form1[0].#subform[2].P4_Line4b_Passport[0]"] = passport_num
    
    passport_expire_date = input('''Passport Expiration Date
    (mm/dd/yyyy)''')
    unit_test.check_date(passport_expire_date)
    data_dict["form1[0].#subform[2].P4_Line4c_ExpDate[0]"] = passport_expire_date
    
    return data_dict

def get_border_card_num(data_dict):
    border_card = input("Border Crossing Card Number (if any)")
    data_dict["form1[0].#subform[2].P4_Line5_BorderCard[0]"] = border_card
    
    return data_dict


