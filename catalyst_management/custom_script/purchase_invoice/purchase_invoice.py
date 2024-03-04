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

    
def update_chart_of_account(doc, methode):
    for item in doc.items:
        result= frappe.db.get_all('Budget Account Mapping',{'parent':item.project,'budget_account_head':item.budget_account_head,},['chart_of_account_head'])
        for i in result:
            item.expense_account = i.chart_of_account_head
      

# Posting date validate according to contract end date 

def validate_posting_date(doc, method):
    for item in doc.items:
        contract_details = frappe.db.get_list('Contract', {'party_name': doc.supplier, 'custom_project': item.project}, ['end_date','name'])
        for i in contract_details:
            if str(i.end_date) < str(doc.posting_date):
                if not doc.custom_reason:
                    ms =f'''
                    <a href="{frappe.utils.get_url_to_form('Contract', i.name)}">{i.name}</a>
                    ''' 
                    frappe.throw(frappe._("Contract has been Expired. Last Date is {0}. If you want to proceed then select reason. Contract is {1}.").format(formatdate(i.end_date), ms))



def calculate_items_amount(doc, method):
    for item in doc.items: 
        project_budgeting_amount = frappe.db.get_all("Project Budgeting", filters={"name": item.project_for_budget}, fields=["custom_grand_total","custom_total_actual_amount","name"])
        for pb in project_budgeting_amount:
            if doc.custom_total_amount > pb.custom_grand_total: 
                frappe.throw(frappe._("Total Consolidated Amount is greater than Grand Total."))

def update_total_actual_amount(doc, method):
    for item in doc.items: 
        project_budgeting_amount = frappe.db.get_all("Project Budgeting", filters={"name": item.project_for_budget}, fields=["custom_grand_total","custom_total_actual_amount","name"])
        for pb in project_budgeting_amount:
                frappe.db.set_value("Project Budgeting", pb["name"] ,"custom_total_actual_amount" , doc.custom_total_amount)
                frappe.db.commit()    




