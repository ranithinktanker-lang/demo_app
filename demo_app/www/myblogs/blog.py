import frappe
from frappe.utils import today
import re


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[\s_]+', '-', text)   
    text = re.sub(r'[^a-z0-9\-]', '', text)  # remove invalid chars
    return text



@frappe.whitelist(allow_guest=True)
def create_blog(title, content, author, status):
    route = slugify(title)
    if frappe.db.exists("Blog_Detail", {"title": title}):
        return "A blog with this title already exists."

    try:
        doc = frappe.get_doc({
            "doctype": "Blog_Detail",
            "title": title,
            "content": content,
            "author": author,
            "status": status,
            "published_on": today(),
            "route": route
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        return "success"
    except Exception as e:
        frappe.log_error(message=str(e), title="Blog Create Error")
        return str(e)


@frappe.whitelist(allow_guest=True)
def get_published_blogs(title=None):
    try:
        filters = [["status", "=", "Published"]]

        if title:
            filters.append(["title", "like", f"%{title}%"])

        blogs = frappe.get_all(
        "Blog_Detail",
        filters=filters,
        fields=["title", "author", "content", "published_on", "route"],
        order_by="published_on desc"
        )

        return blogs
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in get_published_blogs")
        return {"error": "Failed to fetch blogs", "details": str(e)}


@frappe.whitelist(allow_guest=True)
def get_blog_by_route(route):
    try:
        blog = frappe.get_all(
        "Blog_Detail",
        filters={"route": route, "status": "Published"},
        fields=["name", "title", "content", "author", "published_on", "route"]
        )
        if not blog:
            return None

        all_blogs = frappe.get_all(
        "Blog_Detail",
        filters={"status": "Published"},
        fields=["name", "title", "route"],
        order_by="published_on asc"
        )

        return {"blog": blog[0], "all_blogs": all_blogs}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in get_blog_by_route")
        return {"error": "Failed to fetch blog by route", "details": str(e)}

