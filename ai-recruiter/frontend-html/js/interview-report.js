/**
 * interview-report.js — Renders interview evaluation report with PDF Export & Print capability.
 */
(function () {
  const params = new URLSearchParams(window.location.search);
  const interviewId = params.get("interview_id");

  const alertBox = document.getElementById("report-alert");
  const wrapper = document.getElementById("report-wrapper");
  const backLink = document.getElementById("back-link");
  const pdfBtn = document.getElementById("btn-download-pdf");
  const printBtn = document.getElementById("btn-print-report");

  function showAlert(message, variant) {
    if (!alertBox) return;
    alertBox.textContent = message;
    alertBox.className = `alert alert-${variant} py-2 no-print`;
    alertBox.classList.remove("d-none");
  }

  function scoreCard(label, value, icon) {
    const roundVal = value != null ? Math.round(value) : null;
    let badgeBg = "bg-secondary";
    if (roundVal != null) {
      if (roundVal >= 75) badgeBg = "bg-success";
      else if (roundVal >= 50) badgeBg = "bg-warning text-dark";
      else badgeBg = "bg-danger";
    }

    return `
      <div class="col-6 col-md-3 mb-3">
        <div class="card border-0 bg-body-secondary p-3 h-100 rounded-3 text-center">
          <div class="small text-muted mb-1">${icon || "📊"} ${label}</div>
          <div class="fs-3 fw-bold text-body">${roundVal != null ? roundVal + "%" : "—"}</div>
        </div>
      </div>
    `;
  }

  function listOrNone(items, emptyText) {
    if (!items || !items.length) return `<div class="text-muted small">${emptyText}</div>`;
    return `<ul class="mb-0 ps-3">${items.map((i) => `<li class="mb-1">${escapeHtml(i)}</li>`).join("")}</ul>`;
  }

  function escapeHtml(str) {
    if (!str) return "";
    return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function render(report, currentUser) {
    if (backLink) {
      backLink.href = currentUser.role === "recruiter" ? "my-jobs.html" : "my-applications.html";
    }

    if (report.status !== "completed") {
      wrapper.innerHTML = `
        <div class="card p-4 text-center border-0 shadow-sm rounded-4">
          <h5 class="fw-semibold mb-2">Interview In Progress</h5>
          <p class="text-muted mb-3">This interview evaluation has not been completed yet.</p>
          ${currentUser.role === "candidate" ? `<a href="interview.html?interview_id=${interviewId}" class="btn btn-primary fw-semibold">Continue Interview</a>` : ""}
        </div>
      `;
      return;
    }

    // Show PDF & Print buttons
    if (pdfBtn) {
      pdfBtn.classList.remove("d-none");
      pdfBtn.classList.add("d-inline-flex");
      pdfBtn.onclick = () => exportPDF(report);
    }
    if (printBtn) {
      printBtn.classList.remove("d-none");
      printBtn.classList.add("d-inline-flex");
      printBtn.onclick = () => window.print();
    }

    const evaluation = report.evaluation || {};
    const interviewDate = report.completed_at ? new Date(report.completed_at).toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' }) : "Recently Completed";

    const questionsHtml = (report.questions || [])
      .map((q, i) => `
        <div class="card p-3 mb-3 border-0 shadow-sm rounded-3">
          <div class="d-flex justify-content-between align-items-start mb-2">
            <div class="fw-bold text-body" style="font-size: 1.05rem;">Q${i + 1}. ${escapeHtml(q.question)}</div>
            <span class="badge ${q.answer_score >= 70 ? "bg-success" : q.answer_score >= 50 ? "bg-warning text-dark" : "bg-secondary"} fs-6">
              ${q.answer_score != null ? Math.round(q.answer_score) + "%" : "—"}
            </span>
          </div>
          <div class="small text-muted mb-2">
            <span class="badge bg-secondary-subtle text-body border">${(q.type || "general").replace("_", " ")}</span>
            <span class="badge bg-light text-dark border ms-1">${q.difficulty || "medium"}</span>
          </div>
          <div class="p-3 bg-body-tertiary rounded-3 mb-2">
            <div class="small fw-semibold text-muted mb-1">Candidate Answer:</div>
            <div class="text-body">${q.answer_text ? escapeHtml(q.answer_text) : '<em class="text-muted">No answer provided</em>'}</div>
          </div>
          ${q.feedback ? `
            <div class="small text-muted mt-2 border-top pt-2">
              <strong>Evaluation Feedback:</strong> ${escapeHtml(q.feedback)}
            </div>` : ""}
        </div>
      `).join("");

    wrapper.innerHTML = `
      <div class="card p-4 mb-4 border-0 shadow-sm rounded-4">
        <div class="d-flex justify-content-between align-items-start border-bottom pb-3 mb-3">
          <div>
            <div class="text-uppercase text-primary fw-bold small tracking-wide">Official Evaluation Report</div>
            <h3 class="fw-bold mb-1">${escapeHtml(report.candidate_name || "Candidate Profile")}</h3>
            <div class="text-muted fw-medium">${escapeHtml(report.job_title || "Target Position")} • <span class="small">${interviewDate}</span></div>
          </div>
          <div class="text-end">
            <div class="small text-muted mb-1">Overall Match Score</div>
            <span class="badge bg-primary fs-3 px-3 py-2 rounded-3">${evaluation.overall_score != null ? Math.round(evaluation.overall_score) + "%" : "—"}</span>
          </div>
        </div>

        <h6 class="fw-bold text-body mb-3">Category Breakdown</h6>
        <div class="row g-2 mb-3">
          ${scoreCard("Technical Skill", evaluation.technical_score, "💻")}
          ${scoreCard("Communication", evaluation.communication_score, "🗣️")}
          ${scoreCard("Problem Solving", evaluation.problem_solving_score, "🧠")}
          ${scoreCard("Relevance", evaluation.relevance_score, "🎯")}
        </div>

        <div class="row mb-4">
          <div class="col-md-6 mb-3 mb-md-0">
            <div class="card p-3 h-100 border bg-success-subtle border-success-subtle rounded-3">
              <h6 class="fw-bold text-success mb-2">Key Strengths</h6>
              ${listOrNone(evaluation.strengths, "No specific strengths recorded.")}
            </div>
          </div>
          <div class="col-md-6">
            <div class="card p-3 h-100 border bg-warning-subtle border-warning-subtle rounded-3">
              <h6 class="fw-bold text-warning-emphasis mb-2">Areas for Growth</h6>
              ${listOrNone(evaluation.weaknesses, "No specific growth areas recorded.")}
            </div>
          </div>
        </div>

        <div class="p-3 bg-body-tertiary rounded-3 mb-4">
          <h6 class="fw-bold text-body mb-2">AI Synthesis &amp; Recommendation</h6>
          <p class="mb-0 text-body" style="line-height: 1.6;">${escapeHtml(evaluation.recommendation || "Evaluation completed successfully.")}</p>
        </div>

        <div class="alert alert-warning py-3 mb-0 rounded-3 d-flex align-items-center gap-2">
          <span class="fs-4">⚠️</span>
          <div>
            <strong>Human Review Required:</strong> This AI evaluation serves as candidate decision support. Final hiring decisions require human recruiter verification and review.
          </div>
        </div>
      </div>

      <h5 class="fw-bold text-body mb-3 px-1">Detailed Question Evaluations</h5>
      ${questionsHtml}
    `;
  }

  function exportPDF(report) {
    const element = document.getElementById("report-printable-area");
    if (!element || typeof html2pdf === "undefined") {
      alert("PDF generator loading. Please try again in a moment.");
      return;
    }

    const candidateName = (report.candidate_name || "Candidate").replace(/[^a-zA-Z0-9]/g, "_");
    const filename = `AI_Interview_Report_${candidateName}.pdf`;

    const opt = {
      margin:       [0.5, 0.5, 0.5, 0.5],
      filename:     filename,
      image:        { type: 'jpeg', quality: 0.98 },
      html2canvas:  { scale: 2, useCORS: true },
      jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
    };

    html2pdf().set(opt).from(element).save();
  }

  document.addEventListener("ar:auth-ready", async (event) => {
    if (!interviewId) {
      showAlert("No interview specified.", "danger");
      return;
    }
    try {
      const res = await API.interviews.getReport(interviewId);
      render(res.data, event.detail.user);
    } catch (err) {
      showAlert(err.message || "Failed to load report", "danger");
      if (wrapper) wrapper.innerHTML = "";
    }
  });
})();
