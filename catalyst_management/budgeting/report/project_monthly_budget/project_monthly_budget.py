# Copyright (c) 2023, Simon Wanyama and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	return get_columns(), get_data(filters)

def get_columns():
	return [
		{
            'fieldname': 'period',
            'label': _('Accounting Period'),
            'fieldtype': 'Link',
            'options': 'Accounting Period'
        },
		{
            'fieldname': 'project',
            'label': _('Project'),
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
			"fieldname": "budget_month",
			"fieldtype": "Data",
			"label": "Distribution Month",
		},
		{
			"fieldname": "monthly_budget_amount",
			"fieldtype": "Currency",
			"label": "Monthly Budget Amount By Percentage",
		},
		{
			"fieldname": "monthly_amount_allocation",
			"fieldtype": "Currency",
			"label": "Monthly Budget Amount By Amount",
		},
        {
            'fieldname': 'amount',
            'label': _('Budget Amount'),
            'fieldtype': 'Currency',
        },
	]

def get_data(filters):
	# conditions for filters
	conditions, data = [], []
	conditions.append({"docstatus": 1})

		# Data
	''' 
	Our main data is actually from a chilldtable from Project Budgeting Doctype
	'''
	budget_account_map = frappe.db.get_all('Budget Account Mapping', [
		"period",
		"budget_account_head",
		"monthly_distribution",
		"amount",
		"modified",
		"docstatus",
		"parent" # => Project Budget == project name as well
	], filters=conditions)

	# Make Data
	for d in budget_account_map:
		# Change fieldname for Project
		d["project"] = d["parent"]

		# Check if transaction falls in this month
		created = d["modified"].date().strftime("%Y-%B").split('-')
		dist = frappe.get_doc("Monthly Distribution", d["monthly_distribution"])
		if created[0] == dist.fiscal_year:
			d["budget_month"] = created[1]

		for m in monthly_distribution_percentages(d["monthly_distribution"]):
			if m.month == d["budget_month"]:
				d["monthly_budget_amount"] = ((m.percentage_allocation / 100) * total_budget(d["project"], budget_account_map))
				d["monthly_amount_allocation"] = m.amount__allocation

		# Add to Data
		data.append(d)

	# ALways return filtered data
	filtered_data = [d for d in data if all(item in d.items() for item in filters.items())]
	return filtered_data

def total_budget(project, budget_account_map):
	amounts = list(filter(lambda x: x['parent'] == project, budget_account_map))
	amount_list = [x['amount'] for x in amounts]
	return sum(amount_list)

def monthly_distribution_percentages(dist):
	distributions = frappe.get_all("Monthly Distribution Percentage", 
		filters={"parent": dist},
		fields=["month", "percentage_allocation", "amount__allocation", "parent"])
	return distributions

