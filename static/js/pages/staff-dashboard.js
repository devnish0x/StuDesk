// staff-dashboard.js - Department Dashboard page (staff only).

const user = checkLogin("staff");
let complaints = [];     // all complaints of this staff member's department

async function start() {
  await loadDepartments();
  document.getElementById("dept-name").textContent = deptName(user.department);

  complaints = await api("/complaints/department");

  // count how many are still waiting
  let pending = 0;
  complaints.forEach(function (c) {
    if (c.status === "pending") {
      pending++;
    }
  });
  document.getElementById("summary").textContent =
    complaints.length + " complaints in total, " + pending + " waiting for a response.";

  showComplaints();
}

// Draws the table rows, using the status filter and the search box
function showComplaints() {
  const chosen = document.getElementById("filter-status").value;
  const search = document.getElementById("search").value.toLowerCase();
  let html = "";
  let count = 0;

  complaints.forEach(function (c) {
    const statusMatches = chosen === "all" || c.status === chosen;
    const textMatches = c.title.toLowerCase().includes(search);

    if (statusMatches && textMatches) {
      count++;
      html += "<tr>" +
        '<td data-label="Title">' + esc(c.title) + "</td>" +
        '<td data-label="Status">' + badge(c.status) + "</td>" +
        '<td data-label="Date">' + formatDate(c.created_at) + "</td>" +
        '<td data-label="Replies">' + c.responses.length + "</td>" +
        '<td data-label="Open"><a href="/complaint-detail.html?id=' + c.id + '">Open</a></td>' +
        "</tr>";
    }
  });

  document.getElementById("complaint-rows").innerHTML = html;
  document.getElementById("empty-message").hidden = count > 0;
}

document.getElementById("filter-status").addEventListener("change", showComplaints);
document.getElementById("search").addEventListener("input", showComplaints);

if (user) {
  start();
}
