frappe.ui.form.on('Employee Advance', {
    before_save(frm) {
        console.log("!!!!!!!!!!!!!!!!!!!")
            frappe.db.get_list('Contract', {
            fields: ['end_date'],
            filters: {party_name: frm.doc.employee, custom_project: frm.doc.project}
        }).then(records => {
            $.each(records, function(i, r) {
                if (r.end_date < frm.doc.posting_date) {
                    frm.set_df_property("custom_reason","hidden",0)
                }
            });
        });
      
    },
    refresh(frm){
        if (frm.doc.custom_reason != null){
            frm.set_df_property("custom_reason","hidden",0)
        }

    }
});

frappe.ui.form.on("Employee Advance", {
    refresh:function(frm){
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