import frappe

@frappe.whitelist(allow_guest=True)
def get_brands_by_category(category=None):
    try:

        if not category:
            all_brands = frappe.db.get_all(
                "Machine Brand",
                fields=["name", "brand_name", "category"]
            )
            
            
            for b in all_brands:
                b["category_name"] = frappe.db.get_value("Machine Category", b["category"], "machine_name")

            return {
                "success": True,
                "brands": all_brands,
                "message": "All brands fetched"
            }

        category_doc = frappe.db.get_value(
            "Machine Category",
            {"machine_name": category}, 
            "name"
        )

        if not category_doc:
            return {"success": False, "brands": [], "message": "Category not found"}

        brands = frappe.db.get_all(
            "Machine Brand",
            filters={"category": category_doc},
            fields=["name", "brand_name"]
        )

        return {
            "success": True,
            "brands": brands,
            
        }
    
    except Exception as e:
        return {
            "success": False,
            "brands": [],
            "message": "error occurred while fetching brands"
        }
    
@frappe.whitelist(allow_guest=True)
def get_machine_details(category=None, brand=None, page=1, page_size=1):
    try:
        page = int(page)
        page_size = int(page_size)
        start = (page - 1) * page_size

        filters = {}

        
        if category:
            category_id = frappe.db.get_value("Machine Category", {"machine_name": category}, "name")
            filters["category"] = category_id if category_id else category

        
        if brand:
            brand_id = frappe.db.get_value("Machine Brand", {"brand_name": brand}, "name")
            filters["brand"] = brand_id if brand_id else brand

        machines = frappe.db.get_all(
            "Machine Detail",
            filters=filters,
            fields=["speed", "weight", "capacity", "category", "brand"],
            limit_start=start,
            limit_page_length=page_size
        )

        
        for m in machines:
            m["category"] = frappe.db.get_value("Machine Category", m["category"], "machine_name")
            m["brand"] = frappe.db.get_value("Machine Brand", m["brand"], "brand_name")

        return {
            "success": True,
            "page": page,
            "page_size": page_size,
            "machines": machines
        }

    except Exception as e:
        return {
            "success": False,
            "message": "error occurred",
            "machines": []
        }
