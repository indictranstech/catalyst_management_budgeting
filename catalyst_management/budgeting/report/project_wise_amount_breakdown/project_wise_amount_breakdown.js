// Copyright (c) 2024, Simon Wanyama and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Project Wise Amount Breakdown"] = {
	"filters": [
		{
			"fieldname": "document",
			"label": __("Doctype"),
			"fieldtype": "Select",
			"options": ["", "Journal Entry", "Purchase Invoice", "Expense Claim", "Sales Invoice"],
			"width": 100,
			"reqd": 0,
		},
		{
			"fieldname": "project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project",
			"width": 100,
			"reqd": 0,
		},
		{
			"fieldname": "budget_account_head",
			"label": __("Budget Account Head"),
			"fieldtype": "Link",
			"options": "Budget Account Head",
			"width": 100,
			"reqd": 0,
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			// "default": frappe.datetime.month_start(),
			"width": 100,
			"reqd": 0,
		},	
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			// "default": frappe.datetime.month_end(),
			"width": 100,
			"reqd": 0,
		},		
	],

	onload: function(report) {
		report.page.add_inner_button(__("Project Monthly Budget"), function() {
			frappe.set_route('query-report', 'Project Monthly Budget',frappe.query_report.get_filter_values());
		});
		report.page.add_inner_button(__("Project Budget Variance"), function() {
			frappe.set_route('query-report', 'Project Budget Variance',frappe.query_report.get_filter_values());
		});
	},
};