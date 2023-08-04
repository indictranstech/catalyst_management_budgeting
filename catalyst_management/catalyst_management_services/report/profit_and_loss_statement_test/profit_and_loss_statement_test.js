// // Copyright (c) 2023, Simon Wanyama and contributors
// // For license information, please see license.txt
// /* eslint-disable */

// frappe.query_reports["Profit and Loss Statement Test"] = {
// 	"filters": [

// 	]
// };
// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt


frappe.require("assets/erpnext/js/financial_statements.js", function() {
	frappe.query_reports["Profit and Loss Statement Test"] = $.extend({},
		erpnext.financial_statements);

	erpnext.utils.add_dimensions('Profit and Loss Statement Test', 10);

	frappe.query_reports["Profit and Loss Statement Test"]["filters"].push(
		{
			"fieldname": "include_default_book_entries",
			"label": __("Include Default Book Entries"),
			"fieldtype": "Check",
			"default": 1
		}
	);
});
