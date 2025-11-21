import frappe

@frappe.whitelist(allow_guest=True)
def get_quote_detail(name):
    try:
        quote = frappe.get_doc("Quote", name)
        return {
            "success": True,
            "Quote": {
                "title": quote.title,
                "author": quote.author,
                "content": quote.content
            }
        }
    except Exception as e:
        return {"success": False, "message": f"Something went wrong: {str(e)}"}
