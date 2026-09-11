/**
 * screening-detail.js — Controller for Recruiter Screening Detail Page.
 * Fetches screening sessions, sub-scores, transcripts, and handles manual recruiter overrides.
 */

document.addEventListener("DOMContentLoaded", async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const applicationId = urlParams.get("application_id");
  const screeningId = urlParams.get("screening_id");

  const spinner = document.getElementById("loading-spinner");
  const errorBox = document.getElementById("error-box");
  const errorMsg = document.getElementById("error-message");
  const content = document.getElementById("screening-content");

  if (!applicationId && !screeningId) {
    spinner.classList.add("d-none");
    errorBox.classList.remove("d-none");
    errorMsg.textContent = "Missing application_id or screening_id URL parameter.";
    return;
  }

  try {
    let sessionData;
    if (applicationId) {
      const res = await screeningAPI.getByApplication(applicationId);
      sessionData = res.data || res;
    } else {
      const res = await screeningAPI.getSession(screeningId);
      sessionData = res.data || res;
    }

    renderScreeningDetails(sessionData);
    spinner.classList.add("d-none");
    content.classList.remove("d-none");
  } catch (err) {
    loggerError(err);
    spinner.classList.add("d-none");
    errorBox.classList.remove("d-none");
    errorMsg.textContent = err?.message || "Failed to load screening session data.";
  }
});

function loggerError(err) {
  console.error("Screening Detail Error:", err);
}

