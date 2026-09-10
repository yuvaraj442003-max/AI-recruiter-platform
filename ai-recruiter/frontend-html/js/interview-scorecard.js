/**
 * interview-scorecard.js — Frontend controller for AI Executive Candidate Scorecard.
 * Manages Radar Chart rendering, timestamp click-to-jump video player seeking,
 * interactive chapter seeking, searchable transcript, and recruiter decision overrides.
 */

let currentScorecard = null;
let radarChartInstance = null;

document.addEventListener("DOMContentLoaded", () => {
  const urlParams = new URLSearchParams(window.location.search);
  const interviewId = urlParams.get("interview_id");

  if (!interviewId) {
    showAlert("No interview ID specified.", "danger");
    return;
  }

  // Bind back link if candidate/job context exists
  const backLink = document.getElementById("back-to-applicants");
  if (backLink) {
    const jobId = urlParams.get("job_id");
    if (jobId) {
      backLink.href = `job-applicants.html?job_id=${jobId}`;
    }
  }

  loadScorecard(interviewId);

  // Bind regenerate button
  const btnRegen = document.getElementById("btn-regenerate");
  if (btnRegen) {
    btnRegen.addEventListener("click", () => regenerateScorecard(interviewId));
  }

  // Bind Recruiter decision buttons
  document.querySelectorAll(".btn-decision").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      document.querySelectorAll(".btn-decision").forEach((b) => b.classList.remove("active", "btn-primary", "btn-success", "btn-warning", "btn-danger"));
      const dec = btn.dataset.decision;
      btn.classList.add("active");
      if (dec === "Strong Candidate") btn.classList.add("btn-success");
      else if (dec === "Shortlist") btn.classList.add("btn-primary");
      else if (dec === "Hold") btn.classList.add("btn-warning");
      else if (dec === "Reject") btn.classList.add("btn-danger");
      btn.dataset.selected = "true";
    });
  });

  // Bind save decision button
  const btnSaveDecision = document.getElementById("btn-save-decision");
  if (btnSaveDecision) {
    btnSaveDecision.addEventListener("click", saveRecruiterDecision);
  }

  // Bind search input for transcript
  const searchInput = document.getElementById("transcript-search-input");
  if (searchInput) {
    searchInput.addEventListener("input", filterTranscript);
  }
});

function showAlert(message, type = "info") {
  const alertEl = document.getElementById("scorecard-alert");
  if (!alertEl) return;
  alertEl.className = `alert alert-${type} py-2`;
  alertEl.textContent = message;
  alertEl.classList.remove("d-none");
}

async function loadScorecard(interviewId) {
  const spinner = document.getElementById("loading-spinner");
  const content = document.getElementById("scorecard-content");

  try {
    const scorecard = await window.interviewScorecardAPI.getScorecard(interviewId);
    currentScorecard = scorecard;

    if (spinner) spinner.classList.add("d-none");
    if (content) content.classList.remove("d-none");

    renderScorecard(scorecard);
  } catch (err) {
    if (spinner) spinner.classList.add("d-none");
    showAlert(err.message || "Failed to load candidate scorecard.", "danger");
  }
}

async function regenerateScorecard(interviewId) {
  if (!confirm("Re-analyze this interview session using AI Intelligence?")) return;

  const btnRegen = document.getElementById("btn-regenerate");
  if (btnRegen) {
    btnRegen.disabled = true;
    btnRegen.innerHTML = `<span>⏳</span> Re-analyzing…`;
  }

  try {
    const scorecard = await window.interviewScorecardAPI.regenerateScorecard(interviewId);
    currentScorecard = scorecard;
    renderScorecard(scorecard);
    showAlert("Scorecard re-analysis complete!", "success");
  } catch (err) {
    showAlert(err.message || "Failed to re-analyze scorecard.", "danger");
  } finally {
    if (btnRegen) {
      btnRegen.disabled = false;
      btnRegen.innerHTML = `<span>🔄</span> Re-analyze Interview`;
    }
  }
}

