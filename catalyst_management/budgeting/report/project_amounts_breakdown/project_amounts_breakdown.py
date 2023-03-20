# Copyright (c) 2023, Simon Wanyama and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	return get_columns(), get_data(filters)


def get_columns():
	return [
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
            'fieldname': 'actual_amount',
            'label': _('Actual Amount'),
            'fieldtype': 'Currency',
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
				"actual_amount": d["amount"]
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

	pi_docs = frappe.get_all('Purchase Invoice Item', fields=["project_for_budget", "project_budget", "budget_account_head", "amount", "modified", "parent", "parenttype"])
	ec_docs = frappe.get_all('Expense Claim Detail', fields=["project_for_budget", "project_budget", "budget_account_head", "amount", "modified", "parent", "parenttype"])
	je_docs = frappe.get_all('Journal Entry Account', fields=["project_for_budget", "project_budget", "budget_account_head", "debit_in_account_currency", "modified", "parent", "parenttype"])

	for i in pi_docs:
		# if start_date < (i.modified).date() < end_date:
		data_.append(i)

	for i in ec_docs:
		# if start_date < (i.modified).date() < end_date:
		data_.append(i)

	for i in je_docs:
		if i.debit_in_account_currency:
			i["amount"] = i["debit_in_account_currency"]
		# if start_date < (i.modified).date() < end_date:
			data_.append(i)

	return data_
