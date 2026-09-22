/**
 * my-applications.js — lists the candidate's own job applications.
 */
(function () {
  const wrapper = document.getElementById("applications-wrapper");

  function statusBadge(status, isShortlisted = false) {
    const s = (status || "applied").toLowerCase();
    if (s === "selected") {
      return `<span class="badge bg-success text-white px-3 py-1.5 rounded-pill fw-bold shadow-sm">🎉 Selected / Offer</span>`;
    }
    if (s === "shortlisted" || isShortlisted) {
      return `<span class="badge bg-primary text-white px-3 py-1.5 rounded-pill fw-bold shadow-sm">⭐ Shortlisted</span>`;
    }
    if (s === "interview") {
      return `<span class="badge bg-warning text-dark px-3 py-1.5 rounded-pill fw-semibold">🎙️ Interview Scheduled</span>`;
    }
    if (s === "under_review") {
      return `<span class="badge bg-info text-dark px-3 py-1.5 rounded-pill fw-semibold">⏳ Under Review</span>`;
    }
    if (s === "rejected") {
      return `<span class="badge bg-danger text-white px-3 py-1.5 rounded-pill fw-semibold">❌ Not Selected</span>`;
    }
    return `<span class="badge bg-secondary text-white px-3 py-1.5 rounded-pill fw-semibold">📝 Applied</span>`;
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
          const isRejected = (app.status || "").toLowerCase() === "rejected";
          const feedbackBtn = isRejected ? `<button class="btn btn-sm btn-outline-dark ms-1 cand-fb-btn" data-app-id="${app.id}" data-title="${app.job_title || 'Position'}">💬 View Feedback</button>` : "";
          const compName = app.company_name ? `<div class="small text-muted mt-0.5">🏢 ${app.company_name} ${app.job_location ? '• 📍 ' + app.job_location : ''}</div>` : '';
          const overrideNote = app.override_reason ? `<div class="small text-secondary fst-italic mt-0.5">📌 Note: ${app.override_reason}</div>` : '';

          return `
        <tr>
          <td class="fw-medium">
            <div class="fw-bold text-dark fs-6">${app.job_title || "—"}</div>
            ${compName}
            ${overrideNote}
          </td>
          <td>
            <span class="badge ${app.ats_score >= 80 ? 'bg-success' : app.ats_score >= 60 ? 'bg-info' : 'bg-secondary'} px-3 py-1 rounded-pill">
              ${app.ats_score != null ? Math.round(app.ats_score) : (app.match_score != null ? Math.round(app.match_score) : "—")}% ATS
            </span>
          </td>
          <td>${statusBadge(app.status, app.is_shortlisted)}</td>
          <td>${new Date(app.applied_at).toLocaleDateString()}</td>
          <td>${interviewCell} ${chatBtn} ${feedbackBtn}</td>
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

      wrapper.querySelectorAll(".cand-fb-btn").forEach(btn => {
        btn.addEventListener("click", () => openCandFeedbackModal(btn.dataset.appId, btn.dataset.title));
      });

    } catch (err) {
      wrapper.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
    }
  }

  let candFbModalInstance = null;
  async function openCandFeedbackModal(appId, jobTitle = "Position") {
    const modalEl = document.getElementById("candFeedbackViewerModal");
    const bodyEl = document.getElementById("cand-fb-modal-body");
    const titleEl = document.getElementById("cand-fb-modal-title");
    if (!modalEl || !bodyEl) return;

    if (!candFbModalInstance && window.bootstrap) {
      candFbModalInstance = new bootstrap.Modal(modalEl);
    }
    if (titleEl) titleEl.textContent = `Feedback — ${jobTitle}`;
    bodyEl.innerHTML = `<div class="text-center py-4 text-muted"><div class="spinner-border text-primary mb-3"></div><div>Loading your feedback…</div></div>`;
    candFbModalInstance.show();

    try {
      const res = await feedbackAPI.get(appId);
      const fb = res.data || res;

      const strengthsList = (fb.strengths || []).map(s => `<span class="badge bg-success-subtle text-success border border-success border-opacity-25 px-3 py-1 rounded-pill me-1 mb-1">✓ ${s}</span>`).join("");
      const gapsList = (fb.areas_for_improvement || []).map(g => `<span class="badge bg-danger-subtle text-danger border border-danger border-opacity-25 px-2 py-1 rounded-pill me-1 mb-1">• ${g}</span>`).join("");

      bodyEl.innerHTML = `
        <div class="mb-3">
          <div class="alert alert-light border-0 shadow-sm p-3 mb-3" style="border-radius: 12px; background: #f8fafc;">
            <div class="fw-bold text-dark fs-6 mb-2">Thank you for applying for ${jobTitle}</div>
            <div class="text-secondary style="white-space: pre-wrap; line-height: 1.6;">${fb.content || fb.summary || 'We appreciate the time you invested in the application process.'}</div>
          </div>

          <div class="row g-3 mb-3">
            <div class="col-md-6">
              <div class="card p-3 border-0 bg-success-subtle bg-opacity-10 h-100" style="border-radius: 10px;">
                <h6 class="fw-bold text-success mb-2">Your Matching Strengths</h6>
                <div>${strengthsList || '<span class="text-muted small">Strong technical background</span>'}</div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="card p-3 border-0 bg-danger-subtle bg-opacity-10 h-100" style="border-radius: 10px;">
                <h6 class="fw-bold text-danger mb-2">Key Role Requirements</h6>
                <div>${gapsList || '<span class="text-muted small">Role specific requirement focus</span>'}</div>
              </div>
            </div>
          </div>

          ${fb.recommendation ? `
            <div class="card p-3 border-primary border-opacity-25 bg-primary-subtle bg-opacity-10" style="border-radius: 10px;">
              <span class="fw-bold text-primary small d-block mb-1">Recommendation & Next Steps:</span>
              <span class="text-dark small">${fb.recommendation}</span>
            </div>
          ` : ''}
        </div>
      `;
    } catch (err) {
      bodyEl.innerHTML = `<div class="alert alert-warning py-3">No detailed feedback is available yet for this application.</div>`;
    }
  }

  document.addEventListener("ar:auth-ready", load);
})();
