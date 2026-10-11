// admin-dashboard.js - Admin Dashboard page (admin only).

const user = checkLogin("admin");

// One number card
function card(number, label) {
  return '<div class="card stat"><strong>' + number + "</strong>" + label + "</div>";
}

async function start() {
  const departments = await loadDepartments();
  const stats = await api("/admin/stats");

  // complaint numbers (a status that nobody has yet is missing, so we use || 0)
  document.getElementById("stat-cards").innerHTML =
    card(stats.total_complaints, "Total complaints") +
    card(stats.by_status.pending || 0, "Pending") +
    card(stats.by_status.in_progress || 0, "In progress") +
    card(stats.by_status.resolved || 0, "Resolved");

  // find the biggest department so the longest bar is 100% wide
  let biggest = 1;
  departments.forEach(function (d) {
    const count = stats.by_department[d.id] || 0;
    if (count > biggest) {
      biggest = count;
    }
  });

  // one bar per department
  let bars = "";
  departments.forEach(function (d) {
    const count = stats.by_department[d.id] || 0;
    const width = (count / biggest) * 100;
    bars += '<div class="bar-row"><span>' + esc(d.name) + "</span>" +
      '<div class="bar"><div style="width:' + width + '%"></div></div>' +
      "<span>" + count + "</span></div>";
  });
  document.getElementById("dept-bars").innerHTML = bars;

  // feedback and model numbers (null means there is no data yet)
  const rating = stats.average_rating === null ? "-" : stats.average_rating + "/5";
  const accuracy = stats.model_accuracy === null ? "-" : stats.model_accuracy + "%";
  document.getElementById("other-cards").innerHTML =
    card(stats.total_feedback, "Feedback received") +
    card(rating, "Average rating") +
    card(accuracy, "Model got the department right");
}

if (user) {
  start();
}
