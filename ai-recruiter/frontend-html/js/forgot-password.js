/**
 * forgot-password.js — handles Forgot Password requests.
 */
(function () {
  const form = document.getElementById("forgot-form");
  const emailInput = document.getElementById("forgot-email");
  const alertBox = document.getElementById("forgot-alert");
  const submitBtn = document.getElementById("forgot-submit");
  const submitText = document.getElementById("forgot-submit-text");
  const spinner = document.getElementById("forgot-spinner");
  const resetLinkContainer = document.getElementById("reset-link-container");
  const devResetLink = document.getElementById("dev-reset-link");

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
      submitText.textContent = "Processing...";
    } else {
      submitBtn.disabled = false;
      spinner.classList.add("d-none");
      submitText.textContent = "Send Reset Link \u2192";
    }
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    alertBox.classList.add("d-none");

    const email = emailInput.value.trim();
    if (!email) {
      showError("Please enter your email address.");
      return;
    }

    setLoading(true);
    try {
      const res = await authAPI.forgotPassword(email);
      showSuccess(res.message || "Password reset instructions have been sent to your email address.");
    } catch (err) {
      showError(err.message || "Failed to process forgot password request.");
    } finally {
      setLoading(false);
    }
  });
})();
