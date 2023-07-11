// Copyright (c) 2023, Simon Wanyama and contributors
// For license information, please see license.txt

frappe.ui.form.on('Budget Account Head', {
	refresh: function(frm) {
		console.log('js')
		frm.set_query("chart_of_account_head", "budget_account_mapping", function(doc, cdt, cdn) {
    		return {
    			filters: {
    				company: cur_frm.doc.comapny,
    			}
    		};
    	});
	},
	onload: function(frm) {
		console.log('jonload')
		frm.set_query("chart_of_account_head", "budget_account_mapping", function(doc, cdt, cdn) {
    		return {
    			filters: {
    				company: cur_frm.doc.comapny,
    			}
    		};
    	});
	}
});
