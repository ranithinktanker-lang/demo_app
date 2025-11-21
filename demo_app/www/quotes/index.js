document.addEventListener("DOMContentLoaded", function() {

    document.getElementById("quote-form").addEventListener("submit", function(e) {
        e.preventDefault();

        let title = this.title.value;
        let author = this.author.value;
        let content = this.content.value;

        frappe.call({
            method: "demo_app.www.quotes.quotes.add_quote",
            args: { title: title, author: author, content: content },
            headers: { "X-Frappe-CSRF-Token": frappe.csrf_token },
            callback: function(r) {
                if(r.message.success) {
                    document.getElementById("message").innerHTML = "<p style='color:green'>Quote added successfully!</p>";
                    document.getElementById("quote-form").reset();
                } else {
                    document.getElementById("message").innerHTML = "<p style='color:red'>" + r.message.message + "</p>";
                }
            }
        });

    });

});
 // --- Search Quote ---
    document.getElementById("search-btn").addEventListener("click", function() {
        let title = document.getElementById("search-title").value;

        frappe.call({
            method: "demo_app.www.quotes.quotes.search_quotes",
            args: { title },
            callback: function(r) {
                let resultsDiv = document.getElementById("search-results");
                resultsDiv.innerHTML = "";
                if(r.message.success && r.message.quotes.length > 0){
                    r.message.quotes.forEach(q => {
                        // Create container div for each quote
                    let quoteDiv = document.createElement("div");
                    quoteDiv.style.border = "1px solid #ccc";
                    quoteDiv.style.padding = "10px";
                    quoteDiv.style.margin = "10px 0";
                    quoteDiv.style.borderRadius = "5px";

                    // Add structured content
                    quoteDiv.innerHTML = `
                        <h3><a href="/quote_detail/detail.html/${q.name}">${q.title}</a></h3>
                        <p><strong>Author:</strong> ${q.author}</p>
                        
                       
                    `;

                    resultsDiv.appendChild(quoteDiv);
                });
            } else {
                resultsDiv.innerHTML = `<p>${r.message.message || "No quotes found"}</p>`;
            }
        }
    });
});

