document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("product-form");
    const msg = document.getElementById("msg");
    const tableBody = document.querySelector("#product-table tbody");
    const preview = document.getElementById("image-preview");
    const childTableBody = document.getElementById("items_table");
    let editingProduct = null;

    // Image Preview
    document.getElementById("image").addEventListener("change", function () {
        const file = this.files[0];
        if (file) {
            preview.src = URL.createObjectURL(file);
            preview.classList.remove("hidden");
        } else {
            preview.src = "";
            preview.classList.add("hidden");
        }
    });

    // Add Item Row
    document.getElementById("add-item").addEventListener("click", function () {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td><input class="item_name border p-1 w-full" type="text" placeholder="Item Name"></td>
            <td><input class="child_qty border p-1 w-full" type="number" placeholder="Quantity"></td>
            <td><input class="child_price border p-1 w-full" type="number" placeholder="Price"></td>
            <td><button type="button" class="remove_item bg-red-500 text-white px-2 py-1 rounded">Remove</button></td>
        `;
        childTableBody.appendChild(row);
        row.querySelector(".remove_item").addEventListener("click", function () {
            row.remove();
        });
    });

    // Validation
    function validateInputs(product_name, price, quantity) {
        if (!product_name.trim()) { showMessage("❌ Product Name is required!", "red"); return false; }
        if (isNaN(price) || price <= 0) { showMessage("❌ Price must be greater than 0!", "red"); return false; }
        if (isNaN(quantity) || quantity <= 0) { showMessage("❌ Quantity must be greater than 0!", "red"); return false; }
        return true;
    }

    function showMessage(text, color) {
        msg.innerText = text;
        msg.className = `mb-4 text-lg font-semibold text-${color}-600`;
    }

    function getChildItems() {
        const items = [];
        childTableBody.querySelectorAll("tr").forEach(row => {
            const item_name = row.querySelector(".item_name").value;
            const qty = row.querySelector(".child_qty").value;
            const price = row.querySelector(".child_price").value;
            if (item_name) items.push({ item_name, quantity: qty, price });
        });
        return items;
    }

    // Form Submit
    form.addEventListener("submit", async function (e) {
        e.preventDefault();
        const product_name = document.getElementById("product_name").value;
        const price = parseFloat(document.getElementById("price").value);
        const description = document.getElementById("description").value;
        const quantity = parseInt(document.getElementById("quantity").value);
        const fileInput = document.getElementById("image");

        if (!validateInputs(product_name, price, quantity)) return;

        let image_url = editingProduct ? editingProduct.image : "";

        // Upload Image if selected
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            const formData = new FormData();
            formData.append("file", file, file.name);
            formData.append("is_private", 0);
            try {
                const uploadRes = await fetch("/api/method/upload_file", {
                    method: "POST",
                    body: formData,
                    headers: { "X-Frappe-CSRF-Token": frappe.csrf_token }
                });
                const uploadData = await uploadRes.json();
                if (uploadData.message && uploadData.message.file_url) {
                    image_url = uploadData.message.file_url;
                } else {
                    showMessage("❌ Image upload failed!", "red");
                    return;
                }
            } catch (err) {
                console.error(err);
                showMessage("❌ Image upload error!", "red");
                return;
            }
        }

        const child_items = getChildItems();

        frappe.call({
            method: editingProduct ? "demo_app.www.product.product.update_product" : "demo_app.www.product.product.save_product",
            args: editingProduct
                ? { name: editingProduct.name, product_name, price, description, quantity, image: image_url, child_items: JSON.stringify(child_items) }
                : { product_name, price, description, quantity, image: image_url, child_items: JSON.stringify(child_items) },
            headers: { "X-Frappe-CSRF-Token": frappe.csrf_token },
            callback: function (r) {
                if (r.message === "success") {
                    showMessage(editingProduct ? "✅ Product Updated!" : "✅ Product Saved!", "green");
                    form.reset();
                    preview.src = "";
                    preview.classList.add("hidden");
                    childTableBody.innerHTML = "";
                    editingProduct = null;
                    loadProducts();
                } else {
                    showMessage("❌ Error saving product!", "red");
                }
            }
        });
    });

    // Load Products
    function loadProducts() {
        frappe.call({
            method: "demo_app.www.product.product.get_products",
            headers: { "X-Frappe-CSRF-Token": frappe.csrf_token },
            callback: function (r) {
                tableBody.innerHTML = "";
                if (r.message && r.message.length) {
                    r.message.forEach(prod => {
                        const row = document.createElement("tr");
                        let childHTML = "";
                        if (prod.product_item && prod.product_item.length) {
                            childHTML = "<ul>";
                            prod.product_item.forEach(i => {
                                childHTML += `<li>${i.item_name} - Qty:${i.quantity} - ₹${i.price}</li>`;
                            });
                            childHTML += "</ul>";
                        }
                        row.innerHTML = `
                          <td class="border p-2">${prod.product_name}</td>
                          <td class="border p-2">${prod.price}</td>
                          <td class="border p-2">${prod.description}</td>
                          <td class="border p-2">${prod.quantity}</td>
                          <td class="border p-2">${prod.image ? `<img src="${window.location.origin + prod.image}" class="h-12 w-12 object-cover rounded"/>` : ""}</td>
                          <td class="border p-2">${childHTML}</td>
                          <td class="border p-2">
                            <button onclick='editProduct(${JSON.stringify(prod)})' class="bg-yellow-500 text-white px-3 py-1 rounded">Edit</button>
                            <button onclick='deleteProduct("${prod.name}")' class="bg-red-500 text-white px-3 py-1 rounded">Delete</button>
                          </td>
                        `;
                        tableBody.appendChild(row);
                    });
                }
            }
        });
    }

    window.editProduct = function (prod) {
        editingProduct = prod;
        document.getElementById("product_name").value = prod.product_name;
        document.getElementById("price").value = prod.price;
        document.getElementById("description").value = prod.description;
        document.getElementById("quantity").value = prod.quantity;
        if (prod.image) {
            preview.src = window.location.origin + prod.image;
            preview.classList.remove("hidden");
        } else {
            preview.src = "";
            preview.classList.add("hidden");
        }
        childTableBody.innerHTML = "";
        if (prod.product_item && prod.product_item.length) {
            prod.product_item.forEach(i => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td><input class="item_name border p-1 w-full" type="text" value="${i.item_name}"></td>
                    <td><input class="child_qty border p-1 w-full" type="number" value="${i.quantity}"></td>
                    <td><input class="child_price border p-1 w-full" type="number" value="${i.price}"></td>
                    <td><button type="button" class="remove_item bg-red-500 text-white px-2 py-1 rounded">Remove</button></td>
                `;
                childTableBody.appendChild(row);
                row.querySelector(".remove_item").addEventListener("click", function () { row.remove(); });
            });
        }
    };

    window.deleteProduct = function (name) {
        if (confirm("Are you sure to delete this product?")) {
            frappe.call({
                method: "demo_app.www.product.product.delete_product",
                args: { name },
                headers: { "X-Frappe-CSRF-Token": frappe.csrf_token },
                callback: function (r) {
                    if (r.message === "success") {
                        showMessage("🗑️ Product Deleted!", "green");
                        loadProducts();
                    } else {
                        showMessage("❌ Error deleting product!", "red");
                    }
                }
            });
        }
    };

    loadProducts();
});
