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
			"fieldname": "start_date",
			"fieldtype": "Date",
			"label": "Start Date",
		},
		{
			"fieldname": "end_date",
			"fieldtype": "Date",
			"label": "End Date",
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
            'fieldname': 'amount',
            'label': _('Budget Amount'),
            'fieldtype': 'Currency',
        },
		{
            'fieldname': 'actual_amount',
            'label': _('Actual Amount'),
            'fieldtype': 'Currency',
        },
		{
            'fieldname': 'variance',
            'label': _('Variance'),
            'fieldtype': 'Currency',
        },
        {
            'fieldname': 'variance_percentage',
            'label': _('Variance (%)'),
            'fieldtype': 'Data',
        }
	]

def get_data(filters):
	# conditions for filters
	conditions, data = [], []
	
	if filters.get("period"): conditions.append(["period", "=", filters.get("period")])
	if filters.get("project"): conditions.append(["parent", "=", filters.get("project")])
	if filters.get("budget_account_head"): conditions.append(["budget_account_head", "=", filters.get("budget_account_head")])
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
		"parent" # => Project Budget == project name as well
	], filters=conditions)

	# Make Data
	for d in budget_account_map:
		# Change fieldname for Project
		d["project"] = d["parent"]

		# Start and End Date from Accounting Period
		d["start_date"] = frappe.get_doc("Accounting Period", d["period"]).start_date
		d["end_date"] = frappe.get_doc("Accounting Period", d["period"]).end_date

		# Actual Amount [JOURNAL ENTRY, EXPENSE CLAIM, PURCHASE INVOICE]
		d["actual_amount"] = actual_amounts(d["project"], d["budget_account_head"], d["start_date"], d["end_date"])
		
		# Variance
		d["variance"] = d["amount"] - d["actual_amount"]

		# Variance (%)
		d["variance_percentage"] = (d["variance"] / d["amount"]) * 100

		# Add to Data
		data.append(d)
	
	return data


def actual_amounts(project, head, start_date, end_date):
	'''
	Actual Amounts for Journal Entry, Expense Claim, and Purchase Entry
	Here we make the total for each and add up
	We take care of conditions for date, project and budget_account_head
	'''
	pi_total = 0
	ec_total = 0
	je_total = 0
	pi_amount = frappe.get_all('Purchase Invoice Item', filters={
		"project_for_budget": project,
		"budget_account_head": head,
		"docstatus": 1
	}, fields=["project_for_budget", "budget_account_head", "amount", "modified"])
	ec_amount = frappe.get_all('Expense Claim Detail', filters={
		"project_for_budget": project,
		"budget_account_head": head,
		"docstatus": 1
	}, fields=["project_for_budget", "budget_account_head", "amount", "modified"])
	je_amount = frappe.get_all('Journal Entry Account', filters={
		"project_for_budget": project,
		"budget_account_head": head,
		"docstatus": 1
	}, fields=["project_for_budget", "budget_account_head", "debit_in_account_currency", "modified"])

	for i in pi_amount:
		if start_date < (i.modified).date() < end_date:
			pi_total = pi_total + i.amount

	for i in ec_amount:
		if start_date < (i.modified).date() < end_date:
			ec_total = ec_total + i.amount

	for i in je_amount:
		if start_date < (i.modified).date() < end_date:
			if i.debit_in_account_currency:
				i["amount"] = i["debit_in_account_currency"]
				je_total = je_total + i.amount

	return pi_total + ec_total + je_total

