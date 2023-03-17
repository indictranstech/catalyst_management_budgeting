import frappe

@frappe.whitelist()
def budget_account_head(project):
    account_heads = frappe.get_all("Budget Account Mapping", filters={"parent":project}, fields=["budget_account_head"])
    return [head["budget_account_head"] for head in account_heads]
   
