/**
 * integrity-report.js — Controller for Recruiter Assessment Integrity Dashboard.
 * Displays integrity scores, risk levels, chronological monitoring timelines, and manual recruiter decision actions.
 */

document.addEventListener("DOMContentLoaded", async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const attemptId = urlParams.get("attempt_id") || urlParams.get("id");

  const spinner = document.getElementById("loading-spinner");
  const errorBox = document.getElementById("error-box");
  const errorMsg = document.getElementById("error-message");
  const content = document.getElementById("report-content");

  if (!attemptId) {
    spinner.classList.add("d-none");
    errorBox.classList.remove("d-none");
    errorMsg.textContent = "Missing attempt_id URL parameter.";
    return;
  }

  try {
    const resIntegrity = await proctoringAPI.getIntegrity(attemptId);
    const resEvents = await proctoringAPI.getEvents(attemptId);

    const integrityData = resIntegrity.data || resIntegrity;
    const eventsData = resEvents.data || resEvents || [];

    renderIntegrityReport(integrityData, eventsData, attemptId);
    spinner.classList.add("d-none");
    content.classList.remove("d-none");
  } catch (err) {
    console.error("Integrity Report Error:", err);
    spinner.classList.add("d-none");
    errorBox.classList.remove("d-none");
    errorMsg.textContent = err?.message || "Failed to load assessment integrity report.";
  }
});

function renderIntegrityReport(integrity, events, attemptId) {
  const scoreBadge = document.getElementById("overall-score-badge");
  const riskBadge = document.getElementById("risk-level-badge");

  const score = Math.round(integrity.overall_integrity_score || 100);
  scoreBadge.textContent = `${score}%`;

  if (score >= 85) {
    scoreBadge.className = "score-badge risk-low shadow-sm";
  } else if (score >= 60) {
    scoreBadge.className = "score-badge risk-review shadow-sm";
  } else {
    scoreBadge.className = "score-badge risk-high shadow-sm";
  }

  riskBadge.textContent = integrity.risk_level || "Low Risk";

  // Sub-scores
  setBar("browser", integrity.browser_score || 100);
  setBar("webcam", integrity.webcam_score || 100);
  setBar("audio", integrity.audio_score || 100);
  setBar("sim", integrity.code_similarity_score || 100);

  // Evidence summary
  const summaryText = document.getElementById("evidence-summary-text");
  summaryText.textContent = integrity.ai_summary || "AI-Assisted Integrity Monitoring summary recorded.";

  // Timeline
  const timelineContainer = document.getElementById("timeline-container");
  timelineContainer.innerHTML = "";

  if (!events || events.length === 0) {
    timelineContainer.innerHTML = '<div class="text-muted small">No integrity events logged during this assessment attempt.</div>';
  } else {
    events.forEach(ev => {
      const item = document.createElement("div");
      const sev = (ev.severity || "low").toLowerCase();
      const isWarn = sev === "medium" || sev === "warning";
      const isDanger = sev === "high" || sev === "critical" || sev === "danger";

      item.className = `timeline-item ${isDanger ? "danger" : isWarn ? "warning" : ""}`;

      const timeStr = ev.occurred_at ? new Date(ev.occurred_at).toLocaleTimeString() : "—";
      const sevBadge = isDanger ? "bg-danger" : isWarn ? "bg-warning text-dark" : "bg-secondary";

      let metaFormatted = "";
      if (ev.metadata_json) {
        try {
          const parsed = typeof ev.metadata_json === "string" ? JSON.parse(ev.metadata_json) : ev.metadata_json;
          metaFormatted = JSON.stringify(parsed);
        } catch (e) {
          metaFormatted = ev.metadata_json;
        }
      }

      item.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-1">
          <strong class="text-dark">${escapeHtml(ev.event_type)}</strong>
          <span class="badge ${sevBadge} text-uppercase small">${sev}</span>
        </div>
        <div class="text-muted small mb-1"><i class="bi bi-clock me-1"></i>${timeStr} | Confidence: ${Math.round((ev.confidence || 1.0) * 100)}%</div>
        ${metaFormatted ? `<div class="font-monospace small text-secondary bg-light p-2 rounded mt-1">${escapeHtml(metaFormatted)}</div>` : ""}
      `;
      timelineContainer.appendChild(item);
    });
  }

  // Pre-fill existing decision if present
  if (integrity.recruiter_decision) {
    document.getElementById("decision-select").value = integrity.recruiter_decision;
  }
  if (integrity.recruiter_notes) {
    document.getElementById("decision-notes").value = integrity.recruiter_notes;
  }

  // Save decision handler
  const btnSave = document.getElementById("btn-save-decision");
  btnSave.addEventListener("click", async () => {
    const decision = document.getElementById("decision-select").value;
    const notes = document.getElementById("decision-notes").value;

    try {
      await proctoringAPI.saveDecision(attemptId, { decision, notes });
      alert("Recruiter decision saved successfully!");
      window.location.reload();
    } catch (e) {
      alert("Failed to save decision: " + (e.message || e));
    }
  });
}

function setBar(id, val) {
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
