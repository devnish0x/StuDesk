// admin-feedback.js - Feedback Review page (admin only).

const user = checkLogin("admin");
let items = [];      // all feedback and suggestions

async function start() {
  items = await api("/admin/feedback");
  showItems();
}

// One <option> for the status dropdown, selected if it matches the current status
function statusOption(value, label, current) {
  return '<option value="' + value + '"' + (value === current ? " selected" : "") + ">" + label + "</option>";
}

// Draws the cards, using the two filters
function showItems() {
  const type = document.getElementById("filter-type").value;
  const status = document.getElementById("filter-status").value;
  let html = "";
  let count = 0;

  items.forEach(function (f) {
    if ((type === "all" || f.type === type) && (status === "all" || f.status === status)) {
      count++;
      html += '<li class="card review-card">' +
        "<h2>" + esc(f.title) + "</h2>" +
        "<p>" + badge(f.status) + " " + f.type + " about " + f.category +
        (f.rating ? ", rated " + f.rating + "/5" : "") + "</p>" +
        "<p>" + esc(f.message) + "</p>" +
        '<p class="review-meta">From ' + esc(f.from_name) + " on " + formatDate(f.created_at) + "</p>" +
        '<div class="review-form">' +
        '<div class="field"><label for="reply-' + f.id + '">Your reply</label>' +
        '<textarea id="reply-' + f.id + '">' + esc(f.admin_reply) + "</textarea></div>" +
        '<div class="field"><label for="status-' + f.id + '">Status</label>' +
        '<select id="status-' + f.id + '">' +
        statusOption("new", "New", f.status) +
        statusOption("reviewed", "Reviewed", f.status) +
        statusOption("implemented", "Implemented", f.status) +
        "</select></div>" +
        '<div><button class="btn" type="button" onclick="saveReview(\'' + f.id + '\')">Save</button></div>' +
        "</div></li>";
    }
  });

  document.getElementById("feedback-list").innerHTML = html;
  document.getElementById("empty-message").hidden = count > 0;
}

// Called by the Save button on a card
async function saveReview(feedbackId) {
  try {
    await api("/admin/feedback/" + feedbackId, "PATCH", {
      status: document.getElementById("status-" + feedbackId).value,
      admin_reply: document.getElementById("reply-" + feedbackId).value
    });
    showMessage("page-message", "Saved.");
    start();      // reload the list
  } catch (error) {
    showMessage("page-message", error.message, true);
  }
}

document.getElementById("filter-type").addEventListener("change", showItems);
document.getElementById("filter-status").addEventListener("change", showItems);

if (user) {
  start();
}
