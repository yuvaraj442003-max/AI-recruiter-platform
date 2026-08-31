/**
 * dashboard.js — shared behavior for both dashboard pages.
 * Waits for auth-guard.js to confirm the session, then fills in
 * the user's name and wires up the logout buttons.
 */
document.addEventListener("ar:auth-ready", (event) => {
  const { user } = event.detail;

  const greeting = document.getElementById("user-greeting");
  if (greeting) {
    greeting.textContent = `${user.name} · ${user.role}`;
    greeting.classList.remove("skeleton");
  }

  const nameSpan = document.getElementById("user-name");
  if (nameSpan) nameSpan.textContent = user.name;
});

function handleLogout() {
  authAPI.logout();
  window.location.href = "login.html";
}

document.getElementById("logout-btn")?.addEventListener("click", handleLogout);
document.getElementById("logout-btn-mobile")?.addEventListener("click", handleLogout);
