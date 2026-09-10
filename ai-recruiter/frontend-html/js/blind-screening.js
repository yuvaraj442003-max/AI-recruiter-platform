/**
 * blind-screening.js — Frontend Controller for Blind Screening Mode.
 * Renders server-side anonymized candidate cards (CAND-10452), sanitized resume preview,
 * recruiter decision actions, and controlled identity reveal with audit logging.
 */

let currentJobId = null;
let currentConfig = null;
let candidatesData = [];
let pendingRevealCandidateCode = null;
let revealModalInstance = null;
let resumeModalInstance = null;

document.addEventListener("DOMContentLoaded", () => {
  const urlParams = new URLSearchParams(window.location.search);
  currentJobId = urlParams.get("job_id");

  if (!currentJobId) {
    showAlert("No job specified. Please select a job posting.", "danger");
    autoSelectFirstJob();
    return;
  }

  // Update back link
  const backLink = document.getElementById("back-link");
  if (backLink && currentJobId) {
    backLink.href = `job-applicants.html?job_id=${currentJobId}`;
  }

  initBlindScreening();
});

async function autoSelectFirstJob() {
  try {
    const res = await window.jobsAPI.list();
    const jobs = res.data || [];
    if (jobs.length > 0) {
      currentJobId = jobs[0].id;
      initBlindScreening();
    }
  } catch (err) {
    loggerError(err);
  }
}

function showAlert(message, type = "info") {
  const alertEl = document.getElementById("blind-alert");
  if (!alertEl) return;
  alertEl.className = `alert alert-${type} py-2 mb-4`;
  alertEl.textContent = message;
  alertEl.classList.remove("d-none");
}

function hideAlert() {
  const alertEl = document.getElementById("blind-alert");
  if (alertEl) {
    alertEl.classList.add("d-none");
  }
}

async function initBlindScreening() {
  hideAlert();
  await loadConfig();
  await loadCandidates();
  await loadStatistics();

  // Bind Toggle
  const toggle = document.getElementById("blind-mode-toggle");
  const toggleStatus = document.getElementById("toggle-status-text");
  if (toggle) {
    toggle.addEventListener("change", async () => {
      const enabled = toggle.checked;
      if (toggleStatus) {
        toggleStatus.textContent = enabled ? "ON" : "OFF";
        toggleStatus.className = enabled ? "text-success" : "text-danger";
      }

      try {
        await window.blindScreeningAPI.updateConfig(currentJobId, { enabled: enabled });
        if (!enabled) {
          if (confirm("Blind Screening Mode disabled. Would you like to switch to standard Job Applicants view?")) {
            window.location.href = `job-applicants.html?job_id=${currentJobId}`;
          }
        }
      } catch (err) {
        showAlert(err.message || "Failed to update configuration.", "danger");
      }
    });
  }

  // Bind Slider & Search
  const slider = document.getElementById("ats-score-slider");
  const sliderVal = document.getElementById("ats-score-val");
  if (slider) {
    slider.addEventListener("input", (e) => {
      if (sliderVal) sliderVal.textContent = `${e.target.value}%`;
      filterAndRenderCandidates();
    });
  }

  const searchInput = document.getElementById("skill-search-input");
  if (searchInput) {
    searchInput.addEventListener("input", filterAndRenderCandidates);
  }

  // Bind Reveal Confirm Button
  const btnConfirmReveal = document.getElementById("btn-confirm-reveal");
  if (btnConfirmReveal) {
    btnConfirmReveal.addEventListener("click", executeIdentityReveal);
  }
}

async function loadConfig() {
  try {
    const config = await window.blindScreeningAPI.getConfig(currentJobId);
    currentConfig = config;

    const toggle = document.getElementById("blind-mode-toggle");
    const toggleStatus = document.getElementById("toggle-status-text");

    if (toggle) toggle.checked = config.enabled;
    if (toggleStatus) {
      toggleStatus.textContent = config.enabled ? "ON" : "OFF";
      toggleStatus.className = config.enabled ? "text-success" : "text-danger";
    }
  } catch (err) {
    loggerError(err);
  }
}

async function loadStatistics() {
  try {
    const stats = await window.blindScreeningAPI.getStatistics(currentJobId);
    document.getElementById("job-title-header").textContent = stats.job_title ? `${stats.job_title} — Blind Screening` : "Blind Screening";
    document.getElementById("stat-total").textContent = stats.total_candidates || 0;
    document.getElementById("stat-shortlisted").textContent = stats.shortlisted_count || 0;
    document.getElementById("stat-revealed").textContent = stats.revealed_count || 0;
  } catch (err) {
    loggerError(err);
  }
}

