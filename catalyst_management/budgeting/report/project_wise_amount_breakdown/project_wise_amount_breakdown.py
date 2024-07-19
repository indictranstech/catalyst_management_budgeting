import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns(filters)
	conditions = get_conditions(filters)
	data = get_data(filters,conditions)
	return columns, data, None

def get_conditions(filters):
    conditions = ""
    if(filters.get('document') == 'Purchase Invoice'):
	    if filters.get("from_date") and filters.get("to_date"):
	        conditions += f" and pi.posting_date between '{filters.get('from_date')}' and '{filters.get('to_date')}'"
	    if filters.get("project"):
	    	conditions += f" and pii.project_budget = '{filters.get('project')}'"
	    if filters.get("budget_account_head"):
	    	conditions += f" and pii.budget_account_head = '{filters.get('budget_account_head')}'"
    

    if(filters.get('document') == 'Sales Invoice'):
	    if filters.get("from_date") and filters.get("to_date"):
	        conditions += f" and si.posting_date between '{filters.get('from_date')}' and '{filters.get('to_date')}'"
	    if filters.get("project"):
	    	conditions += f" and sii.project_budget = '{filters.get('project')}'"
	    if filters.get("budget_account_head"):
	    	conditions += f" and sii.budget_account_head = '{filters.get('budget_account_head')}'"
    
    if(filters.get('document') == 'Journal Entry'):
	    if filters.get("from_date") and filters.get("to_date"):
	        conditions += f" and je.posting_date between '{filters.get('from_date')}' and '{filters.get('to_date')}'"
	    if filters.get("project"):
	    	conditions += f" and jea.project_budget = '{filters.get('project')}'"
	    if filters.get("budget_account_head"):
	    	conditions += f" and jea.budget_account_head = '{filters.get('budget_account_head')}'"
    
    if(filters.get('document') == 'Expense Claim'):
	    if filters.get("from_date") and filters.get("to_date"):
	        conditions += f" and ec.posting_date between '{filters.get('from_date')}' and '{filters.get('to_date')}'"
	    if filters.get("project"):
	    	conditions += f" and ecd.project_budget = '{filters.get('project')}'"
	    if filters.get("budget_account_head"):
	    	conditions += f" and ecd.budget_account_head = '{filters.get('budget_account_head')}'"
    

    return conditions


