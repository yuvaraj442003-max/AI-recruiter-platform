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
  const searchInput = document.getElementById("candidate-table-search");

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

  // Load existing uploaded candidates on page load
  async function loadExistingCandidates() {
    if (!resultsTableBody) return;
    try {
      const token = getToken();
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      let response = await fetch(`${BASE_URL}/resumes/recruiter/my-candidates`, { headers });
      if (response.ok) {
        const res = await response.json();
        if (res.success && Array.isArray(res.data) && res.data.length > 0) {
          currentResultsStore = res.data;
          renderResults(currentResultsStore);
        }
      }
    } catch (err) {
      console.warn("Could not load existing uploaded candidates:", err);
    }
  }

  loadExistingCandidates();

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

  // Live Search Filter for Extracted Table
  if (searchInput) {
    searchInput.addEventListener("input", () => {
      const query = searchInput.value.trim().toLowerCase();
      if (!query) {
        renderResults(currentResultsStore);
        return;
      }
      const filtered = currentResultsStore.filter((item) => {
        const d = item.extracted_data || {};
        const name = (d.name || item.filename || "").toLowerCase();
        const email = (d.email || "").toLowerCase();
        const phone = (d.phone || "").toLowerCase();
        const location = (d.location || "").toLowerCase();
        const skills = (Array.isArray(d.skills) ? d.skills.join(" ") : d.skills || "").toLowerCase();
        const exp = String(d.experience_years || "").toLowerCase();
        return (
          name.includes(query) ||
          email.includes(query) ||
          phone.includes(query) ||
          location.includes(query) ||
          skills.includes(query) ||
          exp.includes(query)
        );
      });
      renderResults(filtered, null, true);
    });
  }

  if (startBtn) {
    startBtn.addEventListener("click", async () => {
      if (selectedFiles.length === 0) {
        alert("Please select at least one PDF/DOCX resume file or ZIP archive.");
        return;
      }

      startBtn.disabled = true;
      if (statusContainer) statusContainer.classList.remove("d-none");
      if (statusLabel) statusLabel.textContent = "Uploading & analyzing resumes via AI parser...";
      if (progressBar) progressBar.style.width = "30%";
      if (statusCount) statusCount.textContent = `0 / ${selectedFiles.length}`;

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
        if (progressBar) progressBar.style.width = "60%";

        let response;
        try {
          response = await fetch(`${BASE_URL}/resumes/bulk-upload`, {
            method: "POST",
            headers: token ? { Authorization: `Bearer ${token}` } : {},
            body: formData,
          });
        } catch (fetchErr) {
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
            throw new Error("Unable to connect to backend server. Please verify FastAPI server is running.");
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
          if (progressBar) progressBar.style.width = "100%";
          if (statusLabel) statusLabel.textContent = "Processing, ATS matching & candidate parsing complete!";
          if (statusCount) statusCount.textContent = `${res.data.successful} stored (${res.data.duplicates || 0} duplicates linked), ${res.data.failed} failed`;
          currentResultsStore = res.data.results || [];
          renderResults(currentResultsStore, res.data.best_match);
          if (typeof window.refreshRecruiterDashboardUploadedResumes === "function") {
            window.refreshRecruiterDashboardUploadedResumes();
          }
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

  function renderResults(results, bestMatch = null, isFiltered = false) {
    if (!resultsWrapper || !resultsTableBody) return;
    resultsWrapper.classList.remove("d-none");

    if (resultsCountBadge) {
      resultsCountBadge.textContent = `${results.length} Candidates`;
    }

    if (!isFiltered) {
      if (bestMatch && bestMatch.candidate_name && bestMatchBanner) {
        bestMatchBanner.classList.remove("d-none");
        const nameEl = document.getElementById("best-candidate-name");
        const scoreEl = document.getElementById("best-candidate-score");
        const subEl = document.getElementById("best-candidate-subtitle");
        if (nameEl) nameEl.textContent = bestMatch.candidate_name;
        if (scoreEl) scoreEl.textContent = `${Math.round(bestMatch.score)}%`;
        if (subEl) subEl.textContent = `Ranked #1 candidate with top matching skills and experience profile.`;
      } else if (bestMatchBanner) {
        bestMatchBanner.classList.add("d-none");
      }
    }

    if (results.length === 0) {
      resultsTableBody.innerHTML = `<tr><td colspan="7" class="text-center text-muted py-4">No candidates found.</td></tr>`;
      return;
    }

    const token = getToken();

    resultsTableBody.innerHTML = results.map((r, index) => {
      const data = r.extracted_data || {};
      const score = Math.round(r.overall_match_score || 0);

      // Matched Job Role logic
      const matchedRole = r.matched_job_role || r.best_suited_role?.best_role_title || data.matched_job_role || data.current_role || data.headline || "Software Professional";
      const roleScore = r.best_suited_role?.best_match_score || score;
      const isActiveJob = r.best_suited_role?.is_active_job;
      const activePill = isActiveJob ? `<span class="badge bg-success text-white small" style="font-size: 0.65rem;" title="Matches an open job opening you posted">🏢 Open Job</span>` : '';

      // Secondary matched roles
      const matchedRolesList = r.matched_roles || r.best_suited_role?.matched_roles || data.matched_roles || [];
      const secondaryRoles = matchedRolesList
        .filter(mr => mr.title && mr.title.toLowerCase() !== matchedRole.toLowerCase())
        .slice(0, 2);

      let secondaryRolesHtml = "";
      if (secondaryRoles.length > 0) {
        secondaryRolesHtml = `<div class="mt-1 d-flex flex-wrap gap-1 align-items-center">
          <span class="text-muted" style="font-size: 0.7rem;">Also fits:</span>
          ${secondaryRoles.map(sr => `<span class="badge bg-secondary-subtle text-dark border border-secondary-subtle" style="font-size: 0.7rem;" title="${escapeHtml(sr.explanation || '')}">${escapeHtml(sr.title)} (${sr.score}%)</span>`).join("")}
        </div>`;
      }

      const roleBadge = `
        <div class="d-flex flex-column align-items-start">
          <div class="d-flex align-items-center gap-1 flex-wrap">
            <span class="badge bg-primary-subtle text-primary border border-primary-subtle px-2 py-1 fs-6 fw-bold shadow-sm d-inline-flex align-items-center gap-1" title="${escapeHtml(r.best_suited_role?.explanation || 'Best suited job position identified for candidate')}">
              <span>🎯</span> ${escapeHtml(matchedRole)}
            </span>
            ${activePill}
          </div>
          <div class="small text-muted mt-1" style="font-size: 0.75rem;">Fit: <strong class="text-dark">${roleScore}% Match</strong></div>
          ${secondaryRolesHtml}
        </div>
      `;

      // Rank Badge
      let rankBadge = `<span class="badge bg-secondary">#${r.rank || index + 1}</span>`;
      if (r.is_best_match || (!isFiltered && index === 0 && score > 0)) {
        rankBadge = `<span class="badge bg-warning text-dark fw-bold shadow-sm">🏆 #1 Match</span>`;
      }

      // Deduplication Badge
      let dedupBadge = `<span class="badge bg-success-subtle text-success border border-success">✨ New</span>`;
      if (r.is_duplicate) {
        dedupBadge = `<span class="badge bg-warning-subtle text-dark border border-warning" title="${escapeHtml(r.duplicate_reason || "Duplicate candidate detected")}">🔄 Duplicate</span>`;
      } else if (r.status === "failed") {
        dedupBadge = `<span class="badge bg-danger-subtle text-danger border border-danger">Failed</span>`;
      }

      // Skills Badges (Top 3)
      const skillsArr = Array.isArray(data.skills) ? data.skills : (data.skills ? String(data.skills).split(",") : []);
      const topSkillsBadges = skillsArr.slice(0, 3).map(s => `<span class="badge bg-primary-subtle text-primary border border-primary-subtle me-1 mb-1">${escapeHtml(s.trim())}</span>`).join("");
      const remainingSkillsCount = skillsArr.length > 3 ? `<span class="badge bg-light text-muted border">+${skillsArr.length - 3}</span>` : "";

      // Social Links (LinkedIn, GitHub, Portfolio)
      let linksHtml = [];
      if (data.linkedin_url) {
        linksHtml.push(`<a href="${escapeHtml(data.linkedin_url)}" target="_blank" class="badge bg-info-subtle text-info border border-info-subtle text-decoration-none me-1" title="LinkedIn Profile">LinkedIn 🔗</a>`);
      }
      if (data.github_url) {
        linksHtml.push(`<a href="${escapeHtml(data.github_url)}" target="_blank" class="badge bg-dark-subtle text-dark border border-dark-subtle text-decoration-none me-1" title="GitHub Profile">GitHub 💻</a>`);
      }
      if (data.portfolio_url) {
        linksHtml.push(`<a href="${escapeHtml(data.portfolio_url)}" target="_blank" class="badge bg-success-subtle text-success border border-success-subtle text-decoration-none me-1" title="Portfolio / Website">Portfolio 🌐</a>`);
      }

      // ATS Score Color
      let scoreBadgeClass = "bg-success";
      if (score < 50) scoreBadgeClass = "bg-danger";
      else if (score < 70) scoreBadgeClass = "bg-warning text-dark";
      else if (score < 85) scoreBadgeClass = "bg-info text-dark";

      const actionBtn = r.candidate_id
        ? `<div class="d-flex flex-column gap-1">
             <button type="button" class="btn btn-sm btn-success py-1 px-2 fw-bold view-cand-btn" data-index="${index}" style="font-size: 0.75rem;">👤 View Details</button>
             <div class="d-flex gap-1">
               <button type="button" class="btn btn-sm btn-outline-primary py-0 px-2 fw-semibold view-ats-btn" data-index="${index}" style="font-size: 0.72rem;">📊 ATS Match</button>
               <button type="button" class="btn btn-sm btn-outline-danger py-0 px-2 fw-semibold delete-cand-btn" data-index="${index}" style="font-size: 0.72rem;">🗑️ Delete</button>
             </div>
           </div>`
        : `<span class="text-muted small">—</span>`;

      return `
        <tr class="${r.is_best_match ? 'table-warning-subtle fw-semibold' : ''}">
          <td>${rankBadge}<div class="mt-1">${dedupBadge}</div></td>
          <td>
            <div class="fw-bold text-dark mb-0 fs-6">${escapeHtml(data.name || r.filename)}</div>
            <div class="small text-muted"><a href="mailto:${escapeHtml(data.email || '')}" class="text-decoration-none text-muted">${escapeHtml(data.email || "—")}</a></div>
            <div class="small text-muted">${escapeHtml(data.phone || "—")}</div>
          </td>
          <td>
            ${roleBadge}
          </td>
          <td>
            <div class="mb-1">${topSkillsBadges} ${remainingSkillsCount}</div>
            <div class="small text-muted">Exp: <strong>${data.experience_years ? data.experience_years + ' yrs' : 'Not specified'}</strong></div>
          </td>
          <td style="max-width: 220px;">
            <div class="small fw-semibold text-dark text-truncate" title="${escapeHtml(data.education || 'No education listed')}">
              🎓 ${escapeHtml(formatCompactEducation(data.education))}
            </div>
            <div class="small text-muted text-truncate" title="${escapeHtml(data.location || 'No location listed')}">
              📍 ${escapeHtml(formatCompactLocation(data.location))}
            </div>
          </td>
          <td>
            <div class="mb-1">${linksHtml.length > 0 ? linksHtml.join("") : '<span class="text-muted small">No links detected</span>'}</div>
            <div class="small font-monospace text-muted">📄 ${escapeHtml(r.filename)}</div>
          </td>
          <td>
            <div class="d-flex align-items-center gap-2">
              <span class="badge ${scoreBadgeClass} px-2 py-1 fs-6">${score}%</span>
            </div>
            <div class="progress mt-1" style="height: 5px; min-width: 60px;">
              <div class="progress-bar ${scoreBadgeClass}" style="width: ${score}%;"></div>
            </div>
          </td>
          <td class="text-end">${actionBtn}</td>
        </tr>
      `;
    }).join("");

    // Attach event listeners for ATS, Candidate Details, and Delete buttons
    document.querySelectorAll(".view-ats-btn").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        const idx = e.currentTarget.getAttribute("data-index");
        const item = results[idx];
        if (item) showAtsModal(item);
      });
    });

    document.querySelectorAll(".view-cand-btn").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        const idx = e.currentTarget.getAttribute("data-index");
        const item = results[idx];
        if (item) showCandidateDetailsModal(item);
      });
    });

    document.querySelectorAll(".delete-cand-btn").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        const idx = e.currentTarget.getAttribute("data-index");
        const item = results[idx];
        if (item && item.candidate_id) {
          deleteCandidate(item.candidate_id, (item.extracted_data && item.extracted_data.name) || item.filename);
        }
      });
    });
  }

  function showCandidateDetailsModal(item) {
    const modalBody = document.getElementById("cand-modal-body");
    const modalTitle = document.getElementById("cand-modal-title");
    if (!modalBody) return;

    const data = item.extracted_data || {};
    const token = getToken();

    if (modalTitle) {
      modalTitle.textContent = `Candidate Details: ${data.name || item.filename}`;
    }

    const skillsArr = Array.isArray(data.skills) ? data.skills : (data.skills ? String(data.skills).split(",") : []);
    const skillsBadges = skillsArr.map(s => `<span class="badge bg-primary-subtle text-primary border border-primary-subtle px-2 py-1 fs-6 me-1 mb-1">${escapeHtml(s.trim())}</span>`).join(" ");

    const matchedRoleModal = item.matched_job_role || item.best_suited_role?.best_role_title || data.matched_job_role || data.current_role || data.headline || 'Candidate Profile';
    const roleScoreModal = item.best_suited_role?.best_match_score || Math.round(item.overall_match_score || 0);

    modalBody.innerHTML = `
      <div class="row g-4">
        <!-- Candidate Overview Card -->
        <div class="col-md-4 border-end">
          <div class="text-center p-3 bg-light rounded-4 border mb-3">
            <div class="fs-1 mb-2">👤</div>
            <h4 class="fw-bold text-dark mb-1">${escapeHtml(data.name || item.filename)}</h4>
            <div class="badge bg-primary-subtle text-primary border border-primary-subtle px-3 py-1 mb-2">🎯 ${escapeHtml(matchedRoleModal)} (${roleScoreModal}% Fit)</div>
            <div><span class="badge bg-success-subtle text-success border border-success px-3 py-1">ATS Score: ${Math.round(item.overall_match_score || 0)}%</span></div>
          </div>

          <div class="card border-0 bg-light rounded-3 p-3 mb-3">
            <h6 class="fw-bold text-dark mb-3 border-bottom pb-2">📋 Contact &amp; Location</h6>
            <div class="small mb-2"><strong>📧 Email:</strong> ${escapeHtml(data.email || 'N/A')}</div>
            <div class="small mb-2"><strong>📞 Phone:</strong> ${escapeHtml(data.phone || 'N/A')}</div>
            <div class="small mb-2"><strong>📍 Location:</strong> ${escapeHtml(data.location || 'N/A')}</div>
            <div class="small mb-2"><strong>🏠 Address:</strong> ${escapeHtml(data.address || 'N/A')}</div>
            <div class="small"><strong>⏳ Experience:</strong> ${data.experience_years ? data.experience_years + ' years' : 'N/A'}</div>
          </div>

          <div class="card border-0 bg-light rounded-3 p-3 mb-3">
            <h6 class="fw-bold text-dark mb-3 border-bottom pb-2">🌐 Links &amp; Resume</h6>
            <div class="d-flex flex-column gap-2 mb-3">
              ${data.linkedin_url ? `<a href="${escapeHtml(data.linkedin_url)}" target="_blank" class="btn btn-sm btn-outline-info text-start fw-bold">🔗 LinkedIn Profile</a>` : '<span class="text-muted small">No LinkedIn link</span>'}
              ${data.github_url ? `<a href="${escapeHtml(data.github_url)}" target="_blank" class="btn btn-sm btn-outline-dark text-start fw-bold">💻 GitHub Profile</a>` : '<span class="text-muted small">No GitHub link</span>'}
              ${data.portfolio_url ? `<a href="${escapeHtml(data.portfolio_url)}" target="_blank" class="btn btn-sm btn-outline-success text-start fw-bold">🌐 Portfolio Site</a>` : '<span class="text-muted small">No Portfolio link</span>'}
            </div>
            ${item.candidate_id ? `
              <a href="${BASE_URL}/resumes/${item.candidate_id}/export?format=pdf&token=${encodeURIComponent(token)}" target="_blank" class="btn btn-success btn-sm w-100 fw-bold">📄 Export Dossier PDF</a>
            ` : ''}
          </div>
        </div>

        <!-- Detailed Parsed Information -->
        <div class="col-md-8">
          <div class="mb-4">
            <h5 class="fw-bold text-dark mb-2">📝 Professional Summary</h5>
            <div class="p-3 bg-light rounded-3 border text-secondary small" style="line-height: 1.6;">
              ${escapeHtml(data.summary || 'No summary extracted from resume.')}
            </div>
          </div>

          <div class="mb-4">
            <h5 class="fw-bold text-dark mb-2">💡 Extracted Skills (${skillsArr.length})</h5>
            <div class="p-3 bg-light rounded-3 border">
              ${skillsBadges || '<span class="text-muted small">No skills detected</span>'}
            </div>
          </div>

          <div class="mb-4">
            <h5 class="fw-bold text-dark mb-2">💼 Work History &amp; Experience</h5>
            <div class="p-3 bg-light rounded-3 border text-secondary small" style="white-space: pre-line;">
              ${escapeHtml(data.work_experience || 'No detailed work experience text.')}
            </div>
          </div>

          <div class="row g-3">
            <div class="col-md-6">
              <h5 class="fw-bold text-dark mb-2">🎓 Education</h5>
              <div class="p-3 bg-light rounded-3 border text-secondary small">
                ${escapeHtml((data.education || '').split(/\b(technical environment|technical skills|key skills)\b/i)[0].replace(/[\n\r,-]+$/, '').trim() || 'No education records.')}
              </div>
            </div>
            <div class="col-md-6">
              <h5 class="fw-bold text-dark mb-2">📜 Certifications</h5>
              <div class="p-3 bg-light rounded-3 border text-secondary small">
                ${data.certifications ? escapeHtml(Array.isArray(data.certifications) ? data.certifications.join(', ') : data.certifications) : 'None listed.'}
              </div>
            </div>
          </div>
        </div>
      </div>
    `;

    const modalInst = new bootstrap.Modal(document.getElementById("candidateDetailModal"));
    
    const modalDeleteBtn = document.getElementById("modal-delete-cand-btn");
    if (modalDeleteBtn) {
      if (item.candidate_id) {
        modalDeleteBtn.classList.remove("d-none");
        modalDeleteBtn.onclick = () => {
          deleteCandidate(item.candidate_id, (item.extracted_data && item.extracted_data.name) || item.filename, modalInst);
        };
      } else {
        modalDeleteBtn.classList.add("d-none");
      }
    }

    modalInst.show();
  }

  async function deleteCandidate(candidateId, candidateName, modalInst = null) {
    if (!confirm(`Are you sure you want to delete candidate "${candidateName}"? This action cannot be undone.`)) {
      return;
    }

    try {
      const token = getToken();
      const response = await fetch(`${BASE_URL}/resumes/${candidateId}`, {
        method: "DELETE",
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });

      if (!response.ok) {
        const errText = await response.text();
        let errMsg = `Server returned status ${response.status}`;
        try {
          const errJson = JSON.parse(errText);
          errMsg = errJson.message || errJson.detail || errMsg;
        } catch (_) {}
        alert(`Failed to delete candidate: ${errMsg}`);
        return;
      }

      const res = await response.json();
      if (res.success) {
        if (modalInst) {
          modalInst.hide();
        }
        currentResultsStore = currentResultsStore.filter(item => item.candidate_id !== candidateId);
        renderResults(currentResultsStore);
        if (typeof window.refreshRecruiterDashboardUploadedResumes === "function") {
          window.refreshRecruiterDashboardUploadedResumes();
        }
      } else {
        alert(res.message || "Failed to delete candidate.");
      }
    } catch (err) {
      console.error("Delete candidate error:", err);
      alert(`Error deleting candidate: ${err.message || err}`);
    }
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

  function formatCompactEducation(rawEdu) {
    if (!rawEdu) return "—";
    let clean = String(rawEdu)
      .replace(/[≡\n\r]/g, " ")
      .replace(/\s+/g, " ")
      .trim();

    clean = clean.replace(/^(Qualification|Degree|Education)\s*:\s*/i, "");

    const degreeMatch = clean.match(/\b(M\.?S\.?|B\.?E\.?|B\.?Tech|M\.?Tech|B\.?Sc|M\.?Sc|Ph\.?D|M\.?B\.?A|Bachelor|Master|Diploma)[^,\.\(\)]*(?:\([^\)]*\))?/i);
    if (degreeMatch) {
      let deg = degreeMatch[0].trim();
      if (deg.length > 45) deg = deg.substring(0, 42) + "...";
      return deg;
    }

    if (clean.length > 50) {
      clean = clean.substring(0, 47) + "...";
    }
    return clean;
  }

  function formatCompactLocation(rawLoc) {
    if (!rawLoc) return "Location not listed";
    let clean = String(rawLoc).replace(/[≡\n\r]/g, " ").replace(/\s+/g, " ").trim();
    if (clean.length > 30) {
      clean = clean.substring(0, 27) + "...";
    }
    return clean;
  }

  function escapeHtml(str) {
    if (!str) return "";
    return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  window.showBulkAtsModal = showAtsModal;
  window.showBulkCandidateDetailsModal = showCandidateDetailsModal;
  window.deleteBulkCandidate = deleteCandidate;
})();
