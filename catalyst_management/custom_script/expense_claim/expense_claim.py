import frappe

def validate(doc, method):
    if doc.workflow_state:
        if (doc.workflow_state == 'Send For Review'):
            doc.custom_prepared_on = doc.modified
        elif (doc.workflow_state == 'Send For Approval'):
            doc.custom_reviewed_on = doc.modified
        elif (doc. workflow_state == 'Approved'):
            doc.custom_approved_on = doc.modified

    