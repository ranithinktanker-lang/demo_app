import frappe

def make_slug(title):
    # Convert title to lowercase and replace spaces with '-'
    return title.strip().lower().replace(" ", "-")

@frappe.whitelist(allow_guest=True)
def add_quote(title, author, content):
    try:
        if not (title and author and content):
            return {"success": False, "message": "Please fill all fields!"}
        slug = make_slug(title)

        if frappe.db.exists("Quote", {"slug": slug}):
            return {"success": False, "message": f"Quote titled '{title}' already exists!"}

        doc = frappe.get_doc({
            "doctype": "Quote",
            "title": title,
            "author": author,
            "content": content,
        })
        doc.insert()
        frappe.db.commit()
        return {"success": True, "message": f"Quote '{title}' added successfully!"}

    except Exception as e:
        return {"success": False, "message": f"Something went wrong: {str(e)}"}
    
    
@frappe.whitelist(allow_guest=True)
def search_quotes(title):
    try:
        if not title:
            return {"success": False, "quotes": [], "message": "Please enter a title to search!"}

        quotes = frappe.get_all(
            "Quote",
            filters=[["title", "like", f"%{title}%"]],
            fields=["name", "title", "author", "content"]
        )

        return {"success": True, "quotes": quotes}

    except Exception as e:
        return {"success": False, "quotes": [], "message": f"Something went wrong: {str(e)}"}