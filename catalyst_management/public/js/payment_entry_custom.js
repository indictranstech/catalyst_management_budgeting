frappe.ui.form.on('Payment Entry', {
	validate(frm) {
		// your code here
		if (cur_frm.doc.reference_no == undefined || cur_frm.doc.reference_no == "" ){
		    frm.set_value('reference_no', '_')
		    frm.refresh_field('reference_no');
		}
		if (cur_frm.doc.reference_date == undefined || cur_frm.doc.reference_date == "" ){
		    frm.set_value('reference_date', frappe.datetime.get_today())
		    frm.refresh_field('reference_date');
		}
				
		
	}
})