function renderScorecard(scorecard) {
  // Header details
  document.getElementById("candidate-name").textContent = scorecard.candidate_name || "Candidate Profile";
  document.getElementById("job-title").textContent = scorecard.job_title || "Target Position";

  const scoreVal = Math.round(scorecard.overall_score || 0);
  const badgeEl = document.getElementById("overall-badge");
  const scoreText = document.getElementById("badge-score");
  scoreText.textContent = scoreVal;

  if (scoreVal >= 80) badgeEl.className = "score-badge score-high";
  else if (scoreVal >= 60) badgeEl.className = "score-badge score-mid";
  else badgeEl.className = "score-badge score-low";

  const recBadge = document.getElementById("recommendation-badge");
  recBadge.textContent = scorecard.recommendation || "Recommended";
  if (scorecard.recommendation === "Strong Candidate") recBadge.className = "badge bg-success fs-6 px-3 py-2";
  else if (scorecard.recommendation === "Recommended") recBadge.className = "badge bg-primary fs-6 px-3 py-2";
  else if (scorecard.recommendation === "Consider") recBadge.className = "badge bg-warning text-dark fs-6 px-3 py-2";
  else recBadge.className = "badge bg-danger fs-6 px-3 py-2";

  document.getElementById("confidence-badge").textContent = `Confidence: ${scorecard.confidence || "High"}`;
  document.getElementById("executive-summary-text").textContent = scorecard.executive_summary || "Executive summary unavailable.";

  // Recruiter notes & decision state
  if (scorecard.recruiter_notes) {
    document.getElementById("recruiter-notes-input").value = scorecard.recruiter_notes;
  }
  if (scorecard.recruiter_decision) {
    document.querySelectorAll(".btn-decision").forEach((b) => {
      if (b.dataset.decision === scorecard.recruiter_decision) {
        b.classList.add("active", "btn-primary");
      }
    });
    document.getElementById("decision-status").textContent = `Saved decision: ${scorecard.recruiter_decision}`;
  }

  // Render Strengths & Weaknesses
  renderList("strengths-list", scorecard.strengths, "No specific strengths logged.");
  renderList("weaknesses-list", scorecard.weaknesses, "No significant risk areas identified.");

  // Render Radar Chart & Categories
  renderRadarChart(scorecard.categories || []);
  renderCategoriesList(scorecard.categories || []);

  // Render Chapters
  renderChapters(scorecard.chapters || []);

  // Render Key Moments
  renderKeyMoments(scorecard.key_moments || []);

  // Render Question Evaluations
  renderQuestionEvaluations(scorecard.question_evaluations || []);
}

function renderList(elementId, items, emptyText) {
  const container = document.getElementById(elementId);
  if (!container) return;
  container.innerHTML = "";

  if (!items || items.length === 0) {
    container.innerHTML = `<li class="text-muted">${emptyText}</li>`;
    return;
  }

  items.forEach((item) => {
    const li = document.createElement("li");
    li.className = "mb-1";
    li.textContent = item;
    container.appendChild(li);
  });
}

function renderRadarChart(categories) {
  const ctx = document.getElementById("competencyRadarChart");
  if (!ctx) return;

  const labels = categories.map((c) => c.category);
  const data = categories.map((c) => c.score);

  if (radarChartInstance) {
    radarChartInstance.destroy();
  }

  radarChartInstance = new Chart(ctx, {
    type: "radar",
    data: {
      labels: labels.length ? labels : ["Technical", "Problem Solving", "Communication", "Soft Skills", "Role Fit"],
      datasets: [
        {
          label: "Candidate Competency Score",
          data: data.length ? data : [85, 80, 75, 90, 85],
          fill: true,
          backgroundColor: "rgba(37, 99, 235, 0.2)",
          borderColor: "#2563eb",
          pointBackgroundColor: "#2563eb",
          pointBorderColor: "#fff",
          pointHoverBackgroundColor: "#fff",
          pointHoverBorderColor: "#2563eb",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          angleLines: { display: true },
          suggestedMin: 0,
          suggestedMax: 100,
          ticks: { stepSize: 20 },
        },
      },
      plugins: {
        legend: { display: false },
      },
    },
  });
}

