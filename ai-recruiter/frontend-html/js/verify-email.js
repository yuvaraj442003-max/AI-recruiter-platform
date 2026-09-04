/**
 * verify-email.js — handles Email Verification URL token processing.
 */
(function () {
  const spinner = document.getElementById("verify-spinner");
  const alertBox = document.getElementById("verify-alert");
  const actionContainer = document.getElementById("action-container");
  const continueBtn = document.getElementById("continue-btn");
  const resendContainer = document.getElementById("resend-container");
  const resendEmail = document.getElementById("resend-email");
  const resendBtn = document.getElementById("resend-btn");

  const urlParams = new URLSearchParams(window.location.search);
  const token = urlParams.get("token");

  function showError(msg) {
    if (spinner) spinner.classList.add("d-none");
    alertBox.className = "alert alert-danger py-3 mb-4";
    alertBox.textContent = msg;
    alertBox.classList.remove("d-none");
    if (resendContainer) resendContainer.classList.remove("d-none");
  }

  function showSuccess(msg, role) {
    if (spinner) spinner.classList.add("d-none");
    alertBox.className = "alert alert-success py-3 mb-4";
    alertBox.textContent = "🎉 " + msg;
    alertBox.classList.remove("d-none");
    if (actionContainer) actionContainer.classList.remove("d-none");

    if (role && continueBtn) {
      if (Session.isLoggedIn()) {
        continueBtn.href = dashboardUrlForRole(role);
        continueBtn.textContent = "Go to Portal Dashboard \u2192";
      } else {
        continueBtn.href = "login.html?verified=1";
        continueBtn.textContent = "Proceed to Sign In \u2192";
      }
    }
  }

  async function processVerification() {
    if (!token) {
      showError("No verification token found in URL. Please check your verification email or request a new link below.");
      return;
    }

    try {
      const res = await authAPI.verifyEmail(token);
      const userRole = res.data?.role || "candidate";

      // If user is currently logged in, update their local session
      if (Session.isLoggedIn()) {
        const user = Session.getUser() || {};
        user.is_email_verified = true;
        Session.save({
          access_token: Session.getAccessToken(),
          refresh_token: safeStorage.getItem("ar_refresh_token"),
          user: user,
        });
      }

      showSuccess(res.message || "Email verified successfully!", userRole);
    } catch (err) {
      showError(err.message || "Verification failed. Token may be invalid or expired.");
    }
  }

  if (resendBtn) {
    resendBtn.addEventListener("click", async () => {
      const email = resendEmail.value.trim();
      if (!email) {
        alert("Please enter your email address.");
        return;
      }
      resendBtn.disabled = true;
      resendBtn.textContent = "Sending...";
      try {
        const res = await authAPI.resendVerification(email);
        alert(res.message || "Verification link sent!");
        if (res.data && res.data.verification_link) {
          console.log("Dev Verification Link:", res.data.verification_link);
        }
      } catch (err) {
        alert(err.message || "Failed to resend verification email.");
      } finally {
        resendBtn.disabled = false;
        resendBtn.textContent = "Resend Link";
      }
    });
  }

  processVerification();
})();
