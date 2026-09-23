/**
 * integrity-report.js — Controller for Recruiter Proctoring & Integrity Audit Dashboard.
 * Supports both Technical Coding Assessments and Live AI Video Interviews.
 * Displays integrity scores, risk levels, breakdown counters, chronological timelines,
 * dialogue transcripts, and human recruiter review decision recording.
 */

document.addEventListener("DOMContentLoaded", async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const sessionId = urlParams.get("id") || urlParams.get("attempt_id") || urlParams.get("interview_id") || urlParams.get("application_id");

  const spinner = document.getElementById("loading-spinner");
  const errorBox = document.getElementById("error-box");
  const errorMsg = document.getElementById("error-message");
  const content = document.getElementById("report-content");

  if (!sessionId) {
    spinner.classList.add("d-none");
    errorBox.classList.remove("d-none");
    errorMsg.textContent = "Missing attempt_id, interview_id, or application_id parameter.";
    return;
  }

  try {
    let reportData = null;
    if (window.proctoringAPI && window.proctoringAPI.getReport) {
      try {
        const res = await proctoringAPI.getReport(sessionId);
        reportData = res.data || res;
      } catch (err) {
        console.warn("Unified report endpoint failed, trying legacy:", err);
      }
    }

    if (!reportData) {
      const resIntegrity = await proctoringAPI.getIntegrity(sessionId);
      const resEvents = await proctoringAPI.getEvents(sessionId);
      reportData = {
        report_type: "coding_assessment",
        session_id: sessionId,
        candidate: { full_name: "Candidate", email: "" },
        integrity_result: resIntegrity.data || resIntegrity,
        events: resEvents.data || resEvents || [],
        event_counts: {},
        dialogue_transcript: [],
      };
    }

    renderIntegrityReport(reportData);
    spinner.classList.add("d-none");
    content.classList.remove("d-none");
  } catch (err) {
    console.error("Integrity Report Error:", err);
    spinner.classList.add("d-none");
    errorBox.classList.remove("d-none");
    errorMsg.textContent = err?.message || "Failed to load assessment integrity report.";
  }
});

