import frappe


def before_save(doc, methode):
    for account in doc.accounts:
        result= frappe.db.get_list('Budget Account Mapping',{'parent':account.project,'budget_account_head':account.budget_account_head,'chart_of_account_head':account.account},['parent', 'budget_account_head', 'chart_of_account_head','custom_party_type','custom_party'])
        for i in result:
            account.custom_member_type = i.custom_party_type
            account.custom_member = i.custom_party
           
