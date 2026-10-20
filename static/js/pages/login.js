// login.js - Login and Register page with 3D card flip animation

// If the person is already logged in, skip this page.
if (getUser() !== null) {
  window.location.href = homeFor(getUser().role);
}

// ===== 3D Card Flip Animation =====
const flipCard = document.querySelector('.flip-card');
const flipCardInner = document.getElementById('flip-card-inner');
const showRegister = document.getElementById('show-register');
const showLogin = document.getElementById('show-login');

// Flip to Register form
if (showRegister) {
  showRegister.addEventListener('click', function (e) {
    e.preventDefault();
    flipCard.classList.add('flipped');
    // Clear login message when switching
    document.getElementById('login-message').textContent = '';
  });
}

// Flip back to Login form  
if (showLogin) {
  showLogin.addEventListener('click', function (e) {
    e.preventDefault();
    flipCard.classList.remove('flipped');
    // Clear register message when switching
    document.getElementById('register-message').textContent = '';
  });
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