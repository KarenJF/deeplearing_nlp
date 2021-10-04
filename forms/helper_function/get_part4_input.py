###############################################################
# Fuctions in this script is used to assign user input value  # 
# to the data dictionary in order to fill the i-821D Form.    #
# This is Part 4 INPUT                                        #
###############################################################

def get_arrested_felony(data_dict):
    qlines = '''
    Have you EVER been arrested for, charged with, or
    convicted of a felony or misdemeanor, including incidents
    handled in juvenile court, in the United States? Do not
    include minor traffic violations unless they were alcoholor
    drug-related. (Yes/No)
    '''
    arrested_ind = input(qlines)
    if arrested_ind in ['Yes','yes','Y','y']:
        data_dict["form1[0].#subform[3].P5_Line1_Checkbox[0]"] = True
        data_dict["form1[0].#subform[3].P5_Line1_Checkbox[1]"] = False
    elif arrested_ind in ['No','no','N','n']:
        data_dict["form1[0].#subform[3].P5_Line1_Checkbox[1]"] = True
        data_dict["form1[0].#subform[3].P5_Line1_Checkbox[0]"] = False
    else:
        data_dict["form1[0].#subform[3].P5_Line1_Checkbox[0]"] = False
        data_dict["form1[0].#subform[3].P5_Line1_Checkbox[1]"] = False
    
    return data_dict

def get_crime_outside(data_dict):
    qlines = '''
    Have you EVER been arrested for, charged with, or
    convicted of a crime in any country other than the United
    States? (Yes/No)
    '''
    crime_outside = input(qlines)
    if crime_outside in ['Yes','yes','Y','y']:
        data_dict["form1[0].#subform[3].P5_Line2_Checkbox[0]"] = True
        data_dict["form1[0].#subform[3].P5_Line2_Checkbox[1]"] = False
    elif crime_outside in ['No','no','N','n']:
        data_dict["form1[0].#subform[3].P5_Line2_Checkbox[1]"] = True
        data_dict["form1[0].#subform[3].P5_Line2_Checkbox[0]"] = False
    else: 
        data_dict["form1[0].#subform[3].P5_Line2_Checkbox[0]"] = False
        data_dict["form1[0].#subform[3].P5_Line2_Checkbox[1]"] = False
        
    return data_dict

def get_engage_terrorist(data_dict):
    qlines = '''
    Have you EVER engaged in, do you continue to engage
    in, or plan to engage in terrorist activities? (Yes/No)
    '''
    terrorist_ind = input(qlines)
    if terrorist_ind in ['Yes','yes','Y','y']:
        data_dict["form1[0].#subform[3].P5_Line3_Checkbox[1]"] = True
        data_dict["form1[0].#subform[3].P5_Line3_Checkbox[0]"] = False
    elif terrorist_ind in ['No','no','N','n']:
        data_dict["form1[0].#subform[3].P5_Line3_Checkbox[0]"] = True
        data_dict["form1[0].#subform[3].P5_Line3_Checkbox[1]"] = False
    else: 
        data_dict["form1[0].#subform[3].P5_Line3_Checkbox[0]"] = False
        data_dict["form1[0].#subform[3].P5_Line3_Checkbox[1]"] = False
        
    return data_dict
        
def get_gang(data_dict):
    qlines = '''
    Are you NOW or have you EVER been a member of a
    gang? (Yes/No)
    '''
    
    gang_ind = input(qlines)
    if gang_ind in ['Yes','yes','Y','y']: 
        data_dict["form1[0].#subform[3].P5_Line4_Checkbox[1]"] = True
        data_dict["form1[0].#subform[3].P5_Line4_Checkbox[0]"] = False
    elif gang_ind in ['No','no','N','n']:
        data_dict["form1[0].#subform[3].P5_Line4_Checkbox[0]"] = True
        data_dict["form1[0].#subform[3].P5_Line4_Checkbox[1]"] = False
    else: 
        data_dict["form1[0].#subform[3].P5_Line4_Checkbox[0]"] = False
        data_dict["form1[0].#subform[3].P5_Line4_Checkbox[1]"] = False
        
    return data_dict
        
def get_activities_5a(data_dict):
    qlines = '''
    Have you EVER engaged in, ordered, incited, assisted, 
    or otherwise participated in torture, genocide, 
    or human trafficking? (Yes/No)
    '''
    torture_ind = input(qlines)
    if torture_ind in ['Yes','yes','Y','y']:
        data_dict["form1[0].#subform[3].P5_Line5a_Checkbox[0]"] = True
        data_dict["form1[0].#subform[3].P5_Line5a_Checkbox[1]"] = False
    elif torture_ind in ['No','no','N','n']:
        data_dict["form1[0].#subform[3].P5_Line5a_Checkbox[1]"] = True
        data_dict["form1[0].#subform[3].P5_Line5a_Checkbox[0]"] = False
    else:
        data_dict["form1[0].#subform[3].P5_Line5a_Checkbox[0]"] = False
        data_dict["form1[0].#subform[3].P5_Line5a_Checkbox[1]"] = False
        
    return data_dict

