// Copyright (c) 2023, Simon Wanyama and contributors
// For license information, please see license.txt
/* eslint-disable */


// frappe.query_reports["Profit and Loss Statement Cost Center Wise"] = {
// 	"filters": [

// 	]
// };



frappe.require("assets/erpnext/js/financial_statements.js", function() {
	frappe.query_reports["Profit and Loss Statement Cost Center Wise"] = $.extend({},
		erpnext.financial_statements);

	erpnext.utils.add_dimensions('Profit and Loss Statement Cost Center Wise', 10);

	frappe.query_reports["Profit and Loss Statement Cost Center Wise"]["filters"].push(
		{
			"fieldname": "project",
			"label": __("Project"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Project', txt);
			}
		},
		{
			"fieldname": "all_cost_center_child",
			"label": __("All Cost Center Child"),
			"fieldtype": "Button",
			onclick: function() {
	
				frappe.query_report.set_filter_value('cost_center', [])
				var new_filter1_value = []
				frappe.call({
					method: 'frappe.client.get_list',
					args: {
						'doctype': 'Cost Center',
						'filters':{'is_group':0},
						'fields': ['name']
					},
					async: false,
					callback: function(r) {
						if (!r.exc) {
							if (r.message) {
								new_filter1_value = r.message.map(obj => obj.name)
								console.log(new_filter1_value)
								frappe.query_report.set_filter_value('cost_center', new_filter1_value)
							}
						}
					}
				})
	
			}
		}, 
		{
			"fieldname": "all_cost_center_parent",
			"label": __("All Cost Center parent"),
			"fieldtype": "Button",
			onclick: function() {
	
				frappe.query_report.set_filter_value('cost_center', [])
				var new_filter1_value = []
				frappe.call({
					method: 'frappe.client.get_list',
					args: {
						'doctype': 'Cost Center',
						'filters':{'is_group':1},
						'fields': ['name']
					},
					async: false,
					callback: function(r) {
						if (!r.exc) {
							if (r.message) {
								new_filter1_value = r.message.map(obj => obj.name)
								console.log(new_filter1_value)
								frappe.query_report.set_filter_value('cost_center', new_filter1_value)
							}
						}
					}
				})
	
			}
		}, 
		{
			"fieldname": "include_default_book_entries",
			"label": __("Include Default Book Entries"),
			"fieldtype": "Check",
			"default": 1
		},
		{
			"fieldname": "crrr",
			"label": __("crrr"),
			"fieldtype": "Check",
			"default": 1,
			"read_only":1,
			"hidden":1,
		},
	);
});



// frappe.require("assets/erpnext/js/financial_statements.js", function() {


	// frappe.query_reports["Profit and Loss Statement Cost Center Wise"] = $.extend({},
	// 	erpnext.financial_statements);

		// erpnext.utils.add_dimensions('Profit and Loss Statement Cost Center Wise', 10);

		// frappe.query_reports["Profit and Loss Statement Cost Center Wise"] = ["filters"].push(
		// 	{
		// 		"fieldname": "project",
		// 		"label": __("Project"),
		// 		"fieldtype": "MultiSelectList",
		// 		get_data: function(txt) {
		// 			return frappe.db.get_link_options('Project', txt);
		// 		}
		// 	},
		// 	{
		// 		"fieldname": "include_default_book_entries",
		// 		"label": __("Include Default Book Entries"),
		// 		"fieldtype": "Check",
		// 		"default": 1
		// 	},
		// 	{
		// 		"fieldname": "crrr",
		// 		"label": __("crrr"),
		// 		"fieldtype": "Check",
		// 		"default": 1,
		// 		"read_only":1,
		// 		"hidden":1,
		// 	},
		// );
// });

