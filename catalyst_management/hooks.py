from . import __version__ as app_version

app_name = "catalyst_management"
app_title = "Catalyst Management Services"
app_publisher = "Simon Wanyama"
app_description = "Catalyst Management Services"
app_email = "simon.w@indictranstech.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/catalyst_management/css/catalyst_management.css"
# app_include_js = "/assets/catalyst_management/js/catalyst_management.js"

# include js, css files in header of web template
# web_include_css = "/assets/catalyst_management/css/catalyst_management.css"
# web_include_js = "/assets/catalyst_management/js/catalyst_management.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "catalyst_management/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_js = {
        "Sales Invoice" : "custom_script/sales_invoice/sales_invoice.js",
        "Purchase Invoice" : "custom_script/purchase_invoice/purchase_invoice.js",
        "Expense Claim": "custom_script/expense_claim/expense_claim.js",
        "Payroll Entry" : "custom_script/payroll_entry/payroll_entry.js",
        "Journal Entry" : "custom_script/journal_entry/journal_entry.js",
        "Payment Entry" : "public/js/payment_entry_custom.js",
        "Project" : "public/js/project.js",
	}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "catalyst_management.utils.jinja_methods",
#	"filters": "catalyst_management.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "catalyst_management.install.before_install"
# after_install = "catalyst_management.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "catalyst_management.uninstall.before_uninstall"
# after_uninstall = "catalyst_management.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "catalyst_management.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Project": {
		"before_insert": "catalyst_management.custom_script.project.project_custom.date_log",
	},
    "Sales Invoice":{   #for tax_item_break table
		"before_save":["catalyst_management.custom_script.sales_invoice.sales_invoice_custom.tax_item_break",#for tax_item_break table
                 	   "catalyst_management.custom_script.utils.frozen_validate_posting_date",
					  ]
	},
    "Sales Order":{    #for tax_item_break table
		"before_save":["catalyst_management.custom_script.sales_invoice.sales_invoice_custom.tax_item_break",#for tax_item_break table
                 	  "catalyst_management.custom_script.utils.frozen_validate_transaction_date",
                      ]
	},
    "Purchase Order":{
		"before_save":["catalyst_management.custom_script.sales_invoice.sales_invoice_custom.tax_item_break",#for tax_item_break table
                 	  "catalyst_management.custom_script.utils.frozen_validate_transaction_date",
                      ]
	},
    "Purchase Invoice":{
		"before_save":["catalyst_management.custom_script.sales_invoice.sales_invoice_custom.tax_item_break",#for tax_item_break table
                 	   "catalyst_management.custom_script.utils.frozen_validate_posting_date",
                      ]
	},
	"Employee Advance": {
		"before_save": "catalyst_management.custom_script.utils.frozen_validate_posting_date",
	},
	"Payment Entry": {
		"before_save": "catalyst_management.custom_script.utils.frozen_validate_posting_date",
	},
	"Expense Claim": {
		"before_save": "catalyst_management.custom_script.utils.frozen_validate_posting_date",
	},
	"Journal Entry": {
		"before_save": "catalyst_management.custom_script.utils.frozen_validate_posting_date",
	},
}

# Scheduled Tasks 
# ---------------

# scheduler_events = {
#	"all": [
#		"catalyst_management.tasks.all"
#	],
#	"daily": [
#		"catalyst_management.tasks.daily"
#	],
#	"hourly": [
#		"catalyst_management.tasks.hourly"
#	],
#	"weekly": [
#		"catalyst_management.tasks.weekly"
#	],
#	"monthly": [
#		"catalyst_management.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "catalyst_management.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"hrms.overrides.employee_payment_entry.get_payment_entry_for_employee": "catalyst_management.custom_script.overrides.employee_payment_entry.get_payment_entry_for_employee"
}

# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "catalyst_management.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["catalyst_management.utils.before_request"]
# after_request = ["catalyst_management.utils.after_request"]

# Job Events
# ----------
# before_job = ["catalyst_management.utils.before_job"]
# after_job = ["catalyst_management.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"catalyst_management.auth.validate"
# ]

