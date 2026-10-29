/**
 * login.js — handles direct login form submit (Candidate & Recruiter) on login.html
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

  function showError(message) {
    if (!message) {
      alertBox.classList.add("d-none");
      return;
    }
    alertBox.className = "alert alert-danger py-2 small fw-semibold";
    if (message.includes("No account found") || message.includes("register a new account")) {
      const selectedRole = document.querySelector('input[name="login-role"]:checked')?.value || "recruiter";
      alertBox.innerHTML = `${message} <a href="register.html?role=${selectedRole}" class="alert-link text-decoration-underline ms-1">Register here &rarr;</a>`;
    } else if (message.includes("Incorrect password")) {
      alertBox.innerHTML = `${message} <a href="forgot-password.html" class="alert-link text-decoration-underline ms-1">Reset password &rarr;</a>`;
    } else {
      alertBox.textContent = message;
    }
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
      const role = res.data?.user?.role || expectedRole;
      window.location.href = dashboardUrlForRole(role);
    } catch (err) {
      showError(err.message || "Invalid email or password.");
    } finally {
      setLoading(false);
    }
  });

  let googleClientId = "";

  // Google Sign-In handler
  async function processGoogleAuth(credential) {
    hideError();
    setLoading(true);
    const expectedRole = document.querySelector('input[name="login-role"]:checked')?.value || "candidate";
    try {
      const res = await authAPI.google(credential, expectedRole);
      Session.save(res.data);
      const role = res.data?.user?.role || res.data?.role || expectedRole;
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
      googleClientId = configRes?.data?.google_client_id;
      if (!googleClientId) return;

      const setupGIS = () => {
        if (!window.google?.accounts?.id) return false;

        window.google.accounts.id.initialize({
          client_id: googleClientId,
          callback: window.handleGoogleCredentialResponse,
          auto_select: false,
          cancel_on_tap_outside: true,
        });

        const btnContainer = document.getElementById("google-signin-container");
        const customBtn = document.getElementById("google-signin-btn");

        if (btnContainer) {
          try {
            window.google.accounts.id.renderButton(btnContainer, {
              type: "standard",
              shape: "rectangular",
              theme: "outline",
              text: "signin_with",
              size: "large",
              logo_alignment: "left",
              width: 380,
            });
            if (customBtn) customBtn.classList.add("d-none");
          } catch (renderErr) {
            console.warn("Standard Google button render failed, falling back to custom button:", renderErr);
            if (customBtn) customBtn.classList.remove("d-none");
          }
        }
        return true;
      };

      if (!setupGIS()) {
        const checkInterval = setInterval(() => {
          if (setupGIS()) clearInterval(checkInterval);
        }, 100);
        setTimeout(() => clearInterval(checkInterval), 4000);
      }
    } catch (err) {
      console.warn("Could not load Google auth config:", err);
    }
  }

  const customGoogleBtn = document.getElementById("google-signin-btn");
  if (customGoogleBtn) {
    customGoogleBtn.addEventListener("click", () => {
      if (window.google?.accounts?.id && googleClientId) {
        window.google.accounts.id.prompt((notification) => {
          if (notification.isNotDisplayed() || notification.isSkippedMoment()) {
            console.info("One Tap dismissed/skipped:", notification.getNotDisplayedReason?.() || notification.getSkippedReason?.());
          }
        });
      } else {
        showError("Google Sign-In is currently unavailable. Please sign in with your email and password.");
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initGoogleGIS);
  } else {
    initGoogleGIS();
  }
})();
