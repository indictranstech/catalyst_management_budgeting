// Filter field "project_budget" in Sales Invoice Item table based on project_for_budget selected
cur_frm.fields_dict["items"].grid.get_field("project_budget").get_query = function(doc, cdt, cdn){
    var d = locals[cdt][cdn];
    return {
        filters:[
            ["project", "=", d.project_for_budget]
        ]
    }
}

// Reset project_budget && budget_account_head fields when project_for_budget field is changed
frappe.ui.form.on("Sales Invoice Item", "project_for_budget", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    d.project_budget = "";
    d.budget_account_head = "";
    frm.refresh_field('items');
});

frappe.ui.form.on("Sales Invoice Item", "project", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    d.project_budget = d.project_for_budget;
    frm.refresh_field('items');
});

// Reset budget_account_head field when project_budget field is changed
frappe.ui.form.on("Sales Invoice Item", "project_budget", function(frm, cdt, cdn) {
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


frappe.ui.form.on('Sales Invoice Item', {
    budget_account_head: function(frm, cdt, cdn) {
        var child = locals[cdt][cdn];
        if (child.project) {
            frappe.db.get_list('Account', {
                fields: ['name'],
                filters: {
                    'account_type': 'Cost of Goods Sold',
                    'company': frm.doc.company
                },
            }).then(records => {
                $.each(records, function(j, s) {
                    frappe.model.set_value(cdt, cdn, 'income_account', s.name);
                });
            });
        }
    }
});

frappe.ui.form.on('Sales Invoice', {
    before_save(frm) {
        frm.doc.items.forEach(item => {
            frappe.db.get_list('Contract', {
            fields: ['end_date'],
            filters: {party_name: frm.doc.customer, custom_project: item.project}
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
frappe.ui.form.on('Sales Invoice', {
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