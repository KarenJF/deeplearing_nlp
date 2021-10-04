import os
import re

#import fitz  # requires fitz, PyMuPDF
import pdfrw
import subprocess
import os.path
import sys
import json

'''
Best link: 
https://westhealth.github.io/exploring-fillable-forms-with-pdfrw.html

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

ANNOT_KEY = '/Annots'           # key for all annotations within a page
ANNOT_FIELD_KEY = '/T'          # Name of field. i.e. given ID of field
ANNOT_FORM_type = '/FT'         # Form type (e.g. text/button)
ANNOT_FORM_flag = '/Ff'         # Form flag
ANNOT_FORM_button = '/Btn'      # ID for buttons, i.e. a checkbox
ANNOT_FORM_text = '/Tx'         # ID for textbox
ANNOT_FORM_choice = '/Ch'       # ID for choice box
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'
PARENT_KEY = '/Parent'

barcode_list = ['form1[0].#subform[0].PDF417BarCode1[0]',
                'form1[0].#subform[1].PDF417BarCode1[1]',
                'form1[0].#subform[2].PDF417BarCode1[2]',
                'form1[0].#subform[3].PDF417BarCode1[3]',
                'form1[0].#subform[4].PDF417BarCode1[4]',
                'form1[0].#subform[5].PDF417BarCode1[5]',
                'form1[0].#subform[6].PDF417BarCode1[6]']

# update text section
def text_form(annotation, value):
    annotation.update(pdfrw.PdfDict(V='{}'.format(value)))
    annotation.update(pdfrw.PdfDict(AP=''))
    
    # The following two codes only works in Adobe PDF, not work on MAC Preview
    #pdfstr = pdfrw.objects.pdfstring.PdfString.encode(value) 
    #annotation.update(pdfrw.PdfDict(V=pdfstr, AS=pdfstr))

# update choice box section
def combobox(annotation, value):
    export = None
    for each in annotation['/Opt']:
        if each[1].to_unicode() == value:
            export = each[0].to_unicode()
    if export is None: 
        raise KeyError(f"Export Value: {value} Not Found")
        
    annotation.update(pdfrw.PdfDict(V='{}'.format(export), AS='{}'.format(export)))
    annotation.update(pdfrw.PdfDict(AP=''))
    
    # The following two codes only works in Adobe PDF, not work on MAC Preview
    #pdfstr = pdfrw.objects.pdfstring.PdfString.encode(export)
    #annotation.update(pdfrw.PdfDict(V=pdfstr, AS=pdfstr))

# update checkbox section
def checkbox(annotation, key_value, export=None):
    if export:
        export = '/' + export
    else:
        keys = annotation['/AP']['/N'].keys()
        if '/Off' in keys:
            keys.remove('/Off')
        export = keys[0]
    if key_value:
        annotation.update(pdfrw.PdfDict(V=export, AS=export))
    else:
        del annotation['/V']
        del annotation['/AS']

# update list box section
def listbox(annotation, values):
    pdfstrs=[]
    for value in values:
        export=None
        for each in annotation['/Opt']:
            if each[1].to_unicode()==value:
                export = each[0].to_unicode()
        if export is None:
            raise KeyError(f"Export Value: {value} Not Found")
    
    pdfstrs.append(pdfrw.objects.pdfstring.PdfString.encode(export))
    annotation.update(pdfrw.PdfDict(V=pdfstrs, AS=pdfstrs))

# update radio button section
def radio_button(annotation, value):
    for each in annotation['/Kids']:
        # determine the export value of each kid
        keys = each['/AP']['/N'].keys()
        keys.remove('/Off')
        export = keys[0]

        if f'/{value}' == export:
            val_str = pdfrw.objects.pdfname.BasePdfName(f'/{value}')
        else:
            val_str = pdfrw.objects.pdfname.BasePdfName(f'/Off')
        each.update(pdfrw.PdfDict(AS=val_str))

    annotation.update(pdfrw.PdfDict(V=pdfrw.objects.pdfname.BasePdfName(f'/{value}')))
        
def fill_pdf(input_pdf_path, output_pdf_path, data_dict):
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    
    for page in template_pdf.pages:
        annotations = page[ANNOT_KEY]
        if annotations is None:
            continue

        for annotation in annotations:
            ft = annotation[ANNOT_FORM_type]
            ff = annotation[ANNOT_FORM_flag]
            if annotation[SUBTYPE_KEY]==WIDGET_SUBTYPE_KEY:
                if not annotation[ANNOT_FIELD_KEY]:
                    annotation=annotation[PARENT_KEY]
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY].to_unicode()
                    if key in barcode_list:
                        continue 
                    
                    if key in data_dict.keys():
                        #print("Key: ", key)
                        #print("data_dict_value: ", data_dict[key])
                        if ft == ANNOT_FORM_button: # fill checkbox
                            if ff and int(ff) & 1 << 15:
                                radio_button(annotation, data_dict[key])
                            else:
                                #print(annotation['/AP']['/N'].keys())
                                checkbox(annotation, data_dict[key], export=None)
                    
                        if annotation[ANNOT_FORM_type] == ANNOT_FORM_text: # fill text
                            text_form(annotation, data_dict[key])
                        
                        if ft == ANNOT_FORM_choice: # fill combo choice
                            if ff and int(ff) & 1 << 17:
                                combobox(annotation, data_dict[key])
                            else: 
                                listbox(annotation, data_dict[key])
                                
                        
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)

if __name__ == '__main__':

    #HelperUtils.initLogging()
    #logging.info("-----start filer-----")

    #pdf_template = sys.path[0] + '/../../forms/daca/i-821d.pdf'
    # set empty i-821D form 
    pdf_template = './daca/i-821d_test-unlocked.pdf'
    template_pdf = pdfrw.PdfReader(pdf_template)
    #print(template_pdf)

    # set output filled pdf location
    pdf_output = "./daca/pdf_temp/output_test_auto.pdf"
    
    # load the data_dictionary from saved scripts
    with open('data_dict.json', 'r') as f:
        data_dict = json.load(f)
        
    fill_pdf(pdf_template, pdf_output, data_dict)