async function loadCandidates() {
  const spinner = document.getElementById("loading-spinner");
  const grid = document.getElementById("blind-candidates-grid");

  try {
    const candidates = await window.blindScreeningAPI.getCandidates(currentJobId);
    candidatesData = candidates;

    if (spinner) spinner.classList.add("d-none");
    if (grid) grid.classList.remove("d-none");

    filterAndRenderCandidates();
  } catch (err) {
    if (spinner) spinner.classList.add("d-none");
    showAlert(err.message || "Failed to load anonymized candidates.", "danger");
  }
}

function filterAndRenderCandidates() {
  const minAts = Number(document.getElementById("ats-score-slider")?.value || 0);
  const search = (document.getElementById("skill-search-input")?.value || "").toLowerCase().trim();

  let filtered = candidatesData.filter((c) => {
    if (c.ats_score < minAts) return false;

    if (search) {
      const skillsStr = (c.skills || []).join(" ").toLowerCase();
      const matchedStr = (c.matched_skills || []).join(" ").toLowerCase();
      const eduStr = (c.education || []).map((e) => e.degree + " " + e.field).join(" ").toLowerCase();
      const codeStr = c.candidate_code.toLowerCase();

      return skillsStr.includes(search) || matchedStr.includes(search) || eduStr.includes(search) || codeStr.includes(search);
    }
    return true;
  });

  document.getElementById("results-count-badge").textContent = `${filtered.length} Anonymized Candidates`;
  renderGrid(filtered);
}

function renderGrid(candidates) {
  const grid = document.getElementById("blind-candidates-grid");
  if (!grid) return;
  grid.innerHTML = "";

  if (!candidates || candidates.length === 0) {
    grid.innerHTML = `
      <div class="col-12 text-center py-5">
        <div class="fs-1 text-muted mb-2">🙈</div>
        <h5 class="fw-bold text-dark">No Anonymized Candidates Match Criteria</h5>
        <p class="text-muted small mb-0">Try lowering the Minimum ATS Score slider or clearing filters.</p>
      </div>
    `;
    return;
  }

  candidates.forEach((cand) => {
    const atsScore = Math.round(cand.ats_score);
    let atsBadge = "bg-primary";
    if (atsScore >= 80) atsBadge = "bg-success";
    else if (atsScore >= 60) atsBadge = "bg-info text-white";
    else if (atsScore >= 40) atsBadge = "bg-warning text-dark";
    else atsBadge = "bg-danger";

    const matchedBadges = (cand.matched_skills || []).map((s) => `<span class="badge bg-success-subtle text-success border border-success me-1 mb-1">✓ ${s}</span>`).join("");
    const missingBadges = (cand.missing_skills || []).map((s) => `<span class="badge bg-danger-subtle text-danger border border-danger me-1 mb-1">✗ ${s}</span>`).join("");

    const eduBadges = (cand.education || []).map((e) => `<span class="badge bg-light text-dark border me-1">${e.degree} — ${e.field}</span>`).join("");

    const col = document.createElement("div");
    col.className = "col-lg-6";

    col.innerHTML = `
      <div class="card candidate-blind-card ${cand.revealed ? "is-revealed" : ""} shadow-sm h-100 p-3">
        <div class="d-flex justify-content-between align-items-start mb-2">
          <div class="d-flex align-items-center gap-2">
            <span class="blind-code-badge">${cand.candidate_code}</span>
            ${cand.revealed ? '<span class="badge bg-success-subtle text-success border">Identity Revealed</span>' : '<span class="badge bg-secondary-subtle text-secondary border">Anonymized</span>'}
          </div>
          <span class="badge ${atsBadge} fs-6 px-3 py-1 rounded-pill">${atsScore}% ATS</span>
        </div>

        <div class="text-secondary small mb-2">
          💼 <strong>${cand.experience_years} Years</strong> Experience • Role Match: <strong>${Math.round(cand.role_match_score)}%</strong>
          ${cand.technical_assessment_score !== null ? ` • Assessment: <strong>${Math.round(cand.technical_assessment_score)}%</strong>` : ""}
        </div>

        <!-- Qualifications / Education -->
        <div class="mb-2">
          <div class="small fw-bold text-muted mb-1">Qualifications:</div>
          <div>${eduBadges || '<span class="small text-muted">Higher Education</span>'}</div>
        </div>

        <!-- Matched & Missing Skills -->
        <div class="mb-3">
          <div class="small fw-bold text-muted mb-1">Matched Skills:</div>
          <div>${matchedBadges} ${missingBadges}</div>
        </div>

        <!-- Decision Status Banner if set -->
        ${cand.recruiter_decision ? `
          <div class="alert alert-light border py-1 px-2 mb-3 small">
            Current Decision: <strong class="text-uppercase text-primary">${cand.recruiter_decision}</strong>
          </div>
        ` : ""}

        <!-- Action Buttons -->
        <div class="d-flex flex-wrap gap-2 mt-auto pt-2 border-top">
          <button class="btn btn-sm btn-success fw-semibold btn-decision" data-code="${cand.candidate_code}" data-decision="shortlist">
            ⭐ Shortlist
          </button>
          <button class="btn btn-sm btn-outline-warning fw-semibold btn-decision" data-code="${cand.candidate_code}" data-decision="hold">
            ⏸️ Hold
          </button>
          <button class="btn btn-sm btn-outline-danger fw-semibold btn-decision" data-code="${cand.candidate_code}" data-decision="reject">
            ❌ Reject
          </button>
          <button class="btn btn-sm btn-outline-primary fw-semibold btn-resume-view" data-code="${cand.candidate_code}">
            📄 Sanitized Resume
          </button>
          ${!cand.revealed ? `
            <button class="btn btn-sm btn-outline-dark fw-semibold btn-reveal-modal ms-auto" data-code="${cand.candidate_code}">
              🔓 Reveal Identity
            </button>
          ` : ""}
        </div>
      </div>
    `;

    grid.appendChild(col);
  });

  // Attach button event listeners
  grid.querySelectorAll(".btn-decision").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const code = btn.dataset.code;
      const dec = btn.dataset.decision;
      btn.disabled = true;

      try {
        const res = await window.blindScreeningAPI.saveDecision(currentJobId, code, dec);
        showAlert(`Recorded decision '${dec}' for ${code}.`, "success");
        loadCandidates();
        loadStatistics();
      } catch (err) {
        alert(`Decision error: ${err.message}`);
        btn.disabled = false;
      }
    });
  });

  grid.querySelectorAll(".btn-resume-view").forEach((btn) => {
    btn.addEventListener("click", () => openSanitizedResumeModal(btn.dataset.code));
  });

  grid.querySelectorAll(".btn-reveal-modal").forEach((btn) => {
    btn.addEventListener("click", () => openRevealConfirmModal(btn.dataset.code));
  });
}

