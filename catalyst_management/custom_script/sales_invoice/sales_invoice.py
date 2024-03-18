import frappe
from frappe import _
from datetime import date
from datetime import datetime # from python std library
from frappe.utils import add_to_date
from frappe.utils import (
	now_datetime, getdate, formatdate
)
import json

def validate(doc, method):
    if doc.workflow_state:
        if (doc.workflow_state == 'Send For Review'):
            doc.custom_prepared_on = doc.modified
        elif (doc.workflow_state == 'Send For Approval'):
            doc.custom_reviewed_on = doc.modified
        elif (doc. workflow_state == 'Approved'):
            doc.custom_approved_on = doc.modified



@frappe.whitelist()
def update_chart_of_account(doc):
    doc = json.loads(doc)
    for d in doc.get('items'):
        result = frappe.db.get_all('Budget Account Mapping', {'parent':d.get('project'),'budget_account_head':d.get('budget_account_head')}, ['chart_of_account_head'])
        result_dict = {}
        for d in result:
            for key, value in d.items():
                result_dict[key] = value
    return result_dict.get('chart_of_account_head')      

# Posting date validate according to contract end date 

def validate_posting_date(doc, method):
    for item in doc.items:
        contract_details = frappe.db.get_list('Contract', {'party_name': doc.customer, 'custom_project': item.project}, ['end_date','name', 'custom_amount'])
        for i in contract_details:
            if str(i.end_date) < str(doc.posting_date):
                if not doc.custom_reason:
                    ms =f'''
                    <a href="{frappe.utils.get_url_to_form('Contract', i.name)}">{i.name}</a>
                    '''
                    frappe.throw(frappe._("Contract has been Expired. Last Date is {0}.If you want to proceed then select reason. If needed kindly access the Contract here - {1}.").format(formatdate(i.end_date), ms))   


def calculate_items_amount(doc, method):
    for item in doc.items: 
        project_budgeting_amount = frappe.db.get_all("Project Budgeting", filters={"name": item.project_for_budget}, fields=["custom_grand_total","custom_total_actual_amount","name"])
        for pb in project_budgeting_amount:
            if doc.custom_total_amount > pb.custom_grand_total: 
                ms =f'''
                    <a href="{frappe.utils.get_url_to_form('Project Budgeting', pb.name)}">{pb.name}</a>
                    ''' 
                frappe.throw(frappe._("Total Consolidated Amount is greater than Project Budget Grand Total. If needed kindly access the Project Budget here - {0}.").format(ms))

def update_project_budget_actual_amount(doc, method):
    for item in doc.items: 
        project_budgeting_amount = frappe.db.get_all("Project Budgeting", filters={"name": item.project_for_budget}, fields=["custom_grand_total","custom_total_actual_amount","name"])
        for pb in project_budgeting_amount:
            frappe.db.set_value("Project Budgeting", pb["name"] ,"custom_total_actual_amount" , doc.custom_total_amount)
            frappe.db.commit()  

def calculate_item_details(self, method):
    item_details = {}

    # Grouping items by item code and HSN code and calculating total amount
    for item in self.items:
        key = (item.project_budget,item.budget_account_head)
        if key in item_details:
            item_details[key] += item.amount
        else:
            item_details[key] = item.amount

    # Clear existing item details
    self.set("custom_item_details", [])
    # Adding grouped item details to the new child table
    for key, amount in item_details.items():
        project_budget,budget_account_head = key
        self.append("custom_item_details", {
            "current_invoice_amount": amount,
            "project_budget": project_budget,
            "budget_account_head":budget_account_head,
        })

def calculate_budget_account_head_amount_actual(self, method):
    if self.custom_item_details:
        for item in self.custom_item_details:
            project_budgeting_amount = frappe.db.get_all("Budget Account Mapping", filters={"parent": item.project_budget, "budget_account_head":item.budget_account_head}, fields=["custom_total_amount", "amount", "parent"])
            for pb in project_budgeting_amount:
                item.total_budget_account_head_amount_actual = pb.custom_total_amount
                item.total_consolidated_budget_account_head_amount = item.current_invoice_amount + pb.custom_total_amount
                if pb.amount < item.total_consolidated_budget_account_head_amount:
                    ms =f'''
                    <a href="{frappe.utils.get_url_to_form('Project Budgeting', pb.parent)}">{pb.parent}</a>
                    '''
                    frappe.throw(frappe._("Total Consolidated Budget Account Head Amount is greater than Budget Account Mapping Amount. If needed kindly access the Project Budget here - {0}.").format(ms))

def update_budget_account_mapping_amount(self, method):
    if self.custom_item_details:
        for item in self.custom_item_details: 
            project_budgeting_amount = frappe.db.get_all("Budget Account Mapping", filters={"parent": item.project_budget, "budget_account_head":item.budget_account_head}, fields=["custom_total_amount", "name"])
            for pb in project_budgeting_amount:
                frappe.db.set_value("Budget Account Mapping", pb["name"] ,"custom_total_amount" , item.total_consolidated_budget_account_head_amount)
                frappe.db.commit()                   

