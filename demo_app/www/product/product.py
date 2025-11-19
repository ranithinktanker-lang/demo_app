import frappe, json

@frappe.whitelist()
def save_product(product_name, price, description, quantity, image=None, child_items=None):
    if not product_name:
        return {"error": "Product name is required"}
    if float(price) <= 0:
        return {"error": "Price must be greater than 0"}
    if int(quantity) <= 0:
        return {"error": "Quantity must be greater than 0"}

    doc = frappe.get_doc({
        "doctype": "Product",
        "product_name": product_name,
        "price": price,
        "description": description,
        "quantity": quantity,
        "image": image
    })

    if child_items:
        
        try:
            items = json.loads(child_items)
        
            for i in items:
                doc.append("item", {   # ✅ fieldname = product_item
                    "item_name": i.get("item_name"),
                    "quantity": i.get("quantity"),
                    "price": i.get("price")
                })
        except Exception as e:
            frappe.log_error(f"Child parsing error: {e}", "Product Save Error")

    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return "success"


@frappe.whitelist()
def get_products():
    products = frappe.get_all("Product",
        fields=["name", "product_name", "price", "description", "quantity", "image"]
    )
    for p in products:
        children = frappe.get_all("Product Item",
            filters={"parent": p.name, "parenttype": "Product"},
            fields=["item_name", "quantity", "price"]
        )
        p["product_item"] = children
    return products


@frappe.whitelist()
def update_product(name, product_name, price, description, quantity, image=None, child_items=None):
    doc = frappe.get_doc("Product", name)
    doc.product_name = product_name
    doc.price = price
    doc.description = description
    doc.quantity = quantity
    if image:
        doc.image = image

    doc.set("product_item", [])
    if child_items:
        items = json.loads(child_items)
        for i in items:
            doc.append("product_item", {
                "item_name": i.get("item_name"),
                "quantity": i.get("quantity"),
                "price": i.get("price")
            })

    doc.save(ignore_permissions=True)
    frappe.db.commit()
    return "success"


@frappe.whitelist()
def delete_product(name):
    frappe.delete_doc("Product", name, ignore_permissions=True)
    frappe.db.commit()
    return "success"
