/**
 * smart-search.js — Smart Candidate Search Engine UI Logic.
 *
 * Handles natural language query parsing, structured multi-criteria filtering,
 * weighted candidate ranking, pagination, and Candidate Comparison integration.
 */
(function () {
  const alertBox = document.getElementById("search-alert");
  const searchForm = document.getElementById("smart-search-form");
  const queryInput = document.getElementById("search-query-input");
  const btnParse = document.getElementById("btn-parse-query");
  const btnReset = document.getElementById("btn-reset-filters");

  const filterSkills = document.getElementById("filter-skills");
  const filterJobId = document.getElementById("filter-job-id");
  const filterMinExp = document.getElementById("filter-min-exp");
  const filterLocation = document.getElementById("filter-location");
  const filterMinAts = document.getElementById("filter-min-ats");
  const atsValBadge = document.getElementById("ats-val-badge");
  const filterJobRole = document.getElementById("filter-job-role");
  const filterMinInterview = document.getElementById("filter-min-interview");

  const sortBySelect = document.getElementById("sort-by-select");
  const resultsContainer = document.getElementById("search-results-container");
  const totalBadge = document.getElementById("search-total-badge");
  const compareSelectedBtn = document.getElementById("compare-selected-btn");
  const compareCountBadge = document.getElementById("compare-count-badge");
  const paginationInfo = document.getElementById("pagination-info");
  const paginationControls = document.getElementById("pagination-controls");

  const compModalEl = document.getElementById("candidateComparisonModal");
  const compModalBody = document.getElementById("comparison-modal-body");
  const compModalTitle = document.getElementById("comparison-modal-title");
  const compModalSubtitle = document.getElementById("comparison-modal-subtitle");

  let currentPage = 1;
  const pageSize = 12;
  const selectedCandidateIds = new Set();
  let compModalInstance = null;

  function showAlert(msg, variant = "danger") {
    if (!alertBox) return;
    alertBox.textContent = msg;
    alertBox.className = `alert alert-${variant} py-2 mb-3`;
    alertBox.classList.remove("d-none");
    setTimeout(() => alertBox.classList.add("d-none"), 4000);
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

  async function loadJobsDropdown() {
    try {
      const res = await jobsAPI.list();
      const jobs = res.data || [];
      if (filterJobId) {
        filterJobId.innerHTML = '<option value="">All Jobs (Baseline Evaluation)</option>' +
          jobs.map(j => `<option value="${j.id}">${j.title} (${j.department || 'General'})</option>`).join('');
      }
    } catch {
      // Ignore if jobs fail to load
    }
  }

  async function executeSmartSearch() {
    resultsContainer.innerHTML = `
      <div class="col-12 text-center py-5 text-muted">
        <div class="spinner-border text-success mb-2" style="width: 2.5rem; height: 2.5rem;"></div>
        <h6 class="fw-bold text-dark">Searching Candidate Database...</h6>
        <p class="small text-secondary mb-0">Applying skill normalization, experience bounds, and weighted candidate ranking.</p>
      </div>
    `;

    const queryStr = queryInput ? queryInput.value.trim() : "";
    const skillsStr = filterSkills ? filterSkills.value.trim() : "";
    const skillList = skillsStr ? skillsStr.split(",").map(s => s.trim()).filter(Boolean) : [];

    const matchMode = document.querySelector('input[name="skill-match-mode"]:checked')?.value || "all";
    const jobIdVal = filterJobId ? filterJobId.value : null;

    const minExpVal = filterMinExp && filterMinExp.value ? Number(filterMinExp.value) : null;
    const locVal = filterLocation && filterLocation.value.trim() ? filterLocation.value.trim() : null;
    const minAtsVal = filterMinAts && Number(filterMinAts.value) > 0 ? Number(filterMinAts.value) : null;
    const jobRoleVal = filterJobRole && filterJobRole.value.trim() ? filterJobRole.value.trim() : null;
    const minInterviewVal = filterMinInterview && filterMinInterview.value ? Number(filterMinInterview.value) : null;
    const sortBy = sortBySelect ? sortBySelect.value : "best_match";

    const payload = {
      query: queryStr,
      job_id: jobIdVal || null,
      filters: {
        skills: skillList,
        skill_match_mode: matchMode,
        minimum_experience: minExpVal,
        location: locVal,
        minimum_ats_score: minAtsVal,
        job_role: jobRoleVal,
        minimum_interview_score: minInterviewVal,
      },
      page: currentPage,
      page_size: pageSize,
      sort_by: sortBy,
    };

    try {
      const res = await candidateSearchAPI.smartSearch(payload);
      const data = res.data;
      renderCandidateResults(data);
      renderPagination(data);
    } catch (err) {
      resultsContainer.innerHTML = `
        <div class="col-12">
          <div class="alert alert-danger p-4">
            <strong>Unable to Search Candidates:</strong> ${err.message}
          </div>
        </div>
      `;
    }
  }

  function renderCandidateResults(data) {
    const results = data.results || [];
    const total = data.total_results || 0;

    if (totalBadge) totalBadge.textContent = `${total} Candidate${total !== 1 ? 's' : ''}`;

    if (!results.length) {
      resultsContainer.innerHTML = `
        <div class="col-12 text-center py-5">
          <div class="fs-1 text-muted mb-2">🔍</div>
          <h5 class="fw-bold text-dark">No candidates found matching your criteria</h5>
          <p class="text-secondary small mb-3">Try lowering the Minimum ATS Score, clearing skill filters, or switching to "Any Skill" match mode.</p>
          <button id="empty-reset-btn" class="btn btn-sm btn-outline-success px-4 fw-semibold">Reset Search Filters</button>
        </div>
      `;
      document.getElementById("empty-reset-btn")?.addEventListener("click", resetFilters);
      return;
    }

    resultsContainer.innerHTML = results.map((c, idx) => {
      const globalRank = (data.page - 1) * data.page_size + idx + 1;
      let rankClass = "rank-badge-other";
      let rankLabel = `#${globalRank}`;
      if (globalRank === 1) { rankClass = "rank-badge-1"; rankLabel = "🥇 #1 Rank"; }
      else if (globalRank === 2) { rankClass = "rank-badge-2"; rankLabel = "🥈 #2 Rank"; }
      else if (globalRank === 3) { rankClass = "rank-badge-3"; rankLabel = "🥉 #3 Rank"; }

      const isChecked = selectedCandidateIds.has(c.candidate_id) ? "checked" : "";
      const matchedBadges = (c.matched_skills || []).map(s => `<span class="badge bg-success-subtle text-success border border-success border-opacity-25 me-1 mb-1">✓ ${s}</span>`).join("") || '<span class="text-muted small">None</span>';
      const missingBadges = (c.missing_skills || []).map(s => `<span class="badge bg-danger-subtle text-danger border border-danger border-opacity-25 me-1 mb-1">⚠ ${s}</span>`).join("");

      const atsScore = Math.round(c.ats_score || 0);
      let atsBadgeClass = "bg-primary";
      if (atsScore >= 80) atsBadgeClass = "bg-success";
      else if (atsScore >= 60) atsBadgeClass = "bg-info text-white";
      else if (atsScore >= 40) atsBadgeClass = "bg-warning text-dark";
      else atsBadgeClass = "bg-danger";

      const interviewText = c.interview_score != null ? `${Math.round(c.interview_score)}/100` : "Not Interviewed";

      return `
        <div class="col-md-6 col-lg-4">
          <div class="card border-0 shadow-sm h-100 p-3" style="border-radius: 12px; background: #ffffff;">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <span class="badge ${rankClass} px-3 py-1 rounded-pill">${rankLabel}</span>
              <div class="form-check mb-0">
                <input type="checkbox" class="form-check-input candidate-select-checkbox cursor-pointer" data-candidate-id="${c.candidate_id}" data-name="${c.candidate_name}" ${isChecked} />
                <label class="form-check-label small text-muted">Select</label>
              </div>
            </div>

            <h5 class="fw-bold text-dark mb-1">${c.candidate_name}</h5>
            <p class="text-secondary small fw-medium mb-2">${c.headline || c.job_role}</p>

            <div class="text-muted small mb-2">
              📍 ${c.location} • 💼 <strong>${c.experience_years} Yrs</strong> Exp
            </div>

            <div class="p-2 bg-light rounded-3 mb-3">
              <div class="d-flex justify-content-between align-items-center mb-1">
                <span class="small text-muted fw-semibold">ATS Match Score:</span>
                <span class="badge ${atsBadgeClass} fs-6 px-3 py-1 rounded-pill">${atsScore}%</span>
              </div>
              <div class="d-flex justify-content-between align-items-center small">
                <span class="text-muted">Interview Performance:</span>
                <strong>${interviewText}</strong>
              </div>
              <div class="d-flex justify-content-between align-items-center small mt-1">
                <span class="text-muted">Weighted Rank Score:</span>
                <strong class="text-success">${Math.round(c.ranking_score)}/100</strong>
              </div>
            </div>

            <div class="mb-2">
              <div class="small fw-semibold text-success mb-1">Matched Skills:</div>
              <div>${matchedBadges}</div>
            </div>

            ${missingBadges ? `
              <div class="mb-3">
                <div class="small fw-semibold text-danger mb-1">Missing Requested Skills:</div>
                <div>${missingBadges}</div>
              </div>
            ` : ''}

            <div class="mt-auto border-top pt-2 d-flex justify-content-between align-items-center">
              <button class="btn btn-sm btn-outline-primary fw-semibold view-cand-profile-btn" data-candidate-id="${c.candidate_id}">
                👤 View Profile
              </button>
              <button class="btn btn-sm btn-outline-secondary fw-semibold" onclick="if(window.openChatWithUser) window.openChatWithUser('${c.user_id || c.candidate_id}', '${encodeURIComponent(c.candidate_name)}', 'candidate', '${encodeURIComponent(c.headline || '')}');">
                💬 Chat
              </button>
            </div>
          </div>
        </div>
      `;
    }).join("");

    // Attach Selection Checkbox Listeners
    resultsContainer.querySelectorAll(".candidate-select-checkbox").forEach(chk => {
      chk.addEventListener("change", (e) => {
        const candId = e.target.dataset.candidateId;
        if (e.target.checked) {
          if (selectedCandidateIds.size >= 5) {
            e.target.checked = false;
            showAlert("You can select a maximum of 5 candidates for side-by-side comparison.", "warning");
            return;
          }
          selectedCandidateIds.add(candId);
        } else {
          selectedCandidateIds.delete(candId);
        }
        updateCompareButtonState();
      });
    });

    // Attach View Profile Listeners
    resultsContainer.querySelectorAll(".view-cand-profile-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const candId = btn.dataset.candidateId;
        if (candId && window.openApplicantDetailModal) {
          window.openApplicantDetailModal(candId);
        } else {
          alert(`Candidate ID: ${candId}`);
        }
      });
    });
  }

  function renderPagination(data) {
    const total = data.total_results || 0;
    const cur = data.page || 1;
    const totalP = data.total_pages || 1;

    const startIdx = total === 0 ? 0 : (cur - 1) * data.page_size + 1;
    const endIdx = Math.min(cur * data.page_size, total);

    if (paginationInfo) paginationInfo.textContent = `Showing ${startIdx}–${endIdx} of ${total} candidates`;

    if (!paginationControls) return;
    paginationControls.innerHTML = "";

    if (totalP <= 1) return;

    // Previous Button
    const prevLi = document.createElement("li");
    prevLi.className = `page-item ${cur === 1 ? 'disabled' : ''}`;
    prevLi.innerHTML = `<a class="page-link" href="#">&laquo; Prev</a>`;
    prevLi.addEventListener("click", (e) => {
      e.preventDefault();
      if (cur > 1) { currentPage = cur - 1; executeSmartSearch(); }
    });
    paginationControls.appendChild(prevLi);

    // Page Numbers
    for (let i = 1; i <= totalP; i++) {
      const li = document.createElement("li");
      li.className = `page-item ${i === cur ? 'active' : ''}`;
      li.innerHTML = `<a class="page-link" href="#">${i}</a>`;
      li.addEventListener("click", (e) => {
        e.preventDefault();
        currentPage = i;
        executeSmartSearch();
      });
      paginationControls.appendChild(li);
    }

    // Next Button
    const nextLi = document.createElement("li");
    nextLi.className = `page-item ${cur === totalP ? 'disabled' : ''}`;
    nextLi.innerHTML = `<a class="page-link" href="#">Next &raquo;</a>`;
    nextLi.addEventListener("click", (e) => {
      e.preventDefault();
      if (cur < totalP) { currentPage = cur + 1; executeSmartSearch(); }
    });
    paginationControls.appendChild(nextLi);
  }

  async function autoFillFiltersFromQuery() {
    const q = queryInput ? queryInput.value.trim() : "";
    if (!q) {
      showAlert("Please enter a natural language search query first.", "warning");
      return;
    }

    if (btnParse) {
      btnParse.disabled = true;
      btnParse.textContent = "Parsing...";
    }

    try {
      const res = await candidateSearchAPI.parseQuery(q);
      const data = res.data;

      if (filterSkills && data.skills && data.skills.length) {
        filterSkills.value = data.skills.join(", ");
      }
      if (filterMinExp && data.minimum_experience != null) {
        filterMinExp.value = data.minimum_experience;
      }
      if (filterLocation && data.location) {
        filterLocation.value = data.location;
      }
      if (filterMinAts && data.minimum_ats_score != null) {
        filterMinAts.value = data.minimum_ats_score;
        if (atsValBadge) atsValBadge.textContent = `${data.minimum_ats_score}%`;
      }
      if (filterJobRole && data.job_role) {
        filterJobRole.value = data.job_role;
      }

      showAlert("Filters auto-extracted from natural language query!", "success");
      currentPage = 1;
      executeSmartSearch();
    } catch (err) {
      showAlert(`Query parsing error: ${err.message}`, "danger");
    } finally {
      if (btnParse) {
        btnParse.disabled = false;
        btnParse.textContent = "🤖 Auto-Fill Filters";
      }
    }
  }

  function resetFilters() {
    if (queryInput) queryInput.value = "";
    if (filterSkills) filterSkills.value = "";
    if (filterJobId) filterJobId.value = "";
    if (filterMinExp) filterMinExp.value = "";
    if (filterLocation) filterLocation.value = "";
    if (filterMinAts) { filterMinAts.value = "0"; if (atsValBadge) atsValBadge.textContent = "0%"; }
    if (filterJobRole) filterJobRole.value = "";
    if (filterMinInterview) filterMinInterview.value = "";
    if (sortBySelect) sortBySelect.value = "best_match";
    const allRadio = document.getElementById("match-all");
    if (allRadio) allRadio.checked = true;

    selectedCandidateIds.clear();
    updateCompareButtonState();
    currentPage = 1;
    executeSmartSearch();
  }

  async function openCandidateComparison() {
    const count = selectedCandidateIds.size;
    if (count < 2 || count > 5) {
      showAlert("Please select between 2 and 5 candidates for side-by-side comparison.", "warning");
      return;
    }

    if (!compModalInstance && window.bootstrap && compModalEl) {
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
      const jobIdVal = filterJobId ? filterJobId.value : null;

      const res = await comparisonAPI.compare(jobIdVal || "00000000-0000-0000-0000-000000000001", candidateIdList);
      const compData = res.data;

      compModalTitle.textContent = `Candidate Side-by-Side Comparison — ${compData.job_title || 'Smart Search Comparison'}`;
      compModalSubtitle.textContent = `Comparing ${compData.candidates.length} Selected Candidates`;

      renderComparisonModalContent(compData);
    } catch (err) {
      compModalBody.innerHTML = `<div class="alert alert-danger p-4"><strong>Comparison Failed:</strong> ${err.message}</div>`;
    }
  }

  function renderComparisonModalContent(data) {
    const candidates = data.candidates || [];
    const recommendedCand = data.recommended_candidate || "Candidate";

    const candHeaders = candidates.map(c => `
      <th style="width: ${Math.floor(80 / candidates.length)}%;" class="text-center border-start py-3">
        <div class="fw-bold fs-5 text-dark mb-1">${c.name}</div>
        <div class="text-muted small mb-2">${c.headline || 'Candidate'}</div>
        <span class="badge bg-primary-subtle text-primary border px-3 py-1 rounded-pill mb-2">${c.email || '—'}</span>
      </th>
    `).join("");

    const infoRoleRow = candidates.map(c => `<td class="border-start small text-center fw-semibold text-secondary">${c.headline || '—'}</td>`).join("");
    const infoLocRow = candidates.map(c => `<td class="border-start small text-center text-muted">📍 ${c.location}</td>`).join("");
    const infoExpRow = candidates.map(c => `<td class="border-start small text-center fw-bold text-dark">${c.experience_years} Years</td>`).join("");

    const atsScoreRow = candidates.map(c => {
      let badge = "bg-success";
      if (c.ats_score < 40) badge = "bg-danger";
      else if (c.ats_score < 60) badge = "bg-warning text-dark";
      else if (c.ats_score < 80) badge = "bg-info text-white";
      return `<td class="border-start text-center py-2"><span class="badge ${badge} fs-5 px-3 py-1 rounded-pill">${c.ats_score}%</span></td>`;
    }).join("");

    compModalBody.innerHTML = `
      <div class="table-responsive mb-4" style="overflow-x: auto;">
        <table class="table table-bordered align-middle mb-0" style="min-width: 800px;">
          <thead class="bg-light">
            <tr>
              <th style="width: 20%;" class="py-3 ps-3 text-dark fw-bold fs-6">Attribute</th>
              ${candHeaders}
            </tr>
          </thead>
          <tbody>
            <tr class="table-dark text-white fw-bold"><td colspan="${candidates.length + 1}">1. Candidate Profile</td></tr>
            <tr><td class="fw-semibold bg-light">Role</td>${infoRoleRow}</tr>
            <tr><td class="fw-semibold bg-light">Location</td>${infoLocRow}</tr>
            <tr><td class="fw-semibold bg-light">Experience</td>${infoExpRow}</tr>

            <tr class="table-dark text-white fw-bold"><td colspan="${candidates.length + 1}">2. ATS Match Score</td></tr>
            <tr><td class="fw-semibold bg-light">ATS Match</td>${atsScoreRow}</tr>
          </tbody>
        </table>
      </div>

      <div class="card border-0 shadow-sm p-4 text-dark" style="background: linear-gradient(135deg, #e8f5e9 0%, #ffffff 100%); border-radius: 14px; border-left: 6px solid #28a745 !important;">
        <div class="d-flex align-items-center gap-2 mb-3">
          <span class="fs-2">🤖</span>
          <div>
            <h5 class="fw-bold text-success mb-0">AI Candidate Recommendation</h5>
            <span class="small text-muted">Powered by AI Recruiter multi-dimensional candidate evaluation</span>
          </div>
        </div>

        <div class="alert alert-success border-success bg-white p-3 rounded-3 mb-0">
          <h5 class="fw-bold text-success mb-1">🏆 Recommended Candidate: <u>${recommendedCand}</u></h5>
          <p class="small text-secondary mb-0">Top candidate alignment across skills, ATS score, experience, and interview performance.</p>
        </div>
      </div>
    `;
  }

  // Setup Event Listeners
  if (filterMinAts) {
    filterMinAts.addEventListener("input", (e) => {
      if (atsValBadge) atsValBadge.textContent = `${e.target.value}%`;
    });
  }

  if (searchForm) {
    searchForm.addEventListener("submit", (e) => {
      e.preventDefault();
      currentPage = 1;
      executeSmartSearch();
    });
  }

  if (btnParse) btnParse.addEventListener("click", autoFillFiltersFromQuery);
  if (btnReset) btnReset.addEventListener("click", resetFilters);
  if (sortBySelect) sortBySelect.addEventListener("change", () => { currentPage = 1; executeSmartSearch(); });
  if (compareSelectedBtn) compareSelectedBtn.addEventListener("click", openCandidateComparison);

  document.addEventListener("ar:auth-ready", async () => {
    await loadJobsDropdown();
    executeSmartSearch();
  });
})();
