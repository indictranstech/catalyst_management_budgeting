import frappe


def date_log(doc,method):
    my_dict = {}
    doc.append('custom_project_date_log',{
            'expected_start_date':doc.expected_start_date,
            "expected_end_date":doc.expected_end_date,
            "on":frappe.utils.today()
        })
