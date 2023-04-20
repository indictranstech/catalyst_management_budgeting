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
				
		
	},
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