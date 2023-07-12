// Copyright (c) 2023, Simon Wanyama and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Project Amounts Breakdown"] = {
	"filters": [
		{
			"fieldname": "document",
			"label": __("Doctype"),
			"fieldtype": "Select",
			"options": ["", "Journal Entry", "Purchase Invoice", "Expense Claim"],
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
		}
	],

	onload: function(report) {
		report.page.add_inner_button(__("Project Budget Breakdown"), function() {
			frappe.set_route('query-report', 'Project Budget Breakdown',frappe.query_report.get_filter_values());
		});
		report.page.add_inner_button(__("Project Budget Variance"), function() {
			frappe.set_route('query-report', 'Project Budget Variance',frappe.query_report.get_filter_values());
		});
	},
};
