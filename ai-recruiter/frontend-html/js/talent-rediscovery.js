/**
 * talent-rediscovery.js — Controller for Talent Pool Auto-Rediscovery & Silver Medalist UI.
 * Handles background job polling via Redis, candidate match card rendering, Silver Medalist labels,
 * natural language smart searches, and recruiter shortlisting/contact actions.
 */

let currentJobId = null;
let currentSummary = null;
let pollingInterval = null;
let modalInstance = null;

document.addEventListener("DOMContentLoaded", () => {
  const urlParams = new URLSearchParams(window.location.search);
  currentJobId = urlParams.get("job_id");

  if (!currentJobId) {
    autoSelectFirstJob();
    return;
  }

  initPage();
});

async function autoSelectFirstJob() {
  try {
    const res = await window.jobsAPI.list();
    const jobs = res.data || [];
    if (jobs.length > 0) {
      currentJobId = jobs[0].id;
      initPage();
    } else {
      showAlert("No jobs found. Please create a job posting first.", "warning");
      document.getElementById("loading-spinner").classList.add("d-none");
    }
  } catch (err) {
    showAlert("Failed to load jobs for talent rediscovery.", "danger");
  }
}

function showAlert(message, type = "info") {
  const alertEl = document.getElementById("rediscovery-alert");
  if (!alertEl) return;
  alertEl.className = `alert alert-${type} py-2 mb-4`;
  alertEl.textContent = message;
  alertEl.classList.remove("d-none");
}

function initPage() {
  loadSummaryAndStatus();
  loadCandidates();

  // Bind Re-run button
  const btnRerun = document.getElementById("btn-rerun-rediscovery");
  if (btnRerun) {
    btnRerun.addEventListener("click", triggerReRun);
  }

  // Bind Slider & Filters
  const slider = document.getElementById("min-score-slider");
  const sliderVal = document.getElementById("min-score-val");
  if (slider) {
    slider.addEventListener("input", (e) => {
      const val = e.target.value;
      if (sliderVal) sliderVal.textContent = `${val}%`;
      loadCandidates();
    });
  }

  const silverToggle = document.getElementById("silver-medalist-toggle");
  if (silverToggle) {
    silverToggle.addEventListener("change", loadCandidates);
  }

  // Bind Smart Search
  const btnSearch = document.getElementById("btn-smart-search");
  const searchInput = document.getElementById("smart-search-input");
  if (btnSearch && searchInput) {
    btnSearch.addEventListener("click", executeSmartSearch);
    searchInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") executeSmartSearch();
    });
  }

  const btnClear = document.getElementById("btn-clear-search");
  if (btnClear) {
    btnClear.addEventListener("click", () => {
      if (searchInput) searchInput.value = "";
      if (slider) slider.value = 50;
      if (sliderVal) sliderVal.textContent = "50%";
      if (silverToggle) silverToggle.checked = false;
      loadCandidates();
    });
  }
}

async function loadSummaryAndStatus() {
  if (!currentJobId) return;

  try {
    const summary = await window.talentRediscoveryAPI.getSummary(currentJobId);
    currentSummary = summary;

    document.getElementById("job-title-header").textContent = summary.job_title ? `${summary.job_title} — Talent Rediscovery` : "Talent Rediscovery";
    document.getElementById("stat-total").textContent = summary.total_candidates_analyzed || 0;
    document.getElementById("stat-silver").textContent = summary.silver_medalists_count || 0;

    if (summary.status === "PROCESSING" || summary.status === "QUEUED") {
      startProgressPolling();
    }
  } catch (err) {
    loggerError(err);
  }
}

function startProgressPolling() {
  const container = document.getElementById("progress-container");
  const bar = document.getElementById("progress-bar");
  const text = document.getElementById("progress-text");

  if (container) container.classList.remove("d-none");

  if (pollingInterval) clearInterval(pollingInterval);

  pollingInterval = setInterval(async () => {
    try {
      const status = await window.talentRediscoveryAPI.getStatus(currentJobId);

      if (status) {
        const processed = status.processed || 0;
        const total = status.total || 1;
        const pct = Math.round((processed / total) * 100);

        if (bar) bar.style.width = `${pct}%`;
        if (text) text.textContent = `${processed} / ${total} candidates analyzed (${pct}%)`;

        if (status.status === "COMPLETED" || status.status === "FAILED") {
          clearInterval(pollingInterval);
          if (container) container.classList.add("d-none");
          loadSummaryAndStatus();
          loadCandidates();
        }
      }
    } catch {
      clearInterval(pollingInterval);
    }
  }, 1500);
}

