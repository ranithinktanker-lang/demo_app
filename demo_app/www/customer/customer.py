import frappe

@frappe.whitelist()
def save_customer(customer_name, email, address):
    try:
        doc = frappe.get_doc({
            "doctype": "Customer Info",  # <-- Doctype का सही नाम डालो
            "customer_name": customer_name,
            "email": email,
            "address": address
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        return True
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Customer Save Error")
        return False
