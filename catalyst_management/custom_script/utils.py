import frappe
import json
import datetime
from frappe.utils import getdate

def frozen_validate_posting_date(doc,method):
    dd = frappe.db.sql(f"""  select
                                 valid_till,
                                 role
                             from `tabFrozen data child` 
                             where doctypes = '{doc.doctype}'  
                         """,as_dict=1)
    session_user_roles = frappe.get_roles(frappe.session.user)
    if dd != []:
        if dd[0]['valid_till'] <= getdate(doc.posting_date) and dd[0]['role'] not in session_user_roles:
            frappe.throw(f"You're Frozen Date is exceeding for <b>{doc.doctype}</b>.<br> log in with user have role <b>{dd[0]['role']}</b> ")



def frozen_validate_transaction_date(doc,method):
    dd = frappe.db.sql(f"""  select
                                 valid_till,
                                 role
                             from `tabFrozen data child` 
                             where doctypes = '{doc.doctype}'  
                         """,as_dict=1)
    session_user_roles = frappe.get_roles(frappe.session.user)
    if dd != []:
        if dd[0]['valid_till'] <= getdate(doc.transaction_date) and dd[0]['role'] not in session_user_roles:
            frappe.throw(f"You're Frozen Date is exceeding for <b>{doc.doctype}</b>.<br> log in with user have role <b>{dd[0]['role']}</b> ")


