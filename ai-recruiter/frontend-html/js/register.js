/**
 * register.js — handles the register form submit on register.html
 */
(function () {
  if (Session.isLoggedIn()) {
    const user = Session.getUser();
    window.location.href = dashboardUrlForRole(user?.role);
    return;
  }

  const form = document.getElementById("register-form");
  const alertBox = document.getElementById("register-alert");
  const submitBtn = document.getElementById("register-submit");
  const submitText = document.getElementById("register-submit-text");
  const spinner = document.getElementById("register-spinner");

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
    submitText.textContent = isLoading ? "Creating account..." : "Create Account";
  }

  const recruiterContainer = document.getElementById("recruiter-fields-container");
  const candResumeContainer = document.getElementById("candidate-resume-container");
  const roleCandidateRadio = document.getElementById("role-candidate");
  const roleRecruiterRadio = document.getElementById("role-recruiter");
  const authCard = document.querySelector(".auth-card");

  function toggleRoleFields() {
    if (roleRecruiterRadio.checked) {
      recruiterContainer.classList.remove("d-none");
      if (candResumeContainer) candResumeContainer.classList.add("d-none");
      if (authCard) authCard.style.maxWidth = "640px";
    } else {
      recruiterContainer.classList.add("d-none");
      if (candResumeContainer) candResumeContainer.classList.remove("d-none");
      if (authCard) authCard.style.maxWidth = "460px";
    }
  }

  roleCandidateRadio.addEventListener("change", toggleRoleFields);
  roleRecruiterRadio.addEventListener("change", toggleRoleFields);

  // Resume Upload Pre-Extraction for Candidates on Registration Page
  const regResumeBtn = document.getElementById("btn-reg-cand-resume");
  const regResumeInput = document.getElementById("reg-cand-resume-file");
  const regResumeBtnText = document.getElementById("reg-cand-resume-btn-text");
  const regResumeSpinner = document.getElementById("reg-cand-resume-spinner");
  const regResumeStatus = document.getElementById("reg-resume-status");

  let pendingUploadedResume = null;

  if (regResumeBtn && regResumeInput) {
    regResumeBtn.addEventListener("click", () => regResumeInput.click());

    regResumeInput.addEventListener("change", async (e) => {
      const file = e.target.files?.[0];
      if (!file) return;

      pendingUploadedResume = file;
      if (regResumeBtn) regResumeBtn.disabled = true;
      if (regResumeBtnText) regResumeBtnText.textContent = "Analyzing...";
      if (regResumeSpinner) regResumeSpinner.classList.remove("d-none");
      if (regResumeStatus) regResumeStatus.classList.add("d-none");

      try {
        const resAPI = window.resumesAPI || window.resumeAPI;
        if (!resAPI || !resAPI.extractDetails) {
          throw new Error("Resume extraction is temporarily unavailable.");
        }
        const res = await resAPI.extractDetails(file);
        const data = res?.data || {};

        if (data.name) {
          const nameInput = document.getElementById("name");
          if (nameInput) {
            nameInput.value = data.name;
            nameInput.classList.add("border-success", "bg-success-subtle", "bg-opacity-10");
          }
        }
        if (data.email) {
          const emailInput = document.getElementById("email");
          if (emailInput && (!emailInput.value || emailInput.value === "name@company.com")) {
            emailInput.value = data.email;
            emailInput.classList.add("border-success", "bg-success-subtle", "bg-opacity-10");
          }
        }

        // Cache structured data for dashboard auto-fill
        if (typeof safeStorage !== "undefined") {
          safeStorage.setItem("pending_resume_autofill", JSON.stringify(data));
        } else {
          try { localStorage.setItem("pending_resume_autofill", JSON.stringify(data)); } catch (err) {}
        }

        if (regResumeStatus) {
          regResumeStatus.className = "alert alert-success py-1.5 px-2.5 mb-0 mt-2 small";
          regResumeStatus.innerHTML = `<span><strong>🎉 Auto-filled!</strong> Verified details for <strong>${data.name || file.name}</strong>.</span>`;
          regResumeStatus.classList.remove("d-none");
        }
      } catch (err) {
        if (regResumeStatus) {
          regResumeStatus.className = "alert alert-danger py-1.5 px-2.5 mb-0 mt-2 small";
          regResumeStatus.innerHTML = `<span>Could not extract resume: ${err.message || "Invalid file format"}</span>`;
          regResumeStatus.classList.remove("d-none");
        }
      } finally {
        if (regResumeBtn) regResumeBtn.disabled = false;
        if (regResumeBtnText) regResumeBtnText.textContent = "Upload Resume";
        if (regResumeSpinner) regResumeSpinner.classList.add("d-none");
      }
    });
  }

  // Auto-preselect role from URL parameter (e.g. register.html?role=recruiter)
  const urlRole = new URLSearchParams(window.location.search).get("role");
  if (urlRole === "recruiter") {
    roleRecruiterRadio.checked = true;
    toggleRoleFields();
  } else if (urlRole === "candidate") {
    roleCandidateRadio.checked = true;
    toggleRoleFields();
  }


  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    hideError();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm-password").value;
    const role = document.querySelector('input[name="role"]:checked')?.value || "candidate";

    const PUBLIC_EMAIL_DOMAINS = new Set([
      "gmail.com", "yahoo.com", "ymail.com", "hotmail.com", "outlook.com",
      "live.com", "icloud.com", "aol.com", "protonmail.com", "zoho.com",
      "mail.com", "gmx.com", "rediffmail.com"
    ]);

    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,10}$/;
    if (!name || !email || !password) {
      showError("Please fill out all required basic fields.");
      return;
    }
    if (!emailRegex.test(email) || email.includes("..") || email.endsWith(".test") || email.endsWith(".localhost")) {
      showError(`Invalid email address format: '${email}'. Please enter a valid email address (e.g. user@example.com).`);
      return;
    }

    if (role === "recruiter") {
      const domain = email.split("@")[1]?.toLowerCase();
      if (domain && PUBLIC_EMAIL_DOMAINS.has(domain)) {
        showError(`Recruiters must use a company email address (e.g. name@companyname.com). Public email domains like @${domain} are not permitted for Recruiter accounts.`);
        return;
      }
    }

    if (password !== confirmPassword) {
      showError("Passwords do not match.");
      return;
    }
    if (password.length < 8) {
      showError("Password must be at least 8 characters.");
      return;
    }

    const payload = { name, email, password, role };

    if (role === "recruiter") {
      const jobTitle = document.getElementById("job-title").value.trim();
      const phone = document.getElementById("phone").value.trim();
      const companyName = document.getElementById("company-name").value.trim();
      const companyWebsite = document.getElementById("company-website").value.trim();

      payload.job_title = jobTitle || "Talent Acquisition / Recruiter";
      payload.phone = phone || null;
      payload.recruiter_linkedin_url = document.getElementById("recruiter-linkedin-url").value.trim() || null;
      payload.company_name = companyName || `${name}'s Company`;
      payload.company_website = companyWebsite || null;
      payload.company_location = document.getElementById("company-location").value.trim() || null;
      payload.industry = document.getElementById("industry").value.trim() || null;
      payload.company_size = document.getElementById("company-size").value || null;
      payload.company_linkedin_url = document.getElementById("company-linkedin-url").value.trim() || null;
      payload.company_description = document.getElementById("company-description").value.trim() || null;
      payload.company_logo = document.getElementById("company-logo").value.trim() || null;
    }

    setLoading(true);
    try {
      const res = await authAPI.register(payload);
      Session.save(res.data);
      const userRole = res.data?.user?.role || role;

      if (pendingUploadedResume && userRole === "candidate") {
        try {
          const resAPI = window.resumesAPI || window.resumeAPI;
          if (resAPI && resAPI.upload) {
            await resAPI.upload(pendingUploadedResume);
          }
        } catch (uErr) {
          console.warn("Background resume upload note:", uErr);
        }
      }

      alertBox.className = "alert alert-success py-3 mb-4";
      alertBox.textContent = "🎉 Registration successful! Redirecting to your dashboard...";
      alertBox.classList.remove("d-none");

      setTimeout(() => {
        window.location.href = dashboardUrlForRole(userRole);
      }, 1000);
    } catch (err) {
      showError(err.message || "Registration failed. Please try again.");
      setLoading(false);
    }
  });


  let googleClientId = "";

  // Google Register handler
  async function processGoogleAuth(credential) {
    const role = document.querySelector('input[name="role"]:checked')?.value || "candidate";
    hideError();
    setLoading(true);
    try {
      const res = await authAPI.google(credential, role);
      Session.save(res.data);
      const userRole = res.data?.user?.role || res.data?.role || role;
      window.location.href = dashboardUrlForRole(userRole);
    } catch (err) {
      showError(err.message || "Google registration failed.");
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

        const regContainer = document.getElementById("google-register-container");
        if (regContainer) {
          window.google.accounts.id.renderButton(regContainer, {
            theme: "outline",
            size: "large",
            text: "signup_with",
            shape: "rectangular",
            width: Math.min(regContainer.offsetWidth || 340, 360),
          });
          const customBtn = document.getElementById("google-register-btn");
          if (customBtn && regContainer.children.length > 0) {
            customBtn.classList.add("d-none");
          }
        }
        return true;
      };

      if (!setupGIS()) {
        const interval = setInterval(() => {
          if (setupGIS()) clearInterval(interval);
        }, 300);
        setTimeout(() => clearInterval(interval), 5000);
      }
    } catch (e) {
      console.warn("Google Auth config init:", e);
    }
  }
  initGoogleGIS();

  const googleBtn = document.getElementById("google-register-btn");
  if (googleBtn) {
    googleBtn.addEventListener("click", () => {
      if (!googleClientId) {
        showError("Google Client ID is not configured on the server.");
        return;
      }

      if (window.google?.accounts?.oauth2) {
        const tokenClient = window.google.accounts.oauth2.initTokenClient({
          client_id: googleClientId,
          scope: "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile openid",
          callback: (tokenResp) => {
            if (tokenResp && tokenResp.access_token) {
              processGoogleAuth(tokenResp.access_token);
            } else if (tokenResp?.error) {
              showError("Google registration was cancelled or failed: " + (tokenResp.error_description || tokenResp.error));
            }
          },
          error_callback: (err) => {
            console.error("Google OAuth error:", err);
            if (err?.type === "popup_closed") {
              showError("Google Sign-In popup was closed before completing.");
            } else {
              showError(`Google OAuth error: Please verify 'http://localhost:8000' is added to Authorized JavaScript origins in Google Cloud Console.`);
            }
          }
        });
        tokenClient.requestAccessToken();
      } else if (window.google?.accounts?.id) {
        window.google.accounts.id.prompt();
      } else {
        showError("Google Sign-In SDK is loading. Please try again in a moment.");
      }
    });
  }
})();




