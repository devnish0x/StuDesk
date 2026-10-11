// my-complaints.js - My Complaints page (students only).

const user = checkLogin("student");
let complaints = [];     // all of this student's complaints

async function start() {
  await loadDepartments();
  complaints = await api("/complaints/mine");
  showComplaints();
}

// Draws the table rows, using the filter dropdown
function showComplaints() {
  const chosen = document.getElementById("filter-status").value;
  let html = "";
  let count = 0;

  complaints.forEach(function (c) {
    if (chosen === "all" || c.status === chosen) {
      count++;
      html += "<tr>" +
        '<td data-label="Title">' + esc(c.title) + "</td>" +
        '<td data-label="Department">' + esc(deptName(c.department)) + "</td>" +
        '<td data-label="Status">' + badge(c.status) + "</td>" +
        '<td data-label="Date">' + formatDate(c.created_at) + "</td>" +
        '<td data-label="Details"><a href="/complaint-detail.html?id=' + c.id + '">View</a></td>' +
        "</tr>";
    }
  });

  document.getElementById("complaint-rows").innerHTML = html;
  document.getElementById("empty-message").hidden = count > 0;   // show the empty message when nothing matches
}

document.getElementById("filter-status").addEventListener("change", showComplaints);

if (user) {
  start();
}
