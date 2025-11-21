import frappe

def get_context(context, route):
    blog = frappe.get_all(
        "Blog_Detail",
        filters={"route": route, "status": "Published"},
        fields=["name", "title", "content", "author", "published_on", "route"]
    )

    if not blog:
        frappe.throw("Blog not found")

    context.blog = blog[0]

    # Fetch previous and next blogs based on published_on
    context.prev_blog = frappe.get_all(
        "Blog_Detail",
        filters=[["published_on", "<", context.blog.published_on], ["status", "=", "Published"]],
        order_by="published_on desc",
        fields=["title", "route"],
        limit_page_length=1
    )
    context.next_blog = frappe.get_all(
        "Blog_Detail",
        filters=[["published_on", ">", context.blog.published_on], ["status", "=", "Published"]],
        order_by="published_on asc",
        fields=["title", "route"],
        limit_page_length=1
    )

    return context


