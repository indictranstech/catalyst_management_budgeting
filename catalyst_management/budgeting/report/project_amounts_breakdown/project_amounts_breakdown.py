# Copyright (c) 2023, Simon Wanyama and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate
from datetime import datetime, timedelta
from datetime import datetime


def execute(filters=None):
	return get_columns(), get_data(filters)


def get_columns():
	return [
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
			"fieldname": "project",
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
		# {
        #     'fieldname': 'coa',
        #     'label': _('Chart of account Head'),
        #     'fieldtype': 'Data',
        # },
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

def get_data(filters):
	data = []
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	project = filters.get('project')
	document = filters.get('document')
	budget_account_head = filters.get('budget_account_head')
	for d in make_data():
		data.append(
			{
				"document": d["parenttype"],
				"document_name": d["parent"],
				"project": d["project_for_budget"],
				"project_budget": d["project_budget"],
				"pbah":d['pbah'],
				"budget_account_head": d["budget_account_head"],
				"actual_amount": d["amount"],
				"party_type": d["party_type"],
				"party": d["party"],
				"coa":d['coa'],
				"pdm":d['pdm'],
				"posting_date":d['posting_date'],
				"cost_center":d['cost_center'],
				"coa_from_transaction":d['coa_from_transaction'],

			}
		)

	# Filters is a dictionary of filters, so we can just filter the data straight away based on the filters dict
	if from_date and to_date and document and not project and not budget_account_head:
		from_date = datetime.strptime(filters['from_date'], '%Y-%m-%d').date()
		to_date = datetime.strptime(filters['to_date'], '%Y-%m-%d').date()
		filtered_data = [d for d in data if from_date <=  d['posting_date'] <= to_date and d['document'] == document]
		return filtered_data

	if from_date and to_date and project and not document and not budget_account_head:
		from_date = datetime.strptime(filters['from_date'], '%Y-%m-%d').date()
		to_date = datetime.strptime(filters['to_date'], '%Y-%m-%d').date()
		filtered_data = [d for d in data if from_date <=  d['posting_date'] <= to_date and d['project'] == project]
		return filtered_data

	if from_date and to_date and budget_account_head and not project and not document :
		from_date = datetime.strptime(filters['from_date'], '%Y-%m-%d').date()
		to_date = datetime.strptime(filters['to_date'], '%Y-%m-%d').date()
		filtered_data = [d for d in data if from_date <=  d['posting_date'] <= to_date and d['budget_account_head'] == budget_account_head]
		return filtered_data

	if from_date and to_date and document and project and not budget_account_head:
		from_date = datetime.strptime(filters['from_date'], '%Y-%m-%d').date()
		to_date = datetime.strptime(filters['to_date'], '%Y-%m-%d').date()
		filtered_data = [d for d in data if from_date <=  d['posting_date'] <= to_date and d['document'] == document and d['project'] == project]
		return filtered_data

	if from_date and to_date and document and not project and budget_account_head:
		from_date = datetime.strptime(filters['from_date'], '%Y-%m-%d').date()
		to_date = datetime.strptime(filters['to_date'], '%Y-%m-%d').date()
		filtered_data = [d for d in data if from_date <=  d['posting_date'] <= to_date and d['document'] == document and d['budget_account_head'] == budget_account_head]
		return filtered_data

	if from_date and to_date and not document and project and budget_account_head:
		from_date = datetime.strptime(filters['from_date'], '%Y-%m-%d').date()
		to_date = datetime.strptime(filters['to_date'], '%Y-%m-%d').date()
		filtered_data = [d for d in data if from_date <=  d['posting_date'] <= to_date and d['project'] == project and d['budget_account_head'] == budget_account_head]
		return filtered_data					

	

	if from_date and to_date and not budget_account_head and not project and not document:
		from_date = datetime.strptime(filters['from_date'], '%Y-%m-%d').date()
		to_date = datetime.strptime(filters['to_date'], '%Y-%m-%d').date()
		filtered_data = [d for d in data if from_date <=  d['posting_date'] <= to_date]
		return filtered_data

	if from_date and to_date and document and project and budget_account_head:
		from_date = datetime.strptime(filters['from_date'], '%Y-%m-%d').date()
		to_date = datetime.strptime(filters['to_date'], '%Y-%m-%d').date()
		filtered_data = [d for d in data if from_date <=  d['posting_date'] <= to_date and d['project'] == project and d['document'] == document and d['budget_account_head'] == budget_account_head]
		return filtered_data
				
		
	else:	
		filtered_data = [d for d in data if all(item in d.items() for item in filters.items())]
		return filtered_data

		

	

			

def make_data():
	'''
	Actual Amounts for Journal Entry, Expense Claim, and Purchase Entry
	Here we make the total for each and add up
	We take care of conditions for date, project and budget_account_head
	'''
	data_ = []

	pi_docs =  frappe.db.sql(f""" 
					select
						pii.project_for_budget, 
						pii.project_budget, 
						pii.budget_account_head, 
						pii.amount, 
						pii.modified, 
						pii.parent, 
						pii.parenttype, 
						pii.docstatus,
						pii.expense_account as coa_from_transaction,
						pii.cost_center,
						pi.posting_date,

						"Supplier" as party_type,
						pi.supplier as party
					from `tabPurchase Invoice Item` pii
					left join `tabPurchase Invoice` pi on pii.parent = pi.name
					where  pii.docstatus = 1 and pii.project_for_budget IS NOT NULL
				""",as_dict=1)

	# Sales Invoice

	si_docs =  frappe.db.sql(f""" 
					select
						sii.project_for_budget, 
						sii.project_budget, 
						sii.budget_account_head, 
						sii.amount, 
						sii.modified, 
						sii.parent, 
						sii.parenttype, 
						sii.docstatus,
						sii.income_account as coa_from_transaction,
						sii.cost_center,
						si.posting_date,

						"Customer" as party_type,
						si.customer as party
					from `tabSales Invoice Item` sii
					left join `tabSales Invoice` si on sii.parent = si.name
					where  sii.docstatus = 1 and sii.project_for_budget IS NOT NULL
				""",as_dict=1)			
	
	ec_docs =  frappe.db.sql(f""" 

					select
						ecd.project_for_budget, 
						ecd.project_budget, 
						ecd.budget_account_head, 
						ecd.amount, 
						ecd.modified, 
						ecd.name,
						ecd.parent, 
						ecd.parenttype, 
						ecd.docstatus,
						ecd.cost_center,
						ecd.default_account as coa_from_transaction,
						ec.posting_date,
						ec.employee as party,
						"Employee" as party_type
			  
					from `tabExpense Claim Detail` ecd
					left join `tabExpense Claim` ec on ecd.parent = ec.name
					where  ecd.docstatus = 1 and ecd.project_for_budget IS NOT NULL  order by ecd.project_for_budget

				""",as_dict=1)
	je_docs = frappe.db.sql(f""" 

						select
							jea.project_for_budget, 
							jea.project_budget, 
							jea.budget_account_head, 
							jea.debit_in_account_currency as amount, 
							jea.modified, 
							jea.name,
							jea.parent, 
							jea.parenttype, 
							jea.docstatus,
							jea.party_type,
							jea.party,
							jea.cost_center,
							jea.account as coa_from_transaction,
			 				je.posting_date

						from `tabJournal Entry Account` jea
			 			left join `tabJournal Entry` je on je.name = jea.parent
						where  jea.docstatus = 1 and jea.project_for_budget IS NOT NULL  order by jea.project_for_budget

				""",as_dict=1)


	for i in si_docs:
		if i.project_for_budget and i.docstatus == 1:
			i.coa = str(frappe.db.get_value('Budget Account Mapping', {'parent': i.project_budget,'budget_account_head':i.budget_account_head}, 'chart_of_account_head'))
			i.pdm = str(frappe.db.get_value('Budget Account Mapping', {'parent': i.project_budget,'budget_account_head':i.budget_account_head}, 'name'))
			i.pbah = str(frappe.db.get_value('Budget Account Mapping', {'parent': i.project_budget,'budget_account_head':i.budget_account_head}, 'parent_budget_account_head'))
			data_.append(i)			
	
	for i in pi_docs:
		if i.project_for_budget and i.docstatus == 1:
			i.coa = str(frappe.db.get_value('Budget Account Mapping', {'parent': i.project_budget,'budget_account_head':i.budget_account_head}, 'chart_of_account_head'))
			i.pdm = str(frappe.db.get_value('Budget Account Mapping', {'parent': i.project_budget,'budget_account_head':i.budget_account_head}, 'name'))
			i.pbah = str(frappe.db.get_value('Budget Account Mapping', {'parent': i.project_budget,'budget_account_head':i.budget_account_head}, 'parent_budget_account_head'))
			data_.append(i)
    
	for i in ec_docs:
		if i.project_for_budget and i.docstatus == 1:
			i.coa  = str(frappe.db.get_value('Budget Account Mapping', {'parent': i.project_budget,'budget_account_head':i.budget_account_head}, 'chart_of_account_head'))
			i.pdm = str(frappe.db.get_value('Budget Account Mapping', {'parent': i.project_budget,'budget_account_head':i.budget_account_head}, 'name'))
			i.pbah = str(frappe.db.get_value('Budget Account Mapping', {'parent': i.project_budget,'budget_account_head':i.budget_account_head}, 'parent_budget_account_head'))
			data_.append(i)

	for i in je_docs:
		if i.amount and i.project_for_budget and i.docstatus == 1:
			i.coa  = str(frappe.db.get_value('Budget Account Mapping', {'parent': i.project_budget,'budget_account_head':i.budget_account_head}, 'chart_of_account_head'))
			i.pdm = str(frappe.db.get_value('Budget Account Mapping', {'parent': i.project_budget,'budget_account_head':i.budget_account_head}, 'name'))
			i.pbah = str(frappe.db.get_value('Budget Account Mapping', {'parent': i.project_budget,'budget_account_head':i.budget_account_head}, 'parent_budget_account_head'))
			data_.append(i)

	return data_
