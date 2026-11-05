/**
 * recruiter-dashboard.js — interactive analytics & hiring funnel dashboard.
 * Loads GET /api/v1/analytics/recruiter with filter params (job_id, date range, status),
 * updates interactive Chart.js charts, KPI cards, and job performance tables.
 */
(function () {
  const alertBox = document.getElementById("dashboard-alert");
  const jobFilterSelect = document.getElementById("analytics-job-filter");
  const dateFilterSelect = document.getElementById("analytics-date-filter");
  const statusFilterSelect = document.getElementById("analytics-status-filter");

  // Chart Instances Registry for Destruction before Re-rendering
  const chartInstances = {};

  function showAlert(message, variant) {
    if (!alertBox) return;
    alertBox.textContent = message;
    alertBox.className = `alert alert-${variant} py-2 mb-3`;
    alertBox.classList.remove("d-none");
    setTimeout(() => alertBox.classList.add("d-none"), 4000);
  }

  function setStat(id, value) {
    const el = document.getElementById(id);
    if (el) {
      el.textContent = value ?? "0";
    }
  }

  function renderOrEmpty(canvasId, hasData, renderFn) {
    const emptyEl = document.getElementById(`${canvasId}-empty`);
    const canvasEl = document.getElementById(canvasId);
    if (!canvasEl) return;

    if (chartInstances[canvasId]) {
      chartInstances[canvasId].destroy();
      delete chartInstances[canvasId];
    }

    if (!hasData) {
      canvasEl.classList.add("d-none");
      if (emptyEl) emptyEl.classList.remove("d-none");
      return;
    }
    canvasEl.classList.remove("d-none");
    if (emptyEl) emptyEl.classList.add("d-none");
    renderFn();
  }

  function renderHiringFunnelChart(data) {
    const stages = data.funnel_stages || {
      Applied: data.total_applications || 0,
      Shortlisted: data.shortlisted_count || 0,
      Interviewed: data.interview_count || 0,
      Hired: data.hired_count || data.selected_count || 0,
    };

    const labels = Object.keys(stages);
    const values = Object.values(stages);
    const hasData = values.some((v) => v > 0);

    renderOrEmpty("chart-hiring-funnel", hasData, () => {
      chartInstances["chart-hiring-funnel"] = new Chart(document.getElementById("chart-hiring-funnel"), {
        type: "bar",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Candidates",
              data: values,
              backgroundColor: ["#2f5fff", "#17a2b8", "#ffc107", "#28a745"],
              borderRadius: 8,
              barThickness: 32,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: (ctx) => `${ctx.label}: ${ctx.raw} candidates`,
              },
            },
          },
          scales: {
            y: { beginAtZero: true, ticks: { precision: 0 } },
          },
        },
      });
    });
  }

  function renderMatchDistributionChart(data) {
    const dist = data.match_score_distribution || {
      "90_100": 0,
      "80_89": 0,
      "70_79": 0,
      "60_69": 0,
      "below_60": 0,
    };

    const labels = ["90–100%", "80–89%", "70–79%", "60–69%", "Below 60%"];
    const values = [
      dist["90_100"] || 0,
      dist["80_89"] || 0,
      dist["70_79"] || 0,
      dist["60_69"] || 0,
      dist["below_60"] || 0,
    ];
    const hasData = values.some((v) => v > 0);

    renderOrEmpty("chart-match-distribution", hasData, () => {
      chartInstances["chart-match-distribution"] = new Chart(document.getElementById("chart-match-distribution"), {
        type: "bar",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Applicants",
              data: values,
              backgroundColor: ["#28a745", "#17a2b8", "#007bff", "#ffc107", "#dc3545"],
              borderRadius: 6,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: { legend: { display: false } },
          scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
        },
      });
    });
  }

  function renderMissingSkillsChart(data) {
    const missingSkills = data.missing_skills_analysis || [];
    const hasData = missingSkills.length > 0;

    renderOrEmpty("chart-missing-skills", hasData, () => {
      chartInstances["chart-missing-skills"] = new Chart(document.getElementById("chart-missing-skills"), {
        type: "bar",
        data: {
          labels: missingSkills.map((s) => s.skill),
          datasets: [
            {
              label: "Missing Candidates",
              data: missingSkills.map((s) => s.count),
              backgroundColor: "#dc3545",
              borderRadius: 6,
            },
          ],
        },
        options: {
          indexAxis: "y",
          responsive: true,
          plugins: { legend: { display: false } },
          scales: { x: { beginAtZero: true, ticks: { precision: 0 } } },
        },
      });
    });
  }

  function renderTopSkillsChart(data) {
    renderOrEmpty("chart-top-skills", data.top_skills && data.top_skills.length > 0, () => {
      chartInstances["chart-top-skills"] = new Chart(document.getElementById("chart-top-skills"), {
        type: "bar",
        data: {
          labels: data.top_skills.map((s) => s.skill),
          datasets: [
            {
              label: "Candidates",
              data: data.top_skills.map((s) => s.count),
              backgroundColor: "#28a745",
              borderRadius: 6,
            },
          ],
        },
        options: {
          indexAxis: "y",
          responsive: true,
          plugins: { legend: { display: false } },
          scales: { x: { beginAtZero: true, ticks: { precision: 0 } } },
        },
      });
    });
  }

  function renderApplicationsByJobChart(data) {
    renderOrEmpty("chart-applications-by-job", data.applications_by_job && data.applications_by_job.length > 0, () => {
      chartInstances["chart-applications-by-job"] = new Chart(document.getElementById("chart-applications-by-job"), {
        type: "bar",
        data: {
          labels: data.applications_by_job.map((j) => j.job_title),
          datasets: [
            {
              label: "Applications",
              data: data.applications_by_job.map((j) => j.count),
              backgroundColor: "#2f5fff",
              borderRadius: 6,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: { legend: { display: false } },
          scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
        },
      });
    });
  }

  function renderInterviewScoresChart(data) {
    renderOrEmpty("chart-interview-scores", data.interview_scores && data.interview_scores.length > 0, () => {
      chartInstances["chart-interview-scores"] = new Chart(document.getElementById("chart-interview-scores"), {
        type: "bar",
        data: {
          labels: data.interview_scores.map((s, i) => s.job_title || `Interview ${i + 1}`),
          datasets: [
            {
              label: "Overall Score",
              data: data.interview_scores.map((s) => s.overall_score),
              backgroundColor: "#ffc107",
              borderRadius: 6,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: { legend: { display: false } },
          scales: { y: { beginAtZero: true, max: 100 } },
        },
      });
    });
  }

  function statusBadgeHtml(status) {
    if (status === "published") return '<span class="badge bg-success">Published</span>';
    if (status === "paused") return '<span class="badge bg-warning text-dark">Paused</span>';
    if (status === "draft") return '<span class="badge bg-secondary">Draft</span>';
    if (status === "closed") return '<span class="badge bg-danger">Closed</span>';
    return `<span class="badge bg-secondary">${status}</span>`;
  }

  function renderJobPerformanceTable(data) {
    const wrapper = document.getElementById("job-performance-table");
    if (!wrapper) return;
    if (!data.job_performance || !data.job_performance.length) {
      wrapper.innerHTML = '<div class="text-muted-custom small py-3">No jobs posted yet.</div>';
      return;
    }

    const rows = data.job_performance
      .map((j) => {
        const isPaused = j.status === "paused";
        const isPublished = j.status === "published";

        let statusToggleBtn = "";
        if (isPublished) {
          statusToggleBtn = `<button class="btn btn-sm btn-outline-warning pause-job-btn me-1" data-job-id="${j.job_id}">⏸️ Pause</button>`;
        } else if (isPaused) {
          statusToggleBtn = `<button class="btn btn-sm btn-outline-success resume-job-btn me-1" data-job-id="${j.job_id}">▶️ Resume</button>`;
        }

        return `
          <tr>
            <td class="fw-bold text-dark">${j.job_title}</td>
            <td>${statusBadgeHtml(j.status)}</td>
            <td><span class="badge bg-light text-dark border px-2 py-1">${j.applications}</span></td>
            <td>${j.avg_match_score != null ? Math.round(j.avg_match_score) + "%" : "—"}</td>
            <td>${j.interviews_completed}</td>
            <td class="text-end">
              ${statusToggleBtn}
              <a href="job-applicants.html?job_id=${j.job_id}" class="btn btn-sm btn-outline-primary me-1">👤 Applicants</a>
              <button class="btn btn-sm btn-outline-danger delete-job-btn" data-job-id="${j.job_id}" data-job-title="${j.job_title}">🗑️ Delete</button>
            </td>
          </tr>
        `;
      })
      .join("");

    wrapper.innerHTML = `
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead>
            <tr>
              <th>Job Title</th>
              <th>Status</th>
              <th>Applications</th>
              <th>Avg Match</th>
              <th>Interviews</th>
              <th class="text-end">Actions</th>
            </tr>
          </thead>
          <tbody>${rows}</tbody>
        </table>
      </div>
    `;

    wrapper.querySelectorAll(".pause-job-btn").forEach((btn) => {
      btn.addEventListener("click", async () => {
        btn.disabled = true;
        try {
          await jobsAPI.update(btn.dataset.jobId, { status: "paused" });
          loadAnalytics();
        } catch (e) {
          alert(e.message);
          btn.disabled = false;
        }
      });
    });

    wrapper.querySelectorAll(".resume-job-btn").forEach((btn) => {
      btn.addEventListener("click", async () => {
        btn.disabled = true;
        try {
          await jobsAPI.update(btn.dataset.jobId, { status: "published" });
          loadAnalytics();
        } catch (e) {
          alert(e.message);
          btn.disabled = false;
        }
      });
    });

    wrapper.querySelectorAll(".delete-job-btn").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const title = btn.dataset.jobTitle || "this job";
        if (confirm(`Are you sure you want to permanently delete "${title}"? This action cannot be undone.`)) {
          btn.disabled = true;
          try {
            await jobsAPI.update(btn.dataset.jobId, { status: "closed" });
            if (jobsAPI.remove) await jobsAPI.remove(btn.dataset.jobId);
            loadAnalytics();
          } catch (e) {
            alert(e.message);
            btn.disabled = false;
          }
        }
      });
    });
  }

  async function getRecruiterMyJobs() {
    try {
      const BASE_URL = window.API_BASE_URL || "http://localhost:8000/api/v1";
      const token = localStorage.getItem("ar_access_token") || "";
      let res = await fetch(`${BASE_URL}/jobs/recruiter/my-jobs`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      if (!res.ok) {
        return (await jobsAPI.list()).data || [];
      }
      const data = await res.json();
      return data.data || [];
    } catch (e) {
      const fallback = await jobsAPI.list();
      return fallback.data || [];
    }
  }

  async function populateJobFilterDropdown() {
    if (!jobFilterSelect) return;
    try {
      const jobs = await getRecruiterMyJobs();
      jobFilterSelect.innerHTML = `<option value="all">All Posted Jobs (${jobs.length})</option>` +
        jobs.map(j => `<option value="${j.id}">${j.title} (${j.status})</option>`).join("");
    } catch (e) {
      console.warn("Could not load jobs list for filter dropdown:", e);
    }
  }

  async function renderScreeningStatsAndTopCandidates() {
    try {
      const myJobs = await getRecruiterMyJobs();
      if (!myJobs.length) {
        setStat("ats-stat-total", 0);
        setStat("ats-stat-eligible", 0);
        setStat("ats-stat-shortlisted", 0);
        setStat("ats-stat-review", 0);
        setStat("ats-stat-not-recommended", 0);
        const topBody = document.getElementById("top-candidates-body");
        if (topBody) {
          topBody.innerHTML = `<tr><td colspan="7" class="text-center py-4 text-muted">No active job requisitions posted yet.</td></tr>`;
        }
        return;
      }

      let totalApps = 0;
      let eligibleApps = 0;
      let shortlistedApps = 0;
      let reviewApps = 0;
      let notRecApps = 0;
      let allCandidateApps = [];

      for (const job of myJobs) {
        try {
          const appsRes = await jobsAPI.applications(job.id);
          const apps = appsRes.data || [];
          const minAts = job.min_ats_score || 60.0;

          apps.forEach((app) => {
            totalApps++;
            const score = app.ats_score || app.match_score || 0;
            const st = (app.status || "applied").toLowerCase();
            const recLower = (app.recommendation || "").toLowerCase();

            const isFailed = st === "rejected" || recLower.includes("failed");

            if (score >= minAts && !isFailed) eligibleApps++;
            if (st === "shortlisted") shortlistedApps++;
            if ((st === "applied" || st === "under_review") && score < minAts) reviewApps++;
            if (score < 40 || isFailed) notRecApps++;

            let recText = app.recommendation;
            if (!recText) {
              if (isFailed) recText = "Failed Assessment (Rejected)";
              else if (score >= 80) recText = "Priority Candidate";
              else if (score >= 60) recText = "Shortlist for Review";
              else if (score >= 40) recText = "Manual Review";
              else recText = "Not Recommended";
            }

            let matchedRole = app.matched_job_role || (app.match_breakdown && typeof app.match_breakdown === "object" ? app.match_breakdown.best_role_title : null);
            if (!matchedRole && app.match_breakdown && typeof app.match_breakdown === "string") {
              try {
                const parsedBk = JSON.parse(app.match_breakdown);
                matchedRole = parsedBk.best_role_title || parsedBk.matched_job_role;
              } catch (_) {}
            }

            allCandidateApps.push({
              application: app,
              job: job,
              candidateName: app.candidate_name || "Candidate",
              candidateEmail: app.candidate_email || "",
              atsScore: Math.round(score),
              jobMatchScore: Math.round(app.job_match_score || score),
              codingScore: app.coding_score != null ? Math.round(app.coding_score) : null,
              recommendation: recText,
              isFailed: isFailed,
              matchedRole: matchedRole || null,
            });
          });
        } catch (e) {
          // Continue loop if single job fails
        }
      }

      setStat("ats-stat-total", totalApps);
      setStat("ats-stat-eligible", eligibleApps);
      setStat("ats-stat-shortlisted", shortlistedApps);
      setStat("ats-stat-review", reviewApps);
      setStat("ats-stat-not-recommended", notRecApps);

      allCandidateApps.sort((a, b) => b.atsScore - a.atsScore);

      const topBody = document.getElementById("top-candidates-body");
      if (topBody) {
        if (!allCandidateApps.length) {
          topBody.innerHTML = `<tr><td colspan="8" class="text-center py-4 text-muted">No applicants submitted yet.</td></tr>`;
          return;
        }

        topBody.innerHTML = allCandidateApps.slice(0, 10).map((item, idx) => {
          let scoreBadge = "bg-success";
          if (item.atsScore < 40) scoreBadge = "bg-danger";
          else if (item.atsScore < 60) scoreBadge = "bg-warning text-dark";
          else if (item.atsScore < 80) scoreBadge = "bg-info text-white";

          let recBadge = '<span class="badge bg-secondary-subtle text-secondary px-2 py-1 rounded-pill small">' + item.recommendation + '</span>';
          if (item.isFailed) {
            recBadge = '<span class="badge bg-danger-subtle text-danger border border-danger px-2 py-1 rounded-pill small">❌ ' + item.recommendation + '</span>';
          } else if (item.recommendation.includes("Passed")) {
            recBadge = '<span class="badge bg-success-subtle text-success border border-success px-2 py-1 rounded-pill small">✅ ' + item.recommendation + '</span>';
          }

          const appId = item.application?.id || "";
          const jobId = item.job?.id || "";
          const jobTitle = item.job?.title || "Position";

          return `
            <tr>
              <td class="fw-bold text-secondary">#${idx + 1}</td>
              <td>
                <div class="fw-bold text-dark fs-6 cursor-pointer text-primary" onclick="window.openRecruiterAssessmentModal('${appId}', '${escapeHtml(item.candidateName)}', '${escapeHtml(jobTitle)}')">${item.candidateName}</div>
                <div class="text-muted small">${item.candidateEmail}</div>
              </td>
              <td class="text-secondary small fw-medium">
                <div class="fw-semibold text-dark">${jobTitle}</div>
                ${item.matchedRole && item.matchedRole !== jobTitle ? `<div class="mt-1"><span class="badge bg-primary-subtle text-primary border border-primary-subtle px-1.5 py-0.5 rounded" style="font-size: 0.72rem;">🎯 Matched: ${escapeHtml(item.matchedRole)}</span></div>` : ''}
              </td>
              <td>
                <span class="badge ${scoreBadge} px-3 py-1 rounded-pill fs-6 cursor-pointer" onclick="window.openRecruiterAssessmentModal('${appId}', '${escapeHtml(item.candidateName)}', '${escapeHtml(jobTitle)}')">${item.atsScore}%</span>
              </td>
              <td>
                <span class="badge bg-light text-dark border px-3 py-1 rounded-pill fs-6">${item.jobMatchScore}%</span>
              </td>
              <td>
                ${item.codingScore != null
                  ? `<span class="badge ${item.codingScore >= 60 ? 'bg-info' : 'bg-warning text-dark'} px-3 py-1 rounded-pill fs-6">${item.codingScore}%</span>`
                  : `<span class="text-muted small">—</span>`
                }
              </td>
              <td>
                ${recBadge}
              </td>
              <td class="text-end">
                <button class="btn btn-sm btn-info text-white fw-semibold view-assessment-btn me-1 shadow-sm" data-app-id="${appId}" data-candidate-name="${escapeHtml(item.candidateName)}" data-job-title="${escapeHtml(jobTitle)}">
                  📊 Score Breakdown
                </button>
                <a href="job-applicants.html?job_id=${jobId}" class="btn btn-sm btn-outline-primary fw-semibold px-3">
                  Inspect Applicants &rarr;
                </a>
              </td>
            </tr>
          `;
        }).join("");

        topBody.querySelectorAll(".view-assessment-btn").forEach((btn) => {
          btn.addEventListener("click", () => {
            openCandidateAssessmentModal(btn.dataset.appId, btn.dataset.candidateName, btn.dataset.jobTitle);
          });
        });
      }
    } catch (err) {
      console.warn("Could not load ATS screening summary:", err);
    }
  }

  let dashboardUploadedCandidatesStore = [];

  async function renderBulkUploadedCandidatesTable() {
    const tableBody = document.getElementById("bulk-uploaded-resumes-body");
    const countBadge = document.getElementById("bulk-table-count-badge");
    const searchInput = document.getElementById("dashboard-bulk-search");
    const roleFilter = document.getElementById("dashboard-bulk-role-filter");

    if (!tableBody) return;

    try {
      const BASE_URL = window.API_BASE_URL || (typeof API_BASE_URL !== "undefined" ? API_BASE_URL : "http://localhost:8000/api/v1");
      const token = (window.Session && window.Session.getAccessToken ? window.Session.getAccessToken() : "") ||
                    localStorage.getItem("ar_access_token") ||
                    localStorage.getItem("access_token") || "";

      let resp;
      try {
        resp = await fetch(`${BASE_URL}/resumes/recruiter/my-candidates`, {
          headers: token ? { Authorization: `Bearer ${token}` } : {},
        });
      } catch (fetchErr) {
        const altBase = BASE_URL.includes("localhost")
          ? BASE_URL.replace("localhost", "127.0.0.1")
          : BASE_URL.replace("127.0.0.1", "localhost");
        try {
          resp = await fetch(`${altBase}/resumes/recruiter/my-candidates`, {
            headers: token ? { Authorization: `Bearer ${token}` } : {},
          });
        } catch (e2) {
          throw new Error("Unable to connect to backend server. Please verify backend is running.");
        }
      }

      if (!resp.ok) {
        tableBody.innerHTML = `<tr><td colspan="7" class="text-center py-4 text-muted">Unable to load uploaded candidate resumes (Status: ${resp.status}).</td></tr>`;
        return;
      }

      const res = await resp.json();
      if (!res.success || !Array.isArray(res.data) || res.data.length === 0) {
        if (countBadge) countBadge.textContent = "0 Resumes";
        tableBody.innerHTML = `
          <tr>
            <td colspan="7" class="text-center py-5 text-muted">
              <div class="fs-1 mb-2">📤</div>
              <h6 class="fw-bold text-dark">No Bulk Resumes Uploaded Yet</h6>
              <p class="small text-muted mb-3" style="max-width: 480px; margin: 0 auto;">
                Upload candidate resumes in the Bulk Resume Upload section to let AI automatically parse qualifications, evaluate skills, and identify their best matching job role(s).
              </p>
              <button class="btn btn-sm btn-success fw-bold px-3 py-1.5 shadow-sm" data-bs-toggle="modal" data-bs-target="#bulkUploadModal">
                📤 Upload Resumes Now
              </button>
            </td>
          </tr>`;
        return;
      }

      dashboardUploadedCandidatesStore = res.data;
      if (countBadge) countBadge.textContent = `${dashboardUploadedCandidatesStore.length} Resumes Analyzed`;

      // Populate unique matched roles in filter dropdown
      if (roleFilter) {
        const uniqueRoles = Array.from(new Set(dashboardUploadedCandidatesStore.map(c => c.matched_job_role || c.best_suited_role?.best_role_title).filter(Boolean))).sort();
        const currentSelected = roleFilter.value;
        roleFilter.innerHTML = `<option value="all">All Matched Job Roles (${uniqueRoles.length})</option>` +
          uniqueRoles.map(r => `<option value="${escapeHtml(r)}" ${currentSelected === r ? "selected" : ""}>${escapeHtml(r)}</option>`).join("");
      }

      function filterAndRenderDashboardCandidates() {
        const query = (searchInput?.value || "").toLowerCase().trim();
        const selectedRole = (roleFilter?.value || "all");

        const filtered = dashboardUploadedCandidatesStore.filter(c => {
          const data = c.extracted_data || {};
          const matchedRole = (c.matched_job_role || c.best_suited_role?.best_role_title || data.matched_job_role || "").toLowerCase();
          
          if (selectedRole !== "all" && matchedRole !== selectedRole.toLowerCase()) {
            return false;
          }

          if (!query) return true;

          const name = (data.name || c.filename || "").toLowerCase();
          const email = (data.email || "").toLowerCase();
          const phone = (data.phone || "").toLowerCase();
          const skills = Array.isArray(data.skills) ? data.skills.join(" ").toLowerCase() : String(data.skills || "").toLowerCase();
          const location = (data.location || "").toLowerCase();
          const education = (data.education || "").toLowerCase();

          return name.includes(query) || email.includes(query) || phone.includes(query) ||
                 matchedRole.includes(query) || skills.includes(query) || location.includes(query) || education.includes(query);
        });

        renderDashboardUploadedTableRows(filtered);
      }

      // Attach search and filter event listeners if not already attached
      if (searchInput && !searchInput.dataset.bound) {
        searchInput.dataset.bound = "true";
        searchInput.addEventListener("input", filterAndRenderDashboardCandidates);
      }
      if (roleFilter && !roleFilter.dataset.bound) {
        roleFilter.dataset.bound = "true";
        roleFilter.addEventListener("change", filterAndRenderDashboardCandidates);
      }

      filterAndRenderDashboardCandidates();
    } catch (err) {
      console.warn("Could not load bulk uploaded candidates on recruiter dashboard:", err);
      tableBody.innerHTML = `<tr><td colspan="7" class="text-center py-4 text-danger">Error loading candidate resumes: ${escapeHtml(err.message || String(err))}</td></tr>`;
    }
  }

  function renderDashboardUploadedTableRows(candidates) {
    const tableBody = document.getElementById("bulk-uploaded-resumes-body");
    if (!tableBody) return;

    if (candidates.length === 0) {
      tableBody.innerHTML = `<tr><td colspan="7" class="text-center py-4 text-muted">No candidates matched the current search or filter.</td></tr>`;
      return;
    }

    tableBody.innerHTML = candidates.map((r, index) => {
      const data = r.extracted_data || {};
      const score = Math.round(r.overall_match_score || 0);

      const matchedRole = r.matched_job_role || r.best_suited_role?.best_role_title || data.matched_job_role || data.current_role || "Candidate Profile";
      const roleScore = r.best_suited_role?.best_match_score || score;
      const isActiveJob = r.best_suited_role?.is_active_job;
      const activePill = isActiveJob ? `<span class="badge bg-success text-white small" style="font-size: 0.65rem;" title="Matches an open job opening you posted">🏢 Open Job</span>` : '';

      // Secondary matched roles
      const matchedRolesList = r.matched_roles || r.best_suited_role?.matched_roles || data.matched_roles || [];
      const secondaryRoles = matchedRolesList
        .filter(mr => mr.title && mr.title.toLowerCase() !== matchedRole.toLowerCase())
        .slice(0, 2);

      let secondaryRolesHtml = "";
      if (secondaryRoles.length > 0) {
        secondaryRolesHtml = `<div class="mt-1 d-flex flex-wrap gap-1 align-items-center">
          <span class="text-muted" style="font-size: 0.7rem;">Also fits:</span>
          ${secondaryRoles.map(sr => `<span class="badge bg-secondary-subtle text-dark border border-secondary-subtle" style="font-size: 0.7rem;" title="${escapeHtml(sr.explanation || '')}">${escapeHtml(sr.title)} (${sr.score}%)</span>`).join("")}
        </div>`;
      }

      const roleCell = `
        <div class="d-flex flex-column align-items-start">
          <div class="d-flex align-items-center gap-1 flex-wrap">
            <span class="badge bg-primary-subtle text-primary border border-primary-subtle px-2.5 py-1.5 fs-6 fw-bold shadow-sm d-inline-flex align-items-center gap-1" title="${escapeHtml(r.best_suited_role?.explanation || 'Best suited job position identified for candidate')}">
              <span>🎯</span> ${escapeHtml(matchedRole)}
            </span>
            ${activePill}
          </div>
          <div class="small text-muted mt-1" style="font-size: 0.75rem;">Fit: <strong class="text-dark">${roleScore}% Match</strong></div>
          ${secondaryRolesHtml}
        </div>
      `;

      // Rank Badge
      let rankBadge = `<span class="badge bg-secondary">#${r.rank || index + 1}</span>`;
      if (index === 0 && score >= 50) {
        rankBadge = `<span class="badge bg-warning text-dark fw-bold shadow-sm">🏆 #1 Match</span>`;
      }

      // Deduplication Badge
      let dedupBadge = `<span class="badge bg-success-subtle text-success border border-success">✨ New</span>`;
      if (r.is_duplicate) {
        dedupBadge = `<span class="badge bg-warning-subtle text-dark border border-warning">🔄 Duplicate</span>`;
      }

      // Skills
      const skillsArr = Array.isArray(data.skills) ? data.skills : (data.skills ? String(data.skills).split(",") : []);
      const topSkillsBadges = skillsArr.slice(0, 3).map(s => `<span class="badge bg-primary-subtle text-primary border border-primary-subtle me-1 mb-1">${escapeHtml(s.trim())}</span>`).join("");
      const remainingSkillsCount = skillsArr.length > 3 ? `<span class="badge bg-light text-muted border">+${skillsArr.length - 3}</span>` : "";

      // Score color
      let scoreBadgeClass = "bg-success";
      if (score < 50) scoreBadgeClass = "bg-danger";
      else if (score < 70) scoreBadgeClass = "bg-warning text-dark";
      else if (score < 85) scoreBadgeClass = "bg-info text-dark";

      // Education & Location
      const eduStr = data.education ? String(data.education).replace(/[\n\r]/g, " ").trim() : "Education not listed";
      const locStr = data.location ? String(data.location).replace(/[\n\r]/g, " ").trim() : "Location not listed";

      return `
        <tr>
          <td>
            ${rankBadge}
            <div class="mt-1">${dedupBadge}</div>
          </td>
          <td>
            <div class="fw-bold text-dark fs-6 mb-0">${escapeHtml(data.name || r.filename)}</div>
            <div class="small text-muted"><a href="mailto:${escapeHtml(data.email || '')}" class="text-decoration-none text-muted">${escapeHtml(data.email || '—')}</a></div>
            <div class="small text-muted">${escapeHtml(data.phone || '—')}</div>
            <div class="small font-monospace text-muted mt-0.5">📄 ${escapeHtml(r.filename)}</div>
          </td>
          <td>
            ${roleCell}
          </td>
          <td>
            <div class="mb-1">${topSkillsBadges} ${remainingSkillsCount}</div>
            <div class="small text-muted">Exp: <strong>${data.experience_years ? data.experience_years + ' yrs' : 'Not specified'}</strong></div>
          </td>
          <td style="max-width: 200px;">
            <div class="small fw-semibold text-dark text-truncate" title="${escapeHtml(eduStr)}">
              🎓 ${escapeHtml(eduStr.length > 35 ? eduStr.substring(0, 32) + '...' : eduStr)}
            </div>
            <div class="small text-muted text-truncate" title="${escapeHtml(locStr)}">
              📍 ${escapeHtml(locStr.length > 30 ? locStr.substring(0, 27) + '...' : locStr)}
            </div>
          </td>
          <td>
            <div class="d-flex align-items-center gap-2">
              <span class="badge ${scoreBadgeClass} px-2.5 py-1 fs-6">${score}%</span>
            </div>
            <div class="progress mt-1" style="height: 5px; min-width: 60px;">
              <div class="progress-bar ${scoreBadgeClass}" style="width: ${score}%;"></div>
            </div>
          </td>
          <td class="text-end">
            <div class="d-flex flex-column gap-1">
              <button type="button" class="btn btn-sm btn-success py-1 px-2 fw-bold dash-view-cand-btn" data-candidate-id="${r.candidate_id}" style="font-size: 0.75rem;">👤 View Details</button>
              <div class="d-flex gap-1 justify-content-end">
                <button type="button" class="btn btn-sm btn-outline-primary py-0 px-2 fw-semibold dash-view-ats-btn" data-candidate-id="${r.candidate_id}" style="font-size: 0.72rem;">📊 ATS Match</button>
                <button type="button" class="btn btn-sm btn-outline-danger py-0 px-2 fw-semibold dash-delete-cand-btn" data-candidate-id="${r.candidate_id}" data-candidate-name="${escapeHtml(data.name || r.filename)}" style="font-size: 0.72rem;">🗑️ Delete</button>
              </div>
            </div>
          </td>
        </tr>
      `;
    }).join("");

    // Wire up buttons to bulk modal handlers
    tableBody.querySelectorAll(".dash-view-cand-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const cId = btn.dataset.candidateId;
        const cand = dashboardUploadedCandidatesStore.find(c => c.candidate_id === cId);
        if (cand && typeof window.showBulkCandidateDetailsModal === "function") {
          window.showBulkCandidateDetailsModal(cand);
        }
      });
    });

    tableBody.querySelectorAll(".dash-view-ats-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const cId = btn.dataset.candidateId;
        const cand = dashboardUploadedCandidatesStore.find(c => c.candidate_id === cId);
        if (cand && typeof window.showBulkAtsModal === "function") {
          window.showBulkAtsModal(cand);
        }
      });
    });

    tableBody.querySelectorAll(".dash-delete-cand-btn").forEach(btn => {
      btn.addEventListener("click", async () => {
        const cId = btn.dataset.candidateId;
        const name = btn.dataset.candidateName;
        if (typeof window.deleteBulkCandidate === "function") {
          await window.deleteBulkCandidate(cId, name);
          renderBulkUploadedCandidatesTable();
        }
      });
    });
  }

  window.refreshRecruiterDashboardUploadedResumes = renderBulkUploadedCandidatesTable;
  window.renderBulkUploadedCandidatesTable = renderBulkUploadedCandidatesTable;

  function escapeHtml(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function generateAssessmentBreakdownHTML(session, app = {}) {
    const channel = (session?.channel || "WhatsApp").toUpperCase() + " SCREENING";
    const candidateName = session?.candidate_name || app?.candidate_name || "Candidate Profile";
    const jobTitle = session?.job_title || app?.job_title || "Target Position";

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
                <li><strong>Option 2 (Request Re-Assessment):</strong> Reset or request the candidate to re-take the pre-screening questionnaire.</li>
                <li><strong>Option 3 (Confirm Rejection):</strong> Leave status as Rejected to generate candidate feedback report.</li>
              </ul>
            </div>
            ${appId ? `
            <div class="d-flex flex-wrap gap-2">
              <button type="button" class="btn btn-sm btn-info text-white fw-bold px-3 shadow-sm" onclick="window.overrideCandidateStatus && window.overrideCandidateStatus('${appId}', 'shortlisted', 'Recruiter Override from Assessment Breakdown')">
                ⭐ Save Override &amp; Shortlist
              </button>
              <button type="button" class="btn btn-sm btn-success fw-bold px-3 shadow-sm" onclick="window.overrideCandidateStatus && window.overrideCandidateStatus('${appId}', 'selected', 'Recruiter Selection from Assessment Breakdown')">
                🎉 Select Candidate (Offer)
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
      <div class="assessment-breakdown-container">
        <!-- Header Banner -->
        <div class="card border-0 p-4 p-md-5 mb-4 shadow-sm" style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #ffffff; border-radius: 16px;">
          <div class="row align-items-center">
            <div class="col-lg-8">
              <span class="badge px-3 py-2 text-uppercase mb-3 fw-bold text-white shadow-sm" style="background: linear-gradient(135deg, #25d366 0%, #128c7e 100%); letter-spacing: 0.05em; font-size: 0.75rem; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.25); box-shadow: 0 2px 8px rgba(37, 211, 102, 0.35);">💬 ${channel}</span>
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
        <h4 class="fw-bold mb-3 d-flex align-items-center gap-2 text-dark">
          <span class="text-primary">📈</span> Score Breakdown
        </h4>
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
        <div class="card border-0 shadow-sm mb-3" style="border-radius: 12px; background: #ffffff;">
          <div class="card-body p-4">
            <h5 class="fw-bold mb-3 d-flex align-items-center gap-2 text-dark">
              <span class="text-primary">🤖</span> AI Evaluation Summary
            </h5>
            <div class="text-secondary" style="line-height: 1.6;">
              ${aiSummary.split('\n').map(line => `<p class="mb-1">${escapeHtml(line)}</p>`).join('')}
            </div>
          </div>
        </div>

        <!-- Recruiter Status Action Bar -->
        ${appId ? `
        <div class="card border-0 shadow-sm mb-3" style="border-radius: 12px; background: #f8fafc;">
          <div class="card-body p-3 d-flex justify-content-between align-items-center flex-wrap gap-2">
            <div>
              <span class="text-muted small fw-bold text-uppercase">Update Application Status:</span>
            </div>
            <div class="d-flex flex-wrap gap-2">
              <button type="button" class="btn btn-sm btn-info text-white fw-bold px-3 shadow-sm" onclick="window.overrideCandidateStatus && window.overrideCandidateStatus('${appId}', 'shortlisted', 'Recruiter Shortlist')">
                ⭐ Shortlist Candidate
              </button>
              <button type="button" class="btn btn-sm btn-success text-white fw-bold px-3 shadow-sm" onclick="window.overrideCandidateStatus && window.overrideCandidateStatus('${appId}', 'selected', 'Recruiter Selection')">
                🎉 Select Candidate (Offer)
              </button>
              <button type="button" class="btn btn-sm btn-outline-danger fw-semibold px-3" onclick="window.overrideCandidateStatus && window.overrideCandidateStatus('${appId}', 'rejected', 'Recruiter Rejection')">
                ❌ Reject
              </button>
            </div>
          </div>
        </div>
        ` : ''}
      </div>
    `;
  }

  async function openCandidateAssessmentModal(appId, candidateName, jobTitle) {
    const modalEl = document.getElementById("recruiterAssessmentModal");
    const modalBody = document.getElementById("recruiter-assessment-modal-body");
    if (!modalEl || !modalBody) return;

    modalBody.innerHTML = `
      <div class="text-center py-5">
        <div class="spinner-border text-primary" role="status"></div>
        <p class="mt-2 text-muted">Loading candidate assessment details...</p>
      </div>
    `;

    if (window.bootstrap) {
      const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
      modal.show();
    }

    try {
      let session = null;
      try {
        const res = await screeningAPI.getByApplication(appId);
        session = res.data || res;
      } catch (err) {
        // Fallback session object
      }

      modalBody.innerHTML = generateAssessmentBreakdownHTML(session, {
        candidate_name: candidateName,
        job_title: jobTitle,
      });
    } catch (err) {
      modalBody.innerHTML = `
        <div class="alert alert-danger">
          Failed to load candidate assessment score: ${escapeHtml(err.message || String(err))}
        </div>
      `;
    }
  }

  window.openRecruiterAssessmentModal = openCandidateAssessmentModal;

  window.overrideCandidateStatus = async function (appId, newStatus, reason = "") {
    if (!appId) {
      alert("Application ID is missing.");
      return;
    }
    try {
      await applicationsAPI.updateStatus(appId, newStatus, reason);
      const emailNotice = (newStatus === "selected" || newStatus === "shortlisted") 
        ? " An automated email notification has been dispatched to the candidate's registered email." 
        : "";
      alert(`Candidate application status successfully updated to '${newStatus.toUpperCase()}'!${emailNotice}`);
      const modalEl = document.getElementById("recruiterAssessmentModal") || document.getElementById("applicantDetailModal");
      if (modalEl && window.bootstrap) {
        const modal = bootstrap.Modal.getInstance(modalEl);
        if (modal) modal.hide();
      }
      if (typeof loadAnalytics === "function") loadAnalytics();
      if (typeof renderScreeningStatsAndTopCandidates === "function") renderScreeningStatsAndTopCandidates();
    } catch (err) {
      alert("Failed to update status: " + (err?.message || String(err)));
    }
  };

  function calculateDateFilterIso() {
    if (!dateFilterSelect) return { start_date: null, end_date: null };
    const val = dateFilterSelect.value;
    if (val === "all") return { start_date: null, end_date: null };

    const now = new Date();
    let days = 30;
    if (val === "7d") days = 7;
    if (val === "30d") days = 30;
    if (val === "90d") days = 90;

    const startDate = new Date(now.getTime() - days * 24 * 60 * 60 * 1000);
    return {
      start_date: startDate.toISOString(),
      end_date: now.toISOString(),
    };
  }

  async function loadAnalytics() {
    try {
      const jobIdVal = jobFilterSelect ? jobFilterSelect.value : "all";
      const statusVal = statusFilterSelect ? statusFilterSelect.value : "all";
      const dateRange = calculateDateFilterIso();

      const params = {};
      if (jobIdVal && jobIdVal !== "all") params.job_id = jobIdVal;
      if (statusVal && statusVal !== "all") params.status = statusVal;
      if (dateRange.start_date) params.start_date = dateRange.start_date;
      if (dateRange.end_date) params.end_date = dateRange.end_date;

      const res = await analyticsAPI.recruiter(params);
      const data = res.data;

      setStat("stat-total-jobs", data.total_jobs);
      setStat("stat-total-candidates", data.total_candidates);
      setStat("stat-applications", data.total_applications);
      setStat("stat-shortlisted", data.shortlisted_count);
      setStat("stat-interviews", data.interview_count);
      setStat("stat-selected", data.hired_count ?? data.selected_count);
      setStat("stat-conversion-rate", `${data.conversion_rate ?? 0}%`);
      setStat("stat-avg-match-score", data.avg_match_score != null ? `${Math.round(data.avg_match_score)}%` : "—");
      setStat("stat-avg-interview-score", data.avg_interview_score != null ? `${Math.round(data.avg_interview_score)}%` : "—");

      try { renderHiringFunnelChart(data); } catch (e) { console.warn("Hiring funnel chart error:", e); }
      try { renderMatchDistributionChart(data); } catch (e) { console.warn("Match distribution chart error:", e); }
      try { renderMissingSkillsChart(data); } catch (e) { console.warn("Missing skills chart error:", e); }
      try { renderTopSkillsChart(data); } catch (e) { console.warn("Top skills chart error:", e); }
      try { renderApplicationsByJobChart(data); } catch (e) { console.warn("Applications by job chart error:", e); }
      try { renderInterviewScoresChart(data); } catch (e) { console.warn("Interview scores chart error:", e); }
      try { renderJobPerformanceTable(data); } catch (e) { console.warn("Job performance table error:", e); }

      try { await renderScreeningStatsAndTopCandidates(); } catch (e) { console.warn("Screening stats error:", e); }
    } catch (err) {
      console.warn("Analytics loading notice:", err);
    }
  }

  // Setup Event Listeners for Filters
  if (jobFilterSelect) jobFilterSelect.addEventListener("change", loadAnalytics);
  if (dateFilterSelect) dateFilterSelect.addEventListener("change", loadAnalytics);
  if (statusFilterSelect) statusFilterSelect.addEventListener("change", loadAnalytics);

  // ==========================================
  // Student Career Guidance & Learning Activity Monitor
  // (View and Monitor Only — No Question Generation)
  // ==========================================
  function escapeHtml(str) {
    if (str == null) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  async function loadStudentLearningMonitor() {
    const searchInput = document.getElementById("sm-filter-search");
    const perfSelect = document.getElementById("sm-filter-performance");
    const trendSelect = document.getElementById("sm-filter-trend");
    const tableBody = document.getElementById("sm-students-table-body");

    const search = searchInput ? searchInput.value.trim() : "";
    const performance = perfSelect ? perfSelect.value : "all";
    const trend = trendSelect ? trendSelect.value : "all";

    if (tableBody) {
      tableBody.innerHTML = `
        <tr>
          <td colspan="8" class="text-center py-4 text-muted">
            <div class="spinner-border spinner-border-sm text-success me-2" role="status"></div>
            Loading student career guidance &amp; aptitude telemetry...
          </td>
        </tr>
      `;
    }

    try {
      const res = await (window.studentAPI || api.student).getRecruiterMonitor({ search, performance, trend });
      const payload = res.data || res;
      const summary = payload.summary || {};
      const students = payload.students || [];

      renderStudentLearningKPIs(summary);
      renderStudentLearningTable(students);
    } catch (err) {
      console.error("Failed to load student learning monitor:", err);
      if (tableBody) {
        tableBody.innerHTML = `
          <tr>
            <td colspan="8" class="text-center py-4 text-danger">
              ⚠️ Failed to load student learning telemetry: ${escapeHtml(err.message || String(err))}
            </td>
          </tr>
        `;
      }
    }
  }

  function renderStudentLearningKPIs(summary) {
    if (!summary) return;
    const totalEl = document.getElementById("sm-kpi-total-students");
    const activeEl = document.getElementById("sm-kpi-active-learners");
    const avgScoreEl = document.getElementById("sm-kpi-avg-score");
    const testsCountEl = document.getElementById("sm-kpi-tests-count");
    const avgRoadmapEl = document.getElementById("sm-kpi-avg-roadmap");
    const wellBadge = document.getElementById("sm-kpi-well-badge");
    const modBadge = document.getElementById("sm-kpi-mod-badge");
    const impBadge = document.getElementById("sm-kpi-imp-badge");
    const consistentEl = document.getElementById("sm-kpi-consistent-learners");

    if (totalEl) totalEl.textContent = summary.total_students ?? 0;
    if (activeEl) activeEl.textContent = `${summary.active_learners_count ?? 0} active learners`;
    if (avgScoreEl) avgScoreEl.textContent = `${summary.avg_aptitude_score ?? 0}%`;
    if (testsCountEl) testsCountEl.textContent = `${summary.active_learners_count ?? 0} active student learners`;
    if (avgRoadmapEl) avgRoadmapEl.textContent = `${summary.avg_roadmap_progress ?? 0}%`;
    if (wellBadge) wellBadge.textContent = `${summary.performing_well_count ?? 0} Well`;
    if (modBadge) modBadge.textContent = `${summary.moderate_count ?? 0} Moderate`;
    if (impBadge) impBadge.textContent = `${summary.needs_improvement_count ?? 0} Needs Imp.`;
    if (consistentEl) consistentEl.textContent = `${summary.consistent_learners_count ?? 0} consistent daily learners`;
  }

  function renderStudentLearningTable(students) {
    const tableBody = document.getElementById("sm-students-table-body");
    if (!tableBody) return;

    if (!students || students.length === 0) {
      tableBody.innerHTML = `
        <tr>
          <td colspan="9" class="text-center py-5 text-muted">
            <div class="mb-2 fs-2">🎓</div>
            <div class="fw-semibold">No student learning activities found</div>
            <small class="text-muted">Try adjusting your search criteria or filter options.</small>
          </td>
        </tr>
      `;
      return;
    }

    const rows = students.map((s) => {
      // 1. Student Academic Details
      const collegeDisplay = s.college_name ? escapeHtml(s.college_name) : "College not set";
      const branchDisplay = [s.degree, s.branch].filter(Boolean).map(escapeHtml).join(" - ");

      // 2. Active Course & Phase
      const courseIcon = s.active_course_icon || "📘";
      const courseName = s.active_course_name || "Software Engineering Track";
      const phaseName = s.active_phase_name || "Phase 1: Foundations";
      const sprintStatus = s.sprint_status || "Sprint Active: Day 1 of 90";

      const courseHtml = `
        <div>
          <div class="fw-bold text-dark d-flex align-items-center gap-1.5" title="${escapeHtml(courseName)}">
            <span>${courseIcon}</span>
            <span class="text-truncate" style="max-width: 190px;">${escapeHtml(courseName)}</span>
          </div>
          <div class="d-flex align-items-center gap-1 mt-1 flex-wrap">
            <span class="badge bg-indigo-subtle text-primary border" style="font-size: 0.68rem;">
              ${escapeHtml(phaseName)}
            </span>
            <span class="badge bg-light text-secondary border" style="font-size: 0.68rem;">
              ${escapeHtml(sprintStatus.replace("Sprint Active: ", ""))}
            </span>
          </div>
        </div>
      `;

      // 3. Topic Mastery Breakdown (Completed / Ongoing / Pending)
      const doneCount = s.completed_topics_count || 0;
      const ongoingCount = s.ongoing_topics_count || 0;
      const pendingCount = s.pending_topics_count || Math.max(0, (s.total_course_topics || 50) - doneCount - ongoingCount);
      const totalCount = Math.max(1, doneCount + ongoingCount + pendingCount);
      const donePct = Math.round((doneCount / totalCount) * 100);
      const ongoingPct = Math.round((ongoingCount / totalCount) * 100);
      const pendingPct = Math.max(0, 100 - donePct - ongoingPct);

      const topicBreakdownHtml = `
        <div>
          <div class="d-flex align-items-center gap-1 small mb-1 flex-wrap">
            <span class="badge bg-success-subtle text-success border border-success px-1.5 py-0.5" style="font-size: 0.68rem;" title="Completed Topics">✓ ${doneCount} Done</span>
            <span class="badge bg-warning-subtle text-dark border border-warning px-1.5 py-0.5" style="font-size: 0.68rem;" title="Ongoing Topics">⚡ ${ongoingCount} Active</span>
            <span class="badge bg-light text-secondary border px-1.5 py-0.5" style="font-size: 0.68rem;" title="Pending Topics">⏳ ${pendingCount}</span>
          </div>
          <div class="progress" style="height: 6px; border-radius: 999px; overflow: hidden; background: #e2e8f0;" title="${doneCount} Done, ${ongoingCount} Ongoing, ${pendingCount} Pending">
            <div class="progress-bar bg-success" style="width: ${donePct}%;"></div>
            <div class="progress-bar bg-warning" style="width: ${ongoingPct}%;"></div>
            <div class="progress-bar bg-secondary-subtle" style="width: ${pendingPct}%;"></div>
          </div>
          <small class="text-muted" style="font-size: 0.68rem;">${doneCount}/${totalCount} topics mastered</small>
        </div>
      `;

      // 4. Learning / Course Progress
      const courseProgress = Math.round(s.course_progress_percentage || s.roadmap_progress || 0);
      const rmBarColor = courseProgress >= 70 ? "bg-success" : courseProgress >= 40 ? "bg-info" : "bg-warning";
      const progressHtml = `
        <div>
          <div class="d-flex align-items-center justify-content-between small mb-1">
            <span class="fw-bold fs-6 text-dark">${courseProgress}%</span>
            <span class="badge ${courseProgress > 0 ? 'bg-primary-subtle text-primary' : 'bg-light text-secondary'} border" style="font-size: 0.68rem;">
              ${courseProgress >= 100 ? 'Completed' : courseProgress > 0 ? 'In Progress' : 'Not Started'}
            </span>
          </div>
          <div class="progress mb-1" style="height: 6px; border-radius: 999px;">
            <div class="progress-bar ${rmBarColor}" style="width: ${courseProgress}%;"></div>
          </div>
          <small class="text-muted" style="font-size: 0.68rem;">⏱️ ${s.total_time_spent_mins || 0}m study time</small>
        </div>
      `;

      // 5. Aptitude & Coding Performance
      const aptitudeScoreClass = s.avg_score >= 70 ? "bg-success" : s.avg_score >= 50 ? "bg-warning text-dark" : "bg-danger";
      const codingScoreClass = s.avg_coding_score >= 70 ? "bg-primary" : s.avg_coding_score >= 50 ? "bg-info text-dark" : "bg-secondary";

      const scoresHtml = `
        <div>
          <div class="d-flex align-items-center gap-1 mb-1">
            <span class="badge ${s.tests_count > 0 ? aptitudeScoreClass : 'bg-light text-muted border'} px-1.5 py-0.5" style="font-size: 0.7rem;">
              ${s.tests_count > 0 ? `${s.avg_score}% Aptitude` : 'No Tests'}
            </span>
            <span class="text-muted small" style="font-size: 0.68rem;">(${s.tests_count} test${s.tests_count === 1 ? '' : 's'})</span>
          </div>
          <div class="d-flex align-items-center gap-1">
            <span class="badge ${s.coding_assessments_count > 0 ? codingScoreClass : 'bg-light text-muted border'} px-1.5 py-0.5" style="font-size: 0.7rem;">
              ${s.coding_assessments_count > 0 ? `${s.avg_coding_score}% Coding` : 'No Coding'}
            </span>
            <span class="text-muted small" style="font-size: 0.68rem;">(${s.coding_assessments_count || 0} labs)</span>
          </div>
        </div>
      `;

      // 6. Consistency
      const streakHtml = s.daily_streak > 0 
        ? `<div class="fw-bold text-danger small">🔥 ${s.daily_streak}d Streak</div>`
        : `<div class="text-muted small">No streak</div>`;
      const consistencyHtml = `
        <div>
          ${streakHtml}
          <span class="badge ${s.consistency_badge || 'bg-light text-secondary'} small mt-0.5" style="font-size: 0.68rem;">${escapeHtml(s.consistency_label || 'Inactive')}</span>
        </div>
      `;

      // 7. Trend
      let trendHtml = "";
      if (s.trend === "improving") {
        trendHtml = `<span class="badge bg-success-subtle text-success border border-success fw-bold px-2 py-1" title="${escapeHtml(s.improvement_notes || 'Scores are improving across recent assessments')}">↗ Improving</span>`;
      } else if (s.trend === "declining") {
        trendHtml = `<span class="badge bg-danger-subtle text-danger border border-danger fw-bold px-2 py-1" title="${escapeHtml(s.improvement_notes || 'Scores are softening, requires guidance')}">↘ Declining</span>`;
      } else if (s.trend === "steady") {
        trendHtml = `<span class="badge bg-primary-subtle text-primary border border-primary fw-bold px-2 py-1">➔ Steady</span>`;
      } else {
        trendHtml = `<span class="badge bg-light text-muted border px-2 py-1">Baseline</span>`;
      }

      // 8. Performance Status & Readiness Rating
      let statusBadge = "";
      if (s.performance_status === "Performing Well") {
        statusBadge = `<span class="badge bg-success text-white px-2 py-1 rounded-pill fw-bold" style="font-size: 0.7rem;">Performing Well ✅</span>`;
      } else if (s.performance_status === "Moderate Progress") {
        statusBadge = `<span class="badge bg-warning text-dark px-2 py-1 rounded-pill fw-bold" style="font-size: 0.7rem;">Moderate Progress ⚠️</span>`;
      } else {
        statusBadge = `<span class="badge bg-danger text-white px-2 py-1 rounded-pill fw-bold" style="font-size: 0.7rem;">Needs Support ❌</span>`;
      }

      const readinessScore = s.placement_readiness_score || 50;
      const readinessBadgeClass = readinessScore >= 75 ? "bg-success-subtle text-success border-success" : readinessScore >= 50 ? "bg-primary-subtle text-primary border-primary" : "bg-warning-subtle text-dark border-warning";

      const readinessHtml = `
        <div>
          ${statusBadge}
          <div class="mt-1">
            <span class="badge ${readinessBadgeClass} border small" style="font-size: 0.68rem;">
              Readiness: <strong>${readinessScore}/100</strong>
            </span>
          </div>
        </div>
      `;

      return `
        <tr>
          <td>
            <div class="d-flex align-items-center gap-2">
              <div class="rounded-circle bg-success text-white d-flex align-items-center justify-content-center fw-bold shadow-sm" style="width: 38px; height: 38px; min-width: 38px; font-size: 14px;">
                ${escapeHtml((s.name || "S").charAt(0).toUpperCase())}
              </div>
              <div class="overflow-hidden" style="max-width: 210px;">
                <div class="fw-bold text-dark text-truncate">${escapeHtml(s.name)}</div>
                <div class="text-muted small text-truncate">${escapeHtml(s.email)}</div>
                <div class="text-secondary small text-truncate" title="${collegeDisplay}">
                  🏛️ ${collegeDisplay} ${branchDisplay ? `(${branchDisplay})` : ''}
                </div>
              </div>
            </div>
          </td>
          <td>${courseHtml}</td>
          <td>${topicBreakdownHtml}</td>
          <td>${progressHtml}</td>
          <td>${scoresHtml}</td>
          <td>${consistencyHtml}</td>
          <td>${trendHtml}</td>
          <td>${readinessHtml}</td>
          <td class="text-end">
            <button class="btn btn-sm btn-outline-success fw-bold text-nowrap d-inline-flex align-items-center gap-1 shadow-sm" onclick="window.openStudentActivityDetailModal('${s.user_id}')">
              <span>🔍</span> Track Learning
            </button>
          </td>
        </tr>
      `;
    }).join("");

    tableBody.innerHTML = rows;
  }

  async function openStudentActivityDetailModal(userId) {
    const modalEl = document.getElementById("studentActivityDetailModal");
    const modalBody = document.getElementById("sad-modal-body");
    const modalName = document.getElementById("sad-modal-name");
    const modalSubtitle = document.getElementById("sad-modal-subtitle");
    if (!modalEl || !modalBody) return;

    modalBody.innerHTML = `
      <div class="text-center py-5">
        <div class="spinner-border text-success" role="status"></div>
        <p class="mt-2 text-muted">Loading real-time learning telemetry and progress...</p>
      </div>
    `;

    if (window.bootstrap) {
      const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
      modal.show();
    }

    try {
      const res = await (window.studentAPI || api.student).getStudentActivityDetail(userId);
      const s = res.data || res;

      if (modalName) modalName.textContent = `${s.name} — Real-Time Learning Telemetry & Performance`;
      if (modalSubtitle) modalSubtitle.textContent = `${s.college_name || 'Academic Institution'} • ${s.degree || 'Student'} ${s.branch ? '(' + s.branch + ')' : ''} • Target Role: ${s.target_role || 'General'}`;

      // 1. Status Badges
      const statusBadge = s.performance_status === "Performing Well"
        ? '<span class="badge bg-success text-white px-3 py-1.5 rounded-pill fs-6">Performing Well ✅</span>'
        : s.performance_status === "Moderate Progress"
        ? '<span class="badge bg-warning text-dark px-3 py-1.5 rounded-pill fs-6">Moderate Progress ⚠️</span>'
        : '<span class="badge bg-danger text-white px-3 py-1.5 rounded-pill fs-6">Needs Improvement ❌</span>';

      const trendBadge = s.trend === "improving"
        ? '<span class="badge bg-success-subtle text-success border border-success fw-bold px-3 py-1.5 rounded-pill">↗ Score Trajectory Improving</span>'
        : s.trend === "declining"
        ? '<span class="badge bg-danger-subtle text-danger border border-danger fw-bold px-3 py-1.5 rounded-pill">↘ Score Trajectory Declining</span>'
        : '<span class="badge bg-primary-subtle text-primary border border-primary fw-bold px-3 py-1.5 rounded-pill">➔ Steady Trajectory</span>';

      const readinessScore = s.placement_readiness_score || 50;

      // 2. Build Topic Mastery Lists (Completed Correctly, Ongoing, Pending)
      const completedTopicsList = s.completed_topics || [];
      const ongoingTopicsList = s.ongoing_topics || [];
      const pendingTopicsList = s.pending_topics || [];

      // Completed Topics HTML
      let completedHtml = "";
      if (completedTopicsList.length > 0) {
        completedHtml = completedTopicsList.map(t => `
          <div class="p-2.5 rounded-3 mb-2 bg-success-subtle border border-success-subtle d-flex justify-content-between align-items-center">
            <div class="d-flex align-items-center gap-2">
              <span class="text-success fs-5">✓</span>
              <div>
                <div class="fw-bold text-dark small">${escapeHtml(t.title || 'Topic')}</div>
                <div class="text-muted" style="font-size: 0.72rem;">${escapeHtml(t.phase_name || 'Phase')} • ${t.hours || 4} hrs • Completed Correctly</div>
              </div>
            </div>
            <span class="badge bg-success text-white rounded-pill px-2.5 py-1 small">100% Mastered</span>
          </div>
        `).join("");
      } else {
        completedHtml = `<div class="p-4 text-center text-muted border rounded-3 bg-light">No completed topics yet. Candidate is currently beginning coursework.</div>`;
      }

      // Ongoing Topics HTML
      let ongoingHtml = "";
      if (ongoingTopicsList.length > 0) {
        ongoingHtml = ongoingTopicsList.map(t => `
          <div class="p-2.5 rounded-3 mb-2 bg-warning-subtle border border-warning-subtle d-flex justify-content-between align-items-center">
            <div class="d-flex align-items-center gap-2">
              <span class="text-warning-emphasis fs-5">⚡</span>
              <div>
                <div class="fw-bold text-dark small">${escapeHtml(t.title || 'Topic')}</div>
                <div class="text-muted" style="font-size: 0.72rem;">${escapeHtml(t.phase_name || 'Phase')} • In Progress</div>
              </div>
            </div>
            <div style="min-width: 120px;">
              <div class="d-flex justify-content-between small text-muted mb-1" style="font-size: 0.7rem;">
                <span>Active</span>
                <span>${t.progress_percent || 50}%</span>
              </div>
              <div class="progress" style="height: 5px;">
                <div class="progress-bar bg-warning" style="width: ${t.progress_percent || 50}%;"></div>
              </div>
            </div>
          </div>
        `).join("");
      } else {
        ongoingHtml = `<div class="p-4 text-center text-muted border rounded-3 bg-light">No active in-progress topics at this moment.</div>`;
      }

      // Pending Topics HTML
      let pendingHtml = "";
      if (pendingTopicsList.length > 0) {
        pendingHtml = pendingTopicsList.slice(0, 15).map(t => `
          <div class="p-2 rounded-2 mb-1.5 bg-white border d-flex justify-content-between align-items-center">
            <div class="d-flex align-items-center gap-2">
              <span class="text-muted">⏳</span>
              <span class="small text-secondary">${escapeHtml(t.title || 'Topic')}</span>
            </div>
            <span class="badge bg-light text-muted border" style="font-size: 0.68rem;">Pending • ${escapeHtml(t.phase_name || 'Upcoming')}</span>
          </div>
        `).join("");
        if (pendingTopicsList.length > 15) {
          pendingHtml += `<div class="text-center text-muted small py-2">+ ${pendingTopicsList.length - 15} additional upcoming topics in curriculum</div>`;
        }
      } else {
        pendingHtml = `<div class="p-4 text-center text-muted border rounded-3 bg-light">All curriculum topics unlocked or completed!</div>`;
      }

      // 3. Build Daily Plan Tasks HTML
      const dailyTasks = s.daily_plan_tasks || [];
      let dailyTasksHtml = "";
      if (dailyTasks.length > 0) {
        dailyTasksHtml = dailyTasks.map(t => {
          const isDone = t.status === "Completed";
          const isInProg = t.status === "In Progress";
          const icon = t.type === "Watch" ? "🎥" : t.type === "Practice" ? "💻" : t.type === "Read" ? "📖" : "📝";
          const statusBadge = isDone 
            ? '<span class="badge bg-success-subtle text-success border border-success">✓ Completed Correctly</span>'
            : isInProg
            ? '<span class="badge bg-warning-subtle text-dark border border-warning">⚡ In Progress</span>'
            : '<span class="badge bg-light text-secondary border">⏳ Pending</span>';

          return `
            <div class="p-3 rounded-3 mb-2 ${isDone ? 'bg-success-subtle border border-success-subtle' : 'bg-white border'} d-flex justify-content-between align-items-center flex-wrap gap-2">
              <div class="d-flex align-items-center gap-2">
                <span class="fs-4">${icon}</span>
                <div>
                  <div class="fw-bold text-dark small">${escapeHtml(t.type)}: ${escapeHtml(t.title)}</div>
                  <div class="text-muted" style="font-size: 0.72rem;">Duration: ${escapeHtml(t.duration || '30 mins')}</div>
                </div>
              </div>
              <div class="d-flex align-items-center gap-2">
                ${statusBadge}
              </div>
            </div>
          `;
        }).join("");
      } else {
        dailyTasksHtml = `<div class="p-4 text-center text-muted border rounded-3 bg-light">No daily plan tasks recorded for today.</div>`;
      }

      // 4. Aptitude Tests History Rows
      let testRowsHtml = "";
      if (s.recent_attempts && s.recent_attempts.length > 0) {
        testRowsHtml = s.recent_attempts.map((att, idx) => {
          const passBadge = att.is_passed
            ? '<span class="badge bg-success-subtle text-success border border-success">PASSED</span>'
            : '<span class="badge bg-danger-subtle text-danger border border-danger">FAILED</span>';
          const scoreClass = att.score_percentage >= 70 ? 'text-success' : att.score_percentage >= 50 ? 'text-warning' : 'text-danger';
          const mins = Math.floor((att.time_taken_seconds || 0) / 60);
          const secs = (att.time_taken_seconds || 0) % 60;
          const timeFormatted = mins > 0 ? `${mins}m ${secs}s` : `${secs}s`;

          return `
            <tr>
              <td class="fw-semibold">#${idx + 1} ${escapeHtml(att.title)}</td>
              <td class="text-muted small">${escapeHtml(att.date || 'Recently')}</td>
              <td><span class="fw-bold fs-6 ${scoreClass}">${att.score_percentage}%</span></td>
              <td>${passBadge}</td>
              <td class="small">
                <span class="text-success fw-bold">✓ ${att.correct_count}</span> / 
                <span class="text-danger fw-bold">✗ ${att.wrong_count}</span> 
                <span class="text-muted">(${att.total_questions} Qs)</span>
              </td>
              <td class="text-muted small">⏱️ ${timeFormatted}</td>
            </tr>
          `;
        }).join("");
      } else {
        testRowsHtml = `
          <tr>
            <td colspan="6" class="text-center py-4 text-muted">
              Student has not attended any aptitude assessments yet.
            </td>
          </tr>
        `;
      }

      // 5. Coding Attempts Rows
      const codingAttempts = s.recent_coding_attempts || [];
      let codingRowsHtml = "";
      if (codingAttempts.length > 0) {
        codingRowsHtml = codingAttempts.map((ca, idx) => {
          const passBadge = ca.passed
            ? '<span class="badge bg-success-subtle text-success border border-success">PASSED</span>'
            : '<span class="badge bg-danger-subtle text-danger border border-danger">FAILED</span>';
          const mins = Math.floor((ca.time_taken_seconds || 0) / 60);
          const secs = (ca.time_taken_seconds || 0) % 60;
          const timeFormatted = mins > 0 ? `${mins}m ${secs}s` : `${secs}s`;

          return `
            <tr>
              <td class="fw-semibold">#${idx + 1} ${escapeHtml(ca.title)}</td>
              <td class="text-muted small">${escapeHtml(ca.date)}</td>
              <td><span class="fw-bold fs-6 ${ca.percentage >= 70 ? 'text-success' : 'text-warning'}">${ca.percentage}%</span></td>
              <td>${passBadge}</td>
              <td class="small text-muted">${escapeHtml(ca.status)}</td>
              <td class="text-muted small">⏱️ ${timeFormatted}</td>
            </tr>
          `;
        }).join("");
      } else {
        codingRowsHtml = `
          <tr>
            <td colspan="6" class="text-center py-4 text-muted">
              No practical coding assessment records logged yet.
            </td>
          </tr>
        `;
      }

      // 6. Phases Breakdown HTML
      const phasesList = s.phases_breakdown || [];
      let phasesHtml = "";
      if (phasesList.length > 0) {
        phasesHtml = phasesList.map(ph => `
          <div class="col-md-6 mb-3">
            <div class="p-3 rounded-3 border bg-white shadow-sm h-100">
              <div class="d-flex justify-content-between align-items-center mb-1">
                <span class="fw-bold text-dark small">Phase ${ph.phase_num}: ${escapeHtml(ph.name)}</span>
                <span class="badge ${ph.progress_percent >= 100 ? 'bg-success' : ph.progress_percent > 0 ? 'bg-primary' : 'bg-light text-muted border'} rounded-pill" style="font-size: 0.68rem;">
                  ${ph.progress_percent >= 100 ? 'Completed' : ph.progress_percent > 0 ? 'In Progress' : (ph.is_locked ? 'Locked' : 'Available')}
                </span>
              </div>
              <div class="text-muted mb-2" style="font-size: 0.72rem;">${escapeHtml(ph.subtitle || '')}</div>
              <div class="d-flex justify-content-between small text-muted mb-1" style="font-size: 0.7rem;">
                <span>${ph.completed_count || 0}/${ph.topics_count || 0} topics completed</span>
                <span class="fw-bold">${ph.progress_percent || 0}%</span>
              </div>
              <div class="progress" style="height: 6px; border-radius: 999px;">
                <div class="progress-bar ${ph.progress_percent >= 100 ? 'bg-success' : 'bg-primary'}" style="width: ${ph.progress_percent || 0}%;"></div>
              </div>
            </div>
          </div>
        `).join("");
      }

      // Build complete modal body
      modalBody.innerHTML = `
        <!-- Evaluation Callout Banner -->
        <div class="card border-0 bg-light p-3 rounded-4 mb-4 shadow-sm">
          <div class="d-flex flex-wrap justify-content-between align-items-center gap-3">
            <div>
              <div class="small text-muted text-uppercase fw-semibold mb-1">Placement Preparation Telemetry</div>
              <div class="d-flex align-items-center gap-2 flex-wrap">
                ${statusBadge}
                ${trendBadge}
                <span class="badge bg-info-subtle text-info border border-info px-3 py-1.5 rounded-pill fw-bold">
                  🎯 Placement Readiness: ${readinessScore}/100
                </span>
                <span class="badge ${s.consistency_badge || 'bg-light text-secondary'} px-3 py-1.5 rounded-pill">
                  🔥 ${s.daily_streak} Day Streak (${escapeHtml(s.consistency_label)})
                </span>
              </div>
            </div>
            <div class="text-end">
              <div class="small text-muted">Last Active Date</div>
              <div class="fw-bold text-dark">${escapeHtml(s.last_active_date || 'Active Today')}</div>
            </div>
          </div>
          ${s.improvement_notes ? `
            <div class="alert alert-info py-2 px-3 mt-3 mb-0 small d-flex align-items-center gap-2 rounded-3 border-0 bg-white shadow-xs">
              <span>📈</span>
              <span><strong>Performance Trajectory:</strong> ${escapeHtml(s.improvement_notes)}</span>
            </div>
          ` : ''}
        </div>

        <!-- 4 Top Telemetry Metric Cards -->
        <div class="row g-3 mb-4">
          <div class="col-sm-6 col-lg-3">
            <div class="p-3 border rounded-3 bg-white shadow-sm h-100">
              <div class="small text-muted fw-semibold mb-1">📘 Active Learning Course</div>
              <div class="fs-6 fw-bold text-dark text-truncate" title="${escapeHtml(s.active_course_name || 'Java Track')}">
                ${s.active_course_icon || '📘'} ${escapeHtml(s.active_course_name || 'Java Enterprise')}
              </div>
              <small class="text-primary fw-semibold">${escapeHtml(s.active_phase_name || 'Phase 1: Foundations')}</small>
              <div class="text-muted" style="font-size: 0.72rem;">${escapeHtml(s.sprint_status || 'Day 1 of 90')}</div>
            </div>
          </div>
          <div class="col-sm-6 col-lg-3">
            <div class="p-3 border rounded-3 bg-white shadow-sm h-100">
              <div class="small text-muted fw-semibold mb-1">🎯 Topic Mastery &amp; Progress</div>
              <div class="fs-4 fw-bold text-success">${s.course_progress_percentage || s.roadmap_progress || 0}%</div>
              <small class="text-muted"><strong>${s.completed_topics_count || 0}</strong> Done • <strong>${s.ongoing_topics_count || 0}</strong> Active • <strong>${s.pending_topics_count || 0}</strong> Pending</small>
            </div>
          </div>
          <div class="col-sm-6 col-lg-3">
            <div class="p-3 border rounded-3 bg-white shadow-sm h-100">
              <div class="small text-muted fw-semibold mb-1">🧠 Aptitude Assessment Average</div>
              <div class="fs-4 fw-bold text-primary">${s.avg_score}%</div>
              <small class="text-muted">${s.passed_count} Passed / ${s.failed_count} Failed (${s.tests_count} Tests)</small>
            </div>
          </div>
          <div class="col-sm-6 col-lg-3">
            <div class="p-3 border rounded-3 bg-white shadow-sm h-100">
              <div class="small text-muted fw-semibold mb-1">💻 Coding Practice &amp; Sandboxes</div>
              <div class="fs-4 fw-bold text-info">${s.avg_coding_score}%</div>
              <small class="text-muted">${s.coding_assessments_count || 0} Coding Labs • ⏱️ ${s.total_time_spent_mins || 0}m study</small>
            </div>
          </div>
        </div>

        <!-- Tabbed Detailed Telemetry Console -->
        <ul class="nav nav-pills mb-3 border-bottom pb-2 gap-2" id="studentDetailTabs" role="tablist">
          <li class="nav-item" role="presentation">
            <button class="nav-link active rounded-pill fw-semibold small py-1.5 px-3" id="tab-topics-btn" data-bs-toggle="pill" data-bs-target="#tab-topics-pane" type="button" role="tab">
              📚 Course &amp; Topics Tracker (${s.completed_topics_count || 0}/${s.total_course_topics || 50})
            </button>
          </li>
          <li class="nav-item" role="presentation">
            <button class="nav-link rounded-pill fw-semibold small py-1.5 px-3" id="tab-daily-btn" data-bs-toggle="pill" data-bs-target="#tab-daily-pane" type="button" role="tab">
              📅 Today's Study Tasks (${dailyTasks.length})
            </button>
          </li>
          <li class="nav-item" role="presentation">
            <button class="nav-link rounded-pill fw-semibold small py-1.5 px-3" id="tab-aptitude-btn" data-bs-toggle="pill" data-bs-target="#tab-aptitude-pane" type="button" role="tab">
              🧠 Aptitude Test History (${s.recent_attempts ? s.recent_attempts.length : 0})
            </button>
          </li>
          <li class="nav-item" role="presentation">
            <button class="nav-link rounded-pill fw-semibold small py-1.5 px-3" id="tab-coding-btn" data-bs-toggle="pill" data-bs-target="#tab-coding-pane" type="button" role="tab">
              💻 Coding Sandbox Attempts (${codingAttempts.length})
            </button>
          </li>
          <li class="nav-item" role="presentation">
            <button class="nav-link rounded-pill fw-semibold small py-1.5 px-3" id="tab-phases-btn" data-bs-toggle="pill" data-bs-target="#tab-phases-pane" type="button" role="tab">
              🗺️ 4-Phase Curriculum Breakdown
            </button>
          </li>
        </ul>

        <div class="tab-content" id="studentDetailTabsContent">
          <!-- Pane 1: Course & Topics Tracker -->
          <div class="tab-pane fade show active" id="tab-topics-pane" role="tabpanel">
            <div class="card border rounded-3 mb-3 shadow-sm">
              <div class="card-header bg-white py-2.5 border-bottom d-flex justify-content-between align-items-center">
                <span class="fw-bold small text-dark">Course Curriculum Progression</span>
                <span class="badge bg-light text-secondary border small">${s.course_progress_percentage || 0}% Completed</span>
              </div>
              <div class="card-body p-3">
                <div class="row g-3">
                  <div class="col-md-4">
                    <div class="p-2.5 rounded-3 bg-success-subtle border border-success-subtle mb-2">
                      <div class="fw-bold text-success small d-flex justify-content-between align-items-center">
                        <span>✅ Completed Topics (${completedTopicsList.length})</span>
                        <span class="badge bg-success text-white">Correct</span>
                      </div>
                      <small class="text-muted" style="font-size: 0.7rem;">Verified learned topics</small>
                    </div>
                    <div style="max-height: 380px; overflow-y: auto; padding-right: 4px;">
                      ${completedHtml}
                    </div>
                  </div>
                  <div class="col-md-4">
                    <div class="p-2.5 rounded-3 bg-warning-subtle border border-warning-subtle mb-2">
                      <div class="fw-bold text-dark small d-flex justify-content-between align-items-center">
                        <span>⚡ Ongoing Topics (${ongoingTopicsList.length})</span>
                        <span class="badge bg-warning text-dark">Active</span>
                      </div>
                      <small class="text-muted" style="font-size: 0.7rem;">Currently being studied</small>
                    </div>
                    <div style="max-height: 380px; overflow-y: auto; padding-right: 4px;">
                      ${ongoingHtml}
                    </div>
                  </div>
                  <div class="col-md-4">
                    <div class="p-2.5 rounded-3 bg-light border mb-2">
                      <div class="fw-bold text-secondary small d-flex justify-content-between align-items-center">
                        <span>⏳ Pending Topics (${pendingTopicsList.length})</span>
                        <span class="badge bg-secondary text-white">Upcoming</span>
                      </div>
                      <small class="text-muted" style="font-size: 0.7rem;">Next in placement sprint</small>
                    </div>
                    <div style="max-height: 380px; overflow-y: auto; padding-right: 4px;">
                      ${pendingHtml}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Pane 2: Today's Daily Plan Tasks -->
          <div class="tab-pane fade" id="tab-daily-pane" role="tabpanel">
            <div class="card border rounded-3 mb-3 shadow-sm">
              <div class="card-header bg-white py-2.5 border-bottom d-flex justify-content-between align-items-center">
                <span class="fw-bold small text-dark">Today's Daily Plan &amp; Study Tasks</span>
                <span class="badge bg-light text-secondary border small">${dailyTasks.filter(t => t.status === 'Completed').length}/${dailyTasks.length} Done Today</span>
              </div>
              <div class="card-body p-3">
                ${dailyTasksHtml}
              </div>
            </div>
          </div>

          <!-- Pane 3: Aptitude Assessment History -->
          <div class="tab-pane fade" id="tab-aptitude-pane" role="tabpanel">
            <div class="card border rounded-3 mb-3 shadow-sm">
              <div class="card-header bg-white py-2.5 border-bottom d-flex justify-content-between align-items-center">
                <span class="fw-bold small text-dark">Aptitude Test Log &amp; Question Accuracy</span>
                <span class="badge bg-light text-dark border">${s.recent_attempts ? s.recent_attempts.length : 0} Tests Evaluated</span>
              </div>
              <div class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                  <thead class="table-light small text-muted text-uppercase">
                    <tr>
                      <th>Test Title</th>
                      <th>Date</th>
                      <th>Score</th>
                      <th>Status</th>
                      <th>Correct / Wrong</th>
                      <th>Time Taken</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${testRowsHtml}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- Pane 4: Coding Sandbox Attempts -->
          <div class="tab-pane fade" id="tab-coding-pane" role="tabpanel">
            <div class="card border rounded-3 mb-3 shadow-sm">
              <div class="card-header bg-white py-2.5 border-bottom d-flex justify-content-between align-items-center">
                <span class="fw-bold small text-dark">Practical Coding Sandbox Challenges</span>
                <span class="badge bg-light text-dark border">${codingAttempts.length} Coding Labs</span>
              </div>
              <div class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                  <thead class="table-light small text-muted text-uppercase">
                    <tr>
                      <th>Challenge Name</th>
                      <th>Date</th>
                      <th>Score</th>
                      <th>Status</th>
                      <th>Submission State</th>
                      <th>Time Taken</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${codingRowsHtml}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- Pane 5: 4-Phase Curriculum Breakdown -->
          <div class="tab-pane fade" id="tab-phases-pane" role="tabpanel">
            <div class="card border rounded-3 mb-3 shadow-sm">
              <div class="card-header bg-white py-2.5 border-bottom">
                <span class="fw-bold small text-dark">4-Phase Placement Curriculum Roadmap</span>
              </div>
              <div class="card-body p-3">
                <div class="row">
                  ${phasesHtml || '<div class="col-12 text-muted text-center py-4">No curriculum phase details available.</div>'}
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
    } catch (err) {
      modalBody.innerHTML = `
        <div class="alert alert-danger">
          Failed to load candidate activity details: ${escapeHtml(err.message || String(err))}
        </div>
      `;
    }
  }

  window.openStudentActivityDetailModal = openStudentActivityDetailModal;

    // Filter Listeners for Student Monitor
  let smSearchTimeout = null;
  const smSearchInput = document.getElementById("sm-filter-search");
  if (smSearchInput) {
    smSearchInput.addEventListener("input", () => {
      clearTimeout(smSearchTimeout);
      smSearchTimeout = setTimeout(loadStudentLearningMonitor, 300);
    });
  }
  const smPerfSelect = document.getElementById("sm-filter-performance");
  if (smPerfSelect) smPerfSelect.addEventListener("change", loadStudentLearningMonitor);

  const smTrendSelect = document.getElementById("sm-filter-trend");
  if (smTrendSelect) smTrendSelect.addEventListener("change", loadStudentLearningMonitor);

  const smResetBtn = document.getElementById("sm-filter-reset-btn");
  if (smResetBtn) {
    smResetBtn.addEventListener("click", () => {
      if (smSearchInput) smSearchInput.value = "";
      if (smPerfSelect) smPerfSelect.value = "all";
      if (smTrendSelect) smTrendSelect.value = "all";
      loadStudentLearningMonitor();
    });
  }

  const smRefreshBtn = document.getElementById("refresh-student-monitor-btn");
  if (smRefreshBtn) smRefreshBtn.addEventListener("click", loadStudentLearningMonitor);

  async function initRecruiterDashboard() {
    // 1. Immediately render candidate resumes table with highest priority
    renderBulkUploadedCandidatesTable().catch(err => {
      console.warn("Bulk candidates table rendering error:", err);
    });

    // 2. Populate job dropdown
    populateJobFilterDropdown().catch(err => {
      console.warn("Job dropdown error:", err);
    });

    // 3. Load analytics
    loadAnalytics().catch(err => {
      console.warn("Analytics error:", err);
    });

    // 4. Load student career guidance & learning activity monitor
    loadStudentLearningMonitor().catch(err => {
      console.warn("Student learning monitor error:", err);
    });
  }

  // If auth is already initialized by auth-guard.js, run immediately
  if (window.__AR_AUTH_READY) {
    initRecruiterDashboard();
  } else {
    document.addEventListener("ar:auth-ready", initRecruiterDashboard);
  }

  // Backup trigger: if page is ready, attempt rendering candidate resumes immediately
  if (document.readyState === "complete" || document.readyState === "interactive") {
    setTimeout(() => {
      renderBulkUploadedCandidatesTable();
      loadStudentLearningMonitor();
    }, 50);
  } else {
    document.addEventListener("DOMContentLoaded", () => {
      setTimeout(() => {
        renderBulkUploadedCandidatesTable();
        loadStudentLearningMonitor();
      }, 50);
    });
  }
})();
