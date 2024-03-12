frappe.ui.form.on("Purchase Order", {
    refresh:function(frm){
        frm.set_query("project","items", function(doc, cdt, cdn) {
			var row = frappe.get_doc(cdt, cdn);
			return {
				filters: [
				    ["Project", "company", "=", frm.doc.company],
					
				]
            }
          
    })
}
})