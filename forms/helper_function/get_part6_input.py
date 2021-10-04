###############################################################
# Fuctions in this script is used to assign user input value  # 
# to the data dictionary in order to fill the i-821D Form.    #
# This is Part 6 INPUT                                        #
###############################################################
from datetime import datetime

def get_interpreter_name(data_dict):
    lname = input("Enter Interpreter's Family Name")
    data_dict["form1[0].#subform[4].P7_Line1a_Name[0]"] = lname
    
    fname = input("Enter Interpreter's First Name")
    data_dict["form1[0].#subform[4].P7_Line1b_Name[0]"] = fname
    
    organization = input('''Enter Interpreter's Business or Organization Name (if any)''')
    data_dict["form1[0].#subform[4].P7_Line2_Organization[0]"] = organization
    
    return data_dict

def get_interpreter_mail_address(data_dict):
    str_name = input("Enter Street Number and Name")
    data_dict["form1[0].#subform[4].P7_Line3a_Street[0]"] = str_name
    
    apt_ste_flr = input('''Is it an apartment, suite or floor? 
    (Apt./Ste./Flr.) Press Enter to continue''')
    if apt_ste_flr in ['apt','apt.','Apt','Apt.']:
        data_dict["form1[0].#subform[4].P7_Line3b_Unit[2]"] = True
        data_dict["form1[0].#subform[4].P7_Line3b_Unit[1]"] = False
        data_dict["form1[0].#subform[4].P7_Line3b_Unit[0]"] = False
        
    elif apt_ste_flr in ['suite','Suite','Ste.', 'Ste','ste','ste.']:
        data_dict["form1[0].#subform[4].P7_Line3b_Unit[0]"] = True
        data_dict["form1[0].#subform[4].P7_Line3b_Unit[2]"] = False
        data_dict["form1[0].#subform[4].P7_Line3b_Unit[1]"] = False
        
    elif apt_ste_flr in ['Floor','floor','Flr.','flr.', 'Flr','flr','Fl.','Fl','fl.', 'fl']:
        data_dict["form1[0].#subform[4].P7_Line3b_Unit[1]"] = True
        data_dict["form1[0].#subform[4].P7_Line3b_Unit[0]"] = False
        data_dict["form1[0].#subform[4].P7_Line3b_Unit[2]"] = False
        
    else:
        data_dict["form1[0].#subform[4].P7_Line3b_Unit[0]"] = False
        data_dict["form1[0].#subform[4].P7_Line3b_Unit[1]"] = False
        data_dict["form1[0].#subform[4].P7_Line3b_Unit[2]"] = False
        
    if len(apt_ste_flr)>0: 
        apt_ste_flr_num = input("Enter Apartment, Suite or Floor No. ")
        data_dict["form1[0].#subform[4].P7_Line3b_Number[0]"] = apt_ste_flr_num
    else:
        data_dict["form1[0].#subform[4].P7_Line3b_Number[0]"] = ""
        
    city_nm = input("Enter the City or Town:")
    data_dict["form1[0].#subform[4].P7_Line3c_City[0]"] = city_nm
    
    state_nm = input("Enter the State Abbriviation: (eg. CA)")
    if len(state_nm) > 0 : 
        data_dict["form1[0].#subform[4].P7_Line3d_State[0]"] = state_nm.upper()
    
    zipcode_nm = input("Enter the zipcode: ")
    if len(zipcode_nm) > 0: 
        data_dict["form1[0].#subform[4].P7_Line3e_ZipCode[0]"] = zipcode_nm
    
    if len(state_nm) == 0: 
        province = input("Enter Province")
        data_dict["form1[0].#subform[4].P7_Line3f_Province[0]"] = province
    
    if len(zipcode_nm) == 0: 
        postal_code = input("Enter Postal Code")
        data_dict["form1[0].#subform[4].P7_Line3g_PostalCode[0]"] = postal_code
    
    country = input("Enter Country")
    data_dict["form1[0].#subform[4].P7_Line3h_Country[0]"] = country
    
    return data_dict
        
def get_interpreter_contact(data_dict):
    day_phone = input("Enter Interpreter's Daytime Telephone Number")
    data_dict["form1[0].#subform[4].P7_Line4_DayPhone[0]"] = day_phone
    
    email_address = input("Enter Interpreter's Email Address")
    data_dict["form1[0].#subform[4].P7_Line5_Email[0]"] = email_address
    
    return data_dict

def get_interpreter_cert(data_dict):
    language = input('''Enter the language the interpreter has read to 
    the requestor each and every question and instruction on this form, 
    as well as the answer to each quetsion.''')
    data_dict["form1[0].#subform[5].P7_Language[0]"] = language
    
    sign_date = datetime.today().strftime("%m/%d/%Y")
    data_dict["form1[0].#subform[5].P7_Line6b_Date[0]"] = sign_date
    
    return data_dict