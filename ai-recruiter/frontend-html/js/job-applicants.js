/**
 * job-applicants.js — manages the applicant list for a specific job,
 * ATS threshold slider filtering, candidate side-by-side comparison tool,
 * detailed candidate ATS match reports, recruiter overrides, and AI recommendations.
 */
(function () {
  const params = new URLSearchParams(window.location.search);
  const jobId = params.get("job_id");

  const alertBox = document.getElementById("applicants-alert");
  const tableBody = document.getElementById("applicants-table-body");
  const jobTitleHeader = document.getElementById("job-title-header");
  const countBadge = document.getElementById("applicants-count-badge");
  const locationBadge = document.getElementById("job-location-badge");
  const modalEl = document.getElementById("applicantDetailModal");
  const modalBody = document.getElementById("modal-applicant-body");
  const modalName = document.getElementById("modal-candidate-name");

  const compModalEl = document.getElementById("candidateComparisonModal");
  const compModalBody = document.getElementById("comparison-modal-body");
  const compModalTitle = document.getElementById("comparison-modal-title");
  const compModalSubtitle = document.getElementById("comparison-modal-subtitle");
  const compareSelectedBtn = document.getElementById("compare-selected-btn");
  const compareCountBadge = document.getElementById("compare-count-badge");

  const slider = document.getElementById("ats-slider");
  const sliderVal = document.getElementById("ats-slider-val");

  let currentJob = null;
  let allApplications = [];
  let modalInstance = null;
  let compModalInstance = null;
  let activeFilter = "all";
  let minAtsFilter = 0;

  // Selected Candidate IDs Set for Comparison (Min 2, Max 3)
  const selectedCandidateIds = new Set();

  function showAlert(msg, variant = "success") {
    if (!alertBox) return;
    alertBox.textContent = msg;
    alertBox.className = `alert alert-${variant} py-2 mb-3`;
    alertBox.classList.remove("d-none");
    setTimeout(() => alertBox.classList.add("d-none"), 4000);
  }

  function getStatusBadge(status) {
    const s = (status || "applied").toLowerCase();
    if (s === "applied") return `<span class="badge bg-primary-subtle text-primary border border-primary border-opacity-25 px-3 py-1 rounded-pill">Applied</span>`;
    if (s === "shortlisted") return `<span class="badge bg-info-subtle text-info border border-info border-opacity-25 px-3 py-1 rounded-pill">Shortlisted</span>`;
    if (s === "under_review") return `<span class="badge bg-warning-subtle text-dark border border-warning border-opacity-25 px-3 py-1 rounded-pill">Under Review</span>`;
    if (s === "interview") return `<span class="badge bg-purple-subtle text-dark border border-purple border-opacity-25 px-3 py-1 rounded-pill">Interview Scheduled</span>`;
    if (s === "selected") return `<span class="badge bg-success-subtle text-success border border-success border-opacity-25 px-3 py-1 rounded-pill">Selected</span>`;
    if (s === "rejected") return `<span class="badge bg-danger-subtle text-danger border border-danger border-opacity-25 px-3 py-1 rounded-pill">Rejected</span>`;
    return `<span class="badge bg-secondary px-3 py-1 rounded-pill">${s}</span>`;
  }

  function updateCompareButtonState() {
    const count = selectedCandidateIds.size;
    if (compareCountBadge) compareCountBadge.textContent = count;

    if (compareSelectedBtn) {
      if (count >= 2 && count <= 5) {
        compareSelectedBtn.classList.remove("btn-secondary", "opacity-50");
        compareSelectedBtn.classList.add("btn-success");
      } else {
        compareSelectedBtn.classList.remove("btn-success");
        compareSelectedBtn.classList.add("btn-secondary");
      }
    }
  }

  function renderTable(apps) {
    if (!apps.length) {
      tableBody.innerHTML = `
        <tr>
          <td colspan="10" class="text-center py-5">
            <div class="fs-1 text-muted mb-2">👥</div>
            <h6 class="fw-bold text-dark">No applicants match your current filters</h6>
            <p class="text-secondary small mb-0">Try lowering the Minimum ATS Score slider or clearing filters.</p>
          </td>
        </tr>
      `;
      return;
    }

    tableBody.innerHTML = apps.map((app) => {
      const atsScore = Math.round(app.ats_score || app.match_score || 0);
      const matchScore = Math.round(app.job_match_score || app.match_score || 0);

      let scoreClass = "bg-primary";
      if (atsScore >= 80) scoreClass = "bg-success";
      else if (atsScore >= 60) scoreClass = "bg-info text-white";
      else if (atsScore >= 40) scoreClass = "bg-warning text-dark";
      else scoreClass = "bg-danger";

      const matchedCount = (app.matched_skills || []).length;
      const missingCount = (app.missing_skills || []).length;
      const totalSkills = matchedCount + missingCount;

      const candidateProfile = app.candidate_profile || {};
      const candId = candidateProfile.id || app.candidate_id || app.id;
      const expYears = candidateProfile.experience_years != null ? candidateProfile.experience_years : "—";
      const locText = candidateProfile.location || app.candidate_location || "—";
      const isChecked = selectedCandidateIds.has(candId) ? "checked" : "";

      const codingScore = app.coding_score !== null && app.coding_score !== undefined ? `${Math.round(app.coding_score)}%` : "—";
      const interviewScore = app.interview_score !== null && app.interview_score !== undefined ? `${Math.round(app.interview_score)}%` : "—";
      const overallScore = app.overall_score !== null && app.overall_score !== undefined ? `${Math.round(app.overall_score)}%` : `${atsScore}%`;

      return `
        <tr>
          <td class="ps-3 text-center">
            <input type="checkbox" class="form-check-input candidate-select-checkbox cursor-pointer" data-candidate-id="${candId}" data-name="${app.candidate_name || 'Candidate'}" ${isChecked} />
          </td>
          <td class="ps-2">
            <div class="fw-bold text-dark fs-6">${app.candidate_name || 'Candidate'}</div>
            <div class="text-muted small">${app.candidate_email || ''}</div>
            ${app.recruiter_override ? `<span class="badge bg-warning-subtle text-dark border border-warning px-2 py-0 small mt-1" title="${app.override_reason}">⚠️ Recruiter Override</span>` : ''}
          </td>
          <td>
            <span class="badge ${scoreClass} px-2 py-1 rounded-pill fs-6">${atsScore}%</span>
          </td>
          <td>
            <a href="screening-detail.html?application_id=${app.id}" class="badge bg-primary-subtle text-primary border border-primary px-2 py-1 rounded-pill fs-6 text-decoration-none" title="View AI Screening Breakdown">
              ${app.overall_score ? Math.round(app.overall_score) + '%' : (app.screening_status === 'completed' ? 'Completed' : 'Screening ➔')}
            </a>
          </td>
          <td>
            <a href="integrity-report.html?attempt_id=${app.coding_attempt_id || app.id}" class="badge bg-info-subtle text-dark border border-info px-2 py-1 rounded-pill fs-6 text-decoration-none" title="View AI-Assisted Integrity Monitoring Report">
              ${codingScore} 🛡️
            </a>
          </td>
          <td>
            <a href="interview-scorecard.html?interview_id=${app.interview_id || app.id}&job_id=${currentJob ? currentJob.id : ''}" class="badge bg-purple-subtle text-dark border border-purple px-2 py-1 rounded-pill fs-6 text-decoration-none" title="View AI Executive Candidate Scorecard">
              ${interviewScore} 📊
            </a>
          </td>
          <td>
            <span class="badge bg-success px-2 py-1 rounded-pill fs-6 text-white">${overallScore}</span>
          </td>
          <td class="text-secondary small fw-medium">${new Date(app.applied_at).toLocaleDateString()}</td>
          <td>${getStatusBadge(app.status)}</td>
          <td class="text-end pe-4">
            <a href="screening-detail.html?application_id=${app.id}" class="btn btn-sm btn-outline-info fw-semibold me-1" title="Inspect AI Candidate Pre-Screening">
              🤖 AI Screening
            </a>
            <button class="btn btn-sm btn-outline-success fw-semibold download-resume-btn me-1" data-candidate-id="${candidateProfile.id || app.candidate_id}">
              📄 Resume
            </button>
            <button class="btn btn-sm btn-outline-primary fw-semibold msg-applicant-btn me-1" data-user-id="${candidateProfile.user_id || ''}" data-name="${app.candidate_name || 'Candidate'}">
              💬 Message
            </button>
            <button class="btn btn-sm btn-outline-secondary fw-semibold schedule-applicant-btn me-1" data-app-id="${app.id}" data-candidate-id="${candId}" data-candidate-name="${app.candidate_name || 'Candidate'}" title="Request &amp; Schedule Interview Time Slot">
              📅 Schedule
            </button>
            <button class="btn btn-sm btn-outline-dark fw-semibold feedback-btn me-1" data-app-id="${app.id}" data-name="${app.candidate_name || 'Candidate'}" title="Candidate Feedback">
              💬 Feedback
            </button>
            <button class="btn btn-sm btn-primary fw-semibold view-applicant-btn px-3" data-app-id="${app.id}">
              👤 Profile &amp; ATS &rarr;
            </button>
          </td>
        </tr>
      `;
    }).join("");

    // Attach Selection Checkbox Listeners with Min 2, Max 3 rule
    tableBody.querySelectorAll(".candidate-select-checkbox").forEach(cb => {
      cb.addEventListener("change", (e) => {
        const cId = cb.dataset.candidateId;
        if (cb.checked) {
          if (selectedCandidateIds.size >= 3) {
            cb.checked = false;
            showAlert("Maximum 3 candidates can be selected for side-by-side comparison.", "warning");
            return;
          }
          selectedCandidateIds.add(cId);
        } else {
          selectedCandidateIds.delete(cId);
        }
        updateCompareButtonState();
      });
    });

    // Attach Action Listeners
    tableBody.querySelectorAll(".download-resume-btn").forEach(btn => {
      btn.addEventListener("click", async (e) => {
        e.stopPropagation();
        const cid = btn.dataset.candidateId;
        if (!cid) return;
        btn.disabled = true;
        try {
          await resumesAPI.download(cid);
        } catch (err) {
          showAlert(`Failed to download resume: ${err.message}`, "danger");
        } finally {
          btn.disabled = false;
        }
      });
    });

    tableBody.querySelectorAll(".msg-applicant-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const uid = btn.dataset.userId;
        const name = btn.dataset.name;
        if (uid && window.openChatWithUser) {
          window.openChatWithUser(uid, name, "candidate");
        } else if (window.openChatWithUser) {
          window.openChatWithUser();
        }
      });
    });

    tableBody.querySelectorAll(".schedule-applicant-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const appId = btn.dataset.appId;
        const candId = btn.dataset.candidateId;
        const candName = btn.dataset.candidateName;

        document.getElementById("sched-modal-job-display").value = currentJob ? currentJob.title : "Position";
        document.getElementById("sched-modal-job-id").value = currentJob ? currentJob.id : "";
        document.getElementById("sched-modal-cand-display").value = candName;
        document.getElementById("sched-modal-cand-id").value = candId;
        document.getElementById("sched-modal-app-id").value = appId;

        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        document.getElementById("sched-modal-date").value = tomorrow.toISOString().slice(0, 10);
        document.getElementById("sched-modal-time").value = "10:00";

        const alertEl = document.getElementById("modal-sched-alert");
        if (alertEl) alertEl.classList.add("d-none");

        const modalEl = document.getElementById("scheduleInterviewModal");
        if (window.bootstrap && modalEl) {
          const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
          modal.show();
        }
      });
    });

    tableBody.querySelectorAll(".view-applicant-btn").forEach(btn => {
      btn.addEventListener("click", () => openApplicantDetail(btn.dataset.appId));
    });

    tableBody.querySelectorAll(".feedback-btn").forEach(btn => {
      btn.addEventListener("click", () => openFeedbackModal(btn.dataset.appId, btn.dataset.name));
    });
  }

  let activeFeedbackAppId = null;
  let feedbackModalInstance = null;

  async function openFeedbackModal(appId, candName = "Candidate") {
    activeFeedbackAppId = appId;
    const modalEl = document.getElementById("candidateFeedbackModal");
    const bodyEl = document.getElementById("feedback-modal-body");
    const titleEl = document.getElementById("feedback-modal-title");
    if (!modalEl || !bodyEl) return;

    if (!feedbackModalInstance && window.bootstrap) {
      feedbackModalInstance = new bootstrap.Modal(modalEl);
    }
    if (titleEl) titleEl.textContent = `Candidate Feedback — ${candName}`;
    bodyEl.innerHTML = `<div class="text-center py-5 text-muted"><div class="spinner-border text-primary mb-3"></div><div>Loading or generating candidate feedback draft…</div></div>`;
    feedbackModalInstance.show();

    try {
      let fbRes;
      try {
        fbRes = await feedbackAPI.get(appId);
      } catch (err) {
        fbRes = await feedbackAPI.generate(appId);
      }
      const fb = fbRes.data || fbRes;
      renderFeedbackModalContent(fb);
    } catch (err) {
      bodyEl.innerHTML = `<div class="alert alert-danger py-2 mb-0">Failed to load candidate feedback: ${err.message}</div>`;
    }
  }

  function renderFeedbackModalContent(fb) {
    const bodyEl = document.getElementById("feedback-modal-body");
    if (!bodyEl) return;

    const strengthsList = (fb.strengths || []).map(s => `<span class="badge bg-success-subtle text-success border border-success border-opacity-25 px-2 py-1 rounded-pill me-1 mb-1">✓ ${s}</span>`).join("");
    const gapsList = (fb.areas_for_improvement || []).map(g => `<span class="badge bg-danger-subtle text-danger border border-danger border-opacity-25 px-2 py-1 rounded-pill me-1 mb-1">• ${g}</span>`).join("");

    bodyEl.innerHTML = `
      <div class="mb-3">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <span class="badge ${fb.feedback_status === 'SENT' ? 'bg-success' : 'bg-warning text-dark'} px-3 py-1 rounded-pill fw-bold">
            Status: ${fb.feedback_status}
          </span>
          <span class="text-muted small">Generated: ${fb.generated_at ? new Date(fb.generated_at).toLocaleString() : 'Now'}</span>
        </div>
        <div class="card p-3 bg-light border-0 mb-3" style="border-radius: 10px;">
          <h6 class="fw-bold text-dark mb-2">Evidence-Based Profile Assessment</h6>
          <div class="mb-2">
            <span class="small fw-bold text-secondary d-block mb-1">Verified Strengths:</span>
            <div>${strengthsList || '<span class="text-muted small">Technical background</span>'}</div>
          </div>
          <div>
            <span class="small fw-bold text-secondary d-block mb-1">Top Job Requirements Gaps:</span>
            <div>${gapsList || '<span class="text-muted small">Specific role requirement gap</span>'}</div>
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label fw-bold text-dark mb-1">Feedback Content (Editable Text):</label>
          <textarea id="feedback-editable-text" class="form-control" rows="8" style="border-radius: 8px; font-size: 0.95rem; line-height: 1.5;">${fb.final_content || fb.draft_content || ''}</textarea>
          <div class="form-text small text-muted">You can edit the text above before approving and sending it to the candidate.</div>
        </div>
      </div>
    `;

    const approveBtn = document.getElementById("btn-feedback-approve-send");
    if (approveBtn) {
      if (fb.feedback_status === "SENT") {
        approveBtn.disabled = true;
        approveBtn.textContent = "✓ Already Sent";
      } else {
        approveBtn.disabled = false;
        approveBtn.textContent = "✅ Approve & Send";
      }
    }
  }

  function applyFilters() {
    let filtered = allApplications.filter(app => {
      const score = Math.round(app.ats_score || app.match_score || 0);

      // Slider filter
      if (score < minAtsFilter) return false;

      // Category / Pill filter
      if (activeFilter === "ats-80") return score >= 80;
      if (activeFilter === "ats-60") return score >= 60;
      if (activeFilter === "ats-low") return score < 60;
      if (activeFilter === "shortlisted") return (app.status || "").toLowerCase() === "shortlisted";
      if (activeFilter === "under_review") return (app.status || "").toLowerCase() === "under_review" || (app.status || "").toLowerCase() === "applied";
      if (activeFilter === "interview") return (app.status || "").toLowerCase() === "interview";
      if (activeFilter === "selected") return (app.status || "").toLowerCase() === "selected";
      if (activeFilter === "rejected") return (app.status || "").toLowerCase() === "rejected";

      return true;
    });

    countBadge.textContent = `Applicants: ${filtered.length} / ${allApplications.length}`;
    renderTable(filtered);
  }

  async function loadJobAndApplicants() {
    let activeJobId = jobId;

    if (!activeJobId || activeJobId === "undefined" || activeJobId === "null") {
      try {
        const jobsRes = await jobsAPI.list();
        const myJobs = jobsRes.data || [];
        if (myJobs.length > 0) {
          activeJobId = myJobs[0].id || myJobs[0].job_id;
          window.history.replaceState({}, "", `job-applicants.html?job_id=${activeJobId}`);
        } else {
          tableBody.innerHTML = `
            <tr>
              <td colspan="10" class="text-center py-5">
                <div class="fs-1 text-muted mb-2">📁</div>
                <h6 class="fw-bold text-dark">No job selected or posted yet</h6>
                <p class="text-secondary small mb-3">Please select a job from <a href="my-jobs.html" class="fw-semibold text-primary">Manage Jobs</a> or create a new job posting.</p>
                <a href="post-job.html" class="btn btn-sm btn-success text-white fw-semibold">➕ Post a New Job</a>
              </td>
            </tr>
          `;
          return;
        }
      } catch (e) {
        tableBody.innerHTML = `<tr><td colspan="10" class="text-center py-4 text-danger">No job specified. Please select a job from <a href="my-jobs.html">Manage Jobs</a>.</td></tr>`;
        return;
      }
    }

    try {
      const [jobRes, appsRes] = await Promise.all([
        jobsAPI.get(activeJobId),
        jobsAPI.applications(activeJobId)
      ]);

      currentJob = jobRes.data;
      jobTitleHeader.textContent = `${currentJob.title} — Applicants`;
      locationBadge.textContent = currentJob.location ? `📍 ${currentJob.location}` : "";

      const rediscoveryBtn = document.getElementById("btn-talent-rediscovery");
      if (rediscoveryBtn && currentJob) {
        rediscoveryBtn.href = `talent-rediscovery.html?job_id=${currentJob.id || currentJob.job_id}`;
      }

      allApplications = appsRes.data || [];
      applyFilters();

    } catch (err) {
      tableBody.innerHTML = `<tr><td colspan="10" class="text-center py-4 text-danger">${err.message}</td></tr>`;
    }
  }

  async function openCandidateComparison() {
    const count = selectedCandidateIds.size;
    if (count < 2 || count > 5) {
      showAlert("Please select between 2 and 5 candidates for side-by-side comparison.", "warning");
      return;
    }

    if (!compModalInstance && window.bootstrap) {
      compModalInstance = new bootstrap.Modal(compModalEl);
    }

    compModalBody.innerHTML = `
      <div class="text-center py-5 text-muted">
        <div class="spinner-border text-success mb-3" style="width: 3rem; height: 3rem;"></div>
        <h5 class="fw-bold text-dark">Generating Candidate Side-by-Side Comparison &amp; AI Recommendation…</h5>
        <p class="small text-secondary mb-0">Analyzing ATS match scores, skill matrix, experience, and interview performance.</p>
      </div>
    `;
    if (compModalInstance) compModalInstance.show();

    try {
      const candidateIdList = Array.from(selectedCandidateIds);
      let compData;
      try {
        const res = await comparisonAPI.compare(jobId, candidateIdList);
        compData = res.data;
      } catch {
        const res = await analyticsAPI.compareCandidates(jobId, candidateIdList);
        compData = res.data;
      }

      compModalTitle.textContent = `Candidate Side-by-Side Comparison — ${compData.job_title}`;
      compModalSubtitle.textContent = `Comparing ${compData.candidates.length} Selected Candidates`;

      renderComparisonModalContent(compData);
    } catch (err) {
      compModalBody.innerHTML = `<div class="alert alert-danger p-4"><strong>Comparison Failed:</strong> ${err.message}</div>`;
    }
  }

  function renderComparisonModalContent(data) {
    const candidates = data.candidates || [];
    const skillMatrix = data.skill_matrix || [];
    const recommendedCand = data.recommended_candidate || "Candidate";

    // 1. Candidate Info Columns Header
    const colWidthPct = Math.floor(80 / candidates.length);

    const candHeaders = candidates.map(c => `
      <th style="width: ${colWidthPct}%;" class="text-center border-start py-3">
        <div class="fw-bold fs-5 text-dark mb-1">${c.name}</div>
        <div class="text-muted small mb-2">${c.headline || 'Candidate'}</div>
        <span class="badge bg-primary-subtle text-primary border px-3 py-1 rounded-pill mb-2">${c.email || '—'}</span>
        <div>
          <button class="btn btn-sm btn-outline-success download-resume-btn px-2 py-1" data-candidate-id="${c.candidate_id}">
            📄 Download Resume
          </button>
        </div>
      </th>
    `).join("");

    // 2. Candidate Information Rows
    const infoRoleRow = candidates.map(c => `<td class="border-start small text-center fw-semibold text-secondary">${c.headline || '—'}</td>`).join("");
    const infoLocRow = candidates.map(c => `<td class="border-start small text-center text-muted">📍 ${c.location}</td>`).join("");
    const infoExpRow = candidates.map(c => `<td class="border-start small text-center fw-bold text-dark">${c.experience_years} Years</td>`).join("");
    const infoEduRow = candidates.map(c => `<td class="border-start small text-center text-secondary">${c.education || 'Not specified'}</td>`).join("");

    // 3. ATS / Job Match Breakdown Rows
    const atsScoreRow = candidates.map(c => {
      let badge = "bg-success";
      if (c.ats_score < 40) badge = "bg-danger";
      else if (c.ats_score < 60) badge = "bg-warning text-dark";
      else if (c.ats_score < 80) badge = "bg-info text-white";
      return `<td class="border-start text-center py-2"><span class="badge ${badge} fs-5 px-3 py-1 rounded-pill">${c.ats_score}%</span></td>`;
    }).join("");

    const skillsScoreRow = candidates.map(c => `<td class="border-start text-center small fw-semibold">${c.skills_match_score}%</td>`).join("");
    const expScoreRow = candidates.map(c => `<td class="border-start text-center small fw-semibold">${c.experience_match_score}%</td>`).join("");
    const kwScoreRow = candidates.map(c => `<td class="border-start text-center small fw-semibold">${c.keyword_match_score}%</td>`).join("");
    const respScoreRow = candidates.map(c => `<td class="border-start text-center small fw-semibold">${c.responsibility_match_score}%</td>`).join("");
    const eduScoreRow = candidates.map(c => `<td class="border-start text-center small fw-semibold">${c.education_match_score}%</td>`).join("");
    const locScoreRow = candidates.map(c => `<td class="border-start text-center small fw-semibold">${c.location_match_score}%</td>`).join("");

    // 4. Interview Performance Rows (Check if any interview data exists)
    const hasAnyInterviews = candidates.some(c => c.interview_performance && c.interview_performance.overall_score != null);

    let interviewSectionHtml = "";
    if (hasAnyInterviews) {
      const intOverallRow = candidates.map(c => {
        const int = c.interview_performance;
        if (!int || int.overall_score == null) return `<td class="border-start text-center text-muted small">—</td>`;
        return `<td class="border-start text-center"><span class="badge bg-warning text-dark fs-6 px-3 py-1 rounded-pill">${int.overall_score}/100</span></td>`;
      }).join("");

      const intTechRow = candidates.map(c => `<td class="border-start text-center small fw-semibold">${(c.interview_performance && c.interview_performance.technical_score) != null ? c.interview_performance.technical_score + '/100' : '—'}</td>`).join("");
      const intCommRow = candidates.map(c => `<td class="border-start text-center small fw-semibold">${(c.interview_performance && c.interview_performance.communication_score) != null ? c.interview_performance.communication_score + '/100' : '—'}</td>`).join("");
      const intProbRow = candidates.map(c => `<td class="border-start text-center small fw-semibold">${(c.interview_performance && c.interview_performance.problem_solving_score) != null ? c.interview_performance.problem_solving_score + '/100' : '—'}</td>`).join("");

      interviewSectionHtml = `
        <tr class="table-dark text-white fw-bold"><td colspan="${candidates.length + 1}">3. Interview Evaluation Performance</td></tr>
        <tr><td class="fw-semibold bg-light">Overall Interview Score</td>${intOverallRow}</tr>
        <tr><td class="fw-semibold bg-light">Technical Score</td>${intTechRow}</tr>
        <tr><td class="fw-semibold bg-light">Communication Score</td>${intCommRow}</tr>
        <tr><td class="fw-semibold bg-light">Problem-Solving Score</td>${intProbRow}</tr>
      `;
    }

    // 5. Skill Matrix Rows
    const skillMatrixRows = skillMatrix.map(skRow => {
      const candidateCells = candidates.map(c => {
        const status = skRow.candidates[c.name];
        if (status === "matching") {
          return `<td class="border-start text-center"><span class="badge bg-success-subtle text-success border border-success px-3 py-1 rounded-pill">✓ Matching</span></td>`;
        } else if (status === "missing") {
          return `<td class="border-start text-center"><span class="badge bg-danger-subtle text-danger border border-danger px-3 py-1 rounded-pill">✗ Missing</span></td>`;
        } else {
          return `<td class="border-start text-center"><span class="badge bg-light text-muted border px-2 py-1">Not Specified</span></td>`;
        }
      }).join("");

      return `
        <tr>
          <td class="fw-medium bg-light">
            ${skRow.skill} ${skRow.is_required ? `<span class="badge bg-primary-subtle text-primary border ms-1 fs-7">Required</span>` : ''}
          </td>
          ${candidateCells}
        </tr>
      `;
    }).join("");

    // 6. Experience & Education Rows
    const expTotalRow = candidates.map(c => `<td class="border-start text-center small fw-bold">${c.experience_years} Years</td>`).join("");
    const expWorkHistoryRow = candidates.map(c => `<td class="border-start small text-secondary p-3"><div style="max-height: 120px; overflow-y: auto;">${c.work_experience}</div></td>`).join("");
    const eduHistoryRow = candidates.map(c => `<td class="border-start small text-secondary p-3"><div style="max-height: 100px; overflow-y: auto;">${c.education}</div></td>`).join("");
    const certsRow = candidates.map(c => `<td class="border-start small text-secondary p-3">${c.certifications}</td>`).join("");

    // AI Recommendation Box HTML
    const formattedWhyReason = (data.recommendation_reason || "")
      .split("\n")
      .map(r => r.trim())
      .filter(r => r.length > 0)
      .map(r => `<li>${r.replace(/^[•\-\*\s]+/, '')}</li>`)
      .join("");

    const candSummariesHtml = candidates.map(c => {
      const strengths = (data.candidate_strengths && data.candidate_strengths[c.name]) || [];
      const weaknesses = (data.candidate_weaknesses && data.candidate_weaknesses[c.name]) || [];
      const missing = (data.missing_skills && data.missing_skills[c.name]) || [];

      return `
        <div class="col-md-${12 / candidates.length}">
          <div class="card border-0 shadow-sm p-3 h-100 ${c.name === recommendedCand ? 'border border-2 border-success bg-success-subtle' : 'bg-light'}">
            <div class="d-flex align-items-center justify-content-between mb-2">
              <h6 class="fw-bold mb-0 text-dark">${c.name}</h6>
              ${c.name === recommendedCand ? '<span class="badge bg-success text-white">★ Recommended</span>' : ''}
            </div>
            <div class="small mb-2">
              <strong class="text-success">Strengths:</strong>
              <ul class="mb-2 ps-3 text-secondary">
                ${strengths.map(s => `<li>${s}</li>`).join('') || '<li>Standard qualifications</li>'}
              </ul>
            </div>
            <div class="small mb-0">
              <strong class="text-danger">Weaknesses / Missing:</strong>
              <ul class="mb-0 ps-3 text-secondary">
                ${weaknesses.map(w => `<li>${w}</li>`).join('') || '<li>No critical drawbacks</li>'}
              </ul>
            </div>
          </div>
        </div>
      `;
    }).join("");

    compModalBody.innerHTML = `
      <!-- Table Wrapper for Horizontal Scroll on Responsive Screens -->
      <div class="table-responsive mb-4" style="overflow-x: auto;">
        <table class="table table-bordered align-middle mb-0" style="min-width: 800px;">
          <thead class="bg-light">
            <tr>
              <th style="width: 20%;" class="py-3 ps-3 text-dark fw-bold fs-6">Comparison Attribute</th>
              ${candHeaders}
            </tr>
          </thead>
          <tbody>
            <!-- 1. Candidate Information -->
            <tr class="table-dark text-white fw-bold"><td colspan="${candidates.length + 1}">1. Candidate Information</td></tr>
            <tr><td class="fw-semibold bg-light">Current / Target Role</td>${infoRoleRow}</tr>
            <tr><td class="fw-semibold bg-light">Location</td>${infoLocRow}</tr>
            <tr><td class="fw-semibold bg-light">Years of Experience</td>${infoExpRow}</tr>
            <tr><td class="fw-semibold bg-light">Education</td>${infoEduRow}</tr>

            <!-- 2. ATS / Job Match Breakdown -->
            <tr class="table-dark text-white fw-bold"><td colspan="${candidates.length + 1}">2. ATS / Job Match Sub-Scores</td></tr>
            <tr><td class="fw-semibold bg-light">ATS Match Score (Overall)</td>${atsScoreRow}</tr>
            <tr><td class="fw-semibold bg-light">Skills Match Score (30%)</td>${skillsScoreRow}</tr>
            <tr><td class="fw-semibold bg-light">Experience Match Score (20%)</td>${expScoreRow}</tr>
            <tr><td class="fw-semibold bg-light">Required Keywords Match (15%)</td>${kwScoreRow}</tr>
            <tr><td class="fw-semibold bg-light">Responsibilities Match (15%)</td>${respScoreRow}</tr>
            <tr><td class="fw-semibold bg-light">Education Match (10%)</td>${eduScoreRow}</tr>
            <tr><td class="fw-semibold bg-light">Location Match (5%)</td>${locScoreRow}</tr>

            <!-- 3. Interview Performance -->
            ${interviewSectionHtml}

            <!-- 4. Skills Matrix -->
            <tr class="table-dark text-white fw-bold"><td colspan="${candidates.length + 1}">4. Skills Matrix &amp; Requirement Match</td></tr>
            ${skillMatrixRows}

            <!-- 5. Experience Comparison -->
            <tr class="table-dark text-white fw-bold"><td colspan="${candidates.length + 1}">5. Detailed Work Experience Comparison</td></tr>
            <tr><td class="fw-semibold bg-light">Total Experience Years</td>${expTotalRow}</tr>
            <tr><td class="fw-semibold bg-light">Previous Roles &amp; Work History</td>${expWorkHistoryRow}</tr>

            <!-- 6. Education Comparison -->
            <tr class="table-dark text-white fw-bold"><td colspan="${candidates.length + 1}">6. Education &amp; Certifications</td></tr>
            <tr><td class="fw-semibold bg-light">Degree &amp; Academic History</td>${eduHistoryRow}</tr>
            <tr><td class="fw-semibold bg-light">Certifications</td>${certsRow}</tr>
          </tbody>
        </table>
      </div>

      <!-- AI Candidate Recommendation Section -->
      <div class="card border-0 shadow-sm p-4 text-dark" style="background: linear-gradient(135deg, #e8f5e9 0%, #ffffff 100%); border-radius: 14px; border-left: 6px solid #28a745 !important;">
        <div class="d-flex align-items-center gap-2 mb-3">
          <span class="fs-2">🤖</span>
          <div>
            <h5 class="fw-bold text-success mb-0">AI Candidate Hiring Recommendation</h5>
            <span class="small text-muted">Powered by AI Recruiter LLM &amp; multi-dimensional ATS evaluation</span>
          </div>
        </div>

        <div class="alert alert-success border-success bg-white p-3 rounded-3 mb-3">
          <h5 class="fw-bold text-success mb-2">🏆 Recommended Candidate: <u>${recommendedCand}</u></h5>
          <p class="fw-semibold text-dark mb-2">Key Reasons for Recommendation:</p>
          <ul class="mb-0 ps-3 text-secondary fw-medium">
            ${formattedWhyReason || '<li>Top overall alignment with job requirements and candidate metrics.</li>'}
          </ul>
        </div>

        <h6 class="fw-bold text-dark mb-3">Candidate Breakdown &amp; Comparative Analysis:</h6>
        <div class="row g-3">
          ${candSummariesHtml}
        </div>
      </div>
    `;

    // Attach Download Listeners inside Comparison Modal
    compModalBody.querySelectorAll(".download-resume-btn").forEach(btn => {
      btn.addEventListener("click", async () => {
        const cid = btn.dataset.candidateId;
        if (!cid) return;
        btn.disabled = true;
        try {
          await resumesAPI.download(cid);
        } catch (err) {
          alert(`Download failed: ${err.message}`);
        } finally {
          btn.disabled = false;
        }
      });
    });
  }

  function escapeHtml(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function renderAssessmentHeaderBanner(session, app = {}) {
    const channel = (session?.channel || "WhatsApp").toUpperCase() + " SCREENING";
    const candidateName = session?.candidate_name || app?.candidate_name || "Candidate Profile";
    const jobTitle = session?.job_title || app?.job_title || (currentJob ? currentJob.title : "Target Position");

    const currentQ = session?.current_question_index ?? 0;
    const totalQ = session?.total_questions ?? 5;
    const statusStr = (session?.status || app?.status || "Pending").toUpperCase();

    const dateStr = session?.completed_at || session?.created_at || app?.applied_at;
    const formattedDate = dateStr ? new Date(dateStr).toLocaleDateString() : "In Progress";

    const rawScore = session?.screening_score ?? app?.overall_score ?? app?.ats_score ?? 0;
    const score = Math.round(rawScore);

    const statusLower = (session?.status || app?.status || "").toLowerCase();
    const recLower = (session?.recommendation || app?.recommendation || "").toLowerCase();
    const isFailed = statusLower === "failed" || statusLower === "rejected" || 
                     recLower.includes("fail") || recLower.includes("reject") || recLower.includes("not recommended") ||
                     (score === 0 && (currentQ > 0 || statusLower === "completed" || statusLower === "failed"));

    let scoreBoxBg = "#fee2e2";
    let scoreBoxColor = "#b91c1c";
    if (isFailed) {
      scoreBoxBg = "#fee2e2";
      scoreBoxColor = "#b91c1c";
    } else if (score >= 80) {
      scoreBoxBg = "#dcfce7";
      scoreBoxColor = "#15803d";
    } else if (score >= 60) {
      scoreBoxBg = "#fef9c3";
      scoreBoxColor = "#a16207";
    }

    let recText = "PENDING EVALUATION";
    if (isFailed) {
      recText = "❌ ASSESSMENT FAILED (NOT RECOMMENDED)";
    } else if (session?.recommendation) {
      recText = session.recommendation.toUpperCase();
    } else if (statusStr === "COMPLETED") {
      recText = "PASSED / RECOMMENDED";
    }

    const appId = app?.id || session?.application_id || "";
    const failedNoticeHtml = isFailed ? `
      <div class="alert alert-danger border-danger shadow-sm p-4 mb-4" style="border-radius: 12px; background: #fff5f5;">
        <div class="d-flex align-items-start gap-3">
          <span class="fs-1 text-danger">⚠️</span>
          <div class="flex-grow-1">
            <div class="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-1">
              <h5 class="fw-bold text-danger mb-0">Assessment Status: FAILED (Not Recommended)</h5>
              <span class="badge bg-danger text-white px-3 py-1 rounded-pill fw-bold">Evaluation Failed</span>
            </div>
            <p class="mb-2 text-dark fs-6 fw-medium">
              This candidate did not clear the pre-screening criteria or achieved a 0% / below-threshold match score.
            </p>
            <div class="p-3 bg-white rounded border border-danger border-opacity-25 mb-3 text-secondary small">
              <strong class="text-dark d-block mb-1 fs-6">💡 How to Fix &amp; Handle This Candidate:</strong>
              <ul class="mb-0 ps-3 style-line-height">
                <li><strong>Option 1 (Recruiter Override):</strong> If candidate has verified offline qualifications, click <strong>"⭐ Save Recruiter Override &amp; Shortlist"</strong> below to override the failure and shortlist them.</li>
                <li><strong>Option 2 (Request Re-Assessment):</strong> Reset or request candidate to re-take the pre-screening questionnaire.</li>
                <li><strong>Option 3 (Confirm Rejection):</strong> Leave status as Rejected to generate candidate feedback report.</li>
              </ul>
            </div>
            ${appId ? `
            <div class="d-flex flex-wrap gap-2">
              <button type="button" class="btn btn-sm btn-success fw-bold px-3 shadow-sm" onclick="window.overrideCandidateStatus && window.overrideCandidateStatus('${appId}', 'shortlisted', 'Recruiter Override from Assessment Breakdown')">
                ⭐ Save Recruiter Override &amp; Shortlist
              </button>
              <button type="button" class="btn btn-sm btn-outline-danger fw-semibold px-3" onclick="window.overrideCandidateStatus && window.overrideCandidateStatus('${appId}', 'rejected', 'Confirmed Rejection from Assessment Breakdown')">
                ❌ Confirm Rejection
              </button>
            </div>
            ` : ''}
          </div>
        </div>
      </div>
    ` : '';

    const result = session?.result || {};
    const techScore = Math.round(result.technical_score ?? (app.skills_match_score || app.ats_score || (isFailed ? 0 : 75)));
    const expScore = Math.round(result.experience_score ?? (app.experience_match_score || app.ats_score || (isFailed ? 0 : 75)));
    const locScore = Math.round(result.location_score ?? (app.location_match_score || (isFailed ? 0 : 80)));
    const availScore = Math.round(result.availability_score ?? (app.availability_score || (isFailed ? 0 : 80)));
    const salScore = Math.round(result.salary_score ?? (app.salary_score || (isFailed ? 0 : 80)));
    const commScore = Math.round(result.communication_score ?? (app.communication_score || (isFailed ? 0 : 85)));

    const aiSummary = result.ai_summary || app.ai_summary || session?.ai_summary || (isFailed ? "Candidate failed evaluation. Does not meet core role qualifications." : "Detailed AI summary available upon completion of all questions.");

    return `
      <!-- Candidate Assessment Banner & Subscore Breakdown -->
      <div class="assessment-breakdown-card mb-4">
        <div class="card border-0 p-4 p-md-5 mb-4 shadow-sm" style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #ffffff; border-radius: 16px;">
          <div class="row align-items-center">
            <div class="col-lg-8">
              <span class="badge bg-primary px-3 py-2 text-uppercase mb-3 fw-bold" style="letter-spacing: 0.05em; font-size: 0.75rem;">${channel}</span>
              <h2 class="fw-bold mb-1 text-white">${escapeHtml(candidateName)}</h2>
              <p class="text-light text-opacity-75 mb-3 fs-5">${escapeHtml(jobTitle)}</p>
              <div class="d-flex flex-wrap gap-3 text-sm text-light text-opacity-90">
                <div>📅 ${formattedDate}</div>
                <div>❓ ${currentQ} / ${totalQ} Questions Answered</div>
                <div>⚡ Status: <span class="fw-bold ${isFailed ? 'text-danger' : 'text-white'}">${statusStr}</span></div>
              </div>
            </div>
            <div class="col-lg-4 text-lg-end mt-4 mt-lg-0">
              <div class="d-inline-block text-center">
                <div class="shadow-sm mb-2" style="background: ${scoreBoxBg}; color: ${scoreBoxColor}; font-size: 2.2rem; font-weight: 800; border-radius: 12px; padding: 12px 28px; display: inline-block;">
                  ${score}%
                </div>
                <div class="fw-bold text-uppercase text-light small" style="letter-spacing: 0.05em;">${recText}</div>
              </div>
            </div>
          </div>
        </div>

        ${failedNoticeHtml}

        <!-- Sub-Score Breakdown Grid -->
        <h5 class="fw-bold mb-3 d-flex align-items-center gap-2 text-dark">
          <span class="text-primary">📈</span> Score Breakdown
        </h5>
        <div class="row g-3 mb-4">
          <div class="col-md-4 col-sm-6">
            <div class="card border p-3 shadow-sm h-100" style="border-radius: 12px; background: #ffffff;">
              <div class="d-flex justify-content-between text-muted small fw-semibold mb-2">
                <span>Technical Skills (30%)</span>
                <span class="text-dark fw-bold">${techScore}%</span>
              </div>
              <div class="progress" style="height: 10px; border-radius: 5px; background-color: #e2e8f0;">
                <div class="progress-bar" style="width: ${techScore}%; background-color: #10b981; border-radius: 5px;"></div>
              </div>
            </div>
          </div>

          <div class="col-md-4 col-sm-6">
            <div class="card border p-3 shadow-sm h-100" style="border-radius: 12px; background: #ffffff;">
              <div class="d-flex justify-content-between text-muted small fw-semibold mb-2">
                <span>Experience Match (20%)</span>
                <span class="text-dark fw-bold">${expScore}%</span>
              </div>
              <div class="progress" style="height: 10px; border-radius: 5px; background-color: #e2e8f0;">
                <div class="progress-bar" style="width: ${expScore}%; background-color: #06b6d4; border-radius: 5px;"></div>
              </div>
            </div>
          </div>

          <div class="col-md-4 col-sm-6">
            <div class="card border p-3 shadow-sm h-100" style="border-radius: 12px; background: #ffffff;">
              <div class="d-flex justify-content-between text-muted small fw-semibold mb-2">
                <span>Location / Work Mode (10%)</span>
                <span class="text-dark fw-bold">${locScore}%</span>
              </div>
              <div class="progress" style="height: 10px; border-radius: 5px; background-color: #e2e8f0;">
                <div class="progress-bar" style="width: ${locScore}%; background-color: #3b82f6; border-radius: 5px;"></div>
              </div>
            </div>
          </div>

          <div class="col-md-4 col-sm-6">
            <div class="card border p-3 shadow-sm h-100" style="border-radius: 12px; background: #ffffff;">
              <div class="d-flex justify-content-between text-muted small fw-semibold mb-2">
                <span>Notice Period / Availability (10%)</span>
                <span class="text-dark fw-bold">${availScore}%</span>
              </div>
              <div class="progress" style="height: 10px; border-radius: 5px; background-color: #e2e8f0;">
                <div class="progress-bar" style="width: ${availScore}%; background-color: #f59e0b; border-radius: 5px;"></div>
              </div>
            </div>
          </div>

          <div class="col-md-4 col-sm-6">
            <div class="card border p-3 shadow-sm h-100" style="border-radius: 12px; background: #ffffff;">
              <div class="d-flex justify-content-between text-muted small fw-semibold mb-2">
                <span>Salary Compatibility (5%)</span>
                <span class="text-dark fw-bold">${salScore}%</span>
              </div>
              <div class="progress" style="height: 10px; border-radius: 5px; background-color: #e2e8f0;">
                <div class="progress-bar" style="width: ${salScore}%; background-color: #6b7280; border-radius: 5px;"></div>
              </div>
            </div>
          </div>

          <div class="col-md-4 col-sm-6">
            <div class="card border p-3 shadow-sm h-100" style="border-radius: 12px; background: #ffffff;">
              <div class="d-flex justify-content-between text-muted small fw-semibold mb-2">
                <span>Communication Quality (5%)</span>
                <span class="text-dark fw-bold">${commScore}%</span>
              </div>
              <div class="progress" style="height: 10px; border-radius: 5px; background-color: #e2e8f0;">
                <div class="progress-bar" style="width: ${commScore}%; background-color: #1f2937; border-radius: 5px;"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- AI Summary Box -->
        <div class="card border-0 shadow-sm mb-4" style="border-radius: 12px; background: #ffffff;">
          <div class="card-body p-4">
            <h5 class="fw-bold mb-3 d-flex align-items-center gap-2 text-dark">
              <span class="text-primary">🤖</span> AI Evaluation Summary
            </h5>
            <div class="text-secondary" style="line-height: 1.6;">
              ${aiSummary.split('\n').map(line => `<p class="mb-1">${escapeHtml(line)}</p>`).join('')}
            </div>
          </div>
        </div>
      </div>
    `;
  }

  async function openApplicantDetail(appId) {
    if (!modalInstance && window.bootstrap) {
      modalInstance = new bootstrap.Modal(modalEl);
    }

    modalBody.innerHTML = `<div class="text-center py-5 text-muted"><div class="spinner-border text-primary mb-2"></div><div>Loading complete candidate profile and ATS match breakdown…</div></div>`;
    if (modalInstance) modalInstance.show();

    try {
      const [res, sessionRes] = await Promise.allSettled([
        applicationsAPI.get(appId),
        screeningAPI.getByApplication(appId)
      ]);

      const app = res.status === "fulfilled" ? res.value.data : {};
      const session = sessionRes.status === "fulfilled" ? (sessionRes.value.data || sessionRes.value) : null;

      const c = app.candidate_profile || {};
      const atsRep = app.ats_report || {};
      const brk = app.breakdown || {};

      modalName.textContent = c.name || app.candidate_name || "Candidate Profile";

      const atsScore = Math.round(app.ats_score || app.match_score || 0);
      const matchScore = Math.round(app.job_match_score || app.match_score || 0);
      const minAtsThreshold = (app.job_details && app.job_details.min_ats_score) || (currentJob && currentJob.min_ats_score) || 60;

      let scoreBadgeClass = "bg-primary";
      if (atsScore >= 80) scoreBadgeClass = "bg-success";
      else if (atsScore >= 60) scoreBadgeClass = "bg-info text-white";
      else if (atsScore >= 40) scoreBadgeClass = "bg-warning text-dark";
      else scoreBadgeClass = "bg-danger";

      // Social links & export
      const socialButtonsHtml = `
        <div class="d-flex flex-wrap gap-2 mt-2">
          ${c.linkedin_url ? `<a href="${c.linkedin_url}" target="_blank" class="social-pill-sm social-linkedin"><span>in</span> LinkedIn</a>` : ''}
          ${c.github_url ? `<a href="${c.github_url}" target="_blank" class="social-pill-sm social-github"><span>💻</span> GitHub</a>` : ''}
          ${c.portfolio_url ? `<a href="${c.portfolio_url}" target="_blank" class="social-pill-sm social-portfolio"><span>🌐</span> Portfolio</a>` : ''}
          <button class="btn btn-sm btn-info text-white fw-semibold export-details-btn px-3 py-1" data-candidate-id="${c.id || app.candidate_id}" data-app-id="${app.id}">
            📄 Export Candidate PDF (.pdf)
          </button>
          <button class="btn btn-sm btn-outline-success fw-semibold download-resume-btn px-3 py-1" data-candidate-id="${c.id || app.candidate_id}">
            ⬇️ Download Resume
          </button>
          <button class="btn btn-sm btn-outline-secondary fw-semibold rescreen-btn px-3 py-1" data-app-id="${app.id}">
            🔄 Re-analyze Resume
          </button>
        </div>
      `;

      // Status Pipeline Controls & Override Banner
      const isBelowThreshold = atsScore < minAtsThreshold;
      const statusPipelineHtml = `
        <div class="card p-3 mb-4 border-0 shadow-sm" style="background: #f8fafc; border-radius: 12px;">
          <div class="d-flex justify-content-between align-items-center flex-wrap gap-3">
            <div>
              <span class="text-muted small fw-semibold">CURRENT APPLICATION STATUS</span>
              <div class="mt-1 d-flex align-items-center gap-2">
                ${getStatusBadge(app.status)}
                ${app.recruiter_override ? `<span class="badge bg-warning text-dark border px-2 py-1 small">Manual Override</span>` : ''}
              </div>
            </div>
            <div class="d-flex flex-wrap gap-2" id="status-action-btn-group">
              <button class="btn btn-sm btn-info text-white fw-semibold update-status-btn" data-status="shortlisted">⭐ Shortlist Candidate</button>
              <button class="btn btn-sm btn-warning text-dark fw-semibold update-status-btn" data-status="interview">🎙️ Schedule Interview</button>
              <button class="btn btn-sm btn-success text-white fw-semibold update-status-btn" data-status="selected">✅ Select Candidate</button>
              <button class="btn btn-sm btn-outline-danger fw-semibold update-status-btn" data-status="rejected">❌ Reject Candidate</button>
            </div>
          </div>
          ${app.override_reason ? `<div class="alert alert-warning py-2 mb-0 mt-3 small"><strong>Recruiter Override Note:</strong> ${app.override_reason}</div>` : ''}
          ${isBelowThreshold ? `<div class="alert alert-info py-2 mb-0 mt-3 small">ℹ️ Note: ATS score (${atsScore}%) is below job threshold (${minAtsThreshold}%). You can still manually shortlist/select this candidate (Recruiter Override).</div>` : ''}
        </div>
      `;

      // Skills Lists
      const matchedSkillsList = app.matched_skills || atsRep.matched_skills || [];
      const missingSkillsList = app.missing_skills || atsRep.missing_skills || [];
      const matchedKeywordsList = app.matched_keywords || atsRep.matched_keywords || [];
      const missingKeywordsList = app.missing_keywords || atsRep.missing_keywords || [];

      const matchedSkillsBadges = matchedSkillsList.map(s => `<span class="badge bg-success-subtle text-success border border-success border-opacity-25 me-1 mb-1">✓ ${s}</span>`).join('') || '<span class="text-muted small">None</span>';
      const missingSkillsBadges = missingSkillsList.map(s => `<span class="badge bg-danger-subtle text-danger border border-danger border-opacity-25 me-1 mb-1">✗ ${s}</span>`).join('') || '<span class="text-success small">None! All required skills matched 🎉</span>';

      const matchedKwBadges = matchedKeywordsList.map(s => `<span class="badge bg-light text-dark border me-1 mb-1">✓ ${s}</span>`).join('') || '<span class="text-muted small">None</span>';
      const missingKwBadges = missingKeywordsList.map(s => `<span class="badge bg-light text-secondary border border-dashed me-1 mb-1">✗ ${s}</span>`).join('') || '<span class="text-muted small">None</span>';

      // Experience & Education Checks
      const candExp = c.experience_years || 0;
      const reqExp = (currentJob && currentJob.experience_required) || 0;
      const expMatched = candExp >= reqExp;

      // Assessment Score Data
      const codingScoreVal = app.coding_score != null ? Math.round(app.coding_score) : null;
      const interviewScoreVal = app.interview_score != null ? Math.round(app.interview_score) : null;
      const overallScoreVal = app.overall_score != null ? Math.round(app.overall_score) : null;

      const codingAttemptId = app.coding_attempt_id || null;
      const interviewId = app.interview_id || null;

      // Score card helper
      function scoreCard(label, value, isHighlighted = false, href = null) {
        const display = value != null ? `${value}%` : `N/A`;
        let cardStyle = isHighlighted
          ? `background: #2f5fff; color: #fff;`
          : `background: #f8fafc; color: #1a1a2e; border: 1px solid #e2e8f0;`;
        if (value != null && isHighlighted === false) {
          if (value >= 80) cardStyle = `background: #1a7a4a; color: #fff;`;
          else if (value >= 60) cardStyle = `background: #0d6efd; color: #fff;`;
          else if (value >= 40) cardStyle = `background: #ffc107; color: #1a1a2e;`;
          else if (value != null) cardStyle = `background: #dc3545; color: #fff;`;
        }
        const inner = `
          <div style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; opacity: 0.85; margin-bottom: 6px;">${label}</div>
          <div style="font-size: 2rem; font-weight: 800; line-height: 1;">${display}</div>
        `;
        if (href) {
          return `<a href="${href}" target="_blank" class="text-decoration-none flex-fill" style="min-width: 120px;">
            <div class="rounded-3 p-3 text-center h-100" style="${cardStyle} transition: opacity .2s;" onmouseover="this.style.opacity='.85'" onmouseout="this.style.opacity='1'">${inner}</div>
          </a>`;
        }
        return `<div class="flex-fill rounded-3 p-3 text-center" style="${cardStyle}; min-width: 120px;">${inner}</div>`;
      }

      const assessmentBannerHtml = `
        <div class="card border-0 shadow-sm p-4 mb-4" style="border-radius: 14px; background: #fff;">
          <div class="d-flex align-items-center justify-content-between mb-3 flex-wrap gap-2">
            <div>
              <h6 class="fw-bold text-dark mb-0">📊 Candidate Score Overview</h6>
              <span class="small text-muted">ATS · Coding Assessment · Interview · Overall</span>
            </div>
            <div class="d-flex gap-2 flex-wrap">
              ${codingAttemptId ? `<a href="integrity-report.html?attempt_id=${codingAttemptId}" target="_blank" class="btn btn-sm btn-outline-info fw-semibold">🛡️ View Coding Report</a>` : ''}
              ${interviewId ? `<a href="interview-scorecard.html?interview_id=${interviewId}" target="_blank" class="btn btn-sm btn-outline-warning fw-semibold">📋 View Interview Scorecard</a>` : ''}
            </div>
          </div>
          <div class="d-flex flex-wrap gap-3">
            ${scoreCard('ATS Score', atsScore, false)}
            ${scoreCard('Coding Score', codingScoreVal, codingScoreVal != null,
              codingAttemptId ? `integrity-report.html?attempt_id=${codingAttemptId}` : null)}
            ${scoreCard('Interview Score', interviewScoreVal, false,
              interviewId ? `interview-scorecard.html?interview_id=${interviewId}` : null)}
            ${scoreCard('Overall Score', overallScoreVal != null ? overallScoreVal : atsScore, false)}
          </div>
          ${codingScoreVal == null && interviewScoreVal == null ? `
            <div class="alert alert-info py-2 mb-0 mt-3 small">
              ℹ️ <strong>Assessment Not Completed:</strong> This candidate has not yet completed the coding assessment or interview for this job.
            </div>` : ''}
        </div>
      `;

      modalBody.innerHTML = `
        ${renderAssessmentHeaderBanner(session, app)}

        ${statusPipelineHtml}

        ${assessmentBannerHtml}

        <div class="row g-4 mb-4">
          <!-- Candidate Profile Left Column -->
          <div class="col-md-6">
            <div class="card border-0 shadow-sm p-4 h-100" style="border-radius: 12px; background: #ffffff;">
              <div class="d-flex align-items-start gap-3 mb-3">
                <img src="${c.profile_photo || `https://ui-avatars.com/api/?name=${encodeURIComponent(c.name || 'Candidate')}&background=2f5fff&color=fff&size=96`}" class="rounded-circle border" style="width: 72px; height: 72px; object-fit: cover;" alt="Avatar" />
                <div>
                  <h4 class="fw-bold text-dark mb-1">${c.name || 'Candidate Name'}</h4>
                  <p class="text-secondary fw-medium mb-1">${c.headline || c.current_role || 'Candidate'}</p>
                  <div class="text-muted small mb-1">📍 ${c.location || 'Not Specified'} • 📧 ${c.email || '—'} • 📞 ${c.phone || '—'}</div>
                  <div class="text-muted small mb-2">💼 <strong>${candExp} Years</strong> Experience</div>
                  <button type="button" class="btn btn-sm btn-outline-primary fw-semibold d-inline-flex align-items-center gap-1" onclick="if(window.openChatWithUser) window.openChatWithUser('${c.user_id}', '${encodeURIComponent(c.name || 'Candidate')}', 'candidate', '${encodeURIComponent(c.headline || '')}');">
                    💬 Direct Message Candidate
                  </button>
                </div>
              </div>

              ${socialButtonsHtml}

              <hr class="my-3" />

              <h6 class="fw-bold text-dark mb-2">About / Candidate Summary</h6>
              <p class="text-secondary small mb-3">${c.summary || c.ai_summary || 'No summary details.'}</p>

              <h6 class="fw-bold text-dark mb-2">Education &amp; Experience History</h6>
              <div class="text-secondary small bg-light p-3 rounded mb-2">
                <strong>Education:</strong> ${c.education || 'Not specified'}
              </div>
              <div class="text-secondary small bg-light p-3 rounded">
                <strong>Work History:</strong> ${c.work_experience || 'Not specified'}
              </div>
            </div>
          </div>

          <!-- ATS Score & Detailed Match Breakdown Right Column -->
          <div class="col-md-6">
            <div class="card border-0 shadow-sm p-4 h-100" style="border-radius: 12px; background: #ffffff;">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <div>
                  <h6 class="fw-bold text-dark mb-0">🎯 ATS Screening Report</h6>
                  <span class="text-secondary small">Status: <strong>${app.screening_status || 'Eligible'}</strong></span>
                </div>
                <div class="text-end">
                  <span class="badge ${scoreBadgeClass} fs-4 px-3 py-1 rounded-pill">${atsScore}% ATS</span>
                  <div class="text-muted small mt-1">Job Match: <strong>${matchScore}%</strong></div>
                </div>
              </div>

              <!-- 100% Sub-Scores Breakdown -->
              <div class="p-3 bg-light rounded-3 mb-3">
                <h6 class="fw-bold small text-dark mb-2">Weighted Score Breakdown (100%)</h6>
                <div class="d-flex justify-content-between small mb-1"><span>Skills Match (30%):</span> <strong>${Math.round(app.skills_match_score || brk.skill_match || 0)}%</strong></div>
                <div class="d-flex justify-content-between small mb-1"><span>Experience Match (20%):</span> <strong>${Math.round(app.experience_match_score || brk.experience_match || 0)}%</strong></div>
                <div class="d-flex justify-content-between small mb-1"><span>Required Keywords (15%):</span> <strong>${Math.round(app.keyword_match_score || 0)}%</strong></div>
                <div class="d-flex justify-content-between small mb-1"><span>Responsibilities Match (15%):</span> <strong>${Math.round(app.responsibility_match_score || brk.semantic_match || 0)}%</strong></div>
                <div class="d-flex justify-content-between small mb-1"><span>Education Match (10%):</span> <strong>${Math.round(app.education_match_score || 100)}%</strong></div>
                <div class="d-flex justify-content-between small mb-1"><span>Location Match (5%):</span> <strong>${Math.round(app.location_match_score || 100)}%</strong></div>
              </div>

              <!-- Requirements Analysis -->
              <div class="mb-3">
                <div class="fw-semibold small text-secondary mb-1">Experience Analysis:</div>
                <div class="small bg-light p-2 rounded">
                  Required: <strong>${reqExp} yrs</strong> | Candidate: <strong>${candExp} yrs</strong>
                  <span class="float-end fw-bold ${expMatched ? 'text-success' : 'text-warning'}">${expMatched ? '✓ Meets requirement' : '⚠️ Below requirement'}</span>
                </div>
              </div>

              <div class="mb-3">
                <div class="fw-semibold small text-success mb-1">Matched Skills:</div>
                <div>${matchedSkillsBadges}</div>
              </div>

              <div class="mb-3">
                <div class="fw-semibold small text-danger mb-1">Missing Skills:</div>
                <div>${missingSkillsBadges}</div>
              </div>

              <div class="mb-3">
                <div class="fw-semibold small text-secondary mb-1">Matched Keywords:</div>
                <div>${matchedKwBadges}</div>
              </div>

              <div class="mb-3">
                <div class="fw-semibold small text-secondary mb-1">Missing Keywords:</div>
                <div>${missingKwBadges}</div>
              </div>

              <div class="p-3 bg-primary-subtle rounded-3 text-primary small mt-auto">
                <strong>💡 Recommendation:</strong> ${app.recommendation || 'Shortlist for Review'}
              </div>
            </div>
          </div>
        </div>
      `;

      // Export Listener inside Modal
      modalBody.querySelectorAll(".export-details-btn").forEach(btn => {
        btn.addEventListener("click", async () => {
          const cid = btn.dataset.candidateId;
          const appId = btn.dataset.appId;
          if (!cid) return;
          btn.disabled = true;
          try {
            await resumesAPI.exportDetails(cid, "pdf", appId);
          } catch (err) {
            alert(`Export failed: ${err.message}`);
          } finally {
            btn.disabled = false;
          }
        });
      });

      // Re-screen Listener inside Modal
      modalBody.querySelectorAll(".rescreen-btn").forEach(btn => {
        btn.addEventListener("click", async () => {
          btn.disabled = true;
          try {
            await applicationsAPI.screen(appId);
            showAlert("Resume re-analyzed successfully!", "success");
            openApplicantDetail(appId);
            loadJobAndApplicants();
          } catch (err) {
            alert(`Re-screen failed: ${err.message}`);
            btn.disabled = false;
          }
        });
      });

      // Status Update Listener inside Modal
      modalBody.querySelectorAll(".update-status-btn").forEach(btn => {
        btn.addEventListener("click", async () => {
          btn.disabled = true;
          const newStatus = btn.dataset.status;
          let overrideReason = null;

          if (isBelowThreshold && (newStatus === "shortlisted" || newStatus === "selected")) {
            const promptReason = prompt(
              `Candidate ATS score (${atsScore}%) is below the minimum job threshold (${minAtsThreshold}%).\n\nPlease enter a reason for overriding the ATS recommendation (optional):`,
              `Recruiter manual shortlist override for ${c.name || 'candidate'}.`
            );
            if (promptReason !== null) {
              overrideReason = promptReason.trim();
            }
          }

          try {
            await applicationsAPI.updateStatus(appId, newStatus, overrideReason);
            showAlert(`Candidate status updated to ${newStatus.replace('_', ' ').toUpperCase()}.`, "success");
            openApplicantDetail(appId);
            loadJobAndApplicants();
          } catch (err) {
            alert(err.message);
            btn.disabled = false;
          }
        });
      });

    } catch (err) {
      modalBody.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
    }
  }

  // Setup Slider & Filter Button & Compare Button Event Listeners
  if (slider) {
    slider.addEventListener("input", (e) => {
      minAtsFilter = Number(e.target.value) || 0;
      if (sliderVal) sliderVal.textContent = `${minAtsFilter}%`;
      applyFilters();
    });
  }

  if (compareSelectedBtn) {
    compareSelectedBtn.addEventListener("click", openCandidateComparison);
  }

  const approveSendBtn = document.getElementById("btn-feedback-approve-send");
  if (approveSendBtn) {
    approveSendBtn.addEventListener("click", async () => {
      if (!activeFeedbackAppId) return;
      const textEl = document.getElementById("feedback-editable-text");
      const overrideText = textEl ? textEl.value : null;

      approveSendBtn.disabled = true;
      approveSendBtn.textContent = "Sending...";
      try {
        await feedbackAPI.approve(activeFeedbackAppId, overrideText);
        showAlert("Candidate feedback approved and sent successfully!", "success");
        if (feedbackModalInstance) feedbackModalInstance.hide();
        loadJobAndApplicants();
      } catch (err) {
        alert(`Failed to approve & send feedback: ${err.message}`);
        approveSendBtn.disabled = false;
        approveSendBtn.textContent = "✅ Approve & Send";
      }
    });
  }

  const regenBtn = document.getElementById("btn-feedback-regenerate");
  if (regenBtn) {
    regenBtn.addEventListener("click", async () => {
      if (!activeFeedbackAppId) return;
      const promptDir = prompt("Enter regeneration focus (e.g. 'more concise', 'more detailed', 'more encouraging', 'focus on skill gaps'):", "more encouraging");
      if (!promptDir) return;

      regenBtn.disabled = true;
      regenBtn.textContent = "Regenerating...";
      try {
        const res = await feedbackAPI.regenerate(activeFeedbackAppId, promptDir);
        const fb = res.data || res;
        renderFeedbackModalContent(fb);
        showAlert("Feedback draft regenerated with new recruiter direction.", "info");
      } catch (err) {
        alert(`Regeneration failed: ${err.message}`);
      } finally {
        regenBtn.disabled = false;
        regenBtn.textContent = "🔄 Regenerate";
      }
    });
  }

  const bulkFbBtn = document.getElementById("bulk-feedback-btn");
  if (bulkFbBtn) {
    bulkFbBtn.addEventListener("click", async () => {
      if (!allApplications.length) return;
      const rejectedApps = allApplications.filter(a => (a.status || "").toLowerCase() === "rejected");
      if (!rejectedApps.length) {
        showAlert("No rejected applications found for bulk feedback generation.", "info");
        return;
      }
      const appIds = rejectedApps.map(a => a.id);
      bulkFbBtn.disabled = true;
      bulkFbBtn.textContent = "Generating...";
      try {
        const res = await feedbackAPI.bulkGenerate(appIds, false);
        const data = res.data || res;
        showAlert(`Bulk candidate feedback generated for ${data.completed || appIds.length} rejected applications!`, "success");
      } catch (err) {
        showAlert(`Bulk feedback failed: ${err.message}`, "danger");
      } finally {
        bulkFbBtn.disabled = false;
        bulkFbBtn.textContent = "💬 Bulk Feedback";
      }
    });
  }

  document.querySelectorAll(".filter-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active", "btn-primary", "btn-success", "btn-warning", "btn-info", "btn-dark", "btn-danger"));
      btn.classList.add("active");
      activeFilter = btn.dataset.filter || "all";
      applyFilters();
    });
  });

  const schedForm = document.getElementById("form-schedule-interview-modal");
  if (schedForm) {
    schedForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const alertEl = document.getElementById("modal-sched-alert");
      const btn = document.getElementById("btn-submit-modal-sched");
      if (alertEl) alertEl.classList.add("d-none");
      btn.disabled = true;
      btn.textContent = "Scheduling...";

      const payload = {
        job_id: document.getElementById("sched-modal-job-id").value,
        candidate_id: document.getElementById("sched-modal-cand-id").value,
        application_id: document.getElementById("sched-modal-app-id").value,
        scheduled_date: document.getElementById("sched-modal-date").value,
        start_time: document.getElementById("sched-modal-time").value,
        duration_minutes: parseInt(document.getElementById("sched-modal-duration").value) || 30,
        timezone: document.getElementById("sched-modal-timezone").value || "Asia/Kolkata",
        send_email: document.getElementById("sched-modal-chk-email").checked,
        sync_calendar: document.getElementById("sched-modal-chk-cal").checked,
      };

      try {
        await scheduledInterviewsAPI.schedule(payload);
        showAlert("Interview scheduled successfully!", "success");
        const modalEl = document.getElementById("scheduleInterviewModal");
        if (window.bootstrap && modalEl) {
          const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
          modal.hide();
        }
        loadJobAndApplicants();
      } catch (err) {
        if (alertEl) {
          alertEl.textContent = err.status === 409 ? (err.message || "An interview already exists during this time.") : err.message;
          alertEl.className = "alert alert-danger py-2 mb-3";
          alertEl.classList.remove("d-none");
        } else {
          showAlert(err.message, "danger");
        }
      } finally {
        btn.disabled = false;
        btn.textContent = "Schedule Interview";
      }
    });
  }

  document.addEventListener("ar:auth-ready", () => {
    loadJobAndApplicants();
  });
})();
