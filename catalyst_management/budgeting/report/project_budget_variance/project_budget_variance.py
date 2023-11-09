# Copyright (c) 2023, Simon Wanyama and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate
from datetime import datetime, timedelta


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
            'fieldname': 'selected_period_budget_amount',
            'label': _('Selected Period Budget Amount'),
            'fieldtype': 'Currency',
        },
		{
            'fieldname': 'actual_amount',
            'label': _('Actual Amount'),
            'fieldtype': 'Currency',
        },
		{
            'fieldname': 'selected_actual_amount',
            'label': _('Selected Actual'),
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
        },
		{
            'fieldname': 'total_utilisation',
            'label': _('Total Utilisation %'),
            'fieldtype': 'percent',
        },
		{
            'fieldname': 'selected_utilisation',
            'label': _('Selected Utilisation %'),
            'fieldtype': 'percent',
        },
		# {
        #     'fieldname': 'chart_of_account_head',
        #     'label': _('Chart of Account Head'),
        #     'fieldtype': 'Data',
        # },
		{
            'fieldname': 'chart_of_account_head',
            'label': _('Chart of Account Head'),
            'fieldtype': 'Link',
			'options': 'Account',
        },
		{
            'fieldname': 'name',
            'label': _('name'),
            'fieldtype': 'Link',
            'options': 'Budget Account Mapping',
			'hidden':1
        },
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
		"name",
		"period",
		"budget_account_head",
		"monthly_distribution",
		"chart_of_account_head",
		"amount",
		"parent" # => Project Budget == project name as well
	], filters=conditions)


	# Make Data
	for d in budget_account_map:
		# Change fieldname for Project
		d["name"] = d["name"]
		d["project"] = d["parent"]

		# Start and End Date from Accounting Period
		d["start_date"] = frappe.get_doc("Accounting Period", d["period"]).start_date
		d["end_date"] = frappe.get_doc("Accounting Period", d["period"]).end_date

		# Actual Amount [JOURNAL ENTRY, EXPENSE CLAIM, PURCHASE INVOICE]
		actual = actual_amounts(d["project"], d["budget_account_head"], d["start_date"], d["end_date"],getdate(filters.get("from_date")),getdate(filters.get("to_date")))
		d["actual_amount"] = actual[0]

		# selected_actual_amount
		d["selected_actual_amount"]=actual[1]

		d['selected_period_budget_amount'] = 0
		if d['monthly_distribution']:
			over_all_percenatage  = get_month_names_and_Selected_Period_over_all_percenatage(d['monthly_distribution'],filters.get("from_date"),filters.get("to_date"))
			if over_all_percenatage != 0 or over_all_percenatage !=None:
				# d['selected_period_budget_amount'] = round(d['amount']* (over_all_percenatage / 100),2)
				d['selected_period_budget_amount'] = round(over_all_percenatage)



		# Variance
		d["variance"] = d["amount"] - d["actual_amount"]

		# % Utilisation = (Total Bud-Total Act)/Total Bud 
		if (d["amount"] != None and d["amount"]  !=0) and (d["actual_amount"] != None and d["actual_amount"]  !=0):
			# d['total_utilisation'] =round((d['amount'] -  d["actual_amount"])/d['amount']* 100,2)
			d['total_utilisation'] =round((d["actual_amount"])/d['amount']* 100,2)
		else:
			d["total_utilisation"] = 0
		# % Utilisation = (Selected Period Bud-Selected Period Act)/Selected Period Bud
		if (d["selected_period_budget_amount"] != None and d["selected_period_budget_amount"]  !=0) and (d["selected_actual_amount"] != None and d["selected_actual_amount"]  !=0):
			# d['selected_utilisation'] =round((d['selected_period_budget_amount'] -  d["selected_actual_amount"])/d['selected_period_budget_amount']* 100,2)
			d['selected_utilisation'] =round((d["selected_actual_amount"])/d['selected_period_budget_amount']* 100,2)
		else:
			d["selected_utilisation"] = 0

		# Variance (%)
			# strt fixing ZeroDivisionError 
		if (d["variance"] != None and d["variance"]  !=0) and (d["amount"] != None and d["amount"]  !=0):
			d["variance_percentage"] = round((d["variance"] / d["amount"]) * 100,2)
		else:
			d["variance_percentage"] = 0
			# end fixing ZeroDivisionError 

		# Add to Data
		data.append(d)
	
	return data


