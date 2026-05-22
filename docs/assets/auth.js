// Lernplatt — auth.js
// Visibility barrier: SHA-256(code) compared to constant.

const AUTH_HASH = "7706d7bdc034343163088e3a2462b772951d448690fd94a4a54c219109341217";
const SESSION_KEY = "lernplatt-auth";

async function sha256Hex(text) {
  const buf = new TextEncoder().encode(text);
  const hash = await crypto.subtle.digest("SHA-256", buf);
  return Array.from(new Uint8Array(hash))
    .map(b => b.toString(16).padStart(2, "0"))
    .join("");
}

async function attemptLogin(code) {
  return (await sha256Hex(code)) === AUTH_HASH;
}

function setAuthenticated() { sessionStorage.setItem(SESSION_KEY, String(Date.now())); }
function isAuthenticated() { return !!sessionStorage.getItem(SESSION_KEY); }

function requireAuth() {
  if (!isAuthenticated()) {
    const depth = window.location.pathname.split("/").filter(p => p && p !== "Habmann_lernplattform").length - 1;
    const prefix = depth > 0 ? "../".repeat(depth) : "./";
    window.location.replace(prefix + "index.html");
  }
}

function logout() {
  sessionStorage.removeItem(SESSION_KEY);
  window.location.replace("./index.html");
}
