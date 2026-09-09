/**
 * post-job.js — handles the "Post a Job" form submit.
 */
(function () {
  const form = document.getElementById("post-job-form");
  const alertBox = document.getElementById("post-job-alert");
  const submitBtn = document.getElementById("post-job-submit");
  const submitText = document.getElementById("post-job-submit-text");
  const spinner = document.getElementById("post-job-spinner");

  function showAlert(message, variant) {
    alertBox.textContent = message;
    alertBox.className = `alert alert-${variant} py-2`;
  }

  function parseSkillList(value) {
    const items = value
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);
    return items.length ? items : null; // null -> let the backend auto-extract
  }

  function setLoading(isLoading) {
    submitBtn.disabled = isLoading;
    spinner.classList.toggle("d-none", !isLoading);
    submitText.textContent = isLoading ? "Posting..." : "Post Job";
  }

  const analyzeBtn = document.getElementById("analyze-btn");
  const analyzeBtnText = document.getElementById("analyze-btn-text");
  const analyzeSpinner = document.getElementById("analyze-spinner");

  analyzeBtn.addEventListener("click", async () => {
    const description = document.getElementById("description").value.trim();
    if (description.length < 10) {
      showAlert("Write a description first (at least 10 characters), then analyze it.", "warning");
      return;
    }

    analyzeBtn.disabled = true;
    analyzeSpinner.classList.remove("d-none");
    analyzeBtnText.textContent = "Analyzing...";

    try {
      const res = await jobsAPI.analyze(description);
      const data = res.data;

      if (data.title) document.getElementById("title").value = data.title;
      if (data.required_skills?.length) {
        document.getElementById("required-skills").value = data.required_skills.join(", ");
      }
      if (data.preferred_skills?.length) {
        document.getElementById("preferred-skills").value = data.preferred_skills.join(", ");
      }
      if (data.non_technical_skills?.length && document.getElementById("non-technical-skills")) {
        document.getElementById("non-technical-skills").value = data.non_technical_skills.join(", ");
      }
      if (data.relevant_work_experience && document.getElementById("relevant-work-experience")) {
        document.getElementById("relevant-work-experience").value = data.relevant_work_experience;
      }
      if (data.company_experience_requirements && document.getElementById("company-experience-requirements")) {
        document.getElementById("company-experience-requirements").value = data.company_experience_requirements;
      }
      showAlert(`Analyzed (${data.source}). Review the pre-filled fields below before posting.`, "success");
    } catch (err) {
      showAlert(err.message, "danger");
    } finally {
      analyzeBtn.disabled = false;
      analyzeSpinner.classList.add("d-none");
      analyzeBtnText.textContent = "Analyze with AI";
    }
  });

  // Auto-prefill company details from saved recruiter profile if available
  (async function prefillCompanyDetails() {
    try {
      const res = await API.get("/recruiter-profile");
      if (res && res.data) {
        const p = res.data;
        if (p.company_name) document.getElementById("company-name").value = p.company_name;
        if (p.company_logo) document.getElementById("company-logo").value = p.company_logo;
        if (p.company_description) document.getElementById("company-description").value = p.company_description;
        if (p.website) document.getElementById("company-website").value = p.website;
        if (p.location) document.getElementById("company-location").value = p.location;
        if (p.industry) document.getElementById("industry").value = p.industry;
        if (p.company_size) document.getElementById("company-size").value = p.company_size;
        if (p.linkedin_url) document.getElementById("linkedin-profile").value = p.linkedin_url;
        if (p.github_url) document.getElementById("github-profile").value = p.github_url;
        if (p.other_links) document.getElementById("other-links").value = p.other_links;
      }
    } catch (e) {
      // Ignore if profile doesn't exist yet
    }
  })();

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    setLoading(true);

    const experienceRaw = document.getElementById("experience-required").value;
    const nonTechRaw = document.getElementById("non-technical-skills") ? document.getElementById("non-technical-skills").value : "";
    const relExpRaw = document.getElementById("relevant-work-experience") ? document.getElementById("relevant-work-experience").value : "";
    const compExpRaw = document.getElementById("company-experience-requirements") ? document.getElementById("company-experience-requirements").value : "";

    const payload = {
      title: document.getElementById("title").value.trim(),
      description: document.getElementById("description").value.trim(),
      location: document.getElementById("location").value.trim() || null,
      employment_type: document.getElementById("employment-type").value,
      experience_required: experienceRaw ? Number(experienceRaw) : null,
      salary_range: document.getElementById("salary-range").value.trim() || null,
      status: document.getElementById("status").value,
      required_skills: parseSkillList(document.getElementById("required-skills").value),
      preferred_skills: parseSkillList(document.getElementById("preferred-skills").value) || [],
      relevant_work_experience: relExpRaw.trim() || null,
      non_technical_skills: parseSkillList(nonTechRaw) || [],
      company_experience_requirements: compExpRaw.trim() || null,
      // Candidate Screening Settings
      min_ats_score: Number(document.getElementById("min-ats-score").value) || 60,
      min_job_match_score: Number(document.getElementById("min-job-match-score").value) || 60,
      min_experience: Number(document.getElementById("min-experience").value) || 0,
      auto_screening: document.getElementById("auto-screening").value === "true",
      auto_shortlist: document.getElementById("auto-shortlist").value === "true",
      // Company details
      company_name: document.getElementById("company-name").value.trim() || null,
      company_logo: document.getElementById("company-logo").value.trim() || null,
      company_description: document.getElementById("company-description").value.trim() || null,
      company_website: document.getElementById("company-website").value.trim() || null,
      company_location: document.getElementById("company-location").value.trim() || null,
      industry: document.getElementById("industry").value.trim() || null,
      company_size: document.getElementById("company-size").value || null,
      linkedin_profile: document.getElementById("linkedin-profile").value.trim() || null,
      github_profile: document.getElementById("github-profile").value.trim() || null,
      other_links: document.getElementById("other-links").value.trim() || null,
    };

    try {
      const jobRes = await jobsAPI.create(payload);
      const createdJob = jobRes.data;

      // Handle Coding Assessment Creation if enabled
      const enableCoding = document.getElementById("enable-coding-assessment")?.checked;
      if (enableCoding && window.codingAPI) {
        const assessmentTitle = document.getElementById("assessment-title")?.value.trim() || `${createdJob.title} Assessment`;
        const duration = parseInt(document.getElementById("assessment-duration")?.value) || 60;
        const passingScore = parseFloat(document.getElementById("assessment-passing-score")?.value) || 60;

        const selectedQIds = Array.from(document.querySelectorAll(".coding-q-checkbox:checked")).map(cb => cb.value);
        const questionsItems = selectedQIds.map((qId, idx) => ({
          question_id: qId,
          question_order: idx + 1,
          points: 20.0
        }));

        try {
          await codingAPI.createAssessment({
            job_id: createdJob.id,
            title: assessmentTitle,
            duration_minutes: duration,
            passing_score: passingScore,
            total_score: 100.0,
            max_attempts: 1,
            allowed_languages: ["python", "javascript", "java", "cpp", "csharp"],
            questions: questionsItems
          });
        } catch (cErr) {
          console.warn("Failed to attach coding assessment:", cErr);
        }
      }

      if (createdJob.fraud_risk_level === "HIGH" || createdJob.status === "pending_review") {
        showAlert(
          `Job "${createdJob.title}" saved, but AI Fraud Scan detected risk factors (Score: ${createdJob.fraud_risk_score}/100). It is currently under Admin Review before publishing.`,
          "warning"
        );
      } else {
        showAlert(`"${createdJob.title}" passed AI fraud verification and was published successfully!`, "success");
      }
      form.reset();
      document.getElementById("employment-type").value = "full_time";
      document.getElementById("status").value = "published";
      if (document.getElementById("coding-assessment-fields")) {
        document.getElementById("coding-assessment-fields").classList.add("d-none");
      }
      loadPostedJobs();
    } catch (err) {
      showAlert(err.message, "danger");
    } finally {
      setLoading(false);
    }
  });

  let currentUserId = null;
  const postedJobsContainer = document.getElementById("posted-jobs-container");
  const postedJobsAlert = document.getElementById("posted-jobs-alert");
  const refreshPostedJobsBtn = document.getElementById("refresh-posted-jobs-btn");

  function showPostedJobsAlert(msg, variant) {
    if (!postedJobsAlert) return;
    postedJobsAlert.textContent = msg;
    postedJobsAlert.className = `alert alert-${variant} py-2 mb-3`;
    postedJobsAlert.classList.remove("d-none");
    setTimeout(() => {
      postedJobsAlert.classList.add("d-none");
    }, 4000);
  }

  async function deleteJobPost(jobId, jobTitle, btn) {
    if (!confirm(`Are you sure you want to delete "${jobTitle}"? This action cannot be undone.`)) {
      return;
    }
    btn.disabled = true;
    btn.textContent = "Deleting...";
    try {
      if (jobsAPI.remove) {
        await jobsAPI.remove(jobId);
      } else {
        await jobsAPI.update(jobId, { status: "closed" });
      }
      showPostedJobsAlert(`Job post "${jobTitle}" was deleted successfully.`, "success");
      loadPostedJobs();
    } catch (err) {
      showPostedJobsAlert(`Failed to delete job: ${err.message}`, "danger");
      btn.disabled = false;
      btn.textContent = "🗑️ Delete";
    }
  }

  async function loadPostedJobs() {
    if (!postedJobsContainer) return;
    postedJobsContainer.innerHTML = '<div class="text-muted text-center py-3">Loading posted jobs…</div>';
    try {
      const res = await jobsAPI.list();
      const allJobs = res.data || [];
      const userJobs = currentUserId ? allJobs.filter(j => j.recruiter_id === currentUserId) : allJobs;

      if (!userJobs.length) {
        postedJobsContainer.innerHTML = '<div class="p-3 text-center text-muted small bg-light rounded">No job posts created yet. Fill out the form above to post your first job requisition!</div>';
        return;
      }

      const rowsHtml = userJobs.map(job => {
        const statusBadge = job.status === "published"
          ? `<span class="badge bg-success-subtle text-success border border-success border-opacity-25 px-2 py-1 rounded-pill">Published</span>`
          : job.status === "paused"
          ? `<span class="badge bg-warning-subtle text-dark border border-warning border-opacity-25 px-2 py-1 rounded-pill">Paused</span>`
          : `<span class="badge bg-secondary-subtle text-secondary border border-secondary border-opacity-25 px-2 py-1 rounded-pill">${job.status}</span>`;

        return `
          <tr>
            <td class="ps-3">
              <div class="fw-bold text-dark">${job.title}</div>
              <div class="text-muted small">ID: #${job.id.slice(0, 8)}...</div>
            </td>
            <td><span class="text-secondary small">${job.location || 'Remote'}</span></td>
            <td>${statusBadge}</td>
            <td class="text-secondary small">${new Date(job.created_at).toLocaleDateString()}</td>
            <td class="text-end pe-3">
              <button class="btn btn-sm btn-outline-danger delete-job-btn fw-semibold" data-job-id="${job.id}" data-job-title="${job.title}">
                🗑️ Delete
              </button>
            </td>
          </tr>
        `;
      }).join("");

      postedJobsContainer.innerHTML = `
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="bg-light text-uppercase fs-7 text-secondary">
              <tr>
                <th class="ps-3 py-2">Job Title</th>
                <th class="py-2">Location</th>
                <th class="py-2">Status</th>
                <th class="py-2">Date Posted</th>
                <th class="text-end pe-3 py-2">Actions</th>
              </tr>
            </thead>
            <tbody>${rowsHtml}</tbody>
          </table>
        </div>
      `;

      postedJobsContainer.querySelectorAll(".delete-job-btn").forEach(btn => {
        btn.addEventListener("click", () => deleteJobPost(btn.dataset.jobId, btn.dataset.jobTitle, btn));
      });
    } catch (err) {
      postedJobsContainer.innerHTML = `<div class="alert alert-danger mb-0">${err.message}</div>`;
    }
  }

  if (refreshPostedJobsBtn) {
    refreshPostedJobsBtn.addEventListener("click", loadPostedJobs);
  }

  // Load jobs initially & listen for auth
  loadPostedJobs();

  // Coding assessment field toggle & question loader
  const enableCodingCheckbox = document.getElementById("enable-coding-assessment");
  const codingFields = document.getElementById("coding-assessment-fields");
  const qSelectContainer = document.getElementById("coding-questions-select-container");

  if (enableCodingCheckbox && codingFields) {
    enableCodingCheckbox.addEventListener("change", async () => {
      codingFields.classList.toggle("d-none", !enableCodingCheckbox.checked);
      if (enableCodingCheckbox.checked && qSelectContainer && window.codingAPI) {
        qSelectContainer.innerHTML = '<small class="text-muted">Loading question bank...</small>';
        try {
          const res = await codingAPI.listQuestions();
          if (res.success && res.data.length > 0) {
            qSelectContainer.innerHTML = res.data.map(q => `
              <div class="form-check">
                <input class="form-check-input coding-q-checkbox" type="checkbox" value="${q.id}" id="q-check-${q.id}" checked />
                <label class="form-check-label small fw-semibold" for="q-check-${q.id}">
                  ${q.title} <span class="badge bg-secondary ms-1">${q.difficulty}</span> <span class="text-muted">(${q.category})</span>
                </label>
              </div>
            `).join("");
          } else {
            qSelectContainer.innerHTML = '<small class="text-muted">No questions in bank. <a href="coding-question-management.html" target="_blank">Create Question</a></small>';
          }
        } catch (err) {
          qSelectContainer.innerHTML = `<small class="text-danger">Failed to load question bank: ${err.message}</small>`;
        }
      }
    });
  }

  document.addEventListener("ar:auth-ready", (event) => {
    currentUserId = event.detail?.user?.id;
    loadPostedJobs();
  });
})();
