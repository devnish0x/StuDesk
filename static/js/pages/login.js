/* Login / Register (Module 1) */
let mode = "login"; // or "register"

const form = document.getElementById("auth-form");
const errorBox = document.getElementById("form-error");

function setMode(newMode) {
  mode = newMode;
  const registering = mode === "register";
  document.getElementById("form-title").textContent = registering ? "Create your account" : "Log in";
  document.getElementById("submit-btn").textContent = registering ? "Create account" : "Log in";
  document.getElementById("switch-text").textContent = registering ? "Already registered?" : "New here?";
  document.getElementById("switch-btn").textContent = registering ? "Log in instead" : "Create a student account";
  document.getElementById("name-field").hidden = !registering;
  document.getElementById("password").autocomplete = registering ? "new-password" : "current-password";
  errorBox.textContent = "";
}

document.getElementById("switch-btn").addEventListener("click", () => setMode(mode === "login" ? "register" : "login"));

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorBox.textContent = "";
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;
  const name = document.getElementById("name").value.trim();

  // Simple checks before we bother the server
  if (!email || !password) { errorBox.textContent = "Enter your email and password."; return; }
  if (password.length < 6) { errorBox.textContent = "Password must be at least 6 characters."; return; }
  if (mode === "register" && name.length < 2) { errorBox.textContent = "Enter your full name."; return; }

  try {
    const result = mode === "login"
      ? await api("/login", { method: "POST", body: { email, password } })
      : await api("/register", { method: "POST", body: { name, email, password } });
    saveSession(result.token, result.user);
    window.location.href = homeFor(result.user.role);
  } catch (error) {
    errorBox.textContent = error.message;
  }
});

// Already logged in? Skip this page.
if (getUser()) window.location.href = homeFor(getUser().role);
