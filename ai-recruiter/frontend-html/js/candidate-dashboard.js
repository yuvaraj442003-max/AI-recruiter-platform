/**
 * candidate-dashboard.js — loads GET /analytics/candidate and renders
 * the stat cards, profile-completion donut, applications-by-status
 * chart, latest interview score, and skill badges.
 */
(function () {
  const alertBox = document.getElementById("dashboard-alert");

  function showAlert(message, variant) {
    alertBox.textContent = message;
    alertBox.className = `alert alert-${variant} py-2`;
  }

  function renderProfileCompletionChart(percent) {
    new Chart(document.getElementById("chart-profile-completion"), {
      type: "doughnut",
      data: {
        labels: ["Complete", "Remaining"],
        datasets: [
          {
            data: [percent, Math.max(0, 100 - percent)],
            backgroundColor: ["#2f5fff", "#e9ecf5"],
            borderWidth: 0,
          },
        ],
      },
      options: {
        cutout: "75%",
        plugins: { legend: { display: false }, tooltip: { enabled: false } },
      },
      plugins: [
        {
          id: "centerText",
          afterDraw(chart) {
            const { ctx, chartArea } = chart;
            ctx.save();
            ctx.font = "bold 22px sans-serif";
            ctx.fillStyle = "#1c2333";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            const x = (chartArea.left + chartArea.right) / 2;
            const y = (chartArea.top + chartArea.bottom) / 2;
            ctx.fillText(`${percent}%`, x, y);
            ctx.restore();
          },
        },
      ],
    });
  }

  function renderApplicationsStatusChart(byStatus) {
    const labels = Object.keys(byStatus);
    const values = Object.values(byStatus);
    const hasData = values.some((v) => v > 0);

    const canvasEl = document.getElementById("chart-applications-status");
    const emptyEl = document.getElementById("chart-applications-status-empty");

    if (!hasData) {
      canvasEl.classList.add("d-none");
      emptyEl.classList.remove("d-none");
      return;
    }
    canvasEl.classList.remove("d-none");
    emptyEl.classList.add("d-none");

    new Chart(canvasEl, {
      type: "doughnut",
      data: {
        labels: labels.map((l) => l.replace("_", " ")),
        datasets: [
          {
            data: values,
            backgroundColor: ["#94a3ff", "#6f8bff", "#2f5fff", "#f5a623", "#2fbf71", "#e5484d"],
          },
        ],
      },
      options: { plugins: { legend: { position: "bottom" } } },
    });
  }

  function resumeStatusLabel(uploaded) {
    return uploaded ? "Uploaded ✓" : "Not uploaded";
  }

  function interviewStatusLabel(status) {
    const map = {
      no_resume: "Upload resume",
      not_started: "Not started",
      in_progress: "In progress",
      completed: "Completed",
    };
    return map[status] || status;
  }

  async function load() {
    try {
      const res = await analyticsAPI.candidate();
      const data = res.data;

      document.getElementById("stat-profile-completion").textContent = `${data.profile_completion}%`;
      document.getElementById("stat-resume-status").textContent = resumeStatusLabel(data.resume_uploaded);
      document.getElementById("stat-applications").textContent = data.applications_count;
      document.getElementById("stat-interview-status").textContent = interviewStatusLabel(data.interview_status);

      renderProfileCompletionChart(data.profile_completion);
      renderApplicationsStatusChart(data.applications_by_status);

      if (data.best_suited_role && data.resume_uploaded) {
        const bestCard = document.getElementById("dash-best-role-card");
        if (bestCard) {
          bestCard.classList.remove("d-none");
          const bestTitle = data.best_suited_role.best_role_title || "Software Developer";
          document.getElementById("dash-best-role-title").textContent = bestTitle;
          document.getElementById("dash-best-role-score").textContent = `${data.best_suited_role.best_match_score}%`;
          document.getElementById("dash-best-role-explanation").textContent = data.best_suited_role.explanation || "";

          // Pre-select best suited role in Explorer dropdown
          const roleSelect = document.getElementById("dash-target-role");
          if (roleSelect && !roleSelect.value) {
            roleSelect.value = bestTitle;
          }
        }
      }

      if (data.latest_interview_score != null) {
        document.getElementById("interview-score-display").textContent = `${Math.round(data.latest_interview_score)}%`;
        document.getElementById("interview-score-caption").textContent = "Most recent completed interview";
      }

      const recommendedLine = document.getElementById("recommended-jobs-line");
      if (!data.resume_uploaded) {
        recommendedLine.textContent = "Upload your resume to identify your best suited position and get job recommendations.";
      } else if (data.recommended_jobs_count > 0) {
        recommendedLine.textContent = `Your resume matches ${data.best_suited_role?.best_role_title || "your target role"} best (${data.best_suited_role?.best_match_score}% fit). You're a strong match for ${data.recommended_jobs_count} open position${data.recommended_jobs_count === 1 ? "" : "s"}.`;
      } else {
        recommendedLine.textContent = `Your resume matches ${data.best_suited_role?.best_role_title || "your target role"} best (${data.best_suited_role?.best_match_score}% fit). Check back as new job postings are published.`;
      }

      const skillsList = document.getElementById("skills-list");
      if (data.skills && data.skills.length) {
        skillsList.innerHTML = data.skills
          .map((s) => `<span class="badge bg-primary-subtle text-primary border border-primary-subtle px-3 py-2 fs-6 shadow-sm me-1 mb-1">⚡ ${s}</span>`)
          .join("");
      } else {
        skillsList.innerHTML = '<span class="text-muted-custom small">No skills added yet. Complete your profile details or upload a resume to see skills here.</span>';
      }

      // Load Job Explorer list
      loadExplorerJobs();

      // Load Advanced Job-Specific ATS Analysis
      loadATSAnalysis();
    } catch (err) {
      showAlert(err.message, "danger");
    }
  }

  async function loadATSAnalysis() {
    try {
      const meRes = await API.get("/resumes/me");
      if (!meRes || !meRes.data) return;
      const candId = meRes.data.id;
      const jobsRes = await jobsAPI.list();
      const jobs = jobsRes.data;
      if (!jobs || !jobs.length) return;

      const firstJob = jobs[0];
      const atsRes = await atsAPI.getAnalysis(candId, firstJob.id);
      const ats = atsRes.data;

      // Render Overall ATS Score & Badge
      const score = Math.round(ats.overall_ats_score);
      const overallEl = document.getElementById("ats-overall-score-display");
      if (overallEl) overallEl.textContent = `${score}%`;

      const badgeEl = document.getElementById("ats-score-badge");
      if (badgeEl) {
        if (score >= 90) {
          badgeEl.textContent = "90–100% → Excellent Match";
          badgeEl.className = "badge bg-success fs-6 px-3 py-1";
        } else if (score >= 75) {
          badgeEl.textContent = "75–89% → Strong Match";
          badgeEl.className = "badge bg-primary fs-6 px-3 py-1";
        } else if (score >= 60) {
          badgeEl.textContent = "60–74% → Moderate Match";
          badgeEl.className = "badge bg-warning text-dark fs-6 px-3 py-1";
        } else {
          badgeEl.textContent = "Below 60% → Low Match";
          badgeEl.className = "badge bg-danger fs-6 px-3 py-1";
        }
      }

      // Render 6 breakdown progress bars
      const bd = ats.score_breakdown;
      ["skills", "experience", "keywords", "responsibilities", "education", "location"].forEach((key) => {
        const val = Math.round(bd[key] || 0);
        const valEl = document.getElementById(`ats-val-${key}`);
        const barEl = document.getElementById(`ats-bar-${key}`);
        if (valEl) valEl.textContent = `${val}%`;
        if (barEl) barEl.style.width = `${val}%`;
      });

      // Render Matched Skills
      const matchedEl = document.getElementById("ats-matched-skills-tags");
      if (matchedEl) {
        if (ats.matched_skills && ats.matched_skills.length) {
          matchedEl.innerHTML = ats.matched_skills
            .map((s) => `<span class="badge bg-success-subtle text-success border border-success-subtle px-2 py-1 me-1 mb-1">✓ ${s}</span>`)
            .join("");
        } else {
          matchedEl.innerHTML = '<span class="text-muted small">No direct skill matches found.</span>';
        }
      }

      // Render Missing Skills
      const missingEl = document.getElementById("ats-missing-skills-tags");
      if (missingEl) {
        if (ats.missing_skills && ats.missing_skills.length) {
          missingEl.innerHTML = ats.missing_skills
            .map((s) => `<span class="badge bg-danger-subtle text-danger border border-danger-subtle px-2 py-1 me-1 mb-1">• ${s}</span>`)
            .join("");
        } else {
          missingEl.innerHTML = '<span class="text-success small fw-semibold">✓ Meets all required skills!</span>';
        }
      }

      // Keywords
      const mkwEl = document.getElementById("ats-matched-keywords-text");
      if (mkwEl) mkwEl.textContent = ats.matched_keywords.length ? ats.matched_keywords.join(", ") : "None";

      const miskwEl = document.getElementById("ats-missing-keywords-text");
      if (miskwEl) miskwEl.textContent = ats.missing_keywords.length ? ats.missing_keywords.join(", ") : "None";

      // AI Suggestions
      const suggEl = document.getElementById("ats-ai-suggestions-list");
      if (suggEl) {
        if (ats.suggestions && ats.suggestions.length) {
          suggEl.innerHTML = ats.suggestions
            .map((s) => `<li class="list-group-item">✓ ${s}</li>`)
            .join("");
        } else {
          suggEl.innerHTML = '<li class="list-group-item text-muted">Your resume looks well aligned for this job position.</li>';
        }
      }
    } catch (err) {
      console.warn("ATS Analysis notice:", err.message);
    }
  }

  async function loadExplorerJobs() {
    const listEl = document.getElementById("dash-job-explorer-list");
    if (!listEl) return;

    const targetRole = document.getElementById("dash-target-role")?.value || "";
    const keyword = document.getElementById("dash-search-keyword")?.value.trim() || "";

    const filters = {};
    let queryTitle = keyword;
    if (targetRole) {
      queryTitle = queryTitle ? `${targetRole} ${queryTitle}` : targetRole;
    }
    if (queryTitle) filters.title = queryTitle;

    listEl.innerHTML = '<div class="col-12 text-muted-custom small">Loading jobs...</div>';
    try {
      const res = await jobsAPI.list(filters);
      const jobs = res.data;
      if (!jobs || !jobs.length) {
        listEl.innerHTML = '<div class="col-12 text-muted-custom small py-2">No active job postings found for this role query.</div>';
        return;
      }
      listEl.innerHTML = jobs.slice(0, 6).map((job) => `
        <div class="col-md-6 col-lg-4">
          <div class="card p-3 h-100 border shadow-sm d-flex flex-column" style="border-radius: 10px;">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <h6 class="fw-bold mb-0 text-dark">${job.title}</h6>
              <span class="badge bg-primary-subtle text-primary">${job.employment_type.replace("_", " ")}</span>
            </div>
            <div class="text-muted small mb-2">${job.location || "Remote"}</div>
            <p class="small text-secondary mb-3" style="flex-grow: 1;">${job.description.slice(0, 100)}...</p>
            <a href="jobs.html" class="btn btn-sm btn-outline-primary fw-semibold mt-auto w-100">
              Explore Job &amp; Apply &rarr;
            </a>
          </div>
        </div>
      `).join("");
    } catch (err) {
      listEl.innerHTML = `<div class="col-12 text-danger small">${err.message}</div>`;
    }
  }

  async function loadCandidateProfileData() {
    try {
      const res = await API.get("/resumes/me");
      if (!res || !res.data) return;
      const p = res.data;
      const user = Session.getUser();

      document.getElementById("cand-name-display").textContent = user ? user.name : "Candidate";
      document.getElementById("cand-headline-display").textContent = p.headline || p.current_role || "Software Professional";
      document.getElementById("cand-location-display").textContent = p.location ? `📍 ${p.location}` : "📍 Location Not Specified";
      document.getElementById("cand-experience-display").textContent = `💼 ${p.experience_years || 0} Years Experience`;

      if (p.profile_photo) {
        document.getElementById("cand-profile-photo").src = p.profile_photo;
      } else {
        const name = encodeURIComponent(user ? user.name : "Candidate");
        document.getElementById("cand-profile-photo").src = `https://ui-avatars.com/api/?name=${name}&background=2f5fff&color=fff&size=128`;
      }

      // Social Links
      const btnIn = document.getElementById("cand-btn-linkedin");
      if (p.linkedin_url) {
        btnIn.href = p.linkedin_url;
        btnIn.classList.remove("d-none");
      } else {
        btnIn.classList.add("d-none");
      }

      const btnGit = document.getElementById("cand-btn-github");
      if (p.github_url) {
        btnGit.href = p.github_url;
        btnGit.classList.remove("d-none");
      } else {
        btnGit.classList.add("d-none");
      }

      const btnPort = document.getElementById("cand-btn-portfolio");
      if (p.portfolio_url) {
        btnPort.href = p.portfolio_url;
        btnPort.classList.remove("d-none");
      } else {
        btnPort.classList.add("d-none");
      }

      // Populate Edit Form
      document.getElementById("edit-cand-headline").value = p.headline || "";
      document.getElementById("edit-cand-role").value = p.current_role || "";
      document.getElementById("edit-cand-photo").value = p.profile_photo || "";
      document.getElementById("edit-cand-location").value = p.location || "";
      document.getElementById("edit-cand-summary").value = p.summary || "";
      document.getElementById("edit-cand-phone").value = p.phone || "";
      document.getElementById("edit-cand-exp").value = p.experience_years || "";
      document.getElementById("edit-cand-certifications").value = p.certifications || "";
      document.getElementById("edit-cand-linkedin").value = p.linkedin_url || "";
      document.getElementById("edit-cand-github").value = p.github_url || "";
      document.getElementById("edit-cand-portfolio").value = p.portfolio_url || "";
    } catch (e) {
      // Ignore if resume not uploaded yet
    }
  }

  const candForm = document.getElementById("edit-cand-profile-form");
  if (candForm) {
    candForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const saveBtn = document.getElementById("save-cand-profile-btn");
      saveBtn.disabled = true;
      saveBtn.textContent = "Saving...";

      const expVal = document.getElementById("edit-cand-exp").value;

      const payload = {
        headline: document.getElementById("edit-cand-headline").value.trim() || null,
        current_role: document.getElementById("edit-cand-role").value.trim() || null,
        profile_photo: document.getElementById("edit-cand-photo").value.trim() || null,
        location: document.getElementById("edit-cand-location").value.trim() || null,
        summary: document.getElementById("edit-cand-summary").value.trim() || null,
        phone: document.getElementById("edit-cand-phone").value.trim() || null,
        experience_years: expVal ? Number(expVal) : null,
        certifications: document.getElementById("edit-cand-certifications").value.trim() || null,
        linkedin_url: document.getElementById("edit-cand-linkedin").value.trim() || null,
        github_url: document.getElementById("edit-cand-github").value.trim() || null,
        portfolio_url: document.getElementById("edit-cand-portfolio").value.trim() || null,
      };

      try {
        await API.put("/resumes/me", payload);
        alert("Candidate profile updated successfully!");
        const modalEl = document.getElementById("editCandProfileModal");
        if (window.bootstrap && modalEl) {
          const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
          modal.hide();
        }
        loadCandidateProfileData();
      } catch (err) {
        alert(err.message);
      } finally {
        saveBtn.disabled = false;
        saveBtn.textContent = "Save Profile";
      }
    });
  }

  const dashSearchBtn = document.getElementById("dash-search-btn");
  if (dashSearchBtn) {
    dashSearchBtn.addEventListener("click", loadExplorerJobs);
  }

  const dashTargetRoleSelect = document.getElementById("dash-target-role");
  if (dashTargetRoleSelect) {
    dashTargetRoleSelect.addEventListener("change", loadExplorerJobs);
  }

  const btnImprove = document.getElementById("btn-improve-resume");
  if (btnImprove) {
    btnImprove.addEventListener("click", triggerResumeImprovement);
  }

  async function triggerResumeImprovement() {
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
  }

  function renderResumeImprovementModalContent(data, candidateId) {
    const modalBody = document.getElementById("resume-improve-modal-body");
    const sc = data.scores || {};

    const overallQ = Math.round(data.overall_resume_quality || 80);

    const priorityHtml = (data.priority_improvements || [])
      .map((p, idx) => `<li class="list-group-item"><strong>${idx + 1}.</strong> ${p}</li>`)
      .join("") || '<li class="list-group-item text-muted">No high priority fixes needed.</li>';

    const weakSentencesHtml = (data.weak_sentences || []).map((w, idx) => `
      <div class="card p-3 mb-3 border shadow-sm style="border-radius: 10px;">
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

  // Load immediately on script execution
  loadExplorerJobs();

  document.addEventListener("ar:auth-ready", () => {
    load();
    loadCandidateProfileData();
    loadExplorerJobs();
  });
})();




