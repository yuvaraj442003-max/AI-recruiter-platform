/**
 * login.js — handles the login form submit on login.html
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
    alertBox.textContent = message;
    alertBox.classList.remove("d-none");
  }

  function hideError() {
    alertBox.classList.add("d-none");
  }

  function setLoading(isLoading) {
    submitBtn.disabled = isLoading;
    spinner.classList.toggle("d-none", !isLoading);
    submitText.textContent = isLoading ? "Signing in..." : "Sign In";
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
        alertBox.className = "alert alert-warning py-3 mb-4";
        alertBox.innerHTML = `
          <div><strong>Email Not Verified:</strong> Please check your inbox for the verification link.</div>
          <button type="button" class="btn btn-sm btn-outline-dark mt-2 fw-semibold" id="resend-unverified-btn">
            📩 Resend Verification Email
          </button>
        `;
        alertBox.classList.remove("d-none");
        document.getElementById("resend-unverified-btn")?.addEventListener("click", async () => {
          try {
            const resendRes = await authAPI.resendVerification(email);
            alert(resendRes.message || "Verification link sent!");
          } catch (resendErr) {
            alert(resendErr.message || "Failed to resend verification email.");
          }
        });
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

        const btnDiv = document.getElementById("google-button-div");
        if (btnDiv) {
          window.google.accounts.id.renderButton(btnDiv, {
            theme: "outline",
            size: "large",
            width: "350",
            text: "signin_with",
          });
          const customBtn = document.getElementById("google-signin-btn");
          if (customBtn) customBtn.classList.add("d-none");
        }
      }
    } catch (e) {
      console.warn("Google Auth config init:", e);
    }
  }
  initGoogleGIS();

  const googleBtn = document.getElementById("google-signin-btn");
  if (googleBtn) {
    googleBtn.addEventListener("click", async () => {
      const promptEmail = prompt("Sign in with Google Account:\nEnter your Google Email (or press OK to sign in as yuvarajyuva442003@gmail.com):", "yuvarajyuva442003@gmail.com");
      if (promptEmail && promptEmail.trim()) {
        processGoogleAuth(promptEmail.trim());
      }
    });
  }
})();




