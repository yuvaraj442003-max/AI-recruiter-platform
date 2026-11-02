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

      try {
        const studRes = await api.student.getProfile();
        const sp = studRes?.data;
        if (sp) {
          if (sp.college_name && document.getElementById("cand-college")) document.getElementById("cand-college").value = sp.college_name;
          if (sp.degree && document.getElementById("cand-degree")) document.getElementById("cand-degree").value = sp.degree;
          if (sp.graduation_year && document.getElementById("cand-grad-year")) document.getElementById("cand-grad-year").value = sp.graduation_year;
          if (sp.cgpa && document.getElementById("cand-cgpa")) document.getElementById("cand-cgpa").value = sp.cgpa;

          if (sp.twelfth_school && document.getElementById("cand-12th-school")) document.getElementById("cand-12th-school").value = sp.twelfth_school;
          if (sp.twelfth_board && document.getElementById("cand-12th-board")) document.getElementById("cand-12th-board").value = sp.twelfth_board;
          if (sp.twelfth_year && document.getElementById("cand-12th-year")) document.getElementById("cand-12th-year").value = sp.twelfth_year;
          if (sp.twelfth_percentage && document.getElementById("cand-12th-marks")) document.getElementById("cand-12th-marks").value = sp.twelfth_percentage;

          if (sp.tenth_school && document.getElementById("cand-10th-school")) document.getElementById("cand-10th-school").value = sp.tenth_school;
          if (sp.tenth_board && document.getElementById("cand-10th-board")) document.getElementById("cand-10th-board").value = sp.tenth_board;
          if (sp.tenth_year && document.getElementById("cand-10th-year")) document.getElementById("cand-10th-year").value = sp.tenth_year;
          if (sp.tenth_percentage && document.getElementById("cand-10th-marks")) document.getElementById("cand-10th-marks").value = sp.tenth_percentage;
        }
      } catch (err) {}
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

      // Structured Academic Details
      const college = document.getElementById("cand-college")?.value?.trim() || "";
      const degree = document.getElementById("cand-degree")?.value?.trim() || "";
      const gradYear = document.getElementById("cand-grad-year")?.value?.trim() || "";
      const cgpa = document.getElementById("cand-cgpa")?.value?.trim() || "";

      const twelfthSchool = document.getElementById("cand-12th-school")?.value?.trim() || "";
      const twelfthBoard = document.getElementById("cand-12th-board")?.value?.trim() || "";
      const twelfthYear = document.getElementById("cand-12th-year")?.value?.trim() || "";
      const twelfthMarks = document.getElementById("cand-12th-marks")?.value?.trim() || "";

      const tenthSchool = document.getElementById("cand-10th-school")?.value?.trim() || "";
      const tenthBoard = document.getElementById("cand-10th-board")?.value?.trim() || "";
      const tenthYear = document.getElementById("cand-10th-year")?.value?.trim() || "";
      const tenthMarks = document.getElementById("cand-10th-marks")?.value?.trim() || "";

      if (college) formData.append("college_name", college);
      if (degree) formData.append("degree", degree);
      if (gradYear) formData.append("graduation_year", gradYear);
      if (cgpa) formData.append("cgpa", cgpa);

      if (twelfthSchool) formData.append("twelfth_school", twelfthSchool);
      if (twelfthBoard) formData.append("twelfth_board", twelfthBoard);
      if (twelfthYear) formData.append("twelfth_year", twelfthYear);
      if (twelfthMarks) formData.append("twelfth_percentage", twelfthMarks);

      if (tenthSchool) formData.append("tenth_school", tenthSchool);
      if (tenthBoard) formData.append("tenth_board", tenthBoard);
      if (tenthYear) formData.append("tenth_year", tenthYear);
      if (tenthMarks) formData.append("tenth_percentage", tenthMarks);

      if (fileInput && fileInput.files && fileInput.files[0]) {
        formData.append("file", fileInput.files[0]);
      } else if (uploadedResumeFile) {
        formData.append("file", uploadedResumeFile);
      }

      const apiObj = getResumeAPI();
      if (!apiObj) {
        throw new Error("Resume API client is not loaded. Please refresh the page.");
      }

      const res = await apiObj.completeRegistration(formData);
      if (res && res.data) {
        Session.save(res.data);
      }

      // Save Student Academic Credentials via student API
      if (college || degree || gradYear || cgpa || twelfthSchool || tenthSchool) {
        try {
          await api.student.updateProfile({
            college_name: college || null,
            degree: degree || null,
            graduation_year: gradYear ? Number(gradYear) : null,
            cgpa: cgpa ? Number(cgpa) : null,
            twelfth_school: twelfthSchool || null,
            twelfth_board: twelfthBoard || null,
            twelfth_year: twelfthYear ? Number(twelfthYear) : null,
            twelfth_percentage: twelfthMarks ? Number(twelfthMarks) : null,
            tenth_school: tenthSchool || null,
            tenth_board: tenthBoard || null,
            tenth_year: tenthYear ? Number(tenthYear) : null,
            tenth_percentage: tenthMarks ? Number(tenthMarks) : null,
            target_role: headline,
            is_student: true,
          });
        } catch (e) {
          console.error("Student profile update notice:", e);
        }
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

  // =========================================================================
  // 2-Step Registration Navigation (Personal Details -> Basic Information)
  // Ensures form data is retained without refreshing the page
  // =========================================================================
  let currentRegStep = 1;

  function switchRegistrationStep(step) {
    currentRegStep = step;
    const sec1 = document.getElementById("reg-step-personal");
    const sec2 = document.getElementById("reg-step-basic");
    const tab1 = document.getElementById("reg-tab-personal");
    const tab2 = document.getElementById("reg-tab-basic");
    const badge1 = document.getElementById("reg-badge-1");
    const badge2 = document.getElementById("reg-badge-2");

    if (step === 1) {
      if (sec1) sec1.classList.remove("d-none");
      if (sec2) sec2.classList.add("d-none");
      if (tab1) {
        tab1.className = "btn btn-sm rounded-pill fw-bold flex-fill py-2 btn-primary text-white shadow-sm";
      }
      if (tab2) {
        tab2.className = "btn btn-sm rounded-pill fw-bold flex-fill py-2 btn-outline-secondary border-0 text-muted";
      }
      if (badge1) {
        badge1.className = "badge bg-white text-primary rounded-circle me-1";
      }
      if (badge2) {
        badge2.className = "badge bg-secondary text-white rounded-circle me-1";
      }
    } else {
      if (sec1) sec1.classList.add("d-none");
      if (sec2) sec2.classList.remove("d-none");
      if (tab1) {
        tab1.className = "btn btn-sm rounded-pill fw-bold flex-fill py-2 btn-outline-secondary border-0 text-muted";
      }
      if (tab2) {
        tab2.className = "btn btn-sm rounded-pill fw-bold flex-fill py-2 btn-primary text-white shadow-sm";
      }
      if (badge1) {
        badge1.className = "badge bg-secondary text-white rounded-circle me-1";
      }
      if (badge2) {
        badge2.className = "badge bg-white text-primary rounded-circle me-1";
      }
    }
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  // Next: Basic Information Button (No page refresh, retains all form data)
  const regNextBtn = document.getElementById("btn-reg-next");
  if (regNextBtn) {
    regNextBtn.addEventListener("click", (e) => {
      if (e) {
        e.preventDefault();
        e.stopPropagation();
      }
      hideError();
      const name = document.getElementById("cand-name")?.value?.trim();
      const phone = document.getElementById("cand-phone")?.value?.trim();
      const location = document.getElementById("cand-location")?.value?.trim();

      if (!name || !phone || !location) {
        showError("Please fill in your Full Name, Phone Number, and Location before proceeding.");
        return;
      }

      switchRegistrationStep(2);
    });
  }

  // Back: Personal Details Button (No page refresh, retains all form data)
  const regPrevBtn = document.getElementById("btn-reg-prev");
  if (regPrevBtn) {
    regPrevBtn.addEventListener("click", (e) => {
      if (e) {
        e.preventDefault();
        e.stopPropagation();
      }
      hideError();
      switchRegistrationStep(1);
    });
  }

  // Direct pill tab clicks
  const regTabPersonal = document.getElementById("reg-tab-personal");
  if (regTabPersonal) {
    regTabPersonal.addEventListener("click", (e) => {
      if (e) e.preventDefault();
      switchRegistrationStep(1);
    });
  }
  const regTabBasic = document.getElementById("reg-tab-basic");
  if (regTabBasic) {
    regTabBasic.addEventListener("click", (e) => {
      if (e) e.preventDefault();
      switchRegistrationStep(2);
    });
  }

  const exitBtns = document.querySelectorAll(".exit-reg-btn");
  exitBtns.forEach((btn) => btn.addEventListener("click", handleExitRegistration));

  if (submitBtn) {
    submitBtn.addEventListener("click", handleRegistrationSubmit);
  }
  if (form) {
    form.addEventListener("submit", handleRegistrationSubmit);
  }

  // Resume Auto-Fill for Complete Registration Wizard
  let uploadedResumeFile = null;
  const regTriggerBtn = document.getElementById("btn-reg-trigger-resume-autofill");
  const regFileInput = document.getElementById("reg-autofill-resume-file");
  const candResumeFileInput = document.getElementById("cand-resume-file");
  const regBtnText = document.getElementById("reg-autofill-btn-text");
  const regSpinner = document.getElementById("reg-autofill-spinner");
  const regStatusAlert = document.getElementById("reg-autofill-status-alert");
  const regStatusMsg = document.getElementById("reg-autofill-status-msg");

  async function autofillFromResume(file) {
    if (!file) return;
    uploadedResumeFile = file;

    if (regStatusAlert) regStatusAlert.classList.add("d-none");
    if (regTriggerBtn) regTriggerBtn.disabled = true;
    if (regBtnText) regBtnText.textContent = "Extracting Info...";
    if (regSpinner) regSpinner.classList.remove("d-none");

    try {
      const resAPI = getResumeAPI();
      if (!resAPI || !resAPI.extractDetails) {
        throw new Error("Resume extraction service is unavailable.");
      }
      const res = await resAPI.extractDetails(file);
      const data = res?.data || {};

      let filledCount = 0;
      const setVal = (id, val) => {
        const el = document.getElementById(id);
        if (el && val !== undefined && val !== null && String(val).trim() !== "") {
          el.value = val;
          el.classList.add("border-success", "bg-success-subtle", "bg-opacity-10");
          setTimeout(() => el.classList.remove("border-success", "bg-success-subtle", "bg-opacity-10"), 4000);
          filledCount++;
        }
      };

      // Personal Details (Step 1)
      setVal("cand-name", data.name);
      setVal("cand-phone", data.phone);
      setVal("cand-location", data.location);
      setVal("cand-exp", data.experience_years);
      setVal("cand-linkedin", data.linkedin_url);
      setVal("cand-github", data.github_url);
      setVal("cand-portfolio", data.portfolio_url);

      // Basic Info (Step 2)
      setVal("cand-headline", data.headline || data.current_role);
      setVal("cand-summary", data.summary);
      setVal("cand-skills", data.skills);
      setVal("cand-college", data.college);
      setVal("cand-degree", data.degree);
      setVal("cand-grad-year", data.graduation_year);
      setVal("cand-cgpa", data.cgpa);

      // 12th & 10th Grade Credentials
      setVal("cand-12th-school", data.twelfth_school);
      setVal("cand-12th-board", data.twelfth_board);
      setVal("cand-12th-year", data.twelfth_year);
      setVal("cand-12th-marks", data.twelfth_percentage);

      setVal("cand-10th-school", data.tenth_school);
      setVal("cand-10th-board", data.tenth_board);
      setVal("cand-10th-year", data.tenth_year);
      setVal("cand-10th-marks", data.tenth_percentage);

      if (regStatusAlert && regStatusMsg) {
        regStatusAlert.className = "alert alert-success py-2 px-3 mb-0 mt-3 d-flex align-items-center justify-content-between small shadow-xs";
        regStatusMsg.innerHTML = `<span><strong>🎉 Success!</strong> Auto-filled <strong>${filledCount} fields</strong> from your resume (${file.name}).</span>`;
        regStatusAlert.classList.remove("d-none");
      }
    } catch (err) {
      if (regStatusAlert && regStatusMsg) {
        regStatusAlert.className = "alert alert-danger py-2 px-3 mb-0 mt-3 d-flex align-items-center justify-content-between small shadow-xs";
        regStatusMsg.innerHTML = `<span><strong>Extraction failed:</strong> ${err.message || "Could not read resume file."}</span>`;
        regStatusAlert.classList.remove("d-none");
      }
    } finally {
      if (regTriggerBtn) regTriggerBtn.disabled = false;
      if (regBtnText) regBtnText.textContent = "Upload Resume";
      if (regSpinner) regSpinner.classList.add("d-none");
    }
  }

  if (regTriggerBtn && regFileInput) {
    regTriggerBtn.addEventListener("click", () => {
      regFileInput.click();
    });

    regFileInput.addEventListener("change", async (e) => {
      const file = e.target.files?.[0];
      if (file) {
        await autofillFromResume(file);
      }
      regFileInput.value = "";
    });
  }

  if (candResumeFileInput) {
    candResumeFileInput.addEventListener("change", async (e) => {
      const file = e.target.files?.[0];
      if (file) {
        await autofillFromResume(file);
      }
    });
  }

})();