def get_data(filters,conditions):
	print(f'\n filters == {filters}\n')
	
	if(filters.get('document') == 'Purchase Invoice'):
		pi_data = frappe.db.sql(f""" SELECT DISTINCT
				pii.project_for_budget, pii.project_budget, pii.budget_account_head,
				pi.grand_total as actual_amount,pii.expense_account as coa,
				pii.amount, pii.modified, pii.parent as document_name, pii.parenttype as document, pii.docstatus,
				pii.expense_account AS coa_from_transaction, pii.cost_center, pi.posting_date,
				"Supplier" AS party_type, pi.supplier AS party
			FROM `tabPurchase Invoice`pi 
			LEFT JOIN `tabPurchase Invoice Item`pii 
			ON pi.name = pii.parent 
			WHERE pii.docstatus = 1 AND pii.project_for_budget IS NOT NULL AND 1=1 
	     	{conditions} 
                    
             """,as_dict=1,debug=1)

		for i in pi_data:
			i.pbah = str(frappe.db.get_value('Budget Account Mapping', {'parent': i.project_budget,'budget_account_head': i.budget_account_head}, 'parent_budget_account_head'))

		return pi_data

	elif(filters.get('document') == 'Sales Invoice'):
		si_data = frappe.db.sql(f""" SELECT DISTINCT
				sii.project_for_budget, sii.project_budget, sii.budget_account_head,
				sii.amount, sii.modified, sii.parent as document_name,
				sii.parenttype as document,sii.docstatus,si.grand_total as actual_amount,
				sii.income_account AS coa_from_transaction, sii.cost_center, 
				si.posting_date,"Customer" AS party_type, si.customer AS party 
			FROM `tabSales Invoice`si 
			JOIN `tabSales Invoice Item`sii 
			ON si.name = sii.parent 
			WHERE sii.docstatus = 1 AND sii.project_for_budget IS NOT NULL AND 1=1 
	     	{conditions} 
                    
             """,as_dict=1,debug=1)
		for i in si_data:
			i.pbah = str(frappe.db.get_value('Budget Account Mapping', {'parent': i.project_budget,'budget_account_head': i.budget_account_head}, 'parent_budget_account_head'))
		return si_data

	elif(filters.get('document') == 'Journal Entry'):
		je_data = frappe.db.sql(f""" SELECT DISTINCT
				jea.project_for_budget, jea.project_budget, jea.budget_account_head,
				jea.debit_in_account_currency AS actual_amount, jea.modified, jea.name,
				jea.parent as document_name,
				jea.parenttype as document, jea.docstatus, jea.party_type, jea.party, jea.cost_center,
				jea.account AS coa_from_transaction, je.posting_date 
			FROM `tabJournal Entry`je 
			JOIN `tabJournal Entry Account`jea 
			ON je.name = jea.parent 
			WHERE jea.docstatus = 1 AND jea.project_for_budget IS NOT NULL AND
			1=1 
	     	{conditions} 
                    
             """,as_dict=1,debug=1)
		for i in je_data:
			i.pbah = str(frappe.db.get_value('Budget Account Mapping', {'parent': i.project_budget,'budget_account_head': i.budget_account_head}, 'parent_budget_account_head'))
			
		return je_data

	elif(filters.get('document') == 'Expense Claim'):
		ec_data = frappe.db.sql(f""" SELECT DISTINCT
				ecd.project_for_budget, ecd.project_budget, ecd.budget_account_head,
				ecd.amount, ecd.modified, ecd.name, ecd.parent as document_name,
				ecd.parenttype as document, ecd.docstatus,ecd.sanctioned_amount as actual_amount,
				ecd.cost_center, ecd.default_account AS coa_from_transaction, ec.posting_date,
				ec.employee AS party, "Employee" AS party_type 
			FROM `tabExpense Claim`ec 
			JOIN `tabExpense Claim Detail`ecd 
			ON ec.name = ecd.parent 
			WHERE ecd.docstatus = 1 AND ecd.project_for_budget IS NOT NULL AND 1=1 
	     	{conditions} 
                    
             """,as_dict=1,debug=1)
		for i in ec_data:
			i.pbah = str(frappe.db.get_value('Budget Account Mapping', {'parent': i.project_budget,'budget_account_head': i.budget_account_head}, 'parent_budget_account_head'))
		return ec_data

	else:
		project = filters.get('project')
		budget_account_head = filters.get('budget_account_head')
		# doc_list = ["Journal Entry", "Purchase Invoice", "Expense Claim", "Sales Invoice"]
		data = frappe.db.sql (f"""SELECT DISTINCT
				pii.project_for_budget, pii.project_budget, pii.budget_account_head,
				pi.grand_total as actual_amount,pii.expense_account as coa,
				pii.amount, pii.modified, pii.parent as document_name, pii.parenttype as document, pii.docstatus,
				pii.expense_account AS coa_from_transaction, pii.cost_center, pi.posting_date,
				"Supplier" AS party_type, pi.supplier AS party
			FROM `tabPurchase Invoice`pi 
			LEFT JOIN `tabPurchase Invoice Item`pii 
			ON pi.name = pii.parent 
			WHERE 1=1 
	     	{conditions} 

			UNION ALL

			SELECT DISTINCT
				sii.project_for_budget,sii.project_budget,
				sii.budget_account_head, sii.amount as actual_amount,
				sii.income_account as coa, sii.amount,sii.modified,
				sii.parent as document_name, sii.parenttype as document,
				sii.docstatus, sii.income_account AS coa_from_transaction,
				sii.cost_center, si.posting_date, "Customer" AS party_type,
				si.customer AS party  
				FROM `tabSales Invoice`si  
				JOIN `tabSales Invoice Item`sii  
				ON si.name = sii.parent 
				WHERE sii.docstatus = 1 AND sii.project_for_budget IS NOT NULL AND  1=1 
	     	{conditions} 

			UNION ALL

			SELECT DISTINCT 
				jea.project_for_budget,jea.project_budget,jea.budget_account_head,
				jea.debit_in_account_currency as actual_amount,jea.account as coa,
				jea.debit_in_account_currency,jea.modified,jea.parent as document_name,
				jea.parenttype as document,jea.docstatus,
				jea.account AS coa_from_transaction, jea.cost_center,
				je.posting_date, jea.party_type AS party_type, jea.party AS party 
			FROM `tabJournal Entry`je  
			JOIN `tabJournal Entry Account`jea  
			ON je.name = jea.parent 
			WHERE jea.docstatus = 1 AND jea.project_for_budget IS NOT NULL AND 1=1 
	     	{conditions} 

			UNION ALL

			SELECT DISTINCT 
				ecd.project_for_budget, ecd.project_budget, ecd.budget_account_head,
				ec.grand_total as actual_amount,ecd.default_account as coa,ecd.amount,
				ecd.modified, ecd.parent as document_name, ecd.parenttype as document,
				ecd.docstatus, ecd.default_account AS coa_from_transaction,ecd.cost_center,
				ec.posting_date, "Employee" AS party_type, ec.employee_name AS party
				FROM `tabExpense Claim`ec 
				JOIN `tabExpense Claim Detail`ecd  
				ON ec.name = ecd.parent
			WHERE 1=1 
	     	{conditions} 

		 	""",as_dict=1,debug=1)
		for i in data:
			i.pbah = str(frappe.db.get_value('Budget Account Mapping', {'parent': i.project_budget,'budget_account_head': i.budget_account_head}, 'parent_budget_account_head'))

		return  data
		



