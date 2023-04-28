import frappe
import json

def tax_item_break(doc,method):
    mya = []
    for i in doc.items:
        my_dict ={}
        my_dict['item_code'] = i.item_code
        js_di = json.loads(i.item_tax_rate)
        for j in doc.taxes:
            if i.item_tax_rate and str(j.account_head) in  js_di:
                if js_di[str(j.account_head)] != None or js_di[str(j.account_head)] != '':
                    my_dict[str(j.account_head)] = f"""({js_di[str(j.account_head)]} %) {(i.amount*js_di[str(j.account_head)])/100}"""
                else:
                    my_dict[str(j.account_head)] = ''
        mya.append(my_dict)

    html = ""
    html  = html + "<table class='table table-bordered'>"
    html  = html + "<tr>"
    for key in mya[0].keys():
        html = html + f"<th>{key}</th>"
    html = html +  "</tr>"
    for row in mya:
        html  = html + "<tr>"
        for key, value in row.items():
            html = html +  f"<td>{value}</td>"
        html = html +  "</tr>"
    html = html +  "</table>"
    doc.taxes_and_charges_calculation_based_on_item_tax_template= html

    frappe.db.commit()
    # Return the HTML code
    # frappe.throw(html)