# ============================================================
# CREATE USER 
# ============================================================
import frappe, json, re, requests
from frappe.model.naming import make_autoname

@frappe.whitelist()
def create_user():
    try:
        raw_body = frappe.local.request.get_data()
        if not raw_body:
            return {"error": "No data provided"}

        data = json.loads(raw_body)

        full_name = data.get("full_name")
        email = data.get("email")
        password = data.get("password")
        address = data.get("address")
        country = data.get("country")
        city = data.get("city")
        state = data.get("state")
        pincode = data.get("pincode")
        mobile = data.get("mobile")

        error = {}

        # Required fields check
        required_fields = ["full_name", "email", "password", "address", "country", "city", "state", "pincode", "mobile"]
        for field in required_fields:
            if not data.get(field):
                error[field] = f"{field.replace('_',' ').title()} is required"

        # Email validation
        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            error["email"] = "Invalid email format"

        # Password validation
        if password and (len(password) < 8 or not any(c.isupper() for c in password)):
            error["password"] = "Password must be at least 8 characters long and contain one uppercase letter"

        # Mobile validation
        if mobile and not re.match(r"^[0-9]{10}$", mobile):
            error["mobile"] = "Mobile number must be 10 digits"

        # Duplicate email check
        if email and frappe.db.exists("User Info", {"email": email}):
            error["email"] = "User with this email already exists"

        #  Gender API
        full_name_val = data.get("full_name")
        if full_name_val:
            try:
                res = requests.get(f"https://api.genderize.io/?name={full_name_val.split()[0]}")
                gender = res.json().get("gender", "Not Specified")
            except:
                gender = "Not Specified"
        else:
            gender = "Not Specified"

        # Return errors dict if any
        if error:
            return {"error": True, "status_code": 422, "errors": error}

        # Create User Info doc
        doc = frappe.new_doc("User Info")
        doc.full_name = full_name
        doc.email = email
        doc.password = password
        doc.address = address
        doc.country = country
        doc.city = city
        doc.state = state
        doc.pincode = pincode
        doc.mobile = mobile
        doc.gender = gender
        doc.insert(ignore_permissions=True)
        frappe.db.commit()

        # ---- Send email with credentials ----
        email_subject = "Your account has been created"
        # Keep message simple HTML — includes email and password
        # login_url = frappe.utils.get_url()  # base site url
        email_message = f"""
        <p>Hi {full_name},</p>
        <p>Your account has been created successfully.</p>
        <p><strong>Login details:</strong></p>
        <ul>
          <li><strong>Email:</strong> {email}</li>
          <li><strong>Password:</strong> {password}</li>
        </ul>
        
        """

        # email_sent = False
        try:
            frappe.sendmail(
                recipients=[email],
                subject=email_subject,
                message=email_message
            )
            # email_sent = True
        except Exception as mail_exc:
            # Log the error but don't break user creation
            frappe.log_error(frappe.get_traceback(), "Create User - Email Send Failed")
            # you may also include the exception message in response for debugging
            mail_error_msg = str(mail_exc)

        # resp = {"message": f"User {full_name} created successfully", "user_id": doc.name}
        # if email_sent:
        #     resp["email_sent"] = True
        # else:
        #     resp["email_sent"] = False
        #     resp["email_error"] = mail_error_msg if 'mail_error_msg' in locals() else "Failed to send email"

        return {"error": False,"status_code": 200,"message": f"User {full_name} created successfully", "user_id": doc.name}

    except Exception as e:
        frappe.log_error(f"Error in create_user: {e}", "Create User API Error")
        return {"error": "Something went wrong", "details": str(e)}


# ============================================================
#  LOGIN 
# ============================================================
@frappe.whitelist()
def user_login():
    try:
        data = json.loads(frappe.local.request.get_data())
        email = data.get("email")
        password = data.get("password")

        user_info = frappe.db.get_value("User Info", {"email": email, "password": password},
                                        ["name", "full_name", "email"], as_dict=True)
        if not user_info:
            return {"error": "Invalid email or password"}

        # Store in session
        frappe.local.session.user_info_email = user_info["email"]
        frappe.db.commit()

        return {"message": "Login successful", "user": user_info}

    except Exception as e:
        frappe.log_error(f"Error in user_login: {e}", "User Login API Error")
        return {"error": "Something went wrong", "details": str(e)}


