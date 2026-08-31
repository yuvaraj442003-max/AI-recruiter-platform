/**
 * jobs.js — loads recommended + searchable job listings and handles
 * "Apply" clicks for the candidate.
 */
(function () {
  const alertBox = document.getElementById("job-alert");
  const jobListEl = document.getElementById("job-list");
  const recommendedListEl = document.getElementById("recommended-list");

  function showAlert(message, variant) {
    if (!alertBox) return;
    alertBox.innerHTML = message;
    alertBox.className = `alert alert-${variant} py-2 mb-3`;
    alertBox.classList.remove("d-none");
  }

  const jobsCache = new Map();

  async function performApply(jobId, btn) {
    btn.disabled = true;
    btn.textContent = "Applying & Verifying Skills…";
    try {
      const res = await jobsAPI.apply(jobId);
      const appData = res.data || {};
      const score = Math.round(appData.ats_score || appData.match_score || 0);
      const matchedList = appData.matched_skills || [];
      const matchedStr = matchedList.length ? matchedList.join(", ") : "None";

      btn.textContent = `Applied · ${score}% match`;
      btn.classList.remove("btn-primary");
      btn.classList.add("btn-success");

      showAlert(
        `🎉 <strong>Application Submitted!</strong> ATS Score: <strong>${score}%</strong>. Verified Matched Skills: <span class="badge bg-success-subtle text-success border border-success-subtle ms-1">${matchedStr}</span>`,
        "success"
      );
    } catch (err) {
      btn.disabled = false;
      btn.textContent = "Apply";
      if (err.errorCode === "NO_RESUME" || (err.message && err.message.toLowerCase().includes("resume"))) {
        showAlert(
          `📄 <strong>Resume Required:</strong> Please upload your resume before applying so the system can verify your skills. <a href="upload-resume.html" class="fw-bold text-decoration-underline text-dark ms-2">Upload Resume Now →</a>`,
          "warning"
        );
      } else if (err.errorCode === "CONFLICT") {
        showAlert(`ℹ️ You have already applied to this job posting.`, "info");
      } else {
        showAlert(`⚠️ ${err.message || "Failed to submit application."}`, "danger");
      }
    }
  }

  function jobCard(job, { matchScore, showApply = true } = {}) {
    jobsCache.set(String(job.id), job);
    const skillBadges = (job.required_skills || [])
      .map((s) => `<span class="badge text-bg-light border me-1 mb-1">${s}</span>`)
      .join("");

    const scoreBadge =
      matchScore != null
        ? `<span class="badge text-bg-primary">${Math.round(matchScore)}% match</span>`
        : "";

    const verifiedBadge = (job.company_name && (job.company_name.includes("Acme") || job.company_name.includes("Tech") || job.company_name.includes("Corp")))
      ? `<span class="badge bg-success-subtle text-success border border-success-subtle ms-1">Verified 🛡️</span>`
      : "";

    const riskBadge = (job.fraud_risk_level === "HIGH")
      ? `<span class="badge bg-danger ms-1">High Scam Risk ⚠️</span>`
      : (job.fraud_risk_level === "MEDIUM")
      ? `<span class="badge bg-warning text-dark ms-1">Medium Risk</span>`
      : "";

    return `
      <div class="col-md-6 col-lg-4">
        <div class="card p-3 h-100 d-flex flex-column border shadow-sm style-card" style="border-radius: 12px;">
          <div class="d-flex justify-content-between align-items-start mb-1">
            <h6 class="fw-bold mb-0 text-dark">${job.title} ${verifiedBadge} ${riskBadge}</h6>
            ${scoreBadge}
          </div>
          <div class="text-muted small mb-2">
            🏢 ${job.company_name || 'Direct Employer'} · 📍 ${job.location || "Remote / Unspecified"} · 💼 ${job.employment_type.replace("_", " ")}
          </div>
          <p class="small text-secondary mb-2" style="flex-grow: 1;">${job.description.slice(0, 130)}${job.description.length > 130 ? "…" : ""}</p>
          <div class="mb-3">${skillBadges}</div>
          <div class="d-flex gap-2 mt-auto">
            <button class="btn btn-sm btn-outline-primary flex-grow-1 details-btn" data-job-id="${job.id}">
              ℹ️ View Details
            </button>
            ${showApply ? `<button class="btn btn-sm btn-primary flex-grow-1 apply-btn" data-job-id="${job.id}">Apply</button>` : ""}
          </div>
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
    const skillsHtml = (job.required_skills || [])
      .map((s) => `<span class="badge bg-primary-subtle text-primary border border-primary-subtle me-1 mb-1 px-3 py-2 fs-6">${s}</span>`)
      .join("");

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
      <div class="mb-3">
        <span class="badge bg-secondary mb-2">${job.employment_type.replace("_", " ").toUpperCase()}</span>
        <h3 class="fw-bold text-dark mb-1">${job.title}</h3>
        <div class="text-muted fs-6">📍 Location: <strong>${job.location || "Remote / Unspecified"}</strong></div>
        ${job.salary_range ? `<div class="text-success fw-semibold mt-1">💰 Salary: ${job.salary_range}</div>` : ""}
        ${job.fraud_risk_score ? `<div class="small text-muted mt-2">🛡️ AI Scam Risk Score: <strong>${job.fraud_risk_score}/100</strong> (${job.fraud_risk_level})</div>` : ''}
      </div>
      <hr />
      <div class="mb-4">
        <h6 class="fw-bold text-dark mb-2">Required Skills &amp; Competencies</h6>
        <div>${skillsHtml || '<span class="text-muted">No specific skills listed.</span>'}</div>
      </div>
      <div class="mb-3">
        <h6 class="fw-bold text-dark mb-2">Full Job Description &amp; Responsibilities</h6>
        <div class="p-3 bg-light rounded text-secondary" style="white-space: pre-line; line-height: 1.6;">${job.description}</div>
      </div>
    `;

    modalApplyBtn.dataset.jobId = job.id;
    modalApplyBtn.disabled = false;
    modalApplyBtn.textContent = "Apply Now →";
    modalApplyBtn.onclick = () => performApply(job.id, modalApplyBtn);


    const modalEl = document.getElementById("jobDetailsModal");
    if (modalEl && window.bootstrap?.Modal) {
      const bsModal = new bootstrap.Modal(modalEl);
      bsModal.show();
    }
  }

  async function loadRecommended() {

    if (!recommendedListEl) return;
    try {
      const res = await recommendationsAPI.jobs(6);
      const items = res.data;
      if (!items || !items.length) {
        recommendedListEl.innerHTML =
          '<div class="col-12"><div class="p-3 text-center border rounded bg-white text-secondary small">No recommendations available yet. <a href="upload-resume.html">Upload your resume</a> to unlock AI-matched job recommendations.</div></div>';
        return;
      }
      recommendedListEl.innerHTML = items
        .map((item) => jobCard(item.job, { matchScore: item.match_score }))
        .join("");
      attachCardHandlers(recommendedListEl);
    } catch (err) {
      recommendedListEl.innerHTML =
        '<div class="col-12"><div class="p-3 text-center border rounded bg-white text-secondary small">No recommendations available yet. Upload your resume to unlock job matching.</div></div>';
    }
  }

  async function loadJobs(filters = {}) {
    if (!jobListEl) return;
    jobListEl.innerHTML = '<div class="col-12 text-muted py-3">Loading available jobs…</div>';
    try {
      const res = await jobsAPI.list(filters);
      const jobs = res.data;
      if (!jobs || !jobs.length) {
        jobListEl.innerHTML =
          '<div class="col-12"><div class="card p-4 text-center border shadow-sm bg-white"><div class="fs-2 mb-2">💼</div><h6 class="fw-bold text-dark mb-1">No Jobs Found</h6><p class="text-secondary small mb-0">No active job postings are available right now. Please check back soon or try another search role/keyword!</p></div></div>';
        return;
      }
      jobListEl.innerHTML = jobs.map((job) => jobCard(job)).join("");
      attachCardHandlers(jobListEl);
    } catch (err) {
      jobListEl.innerHTML = `<div class="col-12 text-danger small">${err.message}</div>`;
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


  const searchBtn = document.getElementById("search-btn");
  if (searchBtn) {
    searchBtn.addEventListener("click", triggerSearch);
  }

  const targetRoleSelect = document.getElementById("search-target-role");
  if (targetRoleSelect) {
    targetRoleSelect.addEventListener("change", triggerSearch);
  }

  // Load immediately on script execution
  loadJobs();
  loadRecommended();

  // Reload when auth user verification completes
  document.addEventListener("ar:auth-ready", () => {
    loadRecommended();
    loadJobs();
  });
})();




