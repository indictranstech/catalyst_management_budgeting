import frappe

all_expense_claim =  ['VL/EXP/23-24/10/0008','VL/EXP/23-24/07/0040-5','VL/EXP/23-24/07/0040-4','VL/EXP/23-24/07/0040-3','VL/EXP/23-24/07/0040-2','VL/EXP/23-24/07/0040-1','VL/EXP/23-24/07/0040','VF/EXP/23-24/05/0022-4','VF/EXP/23-24/05/0022-3','VF/EXP/23-24/05/0022-2','VF/EXP/23-24/05/0022-1','VF/EXP/23-24/05/0022']



def execute():
    alldoc = frappe.get_all('Expense Claim',{'name':['in',all_expense_claim]},['status', 'name', 'is_paid', 'docstatus'])
    for data in alldoc:
        if data.is_paid == 1 and data.status == 'Paid' and data.docstatus == 2:
            frappe.db.sql("update `tabExpense Claim` set status = '{0}' where name = '{1}'".format('Cancelled', data.name))


            
