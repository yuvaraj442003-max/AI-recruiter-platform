/**
 * bulk-upload.js — Recruiter Bulk Resume Upload & Batch Parsing Frontend Logic
 */
(function () {
  const BASE_URL = window.API_BASE_URL || (typeof API_BASE_URL !== "undefined" ? API_BASE_URL : "http://localhost:8000/api/v1");
  const getToken = () => (window.Session && window.Session.getAccessToken ? window.Session.getAccessToken() : (localStorage.getItem("ar_access_token") || ""));

  const dropzone = document.getElementById("bulk-upload-dropzone");
  const fileInput = document.getElementById("bulk-resume-file-input");
  const startBtn = document.getElementById("start-bulk-upload-btn");
  const jobSelect = document.getElementById("bulk-job-select");
  const statusContainer = document.getElementById("bulk-status-container");
  const statusLabel = document.getElementById("bulk-status-label");
  const statusCount = document.getElementById("bulk-status-count");
  const progressBar = document.getElementById("bulk-progress-bar");
  const resultsWrapper = document.getElementById("bulk-results-wrapper");
  const resultsTableBody = document.getElementById("bulk-results-table-body");
  const resultsCountBadge = document.getElementById("bulk-results-count-badge");
  const bestMatchBanner = document.getElementById("bulk-best-match-banner");

  // JD Collection Toggle Elements
  const btnModePosted = document.getElementById("btn-mode-posted-job");
  const btnModeCustom = document.getElementById("btn-mode-custom-jd");
  const sectionPosted = document.getElementById("section-posted-job");
  const sectionCustom = document.getElementById("section-custom-jd");

  let selectedFiles = [];
  let currentJdMode = "posted"; // 'posted' or 'custom'
  let currentResultsStore = [];

  if (!dropzone || !fileInput) return;

  // Toggle JD Collection Modes
  if (btnModePosted && btnModeCustom) {
    btnModePosted.addEventListener("click", () => {
      currentJdMode = "posted";
      btnModePosted.classList.add("active");
      btnModeCustom.classList.remove("active");
      sectionPosted.classList.remove("d-none");
      sectionCustom.classList.add("d-none");
    });

    btnModeCustom.addEventListener("click", () => {
      currentJdMode = "custom";
      btnModeCustom.classList.add("active");
      btnModePosted.classList.remove("active");
      sectionCustom.classList.remove("d-none");
      sectionPosted.classList.add("d-none");
    });
  }

  // Load posted jobs into select dropdown
  async function loadJobsDropdown() {
    if (!jobSelect) return;
    try {
      let response = await fetch(`${BASE_URL}/jobs/recruiter/my-jobs`, {
        headers: { Authorization: `Bearer ${getToken()}` },
      });
      if (!response.ok) {
        response = await fetch(`${BASE_URL}/jobs`, {
          headers: { Authorization: `Bearer ${getToken()}` },
        });
      }
      const res = await response.json();
      if (res.success && Array.isArray(res.data)) {
        jobSelect.innerHTML = `<option value="">General Candidate Talent Pool (No job linked)</option>` +
          res.data.map(j => `<option value="${j.id}">${escapeHtml(j.title)} (${j.location || "Remote"})</option>`).join("");
      }
    } catch (err) {
      console.warn("Could not load recruiter jobs for bulk upload:", err);
    }
  }

  const modalEl = document.getElementById("bulkUploadModal");
  if (modalEl) {
    modalEl.addEventListener("show.bs.modal", loadJobsDropdown);
  } else {
    loadJobsDropdown();
  }

  dropzone.addEventListener("click", () => fileInput.click());

  dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("bg-success-subtle");
  });

  dropzone.addEventListener("dragleave", () => {
    dropzone.classList.remove("bg-success-subtle");
  });

  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("bg-success-subtle");
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      selectedFiles = Array.from(e.dataTransfer.files);
      updateDropzoneLabel();
    }
  });

  fileInput.addEventListener("change", () => {
    if (fileInput.files && fileInput.files.length > 0) {
      selectedFiles = Array.from(fileInput.files);
      updateDropzoneLabel();
    }
  });

  function updateDropzoneLabel() {
    const heading = dropzone.querySelector("h6");
    if (heading) {
      heading.textContent = `Selected ${selectedFiles.length} file(s): ${selectedFiles.map(f => f.name).join(", ")}`;
    }
  }

  if (startBtn) {
    startBtn.addEventListener("click", async () => {
      if (selectedFiles.length === 0) {
        alert("Please select at least one PDF/DOCX resume file or ZIP archive.");
        return;
      }

      startBtn.disabled = true;
      statusContainer.classList.remove("d-none");
      statusLabel.textContent = "Uploading & analyzing resumes via ATS engine...";
      progressBar.style.width = "30%";
      statusCount.textContent = `0 / ${selectedFiles.length}`;

      const formData = new FormData();
      selectedFiles.forEach((file) => {
        formData.append("files", file, file.name);
      });

      if (currentJdMode === "posted" && jobSelect && jobSelect.value) {
        formData.append("job_id", jobSelect.value);
      } else if (currentJdMode === "custom") {
        const titleVal = document.getElementById("custom-jd-title")?.value || "";
        const expVal = document.getElementById("custom-jd-exp")?.value || "";
        const skillsVal = document.getElementById("custom-jd-skills")?.value || "";
        const descVal = document.getElementById("custom-jd-desc")?.value || "";

        if (titleVal) formData.append("custom_jd_title", titleVal);
        if (expVal) formData.append("custom_jd_exp", expVal);
        if (skillsVal) formData.append("custom_jd_skills", skillsVal);
        if (descVal) formData.append("custom_jd_description", descVal);
      }

      try {
        const token = getToken();
        progressBar.style.width = "60%";
        
        let response;
        try {
          response = await fetch(`${BASE_URL}/resumes/bulk-upload`, {
            method: "POST",
            headers: token ? { Authorization: `Bearer ${token}` } : {},
            body: formData,
          });
        } catch (fetchErr) {
          // Fallback check between localhost and 127.0.0.1
          const altBase = BASE_URL.includes("localhost") 
            ? BASE_URL.replace("localhost", "127.0.0.1")
            : BASE_URL.replace("127.0.0.1", "localhost");
          
          try {
            response = await fetch(`${altBase}/resumes/bulk-upload`, {
              method: "POST",
              headers: token ? { Authorization: `Bearer ${token}` } : {},
              body: formData,
            });
          } catch (_) {
            throw new Error("Unable to connect to the backend server (http://localhost:8000). Please check that FastAPI / Uvicorn is running.");
          }
        }

        if (!response.ok) {
          const errText = await response.text();
          let errMsg = `Server returned status ${response.status}`;
          try {
            const errJson = JSON.parse(errText);
            errMsg = errJson.message || errJson.detail || errMsg;
          } catch (_) {}
          alert(`Bulk upload failed: ${errMsg}`);
          return;
        }

        const res = await response.json();
        if (res.success && res.data) {
          progressBar.style.width = "100%";
          statusLabel.textContent = "Processing, ATS matching & deduplication complete!";
          statusCount.textContent = `${res.data.successful} stored (${res.data.duplicates || 0} duplicates linked), ${res.data.failed} failed`;
          currentResultsStore = res.data.results || [];
          renderResults(currentResultsStore, res.data.best_match);
        } else {
          alert(res.message || "Bulk upload failed.");
        }
      } catch (err) {
        console.error("Bulk upload error:", err);
        alert(`Error during bulk upload: ${err.message || err}`);
      } finally {
        startBtn.disabled = false;
      }
    });
  }

  function renderResults(results, bestMatch) {
    if (!resultsWrapper || !resultsTableBody) return;
    resultsWrapper.classList.remove("d-none");

    if (resultsCountBadge) {
      resultsCountBadge.textContent = `${results.length} Candidates Analyzed`;
    }

    if (bestMatch && bestMatch.candidate_name && bestMatchBanner) {
      bestMatchBanner.classList.remove("d-none");
      const nameEl = document.getElementById("best-candidate-name");
      const scoreEl = document.getElementById("best-candidate-score");
      const subEl = document.getElementById("best-candidate-subtitle");
      if (nameEl) nameEl.textContent = bestMatch.candidate_name;
      if (scoreEl) scoreEl.textContent = `${Math.round(bestMatch.score)}%`;
      if (subEl) subEl.textContent = `Ranked #1 candidate with top skills and highest ATS match score`;
    } else if (bestMatchBanner) {
      bestMatchBanner.classList.add("d-none");
    }

    if (results.length === 0) {
      resultsTableBody.innerHTML = `<tr><td colspan="6" class="text-center text-muted py-3">No files processed.</td></tr>`;
      return;
    }

    const token = getToken();

    resultsTableBody.innerHTML = results.map((r, index) => {
      const data = r.extracted_data || {};
      const score = Math.round(r.overall_match_score || 0);

      // Rank Badge
      let rankBadge = `<span class="badge bg-secondary">#${r.rank || index + 1}</span>`;
      if (r.is_best_match || index === 0) {
        rankBadge = `<span class="badge bg-warning text-dark fw-bold shadow-sm">🏆 #1 Top Match</span>`;
      }

      // Deduplication & Storage Status Badge
      let dedupBadge = `<span class="badge bg-success-subtle text-success border border-success">✨ Stored New</span>`;
      if (r.is_duplicate) {
        dedupBadge = `<span class="badge bg-warning-subtle text-dark border border-warning" title="${escapeHtml(r.duplicate_reason || "Duplicate candidate detected")}">🔄 Duplicate Linked</span>`;
      } else if (r.status === "failed") {
        dedupBadge = `<span class="badge bg-danger-subtle text-danger border border-danger">Failed</span>`;
      }

      // ATS Score Color
      let scoreBadgeClass = "bg-success";
      if (score < 50) scoreBadgeClass = "bg-danger";
      else if (score < 70) scoreBadgeClass = "bg-warning text-dark";
      else if (score < 85) scoreBadgeClass = "bg-info text-dark";

      const actionBtn = r.candidate_id
        ? `<div class="btn-group btn-group-sm">
             <button type="button" class="btn btn-sm btn-outline-primary py-0 px-2 fw-bold view-ats-btn" data-index="${index}" style="font-size: 0.75rem;">🔍 View ATS</button>
             <a href="${BASE_URL}/resumes/${r.candidate_id}/export?format=pdf&token=${encodeURIComponent(token)}" target="_blank" class="btn btn-sm btn-outline-success py-0 px-2 fw-bold" style="font-size: 0.75rem;">📄 Dossier</a>
           </div>`
        : `<span class="text-muted small">—</span>`;

      return `
        <tr class="${r.is_best_match ? 'table-warning-subtle fw-semibold' : ''}">
          <td>${rankBadge}</td>
          <td>
            <div class="fw-bold text-dark mb-0">${escapeHtml(data.name || r.filename)}</div>
            <div class="small text-muted font-monospace" style="font-size: 0.75rem;">${escapeHtml(r.filename)}</div>
          </td>
          <td>
            <div class="small">${escapeHtml(data.email || "—")}</div>
            <div class="small text-muted">${escapeHtml(data.phone || "—")}</div>
          </td>
          <td>${dedupBadge}</td>
          <td>
            <div class="d-flex align-items-center gap-2">
              <span class="badge ${scoreBadgeClass} px-2 py-1 fs-6">${score}%</span>
              <div class="progress flex-grow-1" style="height: 6px; min-width: 50px;">
                <div class="progress-bar ${scoreBadgeClass}" style="width: ${score}%;"></div>
              </div>
            </div>
          </td>
          <td>${actionBtn}</td>
        </tr>
      `;
    }).join("");

    // Attach event listeners for ATS view buttons
    document.querySelectorAll(".view-ats-btn").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        const idx = e.currentTarget.getAttribute("data-index");
        const item = currentResultsStore[idx];
        if (item) showAtsModal(item);
      });
    });
  }

  function showAtsModal(item) {
    const modalBody = document.getElementById("ats-modal-body");
    const modalTitle = document.getElementById("ats-modal-title");
    if (!modalBody) return;

    const data = item.extracted_data || {};
    const ats = item.ats_analysis || {};
    const bk = ats.score_breakdown || {};
    const overall = Math.round(item.overall_match_score || 0);

    if (modalTitle) {
      modalTitle.textContent = `ATS Analysis & Match Breakdown: ${data.name || item.filename}`;
    }

    const matchedSkills = ats.matched_skills || [];
    const missingSkills = ats.missing_skills || [];
    const suggestions = ats.suggestions || [];

    modalBody.innerHTML = `
      <div class="row g-3 align-items-center mb-4 p-3 bg-light rounded-3 border">
        <div class="col-md-3 text-center border-end">
          <div class="display-5 fw-bold text-success">${overall}%</div>
          <span class="badge bg-success-subtle text-success border border-success fw-bold uppercase">Overall ATS Match Score</span>
        </div>
        <div class="col-md-9">
          <div class="row g-2 small">
            <div class="col-6 col-md-4">
              <div class="text-muted mb-1">Skills Match: <strong>${Math.round(bk.skills || 0)}%</strong></div>
              <div class="progress" style="height: 5px;"><div class="progress-bar bg-success" style="width: ${bk.skills || 0}%;"></div></div>
            </div>
            <div class="col-6 col-md-4">
              <div class="text-muted mb-1">Experience: <strong>${Math.round(bk.experience || 0)}%</strong></div>
              <div class="progress" style="height: 5px;"><div class="progress-bar bg-info" style="width: ${bk.experience || 0}%;"></div></div>
            </div>
            <div class="col-6 col-md-4">
              <div class="text-muted mb-1">Keywords: <strong>${Math.round(bk.keywords || 0)}%</strong></div>
              <div class="progress" style="height: 5px;"><div class="progress-bar bg-primary" style="width: ${bk.keywords || 0}%;"></div></div>
            </div>
            <div class="col-6 col-md-4">
              <div class="text-muted mb-1">Responsibilities: <strong>${Math.round(bk.responsibilities || 0)}%</strong></div>
              <div class="progress" style="height: 5px;"><div class="progress-bar bg-warning" style="width: ${bk.responsibilities || 0}%;"></div></div>
            </div>
            <div class="col-6 col-md-4">
              <div class="text-muted mb-1">Education: <strong>${Math.round(bk.education || 0)}%</strong></div>
              <div class="progress" style="height: 5px;"><div class="progress-bar bg-secondary" style="width: ${bk.education || 0}%;"></div></div>
            </div>
            <div class="col-6 col-md-4">
              <div class="text-muted mb-1">Location: <strong>${Math.round(bk.location || 0)}%</strong></div>
              <div class="progress" style="height: 5px;"><div class="progress-bar bg-dark" style="width: ${bk.location || 0}%;"></div></div>
            </div>
          </div>
        </div>
      </div>

      <div class="row g-3 mb-3">
        <div class="col-md-6">
          <h6 class="fw-bold text-success mb-2">✅ Matched Skills (${matchedSkills.length})</h6>
          <div class="d-flex flex-wrap gap-1">
            ${matchedSkills.length > 0 
              ? matchedSkills.map(s => `<span class="badge bg-success-subtle text-success border border-success">${escapeHtml(s)}</span>`).join(" ")
              : `<span class="text-muted small">No direct skill matches detected</span>`}
          </div>
        </div>
        <div class="col-md-6">
          <h6 class="fw-bold text-danger mb-2">⚠️ Missing Required Skills (${missingSkills.length})</h6>
          <div class="d-flex flex-wrap gap-1">
            ${missingSkills.length > 0
              ? missingSkills.map(s => `<span class="badge bg-danger-subtle text-danger border border-danger">${escapeHtml(s)}</span>`).join(" ")
              : `<span class="text-muted small">No missing skills detected!</span>`}
          </div>
        </div>
      </div>

      ${suggestions.length > 0 ? `
        <div class="mt-3 p-3 bg-warning-subtle rounded-3 border border-warning">
          <h6 class="fw-bold text-dark mb-2">💡 AI Match &amp; Profile Recommendations</h6>
          <ul class="mb-0 small ps-3">
            ${suggestions.map(sg => `<li class="mb-1">${escapeHtml(sg)}</li>`).join("")}
          </ul>
        </div>
      ` : ""}
    `;

    const modalInst = new bootstrap.Modal(document.getElementById("atsBreakdownModal"));
    modalInst.show();
  }

  function escapeHtml(str) {
    if (!str) return "";
    return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
})();

