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

            if (score >= minAts) eligibleApps++;
            if (st === "shortlisted") shortlistedApps++;
            if ((st === "applied" || st === "under_review") && score < minAts) reviewApps++;
            if (score < 40) notRecApps++;

            allCandidateApps.push({
              application: app,
              job: job,
              candidateName: app.candidate_name || "Candidate",
              candidateEmail: app.candidate_email || "",
              atsScore: Math.round(score),
              jobMatchScore: Math.round(app.job_match_score || score),
              recommendation: app.recommendation || (score >= 80 ? "Priority Candidate" : score >= 60 ? "Shortlist for Review" : score >= 40 ? "Manual Review" : "Not Recommended"),
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
          topBody.innerHTML = `<tr><td colspan="7" class="text-center py-4 text-muted">No applicants submitted yet.</td></tr>`;
          return;
        }

        topBody.innerHTML = allCandidateApps.slice(0, 10).map((item, idx) => {
          let scoreBadge = "bg-success";
          if (item.atsScore < 40) scoreBadge = "bg-danger";
          else if (item.atsScore < 60) scoreBadge = "bg-warning text-dark";
          else if (item.atsScore < 80) scoreBadge = "bg-info text-white";

          return `
            <tr>
              <td class="fw-bold text-secondary">#${idx + 1}</td>
              <td>
                <div class="fw-bold text-dark fs-6">${item.candidateName}</div>
                <div class="text-muted small">${item.candidateEmail}</div>
              </td>
              <td class="text-secondary small fw-medium">${item.job.title}</td>
              <td>
                <span class="badge ${scoreBadge} px-3 py-1 rounded-pill fs-6">${item.atsScore}%</span>
              </td>
              <td>
                <span class="badge bg-light text-dark border px-3 py-1 rounded-pill fs-6">${item.jobMatchScore}%</span>
              </td>
              <td>
                <span class="badge bg-secondary-subtle text-secondary px-2 py-1 rounded-pill small">${item.recommendation}</span>
              </td>
              <td class="text-end">
                <a href="job-applicants.html?job_id=${item.job.id}" class="btn btn-sm btn-outline-primary fw-semibold px-3">
                  Inspect Applicants &rarr;
                </a>
              </td>
            </tr>
          `;
        }).join("");
      }
    } catch (err) {
      console.warn("Could not load ATS screening summary:", err);
    }
  }

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

      renderHiringFunnelChart(data);
      renderMatchDistributionChart(data);
      renderMissingSkillsChart(data);
      renderTopSkillsChart(data);
      renderApplicationsByJobChart(data);
      renderInterviewScoresChart(data);
      renderJobPerformanceTable(data);

      await renderScreeningStatsAndTopCandidates();
    } catch (err) {
      showAlert(err.message, "danger");
    }
  }

  // Setup Event Listeners for Filters
  if (jobFilterSelect) jobFilterSelect.addEventListener("change", loadAnalytics);
  if (dateFilterSelect) dateFilterSelect.addEventListener("change", loadAnalytics);
  if (statusFilterSelect) statusFilterSelect.addEventListener("change", loadAnalytics);

  document.addEventListener("ar:auth-ready", async () => {
    await populateJobFilterDropdown();
    await loadAnalytics();
  });
})();