def get_columns(filters):
	columns = [
		{
            'fieldname': 'posting_date',
            'label': _('Posting Date'),
            'fieldtype': 'Date',
        },
		{
            'fieldname': 'document',
            'label': _('Document'),
            'fieldtype': 'Data',
        },
		{
            'fieldname': 'document_name',
            'label': _('Document Name'),
            'fieldtype': 'Data',
        },
		{
			"fieldname": "project_budget",
			'label': _('Project'),
			"fieldtype": "Link",
			"options": "Project",
		},
		{
            'fieldname': 'project_budget',
            'label': _('Project Budget'),
            'fieldtype': 'Link',
            'options': 'Project Budgeting'
        },
		{
            'fieldname': 'pbah',
            'label': _('Parent Budget Account Head'),
            'fieldtype': 'Data',
        },
		{
            'fieldname': 'budget_account_head',
            'label': _('Budget Account Head'),
            'fieldtype': 'Link',
            'options': 'Budget Account Head'
        },
		{
            'fieldname': 'cost_center',
            'label': _('Cost Center'),
            'fieldtype': 'Link',
            'options': 'Cost Center'
        },
		{
            'fieldname': 'actual_amount',
            'label': _('Actual Amount'),
            'fieldtype': 'Currency',
        },
		
		{
            'fieldname': 'coa',
            'label': _('Chart of account Head'),
            'fieldtype': 'Link',
			'options': 'Account',
        },
		{
            'fieldname': 'pdm',
            'label': _('Name'),
            'fieldtype': 'Link',
			'options': 'Budget Account Mapping',
			'hidden':1,
			
        },
		{
            'fieldname': 'party_type',
            'label': _('Party Type'),
            'fieldtype': 'Data',
        },
		{
            'fieldname': 'party',
            'label': _('Party'),
            'fieldtype': 'Data',
        },
		{
            'fieldname': 'coa_from_transaction',
            'label': _('COA From Transaction'),
            'fieldtype': 'Data',
        }
    ]
	return columns

# def get_data(filters):
# 	pi_data = {}
# 	si_data = {}
# 	je_data = {}
# 	ec_data = {}
# 	data = {}

