import frappe

def before_save(doc,method):
    total_amount = sum(amt.amount_allocation for amt in doc.percentages)
    # Update grand total in Monthly Distribution
    doc.custom_grand_total = total_amount