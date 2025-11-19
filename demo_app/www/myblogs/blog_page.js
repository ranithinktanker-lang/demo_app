document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById("blogContainer");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");

  // Extract route from URL
  const routeFull = window.location.pathname.split('/');
  const blogRoute = routeFull[2]; // /blogs/<route>

  let currentIndex = 0;
  let blogsList = [];

  function loadBlog(route) {
    container.innerHTML = "<p>Loading blog...</p>";

    frappe.call({
      method: "demo_app.www.myblogs.blog.get_blog_by_route",
      args: { route: route },
      callback: function (r) {
        if (r.message) {
          const blog = r.message.blog;
          blogsList = r.message.all_blogs; // for navigation
          currentIndex = blogsList.findIndex(b => b.name === blog.name);

          container.innerHTML = `
            <h2>${blog.title}</h2>
            <p><b>Author:</b> ${blog.author}</p>
            <p>${blog.content}</p>
            <small>Published on: ${blog.published_on}</small>
          `;

          // Disable buttons if at start or end
          prevBtn.disabled = currentIndex <= 0;
          nextBtn.disabled = currentIndex >= blogsList.length - 1;
        } else {
          container.innerHTML = "<p>Blog not found.</p>";
          prevBtn.disabled = true;
          nextBtn.disabled = true;
        }
      }
    });
  }

  prevBtn.addEventListener("click", function () {
    if (currentIndex > 0) {
      const prevRoute = blogsList[currentIndex - 1].route;
      window.location.href = `/blogs/${prevRoute}`;
    }
  });

  nextBtn.addEventListener("click", function () {
    if (currentIndex < blogsList.length - 1) {
      const nextRoute = blogsList[currentIndex + 1].route;
      window.location.href = `/blogs/${nextRoute}`;
    }
  });

  // Initial load
  loadBlog(blogRoute);
});
