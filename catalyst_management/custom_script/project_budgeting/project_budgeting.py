import frappe

def before_save(doc,method):
    total_amount = sum(amt.amount for amt in doc.budget_account_mapping)

    # Updated grand total in project budgeting
    doc.custom_grand_total = total_amount