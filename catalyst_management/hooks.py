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
        "Sales Order" : "custom_script/sales_order/sales_order.js"


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

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }
doc_events = {
	"Project": {
		"before_save": "catalyst_management.custom_script.project.project_custom.date_log",
	},
	"Monthly Distribution": {
		"before_save": "catalyst_management.custom_script.monthly_distribution.monthly_distribution.before_save",
	},
	"Project Budgeting": {
		"before_save": "catalyst_management.custom_script.project_budgeting.project_budgeting.before_save",
		"on_update_after_submit": "catalyst_management.custom_script.project_budgeting.project_budgeting.before_save",
	},
	"Purchase Invoice":{
		"validate": "catalyst_management.custom_script.purchase_invoice.purchase_invoice.validate",

	},
	"Purchase Order":{
		"validate": "catalyst_management.custom_script.purchase_order.purchase_order.validate",
	},
	"Expense Claim":{
		"validate": "catalyst_management.custom_script.expense_claim.expense_claim.validate",
	},
	"Sales Order":{
		"validate": "catalyst_management.custom_script.sales_order.sales_order.validate",
	},
	"Sales Invoice":{
		"validate": "catalyst_management.custom_script.sales_invoice.sales_invoice.validate",
	},
	"Payment Entry":{
		"validate": "catalyst_management.custom_script.payment_entry.payment_entry.validate",
	},
	"Journal Entry":{
		"validate": "catalyst_management.custom_script.journal_entry.journal_entry.validate",
	},
	"Employee Advance":{
		"validate": "catalyst_management.custom_script.employee_advance.employee_advance.validate",
	},
	
	
	# "Journal Entry": {
	# 	"before_save": "catalyst_management.custom_script.journal_entry.journal_entry.before_save",
	# }
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
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "catalyst_management.event.get_events"
# }
#
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
		"dt": "Property Setter", "filters": [
			[
				"name", "in", [
					"Expense Claim Detail-sanctioned_amount-reqd",
                    "Error Log-seen-default",
                    "Expense Claim-posting_date-hidden"
				]
			]
		]
	},'Role','Workflow','Workflow State','Workflow Action Master',
]
