cur_frm.fields_dict["items"].grid.get_field("project_budget").get_query = function(doc, cdt, cdn){
    var d = locals[cdt][cdn];
	return {
		filters:[
			["project", "=", d.project_for_budget]
		]
	}
}

// Reset project_budget && budget_account_head fields when project_for_budget field is changed
frappe.ui.form.on("Purchase Invoice Item", "project_for_budget", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    d.project_budget = "";
    d.budget_account_head = "";
    frm.refresh_field('items');
});

frappe.ui.form.on("Purchase Invoice Item", "project", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    d.project_budget = d.project_for_budget;
    frm.refresh_field('items');
});

// Reset budget_account_head field when project_budget field is changed
frappe.ui.form.on("Purchase Invoice Item", "project_budget", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    d.budget_account_head = "";
    frm.refresh_field('items');
});

cur_frm.fields_dict["items"].grid.get_field("budget_account_head").get_query = function(doc, cdt, cdn){
    var d = locals[cdt][cdn];

    var return_first = function () {
        var tmp = null;
        frappe.call({
            method: "catalyst_management.custom_script.fetch_budget_account_head.budget_account_head",
            args: {
                "project": d.project_budget
            },
            async: false, // This was a charm after 18 hours
            callback: function(r){
                tmp = r.message
            }
        })
        return tmp;
    }();

    // Filter Now
    return {
        filters:[
            ["Budget Account Head", "name", "in", return_first]
        ]
    }
}

frappe.ui.form.on('Purchase Invoice Item', {
    budget_account_head(frm) {
        frappe.call({
            method: 'catalyst_management.custom_script.purchase_invoice.purchase_invoice.update_chart_of_account',
            args: {
                doc: frm.doc
            },
            callback: function(r) {
                if (r.message) {
                    // Loop through each row in the child table
                    frm.doc.items.forEach(function(item) {
                        // Set the value of the expense_account field for each row
                        frappe.model.set_value(item.doctype, item.name, 'expense_account', r.message);
                    });

                    refresh_field('items');
                }
            }
        });
    }
});




frappe.ui.form.on('Purchase Invoice', {
    before_save(frm) {
        frm.doc.items.forEach(item => {
            frappe.db.get_list('Contract', {
            fields: ['end_date'],
            filters: {party_name: frm.doc.supplier, custom_project: item.project}
        }).then(records => {
            $.each(records, function(i, r) {
                if (r.end_date < frm.doc.posting_date) {
                    frm.set_df_property("custom_reason","hidden",0)
                }
            });
        });
        })
    },
    refresh(frm){
        if (frm.doc.custom_reason != null){
            frm.set_df_property("custom_reason","hidden",0)
        }

    }
});
frappe.ui.form.on('Purchase Invoice', {
    before_save(frm) {
        frm.doc.items.forEach(item => {
        frappe.db.get_list('Project Budgeting', {
        fields: ['custom_total_actual_amount'],
        filters: {name: item.project
        },
    }).then(records => {
        $.each(records, function(i, j) {
            console.log("j.custom_total_actual_amount ",j.custom_grand_total )
            frm.set_value('custom_total_amount_from_invoice', frm.doc.total);
            frm.set_value('custom_total_amount_from_project_budget', j.custom_total_actual_amount);
            frm.set_value('custom_total_amount',frm.doc.total + j.custom_total_actual_amount  );
    });
    })
    })
}
});

frappe.ui.form.on("Purchase Invoice", {
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