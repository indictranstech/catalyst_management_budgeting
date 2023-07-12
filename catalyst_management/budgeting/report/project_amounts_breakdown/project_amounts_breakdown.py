# Copyright (c) 2023, Simon Wanyama and contributors
# For license information, please see license.txt

import frappe
from frappe import _


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
            'fieldtype': 'Data',
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
        }
	]

def get_data(filters):
	data = []

	for d in make_data():
		data.append(
			{
				"document": d["parenttype"],
				"document_name": d["parent"],
				"project": d["project_for_budget"],
				"project_budget": d["project_budget"],
				"budget_account_head": d["budget_account_head"],
				"actual_amount": d["amount"],
				"party_type": d["party_type"],
				"party": d["party"],
				"coa":d['coa'],
				"posting_date":d['posting_date'],
				"cost_center":d['cost_center'],

			}
		)

	# Filters is a dictionary of filters, so we can just filter the data straight away based on the filters dict
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
						pii.cost_center,
						pi.posting_date,

						"Supplier" as party_type,
						pi.supplier as party
					from `tabPurchase Invoice Item` pii
					left join `tabPurchase Invoice` pi on pii.parent = pi.name
					where  pii.docstatus = 1 and pii.project_for_budget IS NOT NULL
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
			 				je.posting_date

						from `tabJournal Entry Account` jea
			 			left join `tabJournal Entry` je on je.name = jea.parent
						where  jea.docstatus = 1 and jea.project_for_budget IS NOT NULL  order by jea.project_for_budget

				""",as_dict=1)
	
	for i in pi_docs:
		if i.project_for_budget and i.docstatus == 1:
			i.coa = str(frappe.db.get_value('Budget Account Mapping', {'parent': i.project_budget,'budget_account_head':i.budget_account_head}, 'chart_of_account_head'))
			data_.append(i)

	for i in ec_docs:
		if i.project_for_budget and i.docstatus == 1:
			i.coa  = str(frappe.db.get_value('Budget Account Mapping', {'parent': i.project_budget,'budget_account_head':i.budget_account_head}, 'chart_of_account_head'))
			data_.append(i)

	for i in je_docs:
		if i.amount and i.project_for_budget and i.docstatus == 1:
			i.coa  = str(frappe.db.get_value('Budget Account Mapping', {'parent': i.project_budget,'budget_account_head':i.budget_account_head}, 'chart_of_account_head'))
			data_.append(i)

	return data_
