// for frozen data
frappe.ui.form.on('Sales Invoice', {
    refresh(frm) {
       // your code here
 
       frappe.call({
          method: 'frappe.client.get_list',
          args: {
             'doctype': 'Frozen data child',
             'filters': {
                'doctypes': cur_frm.doc.doctype
             },
             'fields': [
                'valid_till',
                'role',
             ],
             parent: 'Frozen Data',
 
          },
          callback: function (r) {
             if (!r.exc) {
                // code snippet
                console.log(r)
                if (r.message[0]) {
 
                   const dd = r.message[0]
 
                   if (!frappe.user_roles.includes(dd.role)) {
                      if (dd.valid_till <= get_today()) {
                         $.each(cur_frm.fields_dict, function (fieldname, field) {
                            field.df.read_only = 1;
                            cur_frm.refresh_field(fieldname)
                         });
                      }
 
                   }
 
                }
             }
          }
       });
 
    },
 
 
    onload(frm) {
       // your code here
 
       frappe.call({
          method: 'frappe.client.get_list',
          args: {
             'doctype': 'Frozen data child',
             'filters': {
                'doctypes': cur_frm.doc.doctype
             },
             'fields': [
                'valid_till',
                'role',
             ],
             parent: 'Frozen Data',
 
          },
          callback: function (r) {
             if (!r.exc) {
                // code snippet
                console.log(r)
                if (r.message[0]) {
 
                   const dd = r.message[0]
 
                   if (!frappe.user_roles.includes(dd.role)) {
                      if (dd.valid_till <= get_today()) {
                         $.each(cur_frm.fields_dict, function (fieldname, field) {
                            field.df.read_only = 1;
                            cur_frm.refresh_field(fieldname)
                         });
                      }
 
                   }
 
                }
             }
          }
       });
 
    },
 
 
 })







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