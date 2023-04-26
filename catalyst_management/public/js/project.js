frappe.ui.form.on('Project', {
    
	expected_start_date(frm) {
		// your code here
        let row = frm.add_child('project_date_log', {
                'expected_start_date':cur_frm.doc.expected_start_date,
                "on":frappe.datetime.get_today()
            
        })
      cur_frm.refresh_fields("project_date_log");
	},
	expected_end_date(frm) {
		// your code here
        let row = frm.add_child('project_date_log', {
                "expected_end_date":cur_frm.doc.expected_end_date,
                "on":frappe.datetime.get_today()
            
        })
      cur_frm.refresh_fields("project_date_log");
	},
		
	
})