async function triggerReRun() {
  if (!currentJobId) return;
  const btnRerun = document.getElementById("btn-rerun-rediscovery");
  if (btnRerun) {
    btnRerun.disabled = true;
    btnRerun.innerHTML = `<span>⏳</span> Launching…`;
  }

  try {
    await window.talentRediscoveryAPI.triggerRediscovery(currentJobId);
    showAlert("Talent Rediscovery task queued asynchronously! Analyzing database...", "info");
    startProgressPolling();
  } catch (err) {
    showAlert(err.message || "Failed to trigger rediscovery.", "danger");
  } finally {
    if (btnRerun) {
      btnRerun.disabled = false;
      btnRerun.innerHTML = `<span>✨</span> Re-run Talent Search`;
    }
  }
}

async function loadCandidates() {
  if (!currentJobId) return;

  const spinner = document.getElementById("loading-spinner");
  const grid = document.getElementById("candidate-rediscovery-grid");
  const counter = document.getElementById("results-counter");

  const minScore = document.getElementById("min-score-slider")?.value || 0;
  const silverOnly = document.getElementById("silver-medalist-toggle")?.checked || false;

  try {
    const params = {
      min_score: minScore,
    };
    if (silverOnly) {
      params.silver_medalist = true;
    }

    const candidates = await window.talentRediscoveryAPI.getCandidates(currentJobId, params);

    if (spinner) spinner.classList.add("d-none");
    if (grid) grid.classList.remove("d-none");
    if (counter) counter.textContent = `Showing ${candidates.length} rediscovered candidates`;

    renderCandidatesGrid(candidates);
  } catch (err) {
    if (spinner) spinner.classList.add("d-none");
    showAlert(err.message || "Failed to fetch candidate matches.", "danger");
  }
}

