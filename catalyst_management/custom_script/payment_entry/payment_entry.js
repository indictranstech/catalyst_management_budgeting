frappe.ui.form.on('Payment Entry', {
	refresh(frm) {
	 frm.set_query("project", function(doc, cdt, cdn) {
			var row = frappe.get_doc(cdt, cdn);
			return {
				filters: [
				    ["Project", "company", "=", frm.doc.company],
					
				]
            }
          
    })
	}
})