def get_activities_5b(data_dict): 
    qlines = '''Killing any person? (Yes/No)
    '''
    kill_ind = input(qlines)
    if kill_ind in ['Yes','yes','Y','y']:
        data_dict["form1[0].#subform[3].P5_Line5b_Checkbox[0]"] = True
        data_dict["form1[0].#subform[3].P5_Line5b_Checkbox[1]"] = False
    elif kill_ind in ['No','no','N','n']:
        data_dict["form1[0].#subform[3].P5_Line5b_Checkbox[1]"] = True
        data_dict["form1[0].#subform[3].P5_Line5b_Checkbox[0]"] = False
    else: 
        data_dict["form1[0].#subform[3].P5_Line5b_Checkbox[0]"] = False
        data_dict["form1[0].#subform[3].P5_Line5b_Checkbox[1]"] = False
        
    return data_dict
        
def get_activities_5c(data_dict):
    qlines = "Severely injuring any person? (Yes/No)"
    
    injure_ind = input(qlines)
    if injure_ind in ['Yes','yes','Y','y']:
        data_dict["form1[0].#subform[3].P5_Line5c_Checkbox[0]"] = True
        data_dict["form1[0].#subform[3].P5_Line5c_Checkbox[1]"] = False
    elif injure_ind in ['No','no','N','n']:
        data_dict["form1[0].#subform[3].P5_Line5c_Checkbox[1]"] = True
        data_dict["form1[0].#subform[3].P5_Line5c_Checkbox[0]"] = False
    else: 
        data_dict["form1[0].#subform[3].P5_Line5c_Checkbox[0]"] = False
        data_dict["form1[0].#subform[3].P5_Line5c_Checkbox[1]"] = False
    
    return data_dict

def get_activities_5d(data_dict):
    qlines = '''
    Any kind of sexual contact or relations with any person
    who was being forced or threatened? (Yes/No)
    '''
    
    force_ind = input(qlines)
    if force_ind in ['Yes','yes','Y','y']:
        data_dict["form1[0].#subform[3].P5_Line5d_Checkbox[0]"] = True
        data_dict["form1[0].#subform[3].P5_Line5d_Checkbox[1]"] = False
    elif force_ind in ['No','no','N','n']:
        data_dict["form1[0].#subform[3].P5_Line5d_Checkbox[1]"] = True
        data_dict["form1[0].#subform[3].P5_Line5d_Checkbox[0]"] = False
    else: 
        data_dict["form1[0].#subform[3].P5_Line5d_Checkbox[0]"] = False
        data_dict["form1[0].#subform[3].P5_Line5d_Checkbox[1]"] = False
    
    return data_dict    

def get_activities_6(data_dict):
    qlines = '''
    Have you EVER recruited, enlisted, conscripted, or used 
    any person to serve in or help an armed force or group 
    while such person was under age 15? (Yes/No)
    '''
    recruit_15_ind = input(qlines)
    if recruit_15_ind in ['Yes','yes','Y','y']:
        data_dict["form1[0].#subform[3].P5_Line6_Checkbox[1]"] = True
        data_dict["form1[0].#subform[3].P5_Line6_Checkbox[0]"] = False
    elif recruit_15_ind in ['No','no','N','n']:
        data_dict["form1[0].#subform[3].P5_Line6_Checkbox[0]"] = True
        data_dict["form1[0].#subform[3].P5_Line6_Checkbox[1]"] = False
    else: 
        data_dict["form1[0].#subform[3].P5_Line6_Checkbox[0]"] = False
        data_dict["form1[0].#subform[3].P5_Line6_Checkbox[1]"] = False
    return data_dict

def get_activities_7(data_dict):
    qlines = '''
    Have you EVERN used any person under age 15 to take
    part in hostilities, or to help or provide services to people
    in combat? (Yes/No)
    '''
    use_15_ind = input(qlines)
    if use_15_ind in ['Yes','yes','Y','y']:
        data_dict["form1[0].#subform[3].P5_Line7_Checkbox[1]"] = True
        data_dict["form1[0].#subform[3].P5_Line7_Checkbox[0]"] = False
    elif use_15_ind in ['No','no','N','n']:
        data_dict["form1[0].#subform[3].P5_Line7_Checkbox[0]"] = True
        data_dict["form1[0].#subform[3].P5_Line7_Checkbox[1]"] = False
    else: 
        data_dict["form1[0].#subform[3].P5_Line7_Checkbox[0]"] = False
        data_dict["form1[0].#subform[3].P5_Line7_Checkbox[1]"] = False
        
    return data_dict
        
    
        