def actual_amounts(project, head, start_date, end_date,month_start,month_end):
	'''
	Actual Amounts for Journal Entry, Expense Claim, and Purchase Entry
	Here we make the total for each and add up
	We take care of conditions for date, project and budget_account_head
	'''
	# for actual
	pi_total = 0
	ec_total = 0
	je_total = 0

	# for date range
	month_pi_total = 0
	month_ec_total = 0
	month_je_total = 0

	pi_amount = frappe.get_all('Purchase Invoice Item', filters={
		"project_for_budget": project,
		"budget_account_head": head,
		"docstatus": 1
	}, fields=["project_for_budget", "budget_account_head", "amount", "modified", "parent"])

	ec_amount = frappe.get_all('Expense Claim Detail', filters={
		"project_for_budget": project,
		"budget_account_head": head,
		"docstatus": 1
	}, fields=["project_for_budget", "budget_account_head", "amount", "modified", "parent"])
	je_amount = frappe.get_all('Journal Entry Account', filters={
		"project_for_budget": project,
		"budget_account_head": head,
		"docstatus": 1
	}, fields=["project_for_budget", "budget_account_head", "debit_in_account_currency", "modified","parent"])

	for i in pi_amount:
		pi_doc = frappe.get_doc('Purchase Invoice', i['parent'])
		posting_date = pi_doc.posting_date
		if start_date <= posting_date <= end_date:
			pi_total = pi_total + i.amount
		if month_start <= posting_date <= month_end:
			month_pi_total = month_pi_total + i.amount


	for i in ec_amount:
		ec_doc = frappe.get_doc('Expense Claim', i['parent'])
		posting_date = ec_doc.posting_date
		if start_date <= posting_date <= end_date:
			ec_total = ec_total + i.amount
		if month_start <= posting_date <= month_end:
			month_ec_total = month_ec_total + i.amount

	for i in je_amount:
		je_doc = frappe.get_doc('Journal Entry', i['parent'])
		posting_date = je_doc.posting_date
		if start_date <= posting_date <= end_date:
			if i.debit_in_account_currency:
				i["amount"] = i["debit_in_account_currency"]
				je_total = je_total + i.amount
			if month_start <= posting_date <= month_end:
				i["amount"] = i["debit_in_account_currency"]
				month_je_total = month_je_total + i.amount
	return [pi_total + ec_total + je_total,month_pi_total + month_ec_total + month_je_total]


def get_month_names_and_Selected_Period_over_all_percenatage(monthly_distribution,start_date, end_date):
	start_date = datetime.strptime(start_date, "%Y-%m-%d")
	end_date = datetime.strptime(end_date, "%Y-%m-%d")
	current_date = start_date
	month_names = []

	# Define the list of month names
	month_names_list = [
		"January", "February", "March", "April", "May", "June", 
		"July", "August", "September", "October", "November", "December"
	]

	while current_date <= end_date:
		month_names.append(month_names_list[current_date.month - 1])
		next_month = current_date.month + 1 if current_date.month < 12 else 1
		current_date = current_date.replace(month=next_month, day=1)


	 # Query the database to calculate the overall percentage allocation for the selected period
	over_all_percenatage =  frappe.db.sql(f"""   
				       select 
				    	sum(mdp.amount_allocation) as percentage_allocation,
				        count(mdp.name),
				        mdp.month
				       
				       from `tabMonthly Distribution` md
				       left join `tabMonthly Distribution Percentage` mdp on md.name  = mdp.parent
				       where md.name = '{monthly_distribution}'  and  mdp.month in {tuple(['month']+month_names)} 
				       
				       
				        """,as_dict=1) 

	return over_all_percenatage[0]['percentage_allocation'] if over_all_percenatage else 0
