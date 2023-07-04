frappe.ui.form.on('Expense Claim', {

    onload: function(frm) {
        frm.set_value('date', frm.doc.posting_date);
    },
    date: function(frm) {
        frm.set_value('posting_date', frm.doc.date);
    },
    posting_date: function(frm) {
        frm.set_value('date', frm.doc.posting_date);
    },


});

cur_frm.fields_dict["expenses"].grid.get_field("project_budget").get_query = function(doc, cdt, cdn){
    var d = locals[cdt][cdn];
	return {
		filters:[
			["project", "=", d.project_for_budget]
		]
	}
}

// Reset project_budget && budget_account_head fields when project_for_budget field is changed
frappe.ui.form.on("Expense Claim Detail", "project_for_budget", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    d.project_budget = "";
    d.budget_account_head = "";
    frm.refresh_field('expenses');
});

// Reset budget_account_head field when project_budget field is changed
frappe.ui.form.on("Expense Claim Detail", "project_budget", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    d.budget_account_head = "";
    frm.refresh_field('expenses');
});

cur_frm.fields_dict["expenses"].grid.get_field("budget_account_head").get_query = function(doc, cdt, cdn){
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