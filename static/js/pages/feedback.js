// feedback.js - Feedback and Suggestions page (students only).

const user = checkLogin("student");

// Show how many characters have been typed
document.getElementById("message").addEventListener("input", function () {
  document.getElementById("char-count").textContent = this.value.length;
});

// Load this student's earlier submissions
async function loadMine() {
  const items = await api("/feedback/mine");
  let html = "";

  items.forEach(function (f) {
    html += '<li class="card">' +
      "<h3>" + esc(f.title) + "</h3>" +
      "<p>" + badge(f.status) + " " + f.type + " about " + f.category +
      (f.rating ? ", rated " + f.rating + "/5" : "") + "</p>" +
      "<p>" + esc(f.message) + "</p>" +
      (f.admin_reply ? '<p class="reply-box"><strong>Reply:</strong> ' + esc(f.admin_reply) + "</p>" : "") +
      "</li>";
  });

  document.getElementById("my-feedback").innerHTML = html;
  document.getElementById("empty-message").hidden = items.length > 0;
}

// Send new feedback
document.getElementById("feedback-form").addEventListener("submit", async function (event) {
  event.preventDefault();

  const chosenRating = document.querySelector('input[name="rating"]:checked');   // null if none chosen

  try {
    await api("/feedback", "POST", {
      type: document.getElementById("type").value,
      category: document.getElementById("category").value,
      title: document.getElementById("title").value,
      message: document.getElementById("message").value,
      rating: chosenRating ? Number(chosenRating.value) : null,
      anonymous: document.getElementById("anonymous").checked
    });
    showMessage("form-message", "Thank you! Your message was sent.");
    document.getElementById("feedback-form").reset();
    document.getElementById("char-count").textContent = "0";
    loadMine();
  } catch (error) {
    showMessage("form-message", error.message, true);
  }
});

if (user) {
  loadMine();
}
