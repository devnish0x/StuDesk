// common.js - helper functions used by every page.
// Every page loads this file first:  <script src="/static/js/common.js"></script>
// Then it loads its own file, e.g.   <script src="/static/js/pages/login.js"></script>

// ---------- Login session ----------
// After login the backend gives us a token and the user's details.
// We keep both in sessionStorage (cleared when the tab is closed).
function saveSession(token, user) {
  sessionStorage.setItem("token", token);
  sessionStorage.setItem("user", JSON.stringify(user));
}

function getToken() {
  return sessionStorage.getItem("token");
}

function getUser() {
  return JSON.parse(sessionStorage.getItem("user"));
}

function logout() {
  sessionStorage.clear();
}

// Which page each role starts on
function homeFor(role) {
  if (role === "student") return "/my-complaints.html";
  if (role === "staff") return "/staff-dashboard.html";
  return "/admin-dashboard.html";
}

// Put at the top of a protected page.
// checkLogin("student") = only students.  checkLogin() = any logged-in user.
// Returns the user, or sends the visitor away and returns null.
function checkLogin(role) {
  const user = getUser();
  if (user === null) {
    window.location.href = "/login.html";
    return null;
  }
  if (role && user.role !== role) {
    window.location.href = homeFor(user.role);
    return null;
  }
  return user;
}

// ---------- Talking to the backend ----------
// const departments = await api("/departments");
// const result = await api("/complaints", "POST", { title: "...", description: "..." });
// It adds the token to every request:  Authorization: Bearer <token>
async function api(url, method, body) {
  const headers = { "Content-Type": "application/json" };
  const token = getToken();
  if (token) {
    headers["Authorization"] = "Bearer " + token;
  }

  const options = { method: method || "GET", headers: headers };
  if (body) {
    options.body = JSON.stringify(body);
  }

  const response = await fetch("/api" + url, options);
  const data = await response.json();

  if (!response.ok) {
    // 401 = token missing or expired (for example the server restarted)
    if (response.status === 401 && token) {
      logout();
      window.location.href = "/login.html";
    }
    // FastAPI sends errors as {"detail": "text"} or {"detail": [ ...list... ]}
    if (typeof data.detail === "string") {
      throw new Error(data.detail);
    }
    throw new Error("Please check what you typed and try again.");
  }
  return data;
}

// ---------- Small helpers ----------
// Shows a message inside the <p> with this id. Pass true for an error.
function showMessage(id, text, isError) {
  const box = document.getElementById(id);
  box.textContent = text;
  box.className = isError ? "message error" : "message";
}

// Use esc() on any text typed by a user before putting it into innerHTML
function esc(text) {
  const div = document.createElement("div");
  div.textContent = text === null || text === undefined ? "" : text;
  return div.innerHTML;
}

function formatDate(iso) {
  return new Date(iso).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });
}

const STATUS_NAMES = {
  pending: "Pending", in_progress: "In progress", resolved: "Resolved",
  new: "New", reviewed: "Reviewed", implemented: "Implemented"
};

function badge(status) {
  return '<span class="badge badge-' + status + '">' + STATUS_NAMES[status] + "</span>";
}

// Departments: call loadDepartments() once, then deptName("it") gives "IT Services"
let departmentNames = {};

async function loadDepartments() {
  const list = await api("/departments");
  list.forEach(function (d) {
    departmentNames[d.id] = d.name;
  });
  return list;
}

function deptName(id) {
  return departmentNames[id] || id;
}

// Adds one <option> per department into a <select>
function fillDepartmentSelect(select, list) {
  list.forEach(function (d) {
    select.innerHTML += '<option value="' + d.id + '">' + esc(d.name) + "</option>";
  });
}