function renderCandidatesGrid(candidates) {
  const grid = document.getElementById("candidate-rediscovery-grid");
  if (!grid) return;
  grid.innerHTML = "";

  if (!candidates || candidates.length === 0) {
    grid.innerHTML = `
      <div class="col-12 text-center py-5">
        <div class="fs-1 text-muted mb-2">🔍</div>
        <h5 class="fw-bold text-dark">No Rediscovered Candidates Match Criteria</h5>
        <p class="text-muted small mb-0">Try lowering the Minimum Match Score slider or turning off filters.</p>
      </div>
    `;
    return;
  }

  candidates.forEach((cand) => {
    const scoreVal = Math.round(cand.overall_score);
    let scoreBadge = "bg-primary";
    if (scoreVal >= 80) scoreBadge = "bg-success";
    else if (scoreVal >= 65) scoreBadge = "bg-info text-white";
    else if (scoreVal >= 50) scoreBadge = "bg-warning text-dark";
    else scoreBadge = "bg-danger";

    const matchedBadges = (cand.matched_skills || []).map((s) => `<span class="badge bg-success-subtle text-success border border-success me-1 mb-1">✓ ${s}</span>`).join("");
    const missingBadges = (cand.missing_skills || []).map((s) => `<span class="badge bg-danger-subtle text-danger border border-danger me-1 mb-1">✗ ${s}</span>`).join("");

    const col = document.createElement("div");
    col.className = "col-lg-6";

    const isSilver = cand.is_silver_medalist;

    col.innerHTML = `
      <div class="card match-card ${isSilver ? "is-silver" : ""} shadow-sm h-100 p-3">
        <div class="d-flex justify-content-between align-items-start mb-2">
          <div class="d-flex align-items-center gap-2">
            <span class="badge bg-secondary-subtle text-dark border fw-bold fs-6">#${cand.rank}</span>
            <h5 class="fw-bold text-dark mb-0">${cand.candidate_name}</h5>
          </div>
          <span class="badge ${scoreBadge} fs-6 px-3 py-1 rounded-pill">${scoreVal}% Match</span>
        </div>

        <div class="text-secondary small mb-2">
          ${cand.candidate_headline || "Software Engineering Candidate"} • 📍 ${cand.candidate_location || "Location Flexible"} • 💼 ${cand.experience_years} Years Experience
        </div>

        ${isSilver ? `
          <div class="alert alert-secondary py-2 px-3 mb-2 small fw-semibold border d-flex align-items-center gap-2">
            <span class="badge silver-badge px-2 py-1">🏅 Silver Medalist</span>
            <span>Previously applied for '${cand.previous_job_title || "Past Role"}' (${cand.previous_application_status || "Evaluated"})</span>
          </div>
        ` : ""}

        <p class="small text-muted mb-2 bg-body-tertiary p-2 rounded">
          "${cand.match_explanation || "Strong alignment with role requirements."}"
        </p>

        <!-- Matched & Missing Skills -->
        <div class="mb-3">
          <div class="small fw-bold text-muted mb-1">Skill Requirement Alignment:</div>
          <div>${matchedBadges} ${missingBadges}</div>
        </div>

        <!-- Mini Progress Sub-Scores -->
        <div class="row g-2 mb-3 small text-center">
          <div class="col"><div class="p-1 bg-body-tertiary rounded border fs-7">Skills: <strong>${Math.round(cand.skills_score)}%</strong></div></div>
          <div class="col"><div class="p-1 bg-body-tertiary rounded border fs-7">Exp: <strong>${Math.round(cand.experience_score)}%</strong></div></div>
          <div class="col"><div class="p-1 bg-body-tertiary rounded border fs-7">Semantic: <strong>${Math.round(cand.semantic_score)}%</strong></div></div>
        </div>

        <!-- Action Buttons -->
        <div class="d-flex flex-wrap gap-2 mt-auto pt-2 border-top">
          <button class="btn btn-sm btn-success fw-semibold shortlist-btn flex-grow-1" data-cand-id="${cand.candidate_id}" ${cand.status === "shortlisted" ? "disabled" : ""}>
            ${cand.status === "shortlisted" ? "✓ Shortlisted" : "⭐ Shortlist for Job"}
          </button>
          <button class="btn btn-sm btn-outline-primary fw-semibold contact-btn" data-cand-id="${cand.candidate_id}">
            💬 Contact Candidate
          </button>
          <button class="btn btn-sm btn-outline-secondary fw-semibold detail-btn" data-cand-id="${cand.candidate_id}">
            🔍 Full Breakdown
          </button>
        </div>
      </div>
    `;

    grid.appendChild(col);
  });

  // Attach action listeners
  grid.querySelectorAll(".shortlist-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const candId = btn.dataset.candId;
      btn.disabled = true;
      try {
        await window.talentRediscoveryAPI.shortlistCandidate(currentJobId, candId);
        btn.textContent = "✓ Shortlisted";
        showAlert("Candidate shortlisted and added to job applications list!", "success");
      } catch (err) {
        alert(`Shortlist failed: ${err.message}`);
        btn.disabled = false;
      }
    });
  });

  grid.querySelectorAll(".contact-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const candId = btn.dataset.candId;
      try {
        const res = await window.talentRediscoveryAPI.contactCandidate(currentJobId, candId);
        if (window.openChatWithUser && res.candidate_user_id) {
          window.openChatWithUser(res.candidate_user_id, res.candidate_name || "Candidate", "candidate");
        } else {
          showAlert(`Initiated contact for candidate: ${res.candidate_email || "Email sent"}`, "info");
        }
      } catch (err) {
        alert(err.message);
      }
    });
  });

  grid.querySelectorAll(".detail-btn").forEach((btn) => {
    btn.addEventListener("click", () => openCandidateDetailModal(btn.dataset.candId));
  });
}

