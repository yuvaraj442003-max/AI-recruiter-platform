/**
 * my-applications.js — lists the candidate's own job applications.
 */
(function () {
  const wrapper = document.getElementById("applications-wrapper");

  function statusBadge(status) {
    const map = {
      applied: "secondary",
      under_review: "info",
      shortlisted: "primary",
      interview: "warning",
      selected: "success",
      rejected: "danger",
    };
    return `<span class="badge text-bg-${map[status] || "secondary"}">${status.replace("_", " ")}</span>`;
  }

  async function load() {
    try {
      const [applicationsRes, interviewsRes] = await Promise.all([applicationsAPI.mine(), interviewsAPI.list()]);
      const applications = applicationsRes.data;

      const interviewsByJobId = {};
      interviewsRes.data.forEach((iv) => {
        interviewsByJobId[iv.job_id] = iv;
      });

      if (!applications.length) {
        wrapper.innerHTML =
          '<div class="card p-4 text-center text-muted-custom">No applications yet. <a href="jobs.html">Browse jobs</a> to get started.</div>';
        return;
      }

      const rows = applications
        .map((app) => {
          const interview = interviewsByJobId[app.job_id];
          let interviewCell = '<span class="text-muted-custom small">Not started</span>';
          if (interview && interview.status === "completed") {
            interviewCell = `<a href="interview-report.html?interview_id=${interview.id}" class="btn btn-sm btn-success">View Report</a>`;
          } else if (interview) {
            interviewCell = `<a href="interview.html?interview_id=${interview.id}" class="btn btn-sm btn-primary">Continue Interview</a>`;
          }

          const chatBtn = `<button class="btn btn-sm btn-outline-primary ms-1 msg-rec-btn" data-job-id="${app.job_id}">💬 Message Recruiter</button>`;

          return `
        <tr>
          <td class="fw-medium">${app.job_title || "—"}</td>
          <td>
            <span class="badge ${app.ats_score >= 80 ? 'bg-success' : app.ats_score >= 60 ? 'bg-info' : 'bg-secondary'} px-3 py-1 rounded-pill">
              ${app.ats_score != null ? Math.round(app.ats_score) : (app.match_score != null ? Math.round(app.match_score) : "—")}% ATS
            </span>
          </td>
          <td>${statusBadge(app.status)}</td>
          <td>${new Date(app.applied_at).toLocaleDateString()}</td>
          <td>${interviewCell} ${chatBtn}</td>
        </tr>
      `;
        })
        .join("");

      wrapper.innerHTML = `
        <div class="card border-0 shadow-sm overflow-hidden" style="border-radius: 12px;">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="bg-light fs-7 text-secondary text-uppercase">
                <tr>
                  <th class="ps-4 py-3">Job Title</th>
                  <th class="py-3">Your ATS Score</th>
                  <th class="py-3">Status</th>
                  <th class="py-3">Applied</th>
                  <th class="text-end pe-4 py-3">Actions</th>
                </tr>
              </thead>
              <tbody>${rows}</tbody>
            </table>
          </div>
        </div>
      `;

      wrapper.querySelectorAll(".msg-rec-btn").forEach(btn => {
        btn.addEventListener("click", (e) => {
          if (e) e.preventDefault();
          if (window.openChatWithUser) {
            window.openChatWithUser();
          }
        });
      });
    } catch (err) {
      wrapper.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
    }
  }

  document.addEventListener("ar:auth-ready", load);
})();
