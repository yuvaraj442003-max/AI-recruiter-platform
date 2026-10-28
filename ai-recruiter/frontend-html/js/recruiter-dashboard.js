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
          <td colspan="8" class="text-center py-5 text-muted">
            <div class="mb-2 fs-2">🎓</div>
            <div class="fw-semibold">No student learning activities found</div>
            <small class="text-muted">Try adjusting your search criteria or filter options.</small>
          </td>
        </tr>
      `;
      return;
    }

    const rows = students.map((s) => {
      // 1. Preparing Topics Badges
      let topicsHtml = "";
      if (s.preparing_topics && s.preparing_topics.length > 0) {
        const visibleTopics = s.preparing_topics.slice(0, 3);
        topicsHtml = visibleTopics.map(t => `<span class="badge bg-light text-dark border me-1 mb-1 small">${escapeHtml(t)}</span>`).join("");
        if (s.preparing_topics.length > 3) {
          topicsHtml += `<span class="badge bg-secondary-subtle text-secondary small" title="${s.preparing_topics.slice(3).map(escapeHtml).join(', ')}">+${s.preparing_topics.length - 3} more</span>`;
        }
      } else {
        topicsHtml = `<span class="text-muted small">No topics chosen</span>`;
      }

      // 2. Aptitude Tests Info
      let aptitudeHtml = "";
      if (s.tests_count > 0) {
        const scoreBadgeClass = s.avg_score >= 70 ? "bg-success" : s.avg_score >= 50 ? "bg-warning text-dark" : "bg-danger";
        aptitudeHtml = `
          <div>
            <span class="badge ${scoreBadgeClass} fw-bold">${s.avg_score}% Avg</span>
            <span class="small text-muted ms-1">(${s.tests_count} test${s.tests_count > 1 ? 's' : ''})</span>
          </div>
          <div class="small text-muted mt-1">
            Pass: <strong>${s.passed_count}</strong> / Fail: <strong>${s.failed_count}</strong> (${s.pass_rate}%)
          </div>
        `;
      } else {
        aptitudeHtml = `<span class="badge bg-light text-muted border">No tests attended</span>`;
      }

      // 3. Learning / Roadmap Progress
      const rmBarColor = s.roadmap_progress >= 70 ? "bg-success" : s.roadmap_progress >= 40 ? "bg-info" : "bg-warning";
      const learningHtml = `
        <div class="d-flex align-items-center justify-content-between small mb-1">
          <span class="fw-bold">${s.roadmap_progress}%</span>
          <span class="text-muted">${s.milestones_completed_count} milestones</span>
        </div>
        <div class="progress" style="height: 6px;">
          <div class="progress-bar ${rmBarColor}" style="width: ${s.roadmap_progress}%;"></div>
        </div>
        <div class="small text-muted mt-1">⏱️ ${s.total_time_spent_mins}m spent</div>
      `;

      // 4. Consistency
      const streakHtml = s.daily_streak > 0 
        ? `<div class="fw-bold text-danger small">🔥 ${s.daily_streak} Day Streak</div>`
        : `<div class="text-muted small">No active streak</div>`;
      const consistencyHtml = `
        ${streakHtml}
        <span class="badge ${s.consistency_badge || 'bg-light text-secondary'} small mt-1">${escapeHtml(s.consistency_label || 'Inactive')}</span>
      `;

      // 5. Trend
      let trendHtml = "";
      if (s.trend === "improving") {
        trendHtml = `<span class="badge bg-success-subtle text-success border border-success fw-bold px-2 py-1" title="Scores are improving across recent tests">↗ Improving</span>`;
      } else if (s.trend === "declining") {
        trendHtml = `<span class="badge bg-danger-subtle text-danger border border-danger fw-bold px-2 py-1" title="Scores are declining, requires attention">↘ Declining</span>`;
      } else if (s.trend === "steady") {
        trendHtml = `<span class="badge bg-primary-subtle text-primary border border-primary fw-bold px-2 py-1">➔ Steady</span>`;
      } else if (s.trend === "baseline") {
        trendHtml = `<span class="badge bg-light text-secondary border px-2 py-1">🎯 1 Test (Base)</span>`;
      } else {
        trendHtml = `<span class="badge bg-light text-muted border px-2 py-1">No Tests</span>`;
      }

      // 6. Status & Star Rating
      let statusHtml = "";
      if (s.performance_status === "Performing Well") {
        statusHtml = `<span class="badge bg-success text-white px-2.5 py-1.5 rounded-pill fw-bold">Performing Well ✅</span>`;
      } else if (s.performance_status === "Moderate Progress") {
        statusHtml = `<span class="badge bg-warning text-dark px-2.5 py-1.5 rounded-pill fw-bold">Moderate Progress ⚠️</span>`;
      } else {
        statusHtml = `<span class="badge bg-danger text-white px-2.5 py-1.5 rounded-pill fw-bold">Needs Improvement ❌</span>`;
      }
      const stars = "★".repeat(s.rating_stars || 1) + "☆".repeat(5 - (s.rating_stars || 1));

      // 7. Student Academic Details
      const collegeDisplay = s.college_name ? escapeHtml(s.college_name) : "College not set";
      const branchDisplay = [s.degree, s.branch].filter(Boolean).map(escapeHtml).join(" - ");

      return `
        <tr>
          <td>
            <div class="d-flex align-items-center gap-2">
              <div class="rounded-circle bg-success text-white d-flex align-items-center justify-content-center fw-bold shadow-sm" style="width: 38px; height: 38px; min-width: 38px; font-size: 14px;">
                ${escapeHtml((s.name || "S").charAt(0).toUpperCase())}
              </div>
              <div class="overflow-hidden">
                <div class="fw-bold text-dark text-truncate">${escapeHtml(s.name)}</div>
                <div class="text-muted small text-truncate">${escapeHtml(s.email)}</div>
                <div class="text-secondary small mt-0.5 text-truncate" title="${collegeDisplay}">
                  🏛️ ${collegeDisplay} ${branchDisplay ? `(${branchDisplay})` : ''}
                </div>
              </div>
            </div>
          </td>
          <td>${topicsHtml}</td>
          <td>${aptitudeHtml}</td>
          <td>${learningHtml}</td>
          <td>${consistencyHtml}</td>
          <td>${trendHtml}</td>
          <td>
            ${statusHtml}
            <div class="small text-warning mt-1" style="font-size: 11px;">${stars}</div>
          </td>
          <td class="text-end">
            <button class="btn btn-sm btn-outline-success fw-semibold text-nowrap" onclick="window.openStudentActivityDetailModal('${s.user_id}')">
              🔍 View Details
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
        <p class="mt-2 text-muted">Loading detailed student activities...</p>
      </div>
    `;

    if (window.bootstrap) {
      const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
      modal.show();
    }

    try {
      const res = await (window.studentAPI || api.student).getStudentActivityDetail(userId);
      const student = res.data || res;

      if (modalName) modalName.textContent = `${student.name} — Career Guidance & Aptitude Telemetry`;
      if (modalSubtitle) modalSubtitle.textContent = `${student.college_name || 'Academic Institution'} • ${student.degree || 'Student'} ${student.branch ? '(' + student.branch + ')' : ''} • Target Role: ${student.target_role || 'General'}`;

      // Build Modal Body HTML
      const statusBadge = student.performance_status === "Performing Well"
        ? '<span class="badge bg-success text-white px-3 py-1.5 rounded-pill fs-6">Performing Well ✅</span>'
        : student.performance_status === "Moderate Progress"
        ? '<span class="badge bg-warning text-dark px-3 py-1.5 rounded-pill fs-6">Moderate Progress ⚠️</span>'
        : '<span class="badge bg-danger text-white px-3 py-1.5 rounded-pill fs-6">Needs Improvement ❌</span>';

      const trendBadge = student.trend === "improving"
        ? '<span class="badge bg-success-subtle text-success border border-success fw-bold px-3 py-1.5 rounded-pill">↗ Performance Improving</span>'
        : student.trend === "declining"
        ? '<span class="badge bg-danger-subtle text-danger border border-danger fw-bold px-3 py-1.5 rounded-pill">↘ Performance Declining</span>'
        : '<span class="badge bg-primary-subtle text-primary border border-primary fw-bold px-3 py-1.5 rounded-pill">➔ Steady Performance</span>';

      // Topics Badges
      const prepTopics = (student.preparing_topics && student.preparing_topics.length > 0)
        ? student.preparing_topics.map(t => `<span class="badge bg-light text-dark border px-2.5 py-1.5 me-1 mb-1">${escapeHtml(t)}</span>`).join("")
        : '<span class="text-muted">No specific topics selected</span>';

      const strongBadges = (student.strong_areas && student.strong_areas.length > 0)
        ? student.strong_areas.map(t => `<span class="badge bg-success-subtle text-success border border-success px-2.5 py-1.5 me-1 mb-1">💪 ${escapeHtml(t)}</span>`).join("")
        : '<span class="text-muted small">None identified yet</span>';

      const weakBadges = (student.weak_areas && student.weak_areas.length > 0)
        ? student.weak_areas.map(t => `<span class="badge bg-danger-subtle text-danger border border-danger px-2.5 py-1.5 me-1 mb-1">⚠️ ${escapeHtml(t)}</span>`).join("")
        : '<span class="text-muted small">None identified yet</span>';

      // Tests Table Rows
      let testRowsHtml = "";
      if (student.recent_attempts && student.recent_attempts.length > 0) {
        testRowsHtml = student.recent_attempts.map((att, idx) => {
          const passBadge = att.is_passed
            ? '<span class="badge bg-success-subtle text-success border border-success">PASSED</span>'
            : '<span class="badge bg-danger-subtle text-danger border border-danger">FAILED</span>';
          const scoreClass = att.score_percentage >= 70 ? 'text-success' : att.score_percentage >= 50 ? 'text-warning' : 'text-danger';
          const mins = Math.floor(att.time_taken_seconds / 60);
          const secs = att.time_taken_seconds % 60;
          const timeFormatted = mins > 0 ? `${mins}m ${secs}s` : `${secs}s`;

          return `
            <tr>
              <td class="fw-semibold">#${idx + 1} ${escapeHtml(att.title)}</td>
              <td class="text-muted small">${escapeHtml(att.created_at || '—')}</td>
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
              Student has not attended any aptitude tests yet in the Career Guidance section.
            </td>
          </tr>
        `;
      }

      modalBody.innerHTML = `
        <!-- Status & Evaluation Banner -->
        <div class="card border-0 bg-light p-3 rounded-4 mb-4 shadow-sm">
          <div class="d-flex flex-wrap justify-content-between align-items-center gap-3">
            <div>
              <div class="small text-muted text-uppercase fw-semibold mb-1">Overall Learning Evaluation</div>
              <div class="d-flex align-items-center gap-2">
                ${statusBadge}
                ${trendBadge}
                <span class="badge ${student.consistency_badge || 'bg-light text-secondary'} px-3 py-1.5 rounded-pill">
                  🔥 ${student.daily_streak} Day Streak (${escapeHtml(student.consistency_label)})
                </span>
              </div>
            </div>
            <div class="text-end">
              <div class="small text-muted">Last Active Date</div>
              <div class="fw-bold text-dark">${escapeHtml(student.last_active_date || 'No recent activity')}</div>
            </div>
          </div>
        </div>

        <!-- 4 KPI Stat Boxes -->
        <div class="row g-3 mb-4">
          <div class="col-sm-6 col-lg-3">
            <div class="p-3 border rounded-3 bg-white shadow-sm h-100">
              <div class="small text-muted fw-semibold">Tests Attended</div>
              <div class="fs-4 fw-bold text-primary">${student.tests_count}</div>
              <small class="text-muted">${student.passed_count} Passed / ${student.failed_count} Failed</small>
            </div>
          </div>
          <div class="col-sm-6 col-lg-3">
            <div class="p-3 border rounded-3 bg-white shadow-sm h-100">
              <div class="small text-muted fw-semibold">Average Test Score</div>
              <div class="fs-4 fw-bold text-success">${student.avg_score}%</div>
              <small class="text-muted">Best Score: <strong>${student.best_score}%</strong></small>
            </div>
          </div>
          <div class="col-sm-6 col-lg-3">
            <div class="p-3 border rounded-3 bg-white shadow-sm h-100">
              <div class="small text-muted fw-semibold">Roadmap Progress</div>
              <div class="fs-4 fw-bold text-info">${student.roadmap_progress}%</div>
              <small class="text-muted">${student.milestones_completed_count} Milestones Completed</small>
            </div>
          </div>
          <div class="col-sm-6 col-lg-3">
            <div class="p-3 border rounded-3 bg-white shadow-sm h-100">
              <div class="small text-muted fw-semibold">Total Study Time</div>
              <div class="fs-4 fw-bold text-dark">${student.total_time_spent_mins} <span class="fs-6 fw-normal">mins</span></div>
              <small class="text-muted">Across all attempts</small>
            </div>
          </div>
        </div>

        <!-- Preparation Topics, Strengths & Weaknesses -->
        <div class="card border mb-4 rounded-3 shadow-sm">
          <div class="card-body p-3">
            <h6 class="fw-bold mb-2">📚 Preparation Topics &amp; Focus Domains</h6>
            <div class="mb-3">${prepTopics}</div>
            <div class="row g-3">
              <div class="col-md-6">
                <div class="small fw-bold text-success mb-1">💪 Strong Subject Areas (&gt;= 70%):</div>
                <div>${strongBadges}</div>
              </div>
              <div class="col-md-6">
                <div class="small fw-bold text-danger mb-1">⚠️ Areas Needing Support (&lt; 60%):</div>
                <div>${weakBadges}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Aptitude Test History Table -->
        <div class="card border rounded-3 shadow-sm">
          <div class="card-header bg-white py-3 border-bottom d-flex justify-content-between align-items-center">
            <h6 class="fw-bold mb-0">🧠 Aptitude Test Attendance &amp; Score History</h6>
            <span class="badge bg-light text-dark border">${student.recent_attempts ? student.recent_attempts.length : 0} Attempts Logged</span>
          </div>
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light small text-muted text-uppercase">
                <tr>
                  <th>Topic / Test Name</th>
                  <th>Date Attended</th>
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