function renderCategoriesList(categories) {
  const container = document.getElementById("categories-list");
  if (!container) return;
  container.innerHTML = "";

  categories.forEach((cat) => {
    const pct = Math.round(cat.score);
    const weightPct = Math.round(cat.weight * 100);

    let barClass = "bg-success";
    if (pct < 60) barClass = "bg-danger";
    else if (pct < 75) barClass = "bg-warning";

    const item = document.createElement("div");
    item.className = "mb-3";
    item.innerHTML = `
      <div class="d-flex justify-content-between align-items-center mb-1">
        <span class="fw-bold">${cat.category} <small class="text-muted">(Weight: ${weightPct}%)</small></span>
        <span class="fw-bold">${pct}/100</span>
      </div>
      <div class="progress" style="height: 6px;">
        <div class="progress-bar ${barClass}" role="progressbar" style="width: ${pct}%"></div>
      </div>
      <div class="text-muted fs-7 mt-1">${cat.evidence_summary || ""}</div>
    `;
    container.appendChild(item);
  });
}

function renderChapters(chapters) {
  const container = document.getElementById("chapters-container");
  if (!container) return;
  container.innerHTML = "";

  if (!chapters.length) {
    container.innerHTML = `<div class="p-3 text-muted">No timeline chapters recorded.</div>`;
    return;
  }

  chapters.forEach((ch) => {
    const startFmt = formatTime(ch.timestamp_start);
    const endFmt = formatTime(ch.timestamp_end);

    const btn = document.createElement("button");
    btn.className = "list-group-item list-group-item-action chapter-pill p-3 text-start";
    btn.onclick = () => seekToTime(ch.timestamp_start);
    btn.innerHTML = `
      <div class="d-flex justify-content-between align-items-center mb-1">
        <span class="fw-bold text-primary">${ch.sequence}. ${ch.title}</span>
        <span class="timestamp-link">${startFmt} - ${endFmt}</span>
      </div>
      <p class="small text-muted mb-0">${ch.summary || ""}</p>
    `;
    container.appendChild(btn);
  });
}

function renderKeyMoments(moments) {
  const container = document.getElementById("key-moments-grid");
  if (!container) return;
  container.innerHTML = "";

  if (!moments.length) {
    container.innerHTML = `<div class="col-12 text-muted">No key moment highlights logged.</div>`;
    return;
  }

  moments.forEach((km) => {
    const timeFmt = formatTime(km.timestamp_start);
    const impClass = km.importance === "High" ? "importance-high" : (km.importance === "Medium" ? "importance-medium" : "importance-low");

    const col = document.createElement("div");
    col.className = "col-md-6";
    col.innerHTML = `
      <div class="card key-moment-card ${impClass} h-100 shadow-sm" onclick="seekToTime(${km.timestamp_start})">
        <div class="card-body p-3">
          <div class="d-flex justify-content-between align-items-start mb-2">
            <span class="badge bg-primary-subtle text-primary fw-semibold">${km.category}</span>
            <span class="timestamp-link">▶ Jump to ${timeFmt}</span>
          </div>
          <h6 class="fw-bold mb-1">${km.title}</h6>
          <p class="small text-muted mb-2">${km.summary}</p>
          ${km.transcript_reference ? `<div class="small bg-body-tertiary p-2 rounded text-italic font-monospace">"${km.transcript_reference}"</div>` : ""}
        </div>
      </div>
    `;
    container.appendChild(col);
  });
}

