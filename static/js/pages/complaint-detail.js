// complaint-detail.js - Complaint Detail page.
// Students see the complaint and the replies.
// Staff of the right department also see three forms: status, reply, re-route.

const user = checkLogin();       // any logged-in user
const id = new URLSearchParams(window.location.search).get("id");    // from the address: ?id=c1

async function start() {
  document.getElementById("back-link").href = homeFor(user.role);

  const departments = await loadDepartments();
  const complaint = await api("/complaints/" + id);
  showComplaint(complaint);

  // only staff see the action forms
  if (user.role === "staff") {
    fillDepartmentSelect(document.getElementById("new-department"), departments);
    document.getElementById("new-department").value = complaint.department;
    document.getElementById("new-status").value = complaint.status;
    document.getElementById("staff-section").hidden = false;
  }
}

// Draws the complaint and its replies
function showComplaint(c) {
  document.getElementById("complaint").innerHTML =
    "<h1>" + esc(c.title) + "</h1>" +
    "<p>" + badge(c.status) + "</p>" +
    "<p>" + esc(c.description) + "</p>" +
    '<p class="hint">Department: ' + esc(deptName(c.department)) +
    " | Suggested by model: " + esc(deptName(c.predicted_department)) +
    " | Submitted: " + formatDate(c.created_at) + "</p>";

  let html = "";
  c.responses.forEach(function (r) {
    html += "<li><p><strong>" + esc(r.by) + "</strong> on " + formatDate(r.at) + "</p>" +
      "<p>" + esc(r.message) + "</p></li>";
  });
  if (html === "") {
    html = '<li class="empty">No replies yet.</li>';
  }
  document.getElementById("replies").innerHTML = html;
}

// 1. Change status
document.getElementById("status-form").addEventListener("submit", async function (event) {
  event.preventDefault();
  try {
    const updated = await api("/complaints/" + id + "/status", "PATCH", {
      status: document.getElementById("new-status").value
    });
    showComplaint(updated);
    showMessage("form-message", "Status updated.");
  } catch (error) {
    showMessage("form-message", error.message, true);
  }
});

// 2. Send a reply
document.getElementById("reply-form").addEventListener("submit", async function (event) {
  event.preventDefault();
  try {
    const updated = await api("/complaints/" + id + "/respond", "POST", {
      message: document.getElementById("reply").value
    });
    showComplaint(updated);
    document.getElementById("reply").value = "";
    showMessage("form-message", "Reply sent.");
  } catch (error) {
    showMessage("form-message", error.message, true);
  }
});

// 3. Re-route to another department
document.getElementById("reroute-form").addEventListener("submit", async function (event) {
  event.preventDefault();
  try {
    const updated = await api("/complaints/" + id + "/reroute", "PATCH", {
      department: document.getElementById("new-department").value
    });
    showComplaint(updated);
    showMessage("form-message", "Moved to " + deptName(updated.department) + ".");
  } catch (error) {
    showMessage("form-message", error.message, true);
  }
});

if (user) {
  start();
}
