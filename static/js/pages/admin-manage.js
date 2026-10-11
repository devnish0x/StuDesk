// admin-manage.js - Manage Users and Departments page (admin only).

const user = checkLogin("admin");

// Draws the users table, the departments list and the department dropdown
async function start() {
  const departments = await loadDepartments();
  const users = await api("/admin/users");

  // ----- users table -----
  let rows = "";
  users.forEach(function (u) {
    const removeButton = u.id === user.id
      ? "-"      // you cannot remove yourself
      : '<button class="btn btn-danger btn-small" type="button" onclick="removeUser(\'' + u.id + '\')">Remove</button>';

    rows += "<tr>" +
      '<td data-label="Name">' + esc(u.name) + "</td>" +
      '<td data-label="Email">' + esc(u.email) + "</td>" +
      '<td data-label="Role">' + u.role + "</td>" +
      '<td data-label="Department">' + (u.department ? esc(deptName(u.department)) : "-") + "</td>" +
      '<td data-label="Remove">' + removeButton + "</td>" +
      "</tr>";
  });
  document.getElementById("user-rows").innerHTML = rows;

  // ----- departments list -----
  let list = "";
  departments.forEach(function (d) {
    list += '<li class="card dept-item">' +
      "<p><strong>" + esc(d.name) + "</strong><br><span class=\"hint\">" + esc(d.description) + "</span></p>" +
      '<button class="btn btn-danger btn-small" type="button" onclick="removeDepartment(\'' + d.id + '\')">Remove</button>' +
      "</li>";
  });
  document.getElementById("dept-list").innerHTML = list;

  // ----- department dropdown inside the "Add staff" form -----
  const select = document.getElementById("staff-department");
  select.innerHTML = "";
  fillDepartmentSelect(select, departments);
}

async function removeUser(userId) {
  if (!confirm("Remove this user?")) {
    return;
  }
  try {
    await api("/admin/users/" + userId, "DELETE");
    showMessage("page-message", "User removed.");
    start();
  } catch (error) {
    showMessage("page-message", error.message, true);
  }
}

async function removeDepartment(deptId) {
  if (!confirm("Remove this department?")) {
    return;
  }
  try {
    await api("/admin/departments/" + deptId, "DELETE");
    showMessage("page-message", "Department removed.");
    start();
  } catch (error) {
    showMessage("page-message", error.message, true);
  }
}

// Add a staff member
document.getElementById("staff-form").addEventListener("submit", async function (event) {
  event.preventDefault();
  try {
    await api("/admin/users", "POST", {
      name: document.getElementById("staff-name").value,
      email: document.getElementById("staff-email").value,
      password: document.getElementById("staff-password").value,
      department: document.getElementById("staff-department").value
    });
    document.getElementById("staff-form").reset();
    showMessage("page-message", "Staff member added.");
    start();
  } catch (error) {
    showMessage("page-message", error.message, true);
  }
});

// Add a department
document.getElementById("dept-form").addEventListener("submit", async function (event) {
  event.preventDefault();
  try {
    await api("/admin/departments", "POST", {
      name: document.getElementById("dept-name").value,
      description: document.getElementById("dept-description").value
    });
    document.getElementById("dept-form").reset();
    showMessage("page-message", "Department added.");
    start();
  } catch (error) {
    showMessage("page-message", error.message, true);
  }
});

if (user) {
  start();
}
