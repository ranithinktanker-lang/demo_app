import frappe

@frappe.whitelist()
def save_user_detail(full_name, email, phone=None, dob=None,
                     gender=None, address=None, city=None,
                     state=None, country=None):
    if not full_name or not email:
        frappe.throw("Full Name and Email required")
    doc = frappe.get_doc({
        "doctype": "User Detail",
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "dob": dob,
        "gender": gender,
        "address": address,
        "city": city,
        "state": state,
        "country": country
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return doc.name

@frappe.whitelist()
def update_user_detail(name, full_name, email, phone=None, dob=None,
                       gender=None, address=None, city=None,
                       state=None, country=None):
    doc = frappe.get_doc("User Detail", name)
    doc.full_name = full_name
    doc.email = email
    doc.phone = phone
    doc.dob = dob
    doc.gender = gender
    doc.address = address
    doc.city = city
    doc.state = state
    doc.country = country
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    return doc.name

@frappe.whitelist()
def delete_user_detail(name):
    frappe.delete_doc("User Detail", name, ignore_permissions=True)
    frappe.db.commit()
    return True

@frappe.whitelist()
def get_all_users():
    """Return all users for table display"""
    users = frappe.get_all("User Detail", fields=["name", "full_name", "email", "phone", "dob", "gender", "address", "city", "state", "country"])
    return users
