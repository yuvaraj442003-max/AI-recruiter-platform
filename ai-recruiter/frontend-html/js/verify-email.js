/**
 * verify-email.js — 6-digit OTP verification script.
 */
(function () {
  const alertBox = document.getElementById("verify-alert");
  const emailInput = document.getElementById("email-input");
  const otpBoxes = Array.from(document.querySelectorAll(".otp-box"));
  const verifyBtn = document.getElementById("verify-btn");
  const otpForm = document.getElementById("otp-form");
  const resendBtn = document.getElementById("resend-btn");

  // Read email from URL query params or active user session
  const urlParams = new URLSearchParams(window.location.search);
  const emailParam = urlParams.get("email");
  const sessionUser = typeof Session !== "undefined" && Session.getUser ? Session.getUser() : null;

  if (emailInput) {
    if (emailParam) {
      emailInput.value = emailParam.trim();
    } else if (sessionUser && sessionUser.email) {
      emailInput.value = sessionUser.email.trim();
    }
  }

  function showError(msg) {
    alertBox.className = "alert alert-danger py-2 mb-4 small fw-semibold";
    alertBox.textContent = msg;
    alertBox.classList.remove("d-none");
  }

  function showSuccess(msg, role) {
    alertBox.className = "alert alert-success py-2 mb-4 small fw-semibold";
    alertBox.textContent = "🎉 " + msg;
    alertBox.classList.remove("d-none");

    const targetUrl = typeof dashboardUrlForRole === "function" ? dashboardUrlForRole(role) : "candidate-portal.html";

    setTimeout(() => {
      window.location.href = targetUrl;
    }, 1500);
  }

  // Handle OTP Box focus & input behavior
  otpBoxes.forEach((box, idx) => {
    box.addEventListener("input", (e) => {
      const val = e.target.value.replace(/[^0-9]/g, "");
      e.target.value = val;
      if (val && idx < otpBoxes.length - 1) {
        otpBoxes[idx + 1].focus();
      }
    });

    box.addEventListener("keydown", (e) => {
      if (e.key === "Backspace" && !box.value && idx > 0) {
        otpBoxes[idx - 1].focus();
      }
    });

    box.addEventListener("paste", (e) => {
      e.preventDefault();
      const pasteData = (e.clipboardData || window.clipboardData).getData("text").replace(/[^0-9]/g, "");
      if (pasteData) {
        for (let i = 0; i < otpBoxes.length; i++) {
          otpBoxes[i].value = pasteData[i] || "";
        }
        if (pasteData.length >= 6) {
          otpBoxes[5].focus();
        } else {
          otpBoxes[Math.min(pasteData.length, 5)].focus();
        }
      }
    });
  });

  function getEnteredOTP() {
    return otpBoxes.map((b) => b.value.trim()).join("");
  }

  async function handleVerification() {
    const email = emailInput.value.trim();
    const otp = getEnteredOTP();

    if (!email) {
      showError("Please enter your registered email address.");
      emailInput.focus();
      return;
    }

    if (otp.length < 6) {
      showError("Please enter the complete 6-digit verification code sent to your email.");
      return;
    }

    verifyBtn.disabled = true;
    verifyBtn.textContent = "Verifying Code...";

    try {
      const res = await authAPI.verifyOTP(email, otp);
      const userRole = res.data?.user?.role || res.data?.role || "candidate";

      // Save tokens & user data into session
      if (res.data && res.data.access_token) {
        Session.save(res.data);
      } else if (Session.isLoggedIn()) {
        const user = Session.getUser() || {};
        user.is_email_verified = true;
        Session.save({
          access_token: Session.getAccessToken(),
          refresh_token: safeStorage.getItem("ar_refresh_token"),
          user: user,
        });
      }

      showSuccess(res.message || "Email verified successfully! Redirecting to dashboard...", userRole);
    } catch (err) {
      showError(err.message || "Invalid or expired verification code. Please try again.");
    } finally {
      verifyBtn.disabled = false;
      verifyBtn.textContent = "Verify OTP Code \u2192";
    }
  }

  if (otpForm) {
    otpForm.addEventListener("submit", (e) => {
      e.preventDefault();
      handleVerification();
    });
  }

  if (resendBtn) {
    resendBtn.addEventListener("click", async () => {
      const email = emailInput.value.trim();
      if (!email) {
        showError("Please enter your email address to resend OTP.");
        emailInput.focus();
        return;
      }

      resendBtn.disabled = true;
      resendBtn.textContent = "Sending Code...";

      try {
        const res = await authAPI.resendOTP(email);
        alertBox.className = "alert alert-info py-2 mb-4 small fw-semibold";
        alertBox.textContent = "ℹ️ " + (res.message || "A new 6-digit code has been sent to your email.");
        alertBox.classList.remove("d-none");
        otpBoxes.forEach((b) => (b.value = ""));
        otpBoxes[0].focus();
      } catch (err) {
        showError(err.message || "Failed to resend verification code.");
      } finally {
        resendBtn.disabled = false;
        resendBtn.textContent = "Resend 6-Digit OTP Code";
      }
    });
  }
})();
