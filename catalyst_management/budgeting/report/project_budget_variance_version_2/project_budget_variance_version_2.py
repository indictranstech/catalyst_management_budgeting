import frappe
from frappe import _
from frappe.utils import getdate
from datetime import datetime, timedelta


def execute(filters=None):
    return get_columns(), get_data(filters)

def get_columns():
    return [
        {
            'fieldname': 'period',
            'label': _('Accounting Period'),
            'fieldtype': 'Link',
            'options': 'Accounting Period'
        },
        {
            "fieldname": "start_date",
            "fieldtype": "Date",
            "label": "Start Date",
        },
        {
            "fieldname": "end_date",
            "fieldtype": "Date",
            "label": "End Date",
        },
        {
            'fieldname': 'project',
            'label': _('Project'),
            'fieldtype': 'Link',
            'options': 'Project Budgeting'
        },
        {
            'fieldname': 'parent_budget_account_head',
            'label': _('Parent Budget Account Head'),
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'budget_account_head',
            'label': _('Budget Account Head'),
            'fieldtype': 'Link',
            'options': 'Budget Account Head'
        },
        {
            'fieldname': 'amount',
            'label': _('Budget Amount'),
            'fieldtype': 'Currency',
        },
        {
            'fieldname': 'selected_period_budget_amount',
            'label': _('Selected Period Budget Amount'),
            'fieldtype': 'Currency',
        },
        {
            'fieldname': 'actual_amount',
            'label': _('Actual Amount'),
            'fieldtype': 'Currency',
        },
        {
            'fieldname': 'selected_actual_amount',
            'label': _('Selected Actual'),
            'fieldtype': 'Currency',
        },
        {
            'fieldname': 'variance',
            'label': _('Variance'),
            'fieldtype': 'Currency',
        },
        {
            'fieldname': 'variance_percentage',
            'label': _('Variance (%)'),
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'total_utilisation',
            'label': _('Total Utilisation %'),
            'fieldtype': 'percent',
        },
        {
            'fieldname': 'selected_utilisation',
            'label': _('Selected Utilisation %'),
            'fieldtype': 'percent',
        },
        {
            'fieldname': 'chart_of_account_head',
            'label': _('Chart of Account Head'),
            'fieldtype': 'Link',
            'options': 'Account',
        },
        {
            'fieldname': 'name',
            'label': _('name'),
            'fieldtype': 'Link',
            'options': 'Budget Account Mapping',
            'hidden': 1
        },
    ]

def get_data(filters):
    conditions = []
    if filters.get("period"): conditions.append(["period", "=", filters.get("period")])
    if filters.get("project"): conditions.append(["parent", "=", filters.get("project")])
    if filters.get("budget_account_head"): conditions.append(["budget_account_head", "=", filters.get("budget_account_head")])
    conditions.append({"docstatus": 1})

    budget_account_map = frappe.db.get_all('Budget Account Mapping', [
        "name",
        "period",
        "budget_account_head",
        "parent_budget_account_head",
        "monthly_distribution",
        "chart_of_account_head",
        "amount",
        "parent"
    ], filters=conditions)

    # Pre-fetch data for accounting periods
    periods = {p.name: p for p in frappe.get_all("Accounting Period", fields=["name", "start_date", "end_date"])}
    for d in budget_account_map:
        period = periods[d["period"]]
        start_date =  period.start_date
        end_date =  period.end_date
        month_start = period.start_date
        month_end = period.end_date

    # Pre-fetch data for actual amounts
    # project_heads = [(d['parent'], d['budget_account_head']) for d in budget_account_map]
    # actuals = get_all_actual_amounts(project_heads, getdate(filters.get("from_date")),getdate(filters.get("to_date")) )
    # print("\n\n\n\n8888888888",actuals)

    data = []
    for d in budget_account_map:
        d["project"] = d["parent"]
        period = periods[d["period"]]
        d["start_date"] = period.start_date
        d["end_date"] = period.end_date

        actual = actual_amounts(d["project"], d["budget_account_head"], d["start_date"], d["end_date"],getdate(filters.get("from_date")),getdate(filters.get("to_date")))
        print("\n\n\n\n",actual)

        d["actual_amount"] = actual[0]
        d["selected_actual_amount"] = actual[1]

        d['selected_period_budget_amount'] = 0
        if d['monthly_distribution']:
            over_all_percentage = get_month_names_and_selected_period_over_all_percentage(d['monthly_distribution'], filters.get("from_date"), filters.get("to_date"))
            if over_all_percentage:
                d['selected_period_budget_amount'] = round(over_all_percentage)

        d["variance"] = d["amount"] - d["actual_amount"]
        d['total_utilisation'] = round(d["actual_amount"] / d['amount'] * 100) if d['amount'] else 0
        d['selected_utilisation'] = round(d["selected_actual_amount"] / d['selected_period_budget_amount'] * 100) if d['selected_period_budget_amount'] else 0
        d["variance_percentage"] = round((d["variance"] / d["amount"]) * 100) if d["amount"] else 0

        data.append(d)

    return data

