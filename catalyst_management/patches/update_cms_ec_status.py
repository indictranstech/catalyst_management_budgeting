import frappe

all_expense_claim =  ['HR-EXP-2023-00035-1','HR-EXP-2023-00007-3','HR-EXP-2023-00007-2','HR-EXP-2023-00035']



def execute():
    alldoc = frappe.get_all('Expense Claim',{'name':['in',all_expense_claim]},['status', 'name', 'is_paid', 'docstatus'])
    for data in alldoc:
        if data.is_paid == 1 and data.status == 'Paid' and data.docstatus == 2:
            frappe.db.sql("update `tabExpense Claim` set status = '{0}' where name = '{1}'".format('Cancelled', data.name))