async function openSanitizedResumeModal(code) {
  const modalEl = document.getElementById("sanitizedResumeModal");
  const titleEl = document.getElementById("modal-resume-title");
  const contentEl = document.getElementById("sanitized-resume-content");

  if (!resumeModalInstance && window.bootstrap) {
    resumeModalInstance = new bootstrap.Modal(modalEl);
  }

  titleEl.textContent = `${code} — Blind Resume Representation`;
  contentEl.textContent = "Loading sanitized resume representation...";
  if (resumeModalInstance) resumeModalInstance.show();

  try {
    const detail = await window.blindScreeningAPI.getCandidateDetail(currentJobId, code);
    contentEl.textContent = detail.sanitized_resume_text || "No resume text content available.";
  } catch (err) {
    contentEl.textContent = `Error loading sanitized resume: ${err.message}`;
  }
}

function openRevealConfirmModal(code) {
  pendingRevealCandidateCode = code;

  const modalEl = document.getElementById("revealConfirmModal");
  const codeEl = document.getElementById("reveal-candidate-code");
  if (codeEl) codeEl.textContent = code;

  if (!revealModalInstance && window.bootstrap) {
    revealModalInstance = new bootstrap.Modal(modalEl);
  }

  if (revealModalInstance) revealModalInstance.show();
}

async function executeIdentityReveal() {
  if (!pendingRevealCandidateCode) return;

  const code = pendingRevealCandidateCode;
  const btn = document.getElementById("btn-confirm-reveal");
  if (btn) {
    btn.disabled = true;
    btn.textContent = "Unlocking...";
  }

  try {
    const res = await window.blindScreeningAPI.revealCandidate(currentJobId, code);
    if (revealModalInstance) revealModalInstance.hide();

    alert(`Candidate Identity Revealed:\n\nName: ${res.name}\nEmail: ${res.email || "N/A"}\nPhone: ${res.phone || "N/A"}\nLocation: ${res.location || "N/A"}`);

    loadCandidates();
    loadStatistics();
  } catch (err) {
    alert(`Failed to reveal candidate: ${err.message}`);
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = "Unlock & Reveal Identity";
    }
  }
}

function loggerError(err) {
  console.error("Blind Screening Error:", err);
}
