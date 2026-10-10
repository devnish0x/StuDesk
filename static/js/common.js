/* ==========================================================
   common.js  -  shared by every page. Load it on every page:
   <script src="/static/js/common.js"></script>
   Gives you:  api(), getUser(), requireRole(), showToast(), escapeHtml(), formatDate()
   and builds the navbar + footer automatically.
   ========================================================== */

const TOKEN_KEY = "studesk_token";
const USER_KEY = "studesk_user";

/* ---------- Session ---------- */
function getToken() { return sessionStorage.getItem(TOKEN_KEY); }
function getUser() {
  try { return JSON.parse(sessionStorage.getItem(USER_KEY)); } catch { return null; }
}
function saveSession(token, user) {
  sessionStorage.setItem(TOKEN_KEY, token);
  sessionStorage.setItem(USER_KEY, JSON.stringify(user));
}
function logout() {
  sessionStorage.clear();
  window.location.href = "/login.html";
}
/* Where each role lands after login */
function homeFor(role) {
  return { student: "/my-complaints.html", staff: "/staff-dashboard.html", admin: "/admin-dashboard.html" }[role] || "/";
}
/* Call at the top of a page's script: requireRole("student") */
function requireRole(...roles) {
  const user = getUser();
  if (!user) { window.location.href = "/login.html"; return null; }
  if (!roles.includes(user.role)) { window.location.href = homeFor(user.role); return null; }
  return user;
}

/* ---------- Talking to the backend ----------
   const data = await api("/complaints/mine");
   const made = await api("/complaints", { method: "POST", body: { title, description } });
   Errors throw an Error whose message is shown to the user. */
async function api(path, { method = "GET", body = null } = {}) {
  const headers = { "Content-Type": "application/json" };
  const token = getToken();
  if (token) headers["Authorization"] = "Bearer " + token;

  const response = await fetch("/api" + path, { method, headers, body: body ? JSON.stringify(body) : null });
  let data = null;
  try { data = await response.json(); } catch { /* no JSON body */ }

  if (!response.ok) {
    if (response.status === 401 && token) { logout(); }
    let message = "Something went wrong. Please try again.";
    if (data && typeof data.detail === "string") message = data.detail;
    else if (data && Array.isArray(data.detail)) message = "Please check the form: " + data.detail.map(d => d.loc[d.loc.length - 1] + " - " + d.msg).join("; ");
    throw new Error(message);
  }
  return data;
}

/* ---------- Small helpers ---------- */
function showToast(message, isError = false) {
  const toast = document.getElementById("toast");
  if (!toast) return;
  toast.textContent = message;
  toast.className = "toast show" + (isError ? " error" : "");
  clearTimeout(showToast.timer);
  showToast.timer = setTimeout(() => { toast.className = "toast"; }, 4000);
}
/* ALWAYS wrap user text in this before putting it into innerHTML */
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text ?? "";
  return div.innerHTML;
}
function formatDate(iso) {
  return new Date(iso).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });
}
function statusLabel(status) {
  return { pending: "Pending", in_progress: "In progress", resolved: "Resolved",
           new: "New", reviewed: "Reviewed", implemented: "Implemented" }[status] || status;
}

/* ---------- Navbar and footer ---------- */
const NAV_LINKS = {
  guest:   [["/", "Home"], ["/login.html", "Log in"]],
  student: [["/submit.html", "New complaint"], ["/my-complaints.html", "My complaints"], ["/feedback.html", "Feedback"]],
  staff:   [["/staff-dashboard.html", "Dashboard"]],
  admin:   [["/admin-dashboard.html", "Dashboard"], ["/admin-feedback.html", "Feedback"], ["/admin-manage.html", "Manage"]],
};

function buildChrome() {
  const user = getUser();
  const links = NAV_LINKS[user ? user.role : "guest"];
  const here = window.location.pathname;
  const items = links.map(([href, label]) =>
    `<li><a href="${href}"${href === here ? ' aria-current="page"' : ""}>${label}</a></li>`).join("");
  const logoutItem = user ? `<li><button type="button" id="logout-btn">Log out (${escapeHtml(user.name)})</button></li>` : "";

  const header = document.getElementById("site-header");
  if (header) {
    header.className = "site-header";
    header.innerHTML = `
      <nav class="nav" aria-label="Main">
        <a class="brand" href="/">Stu<span>Desk</span></a>
        <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-links">Menu</button>
        <ul class="nav-links" id="nav-links">${items}${logoutItem}</ul>
      </nav>`;
    const toggle = header.querySelector(".nav-toggle");
    toggle.addEventListener("click", () => {
      const open = header.querySelector(".nav-links").classList.toggle("open");
      toggle.setAttribute("aria-expanded", open);
    });
    const logoutBtn = document.getElementById("logout-btn");
    if (logoutBtn) logoutBtn.addEventListener("click", logout);
  }

  const footer = document.getElementById("site-footer");
  if (footer) {
    footer.className = "site-footer";
    footer.innerHTML = `<p>StuDesk: complaints and feedback for our campus. MCA Web Technology mini project.</p>`;
  }
}
document.addEventListener("DOMContentLoaded", buildChrome);
