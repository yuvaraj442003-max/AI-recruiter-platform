/**
 * auth-guard.js — include this on any page that requires login.
 * Redirects to login.html if there's no token, and verifies the
 * token is still valid by calling /auth/me. Optionally restricts
 * the page to a specific role via `data-required-role` on <body>.
 */
(async function guard() {
  if (!Session.isLoggedIn()) {
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
    Session.clear();
    window.location.href = "login.html";
  }
})();
