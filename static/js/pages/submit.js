// submit.js - Submit Complaint page (students only).

const user = checkLogin("student");

// Fill the department dropdown when the page opens
async function start() {
  const departments = await loadDepartments();
  fillDepartmentSelect(document.getElementById("department"), departments);
}

// "Suggest department" button: asks the ML model and selects its answer
document.getElementById("suggest-btn").addEventListener("click", async function () {
  const title = document.getElementById("title").value;
  const description = document.getElementById("description").value;

  try {
    const result = await api("/predict", "POST", { text: title + ". " + description });
    document.getElementById("department").value = result.department;
    const percent = Math.round(result.confidence * 100);
    showMessage("suggest-result", "Suggested: " + deptName(result.department) + " (" + percent + "% sure). You can change it.");
  } catch (error) {
    showMessage("suggest-result", "Write a title and a description first.", true);
  }
});

// Submit the complaint
document.getElementById("complaint-form").addEventListener("submit", async function (event) {
  event.preventDefault();

  try {
    await api("/complaints", "POST", {
      title: document.getElementById("title").value,
      description: document.getElementById("description").value,
      department: document.getElementById("department").value   // "" means "let StuDesk decide"
    });
    showMessage("form-message", "Complaint submitted. Taking you to your list...");
    setTimeout(function () {
      window.location.href = "/my-complaints.html";
    }, 1200);
  } catch (error) {
    showMessage("form-message", error.message, true);
  }
});

if (user) {
  start();
}
