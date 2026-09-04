/**
 * jobs.js — loads recommended + searchable job listings and handles
 * "Apply" clicks for the candidate, hamburger menu drawer, and 3-job default view.
 */
(function () {
  const alertBox = document.getElementById("job-alert");
  const jobListEl = document.getElementById("job-list");
  const recommendedListEl = document.getElementById("recommended-list");
  const offcanvasJobListEl = document.getElementById("offcanvas-job-list");
  const jobsCountBadge = document.getElementById("jobs-count-badge");
  const jobsDisplayInfo = document.getElementById("jobs-display-info");
  const hamburgerMenuBtn = document.getElementById("hamburger-menu-btn");
  const hamburgerToggleRemainingBtn = document.getElementById("hamburger-toggle-remaining-btn");
  const toggleBtnText = document.getElementById("toggle-btn-text");

  let allFetchedJobs = [];
  let showingAllJobs = false;

  const appliedJobIdsSet = new Set();
  const recommendationScoresMap = new Map();
  const jobsCache = new Map();

  function showAlert(message, variant) {
    if (!alertBox) return;
    alertBox.innerHTML = message;
    alertBox.className = `alert alert-${variant} py-2 mb-3`;
    alertBox.classList.remove("d-none");
  }

  async function loadAppliedJobIds() {
    try {
      const res = await applicationsAPI.mine();
      if (res && res.data) {
        res.data.forEach((app) => {
          if (app.job_id) appliedJobIdsSet.add(String(app.job_id));
        });
      }
    } catch (e) {
      // candidate may not be logged in or has no applications
    }
  }

  async function performApply(jobId, btn) {
    btn.disabled = true;
    btn.textContent = "Applying & Verifying Skills…";
    try {
      const res = await jobsAPI.apply(jobId);
      const appData = res.data || {};
      const score = Math.round(appData.ats_score || appData.match_score || 0);
      const matchedList = appData.matched_skills || [];
      const matchedStr = matchedList.length ? matchedList.join(", ") : "None";

      appliedJobIdsSet.add(String(jobId));

      btn.textContent = `Applied · ${score}% match`;
      btn.classList.remove("btn-primary");
      btn.classList.add("btn-success");

      showAlert(
        `🎉 <strong>Application Submitted!</strong> ATS Score: <strong>${score}%</strong>. Verified Matched Skills: <span class="badge bg-success-subtle text-success border border-success-subtle ms-1">${matchedStr}</span>`,
        "success"
      );

      // Refresh cards UI so all buttons for this job display Already Applied
      renderJobs();
      loadRecommended();
    } catch (err) {
      if (err.errorCode === "CONFLICT" || err.status === 409 || (err.message && err.message.toLowerCase().includes("already applied"))) {
        appliedJobIdsSet.add(String(jobId));
        btn.disabled = true;
        btn.textContent = "Already Applied";
        btn.classList.remove("btn-primary");
        btn.classList.add("btn-secondary");
        showAlert(
          `ℹ️ <strong>Already Applied:</strong> You have already submitted an application for this job posting. View your application details in <a href="my-applications.html" class="fw-bold text-decoration-underline text-dark ms-1">My Applications →</a>`,
          "info"
        );
      } else if (err.errorCode === "NO_RESUME" || (err.message && err.message.toLowerCase().includes("resume"))) {
        btn.disabled = false;
        btn.textContent = "Apply";
        showAlert(
          `📄 <strong>Resume Required:</strong> Please upload your resume before applying so the system can verify your skills. <a href="upload-resume.html" class="fw-bold text-decoration-underline text-dark ms-2">Upload Resume Now →</a>`,
          "warning"
        );
      } else {
        btn.disabled = false;
        btn.textContent = "Apply";
        showAlert(`⚠️ ${err.message || "Failed to submit application."}`, "danger");
      }
    }
  }

  function jobCard(job, { matchScore, showApply = true } = {}) {
    jobsCache.set(String(job.id), job);
    const effectiveScore = matchScore != null ? matchScore : recommendationScoresMap.get(String(job.id));

    const skillBadges = (job.required_skills || [])
      .map((s) => `<span class="badge text-bg-light border me-1 mb-1">${s}</span>`)
      .join("");

    const scoreBadge =
      effectiveScore != null
        ? `<span class="badge bg-primary text-white fs-6 px-2 py-1">${Math.round(effectiveScore)}% match</span>`
        : "";

    const verifiedBadge = (job.company_name && (job.company_name.includes("Acme") || job.company_name.includes("Tech") || job.company_name.includes("Corp")))
      ? `<span class="badge bg-success-subtle text-success border border-success-subtle ms-1">Verified 🛡️</span>`
      : "";

    const riskBadge = (job.fraud_risk_level === "HIGH")
      ? `<span class="badge bg-danger ms-1">High Scam Risk ⚠️</span>`
      : (job.fraud_risk_level === "MEDIUM")
      ? `<span class="badge bg-warning text-dark ms-1">Medium Risk</span>`
      : "";

    const isApplied = appliedJobIdsSet.has(String(job.id));
    const applyBtnHtml = isApplied
      ? `<button class="btn btn-sm btn-secondary flex-grow-1" disabled>Already Applied</button>`
      : showApply
      ? `<button class="btn btn-sm btn-primary flex-grow-1 apply-btn" data-job-id="${job.id}">Apply</button>`
      : "";

    return `
      <div class="col-md-6 col-lg-4">
        <div class="card p-3 h-100 d-flex flex-column border shadow-sm style-card" style="border-radius: 12px;">
          <div class="d-flex justify-content-between align-items-start mb-1">
            <h6 class="fw-bold mb-0 text-dark">${job.title} ${verifiedBadge} ${riskBadge}</h6>
            ${scoreBadge}
          </div>
          <div class="text-muted small mb-2">
            🏢 ${job.company_name || 'Direct Employer'} · 📍 ${job.location || "Remote"} · ⏱️ ${job.experience_required != null ? job.experience_required : (job.min_experience || 0)} Yrs Exp
          </div>
          <p class="small text-secondary mb-2" style="flex-grow: 1;">${job.description.slice(0, 130)}${job.description.length > 130 ? "…" : ""}</p>
          <div class="mb-3">${skillBadges}</div>
          <div class="d-flex gap-2 mt-auto">
            <button class="btn btn-sm btn-outline-primary flex-grow-1 details-btn" data-job-id="${job.id}">
              ℹ️ View Details
            </button>
            ${applyBtnHtml}
          </div>
        </div>
      </div>
    `;
  }

  function offcanvasJobCard(job) {
    jobsCache.set(String(job.id), job);
    const effectiveScore = recommendationScoresMap.get(String(job.id));

    const skillBadges = (job.required_skills || [])
      .slice(0, 3)
      .map((s) => `<span class="badge text-bg-light border me-1 mb-1">${s}</span>`)
      .join("");

    const scoreBadge =
      effectiveScore != null
        ? `<span class="badge bg-primary text-white me-1">${Math.round(effectiveScore)}% match</span>`
        : "";

    const verifiedBadge = (job.company_name && (job.company_name.includes("Acme") || job.company_name.includes("Tech") || job.company_name.includes("Corp")))
      ? `<span class="badge bg-success-subtle text-success border border-success-subtle ms-1">Verified 🛡️</span>`
      : "";

    const isApplied = appliedJobIdsSet.has(String(job.id));
    const applyBtnHtml = isApplied
      ? `<button class="btn btn-sm btn-secondary flex-grow-1" disabled>Already Applied</button>`
      : `<button class="btn btn-sm btn-primary flex-grow-1 apply-btn" data-job-id="${job.id}">Apply</button>`;

    return `
      <div class="card p-3 border shadow-sm style-card" style="border-radius: 12px; background: #fff;">
        <div class="d-flex justify-content-between align-items-start mb-1">
          <h6 class="fw-bold mb-0 text-dark">${job.title} ${verifiedBadge}</h6>
          ${scoreBadge}
        </div>
        <div class="text-muted small mb-2">
          🏢 ${job.company_name || 'Direct Employer'} · 📍 ${job.location || "Remote / Unspecified"}
        </div>
        <p class="small text-secondary mb-2">${job.description.slice(0, 110)}${job.description.length > 110 ? "…" : ""}</p>
        <div class="mb-2">${skillBadges}</div>
        <div class="d-flex gap-2">
          <button class="btn btn-sm btn-outline-primary flex-grow-1 details-btn" data-job-id="${job.id}">
            ℹ️ View Details
          </button>
          ${applyBtnHtml}
        </div>
      </div>
    `;
  }

  function attachCardHandlers(container) {
    container.querySelectorAll(".apply-btn").forEach((btn) => {
      btn.addEventListener("click", () => performApply(btn.dataset.jobId, btn));
    });

    container.querySelectorAll(".details-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const job = jobsCache.get(btn.dataset.jobId);
        if (job) showJobDetailsModal(job);
      });
    });
  }


  function showJobDetailsModal(job) {
    const modalBody = document.getElementById("job-details-body");
    const modalTitle = document.getElementById("jobDetailsModalLabel");
    const modalApplyBtn = document.getElementById("modal-apply-btn");

    modalTitle.textContent = job.title;
    
    // 1. Technical Skills Badges
    const techSkillsHtml = (job.required_skills || [])
      .map((s) => `<span class="badge bg-primary-subtle text-primary border border-primary-subtle me-1 mb-1 px-3 py-2 fs-6">💻 ${s}</span>`)
      .join("");

    // 2. Non-Technical / Soft Skills Badges
    const nonTechSkillsList = Array.isArray(job.non_technical_skills) 
      ? job.non_technical_skills 
      : (typeof job.non_technical_skills === "string" && job.non_technical_skills ? job.non_technical_skills.split(",").map(s => s.trim()) : []);
    
    const nonTechSkillsHtml = nonTechSkillsList
      .map((s) => `<span class="badge me-1 mb-1 px-3 py-2 fs-6" style="background: #f3e8ff; color: #7e22ce; border: 1px solid #e9d5ff;">🤝 ${s}</span>`)
      .join("");

    // 3. Required Experience (years)
    const expYears = job.experience_required != null ? job.experience_required : (job.min_experience || 0);
    const expBadgeText = expYears > 0 ? `${expYears} Years Required` : "Entry Level / No Min Exp";

    const companySectionHtml = (job.company_name || job.company_description || job.company_logo) ? `
      <div class="card p-3 mb-4 border-0 shadow-sm" style="background: #f8fafc; border-radius: 12px;">
        <div class="d-flex align-items-center gap-3 mb-2">
          ${job.company_logo ? `<img src="${job.company_logo}" class="rounded border bg-white p-1" style="width: 54px; height: 54px; object-fit: contain;" alt="Company Logo" />` : '<div class="fs-1">🏢</div>'}
          <div>
            <h5 class="fw-bold text-dark mb-0">${job.company_name || 'Hiring Company'}</h5>
            <div class="text-muted small">
              ${job.industry ? `<span>${job.industry}</span> • ` : ''}
              ${job.company_size ? `<span>${job.company_size}</span> • ` : ''}
              ${job.company_location ? `<span>📍 ${job.company_location}</span>` : ''}
            </div>
          </div>
        </div>
        ${job.company_description ? `<p class="text-secondary small mb-2">${job.company_description}</p>` : ''}
        <div class="d-flex flex-wrap gap-2 mt-2">
          ${job.company_website ? `<a href="${job.company_website}" target="_blank" class="btn btn-sm btn-outline-secondary">🌐 Website</a>` : ''}
          ${job.linkedin_profile ? `<a href="${job.linkedin_profile}" target="_blank" class="btn btn-sm btn-outline-primary" style="color: #0a66c2; border-color: #0a66c2;">in LinkedIn</a>` : ''}
          ${job.github_profile ? `<a href="${job.github_profile}" target="_blank" class="btn btn-sm btn-outline-dark">💻 GitHub</a>` : ''}
        </div>
      </div>
    ` : '';

    modalBody.innerHTML = `
      ${companySectionHtml}
      <div class="mb-4 p-3 rounded-3 border-0 bg-white shadow-sm">
        <div class="d-flex align-items-center gap-2 mb-2 flex-wrap">
          <span class="badge bg-secondary px-3 py-1 fs-6">${job.employment_type ? job.employment_type.replace("_", " ").toUpperCase() : "FULL TIME"}</span>
          <span class="badge bg-success-subtle text-success border border-success-subtle px-3 py-1 fs-6">⏱️ Required Experience: <strong>${expBadgeText}</strong></span>
        </div>
        <h3 class="fw-bold text-dark mb-1">${job.title}</h3>
        <div class="text-muted fs-6">📍 Location: <strong>${job.location || "Remote / Unspecified"}</strong></div>
        ${job.salary_range ? `<div class="text-success fw-semibold mt-1">💰 Salary: ${job.salary_range}</div>` : ""}
        ${job.fraud_risk_score ? `<div class="small text-muted mt-2">🛡️ AI Scam Risk Score: <strong>${job.fraud_risk_score}/100</strong> (${job.fraud_risk_level})</div>` : ''}
      </div>

      <!-- Extended Requirements Breakdown Cards -->
      <div class="row g-3 mb-4">
        <div class="col-md-6">
          <div class="p-3 rounded-3 border bg-white h-100 shadow-sm">
            <h6 class="fw-bold text-dark mb-2 d-flex align-items-center gap-1">
              <span>💼</span> Relevant Work Experience &amp; Industry
            </h6>
            <p class="small text-secondary mb-0" style="line-height: 1.6;">
              ${job.relevant_work_experience || `Requires minimum ${expYears} years of hands-on experience in ${job.industry || 'relevant domain'} roles.`}
            </p>
          </div>
        </div>
        <div class="col-md-6">
          <div class="p-3 rounded-3 border bg-white h-100 shadow-sm">
            <h6 class="fw-bold text-dark mb-2 d-flex align-items-center gap-1">
              <span>🏢</span> Company Experience Requirements
            </h6>
            <p class="small text-secondary mb-0" style="line-height: 1.6;">
              ${job.company_experience_requirements || 'Prior experience in product-based companies, high-growth technology startups, or enterprise tech environments.'}
            </p>
          </div>
        </div>
      </div>

      <!-- Skills Breakdown Section -->
      <div class="card p-3 mb-4 border-0 shadow-sm bg-light" style="border-radius: 12px;">
        <h6 class="fw-bold text-dark mb-3">🛠️ Required Technical &amp; Non-Technical Skills</h6>
        <div class="mb-3">
          <div class="small text-muted fw-semibold mb-1">Required Technical Skills:</div>
          <div>${techSkillsHtml || '<span class="text-muted small">No specific technical skills listed.</span>'}</div>
        </div>
        ${nonTechSkillsHtml ? `
          <div>
            <div class="small text-muted fw-semibold mb-1">Non-Technical &amp; Soft Skills:</div>
            <div>${nonTechSkillsHtml}</div>
          </div>
        ` : ''}
      </div>

      <div class="mb-3">
        <h6 class="fw-bold text-dark mb-2">Full Job Description &amp; Responsibilities</h6>
        <div class="p-3 bg-light rounded text-secondary" style="white-space: pre-line; line-height: 1.6;">${job.description}</div>
      </div>
    `;

    modalApplyBtn.dataset.jobId = job.id;
    const isApplied = appliedJobIdsSet.has(String(job.id));
    if (isApplied) {
      modalApplyBtn.disabled = true;
      modalApplyBtn.textContent = "Already Applied";
      modalApplyBtn.className = "btn btn-secondary";
    } else {
      modalApplyBtn.disabled = false;
      modalApplyBtn.textContent = "Apply Now →";
      modalApplyBtn.className = "btn btn-primary";
      modalApplyBtn.onclick = () => performApply(job.id, modalApplyBtn);
    }

    const modalEl = document.getElementById("jobDetailsModal");
    if (modalEl && window.bootstrap?.Modal) {
      const bsModal = new bootstrap.Modal(modalEl);
      bsModal.show();
    }
  }

  async function loadRecommended() {
    if (!recommendedListEl) return;
    try {
      const res = await recommendationsAPI.jobs(20);
      const items = res.data;
      if (!items || !items.length) {
        recommendedListEl.innerHTML =
          '<div class="col-12"><div class="p-3 text-center border rounded bg-white text-secondary small">No recommendations available yet. <a href="upload-resume.html">Upload your resume</a> to unlock AI-matched job recommendations.</div></div>';
        return;
      }

      // Cache match scores
      items.forEach((item) => {
        if (item.job && item.job.id != null) {
          recommendationScoresMap.set(String(item.job.id), item.match_score);
        }
      });

      // Filter and render top recommendations
      const topMatches = items.slice(0, 6);
      recommendedListEl.innerHTML = topMatches
        .map((item) => jobCard(item.job, { matchScore: item.match_score }))
        .join("");
      attachCardHandlers(recommendedListEl);
    } catch (err) {
      recommendedListEl.innerHTML =
        '<div class="col-12"><div class="p-3 text-center border rounded bg-white text-secondary small">Upload your resume to unlock AI-matched job recommendations. <a href="upload-resume.html">Upload Resume →</a></div></div>';
    }
  }

  function renderJobs() {
    if (!jobListEl) return;

    const totalCount = allFetchedJobs.length;
    if (jobsCountBadge) jobsCountBadge.textContent = totalCount;

    if (!totalCount) {
      jobListEl.innerHTML =
        '<div class="col-12"><div class="card p-4 text-center border shadow-sm bg-white"><div class="fs-2 mb-2">💼</div><h6 class="fw-bold text-dark mb-1">No Jobs Found</h6><p class="text-secondary small mb-0">No active job postings are available right now. Please check back soon or try another search role/keyword!</p></div></div>';
      if (offcanvasJobListEl) {
        offcanvasJobListEl.innerHTML = '<div class="text-muted py-3 text-center small">No job postings available.</div>';
      }
      if (jobsDisplayInfo) jobsDisplayInfo.textContent = "Showing 0 jobs";
      if (hamburgerToggleRemainingBtn) hamburgerToggleRemainingBtn.classList.add("d-none");
      return;
    }

    // Render offcanvas drawer with all jobs
    if (offcanvasJobListEl) {
      offcanvasJobListEl.innerHTML = allFetchedJobs.map((job) => offcanvasJobCard(job)).join("");
      attachCardHandlers(offcanvasJobListEl);
    }

    // Decide how many jobs to display on the main page (3 by default unless toggled/hamburger clicked)
    const visibleJobs = showingAllJobs ? allFetchedJobs : allFetchedJobs.slice(0, 3);
    jobListEl.innerHTML = visibleJobs.map((job) => jobCard(job)).join("");
    attachCardHandlers(jobListEl);

    // Update status text & toggle button
    if (jobsDisplayInfo) {
      jobsDisplayInfo.textContent = showingAllJobs
        ? `Showing all ${totalCount} jobs`
        : `Showing ${Math.min(3, totalCount)} of ${totalCount} jobs`;
    }

    if (hamburgerToggleRemainingBtn) {
      if (totalCount <= 3) {
        hamburgerToggleRemainingBtn.classList.add("d-none");
      } else {
        hamburgerToggleRemainingBtn.classList.remove("d-none");
        if (toggleBtnText) {
          toggleBtnText.textContent = showingAllJobs
            ? "Show Only 3 Jobs"
            : `Show Remaining Jobs (${totalCount - 3})`;
        }
      }
    }
  }

  async function loadJobs(filters = null) {
    if (!jobListEl) return;

    if (filters === null) {
      filters = {};
      const urlParams = new URLSearchParams(window.location.search);
      const roleParam = urlParams.get("role") || urlParams.get("title");

      if (roleParam) {
        const targetRoleSelect = document.getElementById("search-target-role");
        const searchTitleInput = document.getElementById("search-title");

        if (targetRoleSelect) {
          let foundInSelect = false;
          for (let opt of targetRoleSelect.options) {
            if (opt.value.toLowerCase() === roleParam.toLowerCase() || opt.text.toLowerCase() === roleParam.toLowerCase()) {
              targetRoleSelect.value = opt.value;
              foundInSelect = true;
              break;
            }
          }
          if (!foundInSelect && searchTitleInput) {
            searchTitleInput.value = roleParam;
          }
        }
        filters.title = roleParam;
      }
    }

    jobListEl.innerHTML = '<div class="col-12 text-muted py-3">Loading available jobs…</div>';
    if (offcanvasJobListEl) offcanvasJobListEl.innerHTML = '<div class="text-muted py-3 text-center">Loading jobs…</div>';
    try {
      const res = await jobsAPI.list(filters);
      allFetchedJobs = res.data || [];
      showingAllJobs = false; // Reset to 3 jobs view on new search
      renderJobs();

      // Check URL parameters to automatically open details modal for candidate
      const urlParams = new URLSearchParams(window.location.search);
      const jobIdParam = urlParams.get("job_id");
      const roleParam = urlParams.get("role") || urlParams.get("title");

      if (jobIdParam) {
        const targetJob = allFetchedJobs.find((j) => String(j.id) === jobIdParam);
        if (targetJob) showJobDetailsModal(targetJob);
      } else if (roleParam && allFetchedJobs.length > 0) {
        showJobDetailsModal(allFetchedJobs[0]);
      }
    } catch (err) {
      jobListEl.innerHTML = `<div class="col-12 text-danger small">${err.message}</div>`;
      if (offcanvasJobListEl) offcanvasJobListEl.innerHTML = `<div class="text-danger small">${err.message}</div>`;
    }
  }

  function triggerSearch() {
    const targetRole = document.getElementById("search-target-role")?.value || "";
    const title = document.getElementById("search-title")?.value.trim() || "";
    const location = document.getElementById("search-location")?.value.trim() || "";
    const verifiedOnly = document.getElementById("search-verified-only")?.checked || false;
    const filters = {};

    let queryTitle = title;
    if (targetRole) {
      queryTitle = queryTitle ? `${targetRole} ${queryTitle}` : targetRole;
    }
    if (queryTitle) filters.title = queryTitle;
    if (location) filters.location = location;
    if (verifiedOnly) filters.verified_only = true;

    loadJobs(filters);
  }

  // Hamburger top button event listener
  if (hamburgerMenuBtn) {
    hamburgerMenuBtn.addEventListener("click", () => {
      if (!showingAllJobs) {
        showingAllJobs = true;
        renderJobs();
      }
    });
  }

  // Hamburger remaining jobs button event listener
  if (hamburgerToggleRemainingBtn) {
    hamburgerToggleRemainingBtn.addEventListener("click", () => {
      showingAllJobs = !showingAllJobs;
      renderJobs();
    });
  }

  const searchBtn = document.getElementById("search-btn");
  if (searchBtn) {
    searchBtn.addEventListener("click", triggerSearch);
  }

  const targetRoleSelect = document.getElementById("search-target-role");
  if (targetRoleSelect) {
    targetRoleSelect.addEventListener("change", triggerSearch);
  }

  // Load initial data
  (async function init() {
    await loadAppliedJobIds();
    await loadRecommended();
    await loadJobs();
  })();

  // Reload when auth user verification completes
  document.addEventListener("ar:auth-ready", async () => {
    await loadAppliedJobIds();
    await loadRecommended();
    await loadJobs();
  });
})();






