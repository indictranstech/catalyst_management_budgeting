import frappe
from frappe.utils import flt, nowdate

import erpnext
from erpnext.accounts.doctype.payment_entry.payment_entry import (
	PaymentEntry,
	get_bank_cash_account,
	get_reference_details,
)
from erpnext.accounts.utils import get_account_currency


@frappe.whitelist()
def get_payment_entry_for_employee(dt, dn, party_amount=None, bank_account=None, bank_amount=None):
	"""Function to make Payment Entry for Employee Advance, Gratuity, Expense Claim"""
	doc = frappe.get_doc(dt, dn)

	party_type = "Employee"
	party_account = get_party_account(doc)
	party_account_currency = get_account_currency(party_account)
	payment_type = "Pay"
	grand_total, outstanding_amount = get_grand_total_and_outstanding_amount(
		doc, party_amount, party_account_currency
	)

	# bank or cash
	bank = get_bank_cash_account(doc, bank_account)

	paid_amount, received_amount = get_paid_amount_and_received_amount(
		doc, party_account_currency, bank, outstanding_amount, payment_type, bank_amount
	)

	pe = frappe.new_doc("Payment Entry")
	pe.payment_type = payment_type
	pe.company = doc.company
	pe.cost_center = doc.get("cost_center")
	pe.posting_date = nowdate()
	pe.mode_of_payment = doc.get("mode_of_payment")
	pe.party_type = "Employee"
	pe.party = doc.get("employee")
	pe.contact_person = doc.get("contact_person")
	pe.contact_email = doc.get("contact_email")
	pe.letter_head = doc.get("letter_head")
	pe.paid_from = bank.account
	pe.paid_to = party_account
	pe.paid_from_account_currency = bank.account_currency
	pe.paid_to_account_currency = party_account_currency
	pe.paid_amount = paid_amount
	pe.received_amount = received_amount

	pe.project = doc.get('project') # added this to fetch project [Simon]

	pe.append(
		"references",
		{
			"reference_doctype": dt,
			"reference_name": dn,
			"bill_no": doc.get("bill_no"),
			"due_date": doc.get("due_date"),
			"total_amount": grand_total,
			"outstanding_amount": outstanding_amount,
			"allocated_amount": outstanding_amount,
		},
	)

	pe.setup_party_account_field()
	pe.set_missing_values()

	if party_account and bank:
		reference_doc = None
		if dt == "Employee Advance":
			reference_doc = doc
		pe.set_exchange_rate(ref_doc=reference_doc)
		pe.set_amounts()

	return pe

def get_party_account(doc):
	party_account = None

	if doc.doctype == "Employee Advance":
		party_account = doc.advance_account
	elif doc.doctype in ("Expense Claim", "Gratuity"):
		party_account = doc.payable_account

	return party_account


def get_grand_total_and_outstanding_amount(doc, party_amount, party_account_currency):
	grand_total = outstanding_amount = 0

	if party_amount:
		grand_total = outstanding_amount = party_amount

	elif doc.doctype == "Expense Claim":
		grand_total = flt(doc.total_sanctioned_amount) + flt(doc.total_taxes_and_charges)
		outstanding_amount = flt(doc.grand_total) - flt(doc.total_amount_reimbursed)

	elif doc.doctype == "Employee Advance":
		grand_total = flt(doc.advance_amount)
		outstanding_amount = flt(doc.advance_amount) - flt(doc.paid_amount)
		if party_account_currency != doc.currency:
			grand_total = flt(doc.advance_amount) * flt(doc.exchange_rate)
			outstanding_amount = (flt(doc.advance_amount) - flt(doc.paid_amount)) * flt(doc.exchange_rate)

	elif doc.doctype == "Gratuity":
		grand_total = doc.amount
		outstanding_amount = flt(doc.amount) - flt(doc.paid_amount)

	else:
		if party_account_currency == doc.company_currency:
			grand_total = flt(doc.get("base_rounded_total") or doc.base_grand_total)
		else:
			grand_total = flt(doc.get("rounded_total") or doc.grand_total)
		outstanding_amount = grand_total - flt(doc.advance_paid)

	return grand_total, outstanding_amount


def get_paid_amount_and_received_amount(
	doc, party_account_currency, bank, outstanding_amount, payment_type, bank_amount
):
	paid_amount = received_amount = 0

	if party_account_currency == bank.account_currency:
		paid_amount = received_amount = abs(outstanding_amount)

	elif payment_type == "Receive":
		paid_amount = abs(outstanding_amount)
		if bank_amount:
			received_amount = bank_amount
		else:
			received_amount = paid_amount * doc.get("conversion_rate", 1)
			if doc.doctype == "Employee Advance":
				received_amount = paid_amount * doc.get("exchange_rate", 1)

	else:
		received_amount = abs(outstanding_amount)
		if bank_amount:
			paid_amount = bank_amount
		else:
			# if party account currency and bank currency is different then populate paid amount as well
			paid_amount = received_amount * doc.get("conversion_rate", 1)
			if doc.doctype == "Employee Advance":
				paid_amount = received_amount * doc.get("exchange_rate", 1)

	return paid_amount, received_amount

