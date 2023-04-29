import frappe
import json
# import datetime
# from frappe.utils import getdate

# def frozen_validate_posting_date(doc,method):
#     dd = frappe.db.sql(f"""  select
#                                  valid_till,
#                                  role
#                              from `tabFrozen data child` 
#                              where doctypes = '{doc.doctype}'  
#                          """,as_dict=1)
#     session_user_roles = frappe.get_roles(frappe.session.user)
#     if dd != []:
#         if dd[0]['valid_till'] <= getdate(doc.posting_date) and dd[0]['role'] not in session_user_roles:
#             frappe.throw(f"You're Frozen Date is exceeding for <b>{doc.doctype}</b>.<br> log in with user have role <b>{dd[0]['role']}</b> ")



# def frozen_validate_transaction_date(doc,method):
#     dd = frappe.db.sql(f"""  select
#                                  valid_till,
#                                  role
#                              from `tabFrozen data child` 
#                              where doctypes = '{doc.doctype}'  
#                          """,as_dict=1)
#     session_user_roles = frappe.get_roles(frappe.session.user)
#     if dd != []:
#         if dd[0]['valid_till'] <= getdate(doc.transaction_date) and dd[0]['role'] not in session_user_roles:
#             frappe.throw(f"You're Frozen Date is exceeding for <b>{doc.doctype}</b>.<br> log in with user have role <b>{dd[0]['role']}</b> ")





def tax_item_break(doc,method):
    mya = []
    for i in doc.items:
        my_dict ={}
        my_dict['item_code'] = i.item_code
        js_di = json.loads(i.item_tax_rate)
        for j in doc.taxes:
            if i.item_tax_rate and str(j.account_head) in  js_di:
                if js_di[str(j.account_head)] != None or js_di[str(j.account_head)] != '':
                    my_dict[str(j.account_head)] = f"""({js_di[str(j.account_head)]} %) {(i.amount*js_di[str(j.account_head)])/100}"""
                else:
                    my_dict[str(j.account_head)] = ''
        mya.append(my_dict)

    html = ""
    html  = html + "<table class='table table-bordered'>"
    html  = html + "<tr>"
    for key in mya[0].keys():
        html = html + f"<th>{key}</th>"
    html = html +  "</tr>"
    for row in mya:
        html  = html + "<tr>"
        for key, value in row.items():
            html = html +  f"<td>{value}</td>"
        html = html +  "</tr>"
    html = html +  "</table>"
    doc.taxes_and_charges_calculation_based_on_item_tax_template= html

    frappe.db.commit()
    # Return the HTML code
    # frappe.throw(html)