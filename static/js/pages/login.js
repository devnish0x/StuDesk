// login.js - Login and Register page.

// If the person is already logged in, skip this page.
if (getUser() !== null) {
  window.location.href = homeFor(getUser().role);
}

// ----- Login -----
document.getElementById("login-form").addEventListener("submit", async function (event) {
  event.preventDefault();

  try {
    const result = await api("/login", "POST", {
      email: document.getElementById("login-email").value,
      password: document.getElementById("login-password").value
    });
    // result = { token: "...", user: { id, name, email, role, department } }
    saveSession(result.token, result.user);
    window.location.href = homeFor(result.user.role);
  } catch (error) {
    showMessage("login-message", error.message, true);
  }
});

// ----- Register (students only) -----
document.getElementById("register-form").addEventListener("submit", async function (event) {
  event.preventDefault();

  try {
    const result = await api("/register", "POST", {
      name: document.getElementById("reg-name").value,
      email: document.getElementById("reg-email").value,
      password: document.getElementById("reg-password").value
    });
    saveSession(result.token, result.user);
    window.location.href = homeFor(result.user.role);
  } catch (error) {
    showMessage("register-message", error.message, true);
  }
});
