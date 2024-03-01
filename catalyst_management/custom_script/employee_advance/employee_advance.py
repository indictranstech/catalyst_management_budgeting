import frappe
from frappe import _
from datetime import date
from datetime import datetime # from python std library
from frappe.utils import add_to_date
from frappe.utils import (
	now_datetime, getdate, formatdate
)

def validate(doc, method):
    if doc.workflow_state:
        if (doc.workflow_state == 'Send For Review'):
            doc.custom_prepared_on = doc.modified
        elif (doc.workflow_state == 'Send For Approval'):
            doc.custom_reviewed_on = doc.modified
        elif (doc. workflow_state == 'Approved'):
            doc.custom_approved_on = doc.modified

def validate_posting_date(doc, method):
        contract_details = frappe.db.get_list('Contract', {'party_name': doc.employee, 'custom_project': doc.project}, ['end_date','name'])
        for i in contract_details:
            if str(i.end_date) < doc.posting_date:
                if not doc.custom_reason:
                    ms =f'''
                    <a href="{frappe.utils.get_url_to_form('Contract', i.name)}">{i.name}</a>
                    ''' 
                    frappe.throw(frappe._("Contract has been Expired. Last Date is {0}. If you want to proceed then select reason.Contract is {1}.").format(formatdate(i.end_date), ms))   



