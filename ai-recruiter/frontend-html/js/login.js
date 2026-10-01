/**
 * login.js — handles login form submit & inline 6-digit OTP email verification on login.html
 */
(function () {
  // Already logged in? Skip straight to the right dashboard.
  if (Session.isLoggedIn()) {
    const user = Session.getUser();
    window.location.href = dashboardUrlForRole(user?.role);
    return;
  }

  const form = document.getElementById("login-form");
  const alertBox = document.getElementById("login-alert");
  const submitBtn = document.getElementById("login-submit");
  const submitText = document.getElementById("login-submit-text");
  const spinner = document.getElementById("login-spinner");

  // OTP Verification View Elements
  const otpContainer = document.getElementById("otp-verification-container");
  const otpInfoAlert = document.getElementById("otp-info-alert");
  const otpForm = document.getElementById("login-otp-form");
  const loginOtpBoxes = Array.from(document.querySelectorAll(".login-otp-box"));
  const verifyOtpSubmit = document.getElementById("verify-otp-submit");
  const verifyOtpBtnText = document.getElementById("verify-otp-btn-text");
  const verifyOtpSpinner = document.getElementById("verify-otp-spinner");
  const resendLoginOtpBtn = document.getElementById("resend-login-otp-btn");
  const resendTimerSpan = document.getElementById("resend-timer-span");
  const changeEmailBtn = document.getElementById("change-email-btn");
  const roleSelectionContainer = document.querySelector("input[name='login-role']")?.closest(".mb-4");

  let currentUnverifiedEmail = "";
  let resendCountdownTimer = null;
  let countdownSeconds = 60;

  function showError(message) {
    if (!message) {
      alertBox.classList.add("d-none");
      return;
    }
    alertBox.className = "alert alert-danger py-2 small fw-semibold";
    alertBox.textContent = message;
    alertBox.classList.remove("d-none");
  }

  function hideError() {
    alertBox.classList.add("d-none");
  }

  function setLoading(isLoading) {
    submitBtn.disabled = isLoading;
    spinner.classList.toggle("d-none", !isLoading);
    submitText.textContent = isLoading ? "Signing in..." : "Sign In \u2192";
  }

  function startResendTimer() {
    if (resendCountdownTimer) clearInterval(resendCountdownTimer);
    countdownSeconds = 60;
    if (resendLoginOtpBtn) resendLoginOtpBtn.disabled = true;
    if (resendTimerSpan) resendTimerSpan.textContent = `(${countdownSeconds}s)`;

    resendCountdownTimer = setInterval(() => {
      countdownSeconds--;
      if (countdownSeconds <= 0) {
        clearInterval(resendCountdownTimer);
        resendCountdownTimer = null;
        if (resendLoginOtpBtn) resendLoginOtpBtn.disabled = false;
        if (resendTimerSpan) resendTimerSpan.textContent = "";
      } else {
        if (resendTimerSpan) resendTimerSpan.textContent = `(${countdownSeconds}s)`;
      }
    }, 1000);
  }

  function showOTPSection(email) {
    currentUnverifiedEmail = email;
    hideError();
    form.classList.add("d-none");
    if (roleSelectionContainer) roleSelectionContainer.classList.add("d-none");

    if (otpInfoAlert) {
      otpInfoAlert.innerHTML = `📩 <strong>Email Not Verified:</strong> A 6-digit OTP code has been sent to <strong>${email}</strong>.`;
    }

    if (otpContainer) otpContainer.classList.remove("d-none");

    loginOtpBoxes.forEach((b) => (b.value = ""));
    if (loginOtpBoxes[0]) loginOtpBoxes[0].focus();

    startResendTimer();
  }

  function hideOTPSection() {
    if (resendCountdownTimer) clearInterval(resendCountdownTimer);
    if (otpContainer) otpContainer.classList.add("d-none");
    form.classList.remove("d-none");
    if (roleSelectionContainer) roleSelectionContainer.classList.remove("d-none");
    hideError();
  }

  if (changeEmailBtn) {
    changeEmailBtn.addEventListener("click", () => {
      hideOTPSection();
      const emailField = document.getElementById("email");
      if (emailField) {
        emailField.focus();
        emailField.select();
      }
    });
  }

  // OTP Box digit navigation
  loginOtpBoxes.forEach((box, idx) => {
    box.addEventListener("input", (e) => {
      const val = e.target.value.replace(/[^0-9]/g, "");
      e.target.value = val;
      if (val && idx < loginOtpBoxes.length - 1) {
        loginOtpBoxes[idx + 1].focus();
      }
    });

    box.addEventListener("keydown", (e) => {
      if (e.key === "Backspace" && !box.value && idx > 0) {
        loginOtpBoxes[idx - 1].focus();
      }
    });

    box.addEventListener("paste", (e) => {
      e.preventDefault();
      const pasteData = (e.clipboardData || window.clipboardData).getData("text").replace(/[^0-9]/g, "");
      if (pasteData) {
        for (let i = 0; i < loginOtpBoxes.length; i++) {
          loginOtpBoxes[i].value = pasteData[i] || "";
        }
        if (pasteData.length >= 6) {
          loginOtpBoxes[5].focus();
        } else {
          loginOtpBoxes[Math.min(pasteData.length, 5)].focus();
        }
      }
    });
  });

  // Resend OTP handler with countdown timer reset
  if (resendLoginOtpBtn) {
    resendLoginOtpBtn.addEventListener("click", async () => {
      if (!currentUnverifiedEmail) return;
      resendLoginOtpBtn.disabled = true;
      if (resendTimerSpan) resendTimerSpan.textContent = "(Sending...)";

      try {
        const res = await authAPI.resendOTP(currentUnverifiedEmail);
        hideError();
        if (otpInfoAlert) {
          otpInfoAlert.innerHTML = `📩 <strong>New OTP Sent:</strong> A fresh 6-digit OTP code has been sent to <strong>${currentUnverifiedEmail}</strong>.`;
        }
        loginOtpBoxes.forEach((b) => (b.value = ""));
        if (loginOtpBoxes[0]) loginOtpBoxes[0].focus();
        startResendTimer();
      } catch (err) {
        showError(err.message || "Failed to resend OTP.");
        resendLoginOtpBtn.disabled = false;
        if (resendTimerSpan) resendTimerSpan.textContent = "";
      }
    });
  }

  // OTP Submit handler
  if (otpForm) {
    otpForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      hideError();

      const otp = loginOtpBoxes.map((b) => b.value.trim()).join("");
      if (otp.length < 6) {
        showError("Please enter the complete 6-digit verification code.");
        return;
      }

      verifyOtpSubmit.disabled = true;
      if (verifyOtpSpinner) verifyOtpSpinner.classList.remove("d-none");
      if (verifyOtpBtnText) verifyOtpBtnText.textContent = "Verifying...";

      try {
        const res = await authAPI.verifyOTP(currentUnverifiedEmail, otp);
        Session.save(res.data);
        const userRole = res.data?.user?.role || res.data?.role || "candidate";

        alertBox.className = "alert alert-success py-2 mb-3 small fw-semibold";
        alertBox.textContent = "🎉 Email verified successfully! Redirecting to your dashboard...";
        alertBox.classList.remove("d-none");

        setTimeout(() => {
          window.location.href = dashboardUrlForRole(userRole);
        }, 1200);
      } catch (err) {
        showError(err.message || "Invalid OTP. Please try again.");
      } finally {
        verifyOtpSubmit.disabled = false;
        if (verifyOtpSpinner) verifyOtpSpinner.classList.add("d-none");
        if (verifyOtpBtnText) verifyOtpBtnText.textContent = "Verify & Sign In \u2192";
      }
    });
  }

  // Auto-preselect login role from URL query param (e.g. login.html?role=recruiter)
  const urlRole = new URLSearchParams(window.location.search).get("role");
  if (urlRole === "recruiter") {
    const rRadio = document.getElementById("login-role-recruiter");
    if (rRadio) rRadio.checked = true;
  } else if (urlRole === "candidate") {
    const cRadio = document.getElementById("login-role-candidate");
    if (cRadio) cRadio.checked = true;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    hideError();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const expectedRole = document.querySelector('input[name="login-role"]:checked')?.value || "candidate";

    if (!email || !password) {
      showError("Please enter both your email address and password.");
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      showError("Please enter a valid email address (e.g. user@example.com).");
      return;
    }

    const PUBLIC_EMAIL_DOMAINS = new Set([
      "gmail.com", "yahoo.com", "ymail.com", "hotmail.com", "outlook.com",
      "live.com", "icloud.com", "aol.com", "protonmail.com", "zoho.com",
      "mail.com", "gmx.com", "rediffmail.com"
    ]);

    if (expectedRole === "recruiter") {
      const domain = email.split("@")[1]?.toLowerCase();
      if (domain && PUBLIC_EMAIL_DOMAINS.has(domain)) {
        showError(`Access Denied: Recruiters must use a company email address (e.g. name@companyname.com). Public email domains like @${domain} are not permitted for Recruiter accounts.`);
        return;
      }
    }

    setLoading(true);
    try {
      const res = await authAPI.login({ email, password, expected_role: expectedRole });
      Session.save(res.data);
      const role = res.data.user.role;
      window.location.href = dashboardUrlForRole(role);
    } catch (err) {
      if (err.errorCode === "EMAIL_NOT_VERIFIED" || (err.message && err.message.toLowerCase().includes("verify your email"))) {
        window.location.href = `verify-email.html?email=${encodeURIComponent(email)}`;
      } else {
        showError(err.message);
      }
    } finally {
      setLoading(false);
    }
  });

  // Quick Demo Login Buttons
  const demoCandBtn = document.getElementById("demo-candidate-btn");
  if (demoCandBtn) {
    demoCandBtn.addEventListener("click", () => {
      document.getElementById("email").value = "alice@example.com";
      document.getElementById("password").value = "Password123!";
      const cRadio = document.getElementById("login-role-candidate");
      if (cRadio) cRadio.checked = true;
      form.dispatchEvent(new Event("submit"));
    });
  }

  const demoRecBtn = document.getElementById("demo-recruiter-btn");
  if (demoRecBtn) {
    demoRecBtn.addEventListener("click", () => {
      document.getElementById("email").value = "recruiter1@techcorp.com";
      document.getElementById("password").value = "Password123!";
      const rRadio = document.getElementById("login-role-recruiter");
      if (rRadio) rRadio.checked = true;
      form.dispatchEvent(new Event("submit"));
    });
  }

  // Google Sign-In handler
  async function processGoogleAuth(credential) {
    hideError();
    setLoading(true);
    const expectedRole = document.querySelector('input[name="login-role"]:checked')?.value || "candidate";
    try {
      const res = await authAPI.google(credential, expectedRole);
      Session.save(res.data);
      const role = res.data.user.role;
      window.location.href = dashboardUrlForRole(role);
    } catch (err) {
      showError(err.message || "Google Sign-In failed.");
    } finally {
      setLoading(false);
    }
  }

  window.handleGoogleCredentialResponse = function (response) {
    if (response && response.credential) {
      processGoogleAuth(response.credential);
    }
  };

  // Fetch GOOGLE_CLIENT_ID from backend .env config and initialize GIS
  async function initGoogleGIS() {
    try {
      const configRes = await authAPI.getConfig();
      const clientId = configRes?.data?.google_client_id;
      if (clientId && window.google?.accounts?.id) {
        window.google.accounts.id.initialize({
          client_id: clientId,
          callback: window.handleGoogleCredentialResponse,
        });
      }
    } catch (e) {
      console.warn("Google Auth config init:", e);
    }
  }
  initGoogleGIS();

  const googleBtn = document.getElementById("google-signin-btn");
  if (googleBtn) {
    googleBtn.addEventListener("click", async () => {
      if (window.google?.accounts?.id) {
        window.google.accounts.id.prompt((notification) => {
          if (notification.isNotDisplayed() || notification.isSkippedMoment()) {
            const promptEmail = prompt("Sign in with Google Account:\nEnter your Google Email (or press OK to sign in as yuvarajyuva442003@gmail.com):", "yuvarajyuva442003@gmail.com");
            if (promptEmail && promptEmail.trim()) {
              processGoogleAuth(promptEmail.trim());
            }
          }
        });
      } else {
        const promptEmail = prompt("Sign in with Google Account:\nEnter your Google Email (or press OK to sign in as yuvarajyuva442003@gmail.com):", "yuvarajyuva442003@gmail.com");
        if (promptEmail && promptEmail.trim()) {
          processGoogleAuth(promptEmail.trim());
        }
      }
    });
  }
})();