fixtures = [
    'Custom Field',
    {
		"dt": "Translation", "filters": [
			[
				"name", "in", [
					"d0874f47be",
				]
			]
		]
	},
    {
		"dt": "Property Setter", "filters": [
			[
				"name", "in", [
                    # Expense Claim
					"Expense Claim-expense_approver-read_only",
                    "Expense Claim-expense_approver-fetch_from",
                    "Expense Claim-approval_status-read_only",
                    "Expense Claim-approval_status-default",
                    
                    # Payment Entry
					"Payment Entry-reference_no-depends_on",
                    "Payment Entry-reference_date-allow_on_submit",
                    "Payment Entry-payment_type-label",
                    "Payment Entry-type_of_payment-label",
				]
			]
		]
	},
     {
		"dt": "Journal Entry", "filters": [
			[
				"name", "in", [
					"Journal Entry-territory_details",
                    "Journal Entry-territory"
				]
			]
		]
	},
    {
		"dt": "Purchase Invoice", "filters": [
			[
				"name", "in", [
					"Purchase Invoice-territory_details",
                    "Purchase Invoice-territory"
				]
			]
		]
	},
    {
		"dt": "Payroll Employee Detail", "filters": [
			[
				"name", "in", [
					"Payroll Employee Detail-project_budgeting",
                    "Payroll Employee Detail-project_for_budget",
                    "Payroll Employee Detail-project_budget",
                    "Payroll Employee Detail-column_break_irse9",
                    "Payroll Employee Detail-budget_account_head"
				]
			]
		]
	},
    {
		"dt": "Journal Entry Account", "filters": [
			[
				"name", "in", [
					"Journal Entry Account-project_budgeting",
                    "Journal Entry Account-project_for_budget",
                    "Journal Entry Account-project_budget",
                    "Journal Entry Account-column_break_rhnkg",
                    "Journal Entry Account-budget_account_head"
				]
			]
		]
	},
    {
		"dt": "Expense Claim Detail", "filters": [
			[
				"name", "in", [
					"Expense Claim Detail-project_budgeting",
                    "Expense Claim Detail-project_for_budget",
                    "Expense Claim Detail-project_budget",
                    "Expense Claim Detail-column_break_zgdqc",
                    "Expense Claim Detail-budget_account_head"
				]
			]
		]
	},
    {
		"dt": "Purchase Invoice Item", "filters": [
			[
				"name", "in", [
					"Purchase Invoice Item-project_budgeting",
                    "Purchase Invoice Item-project_for_budget",
                    "Purchase Invoice Item-project_budget",
                    "Purchase Invoice Item-column_break_aipxo",
                    "Purchase Invoice Item-budget_account_head"
				]
			]
		]
	},
    {
		"dt": "Sales Invoice Item", "filters": [
			[
				"name", "in", [
					"Sales Invoice Item-project_budgeting",
                    "Sales Invoice Item-project_for_budget",
                    "Sales Invoice Item-project_budget",
                    "Sales Invoice Item-column_break_mnjj5",
                    "Sales Invoice Item-budget_account_head"
				]
			]
		]
	},
    {
		"dt": "Donor", "filters": [
			[
				"name", "in", [
					"Donor-pan_number",
                    "Donor-aadhar_number",
                    "Donor-project_budgeting",
                    "Donor-project_for_budget",
                    "Donor-project_budget",
                    "Donor-column_break_ilgv0",
                    "Donor-budget_account_head"
				]
			]
		]
	},
    {
		"dt": "Donation", "filters": [
			[
				"name", "in", [
					"Donation-pan_number",
                    "Donation-aadhar_number",
                    "Donation-project_budgeting",
                    "Donation-project_for_budget",
                    "Donation-project_budget",
                    "Donation-column_break_kgqf5",
                    "Donation-budget_account_head"
				]
			]
		]
	},
    {
		"dt": "Monthly Distribution Percentage", "filters": [
			[
				"name", "in", [
					"Monthly Distribution Percentage-amount_allocation",
				]
			]
		]
	},

]
