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
  const roleCandidateRadio = document.getElementById("role-candidate");
  const roleRecruiterRadio = document.getElementById("role-recruiter");
  const authCard = document.querySelector(".auth-card");

  function toggleRoleFields() {
    if (roleRecruiterRadio.checked) {
      recruiterContainer.classList.remove("d-none");
      if (authCard) authCard.style.maxWidth = "640px";
    } else {
      recruiterContainer.classList.add("d-none");
      if (authCard) authCard.style.maxWidth = "460px";
    }
  }

  roleCandidateRadio.addEventListener("change", toggleRoleFields);
  roleRecruiterRadio.addEventListener("change", toggleRoleFields);

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

    if (!name || !email || !password) {
      showError("Please fill out all required basic fields.");
      return;
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
      window.location.href = dashboardUrlForRole(role);
    } catch (err) {
      showError(err.message);
    } finally {
      setLoading(false);
    }
  });


  // Google Register handler
  async function processGoogleAuth(credential) {
    const role = document.querySelector('input[name="role"]:checked')?.value || "candidate";
    hideError();
    setLoading(true);
    try {
      const res = await authAPI.google(credential, role);
      Session.save(res.data);
      window.location.href = dashboardUrlForRole(res.data.user.role);
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
            text: "signup_with",
          });
          const customBtn = document.getElementById("google-register-btn");
          if (customBtn) customBtn.classList.add("d-none");
        }
      }
    } catch (e) {
      console.warn("Google Auth config init:", e);
    }
  }
  initGoogleGIS();

  const googleBtn = document.getElementById("google-register-btn");
  if (googleBtn) {
    googleBtn.addEventListener("click", async () => {
      const promptEmail = prompt("Continue with Google Account:\nEnter your Google Email (or press OK to sign in as yuvarajyuva442003@gmail.com):", "yuvarajyuva442003@gmail.com");
      if (promptEmail && promptEmail.trim()) {
        processGoogleAuth(promptEmail.trim());
      }
    });
  }
})();




