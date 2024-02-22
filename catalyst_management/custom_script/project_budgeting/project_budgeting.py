import frappe

def before_save(doc,method):
    total_amount = sum(amt.amount for amt in doc.budget_account_mapping)
    doc.custom_grand_total = total_amount


def update_grand_total(doc, method):
    total_amount = sum(amt.amount for amt in doc.budget_account_mapping)
    frappe.db.set_value('Project Budgeting', doc.name, 'custom_grand_total', total_amount)    
    


