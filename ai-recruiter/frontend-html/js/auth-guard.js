/**
 * auth-guard.js — include this on any page that requires login.
 * Redirects to login.html if there's no token, and verifies the
 * token is still valid by calling /auth/me. Optionally restricts
 * the page to a specific role via `data-required-role` on <body>.
 */
(async function guard() {
  if (typeof Session === "undefined" || !Session.isLoggedIn()) {
    window.location.href = "login.html";
    return;
  }

  try {
    const res = await authAPI.me();
    const user = res.data;
    if (typeof safeStorage !== "undefined") {
      safeStorage.setItem("ar_user", JSON.stringify(user));
    } else {
      try { localStorage.setItem("ar_user", JSON.stringify(user)); } catch (e) {}
    }

    const requiredRole = document.body.dataset.requiredRole;
    if (requiredRole && user.role !== requiredRole) {
      window.location.href = dashboardUrlForRole(user.role);
      return;
    }

    window.__AR_AUTH_READY = true;
    window.__AR_USER = user;
    document.dispatchEvent(new CustomEvent("ar:auth-ready", { detail: { user } }));

  } catch (err) {
    if (typeof Session !== "undefined" && Session.clear) {
      Session.clear();
    }
    window.location.href = "login.html";
  }
})();

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("#logout-btn, #logout-btn-mobile").forEach(btn => {
    btn.addEventListener("click", () => {
      if (typeof authAPI !== "undefined" && authAPI.logout) authAPI.logout();
      else if (typeof Session !== "undefined" && Session.clear) Session.clear();
      window.location.href = "login.html";
    });
  });
});