# 	if filters:
# 		print(f'\n filters == {filters}\n')
# 		if(filters.get('document') == 'Purchase Invoice'):
# 			pi_data = frappe.db.sql(""" SELECT DISTINCT
# 					pii.project_for_budget, pii.project_budget, pii.budget_account_head,
# 					pi.grand_total as actual_amount,pii.expense_account as coa,
# 					pii.amount, pii.modified, pii.parent as document_name, pii.parenttype as document, pii.docstatus,
# 					pii.expense_account AS coa_from_transaction, pii.cost_center, pi.posting_date,
# 					"Supplier" AS party_type, pi.supplier AS party
# 				FROM `tabPurchase Invoice`pi 
# 				LEFT JOIN `tabPurchase Invoice Item`pii 
# 				ON pi.name = pii.parent 
# 				WHERE pi.posting_date BETWEEN '{0}' and '{1}'  
# 				AND  pii.project_budget = '{2}' AND pii.budget_account_head = '{3}'

# 		 	""".format(filters.get('from_date'), filters.get('to_date'),filters.get('project'),filters.get('budget_account_head')),as_dict=1,debug=1)

# 			return pi_data

# 		if(filters.get('document') == 'Sales Invoice'):
# 			si_data = frappe.db.sql(""" SELECT DISTINCT
# 					sii.project_for_budget, sii.project_budget, sii.budget_account_head,
# 					sii.amount, sii.modified, sii.parent as document_name,
# 					sii.parenttype as document,sii.docstatus,si.grand_total as actual_amount,
# 					sii.income_account AS coa_from_transaction, sii.cost_center, 
# 					si.posting_date,"Customer" AS party_type, si.customer AS party 
# 				FROM `tabSales Invoice`si 
# 				JOIN `tabSales Invoice Item`sii 
# 				ON si.name = sii.parent 
# 				WHERE sii.project_budget = '{0}' OR sii.budget_account_head = '{1}'

# 		 	""".format(filters.get('project'),filters.get('budget_account_head')),as_dict=1,debug=1)

# 			return si_data

# 		if(filters.get('document') == 'Journal Entry'):
# 			je_data = frappe.db.sql(""" SELECT DISTINCT
# 					jea.project_for_budget, jea.project_budget, jea.budget_account_head,
# 					jea.debit_in_account_currency AS actual_amount, jea.modified, jea.name,
# 					jea.parent as document_name,
# 					jea.parenttype as document, jea.docstatus, jea.party_type, jea.party, jea.cost_center,
# 					jea.account AS coa_from_transaction, je.posting_date 
# 				FROM `tabJournal Entry`je 
# 				JOIN `tabJournal Entry Account`jea 
# 				ON je.name = jea.parent 
# 				WHERE jea.project_budget = '{0}' AND jea.budget_account_head = '{1}'

# 		 	""".format(filters.get('project'),filters.get('budget_account_head')),as_dict=1,debug=1)

# 			return je_data

# 		if(filters.get('document') == 'Expense Claim'):
# 			ec_data = frappe.db.sql(""" SELECT DISTINCT
# 					ecd.project_for_budget, ecd.project_budget, ecd.budget_account_head,
# 					ecd.amount, ecd.modified, ecd.name, ecd.parent as document_name,
# 					ecd.parenttype as document, ecd.docstatus,ecd.sanctioned_amount as actual_amount,
# 					ecd.cost_center, ecd.default_account AS coa_from_transaction, ec.posting_date,
# 					ec.employee AS party, "Employee" AS party_type 
# 				FROM `tabExpense Claim`ec 
# 				JOIN `tabExpense Claim Detail`ecd 
# 				ON ec.name = ecd.parent 
# 				WHERE ecd.project_budget = '{0}'OR ecd.budget_account_head = '{1}'

# 		 	""".format(filters.get('project'),filters.get('budget_account_head')),as_dict=1,debug=1)

# 			return ec_data
# 	else:
# 		data.update(pi_data)
# 		data.update(si_data)
# 		data.update(je_data)
# 		data.update(ec_data)

# 		return  data