# ============================================================
#  Helper: Check login
# ============================================================
def check_login():
    # Try session first
    user_email = getattr(frappe.local.session, "user_info_email", None)

    # Allow Postman header too
    if not user_email:
        user_email = frappe.local.request.headers.get("X-User-Email")
        if not user_email:
            frappe.throw("Login required to access this API", frappe.PermissionError)

    # ✅ Validate against User Info (not Frappe User)
    if not frappe.db.exists("User Info", {"email": user_email}):
        frappe.throw(f"Custom user not found: {user_email}", frappe.DoesNotExistError)

    return user_email


# ============================================================
#  CREATE POST
# ============================================================

@frappe.whitelist()
def create_post():
    try:
        error = {}
        user_email = getattr(frappe.local.session, "user_info_email", None)
        if not user_email:
            user_email = frappe.local.request.headers.get("X-User-Email")
        if not user_email:
            return {"error": "Login required to access this API"}
        user_email = user_email.strip()

        user_info = frappe.db.get_value(
            "User Info",
            {"email": user_email},
            ["name", "full_name", "email"],
            as_dict=True
        )
        if not user_info:
            return {"error": "User not found"}

        # Step 4: Get form fields
        title = frappe.form_dict.get("title")
        content = frappe.form_dict.get("content")
        image_file = frappe.local.request.files.get("image")
        description = frappe.form_dict.get("description")
        print("image_file-----------------",image_file)

        if not title:
            error['title'] = "Title is required."
        if not content:
            error['content'] = "Content is required."
        if not description:
            error['description'] = "description is required"
        if not image_file:
            error['image_file'] = "image_file is required"

        if error:
            return {"error": True,"status_code":422,"errors":error}

        # Step 5: Save image in File doctype (optional)
        if image_file:
            file_doc = frappe.get_doc({
                "doctype": "File",
                "file_name": image_file.filename,
                "content": image_file.read(),
                "is_private": 0
            })
            file_doc.save()
            frappe.db.commit()
            image_url = file_doc.file_url
        else:
            image_url = None

        # Step 6: Create Post
        doc = frappe.get_doc({
            "doctype": "Post",
            "title": title,
            "content": content,
            "description": frappe.form_dict.get("description"),
            "image": image_url,
            "user_email": user_info["email"],
            "user_id": user_info["name"],
            "owner": user_info["email"]
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()

        return {"error": False,'status_code':200,"message": "Post created successfully", "user_email": user_info["email"]}

    except Exception as e:
        import sys, traceback
        tb = sys.exc_info()[2].tb_lineno
        print(f"Error on line {tb}: {e}")
        frappe.log_error(traceback.format_exc(), "Create Post API Error")
        return {"error": "Something went wrong", "details": str(e)}


# ============================================================
#  UPDATE POST 
# ============================================================
@frappe.whitelist()
def update_post(post_id):
    try:
        user_email = check_login()
        print("user_email------------------------------------",user_email)
        data = json.loads(frappe.local.request.get_data())

        post = frappe.get_doc("Post", post_id)

        #  Check ownership manually
        if post.user_email != user_email:
            return {"error": "You can only update your own posts"}

        for field in ["title", "content", "description", "category", "image"]:
            if data.get(field):
                setattr(post, field, data.get(field))

        post.save(ignore_permissions=True)
        frappe.db.commit()

        return {"message": "Post updated successfully", "post_name": post.name}

    except frappe.DoesNotExistError:
        return {"error": f"Post {post_id} not found"}
    except Exception as e:
        frappe.log_error(f"Error in update_post: {e}", "Update Post API Error")
        return {"error": "Something went wrong", "details": str(e)}


# ============================================================
#  DELETE POST 
# ============================================================
@frappe.whitelist()
def delete_post(post_id):
    try:
        user_email = check_login()
        post = frappe.get_doc("Post", post_id)

        if post.user_email != user_email:
            return {"error": "You can only delete your own posts"}

        post.is_deleted = 1
        post.save(ignore_permissions=True)
        frappe.db.commit()

        return {"message": f"Post {post_id} deleted successfully"}

    except frappe.DoesNotExistError:
        return {"error": f"Post {post_id} not found"}
    except Exception as e:
        frappe.log_error(f"Error in delete_post: {e}", "Delete Post API Error")
        return {"error": "Something went wrong", "details": str(e)}


# ============================================================
#  CREATE LIKE 
# ============================================================
@frappe.whitelist()
def create_like():
    try:
        error = {}
        user_email = check_login()
        user_info = frappe.db.get_value("User Info", {"email": user_email},
                                        ["name", "full_name", "email"], as_dict=True)

        data = json.loads(frappe.local.request.get_data())
        post_id = data.get("post_id")
        if not post_id:
            error['post_id'] = "post_id is required"
        if not frappe.db.exists("Post", post_id):
            error["post_id"] = "Post not found"

        if frappe.db.exists("Like", {"post_id": post_id, "user_id": user_info["name"]}):
            error['like_id'] =  "Already liked"
        
        if error:
            return {"error": True,"status_code":422,"error":error}

        like_doc = frappe.get_doc({
            "doctype": "Like",
            "like_id": frappe.generate_hash(length=6).upper(),
            "post_id": post_id,
            "user_id": user_info["name"]
        })
        like_doc.insert(ignore_permissions=True)
        frappe.db.commit()

        return {"error":False,'status_code ':200, "message": "Like created successfully", "like_id": like_doc.name}

    except Exception as e:
        frappe.log_error(f"Error in create_like: {e}", "Create Like API Error")
        return {"error": "Something went wrong", "details": str(e)}


# ============================================================
#  DELETE LIKE 
# ============================================================
@frappe.whitelist()
def delete_like(like_id):
    try:
        user_email = check_login()
        user_info = frappe.db.get_value("User Info", {"email": user_email},
                                        ["name", "full_name", "email"], as_dict=True)

        like = frappe.get_doc("Like", like_id)
        if like.user_id != user_info["name"]:
            return {"error": "Only owner can delete this like"}

        like.is_deleted = 1
        like.save(ignore_permissions=True)
        frappe.db.commit()

        return {"message": f"Like {like_id} soft deleted successfully"}

    except frappe.DoesNotExistError:
        return {"error": f"Like {like_id} not found"}
    except Exception as e:
        frappe.log_error(f"Error in delete_like: {e}", "Delete Like API Error")
        return {"error": "Something went wrong", "details": str(e)}


# ============================================================
#  GET POST / LIKE / USER
# ============================================================
@frappe.whitelist(allow_guest=True)
def get_post(post_id):
    try:
        # check_login()
        post = frappe.get_doc("Post", post_id)
        likes_count = frappe.db.count("Like", {"post_id": post.name, "is_deleted": 0})

        return {
            "post_id": post.name,
            "title": post.title,
            "description": post.description,
            "content": post.content,
            "image": post.image,
            "user_name": post.user_name,
            "user_email": post.user_email,
            "category": post.category,
            "creation_date": str(post.creation_date),
            "likes_count": likes_count
        }

    except frappe.DoesNotExistError:
        return {"error": f"Post {post_id} not found"}
    except Exception as e:
        frappe.log_error(f"Error in get_post: {e}", "Get Post API Error")
        return {"error": "Something went wrong", "details": str(e)}


@frappe.whitelist()
def get_like(like_id):
    try:
        check_login()
        like = frappe.get_doc("Like", like_id)
        return {"like_id": like.name, "post_id": like.post_id, "user_id": like.user_id}
    except frappe.DoesNotExistError:
        return {"error": f"Like {like_id} not found"}
    except Exception as e:
        frappe.log_error(f"Error in get_like: {e}", "Get Like API Error")
        return {"error": "Something went wrong", "details": str(e)}


@frappe.whitelist(allow_guest=True)
def get_user(user_id):
    try:
        # check_login()
        user = frappe.get_doc("User Info", user_id)
        return {
            "user_id": user.name,
            "full_name": user.full_name,
            "email": user.email,
            "address": getattr(user, "address", ""),
            "country": getattr(user, "country", ""),
            "city": getattr(user, "city", ""),
            "state": getattr(user, "state", ""),
            "pincode": getattr(user, "pincode", ""),
            "mobile": getattr(user, "mobile", ""),
            "gender": getattr(user, "gender", "")
        }
    except frappe.DoesNotExistError:
        return {"error": f"User {user_id} not found"}
    except Exception as e:
        frappe.log_error(f"Error in get_user: {e}", "Get User API Error")
        return {"error": "Something went wrong", "details": str(e)}


# ============================================================
# GET ALL POSTS / USERS
# ============================================================
@frappe.whitelist(allow_guest=True)
def get_all_posts(page_no=1, page_size=10):
    try:
        # check_login()
        import math
        args = frappe.local.form_dict
        page_no = int(args.get("page_no", page_no))
        page_size = int(args.get("page_size", page_size))
        search = args.get("search")
        user_id = args.get("user_id")
        start_date = args.get("start_date")
        end_date = args.get("end_date")

        filters = {"is_deleted": 0}
        if user_id:
            filters["user_id"] = user_id
        if start_date and end_date:
            filters["creation_date"] = ["between", [start_date, end_date]]

        posts = frappe.get_all(
            "Post",
            filters=filters,
            fields=["post_id", "title", "content", "user_id", "creation_date"],
            order_by="creation_date desc"
        )

        if search:
            posts = [p for p in posts if search.lower() in (p.title.lower() + p.content.lower())]

        total_records = len(posts)
        total_pages = math.ceil(total_records / page_size)
        start = (page_no - 1) * page_size
        end = start + page_size
        posts_paginated = posts[start:end]

        result = []
        for post in posts_paginated:
            user_name = frappe.db.get_value("User Info", post.user_id, "full_name") if post.user_id else None
            like_count = frappe.db.count("Like", {"post_id": post.post_id, "is_deleted": 0})
            result.append({
                "post_id": post.post_id,
                "title": post.title,
                "content": post.content,
                "user_name": user_name,
                "creation_date": str(post.creation_date),
                "like_count": like_count
            })

        return {"total_records": total_records, "page_no": page_no, "page_size": page_size, "total_pages": total_pages, "posts": result}

    except Exception as e:
        frappe.log_error(f"Error in get_all_posts: {e}", "Get All Posts API Error")
        return {"error": "Something went wrong", "details": str(e)}


# @frappe.whitelist(allow_guest=True)
# def get_all_users_with_posts(page_no=1, page_size=10,search_value=None,filter=None):
#     try:
#         # check_login()
#         page_no = int(page_no)
#         page_size = int(page_size)
#         start = (page_no - 1) * page_size

#         users = frappe.get_all(
#             "User Info",
#             filters={"is_deleted": 0},
#             fields=["name", "full_name", "email"],
#             limit_start=start,
#             limit_page_length=page_size,
#             order_by="creation desc"
#         )
#         total_records = frappe.db.count("User Info", {"is_deleted": 0})
#         total_pages = (total_records + page_size - 1) // page_size

        
#         user_list = []
#         for user in users:
#             posts = frappe.get_all(
#                 "Post",
#                 filters={"user_id": user.name, "is_deleted": 0},
#                 fields=["post_id", "title", "content", "creation"],
#                 order_by="creation desc"
#             )
#             posts_with_likes = []
#             for post in posts:
#                 like_count = frappe.db.count("Like", {"post_id": post.post_id, "is_deleted": 0})
#                 posts_with_likes.append({
#                     "post_id": post.post_id,
#                     "title": post.title,
#                     "content": post.content,
#                     "creation": post.creation,
#                     "like_count": like_count
#                 })
#             user_list.append({
#                 "user_id": user.name,
#                 "full_name": user.full_name,
#                 "email": user.email,
#                 "total_posts": len(posts),
#                 "posts": posts_with_likes
#             })

#         return {"message": {"total_records": total_records, "page_no": page_no, "page_size": page_size, "total_pages": total_pages, "users": user_list}}

#     except Exception as e:
#         frappe.log_error(f"Error in get_all_users_with_posts: {e}", "Get All Users API Error")
#         return {"error": "Something went wrong", "details": str(e)}


@frappe.whitelist(allow_guest=True)
def get_all_users_with_posts(page_no=1, page_size=10, search_value=None, filters=[]):
    # print("filters------------------"(filters))
    try:
        import json
        page_no = int(page_no)
        page_size = int(page_size)
        start = (page_no - 1) * page_size

        where_clause = "ui.is_deleted = 0"
        values = {}

        # -------------------------------
        # 🔍 Handle Search
        # -------------------------------
        if search_value:
            where_clause += " AND (ui.full_name LIKE %(search)s OR ui.email LIKE %(search)s OR p.title LIKE %(search)s OR p.content LIKE %(search)s)"
            values["search"] = f"%{search_value}%"

        # -------------------------------
        #  Handle Filters (JSON string from frontend)
        # Example: [{"field":"email","operator":"like","value":"gmail"}]
        # -------------------------------
        # print("--------------------------------------")
        if filters and isinstance(filters, (list, tuple)):
            for f in filters:
                field = f.get("field")
                operator = f.get("operator", "=")
                value = f.get("value")
                if field and value is not None:
                    if operator.lower() == "like":
                        value = f"%{value}%"
                    where_clause += f" AND ui.{field} {operator} %(f_{field})s"
                    values[f"f_{field}"] = value
 
        # -------------------------------
        #  SQL Query with JOIN (to search by post)
        # -------------------------------
        query = f"""
            SELECT DISTINCT
                ui.name as user_id,
                ui.full_name,
                ui.email
            FROM `tabUser Info` ui
            LEFT JOIN `tabPost` p ON p.user_id = ui.name AND p.is_deleted = 0
            WHERE {where_clause}
            ORDER BY ui.creation DESC
            LIMIT {start}, {page_size}
        """

        users = frappe.db.sql(query, values, as_dict=True)

        # Count total records
        count_query = f"""
            SELECT COUNT(DISTINCT ui.name)
            FROM `tabUser Info` ui
            LEFT JOIN `tabPost` p ON p.user_id = ui.name AND p.is_deleted = 0
            WHERE {where_clause}
        """
        total_records = frappe.db.sql(count_query, values)[0][0]
        total_pages = (total_records + page_size - 1) // page_size

        # -------------------------------
        #  Build User + Post Data
        # -------------------------------
        user_list = []
        for user in users:
            posts = frappe.get_all(
                "Post",
                filters={"user_id": user.user_id, "is_deleted": 0},
                fields=["name as post_id", "title", "content", "creation"],
                order_by="creation desc"
            )

            posts_with_likes = []
            for post in posts:
                like_count = frappe.db.count("Like", {"post_id": post["post_id"], "is_deleted": 0})
                posts_with_likes.append({
                    "post_id": post["post_id"],
                    "title": post["title"],
                    "content": post["content"],
                    "creation": post["creation"],
                    "like_count": like_count
                })

            user_list.append({
                "user_id": user.user_id,
                "full_name": user.full_name,
                "email": user.email,
                "total_posts": len(posts),
                "posts": posts_with_likes
            })

        # -------------------------------
        #  Final Response
        # -------------------------------
        return {
            "message": {
                "total_records": total_records,
                "page_no": page_no,
                "page_size": page_size,
                "total_pages": total_pages,
                "users": user_list
            }
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get All Users API Error")
        return {"error": "Something went wrong", "details": str(e)}


import csv, io
from frappe.utils.file_manager import save_file
from frappe.core.doctype.communication.email import make
from frappe.utils import get_site_path

# ============================================================
#  EXPORT POSTS CSV (Owner only)
# ============================================================
@frappe.whitelist(allow_guest=True)
def export_posts_csv():
    try:
        # Step 1: Check login
        user_email = check_login()

        # Step 2: Fetch user's posts
        posts = frappe.get_all(
            "Post",
            filters={"user_email": user_email, "is_deleted": 0},
            fields=["name", "title", "content", "description", "creation"]
        )

        if not posts:
            return {"error": "No posts found for this user"}

        # Step 3: Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Post ID", "Title", "Content", "Description", "Created On"])

        for post in posts:
            writer.writerow([post.name, post.title, post.content, post.description, post.creation])

        csv_content = output.getvalue()
        output.close()

        # Step 4: Save CSV file in File Doctype
        filename = f"Posts_{user_email.replace('@', '_')}.csv"
        file_doc = save_file(filename, csv_content.encode('utf-8'), None, None, is_private=0)
        file_url = file_doc.file_url

        # Step 5: Email CSV to user
        subject = "Your Exported Posts CSV"
        message = f"""
        Hello,<br><br>
        Please find attached the CSV export of your posts.<br><br>
        You can also <a href="{file_url}">download it here</a>.<br><br>
        Regards,<br>AccuPanel Team
        """

        frappe.sendmail(
            recipients=[user_email],
            subject=subject,
            message=message,
            attachments=[{
                "fname": filename,
                "fcontent": csv_content
            }]
        )

        return {
            "message": "Posts exported successfully",
            "download_url": file_url,
            "email_sent_to": user_email
        }

    except frappe.PermissionError:
        return {"error": "Login required"}
    except Exception as e:
        import sys, traceback
        tb = sys.exc_info()[2].tb_lineno
        print(f"Error on line {tb}: {e}")
        frappe.log_error(traceback.format_exc(), "Export Posts CSV API Error")
        return {"error": "Something went wrong", "details": str(e)}
