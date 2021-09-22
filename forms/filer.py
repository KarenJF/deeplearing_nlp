import logging
import sys

import pdfrw
from datetime import date

from utils import HelperUtils

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
    pdf_template = sys.path[0] + '/daca/i-821d.pdf'

    template_pdf = pdfrw.PdfReader(pdf_template)
    print(template_pdf)

    pdf_output = "output.pdf"

    '''
    sample_data_dict = {
        'name': 'Andrew Krcatovich',
        'phone': '(123) 123-1234',
        #         'date': date.today(),  # Removed date so we can dynamically set in python.
        'account_number': '123123123',
        'cb_1': True,
        'cb_2': False,
    }

    fill_simple_pdf_file(
        sample_data_dict,
        pdf_template,
        pdf_output
    )
    '''