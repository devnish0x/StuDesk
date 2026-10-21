// index.js — Landing page only.
// The FAQ uses <details>/<summary> which works without JavaScript.
// This file only adds smooth scrolling for the nav anchor links.

document.querySelectorAll('a[href^="#"]').forEach(function (link) {
  link.addEventListener("click", function (event) {
    var target = document.querySelector(link.getAttribute("href"));
    if (!target) return;
    event.preventDefault();
    target.scrollIntoView({ behavior: "smooth", block: "start" });
  });
});