function renderScreeningDetails(session) {
  const channelBadge = document.getElementById("channel-badge");
  const candidateName = document.getElementById("candidate-name");
  const jobTitle = document.getElementById("job-title");
  const completedDate = document.getElementById("completed-date");
  const questionCount = document.getElementById("question-count");
  const statusText = document.getElementById("status-text");

  const scoreBadge = document.getElementById("score-badge");
  const recBadge = document.getElementById("recommendation-badge");

  channelBadge.textContent = (session.channel || "WhatsApp").toUpperCase() + " SCREENING";
  if (candidateName) candidateName.textContent = session.candidate_name || session.candidate_email || "Candidate Profile";
  if (jobTitle) jobTitle.textContent = session.job_title || "Target Position";

  statusText.textContent = (session.status || "Pending").toUpperCase();
  questionCount.textContent = `${session.current_question_index || 0} / ${session.total_questions || 0} Questions Answered`;

  const dateStr = session.completed_at || session.created_at;
  completedDate.textContent = dateStr ? new Date(dateStr).toLocaleDateString() : "In Progress";

  const score = session.screening_score != null ? Math.round(session.screening_score) : 0;
  scoreBadge.textContent = `${score}%`;

  const statusLower = (session.status || "").toLowerCase();
  const isFailed = statusLower === "failed" || (session.recommendation || "").toLowerCase().includes("fail") || (session.recommendation || "").toLowerCase().includes("reject");

  if (score >= 85 && !isFailed) {
    scoreBadge.className = "score-badge score-high shadow-sm";
  } else if (score >= 70 && !isFailed) {
    scoreBadge.className = "score-badge score-mid shadow-sm";
  } else {
    scoreBadge.className = "score-badge score-low shadow-sm";
  }

  if (isFailed) {
    recBadge.textContent = "❌ ASSESSMENT FAILED (NOT RECOMMENDED)";
    recBadge.className = "mt-2 fw-bold text-center text-danger bg-white px-2 py-1 rounded shadow-sm";
  } else if (session.recommendation) {
    recBadge.textContent = session.recommendation.toUpperCase();
  } else if (statusLower === "completed") {
    recBadge.textContent = "PASSED";
  } else {
    recBadge.textContent = "PENDING EVALUATION";
  }

  // Sub-scores from session.result
  const result = session.result || {};
  setSubScore("tech", result.technical_score || 75);
  setSubScore("exp", result.experience_score || 75);
  setSubScore("loc", result.location_score || 80);
  setSubScore("avail", result.availability_score || 80);
  setSubScore("sal", result.salary_score || 80);
  setSubScore("comm", result.communication_score || 85);

  const aiSummaryText = document.getElementById("ai-summary-text");
  if (result.ai_summary) {
    aiSummaryText.innerHTML = result.ai_summary.split("\n").map(line => `<div class="mb-1">${escapeHtml(line)}</div>`).join("");
  } else {
    aiSummaryText.textContent = "Detailed AI summary available upon completion of all questions.";
  }

  // Populate Q&A Transcript
  const qaContainer = document.getElementById("qa-list-container");
  qaContainer.innerHTML = "";

  const questions = session.questions || [];
  const answers = session.answers || [];
  const answerMap = {};
  answers.forEach(a => { answerMap[a.screening_question_id] = a; });

  if (questions.length === 0) {
    qaContainer.innerHTML = '<div class="alert alert-info">No screening questions recorded yet.</div>';
    return;
  }

  questions.forEach((q, idx) => {
    const ans = answerMap[q.id];
    const card = document.createElement("div");
    card.className = "qa-card shadow-sm";

    let extractedFormatted = "No data extracted";
    if (ans && ans.extracted_value) {
      try {
        const obj = JSON.parse(ans.extracted_value);
        extractedFormatted = JSON.stringify(obj, null, 2);
      } catch (e) {
        extractedFormatted = ans.extracted_value;
      }
    }

    const qScore = ans ? Math.round(ans.ai_score) : 0;
    const scoreClass = qScore >= 80 ? "text-success" : qScore >= 60 ? "text-warning" : "text-danger";

    card.innerHTML = `
      <div class="d-flex justify-content-between align-items-start mb-2">
        <h6 class="fw-bold mb-0 text-primary">Q${idx + 1} (${escapeHtml(q.question_type)}): ${escapeHtml(q.question)}</h6>
        ${ans ? `<span class="badge bg-light ${scoreClass} fs-6 border">Score: ${qScore}%</span>` : '<span class="badge bg-secondary">Unanswered</span>'}
      </div>
      <p class="text-muted small mb-2"><strong>Expected Criteria:</strong> ${escapeHtml(q.expected_answer || 'N/A')}</p>
      <div class="mb-3">
        <strong class="text-dark">Candidate Answer:</strong>
        <div class="p-3 bg-light rounded mt-1 text-secondary fs-6" style="white-space: pre-wrap;">${ans ? escapeHtml(ans.candidate_answer) : '<i>Awaiting response...</i>'}</div>
      </div>
      ${ans ? `
      <div>
        <strong class="text-dark small">AI Extracted Data & Justification:</strong>
        <div class="extracted-box mt-1">${escapeHtml(extractedFormatted)}</div>
        <div class="text-muted small mt-1"><em>Reason: ${escapeHtml(ans.ai_reason || 'Evaluated')}</em></div>
      </div>
      ` : ''}
    `;
    qaContainer.appendChild(card);
  });

  // Setup Override Handler
  const btnSaveOverride = document.getElementById("btn-save-override");
  btnSaveOverride.addEventListener("click", async () => {
    const overrideVal = document.getElementById("override-select").value;
    const reasonVal = document.getElementById("override-reason").value;

    if (!overrideVal) {
      alert("Please select an override recommendation option.");
      return;
    }

    try {
      const formData = new FormData();
      formData.append("override_recommendation", overrideVal);
      formData.append("reason", reasonVal);

      await screeningAPI.override(session.id, formData);
      alert("Recruiter override saved successfully!");
      window.location.reload();
    } catch (err) {
      alert("Failed to save override: " + (err.message || err));
    }
  });
}

function setSubScore(id, val) {
  const roundVal = Math.round(val);
  const scoreEl = document.getElementById(`score-${id}`);
  const barEl = document.getElementById(`bar-${id}`);
  if (scoreEl) scoreEl.textContent = `${roundVal}%`;
  if (barEl) barEl.style.width = `${roundVal}%`;
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
