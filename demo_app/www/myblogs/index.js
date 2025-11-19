document.addEventListener("DOMContentLoaded", function () {
  console.log("✅ index.js loaded successfully");

  const button = document.getElementById("saveBlog");
  const message = document.getElementById("message");
  const searchBtn = document.getElementById("searchBtn");
  const searchInput = document.getElementById("searchTitle");
  const container = document.getElementById("blogsContainer");

  // --- Blog Creation ---
  if (button) {
    button.addEventListener("click", function () {
      const title = document.getElementById("title").value.trim();
      const content = document.getElementById("content").value.trim();
      const author = document.getElementById("author").value.trim();
      const status = document.getElementById("status").value;

      if (!title || !content || !author) {
        message.style.color = "red";
        message.textContent = "Please fill all fields!";
        return;
      }

      message.textContent = "Saving...";

      frappe.call({
        method: "demo_app.www.myblogs.blog.create_blog",
        args: { title, content, author, status },
        headers: { "X-Frappe-CSRF-Token": frappe.csrf_token },
        callback: function (r) {
          if (r.message === "success") {
            message.style.color = "green";
            message.textContent = "✅ Blog created successfully!";
            document.getElementById("blogForm").reset();
            loadPublishedBlogs();
          } else {
            message.style.color = "red";
            message.textContent = "❌ " + (r.message || "Error creating blog");
          }
        },
        error: function (err) {
          console.error("❌ Server Error:", err);
          message.style.color = "red";
          message.textContent = "❌ Server Error!";
        },
      });
    });
  }

  // --- Load Blogs ---
  function loadPublishedBlogs(titleQuery = "") {
    if (!container) return;

    container.innerHTML = "<p>Loading blogs...</p>";

    frappe.call({
      method: "demo_app.www.myblogs.blog.get_published_blogs",
      args: titleQuery ? { title: titleQuery } : {},
      callback: function (r) {
        container.innerHTML = "";
        if (r.message && r.message.length > 0) {
          r.message.forEach(blog => {
            const div = document.createElement("div");
            div.style.border = "1px solid #ccc";
            div.style.padding = "10px";
            div.style.margin = "10px 0";

            const tempDiv = document.createElement("div");
            tempDiv.innerHTML = blog.content;
            const excerpt = tempDiv.textContent.substring(0, 150) + "...";

            div.innerHTML = `
              <h3><a href="/blogs/${blog.route}">${blog.title}</a></h3>
              <p><b>Author:</b> ${blog.author}</p>
              <p>${excerpt}</p>
              <small>Published on: ${blog.published_on}</small>
            `;

            // Make entire card clickable
            div.addEventListener("click", function(e) {
              if (e.target.tagName.toLowerCase() !== 'a') {
                window.location.href = `/blogs/${blog.route}`;
              }
            });

            container.appendChild(div);
          });
        } else {
          container.innerHTML = "<p>No blogs found.</p>";
        }
      },
      error: function (err) {
        console.error("❌ Error fetching blogs:", err);
        container.innerHTML = "<p>Failed to load blogs.</p>";
      }
    });
  }

  // --- Search ---
  if (searchBtn) {
    searchBtn.addEventListener("click", function () {
      const query = searchInput.value.trim();
      loadPublishedBlogs(query);
    });
  }

  // --- Initial load ---
  loadPublishedBlogs();
});
