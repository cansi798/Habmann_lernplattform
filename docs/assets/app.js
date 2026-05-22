// Lernplatt — app.js
// Logout binding for any page that has a .brand-bar .logout link.

function bindLogoutLinks() {
  document.querySelectorAll(".brand-bar .logout").forEach(link => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      if (typeof logout === "function") logout();
    });
  });
}
document.addEventListener("DOMContentLoaded", bindLogoutLinks);
