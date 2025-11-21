document.addEventListener("DOMContentLoaded", function() {
    // Extract quote name from URL
    let pathParts = window.location.pathname.split("/");
    let quoteName = pathParts[pathParts.length - 1];

    frappe.call({
        method: "demo_app.www.quote_detail.detail.get_quote_detail",
        args: { name: quoteName },
        callback: function(r) {
            if(r.message.success){
                document.getElementById("quote-title").innerText = r.message.quote.title;
                document.getElementById("quote-author").innerText = r.message.quote.author;
                document.getElementById("quote-content").innerText = r.message.quote.content;
            } else {
                document.getElementById("quote-container").innerHTML = "<p style='color:red'>" + r.message.message + "</p>";
            }
        }
    });
});
