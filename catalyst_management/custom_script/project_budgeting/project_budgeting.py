import frappe

def before_save(doc,method):
    total_amount = sum(amt.amount for amt in doc.budget_account_mapping)
    doc.custom_grand_total = total_amount

def before_save_on_update(doc,method):
    total_amount = sum(amt.amount for amt in doc.budget_account_mapping)
    doc.custom_grand_total = total_amount
    doc.db_update()    

def calculating_total_actual_amount(doc, method):
    doc.custom_total_actual_amount = 0.0  # Initialize total amount

    if doc.budget_account_mapping:
        for bam in doc.budget_account_mapping:
            bam.custom_total_amount = 0
            pi_amount_total = 0.0
            si_amount_total = 0.0
            je_amount_total = 0.0
            ec_amount_total = 0.0

            pi_amount = frappe.db.get_all("Purchase Invoice Item", {"project_for_budget": doc.name, "budget_account_head": bam.budget_account_head, "docstatus": 1}, "amount")
            si_amount = frappe.db.get_all("Sales Invoice Item", {"project_for_budget": doc.name, "budget_account_head": bam.budget_account_head, "docstatus": 1}, "amount")
            je_amount = frappe.db.get_all("Journal Entry Account", {"project_for_budget": doc.name, "budget_account_head": bam.budget_account_head, "docstatus": 1}, "debit_in_account_currency")
            ec_amount = frappe.db.get_all("Expense Claim Detail", {"project_for_budget": doc.name, "budget_account_head": bam.budget_account_head, "docstatus": 1}, "amount")

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
            doc.custom_total_actual_amount += pi_amount_total + si_amount_total + je_amount_total + ec_amount_total

def calculating_total_actual_amount_on_update(doc, method):
    doc.custom_total_actual_amount = 0.0  # Initialize total amount

    if doc.budget_account_mapping:
        for bam in doc.budget_account_mapping:
            bam.custom_total_amount = 0
            pi_amount_total = 0.0
            si_amount_total = 0.0
            je_amount_total = 0.0
            ec_amount_total = 0.0

            pi_amount = frappe.db.get_all("Purchase Invoice Item", {"project_for_budget": doc.name, "budget_account_head": bam.budget_account_head, "docstatus": 1}, "amount")
            si_amount = frappe.db.get_all("Sales Invoice Item", {"project_for_budget": doc.name, "budget_account_head": bam.budget_account_head, "docstatus": 1}, "amount")
            je_amount = frappe.db.get_all("Journal Entry Account", {"project_for_budget": doc.name, "budget_account_head": bam.budget_account_head, "docstatus": 1}, "debit_in_account_currency")
            ec_amount = frappe.db.get_all("Expense Claim Detail", {"project_for_budget": doc.name, "budget_account_head": bam.budget_account_head, "docstatus": 1}, "amount")

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
            