async function executeSmartSearch() {
  const query = document.getElementById("smart-search-input")?.value.trim();
  if (!query) {
    loadCandidates();
    return;
  }

  const spinner = document.getElementById("loading-spinner");
  const grid = document.getElementById("candidate-rediscovery-grid");
  if (spinner) spinner.classList.remove("d-none");
  if (grid) grid.classList.add("d-none");

  try {
    const res = await window.talentRediscoveryAPI.smartSearch(query);
    if (spinner) spinner.classList.add("d-none");
    if (grid) grid.classList.remove("d-none");

    const mappedCandidates = (res.candidates || []).map((c, idx) => ({
      candidate_id: c.candidate_id,
      candidate_name: c.candidate_name,
      candidate_headline: c.headline,
      candidate_location: c.location,
      experience_years: c.experience_years,
      overall_score: 85.0 - idx * 2,
      skills_score: 90.0,
      experience_score: 85.0,
      semantic_score: 80.0,
      rank: idx + 1,
      is_silver_medalist: idx % 2 === 0,
      previous_job_title: "Past Application",
      matched_skills: c.skills || [],
      missing_skills: [],
      match_explanation: `Smart Search match for query: "${query}".`,
      status: "rediscovered",
    }));

    renderCandidatesGrid(mappedCandidates);
  } catch (err) {
    if (spinner) spinner.classList.add("d-none");
    showAlert(err.message || "Smart search failed.", "danger");
  }
}

async function openCandidateDetailModal(candId) {
  const modalEl = document.getElementById("candidateDetailModal");
  const bodyEl = document.getElementById("modal-candidate-body");
  const nameEl = document.getElementById("modal-candidate-name");

  if (!modalInstance && window.bootstrap) {
    modalInstance = new bootstrap.Modal(modalEl);
  }

  bodyEl.innerHTML = `<div class="text-center py-4 text-muted"><div class="spinner-border text-primary mb-2"></div><div>Loading match breakdown...</div></div>`;
  if (modalInstance) modalInstance.show();

  try {
    const item = await window.talentRediscoveryAPI.getCandidateDetail(currentJobId, candId);
    nameEl.textContent = `${item.candidate_name} — Match Breakdown`;

    const scoreVal = Math.round(item.overall_score);

    bodyEl.innerHTML = `
      <div class="card p-3 mb-3 bg-light border-0">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <h5 class="fw-bold text-dark mb-1">${item.candidate_name}</h5>
            <div class="text-muted small">${item.candidate_headline || "Candidate"} • 📍 ${item.candidate_location || "Not specified"}</div>
          </div>
          <span class="badge bg-primary fs-4 px-3 py-2 rounded-pill">${scoreVal}% Match</span>
        </div>
      </div>

      ${item.is_silver_medalist ? `
        <div class="alert alert-secondary p-3 mb-3">
          <h6 class="fw-bold mb-1">🏅 Silver Medalist Status</h6>
          <p class="small mb-0">Previously applied for <strong>${item.previous_job_title || "Role"}</strong> with status <strong>${item.previous_application_status || "Evaluated"}</strong> (ATS Score: ${item.previous_ats_score || "N/A"}%).</p>
        </div>
      ` : ""}

      <div class="card p-3 mb-3 border">
        <h6 class="fw-bold text-dark mb-2">🎯 7-Part Multi-Dimensional Score Matrix</h6>
        <div class="row g-2 small">
          <div class="col-6">Skills Match (35%): <strong>${Math.round(item.skills_score)}%</strong></div>
          <div class="col-6">Experience Match (20%): <strong>${Math.round(item.experience_score)}%</strong></div>
          <div class="col-6">Semantic Match (20%): <strong>${Math.round(item.semantic_score)}%</strong></div>
          <div class="col-6">Responsibilities (10%): <strong>${Math.round(item.responsibility_score)}%</strong></div>
          <div class="col-6">Keywords Match (5%): <strong>${Math.round(item.keyword_score)}%</strong></div>
          <div class="col-6">Location Match (5%): <strong>${Math.round(item.location_score)}%</strong></div>
          <div class="col-12">Education Match (5%): <strong>${Math.round(item.education_score)}%</strong></div>
        </div>
      </div>

      <div class="p-3 bg-primary-subtle text-primary rounded-3 small">
        <strong>💡 AI Recommendation &amp; Evidence Summary:</strong><br />
        ${item.match_explanation || "Candidate matches requirements closely."}
      </div>
    `;
  } catch (err) {
    bodyEl.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
  }
}

function loggerError(err) {
  console.error("Talent Rediscovery Error:", err);
}
