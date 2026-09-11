/**
 * my-jobs.js — lists the recruiter's job postings with a link to each
 * job's ranked applicant list, filtering, and metric stats.
 */
(function () {
  const wrapper = document.getElementById("jobs-table-wrapper");
  const searchInput = document.getElementById("job-search-input");
  const statusFilter = document.getElementById("job-status-filter");
  const statJobCount = document.getElementById("stat-job-count");
  const statPublishedCount = document.getElementById("stat-published-count");
  const statPausedCount = document.getElementById("stat-paused-count");

  let allJobs = [];

  function statusBadge(status) {
    if (status === "published") return `<span class="badge bg-success-subtle text-success border border-success border-opacity-25 px-2 py-1 rounded-pill">Published</span>`;
    if (status === "paused") return `<span class="badge bg-warning-subtle text-dark border border-warning border-opacity-25 px-2 py-1 rounded-pill">Paused</span>`;
    if (status === "draft") return `<span class="badge bg-secondary-subtle text-secondary border border-secondary border-opacity-25 px-2 py-1 rounded-pill">Draft</span>`;
    if (status === "closed") return `<span class="badge bg-danger-subtle text-danger border border-danger border-opacity-25 px-2 py-1 rounded-pill">Closed</span>`;
    return `<span class="badge bg-secondary px-2 py-1 rounded-pill">${status}</span>`;
  }

  function updateMetrics(jobs) {
    if (statJobCount) statJobCount.textContent = jobs.length;
    if (statPublishedCount) statPublishedCount.textContent = jobs.filter(j => j.status === "published").length;
    if (statPausedCount) statPausedCount.textContent = jobs.filter(j => j.status === "paused" || j.status === "draft").length;
  }

  function renderTable(jobs, currentUserId) {
    if (!jobs.length) {
      const isFiltered = (searchInput && searchInput.value) || (statusFilter && statusFilter.value !== "all");
      wrapper.innerHTML = `
        <div class="card border-0 shadow-sm p-5 text-center" style="border-radius: 12px; background: #ffffff;">
          <div class="fs-1 text-muted mb-3">📁</div>
          <h5 class="fw-bold text-dark mb-2">${isFiltered ? 'No matching jobs found' : 'No jobs posted yet'}</h5>
          <p class="text-secondary small mb-4">${isFiltered ? 'Try clearing your search query or filter criteria.' : 'Get started by creating your first job posting requisition.'}</p>
          <div>
            <a href="post-job.html" class="btn btn-success text-white fw-semibold px-4 py-2">➕ Post a New Job</a>
          </div>
        </div>
      `;
      return;
    }

    const rows = jobs
      .map((job) => {
        const jobId = job.id || job.job_id;
        const isPaused = job.status === "paused";
        const isPublished = job.status === "published";

        let statusToggleBtn = "";
        if (isPublished) {
          statusToggleBtn = `<button class="btn btn-sm btn-outline-warning pause-job-btn me-1 fw-medium" data-job-id="${jobId}">⏸️ Pause</button>`;
        } else if (isPaused) {
          statusToggleBtn = `<button class="btn btn-sm btn-outline-success resume-job-btn me-1 fw-medium" data-job-id="${jobId}">▶️ Resume</button>`;
        }

        const appCount = job.applications_count != null ? job.applications_count : (job.applicant_count || 0);

        return `
          <tr>
            <td class="ps-4">
              <div class="fw-bold text-dark fs-6">${job.title}</div>
              <div class="text-muted small">Job ID: #${jobId}</div>
            </td>
            <td>
              <span class="text-secondary fw-medium">${job.location ? '📍 ' + job.location : '—'}</span>
            </td>
            <td>${statusBadge(job.status)}</td>
            <td class="text-secondary small fw-medium">${new Date(job.created_at).toLocaleDateString()}</td>
            <td>
              <span class="badge bg-primary-subtle text-primary border border-primary border-opacity-25 px-3 py-1 rounded-pill fw-bold fs-6">
                👥 ${appCount} Applicant${appCount !== 1 ? 's' : ''}
              </span>
            </td>
            <td class="text-end pe-4">
              <a href="job-applicants.html?job_id=${jobId}" class="btn btn-sm btn-primary fw-semibold me-1 px-3 shadow-sm">
                👥 View Applicants
              </a>
              ${statusToggleBtn}
              <button class="btn btn-sm btn-outline-danger delete-job-btn fw-medium" data-job-id="${jobId}" data-job-title="${job.title}">🗑️ Delete</button>
            </td>
          </tr>
        `;
      })
      .join("");

    wrapper.innerHTML = `
      <div class="card border-0 shadow-sm overflow-hidden" style="border-radius: 12px; background: #ffffff;">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="bg-light text-uppercase fs-7 text-secondary">
              <tr>
                <th class="ps-4 py-3">Job Title</th>
                <th class="py-3">Location</th>
                <th class="py-3">Status</th>
                <th class="py-3">Date Posted</th>
                <th class="py-3">Applicants</th>
                <th class="text-end pe-4 py-3">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y">${rows}</tbody>
          </table>
        </div>
      </div>
    `;

    // Attach event handlers
    wrapper.querySelectorAll(".pause-job-btn").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const jobId = btn.dataset.jobId;
        if (!jobId || jobId === "undefined") {
          alert("Invalid job ID.");
          return;
        }
        btn.disabled = true;
        try {
          await jobsAPI.update(jobId, { status: "paused" });
          loadJobs(currentUserId);
        } catch (e) {
          alert(e.message);
          btn.disabled = false;
        }
      });
    });

    wrapper.querySelectorAll(".resume-job-btn").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const jobId = btn.dataset.jobId;
        if (!jobId || jobId === "undefined") {
          alert("Invalid job ID.");
          return;
        }
        btn.disabled = true;
        try {
          await jobsAPI.update(jobId, { status: "published" });
          loadJobs(currentUserId);
        } catch (e) {
          alert(e.message);
          btn.disabled = false;
        }
      });
    });

    wrapper.querySelectorAll(".delete-job-btn").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const jobId = btn.dataset.jobId;
        if (!jobId || jobId === "undefined") {
          alert("Invalid job ID.");
          return;
        }
        const title = btn.dataset.jobTitle || "this job";
        if (confirm(`Are you sure you want to permanently delete "${title}"? This action cannot be undone.`)) {
          btn.disabled = true;
          try {
            if (jobsAPI.remove) {
              await jobsAPI.remove(jobId);
            } else {
              await jobsAPI.update(jobId, { status: "closed" });
            }
            loadJobs(currentUserId);
          } catch (e) {
            alert(e.message);
            btn.disabled = false;
          }
        }
      });
    });
  }

  function applyFilters(currentUserId) {
    const query = (searchInput?.value || "").toLowerCase().trim();
    const statusVal = statusFilter?.value || "all";

    const filtered = allJobs.filter(job => {
      const matchQuery = !query ||
        (job.title && job.title.toLowerCase().includes(query)) ||
        (job.location && job.location.toLowerCase().includes(query));

      const matchStatus = statusVal === "all" || job.status === statusVal;
      return matchQuery && matchStatus;
    });

    renderTable(filtered, currentUserId);
  }

  async function loadJobs(currentUserId) {
    try {
      const res = await jobsAPI.list();
      allJobs = res.data.filter((j) => j.recruiter_id === currentUserId);

      updateMetrics(allJobs);
      applyFilters(currentUserId);

      if (searchInput) {
        searchInput.oninput = () => applyFilters(currentUserId);
      }
      if (statusFilter) {
        statusFilter.onchange = () => applyFilters(currentUserId);
      }
    } catch (err) {
      wrapper.innerHTML = `<div class="alert alert-danger shadow-sm border-0" style="border-radius: 12px;">${err.message}</div>`;
    }
  }

  document.addEventListener("ar:auth-ready", (event) => {
    loadJobs(event.detail.user.id);
  });
})();

