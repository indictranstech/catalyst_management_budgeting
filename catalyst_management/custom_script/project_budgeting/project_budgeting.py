import frappe

def before_save(doc,method):
    total_amount = sum(amt.amount for amt in doc.budget_account_mapping)
    doc.custom_grand_total = total_amount

def before_save_on_update(doc,method):
    total_amount = sum(amt.amount for amt in doc.budget_account_mapping)
    doc.custom_grand_total = total_amount
    doc.db_update()    


def calculating_total_actual_amount_on_update(doc, method):
    doc.custom_total_actual_amount = 0.0  # Initialize total amount

    if doc.budget_account_mapping:
        for bam in doc.budget_account_mapping:
            bam.custom_total_amount = 0
            pi_amount_total = 0.0
            si_amount_total = 0.0
            je_amount_total = 0.0
            ec_amount_total = 0.0
            start_date = frappe.get_doc("Accounting Period", bam.period).start_date
            end_date = frappe.get_doc("Accounting Period", bam.period).end_date

            sql_query = """
                SELECT p.posting_date, i.amount
                FROM `tabPurchase Invoice Item` i, `tabPurchase Invoice` p 
                WHERE i.parent = p.name AND i.project_for_budget = %s 
                AND i.budget_account_head = %s 
                AND p.docstatus = 1 
                AND p.posting_date BETWEEN %s AND %s
            """
            pi_amount = frappe.db.sql(sql_query, (doc.name, bam.budget_account_head, start_date, end_date), as_dict=True)

            sql_query1 = """
                SELECT s.posting_date, i.amount 
                FROM `tabSales Invoice Item` i, `tabSales Invoice` s 
                WHERE i.parent = s.name AND i.project_for_budget = %s 
                AND i.budget_account_head = %s 
                AND s.docstatus = 1 
                AND s.posting_date BETWEEN %s AND %s
            """
            si_amount = frappe.db.sql(sql_query1, (doc.name, bam.budget_account_head, start_date, end_date), as_dict=True)

            sql_query2 = """
                SELECT j.posting_date, i.debit_in_account_currency 
                FROM `tabJournal Entry Account` i, `tabJournal Entry` j 
                WHERE i.parent = j.name AND i.project_for_budget = %s 
                AND i.budget_account_head = %s 
                AND j.docstatus = 1 
                AND j.posting_date BETWEEN %s AND %s
            """
            je_amount = frappe.db.sql(sql_query2, (doc.name, bam.budget_account_head, start_date, end_date), as_dict=True)

            sql_query3 = """
                SELECT e.posting_date, i.amount
                FROM `tabExpense Claim Detail` i, `tabExpense Claim` e 
                WHERE i.parent = e.name AND i.project_for_budget = %s 
                AND i.budget_account_head = %s 
                AND e.docstatus = 1 
                AND e.posting_date BETWEEN %s AND %s
            """
            ec_amount = frappe.db.sql(sql_query3, (doc.name, bam.budget_account_head, start_date, end_date), as_dict=True)

            
            for pi in pi_amount:
                pi_amount_total += float(pi.get('amount', 0))

            for si in si_amount:
                si_amount_total += float(si.get('amount', 0))

            for je in je_amount:
                je_amount_total += float(je.get('debit_in_account_currency', 0))

            for ec in ec_amount:
                ec_amount_total += float(ec.get('amount', 0))

            # Add each amount to the total
            bam.custom_total_amount += pi_amount_total + si_amount_total + je_amount_total + ec_amount_total
            bam.db_update()
            doc.custom_total_actual_amount += pi_amount_total + si_amount_total + je_amount_total + ec_amount_total
            doc.db_update()            
            


