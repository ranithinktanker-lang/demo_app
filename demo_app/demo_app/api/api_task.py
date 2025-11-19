import frappe,re
from frappe.utils import nowdate

@frappe.whitelist(allow_guest=True)
def create_blog(title, content, author,status="Draft"):
    try:
        
        existing = frappe.db.exists("Blog_Post", {"title": title})
        if existing:
            return {
                "success": False,
                "error": "Validation failed.",
                "details": f"Blog with title {title} already exists!"
            }


       
        slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')
        print("Generated Route:", slug)
        base_slug = slug
        count = 1
        while frappe.db.exists("Blog_Post", {"route": slug}):
            slug = f"{base_slug}-{count}"
            count += 1

        frappe.logger().info(f"Generated route: {slug}")

        blog = frappe.get_doc({
            "doctype": "Blog_Post",
            "title": title,
            "content": content,
            "author": author,
            "published_on": nowdate(),
            "status": status,
            "route": slug   
        })

        blog.flags.ignore_hidden_fields = True
        

        blog.insert(ignore_permissions=True)
        frappe.db.set_value("Blog_Post", blog.name, "route", slug)
        frappe.db.commit()

    
        return {
            "success": True,
            "message": "Blog created successfully",
            "route": blog.route
        }

    except frappe.ValidationError as e:
        return {"success": False, "error": "Validation failed.", "details": str(e)}

    except Exception as e:
        return {"success": False, "error": "Something went wrong.", "details": str(e)}


@frappe.whitelist(allow_guest=True)
def get_published_blogs(search=None):
    try:
        filters = {"status": "Published"}
        if search:
            filters["title"] = ["like", f"%{search}%"]

        blogs = frappe.get_all(
            "Blog_Post",
            filters=filters,
            fields=["name", "title", "author", "published_on", "content", "route"],
            order_by="published_on desc"
        )

        if not blogs:
            return {"success": False, "message": "No published blogs found."}
       
        for blog in blogs:
            if blog.get("content"):
                blog["content"] = (
                    blog["content"][:200] + "..."
                    if len(blog["content"]) > 200
                    else blog["content"]
                )

        return {"success": True, "blogs": blogs, "count": len(blogs)}

    except Exception as e:
        frappe.log_error(f"Error fetching published blogs: {str(e)}", "Get Blogs Error")
        return {"success": False, "error": "Failed to fetch blogs.", "details": str(e)}



# @frappe.whitelist(allow_guest=True)
# def get_blog_detail(route=None):
#     if not route:
#         route = frappe.form_dict.route
#     return frappe.render_template("templates/pages/blog_detail.html", {"route": route})



@frappe.whitelist(allow_guest=True)
def get_blog_detail(route=None):
    if not route:
        route = frappe.form_dict.get("route")
    print("rr",route)
    blog = None
    if route:
        blogs = frappe.get_all(
            "Blog_Post",
            filters={"route": route, "status": "Published"},
            fields=["name", "title", "blogger", "author", "published_on", "content", "route"],
            limit_page_length=1
        )
        if blogs:
            blog = blogs[0]

    return frappe.render_template("templates/pages/blog_detail.html", {"blog": blog})

# @frappe.whitelist(allow_guest=True)
# def blog_listing():
#     data = frappe.get_all('Blog_Post',fields=["*"])

#     return data