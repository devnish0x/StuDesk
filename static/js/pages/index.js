/* Home page (Module 1) */

// Live demo: calls the same /api/predict that the Submit page uses
document.getElementById("demo-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const result = document.getElementById("demo-result");
  result.textContent = "Checking...";
  try {
    const data = await api("/predict", { method: "POST", body: { text: document.getElementById("demo-text").value } });
    result.textContent = "This would go to: " + data.department.toUpperCase() + " (confidence " + Math.round(data.confidence * 100) + "%)";
  } catch (error) {
    result.textContent = error.message;
  }
});

// FAQ accordion: each button shows or hides the paragraph it controls
document.querySelectorAll(".faq-btn").forEach((button) => {
  button.addEventListener("click", () => {
    const open = button.getAttribute("aria-expanded") === "true";
    button.setAttribute("aria-expanded", String(!open));
    document.getElementById(button.getAttribute("aria-controls")).hidden = open;
  });
});
