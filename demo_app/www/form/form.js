document.addEventListener("DOMContentLoaded", function() {
  const btn = document.getElementById('submitBtn');
  const feedback = document.getElementById('feedback');
  const tableBody = document.querySelector("#userTable tbody");
  const userIdInput = document.getElementById("user_id");

  function show(msg, ok=true){
    feedback.style.display = 'block';
    feedback.className = 'msg ' + (ok ? 'success' : 'error');
    feedback.innerText = msg;
  }

  function clearForm(){
    document.querySelectorAll("input,textarea,select").forEach(el => el.value="");
    userIdInput.value = "";
  }

  function addRowToTable(data){
    const row = document.createElement("tr");
    row.dataset.name = data.name;
    row.innerHTML = `
      <td>${data.full_name}</td>
      <td>${data.email}</td>
      <td>${data.phone || ""}</td>
      <td>${data.dob || ""}</td>
      <td>${data.gender || ""}</td>
      <td>${data.city || ""}</td>
      <td>${data.state || ""}</td>
      <td>${data.country || ""}</td>
      <td>
        <button class="action-btn edit-btn">Edit</button>
        <button class="action-btn delete-btn">Delete</button>
      </td>
    `;
    tableBody.appendChild(row);

    // Edit
    row.querySelector(".edit-btn").addEventListener("click", function(){
      userIdInput.value = data.name;
      document.getElementById("full_name").value = data.full_name;
      document.getElementById("email").value = data.email;
      document.getElementById("phone").value = data.phone;
      document.getElementById("dob").value = data.dob;
      document.getElementById("gender").value = data.gender;
      document.getElementById("address").value = data.address;
      document.getElementById("city").value = data.city;
      document.getElementById("state").value = data.state;
      document.getElementById("country").value = data.country;
    });

    // Delete
    row.querySelector(".delete-btn").addEventListener("click", function(){
      if(confirm("Are you sure you want to delete this record?")){
        frappe.call({
          method: "demo_app.www.form.form.delete_user_detail",
          args: { name: data.name },
          headers: { "X-Frappe-CSRF-Token": frappe.csrf_token },
          callback: function(r){
            if(r.exc){
              show("Error deleting: " + r.exc, false);
            } else {
              show("Record deleted", true);
              row.remove();
              clearForm();
            }
          }
        });
      }
    });
  }

  // Load existing records on page load
  frappe.call({
    method: "demo_app.www.form.form.get_all_users",
    headers: { "X-Frappe-CSRF-Token": frappe.csrf_token },
    callback: function(r){
      if(r.message){
        r.message.forEach(u => addRowToTable(u));
      }
    }
  });

  // Submit
  btn.addEventListener('click', function(){
    const full_name = document.getElementById('full_name').value.trim();
    const email = document.getElementById('email').value.trim();

    if(!full_name || !email){
      show("Full Name and Email are required", false);
      return;
    }

    const data = {
      name: userIdInput.value || null,
      full_name,
      email,
      phone: document.getElementById('phone').value,
      dob: document.getElementById('dob').value,
      gender: document.getElementById('gender').value,
      address: document.getElementById('address').value,
      city: document.getElementById('city').value,
      state: document.getElementById('state').value,
      country: document.getElementById('country').value
    };

    const method = data.name ? "demo_app.www.update_user_detail" : "demo_app.www.save_user_detail";

    frappe.call({
      method:"demo_app.www.form.form.save_user_detail",
      args: data,
      headers: { "X-Frappe-CSRF-Token": frappe.csrf_token },
      callback: function(r){
        if(r.exc){
          show("Error saving user: " + r.exc, false);
        } else {
          show("User saved successfully! ID: " + r.message, true);
          if(!data.name){
            data.name = r.message;
            addRowToTable(data);
          } else {
            const row = tableBody.querySelector(`tr[data-name="${data.name}"]`);
            if(row){
              row.cells[0].innerText = data.full_name;
              row.cells[1].innerText = data.email;
              row.cells[2].innerText = data.phone;
              row.cells[3].innerText = data.dob;
              row.cells[4].innerText = data.gender;
              row.cells[5].innerText = data.city;
              row.cells[6].innerText = data.state;
              row.cells[7].innerText = data.country;
            }
          }
          clearForm();
        }
      }
    });
  });
});



// method: "demo_app.www.form.form.save_user_detail",
// headers: { "X-Frappe-CSRF-Token": frappe.csrf_token },