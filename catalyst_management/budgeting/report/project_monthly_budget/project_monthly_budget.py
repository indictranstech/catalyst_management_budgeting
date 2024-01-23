# Copyright (c) 2023, Simon Wanyama and contributors
# For license information, please see license.txt

import copy
from collections import OrderedDict

import frappe
from frappe import _
from frappe.utils import date_diff, flt, getdate

def execute(filters=None):
    # if not filters:
    #     return [], [], None, []


    columns = get_columns(filters)
    conditions = get_conditions(filters)
    data = get_data(conditions, filters)

    if not data:
        return [], [], None, []

    data

    return columns, data, None

def get_conditions(filters):
    conditions = ""
    if filters.get("period"):
        conditions += " and bam.period = %(period)s"
 
    if(filters.get('project')):
      conditions += " and pb.name = %(project)s"

    if(filters.get('budget_account_head')):
      conditions += " and bam.budget_account_head = %(budget_account_head)s"
       
    if filters.get("budget_month"):
        conditions += " and mdp.month = %(budget_month)s"    

    return conditions



def get_data(conditions,filters):
    data = frappe.db.sql("""
       SELECT  bam.period AS period,
	   pb.name AS project,
	   bam.budget_account_head AS budget_account_head,
	   bam.amount AS budget_amount,
	   mdp.month As budget_month,
	   mdp.amount_allocation AS monthly_distribution
       FROM `tabProject Budgeting` pb,`tabBudget Account Mapping` bam,`tabMonthly Distribution` md, `tabMonthly Distribution Percentage` mdp WHERE pb.docstatus = 1 and pb.name = bam.parent and pb.name = md.custom_project and bam.budget_account_head = md.custom_budget_account_head and md.name = mdp.parent and mdp.amount_allocation > 0{conditions}
    """.format(
        conditions=conditions
    ), filters, as_dict=1)

   
    return data


def get_columns(filters):
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
			"fieldname": "monthly_distribution",
			"fieldtype": "Currency",
			"label": "Monthly Distribution",
		},
        {
            'fieldname': 'budget_amount',
            'label': _('Budget Amount'),
            'fieldtype': 'Currency',
        },
	]