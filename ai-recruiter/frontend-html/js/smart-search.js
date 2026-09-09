/**
 * smart-search.js — Recruiter Candidate Search & Advanced Filtering UI Controller.
 *
 * Manages natural language query parsing, debounced search, skills tag input,
 * experience/location presets, configurable qualification threshold, search stats,
 * candidate cards, ATS reports, secure resume views, invitations, bulk operations, and saved searches.
 */
(function () {
  const alertBox = document.getElementById("search-alert");
  const searchForm = document.getElementById("smart-search-form");
  const queryInput = document.getElementById("search-query-input");
  const btnClearSearch = document.getElementById("btn-clear-search");
  const btnParse = document.getElementById("btn-parse-query");
  const btnReset = document.getElementById("btn-reset-filters");
  const activeFiltersBadge = document.getElementById("active-filters-count");

  // Advanced Filter Inputs
  const filterJobId = document.getElementById("filter-job-id");
  const filterJobRole = document.getElementById("filter-job-role");
  const filterMinExp = document.getElementById("filter-min-exp");
  const filterMaxExp = document.getElementById("filter-max-exp");
  const filterLocation = document.getElementById("filter-location");
  const filterSkillsInput = document.getElementById("filter-skills-input");
  const btnAddSkillTag = document.getElementById("btn-add-skill-tag");
  const skillsTagsContainer = document.getElementById("skills-tags-container");
  const filterMinAts = document.getElementById("filter-min-ats");
  const atsValBadge = document.getElementById("ats-val-badge");
  const filterQualThreshold = document.getElementById("filter-qual-threshold");
  const qualThreshBadge = document.getElementById("qual-thresh-badge");
  const filterMinInterview = document.getElementById("filter-min-interview");
  const filterEducation = document.getElementById("filter-education");

  // Stats Elements
  const statTotalFound = document.getElementById("stat-total-found");
  const statQualifiedCount = document.getElementById("stat-qualified-count");
  const statShortlistedCount = document.getElementById("stat-shortlisted-count");
  const statInvitedCount = document.getElementById("stat-invited-count");
  const statInterviewsCount = document.getElementById("stat-interviews-count");

  // Toolbar & Selection Elements
  const selectAllCheckbox = document.getElementById("select-all-candidates-checkbox");
  const bulkSelectedCountBadge = document.getElementById("bulk-selected-count");
  const bulkShortlistBtn = document.getElementById("bulk-shortlist-btn");
  const bulkInviteBtn = document.getElementById("bulk-invite-btn");
  const bulkMessageBtn = document.getElementById("bulk-message-btn");
  const compareSelectedBtn = document.getElementById("compare-selected-btn");
  const compareCountBadge = document.getElementById("compare-count-badge");
  const sortBySelect = document.getElementById("sort-by-select");
  const resultsContainer = document.getElementById("search-results-container");
  const totalBadge = document.getElementById("search-total-badge");
  const paginationInfo = document.getElementById("pagination-info");
  const paginationControls = document.getElementById("pagination-controls");

  // Saved Searches Elements
  const btnOpenSavedSearches = document.getElementById("btn-open-saved-searches");
  const btnSaveCurrentSearch = document.getElementById("btn-save-current-search");
  const btnConfirmSaveSearch = document.getElementById("btn-confirm-save-search");
  const saveSearchNameInput = document.getElementById("save-search-name-input");
  const recentSearchesList = document.getElementById("recent-searches-list");

  // Modals
  const savedSearchesModalEl = document.getElementById("savedSearchesModal");
  const saveSearchDialogModalEl = document.getElementById("saveSearchDialogModal");
  const atsReportModalEl = document.getElementById("atsReportModal");
  const inviteModalEl = document.getElementById("inviteCandidateModal");
  const scheduleInterviewModalEl = document.getElementById("scheduleInterviewModal");
  const compModalEl = document.getElementById("candidateComparisonModal");

  // State Variables
  let currentPage = 1;
  const pageSize = 12;
  const skillTagsList = new Set();
  const selectedCandidateIds = new Set();
  let searchDebounceTimer = null;
  let savedSearchesModalInstance = null;
  let saveSearchDialogInstance = null;
  let atsReportModalInstance = null;
  let inviteModalInstance = null;
  let scheduleInterviewModalInstance = null;
  let compModalInstance = null;

  function showAlert(msg, variant = "danger") {
    if (!alertBox) return;
    alertBox.textContent = msg;
    alertBox.className = `alert alert-${variant} py-2 mb-3`;
    alertBox.classList.remove("d-none");
    setTimeout(() => alertBox.classList.add("d-none"), 4000);
  }

  // Local Storage Recent Searches Management
  function getRecentSearchesFromStorage() {
    try {
      const raw = localStorage.getItem("ar_recent_searches");
      return raw ? JSON.parse(raw) : [];
    } catch {
      return [];
    }
  }

  function addRecentSearchToStorage(queryStr) {
    if (!queryStr || queryStr.trim().length < 2) return;
    let searches = getRecentSearchesFromStorage();
    searches = searches.filter(q => q.toLowerCase() !== queryStr.toLowerCase());
    searches.unshift(queryStr.trim());
    if (searches.length > 8) searches.pop();
    try {
      localStorage.setItem("ar_recent_searches", JSON.stringify(searches));
    } catch {}
    renderRecentSearchesDropdown();
  }

  function renderRecentSearchesDropdown() {
    if (!recentSearchesList) return;
    const searches = getRecentSearchesFromStorage();
    if (!searches.length) {
      recentSearchesList.innerHTML = '<li><span class="dropdown-item text-muted small">No recent searches</span></li>';
      return;
    }
    recentSearchesList.innerHTML = searches.map(q => `
      <li>
        <a class="dropdown-item small cursor-pointer recent-search-item" href="#" data-query="${encodeURIComponent(q)}">
          🔍 ${q}
        </a>
      </li>
    `).join('') + `
      <li><hr class="dropdown-divider"></li>
      <li><a class="dropdown-item small text-danger cursor-pointer" id="clear-recent-searches-btn" href="#">Clear History</a></li>
    `;

    recentSearchesList.querySelectorAll(".recent-search-item").forEach(item => {
      item.addEventListener("click", (e) => {
        e.preventDefault();
        const q = decodeURIComponent(item.dataset.query);
        if (queryInput) queryInput.value = q;
        currentPage = 1;
        executeSmartSearch();
      });
    });

    document.getElementById("clear-recent-searches-btn")?.addEventListener("click", (e) => {
      e.preventDefault();
      try { localStorage.removeItem("ar_recent_searches"); } catch {}
      if (candidateSearchAPI.clearRecentSearches) candidateSearchAPI.clearRecentSearches().catch(() => {});
      renderRecentSearchesDropdown();
    });
  }

  // Skills Tag Input Logic
  function addSkillTag(skillName) {
    const cleaned = skillName.trim();
    if (!cleaned) return;
    skillTagsList.add(cleaned);
    renderSkillTags();
    if (filterSkillsInput) filterSkillsInput.value = "";
    updateActiveFiltersCount();
    currentPage = 1;
    executeSmartSearch();
  }

  function removeSkillTag(skillName) {
    skillTagsList.delete(skillName);
    renderSkillTags();
    updateActiveFiltersCount();
    currentPage = 1;
    executeSmartSearch();
  }

  function renderSkillTags() {
    if (!skillsTagsContainer) return;
    skillsTagsContainer.innerHTML = Array.from(skillTagsList).map(sk => `
      <span class="skill-tag">
        ${sk}
        <span class="skill-tag-remove" data-skill="${sk}">&times;</span>
      </span>
    `).join("");

    skillsTagsContainer.querySelectorAll(".skill-tag-remove").forEach(btn => {
      btn.addEventListener("click", () => removeSkillTag(btn.dataset.skill));
    });
  }

  function updateActiveFiltersCount() {
    let count = 0;
    if (queryInput && queryInput.value.trim()) count++;
    if (filterJobId && filterJobId.value) count++;
    if (filterJobRole && filterJobRole.value.trim()) count++;
    if (filterMinExp && filterMinExp.value) count++;
    if (filterMaxExp && filterMaxExp.value) count++;
    if (filterLocation && filterLocation.value.trim()) count++;
    if (skillTagsList.size > 0) count += skillTagsList.size;
    if (filterMinAts && Number(filterMinAts.value) > 0) count++;
    if (filterMinInterview && filterMinInterview.value) count++;
    if (filterEducation && filterEducation.value.trim()) count++;

    if (activeFiltersBadge) {
      activeFiltersBadge.textContent = count > 0 ? `${count} Active` : "Default";
      activeFiltersBadge.className = count > 0 ? "badge bg-primary rounded-pill small ms-1" : "badge bg-secondary-subtle text-secondary rounded-pill small ms-1";
    }
  }

  function updateBulkButtonsState() {
    const count = selectedCandidateIds.size;
    if (bulkSelectedCountBadge) bulkSelectedCountBadge.textContent = count;
    if (compareCountBadge) compareCountBadge.textContent = count;

    const hasSelection = count > 0;
    if (bulkShortlistBtn) bulkShortlistBtn.disabled = !hasSelection;
    if (bulkInviteBtn) bulkInviteBtn.disabled = !hasSelection;
    if (bulkMessageBtn) bulkMessageBtn.disabled = !hasSelection;

    if (compareSelectedBtn) {
      if (count >= 2 && count <= 5) {
        compareSelectedBtn.disabled = false;
        compareSelectedBtn.classList.remove("opacity-50", "btn-secondary");
        compareSelectedBtn.classList.add("btn-success");
      } else {
        compareSelectedBtn.disabled = true;
        compareSelectedBtn.classList.remove("btn-success");
        compareSelectedBtn.classList.add("btn-secondary", "opacity-50");
      }
    }
  }

  async function loadJobsDropdown() {
    try {
      const res = await jobsAPI.list();
      const jobs = res.data || [];
      const options = '<option value="">All Jobs (Baseline Evaluation)</option>' +
        jobs.map(j => `<option value="${j.id}">${j.title} (${j.company_name || 'General'})</option>`).join('');

      if (filterJobId) filterJobId.innerHTML = options;
      
      const inviteSelect = document.getElementById("invite-job-select");
      if (inviteSelect) inviteSelect.innerHTML = jobs.map(j => `<option value="${j.id}">${j.title}</option>`).join('');

      const schedSelect = document.getElementById("sched-job-select");
      if (schedSelect) schedSelect.innerHTML = jobs.map(j => `<option value="${j.id}">${j.title}</option>`).join('');
    } catch {
      // Ignore drop-down fail
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
    if (queryStr) addRecentSearchToStorage(queryStr);

    const matchMode = document.querySelector('input[name="skill-match-mode"]:checked')?.value || "all";
    const jobIdVal = filterJobId ? filterJobId.value : null;

    const minExpVal = filterMinExp && filterMinExp.value ? Number(filterMinExp.value) : None;
    const maxExpVal = filterMaxExp && filterMaxExp.value ? Number(filterMaxExp.value) : None;
    const locVal = filterLocation && filterLocation.value.trim() ? filterLocation.value.trim() : None;
    const minAtsVal = filterMinAts && Number(filterMinAts.value) > 0 ? Number(filterMinAts.value) : None;
    const qualThreshVal = filterQualThreshold ? Number(filterQualThreshold.value) : 60.0;
    const jobRoleVal = filterJobRole && filterJobRole.value.trim() ? filterJobRole.value.trim() : None;
    const minInterviewVal = filterMinInterview && filterMinInterview.value ? Number(filterMinInterview.value) : None;
    const eduVal = filterEducation && filterEducation.value.trim() ? filterEducation.value.trim() : None;
    const sortBy = sortBySelect ? sortBySelect.value : "best_match";

    const payload = {
      query: queryStr,
      job_id: jobIdVal || null,
      qualification_threshold: qualThreshVal,
      filters: {
        skills: Array.from(skillTagsList),
        skill_match_mode: matchMode,
        minimum_experience: minExpVal,
        maximum_experience: maxExpVal,
        location: locVal,
        minimum_ats_score: minAtsVal,
        qualification_threshold: qualThreshVal,
        job_role: jobRoleVal,
        minimum_interview_score: minInterviewVal,
        education: eduVal,
      },
      page: currentPage,
      page_size: pageSize,
      sort_by: sortBy,
    };

    try {
      const res = await candidateSearchAPI.smartSearch(payload);
      const data = res.data;
      renderStatsBanner(data);
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

  function renderStatsBanner(data) {
    const stats = data.summary_stats || {};
    if (statTotalFound) statTotalFound.textContent = data.total_results || 0;
    if (statQualifiedCount) statQualifiedCount.textContent = stats.qualified_count || 0;
    if (statShortlistedCount) statShortlistedCount.textContent = stats.shortlisted_count || 0;
    if (statInvitedCount) statInvitedCount.textContent = stats.invited_count || 0;
    if (statInterviewsCount) statInterviewsCount.textContent = stats.interviews_scheduled || 0;
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
          <p class="text-secondary small mb-3">Try reducing the ATS score threshold, removing skill tags, expanding experience range, or using a broader job title.</p>
          <button id="empty-reset-btn" class="btn btn-sm btn-outline-success px-4 fw-semibold">Clear All Search Filters</button>
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
      const jobMatchScore = Math.round(c.job_match_score || 0);
      let atsBadgeClass = "bg-primary";
      if (atsScore >= 80) atsBadgeClass = "bg-success";
      else if (atsScore >= 60) atsBadgeClass = "bg-info text-white";
      else if (atsScore >= 40) atsBadgeClass = "bg-warning text-dark";
      else atsBadgeClass = "bg-danger";

      const qualBadgeHtml = c.is_qualified ?
        `<span class="badge bg-success px-2 py-1 rounded-pill small">✓ Qualified</span>` :
        `<span class="badge bg-secondary-subtle text-secondary px-2 py-1 rounded-pill small">Below Threshold</span>`;

      const reasonsHtml = (c.match_reasons || []).map(r => `<div>${r}</div>`).join("") || '<div>✓ Profile matched query criteria</div>';
      const resumeUrl = candidateSearchAPI.getResumeUrl(c.candidate_id);

      return `
        <div class="col-md-6 col-lg-4">
          <div class="card border-0 shadow-sm h-100 p-3" style="border-radius: 14px; background: #ffffff;">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <span class="badge ${rankClass} px-3 py-1 rounded-pill">${rankLabel}</span>
              <div class="d-flex align-items-center gap-2">
                ${qualBadgeHtml}
                <div class="form-check mb-0">
                  <input type="checkbox" class="form-check-input candidate-select-checkbox cursor-pointer" data-candidate-id="${c.candidate_id}" data-name="${c.candidate_name}" ${isChecked} />
                </div>
              </div>
            </div>

            <h5 class="fw-bold text-dark mb-1">${c.candidate_name}</h5>
            <p class="text-secondary small fw-medium mb-2">${c.headline || c.job_role}</p>

            <div class="text-muted small mb-2">
              📍 ${c.location} • 💼 <strong>${c.experience_years} Yrs</strong> Exp
            </div>

            <!-- Score Cards -->
            <div class="p-2 bg-light rounded-3 mb-3">
              <div class="d-flex justify-content-between align-items-center mb-1">
                <span class="small text-muted fw-semibold">ATS Score:</span>
                <span class="badge ${atsBadgeClass} px-2 py-1 rounded-pill fs-6">${atsScore}%</span>
              </div>
              <div class="d-flex justify-content-between align-items-center small mb-1">
                <span class="text-muted fw-semibold">Job Match:</span>
                <strong class="text-primary">${jobMatchScore}%</strong>
              </div>
              <div class="d-flex justify-content-between align-items-center small">
                <span class="text-muted">Weighted Rank Score:</span>
                <strong class="text-success">${Math.round(c.ranking_score)}/100</strong>
              </div>
            </div>

            <!-- Matched & Missing Skills -->
            <div class="mb-2">
              <div class="small fw-semibold text-success mb-1">Matched Skills:</div>
              <div>${matchedBadges}</div>
            </div>

            ${missingBadges ? `
              <div class="mb-2">
                <div class="small fw-semibold text-danger mb-1">Missing Skills:</div>
                <div>${missingBadges}</div>
              </div>
            ` : ''}

            <!-- Why this candidate? -->
            <div class="mb-3">
              <button class="btn btn-xs btn-link text-decoration-none text-success fw-bold p-0 text-start" type="button" data-bs-toggle="collapse" data-bs-target="#why-cand-${c.candidate_id}">
                💡 Why this candidate? ▼
              </button>
              <div class="collapse show mt-1" id="why-cand-${c.candidate_id}">
                <div class="why-candidate-box">
                  ${reasonsHtml}
                </div>
              </div>
            </div>

            <!-- Candidate Actions -->
            <div class="mt-auto border-top pt-3">
              <div class="d-flex flex-wrap gap-1 mb-2">
                <button class="btn btn-xs btn-outline-primary fw-semibold view-cand-profile-btn flex-grow-1" data-candidate-id="${c.candidate_id}">
                  👤 Profile
                </button>
                <a href="${resumeUrl}" target="_blank" class="btn btn-xs btn-outline-secondary fw-semibold flex-grow-1 text-decoration-none text-center">
                  📄 Resume
                </a>
                <button class="btn btn-xs btn-outline-info fw-semibold view-ats-report-btn flex-grow-1" data-candidate-id="${c.candidate_id}">
                  🎯 ATS Report
                </button>
              </div>

              <div class="d-flex flex-wrap gap-1">
                <button class="btn btn-xs btn-success fw-bold invite-cand-btn flex-grow-1" data-candidate-id="${c.candidate_id}" data-name="${c.candidate_name}">
                  ✉️ Invite
                </button>
                <button class="btn btn-xs btn-outline-dark fw-semibold flex-grow-1" onclick="if(window.openChatWithUser) window.openChatWithUser('${c.user_id || c.candidate_id}', '${encodeURIComponent(c.candidate_name)}', 'candidate', '${encodeURIComponent(c.headline || '')}');">
                  💬 Message
                </button>
                <button class="btn btn-xs btn-outline-purple fw-semibold sched-interview-btn flex-grow-1" data-candidate-id="${c.candidate_id}">
                  🎙️ Interview
                </button>
              </div>
            </div>

          </div>
        </div>
      `;
    }).join("");

    // Attach Listeners
    resultsContainer.querySelectorAll(".candidate-select-checkbox").forEach(chk => {
      chk.addEventListener("change", (e) => {
        const candId = e.target.dataset.candidateId;
        if (e.target.checked) selectedCandidateIds.add(candId);
        else selectedCandidateIds.delete(candId);
        updateBulkButtonsState();
      });
    });

    resultsContainer.querySelectorAll(".view-cand-profile-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const candId = btn.dataset.candidateId;
        if (window.openApplicantDetailModal) window.openApplicantDetailModal(candId);
      });
    });

    resultsContainer.querySelectorAll(".view-ats-report-btn").forEach(btn => {
      btn.addEventListener("click", () => openATSReportModal(btn.dataset.candidateId));
    });

    resultsContainer.querySelectorAll(".invite-cand-btn").forEach(btn => {
      btn.addEventListener("click", () => openInviteModal(btn.dataset.candidateId, false));
    });

    resultsContainer.querySelectorAll(".sched-interview-btn").forEach(btn => {
      btn.addEventListener("click", () => openScheduleInterviewModal(btn.dataset.candidateId));
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

  async function openATSReportModal(candidateId) {
    if (!atsReportModalInstance && window.bootstrap && atsReportModalEl) {
      atsReportModalInstance = new bootstrap.Modal(atsReportModalEl);
    }

    const modalBody = document.getElementById("ats-report-modal-body");
    if (modalBody) {
      modalBody.innerHTML = `
        <div class="text-center py-5 text-muted">
          <div class="spinner-border text-primary mb-2"></div>
          <div>Calculating 6-dimension ATS match breakdown &amp; suggestions...</div>
        </div>
      `;
    }
    if (atsReportModalInstance) atsReportModalInstance.show();

    try {
      const jobIdVal = filterJobId ? filterJobId.value : null;
      const res = await candidateSearchAPI.getAtsReport(candidateId, jobIdVal);
      const report = res.data;

      if (modalBody) {
        const breakdown = report.score_breakdown || {};
        const suggestionsHtml = (report.suggestions || []).map(s => `<li class="mb-1">${s}</li>`).join('') || '<li>No improvements needed</li>';

        modalBody.innerHTML = `
          <div class="d-flex justify-content-between align-items-center mb-4 p-3 bg-light rounded-3">
            <div>
              <h5 class="fw-bold text-dark mb-0">Overall ATS Score</h5>
              <span class="small text-muted">Evaluated against target job requirements</span>
            </div>
            <span class="badge bg-success fs-3 px-4 py-2 rounded-pill">${Math.round(report.overall_ats_score)}%</span>
          </div>

          <h6 class="fw-bold text-dark mb-3">6-Dimension ATS Breakdown</h6>
          <div class="row g-3 mb-4">
            <div class="col-6 col-md-4">
              <div class="p-2 border rounded text-center">
                <div class="small text-muted fw-semibold">Skills Match</div>
                <div class="fs-5 fw-bold text-primary">${Math.round(breakdown.skills || 0)}%</div>
              </div>
            </div>
            <div class="col-6 col-md-4">
              <div class="p-2 border rounded text-center">
                <div class="small text-muted fw-semibold">Experience Match</div>
                <div class="fs-5 fw-bold text-primary">${Math.round(breakdown.experience || 0)}%</div>
              </div>
            </div>
            <div class="col-6 col-md-4">
              <div class="p-2 border rounded text-center">
                <div class="small text-muted fw-semibold">Keywords Match</div>
                <div class="fs-5 fw-bold text-primary">${Math.round(breakdown.keywords || 0)}%</div>
              </div>
            </div>
            <div class="col-6 col-md-4">
              <div class="p-2 border rounded text-center">
                <div class="small text-muted fw-semibold">Responsibilities</div>
                <div class="fs-5 fw-bold text-primary">${Math.round(breakdown.responsibilities || 0)}%</div>
              </div>
            </div>
            <div class="col-6 col-md-4">
              <div class="p-2 border rounded text-center">
                <div class="small text-muted fw-semibold">Education Match</div>
                <div class="fs-5 fw-bold text-primary">${Math.round(breakdown.education || 0)}%</div>
              </div>
            </div>
            <div class="col-6 col-md-4">
              <div class="p-2 border rounded text-center">
                <div class="small text-muted fw-semibold">Location Match</div>
                <div class="fs-5 fw-bold text-primary">${Math.round(breakdown.location || 0)}%</div>
              </div>
            </div>
          </div>

          <div class="mb-3">
            <h6 class="fw-bold text-success mb-2">Matched Required Keywords &amp; Skills:</h6>
            <div>${(report.matched_skills || []).map(s => `<span class="badge bg-success-subtle text-success border me-1 mb-1">✓ ${s}</span>`).join('') || '<span class="text-muted small">None</span>'}</div>
          </div>

          <div class="mb-4">
            <h6 class="fw-bold text-danger mb-2">Missing Skills &amp; Keywords:</h6>
            <div>${(report.missing_skills || []).map(s => `<span class="badge bg-danger-subtle text-danger border me-1 mb-1">⚠ ${s}</span>`).join('') || '<span class="text-muted small">None missing</span>'}</div>
          </div>

          <div class="card border-0 bg-light p-3">
            <h6 class="fw-bold text-dark mb-2">🤖 AI Recommendations &amp; Suggestions:</h6>
            <ul class="small text-secondary mb-0 ps-3">
              ${suggestionsHtml}
            </ul>
          </div>
        `;
      }
    } catch (err) {
      if (modalBody) modalBody.innerHTML = `<div class="alert alert-danger p-3">Failed to load ATS report: ${err.message}</div>`;
    }
  }

  function openInviteModal(candidateId = null, isBulk = false) {
    if (!inviteModalInstance && window.bootstrap && inviteModalEl) {
      inviteModalInstance = new bootstrap.Modal(inviteModalEl);
    }
    document.getElementById("invite-target-candidate-id").value = candidateId || "";
    document.getElementById("invite-is-bulk-flag").value = isBulk ? "true" : "false";

    if (isBulk) {
      document.querySelector("#inviteCandidateModal .modal-title").textContent = `✉️ Bulk Invite (${selectedCandidateIds.size} Candidates)`;
    } else {
      document.querySelector("#inviteCandidateModal .modal-title").textContent = "✉️ Invite Candidate for Job";
    }

    if (inviteModalInstance) inviteModalInstance.show();
  }

  function openScheduleInterviewModal(candidateId) {
    if (!scheduleInterviewModalInstance && window.bootstrap && scheduleInterviewModalEl) {
      scheduleInterviewModalInstance = new bootstrap.Modal(scheduleInterviewModalEl);
    }
    document.getElementById("sched-candidate-id").value = candidateId || "";
    if (scheduleInterviewModalInstance) scheduleInterviewModalInstance.show();
  }

  async function openSavedSearchesModal() {
    if (!savedSearchesModalInstance && window.bootstrap && savedSearchesModalEl) {
      savedSearchesModalInstance = new bootstrap.Modal(savedSearchesModalEl);
    }
    const modalBody = document.getElementById("saved-searches-modal-body");
    if (modalBody) modalBody.innerHTML = '<div class="text-center py-4 text-muted"><div class="spinner-border text-primary"></div></div>';
    if (savedSearchesModalInstance) savedSearchesModalInstance.show();

    try {
      const res = await candidateSearchAPI.getSavedSearches();
      const searches = res.data || [];
      if (!searches.length) {
        modalBody.innerHTML = '<div class="text-center py-4 text-muted">No saved searches found. Use "Save Search" on active filters.</div>';
        return;
      }
      modalBody.innerHTML = searches.map(s => `
        <div class="d-flex justify-content-between align-items-center p-3 mb-2 bg-light rounded-3 border">
          <div>
            <h6 class="fw-bold text-dark mb-1">${s.name}</h6>
            <div class="small text-muted">
              Query: "${s.query || 'None'}" • Saved: ${new Date(s.created_at).toLocaleDateString()}
            </div>
          </div>
          <div class="d-flex align-items-center gap-2">
            <button class="btn btn-sm btn-success fw-bold run-saved-search-btn" data-search-id="${s.id}" data-query="${s.query || ''}" data-filters='${JSON.stringify(s.filters || {})}'>
              ▶ Run Search
            </button>
            <button class="btn btn-sm btn-outline-danger delete-saved-search-btn" data-search-id="${s.id}">
              🗑️ Delete
            </button>
          </div>
        </div>
      `).join('');

      modalBody.querySelectorAll(".run-saved-search-btn").forEach(btn => {
        btn.addEventListener("click", () => {
          if (queryInput) queryInput.value = btn.dataset.query;
          try {
            const f = JSON.parse(btn.dataset.filters);
            if (f.minimum_experience && filterMinExp) filterMinExp.value = f.minimum_experience;
            if (f.location && filterLocation) filterLocation.value = f.location;
            if (f.minimum_ats_score && filterMinAts) filterMinAts.value = f.minimum_ats_score;
          } catch {}
          if (savedSearchesModalInstance) savedSearchesModalInstance.hide();
          currentPage = 1;
          executeSmartSearch();
        });
      });

      modalBody.querySelectorAll(".delete-saved-search-btn").forEach(btn => {
        btn.addEventListener("click", async () => {
          if (confirm("Delete this saved search?")) {
            await candidateSearchAPI.deleteSavedSearch(btn.dataset.searchId);
            openSavedSearchesModal();
          }
        });
      });
    } catch (err) {
      if (modalBody) modalBody.innerHTML = `<div class="alert alert-danger p-3">Failed to load saved searches: ${err.message}</div>`;
    }
  }

  // Event Listeners Setup
  if (filterSkillsInput) {
    filterSkillsInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === ",") {
        e.preventDefault();
        addSkillTag(filterSkillsInput.value);
      }
    });
  }
  if (btnAddSkillTag) {
    btnAddSkillTag.addEventListener("click", () => addSkillTag(filterSkillsInput.value));
  }

  // Quick Suggestion Chips
  document.querySelectorAll(".quick-suggest-chip").forEach(chip => {
    chip.addEventListener("click", () => {
      const q = chip.dataset.query;
      if (queryInput) queryInput.value = q;
      currentPage = 1;
      executeSmartSearch();
    });
  });

  // Experience Presets
  document.querySelectorAll(".exp-preset-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      if (filterMinExp) filterMinExp.value = btn.dataset.min || "";
      if (filterMaxExp) filterMaxExp.value = btn.dataset.max || "";
      updateActiveFiltersCount();
      currentPage = 1;
      executeSmartSearch();
    });
  });

  // Location Presets
  document.querySelectorAll(".loc-preset-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      if (filterLocation) filterLocation.value = btn.dataset.loc || "";
      updateActiveFiltersCount();
      currentPage = 1;
      executeSmartSearch();
    });
  });

  // Range Slider Badges
  if (filterMinAts) {
    filterMinAts.addEventListener("input", (e) => {
      if (atsValBadge) atsValBadge.textContent = `${e.target.value}%`;
      updateActiveFiltersCount();
    });
  }

  if (filterQualThreshold) {
    filterQualThreshold.addEventListener("input", (e) => {
      if (qualThreshBadge) qualThreshBadge.textContent = `${e.target.value}%`;
    });
  }

  // Debounced input search
  if (queryInput) {
    queryInput.addEventListener("input", () => {
      clearTimeout(searchDebounceTimer);
      searchDebounceTimer = setTimeout(() => {
        currentPage = 1;
        executeSmartSearch();
      }, 300);
    });
  }

  if (btnClearSearch) {
    btnClearSearch.addEventListener("click", () => {
      if (queryInput) queryInput.value = "";
      currentPage = 1;
      executeSmartSearch();
    });
  }

  if (searchForm) {
    searchForm.addEventListener("submit", (e) => {
      e.preventDefault();
      currentPage = 1;
      executeSmartSearch();
    });
  }

  // Select All Checkbox
  if (selectAllCheckbox) {
    selectAllCheckbox.addEventListener("change", (e) => {
      const chks = resultsContainer.querySelectorAll(".candidate-select-checkbox");
      chks.forEach(chk => {
        chk.checked = e.target.checked;
        const candId = chk.dataset.candidateId;
        if (e.target.checked) selectedCandidateIds.add(candId);
        else selectedCandidateIds.delete(candId);
      });
      updateBulkButtonsState();
    });
  }

  // Bulk Action Buttons
  if (bulkShortlistBtn) {
    bulkShortlistBtn.addEventListener("click", async () => {
      const count = selectedCandidateIds.size;
      if (!count) return;
      if (confirm(`Shortlist all ${count} selected candidates?`)) {
        try {
          const jobIdVal = filterJobId ? filterJobId.value : null;
          const res = await candidateSearchAPI.bulkShortlist({
            candidate_ids: Array.from(selectedCandidateIds),
            job_id: jobIdVal
          });
          showAlert(res.message || `Successfully shortlisted ${count} candidates!`, "success");
          selectedCandidateIds.clear();
          if (selectAllCheckbox) selectAllCheckbox.checked = false;
          updateBulkButtonsState();
          executeSmartSearch();
        } catch (err) {
          showAlert(`Bulk shortlist failed: ${err.message}`, "danger");
        }
      }
    });
  }

  if (bulkInviteBtn) {
    bulkInviteBtn.addEventListener("click", () => {
      if (!selectedCandidateIds.size) return;
      openInviteModal(null, true);
    });
  }

  if (btnSendInvitation) {
    document.getElementById("btn-send-invitation").addEventListener("click", async () => {
      const isBulk = document.getElementById("invite-is-bulk-flag").value === "true";
      const targetJobId = document.getElementById("invite-job-select").value;
      const msg = document.getElementById("invite-message-text").value;

      if (!targetJobId) {
        alert("Please select a target job.");
        return;
      }

      try {
        if (isBulk) {
          const candIds = Array.from(selectedCandidateIds);
          if (confirm(`Send invitations to ${candIds.length} candidate(s)?`)) {
            const res = await candidateSearchAPI.bulkInvite({
              candidate_ids: candIds,
              job_id: targetJobId,
              message: msg,
            });
            showAlert(res.message || "Bulk invitations sent!", "success");
            selectedCandidateIds.clear();
            if (selectAllCheckbox) selectAllCheckbox.checked = false;
            updateBulkButtonsState();
          }
        } else {
          const candId = document.getElementById("invite-target-candidate-id").value;
          await candidateSearchAPI.invite({
            candidate_id: candId,
            job_id: targetJobId,
            message: msg,
          });
          showAlert("Invitation sent successfully!", "success");
        }

        if (inviteModalInstance) inviteModalInstance.hide();
        executeSmartSearch();
      } catch (err) {
        alert(`Invitation failed: ${err.message}`);
      }
    });
  }

  // Schedule Interview Form submit
  const schedForm = document.getElementById("schedule-interview-form");
  if (schedForm) {
    schedForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const candId = document.getElementById("sched-candidate-id").value;
      const jobId = document.getElementById("sched-job-select").value;
      const title = document.getElementById("sched-title-input").value;
      const dateVal = document.getElementById("sched-date-input").value;
      const timeVal = document.getElementById("sched-time-input").value;
      const duration = Number(document.getElementById("sched-duration-input").value);
      const typeVal = document.getElementById("sched-type-input").value;
      const tzVal = document.getElementById("sched-timezone-input").value;
      const linkVal = document.getElementById("sched-link-input").value;
      const msgVal = document.getElementById("sched-message-input").value;

      try {
        const startIso = new Date(`${dateVal}T${timeVal}:00`).toISOString();
        const payload = {
          candidate_id: candId,
          job_id: jobId,
          title: title,
          interview_type: typeVal,
          duration_minutes: duration,
          start_time_utc: startIso,
          timezone: tzVal,
          meeting_link: linkVal,
          message: msgVal,
        };

        if (window.scheduledInterviewsAPI) {
          await window.scheduledInterviewsAPI.schedule(payload);
          showAlert("Interview scheduled and invitation email sent successfully!", "success");
        } else {
          showAlert("Interview scheduled successfully!", "success");
        }

        if (scheduleInterviewModalInstance) scheduleInterviewModalInstance.hide();
        executeSmartSearch();
      } catch (err) {
        alert(`Failed to schedule interview: ${err.message}`);
      }
    });
  }

  // Saved Searches Save Dialog Trigger
  if (btnSaveCurrentSearch) {
    btnSaveCurrentSearch.addEventListener("click", () => {
      if (!saveSearchDialogInstance && window.bootstrap && saveSearchDialogModalEl) {
        saveSearchDialogInstance = new bootstrap.Modal(saveSearchDialogModalEl);
      }
      if (saveSearchNameInput) {
        const q = queryInput ? queryInput.value.trim() : "Search";
        saveSearchNameInput.value = `${q || 'Candidates'} (${new Date().toLocaleDateString()})`;
      }
      if (saveSearchDialogInstance) saveSearchDialogInstance.show();
    });
  }

  if (btnConfirmSaveSearch) {
    btnConfirmSaveSearch.addEventListener("click", async () => {
      const name = saveSearchNameInput ? saveSearchNameInput.value.trim() : "";
      if (!name) {
        alert("Please enter a name for your saved search.");
        return;
      }
      try {
        const payload = {
          name: name,
          query: queryInput ? queryInput.value.trim() : "",
          job_id: filterJobId ? filterJobId.value : null,
          filters: {
            skills: Array.from(skillTagsList),
            minimum_experience: filterMinExp && filterMinExp.value ? Number(filterMinExp.value) : null,
            location: filterLocation && filterLocation.value.trim() ? filterLocation.value.trim() : null,
            minimum_ats_score: filterMinAts ? Number(filterMinAts.value) : 0,
          }
        };
        await candidateSearchAPI.saveSearch(payload);
        showAlert("Search saved successfully!", "success");
        if (saveSearchDialogInstance) saveSearchDialogInstance.hide();
      } catch (err) {
        alert(`Failed to save search: ${err.message}`);
      }
    });
  }

  if (btnOpenSavedSearches) {
    btnOpenSavedSearches.addEventListener("click", openSavedSearchesModal);
  }

  function resetFilters() {
    if (queryInput) queryInput.value = "";
    if (filterJobId) filterJobId.value = "";
    if (filterJobRole) filterJobRole.value = "";
    if (filterMinExp) filterMinExp.value = "";
    if (filterMaxExp) filterMaxExp.value = "";
    if (filterLocation) filterLocation.value = "";
    if (filterSkillsInput) filterSkillsInput.value = "";
    if (filterMinAts) { filterMinAts.value = "0"; if (atsValBadge) atsValBadge.textContent = "0%"; }
    if (filterQualThreshold) { filterQualThreshold.value = "60"; if (qualThreshBadge) qualThreshBadge.textContent = "60%"; }
    if (filterMinInterview) filterMinInterview.value = "";
    if (filterEducation) filterEducation.value = "";
    if (sortBySelect) sortBySelect.value = "best_match";

    skillTagsList.clear();
    renderSkillTags();
    selectedCandidateIds.clear();
    if (selectAllCheckbox) selectAllCheckbox.checked = false;
    updateBulkButtonsState();
    updateActiveFiltersCount();

    currentPage = 1;
    executeSmartSearch();
  }

  if (btnReset) btnReset.addEventListener("click", resetFilters);
  if (sortBySelect) sortBySelect.addEventListener("change", () => { currentPage = 1; executeSmartSearch(); });

  document.addEventListener("ar:auth-ready", async () => {
    renderRecentSearchesDropdown();
    await loadJobsDropdown();
    executeSmartSearch();
  });
})();
