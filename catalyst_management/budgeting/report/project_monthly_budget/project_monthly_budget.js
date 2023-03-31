// Copyright (c) 2023, Simon Wanyama and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Project Monthly Budget"] = {
	"filters": [
		{
			"fieldname": "period",
			"label": __("Accounting Period"),
			"fieldtype": "Link",
			"options": "Accounting Period",
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
			"fieldname": "budget_month",
			"label": __("Budget Month"),
			"fieldtype": "Select",
			"options": ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
			"width": 100,
			"reqd": 0,
		}
	],

	onload: function(report) {
		report.page.add_inner_button(__("Project Amounts Breakdown"), function() {
			frappe.set_route('query-report', 'Project Amounts Breakdown');
		});
		report.page.add_inner_button(__("Project Budget Variance"), function() {
			frappe.set_route('query-report', 'Project Budget Variance');
		});
	}
};
