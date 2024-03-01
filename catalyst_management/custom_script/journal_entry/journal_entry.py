import frappe
from frappe import _
from datetime import date
from datetime import datetime # from python std library
from frappe.utils import add_to_date
from frappe.utils import (
	now_datetime, getdate, formatdate
)


def before_save(doc, methode):
    pass
    # for account in doc.accounts:
    #     result= frappe.db.get_list('Budget Account Mapping',{'parent':account.project,'budget_account_head':account.budget_account_head,'chart_of_account_head':account.account},['parent', 'budget_account_head', 'chart_of_account_head','custom_party_type','custom_party'])
    #     for i in result:
    #         account.custom_member_type = i.custom_party_type
    #         account.custom_member = i.custom_party
           

def validate(doc, method):
    if doc.workflow_state:
        if (doc.workflow_state == 'Send For Review'):
            doc.custom_prepared_on = doc.modified
        elif (doc.workflow_state == 'Send For Approval'):
            doc.custom_reviewed_on = doc.modified
        elif (doc. workflow_state == 'Approved'):
            doc.custom_approved_on = doc.modified



def validate_posting_date(doc, method):
    for item in doc.accounts:
        contract_details = frappe.db.get_list('Contract', {'party_type':item.party_type,'party_name': item.party, 'custom_project': item.project}, ['end_date','name'])
        for i in contract_details:
            if str(i.end_date) < doc.posting_date:
                if not doc.custom_reason:
                    ms =f'''
                    <a href="{frappe.utils.get_url_to_form('Contract', i.name)}">{i.name}</a>
                    ''' 
                    frappe.throw(frappe._("Contract has been Expired. Last Date is {0}. If you want to proceed then select reason. Contract is {1}.").format(formatdate(i.end_date), ms))   



def calculate_items_amount(doc, method):
    total_amount = 0
    for amt in doc.accounts:
        if amt.custom_report_type == 'Profit and Loss':
            total_amount += amt.debit_in_account_currency
    

        project_budgeting_amount = frappe.db.get_all("Project Budgeting", filters={"name": amt.project_for_budget}, fields=["custom_grand_total","custom_total_actual_amount","name"])
        for pd in project_budgeting_amount:
             doc.custom_total_amount = pd.custom_total_actual_amount +  total_amount
             doc.custom_total_amount_from_project_budget = pd.custom_total_actual_amount
             doc.custom_total_amount_from_invoice = total_amount
             if doc.custom_total_amount > pd.custom_grand_total:
                frappe.throw(frappe._("Total Consolidated amount is greater than Grand Total"))


def update_total_actual_amount(doc, method):
    for amt in doc.accounts:
        project_budgeting_amount = frappe.db.get_all("Project Budgeting", filters={"name": amt.project_for_budget}, fields=["custom_grand_total","custom_total_actual_amount","name"])
        for pd in project_budgeting_amount:
            frappe.db.set_value("Project Budgeting", pd["name"] ,"custom_total_actual_amount" , doc.custom_total_amount)
            frappe.db.commit()
                           



    