function renderQuestionEvaluations(evals) {
  const container = document.getElementById("question-evaluations-container");
  if (!container) return;
  container.innerHTML = "";

  if (!evals.length) {
    container.innerHTML = `<div class="text-muted p-3">No question evaluations recorded.</div>`;
    return;
  }

  evals.forEach((qe, idx) => {
    const startFmt = qe.timestamp_start !== null ? formatTime(qe.timestamp_start) : null;
    const scoreVal = Math.round(qe.overall_score || 0);

    const card = document.createElement("div");
    card.className = "card border shadow-sm mb-3 question-eval-item";
    card.dataset.text = (qe.question_text + " " + qe.candidate_answer + " " + (qe.evaluation_summary || "")).toLowerCase();

    card.innerHTML = `
      <div class="card-header bg-body d-flex justify-content-between align-items-center py-3">
        <span class="fw-bold text-dark">Q${idx + 1}: ${qe.question_text}</span>
        <div class="d-flex align-items-center gap-2">
          ${startFmt ? `<span class="timestamp-link" onclick="seekToTime(${qe.timestamp_start})">▶ ${startFmt}</span>` : ""}
          <span class="badge ${scoreVal >= 75 ? "bg-success" : (scoreVal >= 60 ? "bg-warning text-dark" : "bg-danger")} fs-6">
            Score: ${scoreVal}/100
          </span>
        </div>
      </div>
      <div class="card-body">
        <div class="mb-3">
          <label class="fw-bold small text-muted text-uppercase mb-1">Candidate Answer:</label>
          <div class="transcript-turn speaker-candidate">
            "${qe.candidate_answer}"
          </div>
        </div>
        <div class="row g-2 mb-3 small text-center">
          <div class="col"><div class="p-2 bg-body-tertiary rounded border"><strong>Technical:</strong> ${Math.round(qe.technical_score)}</div></div>
          <div class="col"><div class="p-2 bg-body-tertiary rounded border"><strong>Accuracy:</strong> ${Math.round(qe.accuracy_score)}</div></div>
          <div class="col"><div class="p-2 bg-body-tertiary rounded border"><strong>Completeness:</strong> ${Math.round(qe.completeness_score)}</div></div>
          <div class="col"><div class="p-2 bg-body-tertiary rounded border"><strong>Clarity:</strong> ${Math.round(qe.clarity_score)}</div></div>
          <div class="col"><div class="p-2 bg-body-tertiary rounded border"><strong>Relevance:</strong> ${Math.round(qe.relevance_score)}</div></div>
        </div>
        ${qe.evaluation_summary ? `<div class="alert alert-light border mb-0 small"><strong>AI Feedback:</strong> ${qe.evaluation_summary}</div>` : ""}
      </div>
    `;
    container.appendChild(card);
  });
}

function seekToTime(seconds) {
  const player = document.getElementById("interview-media-player");
  if (player) {
    player.currentTime = seconds;
    player.play();
    player.scrollIntoView({ behavior: "smooth", block: "center" });
  }
}

function formatTime(seconds) {
  if (seconds === null || seconds === undefined) return "00:00";
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
}

function filterTranscript(e) {
  const query = e.target.value.toLowerCase().trim();
  const items = document.querySelectorAll(".question-eval-item");

  items.forEach((item) => {
    if (!query || item.dataset.text.includes(query)) {
      item.classList.remove("d-none");
    } else {
      item.classList.add("d-none");
    }
  });
}

async function saveRecruiterDecision() {
  if (!currentScorecard) return;

  const activeBtn = document.querySelector(".btn-decision.active");
  const decision = activeBtn ? activeBtn.dataset.decision : null;

  if (!decision) {
    showAlert("Please select a recruiter audit decision (Strong Candidate, Shortlist, Hold, or Reject).", "warning");
    return;
  }

  const notes = document.getElementById("recruiter-notes-input").value;
  const statusEl = document.getElementById("decision-status");

  try {
    const updated = await window.interviewScorecardAPI.saveDecision(currentScorecard.id, {
      decision: decision,
      notes: notes,
    });
    currentScorecard = updated;
    if (statusEl) {
      statusEl.textContent = `✅ Saved decision '${decision}' on ${new Date().toLocaleTimeString()}`;
      statusEl.className = "small text-success mt-1";
    }
  } catch (err) {
    showAlert(err.message || "Failed to save decision.", "danger");
  }
}
