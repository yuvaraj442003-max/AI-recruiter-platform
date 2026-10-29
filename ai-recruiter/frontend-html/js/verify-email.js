/**
 * verify-email.js — OTP verification has been removed.
 * Automatically forwards users to their dashboard or login.
 */
(function () {
  if (typeof Session !== "undefined" && Session.isLoggedIn()) {
    const user = Session.getUser();
    const target = typeof dashboardUrlForRole === "function" ? dashboardUrlForRole(user?.role) : "login.html";
    window.location.href = target;
    return;
  }

  const alertBox = document.getElementById("verify-alert");
  if (alertBox) {
    alertBox.className = "alert alert-info py-2 mb-4 small fw-semibold";
    alertBox.textContent = "Email verification is not required. Redirecting to login...";
    alertBox.classList.remove("d-none");
  }

  setTimeout(() => {
    window.location.href = "login.html";
  }, 500);
})();
