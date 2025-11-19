document.getElementById("customer-form").addEventListener("submit", function(e) {
    e.preventDefault();

    let customer_name = document.getElementById("customer_name").value;
    let email = document.getElementById("email").value;
    let address = document.getElementById("address").value;

    frappe.call({
        method: "demo_app.www.customer.customer.save_customer",  
        args: {
            customer_name: customer_name,
            email: email,
            address: address
        },
        headers: { "X-Frappe-CSRF-Token": frappe.csrf_token },
        callback: function(r) {
            let msg = document.getElementById("msg");
            if(r.message) {
                msg.innerText = "✅ Customer Saved Successfully!";
                msg.className = "text-green-600 text-lg";
                document.getElementById("customer-form").reset();
            } else {
                msg.innerText = "❌ Error saving customer!";
                msg.className = "text-red-600 text-lg";
            }
        }
    });
});
