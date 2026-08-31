/**
 * upload-resume.js — drag/click-to-upload, calls resumeAPI.upload(),
 * and renders the parsed profile once the backend returns it.
 * Also loads any existing profile on page load (GET /resumes/me).
 */
(function () {
  const fileInput = document.getElementById("resume-file-input");
  const dropzone = document.getElementById("dropzone");
  const dropzoneTitle = document.getElementById("dropzone-title");
  const uploadBtn = document.getElementById("upload-btn");
  const uploadBtnText = document.getElementById("upload-btn-text");
  const uploadSpinner = document.getElementById("upload-spinner");
  const alertBox = document.getElementById("upload-alert");

  let selectedFile = null;

  function showAlert(message, variant) {
    alertBox.textContent = message;
    alertBox.className = `alert alert-${variant} py-2`;
  }

  function hideAlert() {
    alertBox.className = "alert d-none";
  }

  function onFileChosen(file) {
    if (!file) return;
    const isAllowed = /\.(pdf|docx)$/i.test(file.name);
    if (!isAllowed) {
      showAlert("Only PDF or DOCX files are accepted.", "danger");
      selectedFile = null;
      uploadBtn.disabled = true;
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      showAlert("File is too large. Maximum size is 10MB.", "danger");
      selectedFile = null;
      uploadBtn.disabled = true;
      return;
    }
    selectedFile = file;
    hideAlert();
    dropzoneTitle.textContent = file.name;
    uploadBtn.disabled = false;
  }

  fileInput.addEventListener("change", (e) => onFileChosen(e.target.files[0]));

  ["dragover", "dragenter"].forEach((evt) =>
    dropzone.addEventListener(evt, (e) => {
      e.preventDefault();
      dropzone.classList.add("border-primary");
    })
  );
  ["dragleave", "drop"].forEach((evt) =>
    dropzone.addEventListener(evt, (e) => {
      e.preventDefault();
      dropzone.classList.remove("border-primary");
    })
  );
  dropzone.addEventListener("drop", (e) => {
    const file = e.dataTransfer.files[0];
    onFileChosen(file);
  });

  function setLoading(isLoading) {
    uploadBtn.disabled = isLoading || !selectedFile;
    uploadSpinner.classList.toggle("d-none", !isLoading);
    uploadBtnText.textContent = isLoading ? "Analyzing..." : "Upload & Analyze";
  }

  uploadBtn.addEventListener("click", async () => {
    if (!selectedFile) return;
    hideAlert();
    setLoading(true);
    try {
      const res = await resumeAPI.upload(selectedFile);
      renderProfile(res.data);
      showAlert("Resume parsed successfully.", "success");
    } catch (err) {
      showAlert(err.message, "danger");
    } finally {
      setLoading(false);
    }
  });

  let availableDomains = [];

  async function loadDomains() {
    try {
      const res = await resumeAPI.getDomains();
      availableDomains = res.data || [];
      const selectEl = document.getElementById("domain-select");
      if (selectEl) {
        selectEl.innerHTML = availableDomains
          .map((d) => `<option value="${d.key}">${d.title}</option>`)
          .join("");
      }
    } catch {
      // Domain list fallback
    }
  }

  async function runDomainAnalysis(specifiedTargetDomain = null) {
    const selectEl = document.getElementById("domain-select");
    const targetDomain = specifiedTargetDomain || selectEl?.value || "auto";

    try {
      const res = await resumeAPI.analyzeDomain(targetDomain);
      const data = res.data;

      // 1. Render Dynamically Identified Primary Role Card
      const explicitCard = document.getElementById("explicit-role-card");
      if (explicitCard && data.explicit_role) {
        explicitCard.classList.remove("d-none");
        const expRole = data.explicit_role;
        const roleName = expRole.role_title || "Professional Role";
        document.getElementById("explicit-role-title").textContent = `Primary Role: ${roleName} — ${expRole.ats_score}% ATS Score`;
        document.getElementById("explicit-role-score").textContent = `${expRole.ats_score}%`;

        const expStatus = document.getElementById("explicit-role-status");
        if (expRole.ats_score >= 75) {
          expStatus.className = "badge bg-success text-white px-3 py-1";
          expStatus.textContent = "Strong Alignment";
        } else if (expRole.ats_score >= 50) {
          expStatus.className = "badge bg-warning text-dark px-3 py-1";
          expStatus.textContent = "Moderate Alignment";
        } else {
          expStatus.className = "badge bg-danger text-white px-3 py-1";
          expStatus.textContent = "ATS Score Gap";
        }

        const expExplanation = document.getElementById("explicit-role-explanation");
        if (expRole.is_explicitly_mentioned && expRole.raw_text_detected) {
          expExplanation.textContent = `Primary job role dynamically identified from your resume as "${expRole.raw_text_detected}".`;
        } else {
          expExplanation.textContent = `Primary job role inferred from your resume's skill set, experience, and education.`;
        }

        const expSkillsContainer = document.getElementById("explicit-role-skills");
        if (expSkillsContainer && expRole.matched_skills && expRole.matched_skills.length) {
          expSkillsContainer.innerHTML = expRole.matched_skills
            .map((s) => `<span class="badge text-bg-primary border border-primary-subtle">${s}</span>`)
            .join(" ");
        } else if (expSkillsContainer) {
          expSkillsContainer.innerHTML = '<span class="text-muted small">No specific core skills matched yet.</span>';
        }
      }

      // Render Top 3 Job Matches Cards Grid
      const otherRolesCard = document.getElementById("other-roles-card");
      const otherGrid = document.getElementById("other-roles-grid");
      const top3Roles = data.top_3_roles && data.top_3_roles.length ? data.top_3_roles : (data.other_role_matches || []).slice(0, 3);

      if (otherRolesCard && otherGrid && top3Roles) {
        otherRolesCard.classList.remove("d-none");

        if (selectEl && data.target_domain) {
          selectEl.value = data.target_domain;
        }

        otherGrid.innerHTML = top3Roles
          .map((item) => {
            const isTarget = item.key === data.target_domain;
            const isPrimary = item.is_primary || (data.explicit_role && (item.key === data.explicit_role.domain_key || item.title === data.explicit_role.role_title));

            let cardStyle = isTarget ? "border-primary border-2 bg-primary-subtle shadow-sm" : "border bg-white shadow-sm";
            let scoreBadgeClass = item.match_score >= 75 ? "bg-success text-white" : item.match_score >= 50 ? "bg-warning text-dark" : "bg-secondary text-white";
            let roleTagBadge = isPrimary
              ? '<span class="badge bg-primary text-white mb-1">#1 Primary Role</span>'
              : `<span class="badge bg-secondary text-white mb-1">${item.badge_label || "Best Alternative"}</span>`;

            return `
              <div class="col-md-4">
                <div class="card h-100 p-3 ${cardStyle} role-selector-card" style="transition: transform 0.15s ease;" data-role-key="${item.key}">
                  <div class="d-flex justify-content-between align-items-start mb-2">
                    <div>
                      ${roleTagBadge}
                      <h5 class="fw-bold mb-0 text-dark fs-6">${item.title}</h5>
                    </div>
                    <span class="badge ${scoreBadgeClass} fs-6 px-2 py-1">${item.match_score}% Match</span>
                  </div>
                  <p class="text-muted small mb-2 flex-grow-1" style="font-size: 0.82rem; line-height: 1.4;">
                    ${item.explanation || item.description || "Matching role based on skills & experience."}
                  </p>
                  <div class="pt-2 border-top mt-auto d-flex justify-content-between align-items-center flex-wrap gap-2">
                    <span class="badge text-bg-light border text-secondary" style="font-size: 0.75rem;">${item.matched_skills_count} Matched Skills</span>
                    <button class="btn btn-sm ${isTarget ? 'btn-primary' : 'btn-outline-primary'} fw-semibold px-2 py-1 check-ats-btn" style="font-size: 0.78rem;" data-role-key="${item.key}">
                      ${isTarget ? 'Active Target Role ✓' : 'Check ATS Score &rarr;'}
                    </button>
                  </div>
                </div>
              </div>
            `;
          })
          .join("");

        otherGrid.querySelectorAll(".role-selector-card").forEach((card) => {
          card.addEventListener("click", (evt) => {
            const roleKey = card.getAttribute("data-role-key");
            if (roleKey) {
              runDomainAnalysis(roleKey);
              document.getElementById("domain-card")?.scrollIntoView({ behavior: "smooth", block: "start" });
            }
          });
        });
      }


      // 3. Render Target Improvement Plan Card
      const domainCard = document.getElementById("domain-card");
      if (domainCard) {
        domainCard.classList.remove("d-none");

        document.getElementById("target-role-name").textContent = data.domain_title;

        const scoreEl = document.getElementById("domain-score-display");
        scoreEl.textContent = `${data.domain_score}%`;

        const statusBadge = document.getElementById("domain-score-status");
        if (data.domain_score >= 75) {
          scoreEl.className = "display-6 fw-bold text-success";
          statusBadge.className = "badge bg-success-subtle text-success border border-success-subtle mt-1";
          statusBadge.textContent = "Strong Target Match";
        } else if (data.domain_score >= 50) {
          scoreEl.className = "display-6 fw-bold text-warning";
          statusBadge.className = "badge bg-warning-subtle text-warning border border-warning-subtle mt-1";
          statusBadge.textContent = "Moderate Alignment";
        } else {
          scoreEl.className = "display-6 fw-bold text-danger";
          statusBadge.className = "badge bg-danger-subtle text-danger border border-danger-subtle mt-1";
          statusBadge.textContent = "Strict Domain Gap";
        }

        document.getElementById("matched-skills-count").textContent = data.matched_required_skills.length;
        document.getElementById("missing-skills-count").textContent = data.missing_required_skills.length;

        const matchedContainer = document.getElementById("domain-matched-skills");
        if (data.matched_required_skills && data.matched_required_skills.length) {
          matchedContainer.innerHTML = data.matched_required_skills
            .map((s) => `<span class="badge text-bg-success-subtle text-success border border-success-subtle">${s}</span>`)
            .join(" ");
        } else {
          matchedContainer.innerHTML = '<span class="text-muted small">No required skills matched yet for this target role.</span>';
        }

        const missingContainer = document.getElementById("domain-missing-skills");
        if (data.missing_required_skills && data.missing_required_skills.length) {
          missingContainer.innerHTML = data.missing_required_skills
            .map((s) => `<span class="badge text-bg-danger-subtle text-danger border border-danger-subtle">${s}</span>`)
            .join(" ");
        } else {
          missingContainer.innerHTML = '<span class="text-success small fw-medium">All core domain required skills present!</span>';
        }

        const catRecs = data.categorized_recommendations || {};

        // Tab 1: Skills & Keywords
        const recsSkillsEl = document.getElementById("recs-skills-list");
        const skillsList = catRecs.skills_and_keywords || data.recommendations || [];
        if (recsSkillsEl && skillsList.length) {
          recsSkillsEl.innerHTML = skillsList.map((rec) => `<li class="mb-1">${rec}</li>`).join("");
        } else if (recsSkillsEl) {
          recsSkillsEl.innerHTML = '<li>Your skills match the requirements for this role.</li>';
        }

        // Tab 2: Experience & Impact
        const recsExpEl = document.getElementById("recs-experience-list");
        const expList = catRecs.experience_improvements || [];
        if (recsExpEl && expList.length) {
          recsExpEl.innerHTML = expList.map((rec) => `<li class="mb-1">${rec}</li>`).join("");
        } else if (recsExpEl) {
          recsExpEl.innerHTML = '<li>Work experience descriptions look well structured for this target role.</li>';
        }

        // Tab 3: Certifications
        const recsCertsEl = document.getElementById("recs-certs-list");
        const certsList = catRecs.certifications || [];
        if (recsCertsEl && certsList.length) {
          recsCertsEl.innerHTML = certsList.map((cert) => `<li class="mb-1">${cert}</li>`).join("");
        } else if (recsCertsEl) {
          recsCertsEl.innerHTML = '<li>No specific additional certifications required for this level.</li>';
        }

        // Tab 4: ATS Formatting & Structure
        const recsFormatEl = document.getElementById("recs-formatting-list");
        const formatList = catRecs.ats_formatting || [];
        if (recsFormatEl && formatList.length) {
          recsFormatEl.innerHTML = formatList.map((tip) => `<li class="mb-1">${tip}</li>`).join("");
        } else if (recsFormatEl) {
          recsFormatEl.innerHTML = '<li>Your resume follows standard ATS structure.</li>';
        }
      }
    } catch (err) {
      // Domain analysis error handling
    }
  }

  document.getElementById("domain-select")?.addEventListener("change", (e) => {
    runDomainAnalysis(e.target.value);
  });

  function renderProfile(profile) {
    currentProfileData = profile;
    document.getElementById("profile-card").classList.remove("d-none");
    document.getElementById("profile-score-badge").textContent = profile.profile_score != null ? `General ATS Score: ${profile.profile_score}%` : "General ATS Score: —";
    document.getElementById("profile-phone").textContent = profile.phone || "—";
    document.getElementById("profile-location").textContent = profile.location || "—";
    document.getElementById("profile-experience").textContent = profile.experience_years
      ? `${profile.experience_years} years`
      : "—";
    document.getElementById("profile-summary").textContent = profile.summary || "—";
    if (document.getElementById("profile-address")) {
      document.getElementById("profile-address").textContent = profile.address || "—";
    }
    if (document.getElementById("profile-work-experience")) {
      document.getElementById("profile-work-experience").textContent = profile.work_experience || "—";
    }
    document.getElementById("profile-education").textContent = profile.education || "—";
    document.getElementById("profile-ai-summary").textContent =
      profile.ai_summary || "Not generated yet.";
    document.getElementById("profile-ai-summary").classList.toggle("fst-italic", !profile.ai_summary);

    const skillsEl = document.getElementById("profile-skills");
    skillsEl.innerHTML = "";
    if (profile.skills && profile.skills.length) {
      profile.skills.forEach((skill) => {
        const badge = document.createElement("span");
        badge.className = "badge text-bg-light border";
        badge.textContent = skill;
        skillsEl.appendChild(badge);
      });
    } else {
      skillsEl.innerHTML = '<span class="text-muted-custom">No skills detected yet.</span>';
    }

    // Automatically trigger strict domain evaluation & explicit role identification
    runDomainAnalysis();
  }

  // Edit Profile modal wire-up
  const editProfileBtn = document.getElementById("edit-profile-btn");
  const saveProfileBtn = document.getElementById("save-profile-btn");
  const saveProfileSpinner = document.getElementById("save-profile-spinner");
  const saveProfileText = document.getElementById("save-profile-text");

  editProfileBtn?.addEventListener("click", () => {
    if (!currentProfileData) return;
    document.getElementById("edit-phone").value = currentProfileData.phone || "";
    document.getElementById("edit-location").value = currentProfileData.location || "";
    document.getElementById("edit-experience").value = currentProfileData.experience_years != null ? currentProfileData.experience_years : "";
    document.getElementById("edit-skills").value = (currentProfileData.skills || []).join(", ");
    document.getElementById("edit-summary").value = currentProfileData.summary || "";
    document.getElementById("edit-address").value = currentProfileData.address || "";
    document.getElementById("edit-work-experience").value = currentProfileData.work_experience || "";
    document.getElementById("edit-education").value = currentProfileData.education || "";

    const editModal = new bootstrap.Modal(document.getElementById("edit-profile-modal"));
    editModal.show();
  });

  saveProfileBtn?.addEventListener("click", async () => {
    saveProfileBtn.disabled = true;
    saveProfileSpinner.classList.remove("d-none");
    saveProfileText.textContent = "Saving...";

    const rawSkills = document.getElementById("edit-skills").value;
    const skillsList = rawSkills.split(",").map((s) => s.trim()).filter(Boolean);
    const expVal = document.getElementById("edit-experience").value;

    const payload = {
      phone: document.getElementById("edit-phone").value || null,
      location: document.getElementById("edit-location").value || null,
      address: document.getElementById("edit-address").value || null,
      summary: document.getElementById("edit-summary").value || null,
      experience_years: expVal !== "" ? parseFloat(expVal) : null,
      education: document.getElementById("edit-education").value || null,
      work_experience: document.getElementById("edit-work-experience").value || null,
      skills: skillsList,
    };

    try {
      const res = await resumeAPI.update(payload);
      renderProfile(res.data);
      showAlert("Profile updated successfully.", "success");
      const modalEl = document.getElementById("edit-profile-modal");
      const modalInst = bootstrap.Modal.getInstance(modalEl);
      if (modalInst) modalInst.hide();
    } catch (err) {
      showAlert(err.message, "danger");
    } finally {
      saveProfileBtn.disabled = false;
      saveProfileSpinner.classList.add("d-none");
      saveProfileText.textContent = "Save Changes";
    }
  });

  // Delete Profile Wire-up
  const deleteProfileBtn = document.getElementById("delete-profile-btn");
  deleteProfileBtn?.addEventListener("click", async () => {
    if (!confirm("Are you sure you want to delete your uploaded resume and parsed profile? This action cannot be undone.")) {
      return;
    }
    try {
      await resumeAPI.delete();
      currentProfileData = null;
      document.getElementById("profile-card").classList.add("d-none");
      document.getElementById("domain-card").classList.add("d-none");
      dropzoneTitle.textContent = "Click to choose a file, or drag it here";
      fileInput.value = "";
      selectedFile = null;
      uploadBtn.disabled = true;
      showAlert("Resume deleted successfully.", "success");
    } catch (err) {
      showAlert(err.message, "danger");
    }
  });

  const generateSummaryBtn = document.getElementById("generate-summary-btn");
  const generateSummaryText = document.getElementById("generate-summary-text");
  const generateSummarySpinner = document.getElementById("generate-summary-spinner");

  generateSummaryBtn.addEventListener("click", async () => {
    generateSummaryBtn.disabled = true;
    generateSummarySpinner.classList.remove("d-none");
    generateSummaryText.textContent = "Generating...";
    try {
      const res = await resumeAPI.generateSummary();
      renderProfile(res.data);
    } catch (err) {
      showAlert(err.message, "danger");
    } finally {
      generateSummaryBtn.disabled = false;
      generateSummarySpinner.classList.add("d-none");
      generateSummaryText.textContent = "Regenerate with AI";
    }
  });

  const btnImproveUpload = document.getElementById("btn-improve-resume-upload");
  if (btnImproveUpload) {
    btnImproveUpload.addEventListener("click", async () => {
      const modalEl = document.getElementById("aiResumeImprovementModal");
      const modalBody = document.getElementById("resume-improve-modal-body");
      let modalInst = null;
      if (window.bootstrap && modalEl) {
        modalInst = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
      }

      modalBody.innerHTML = `
        <div class="text-center py-5 text-muted">
          <div class="spinner-border text-primary mb-3" style="width: 3rem; height: 3rem;"></div>
          <h5 class="fw-bold text-dark">Analyzing Resume against Target Job...</h5>
          <p class="small text-secondary mb-0">Detecting weak sentences, missing keywords, achievement metric opportunities, and grammar fixes.</p>
        </div>
      `;
      if (modalInst) modalInst.show();

      try {
        const meRes = await API.get("/resumes/me");
        if (!meRes || !meRes.data) throw new Error("Please upload a resume first.");
        const candId = meRes.data.id;
        const jobsRes = await jobsAPI.list();
        const jobs = jobsRes.data;
        if (!jobs || !jobs.length) throw new Error("No open jobs available for comparison.");
        const firstJob = jobs[0];

        const res = await resumeImprovementAPI.improve(candId, firstJob.id);
        renderResumeImprovementModalContent(res.data, candId);
      } catch (err) {
        modalBody.innerHTML = `<div class="alert alert-danger p-4"><strong>Analysis Error:</strong> ${err.message}</div>`;
      }
    });
  }

  function renderResumeImprovementModalContent(data, candidateId) {
    const modalBody = document.getElementById("resume-improve-modal-body");
    const sc = data.scores || {};
    const overallQ = Math.round(data.overall_resume_quality || 80);

    const priorityHtml = (data.priority_improvements || [])
      .map((p, idx) => `<li class="list-group-item"><strong>${idx + 1}.</strong> ${p}</li>`)
      .join("") || '<li class="list-group-item text-muted">No high priority fixes needed.</li>';

    const weakSentencesHtml = (data.weak_sentences || []).map((w) => `
      <div class="card p-3 mb-3 border shadow-sm" style="border-radius: 10px;">
        <div class="text-danger small fw-bold mb-1">❌ Current:</div>
        <div class="p-2 bg-light rounded text-dark small mb-2">${w.original}</div>
        <div class="text-success small fw-bold mb-1">✨ Recommended:</div>
        <div class="p-2 bg-success-subtle border border-success border-opacity-25 rounded text-dark small fw-medium mb-2">${w.recommended}</div>
        <div class="small text-secondary mb-3">
          <strong>Why this is better:</strong>
          <ul class="mb-0 ps-3">
            ${(w.reason || []).map(r => `<li>✓ ${r}</li>`).join("")}
          </ul>
        </div>
        <div>
          <button class="btn btn-sm btn-success fw-semibold accept-imp-btn me-2" data-cand-id="${candidateId}" data-orig="${encodeURIComponent(w.original)}" data-imp="${encodeURIComponent(w.recommended)}">
            ✓ Accept Improvement
          </button>
        </div>
      </div>
    `).join("") || '<div class="alert alert-success py-2 small mb-0">✓ No weak or passive sentences detected!</div>';

    const kwHtml = (data.missing_keywords || []).map(kw => `
      <span class="badge bg-warning-subtle text-dark border border-warning px-2 py-1 me-1 mb-1">⚠ ${kw}</span>
    `).join("") || '<span class="text-success small fw-semibold">✓ All target job keywords matched!</span>';

    const skillsHtml = (data.missing_skills || []).map(sk => `
      <span class="badge bg-danger-subtle text-danger border border-danger px-2 py-1 me-1 mb-1">⚠ ${sk}</span>
    `).join("") || '<span class="text-success small fw-semibold">✓ All required skills matched!</span>';

    const achievementsHtml = (data.achievement_suggestions || []).map(a => `
      <div class="p-3 bg-light rounded border mb-2 small">
        <div class="text-dark fw-bold mb-1">Original: "${a.original}"</div>
        <div class="text-primary mb-1">💡 <strong>Suggestion:</strong> ${a.suggestion}</div>
        <div class="text-muted text-xs">⚠️ Add actual metrics if verifiable (e.g. replace [X%] with your real accomplishment).</div>
      </div>
    `).join("") || '<div class="text-muted small">Your resume contains strong quantifiable metrics.</div>';

    const grammarHtml = (data.grammar_corrections || []).map(g => `
      <div class="p-2 bg-light rounded border mb-2 small">
        <span class="text-danger text-decoration-line-through me-2">${g.original}</span>
        &rarr;
        <span class="text-success fw-bold ms-2">${g.corrected}</span>
      </div>
    `).join("") || '<div class="text-success small fw-semibold">✓ No grammar or tense errors detected.</div>';

    const formattingHtml = (data.formatting_suggestions || []).map(f => `
      <div class="p-2 bg-light rounded border mb-1 small">ℹ️ ${f}</div>
    `).join("") || '<div class="text-success small">✓ Good formatting and structure.</div>';

    modalBody.innerHTML = `
      <!-- Overall Quality Gauge -->
      <div class="card p-4 mb-4 border-0 shadow-sm" style="background: linear-gradient(135deg, #f4f7ff 0%, #ffffff 100%); border-radius: 12px;">
        <div class="d-flex justify-content-between align-items-center flex-wrap gap-3">
          <div>
            <span class="badge bg-primary text-white mb-1">AI Resume Coach Analysis</span>
            <h4 class="fw-bold text-dark mb-0">Overall Resume Quality Score</h4>
            <p class="text-muted small mb-0">Based on target job description, action verbs, keyword density, and metrics.</p>
          </div>
          <div class="text-end">
            <div class="display-5 fw-bold text-primary">${overallQ}%</div>
            <span class="badge ${overallQ >= 80 ? 'bg-success' : 'bg-primary'} px-3 py-1">Job-Specific Fit</span>
          </div>
        </div>
      </div>

      <!-- 6 Quality Sub-Scores Progress Bars -->
      <div class="card p-4 mb-4 border-0 shadow-sm" style="border-radius: 12px;">
        <h6 class="fw-bold mb-3">📊 Resume Quality Sub-Scores Breakdown</h6>
        <div class="row g-3">
          <div class="col-md-4">
            <div class="d-flex justify-content-between small fw-semibold mb-1"><span>Writing Quality</span><span>${Math.round(sc.writing_quality || 85)}%</span></div>
            <div class="progress" style="height: 8px;"><div class="progress-bar bg-primary" style="width: ${sc.writing_quality || 85}%;"></div></div>
          </div>
          <div class="col-md-4">
            <div class="d-flex justify-content-between small fw-semibold mb-1"><span>Keyword Optimization</span><span>${Math.round(sc.keyword_optimization || 70)}%</span></div>
            <div class="progress" style="height: 8px;"><div class="progress-bar bg-info" style="width: ${sc.keyword_optimization || 70}%;"></div></div>
          </div>
          <div class="col-md-4">
            <div class="d-flex justify-content-between small fw-semibold mb-1"><span>Achievement Impact</span><span>${Math.round(sc.achievement_impact || 55)}%</span></div>
            <div class="progress" style="height: 8px;"><div class="progress-bar bg-warning" style="width: ${sc.achievement_impact || 55}%;"></div></div>
          </div>
          <div class="col-md-4">
            <div class="d-flex justify-content-between small fw-semibold mb-1"><span>Grammar &amp; Tense</span><span>${Math.round(sc.grammar || 95)}%</span></div>
            <div class="progress" style="height: 8px;"><div class="progress-bar bg-success" style="width: ${sc.grammar || 95}%;"></div></div>
          </div>
          <div class="col-md-4">
            <div class="d-flex justify-content-between small fw-semibold mb-1"><span>Formatting &amp; Structure</span><span>${Math.round(sc.formatting || 90)}%</span></div>
            <div class="progress" style="height: 8px;"><div class="progress-bar bg-secondary" style="width: ${sc.formatting || 90}%;"></div></div>
          </div>
          <div class="col-md-4">
            <div class="d-flex justify-content-between small fw-semibold mb-1"><span>Job Relevance</span><span>${Math.round(sc.job_relevance || 88)}%</span></div>
            <div class="progress" style="height: 8px;"><div class="progress-bar bg-dark" style="width: ${sc.job_relevance || 88}%;"></div></div>
          </div>
        </div>
      </div>

      <!-- Priority Improvements -->
      <div class="card p-4 mb-4 border-0 shadow-sm" style="border-radius: 12px;">
        <h6 class="fw-bold mb-2 text-primary">🚀 Priority Improvements for Target Job</h6>
        <ul class="list-group list-group-flush small">
          ${priorityHtml}
        </ul>
      </div>

      <!-- Weak Sentence Rewriting (Before vs After) -->
      <div class="card p-4 mb-4 border-0 shadow-sm" style="border-radius: 12px;">
        <h6 class="fw-bold mb-2">✏️ Weak Sentence Rewriting (Before &amp; After)</h6>
        <p class="text-muted small mb-3">Action-oriented sentence recommendations with strong domain keywords.</p>
        ${weakSentencesHtml}
      </div>

      <!-- Missing Keywords & Missing Skills Guidance -->
      <div class="row g-3 mb-4">
        <div class="col-md-6">
          <div class="card p-3 h-100 border-0 shadow-sm" style="border-radius: 12px;">
            <h6 class="fw-bold mb-2">🔑 Missing Target Job Keywords</h6>
            <div class="mb-2">${kwHtml}</div>
            <p class="text-muted text-xs mb-0">Add these keywords to your experience or summary only if truthful.</p>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card p-3 h-100 border-0 shadow-sm" style="border-radius: 12px;">
            <h6 class="fw-bold mb-2">💡 Recommended Skill Learning Areas</h6>
            <div class="mb-2">${skillsHtml}</div>
            <p class="text-muted text-xs mb-0">Required by job. Add to resume only if you have genuine project or course experience.</p>
          </div>
        </div>
      </div>

      <!-- Achievement Metrics & Grammar/Formatting -->
      <div class="row g-3 mb-3">
        <div class="col-md-6">
          <div class="card p-3 h-100 border-0 shadow-sm" style="border-radius: 12px;">
            <h6 class="fw-bold mb-2">📈 Measurable Achievement Suggestions</h6>
            ${achievementsHtml}
          </div>
        </div>
        <div class="col-md-6">
          <div class="card p-3 h-100 border-0 shadow-sm" style="border-radius: 12px;">
            <h6 class="fw-bold mb-2">📝 Grammar &amp; Formatting Tips</h6>
            <div class="mb-3">
              <strong class="small text-secondary">Grammar Fixes:</strong>
              ${grammarHtml}
            </div>
            <div>
              <strong class="small text-secondary">Formatting Checklist:</strong>
              ${formattingHtml}
            </div>
          </div>
        </div>
      </div>
    `;

    // Attach Listeners for Accept Improvement buttons
    modalBody.querySelectorAll(".accept-imp-btn").forEach(btn => {
      btn.addEventListener("click", async () => {
        const orig = decodeURIComponent(btn.dataset.orig);
        const imp = decodeURIComponent(btn.dataset.imp);
        const cid = btn.dataset.candId;

        btn.disabled = true;
        try {
          await resumeImprovementAPI.acceptImprovement(cid, orig, imp, "experience");
          btn.className = "btn btn-sm btn-outline-success disabled fw-bold";
          btn.textContent = "✓ Accepted & Saved!";
        } catch (err) {
          alert(`Could not save improvement: ${err.message}`);
          btn.disabled = false;
        }
      });
    });
  }

  // Load any existing profile so returning candidates see their last upload.
  document.addEventListener("ar:auth-ready", async () => {
    await loadDomains();
    try {
      const res = await resumeAPI.me();
      renderProfile(res.data);
    } catch {
      // No resume uploaded yet — that's fine, leave the profile card hidden.
    }
  });
})();
