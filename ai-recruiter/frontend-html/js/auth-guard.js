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
    if (requiredRole) {
      const isRecruiterRole = (requiredRole === "recruiter" && (user.role === "recruiter" || user.role === "company_admin"));
      const isCandidateRole = (requiredRole === "candidate" && user.role === "candidate");
      const isAdminRole = (requiredRole === "admin" && (user.role === "admin" || user.role === "superadmin"));

      if (!isRecruiterRole && !isCandidateRole && !isAdminRole && user.role !== requiredRole) {
        window.location.href = dashboardUrlForRole(user.role);
        return;
      }
    }

    window.__AR_AUTH_READY = true;
    window.__AR_USER = user;
    document.dispatchEvent(new CustomEvent("ar:auth-ready", { detail: { user } }));

  } catch (err) {
    if (err?.status === 401) {
      if (typeof Session !== "undefined" && Session.clear) {
        Session.clear();
      }
      window.location.href = "login.html?expired=1";
    } else {
      console.warn("Auth guard warning:", err);
    }
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
