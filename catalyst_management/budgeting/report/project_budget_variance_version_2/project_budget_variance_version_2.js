// Copyright (c) 2024, Simon Wanyama and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Project Budget Variance Version 2"] = {
	"filters": [

		{
			"fieldname": "project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project",
			"width": 100,
			"reqd": 0,
			"on_change": function() {
				var pr = frappe.query_report.get_filter_value("project");
				if (pr) {
					frappe.call({
						method: "frappe.client.get_value",
						args: {
							doctype: "Project",
							filters: { name: pr },
							fieldname: "company"
						},
						callback: function(response) {
							var company = response.message.company;
							frappe.query_report.set_filter_value("period", "");
							frappe.query_report.set_filter_value("period", "");
						}
					});
				} else {
					frappe.query_report.set_filter_value("period", "");
				}
			}
		},
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"width": 100,
			"reqd": 0,
		},
		{
			"fieldname": "period",
			"label": __("Accounting Period"),
			"fieldtype": "Link",
			"options": "Accounting Period",
			"width": 100,
			"reqd": 0,
			"get_query": function() {
				var pr = frappe.query_report.get_filter_value("company");
				return {
						'doctype': 'Accounting Period',
						'filters': { 'company':pr},
						'limit_page_length': 10000
					};
			}
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
				"default": frappe.datetime.month_start(),
				"width": 100,
				"reqd": 1,
			},	
			{
				"fieldname": "to_date",
				"label": __("To Date"),
				"fieldtype": "Date",
				"default": frappe.datetime.month_end(),
				"width": 100,
				"reqd": 1,
			},		
		],
	
		onload: function(report) {
			report.page.add_inner_button(__("Project Amounts Breakdown"), function() {
				frappe.set_route('query-report', 'Project Amounts Breakdown',frappe.query_report.get_filter_values());
			});
			report.page.add_inner_button(__("Project Monthly Budget"), function() {
				frappe.set_route('query-report', 'Project Monthly Budget',frappe.query_report.get_filter_values());
			});
			
		}
	};
	