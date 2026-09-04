/**
 * complete-registration.js — handles Candidate Profile Details submission.
 */
(function () {
  if (!Session.isLoggedIn()) {
    window.location.href = "login.html";
    return;
  }

  const user = Session.getUser();
  if (user && user.role !== "candidate") {
    window.location.href = dashboardUrlForRole(user.role);
    return;
  }

  // If candidate profile details are already submitted and complete, skip registration form
  if (user && user.is_profile_complete === true && !window.location.search.includes("edit=1")) {
    window.location.replace("candidate-dashboard.html");
    return;
  }

  const form = document.getElementById("complete-reg-form");
  const alertBox = document.getElementById("complete-alert");
  const submitBtn = document.getElementById("complete-submit-btn");
  const submitText = document.getElementById("complete-submit-text");
  const spinner = document.getElementById("complete-spinner");

  // Pre-fill user name if logged in
  if (user && user.name) {
    const nameInput = document.getElementById("cand-name");
    if (nameInput) nameInput.value = user.name;
  }

  function getResumeAPI() {
    return (
      window.resumesAPI ||
      window.resumeAPI ||
      (typeof resumesAPI !== "undefined" ? resumesAPI : undefined) ||
      (typeof resumeAPI !== "undefined" ? resumeAPI : undefined)
    );
  }

  // Pre-fill existing candidate profile if user is returning to update
  (async function loadExisting() {
    try {
      const apiObj = getResumeAPI();
      if (!apiObj) return;
      const res = await apiObj.me();
      const prof = res.data;
      if (prof) {
        if (prof.phone) document.getElementById("cand-phone").value = prof.phone;
        if (prof.location) document.getElementById("cand-location").value = prof.location;
        if (prof.experience_years) document.getElementById("cand-exp").value = prof.experience_years;
        if (prof.headline) document.getElementById("cand-headline").value = prof.headline;
        if (prof.summary) document.getElementById("cand-summary").value = prof.summary;
        if (prof.skills && prof.skills.length) document.getElementById("cand-skills").value = prof.skills.join(", ");
        if (prof.linkedin_url) document.getElementById("cand-linkedin").value = prof.linkedin_url;
        if (prof.github_url) document.getElementById("cand-github").value = prof.github_url;
        if (prof.portfolio_url) document.getElementById("cand-portfolio").value = prof.portfolio_url;
      }
    } catch (e) {
      // No existing profile yet
    }
  })();

  function handleExitRegistration(e) {
    if (e) {
      if (e.preventDefault) e.preventDefault();
      if (e.stopPropagation) e.stopPropagation();
    }
    if (confirm("Are you sure you want to exit without completing registration? You will be signed out.")) {
      Session.clear();
      window.location.href = "index.html";
    }
  }

  function showError(msg) {
    alertBox.className = "alert alert-danger p-3 mb-4 shadow-sm fw-medium";
    alertBox.innerHTML = `
      <div class="d-flex flex-column flex-sm-row align-items-sm-center justify-content-between gap-3">
        <div style="white-space: pre-line;">${msg}</div>
        <button type="button" class="btn btn-sm btn-outline-danger text-nowrap exit-reg-btn mt-2 mt-sm-0 fw-semibold">
          ✕ Exit &amp; Leave
        </button>
      </div>
    `;
    alertBox.classList.remove("d-none");
    const alertExitBtn = alertBox.querySelector(".exit-reg-btn");
    if (alertExitBtn) alertExitBtn.addEventListener("click", handleExitRegistration);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function hideError() {
    alertBox.classList.add("d-none");
    alertBox.innerHTML = "";
  }

  function setLoading(isLoading) {
    submitBtn.disabled = isLoading;
    spinner.classList.toggle("d-none", !isLoading);
    submitText.textContent = isLoading ? "Submitting Registration Details..." : "Submit Details & Access Candidate Dashboard →";
  }

  async function handleRegistrationSubmit(e) {
    if (e) {
      if (e.preventDefault) e.preventDefault();
      if (e.stopPropagation) e.stopPropagation();
    }
    hideError();

    setLoading(true);

    try {
      const name = document.getElementById("cand-name")?.value?.trim() || "";
      const phone = document.getElementById("cand-phone")?.value?.trim() || "";
      const location = document.getElementById("cand-location")?.value?.trim() || "";
      const exp = document.getElementById("cand-exp")?.value?.trim() || "";
      const headline = document.getElementById("cand-headline")?.value?.trim() || "";
      const summary = document.getElementById("cand-summary")?.value?.trim() || "";
      const skills = document.getElementById("cand-skills")?.value?.trim() || "";
      const fileInput = document.getElementById("cand-resume-file");

      if (!name || !phone || !location || !headline || !summary || !skills) {
        showError("Please fill out all required fields marked with * before proceeding.");
        setLoading(false);
        return;
      }

      const formData = new FormData();
      formData.append("name", name);
      formData.append("phone", phone);
      formData.append("location", location);
      if (exp) formData.append("experience_years", exp);
      formData.append("headline", headline);
      formData.append("current_role", headline);
      formData.append("summary", summary);
      formData.append("skills", skills);

      const linkedin = document.getElementById("cand-linkedin")?.value?.trim() || "";
      const github = document.getElementById("cand-github")?.value?.trim() || "";
      const portfolio = document.getElementById("cand-portfolio")?.value?.trim() || "";

      if (linkedin) formData.append("linkedin_url", linkedin);
      if (github) formData.append("github_url", github);
      if (portfolio) formData.append("portfolio_url", portfolio);

      if (fileInput && fileInput.files && fileInput.files[0]) {
        formData.append("file", fileInput.files[0]);
      }

      const apiObj = getResumeAPI();
      if (!apiObj) {
        throw new Error("Resume API client is not loaded. Please refresh the page.");
      }

      const res = await apiObj.completeRegistration(formData);
      if (res && res.data) {
        Session.save(res.data);
      }

      const updatedUser = Session.getUser() || {};
      updatedUser.is_profile_complete = true;
      Session.save({
        access_token: Session.getAccessToken(),
        refresh_token: safeStorage.getItem("ar_refresh_token"),
        user: updatedUser,
      });

      alertBox.className = "alert alert-success py-2 mb-4";
      alertBox.textContent = "🎉 Registration completed successfully! Redirecting to your Candidate Dashboard...";
      alertBox.classList.remove("d-none");

      setTimeout(() => {
        window.location.href = "candidate-dashboard.html";
      }, 100);
    } catch (err) {
      showError(err.message || "Failed to submit registration details. Please try again.");
      setLoading(false);
    }
  }

  const exitBtns = document.querySelectorAll(".exit-reg-btn");
  exitBtns.forEach((btn) => btn.addEventListener("click", handleExitRegistration));

  if (submitBtn) {
    submitBtn.addEventListener("click", handleRegistrationSubmit);
  }
  if (form) {
    form.addEventListener("submit", handleRegistrationSubmit);
  }
})();
