/**
 * reset-password.js — handles Password Reset execution.
 */
(function () {
  const form = document.getElementById("reset-form");
  const tokenInput = document.getElementById("reset-token");
  const newPasswordInput = document.getElementById("new-password");
  const confirmPasswordInput = document.getElementById("confirm-password");
  const alertBox = document.getElementById("reset-alert");
  const submitBtn = document.getElementById("reset-submit");
  const submitText = document.getElementById("reset-submit-text");
  const spinner = document.getElementById("reset-spinner");

  // Extract token from query params
  const urlParams = new URLSearchParams(window.location.search);
  const token = urlParams.get("token");

  if (!token) {
    showError("Invalid or missing password reset token. Please request a new reset link.");
    if (submitBtn) submitBtn.disabled = true;
  } else if (tokenInput) {
    tokenInput.value = token;
  }

  function showError(msg) {
    alertBox.className = "alert alert-danger py-2 mb-4";
    alertBox.textContent = msg;
    alertBox.classList.remove("d-none");
  }

  function showSuccess(msg) {
    alertBox.className = "alert alert-success py-2 mb-4";
    alertBox.textContent = msg;
    alertBox.classList.remove("d-none");
  }

  function setLoading(loading) {
    if (loading) {
      submitBtn.disabled = true;
      spinner.classList.remove("d-none");
      submitText.textContent = "Updating Password...";
    } else {
      submitBtn.disabled = false;
      spinner.classList.add("d-none");
      submitText.textContent = "Reset Password \u2192";
    }
  }

  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      alertBox.classList.add("d-none");

      const tokenVal = tokenInput.value || token;
      const newPassword = newPasswordInput.value;
      const confirmPassword = confirmPasswordInput.value;

      if (!tokenVal) {
        showError("Reset token is missing. Please use the link provided in your reset email.");
        return;
      }

      if (!newPassword || newPassword.length < 8) {
        showError("Password must be at least 8 characters long.");
        return;
      }

      if (newPassword !== confirmPassword) {
        showError("New password and confirmation password do not match.");
        return;
      }

      setLoading(true);
      try {
        const res = await authAPI.resetPassword({
          token: tokenVal,
          new_password: newPassword,
        });

        showSuccess(res.message || "Your password has been reset successfully! Redirecting to login...");
        setTimeout(() => {
          window.location.href = "login.html?reset=success";
        }, 1500);
      } catch (err) {
        showError(err.message || "Failed to reset password. Token may be expired.");
        setLoading(false);
      }
    });
  }
})();
