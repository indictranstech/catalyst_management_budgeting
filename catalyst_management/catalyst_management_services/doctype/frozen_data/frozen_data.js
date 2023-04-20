// Copyright (c) 2023, Simon Wanyama and contributors
// For license information, please see license.txt

frappe.ui.form.on('Frozen Data', {
	refresh: function(frm) {

		frm.set_query('doctypes', 'frozen_data_child', () => {
			return {
				filters: {
					name:['in',  ['Sales Invoice','Purchase Invoice','Journal Entry','Purchase Order','Receipt / Tranfer entry','Payment Entry','Employee Advance','Expense Claim'] ]
				}
			}
		})

	},
	onload: function(frm) {

		frm.set_query('doctypes', 'frozen_data_child', () => {
			return {
				filters: {
					name:['in',  ['Sales Invoice','Purchase Invoice','Journal Entry','Purchase Order','Receipt / Tranfer entry','Payment Entry','Employee Advance','Expense Claim'] ]
				}
			}
		})

	},
});

frappe.ui.form.on('Frozen data child', {
	freeze_date(frm,cdt,cdn) {
		// your code here
		const d = locals[cdt][cdn] 
		if(d.grace_days){
		    frappe.model.set_value(d.doctype,d.name,{"valid_till":frappe.datetime.add_days(d.freeze_date,d.grace_days)})
		}
	},

	grace_days(frm,cdt,cdn) {
		// your code here
		const d = locals[cdt][cdn] 
		if(d.freeze_date){
		    frappe.model.set_value(d.doctype,d.name,{"valid_till":frappe.datetime.add_days(d.freeze_date,d.grace_days)})
		}
	},
	
})
