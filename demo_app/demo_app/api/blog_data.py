# import frappe
# from frappe.utils import nowdate
# import re

# @frappe.whitelist(allow_guest=True)
# def create_blog(title, content, author):
#     # Check for duplicate title
#     if frappe.db.exists("Blog_Data", {"title": title}):
#         return {"status": "error", "message": "A blog with this title already exists."}

#     # Generate route slug (e.g., "my-first-blog")
#     route_slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.strip().lower()).strip('-')

#     # Create blog record
#     blog = frappe.get_doc({
#         "doctype": "Blog_Data",
#         "title": title,
#         "content": content,
#         "author": author,
#         "published_on": nowdate(),
#         "route": route_slug,
#         "status": "Draft"  # default
#     })
#     blog.insert(ignore_permissions=True)
#     frappe.db.commit()

#     return {
#         "status": "success",
#         "message": "Blog created successfully",
#         "route": route_slug
#     }


# @frappe.whitelist(allow_guest=True)
# def get_published_blogs(search=None):
#     """Fetch all published blogs (optionally filter by search term)"""
#     filters = {"status": "Published"}
#     if search:
#         filters["title"] = ["like", f"%{search}%"]

#     blogs = frappe.get_all(
#         "Blog_Data",
#         filters=filters,
#         fields=["title", "author", "published_on", "content", "route"],
#         order_by="published_on desc"
#     )

#     # Truncate content for preview
#     for blog in blogs:
#         blog["short_content"] = (blog["content"][:200] + "...") if blog["content"] else ""

#     return blogs
