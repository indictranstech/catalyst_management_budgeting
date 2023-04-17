// Copyright (c) 2023, Simon Wanyama and contributors
// For license information, please see license.txt
/* eslint-disable */

// frappe.query_reports["Profit and Loss Statement Project Wise"] = {
// 	"filters": [

// 	]
// };


frappe.require("assets/erpnext/js/financial_statements.js", function() {
	frappe.query_reports["Profit and Loss Statement Project Wise"] = $.extend({},
		erpnext.financial_statements);

	erpnext.utils.add_dimensions('Profit and Loss Statement Project Wise', 10);

	frappe.query_reports["Profit and Loss Statement Project Wise"]["filters"].push(
		{
			"fieldname": "project",
			"label": __("Project"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Project', txt);
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

