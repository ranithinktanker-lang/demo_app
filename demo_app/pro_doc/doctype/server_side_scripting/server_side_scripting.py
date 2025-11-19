# Copyright (c) 2025, demo_app and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class ServerSideScripting(Document):
	@frappe.whitelist()
	# -->evnets
	
	# def before_save(self):
	# 	frappe.msgprint("hello")

	# def validate(self):
	# 	frappe.msgprint("validate event")

	# def after_insert(self):
	# 	frappe.throw("from after_insert event")

	# def before_insert(self):
	# 	frappe.msgprint("from before_insert event")
    
	# def on_update(self):
	# 	frappe.msgprint("from on_update event")
    
	# def before_submit(self):
	# 	frappe.msgprint("from before_submit event")

	# def on_submit(self):
	# 	frappe.msgprint("from on_submit event")
	
	# def on_cancel(self):
	# 	frappe.msgprint("from on_cancel")

	# def on_trash(self):
	# 	frappe.msgprint("from on_trash event")

	# def after_delete(self):
	# 	frappe.msgprint("from after_delete event")

# -->fetching a value
	# def before_save(self):
	# 	first_name=self.first_name
	# 	last_name=self.last_name
	# 	frappe.msgprint(f" First Name is:{first_name} and last name is {last_name}")


# -->get_doc --for update

	# def validate(self):
	# 	self.get_document()
	# def get_document(self):
	# 	doc=frappe.get_doc("Client Side Scripting",self.client_side_doc)
	# 	frappe.msgprint(f"The First Name is{doc.first_name} And Age is{doc.age}")
    


# -->new_doc ---for insert

	# def validate(self):
	# 	self.new_document()
	
	# def new_document(self):
	# 	doc=frappe.new_doc("Client Side Scripting")
	# 	doc.first_name='Jack'
	# 	doc.last_name='j'
	# 	doc.age=13
	# 	doc.insert()
    
# -->frappe.delete_doc --for delete

	# def validate(self):
	# 	frappe.delete_doc("Client Side Scripting","SER00015")
	# 	frappe.msgprint("SER00015 record deleted")
    
	# def validate(self):
	# 	frappe.msgprint(f"helloooo{self.first_name}")

	
# -->get_list() ==========not done
 
	# def validate(self):
	# 	self.get_list()
	
	# def  get_list(self):
	# 	doc = frappe.db.get_list('Client Side Scripting',
	# 					   filters={
	# 						   'enable':"1"
	# 					   },
	# 					   fields=['first_name','age'])
	# 	for d in doc:
	# 		# frappe.msgprint("The first name is {0} and age is {1}").format(d.first_name,d.age)
	# 		frappe.msgprint(f"the first name is{d['first_name']} and age is {d['age']}")
    
	

	def validate(self):
			self.get_list()
	
	def get_list(self):
			print('------------------------',self)
			doc = frappe.db.get_list('Client Side Scripting',
							filters={
								'enable':1
							},
							fields=['first_name','age']
							)
			print('-------------doc----------------,',doc)
			for d in doc:
				frappe.msgprint(_("The Parent First Name is {0} and age is {1}").format(d.first_name,d.age))
 









	# -->frappe.db.get_value()
	# def validate(self):
	# 	self.get_value()
	# def get_value(self):
	# 	first_name,age = frappe.db.get_value("Client Side Scripting",'SER00008',['first_name','age'])
	# 	frappe.msgprint(f"the first name{first_name} and age is {age}")
		



# -->set_value
    # def validate(self):
    #     self.set_value()
    # def set_value(self):
    #     frappe.db.set_value("Client Side Scripting",'SER00012','age',25)
    #     first_name,age=frappe.db.get_value("Client Side Scripting",'SER00012',['first_name','age'])
    #     frappe.msgprint(f"the name is{first_name} and age is {age}")


# -->frape.db.exists()

	# def validate(self):
	# 	if frappe.db.exists('Client Side Scripting','SER00012'):
	# 		frappe.msgprint("the document is exists")
	# 	else:
	# 		frappe.msgprint("the document does not exists")
    
# -->frappe.db.count()

	# def validate(self):
	# 	doc_count = frappe.db.count('Client Side Scripting',{'enable:1'})
	# 	frappe.msgprint(f"the enable doc count is{doc_count}")
    

# -->sql()

	# def sql(self):
	# 	data = frappe.db.sql("""
	# 						SELECT
	# 				   			first_name,age
	# 				   		FROM
	# 				   			`tabClient Side Scripting`
	# 						WHERE
	# 				   			enable = 1


	# 				""",as_dict = 1)
	# 	for d in data:
	# 		frappe.msgprint(f"first name is{d['first_name']} and age is {d['age']}")
	
	
	# def frm_call(self,msg):
	# 	import time
	# 	time.sleep(5)
	# 	frappe.msgprint(msg)



	# 	return "Hii this message from frm_call"


	
	# def refresh(self):
	# 	self.get_list()
	# 	def get_list(self):
	# 		data = frappe.get_list("Client Side Scripting")
	# 		for d in data:
   	# 			 frappe.msgprint(d.first_name)

