import os
import re

#import fitz  # requires fitz, PyMuPDF
import pdfrw
import subprocess
import os.path
import sys

'''
MAIN ONE
https://akdux.com/python/2020/10/31/python-fill-pdf-files.html

OTHERS
https://medium.com/@zwinny/filling-pdf-forms-in-python-the-right-way-eb9592e03dba
https://medium.com/@vivsvaan/filling-editable-pdf-in-python-76712c3ce99
https://www.blog.pythonlibrary.org/2018/05/22/filling-pdf-forms-with-python/
https://yoongkang.com/blog/pdf-forms-with-python/


https://stackoverflow.com/questions/10476265/batch-fill-pdf-forms-from-python-or-bash
https://stackoverflow.com/questions/1890570/how-can-i-auto-populate-a-pdf-form-in-django-python
https://stackoverflow.com/questions/52448560/how-to-fill-pdf-forms-using-python
https://stackoverflow.com/questions/17742042/how-to-fill-pdf-form-in-python

'''


ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'


def fill_pdf(input_pdf_path, output_pdf_path, data_dict):
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    for page in template_pdf.pages:
        annotations = page[ANNOT_KEY]
        for annotation in annotations:
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY][1:-1]
                    if key in data_dict.keys():
                        if type(data_dict[key]) == bool:
                            if data_dict[key] == True:
                                annotation.update(pdfrw.PdfDict(
                                    AS=pdfrw.PdfName('Yes')))
                        else:
                            annotation.update(
                                pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                            )
                            annotation.update(pdfrw.PdfDict(AP=''))
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)



# NEW
def fill_simple_pdf_file(
        data,
        template_input,
        template_output
):

    some_date = date.today()

    data_dict = {
        'name': data.get('name', ''),
        'phone': data.get('phone', ''),
        'date': some_date,
        'account_number': data.get('account_number', ''),
        'cb_1': data.get('cb_1', False),
        'cb_2': data.get('cb_2', False),
    }

    return fill_pdf(template_input, template_output, data_dict)


if __name__ == '__main__':

    HelperUtils.initLogging()
    logging.info("-----start filer-----")

    #pdf_template = sys.path[0] + '/../../forms/daca/i-821d.pdf'
    pdf_template = './daca/i-821d_test-unlocked.pdf'

    template_pdf = pdfrw.PdfReader(pdf_template)
    print(template_pdf)

    pdf_output = "./daca/pdf_temp/output.pdf"

    data_dict = {
        #"form1[0].#subform[0].G28_Attached[0]": "",
        #"form1[0].#subform[0].#area[0].AttyLicenseNum[0]": "",
        "form1[0].#subform[0].P1_Line3a_Name[0]": "Fang",
        "form1[0].#subform[0].P1_Line3b_Name[0]": "Jiaqi",
        #"form1[0].#subform[0].P1_Line3c_Name[0]": "",
        "form1[0].#subform[0].P1_Line2b_Date[0]": "01/31/2022",
        "form1[0].#subform[0].P1_Line1_2a_Checkbox[0]": False, 
        "form1[0].#subform[0].P1_Line1_2a_Checkbox[1]": True,
        #"form1[0].#subform[0].P1_Line4a_Name[0]": "",
        "form1[0].#subform[0].P1_Line4b_Street[0]": "39967 Waxwing Drive",
        #"form1[0].#subform[0].P1_Line4c_Number[0]": "",
        #"form1[0].#subform[0].P1_Line4c_Unit[0]":"",
        #"form1[0].#subform[0].P1_Line4c_Unit[1]": "",
        #"form1[0].#subform[0].P1_Line4c_Unit[2]": "",
        "form1[0].#subform[0].P1_Line5_Checkbox[0]": False,
        "form1[0].#subform[0].P1_Line5_Checkbox[1]": True,
        "form1[0].#subform[0].P1_Line5a_Checkbox[0]": False, 
        "form1[0].#subform[0].P1_Line5b_Checkbox[0]": False,
        "form1[0].#subform[0].P1_Line5c_Checkbox[0]": False, 
        "form1[0].#subform[0].P1_Line5d_Checkbox[0]": False,
        #"form1[0].#subform[0].P1_Line5g_Location[0]": "",
        #"form1[0].#subform[0].P1_Line5f_Date[0]": "",
        "form1[0].#subform[0].P1_Line5e_Checkbox[0]": False,
        "form1[0].#subform[0].P1_Line4f_ZipCode[0]": '94560',
        "form1[0].#subform[0].P1_Line4e_State[0]": 'CA',
        "form1[0].#subform[0].P1_Line4d_City[0]": 'Newark'
        #"form1[0].#subform[0].PDF417BarCode1[0]":""
    }
    
    fill_pdf(pdf_template, pdf_output, data_dict)
