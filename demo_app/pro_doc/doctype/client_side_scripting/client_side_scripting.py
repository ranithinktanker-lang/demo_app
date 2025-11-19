# Copyright (c) 2025, demo_app and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ClientSideScripting(Document):
	pass

@frappe.whitelist(allow_guest=True) 
def frappe_call(msg):
	print("--------------------------")
	print('=--------------------------------->',msg)
	# import time
	# time.sleep(5)
	# frappe.msgprint(msg)



	return "Hii this message from frappe_call"

