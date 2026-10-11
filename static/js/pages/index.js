// index.js - Home page.
// The "Try the router" box: sends the text to /api/predict and shows the department.

document.getElementById("demo-form").addEventListener("submit", async function (event) {
  event.preventDefault();   // stop the page from reloading

  const text = document.getElementById("demo-text").value;

  try {
    await loadDepartments();                                   // so we can show the department's full name
    const result = await api("/predict", "POST", { text: text });
    const percent = Math.round(result.confidence * 100);
    showMessage("demo-result", "This would go to: " + deptName(result.department) + " (" + percent + "% sure)");
  } catch (error) {
    showMessage("demo-result", error.message, true);
  }
});
