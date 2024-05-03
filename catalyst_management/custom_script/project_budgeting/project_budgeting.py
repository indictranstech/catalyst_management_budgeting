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

            pi_amount = frappe.db.get_all("Purchase Invoice Item", {"project_for_budget": doc.name, "budget_account_head": bam.budget_account_head, "docstatus": 1}, ["amount","parent"])
            si_amount = frappe.db.get_all("Sales Invoice Item", {"project_for_budget": doc.name, "budget_account_head": bam.budget_account_head, "docstatus": 1}, ["amount","parent"])
            je_amount = frappe.db.get_all("Journal Entry Account", {"project_for_budget": doc.name, "budget_account_head": bam.budget_account_head, "docstatus": 1}, ["debit_in_account_currency","parent"])
            ec_amount = frappe.db.get_all("Expense Claim Detail", {"project_for_budget": doc.name, "budget_account_head": bam.budget_account_head, "docstatus": 1}, ["amount","parent"])

            for pi in pi_amount:
                pi_doc = frappe.get_doc('Purchase Invoice', pi['parent'])
                posting_date = pi_doc.posting_date
                if start_date <= posting_date <= end_date:
                    pi_amount_total += float(pi.get('amount', 0))

            for si in si_amount:
                si_doc = frappe.get_doc('Sales Invoice', si['parent'])
                posting_date = si_doc.posting_date
                if start_date <= posting_date <= end_date:
                    si_amount_total += float(si.get('amount', 0))

            for je in je_amount:
                je_doc = frappe.get_doc('Journal Entry', je['parent'])
                posting_date = je_doc.posting_date
                if start_date <= posting_date <= end_date:
                    je_amount_total += float(je.get('debit_in_account_currency', 0))

            for ec in ec_amount:
                ec_doc = frappe.get_doc('Expense Claim', ec['parent'])
                posting_date = ec_doc.posting_date
                if start_date <= posting_date <= end_date:
                    ec_amount_total += float(ec.get('amount', 0))

            # Add each amount to the total
            bam.custom_total_amount += pi_amount_total + si_amount_total + je_amount_total + ec_amount_total
            bam.db_update()
            doc.custom_total_actual_amount += pi_amount_total + si_amount_total + je_amount_total + ec_amount_total
            doc.db_update()            
            