def actual_amounts(project, head, start_date, end_date, month_start, month_end):
    '''
    Actual Amounts for Journal Entry, Expense Claim, and Purchase Entry
    We make the total for each and add up, handling date, project, and budget_account_head conditions
    '''

    # Initialize totals
    si_total, pi_total, ec_total, je_total = 0, 0, 0, 0
    month_si_total, month_pi_total, month_ec_total, month_je_total = 0, 0, 0, 0

    # Fetch Sales Invoice Items
    si_amount = frappe.get_all('Sales Invoice Item', filters={
        "project_for_budget": project,
        "budget_account_head": head,
        "docstatus": 1
    }, fields=["parent", "amount"])

    # Fetch Purchase Invoice Items
    pi_amount = frappe.get_all('Purchase Invoice Item', filters={
        "project_for_budget": project,
        "budget_account_head": head,
        "docstatus": 1
    }, fields=["parent", "amount"])

    # Fetch Expense Claim Details
    ec_amount = frappe.get_all('Expense Claim Detail', filters={
        "project_for_budget": project,
        "budget_account_head": head,
        "docstatus": 1
    }, fields=["parent", "amount"])

    # Fetch Journal Entry Accounts
    je_amount = frappe.get_all('Journal Entry Account', filters={
        "project_for_budget": project,
        "budget_account_head": head,
        "docstatus": 1
    }, fields=["parent", "debit_in_account_currency"])

    # Get posting dates for all documents in one go
    si_docs = frappe.get_all('Sales Invoice', filters={"name": ["in", [i['parent'] for i in si_amount]]}, fields=["name", "posting_date"])
    pi_docs = frappe.get_all('Purchase Invoice', filters={"name": ["in", [i['parent'] for i in pi_amount]]}, fields=["name", "posting_date"])
    ec_docs = frappe.get_all('Expense Claim', filters={"name": ["in", [i['parent'] for i in ec_amount]]}, fields=["name", "posting_date"])
    je_docs = frappe.get_all('Journal Entry', filters={"name": ["in", [i['parent'] for i in je_amount]]}, fields=["name", "posting_date"])

    # Create dictionaries for quick lookup of posting dates
    si_date_map = {d.name: d.posting_date for d in si_docs}
    pi_date_map = {d.name: d.posting_date for d in pi_docs}
    ec_date_map = {d.name: d.posting_date for d in ec_docs}
    je_date_map = {d.name: d.posting_date for d in je_docs}

    # Aggregate totals
    for i in si_amount:
        posting_date = si_date_map.get(i['parent'])
        if posting_date:
            if start_date <= posting_date <= end_date:
                si_total += i['amount']
            if month_start <= posting_date <= month_end and start_date <= posting_date <= end_date:
                month_si_total += i['amount']

    for i in pi_amount:
        posting_date = pi_date_map.get(i['parent'])
        if posting_date:
            if start_date <= posting_date <= end_date:
                pi_total += i['amount']
            if month_start <= posting_date <= month_end and start_date <= posting_date <= end_date:
                month_pi_total += i['amount']

    for i in ec_amount:
        posting_date = ec_date_map.get(i['parent'])
        if posting_date:
            if start_date <= posting_date <= end_date:
                ec_total += i['amount']
            if month_start <= posting_date <= month_end and start_date <= posting_date <= end_date:
                month_ec_total += i['amount']

    for i in je_amount:
        posting_date = je_date_map.get(i['parent'])
        if posting_date:
            if start_date <= posting_date <= end_date:
                if i['debit_in_account_currency']:
                    je_total += i['debit_in_account_currency']
            if month_start <= posting_date <= month_end and start_date <= posting_date <= end_date:
                if i['debit_in_account_currency']:
                    month_je_total += i['debit_in_account_currency']

    return [si_total + pi_total + ec_total + je_total, month_si_total + month_pi_total + month_ec_total + month_je_total]


def get_month_names_and_selected_period_over_all_percentage(monthly_distribution, start_date, end_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    current_date = start_date
    month_names = []

    month_names_list = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    while current_date <= end_date:
        month_names.append(month_names_list[current_date.month - 1])
        next_month = current_date.month + 1 if current_date.month < 12 else 1
        next_year = current_date.year if current_date.month < 12 else current_date.year + 1
        current_date = current_date.replace(month=next_month, year=next_year, day=1)

    over_all_percentage = frappe.db.sql(f"""
         select 
				    	sum(mdp.amount_allocation) as percentage_allocation,
				        count(mdp.name),
				        mdp.month
				       
				       from `tabMonthly Distribution` md
				       left join `tabMonthly Distribution Percentage` mdp on md.name  = mdp.parent
				       where md.name = '{monthly_distribution}'  and  mdp.month in {tuple(['month']+month_names)} 
				       
				       
				        """,as_dict=1)

    return over_all_percentage[0]['percentage_allocation'] if over_all_percentage else 0
