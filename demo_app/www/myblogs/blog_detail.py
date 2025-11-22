import frappe
import re

def get_context(context):
    route = frappe.form_dict.route
    if not route:
        frappe.throw("No blog route provided")

    normalized_route = route.replace("-", "_").lower()

    # Fetch published blogs
    all_blogs = frappe.db.get_all(
        "Blog_Detail",
        filters={"status": "Published"},
        fields=["name", "title", "content", "author", "published_on", "route"],
        order_by="published_on asc"
    )

    # Match the blog by route
    current_blog = None
    for b in all_blogs:
        if b.route.lower().replace("-", "_") == normalized_route:
            current_blog = b
            break

    if not current_blog:
        frappe.throw("Blog not found or not published")

    context.blog = current_blog

    # --- Determine Previous and Next blogs ---
    current_index = all_blogs.index(current_blog)
    context.previous = all_blogs[current_index - 1] if current_index > 0 else None
    context.next = all_blogs[current_index + 1] if current_index < len(all_blogs) - 1 else None

    return context