function renderIntegrityReport(report) {
  const integrity = report.integrity_result || {};
  const events = report.events || [];
  const candidate = report.candidate || {};
  const isInterview = report.report_type === "interview";

  // Header Details
  const candNameEl = document.getElementById("cand-name");
  const assessNameEl = document.getElementById("assessment-name");
  const subIdEl = document.getElementById("sub-id");
  const dateEl = document.getElementById("assessment-date");

  if (candNameEl) candNameEl.textContent = candidate.full_name || "Candidate";
  if (assessNameEl) {
    assessNameEl.textContent = isInterview
      ? "AI Video Interview Session"
      : "Technical Coding Assessment";
  }
  if (subIdEl) subIdEl.textContent = report.session_id ? report.session_id.substring(0, 8) : "—";
  if (dateEl) dateEl.textContent = new Date().toLocaleDateString();

  // Overall Score & Risk Badge
  const scoreBadge = document.getElementById("overall-score-badge");
  const riskBadge = document.getElementById("risk-level-badge");
  const score = Math.round(integrity.overall_integrity_score !== undefined ? integrity.overall_integrity_score : 100);

  if (scoreBadge) {
    scoreBadge.textContent = `${score}%`;
    if (score >= 85) {
      scoreBadge.className = "score-badge risk-low shadow-sm";
    } else if (score >= 60) {
      scoreBadge.className = "score-badge risk-review shadow-sm";
    } else {
      scoreBadge.className = "score-badge risk-high shadow-sm";
    }
  }

  if (riskBadge) {
    riskBadge.textContent = integrity.risk_level || (score >= 85 ? "Low Risk" : (score >= 60 ? "Review Recommended" : "High Risk"));
  }

  // Sub-Scores
  setBar("browser", integrity.browser_score || 100);
  setBar("webcam", integrity.webcam_score || 100);
  setBar("audio", integrity.audio_score || 100);
  setBar("sim", integrity.code_similarity_score !== undefined ? integrity.code_similarity_score : 100);

  // Counters
  const counts = report.event_counts || {};
  let noFaceCnt = counts["NO_FACE_DETECTED"] || counts["NO_FACE"] || 0;
  let multiFaceCnt = counts["MULTIPLE_FACES_DETECTED"] || counts["MULTIPLE_FACES"] || 0;
  let tabSwitchCnt = counts["TAB_SWITCH"] || 0;
  let clipCnt = (counts["COPY_ATTEMPT"] || 0) + (counts["PASTE_ATTEMPT"] || 0) + (counts["CUT_ATTEMPT"] || 0) + (counts["PASTE"] || 0);
  let audioCnt = (counts["HIGH_AUDIO_SPIKE"] || 0) + (counts["SUSPICIOUS_AUDIO"] || 0) + (counts["NOISE_DETECTED"] || 0) + (counts["MIC_MUTED_OR_DISCONNECTED"] || 0);

  // If counts not in report.event_counts, count from events array
  if (!report.event_counts || Object.keys(report.event_counts).length === 0) {
    events.forEach(ev => {
      const type = (ev.event_type || "").toUpperCase();
      if (type.includes("NO_FACE")) noFaceCnt++;
      else if (type.includes("MULTIPLE_FACES")) multiFaceCnt++;
      else if (type.includes("TAB_SWITCH")) tabSwitchCnt++;
      else if (type.includes("COPY") || type.includes("PASTE") || type.includes("CUT")) clipCnt++;
      else if (type.includes("AUDIO") || type.includes("NOISE") || type.includes("MIC")) audioCnt++;
    });
  }

  const setCnt = (id, val) => {
    const el = document.getElementById(id);
    if (el) el.textContent = val;
  };
  setCnt("cnt-no-face", noFaceCnt);
  setCnt("cnt-multi-face", multiFaceCnt);
  setCnt("cnt-tab-switch", tabSwitchCnt);
  setCnt("cnt-clipboard", clipCnt);
  setCnt("cnt-audio-spike", audioCnt);

  // Evidence Summary
  const summaryText = document.getElementById("evidence-summary-text");
  if (summaryText) {
    summaryText.textContent = integrity.ai_summary || "Proctoring monitoring active. No critical infractions recorded.";
  }

  // Interview Dialogue Transcript (if interview)
  const transcriptSection = document.getElementById("transcript-section");
  const transcriptContainer = document.getElementById("dialogue-transcript-container");
  if (report.dialogue_transcript && report.dialogue_transcript.length > 0) {
    if (transcriptSection) transcriptSection.classList.remove("d-none");
    if (transcriptContainer) {
      transcriptContainer.innerHTML = report.dialogue_transcript.map(turn => `
        <div class="mb-2 p-2 bg-white rounded border border-light shadow-sm">
          <div class="d-flex justify-content-between align-items-center mb-1">
            <span class="badge ${turn.speaker === 'Candidate' ? 'bg-primary' : 'bg-secondary'}">${escapeHtml(turn.speaker || 'Candidate')}</span>
            <span class="small text-muted font-monospace">${escapeHtml(turn.timestamp || '')}</span>
          </div>
          <div class="small text-dark">${escapeHtml(turn.text || '')}</div>
        </div>
      `).join("");
    }
  }

  // Chronological Timeline with Filters
  renderTimeline(events);

  // Filter Buttons
  const filterBtns = document.querySelectorAll("#timeline-filters button");
  filterBtns.forEach(btn => {
    btn.onclick = () => {
      filterBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const f = btn.dataset.filter;
      if (f === "all") {
        renderTimeline(events);
      } else if (f === "camera") {
        renderTimeline(events.filter(e => e.event_type.includes("FACE")));
      } else if (f === "browser") {
        renderTimeline(events.filter(e => e.event_type.includes("TAB") || e.event_type.includes("WINDOW") || e.event_type.includes("PASTE") || e.event_type.includes("COPY")));
      } else if (f === "audio") {
        renderTimeline(events.filter(e => e.event_type.includes("AUDIO") || e.event_type.includes("MIC") || e.event_type.includes("NOISE")));
      }
    };
  });

  // Pre-fill existing recruiter decision if present
  if (integrity.recruiter_decision) {
    const sel = document.getElementById("decision-select");
    if (sel) sel.value = integrity.recruiter_decision;
  }
  if (integrity.recruiter_notes) {
    const notesEl = document.getElementById("decision-notes");
    if (notesEl) notesEl.value = integrity.recruiter_notes;
  }

  // Save decision handler
  const btnSave = document.getElementById("btn-save-decision");
  if (btnSave) {
    btnSave.onclick = async () => {
      const decision = document.getElementById("decision-select").value;
      const notes = document.getElementById("decision-notes").value;

      try {
        if (isInterview && proctoringAPI.saveInterviewDecision) {
          await proctoringAPI.saveInterviewDecision(report.session_id, { decision, notes });
        } else {
          await proctoringAPI.saveDecision(report.session_id, { decision, notes });
        }
        alert("Recruiter review decision saved successfully!");
        window.location.reload();
      } catch (e) {
        alert("Failed to save decision: " + (e.message || e));
      }
    };
  }
}

function renderTimeline(events) {
  const timelineContainer = document.getElementById("timeline-container");
  if (!timelineContainer) return;
  timelineContainer.innerHTML = "";

  if (!events || events.length === 0) {
    timelineContainer.innerHTML = '<div class="text-muted small">No proctoring events recorded for this session.</div>';
    return;
  }

  events.forEach(ev => {
    const item = document.createElement("div");
    const sev = (ev.severity || "low").toLowerCase();
    const isWarn = sev === "medium" || sev === "warning";
    const isDanger = sev === "high" || sev === "critical" || sev === "danger";

    item.className = `timeline-item ${isDanger ? "danger" : isWarn ? "warning" : ""}`;

    const timeStr = ev.occurred_at ? new Date(ev.occurred_at).toLocaleTimeString() : "—";
    const sevBadge = isDanger ? "bg-danger" : isWarn ? "bg-warning text-dark" : "bg-secondary";

    let durationLabel = "";
    if (ev.duration_seconds) {
      durationLabel = ` | Duration: ${ev.duration_seconds}s`;
    }

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
      <div class="text-muted small mb-1"><i class="bi bi-clock me-1"></i>${timeStr}${durationLabel} | Confidence: ${Math.round((ev.confidence || 1.0) * 100)}%</div>
      ${metaFormatted ? `<div class="font-monospace small text-secondary bg-light p-2 rounded mt-1">${escapeHtml(metaFormatted)}</div>` : ""}
    `;
    timelineContainer.appendChild(item);
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
