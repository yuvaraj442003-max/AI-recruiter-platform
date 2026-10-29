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
      let successMsg = res.message || "Password reset instructions have been generated.";
      if (res.data && res.data.reset_url) {
        alertBox.className = "alert alert-success py-3 mb-4";
        alertBox.innerHTML = `<div>${successMsg}</div><div class="mt-3"><a href="${res.data.reset_url}" class="btn btn-primary btn-sm w-100 fw-bold">Click here to Reset Password Now &rarr;</a></div>`;
        alertBox.classList.remove("d-none");
      } else {
        showSuccess(successMsg);
      }
    } catch (err) {
      showError(err.message || "Failed to process forgot password request.");
    } finally {
      setLoading(false);
    }
  });
})();
