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

      const elComp = document.getElementById("stat-profile-completion");
      if (elComp) elComp.textContent = `${data.profile_completion}%`;
      
      const elStatus = document.getElementById("stat-resume-status");
      if (elStatus) elStatus.textContent = resumeStatusLabel(data.resume_uploaded);
      
      const elApps = document.getElementById("stat-applications-count") || document.getElementById("stat-applications");
      if (elApps) elApps.textContent = data.applications_count;
      
      const elInt = document.getElementById("stat-interviews-count") || document.getElementById("stat-interview-status");
      if (elInt) elInt.textContent = interviewStatusLabel ? interviewStatusLabel(data.interview_status) : data.applications_count;

      renderProfileCompletionChart(data.profile_completion);
      renderApplicationsStatusChart(data.applications_by_status);

      if (data.best_suited_role && data.resume_uploaded) {
        const bestCard = document.getElementById("dash-best-role-card");
        if (bestCard) {
          bestCard.classList.remove("d-none");
          const bestTitle = data.best_suited_role.best_role_title || "Software Developer";
          const elTitle = document.getElementById("dash-best-role-title");
          if (elTitle) elTitle.textContent = bestTitle;
          const elScore = document.getElementById("dash-best-role-score");
          if (elScore) elScore.textContent = `${data.best_suited_role.best_match_score}%`;
          const elExp = document.getElementById("dash-best-role-explanation");
          if (elExp) elExp.textContent = data.best_suited_role.explanation || "";

          // Pre-select best suited role in Explorer dropdown
          const roleSelect = document.getElementById("dash-target-role");
          if (roleSelect && !roleSelect.value) {
            roleSelect.value = bestTitle;
          }
        }
      }

      if (data.latest_interview_score != null) {
        const elDisp = document.getElementById("interview-score-display");
        if (elDisp) elDisp.textContent = `${Math.round(data.latest_interview_score)}%`;
        const elCapt = document.getElementById("interview-score-caption");
        if (elCapt) elCapt.textContent = "Most recent completed interview";
      }

      const recommendedLine = document.getElementById("recommended-jobs-line");
      if (recommendedLine) {
        if (!data.resume_uploaded) {
          recommendedLine.textContent = "Upload your resume to identify your best suited position and get job recommendations.";
        } else if (data.recommended_jobs_count > 0) {
          recommendedLine.textContent = `Your resume matches ${data.best_suited_role?.best_role_title || "your target role"} best (${data.best_suited_role?.best_match_score}% fit). You're a strong match for ${data.recommended_jobs_count} open position${data.recommended_jobs_count === 1 ? "" : "s"}.`;
        } else {
          recommendedLine.textContent = `Your resume matches ${data.best_suited_role?.best_role_title || "your target role"} best (${data.best_suited_role?.best_match_score}% fit). Check back as new job postings are published.`;
        }
      }

      const skillsList = document.getElementById("skills-list");
      if (skillsList) {
        if (data.skills && data.skills.length) {
          skillsList.innerHTML = data.skills
            .map((s) => `<span class="badge bg-primary-subtle text-primary border border-primary-subtle px-3 py-2 fs-6 shadow-sm me-1 mb-1">⚡ ${s}</span>`)
            .join("");
        } else {
          skillsList.innerHTML = '<span class="text-muted-custom small">No skills added yet. Complete your profile details or upload a resume to see skills here.</span>';
        }
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

      const nameEl = document.getElementById("cand-name-display");
      if (nameEl) nameEl.textContent = user ? user.name : "Candidate";
      const headlineEl = document.getElementById("cand-headline-display");
      if (headlineEl) headlineEl.textContent = p.headline || p.current_role || "Software Professional";
      const locEl = document.getElementById("cand-location-display");
      if (locEl) locEl.textContent = p.location ? `📍 ${p.location}` : "📍 Location Not Specified";
      const expEl = document.getElementById("cand-experience-display");
      if (expEl) expEl.textContent = `💼 ${p.experience_years || 0} Years Experience`;

      const photoEl = document.getElementById("cand-profile-photo");
      if (photoEl) {
        if (p.profile_photo) {
          photoEl.src = p.profile_photo;
        } else {
          const name = encodeURIComponent(user ? user.name : "Candidate");
          photoEl.src = `https://ui-avatars.com/api/?name=${name}&background=2f5fff&color=fff&size=128`;
        }
      }

      // Social Links
      const btnIn = document.getElementById("cand-btn-linkedin");
      if (btnIn) {
        if (p.linkedin_url) {
          btnIn.href = p.linkedin_url;
          btnIn.classList.remove("d-none");
        } else {
          btnIn.classList.add("d-none");
        }
      }

      const btnGit = document.getElementById("cand-btn-github");
      if (btnGit) {
        if (p.github_url) {
          btnGit.href = p.github_url;
          btnGit.classList.remove("d-none");
        } else {
          btnGit.classList.add("d-none");
        }
      }

      const btnPort = document.getElementById("cand-btn-portfolio");
      if (btnPort) {
        if (p.portfolio_url) {
          btnPort.href = p.portfolio_url;
          btnPort.classList.remove("d-none");
        } else {
          btnPort.classList.add("d-none");
        }
      }

      // Populate Edit Form
      const setVal = (id, val) => {
        const el = document.getElementById(id);
        if (el) el.value = val || "";
      };
      setVal("edit-cand-headline", p.headline);
      setVal("edit-cand-role", p.current_role);
      setVal("edit-cand-photo", p.profile_photo);
      setVal("edit-cand-location", p.location);
      setVal("edit-cand-summary", p.summary);
      setVal("edit-cand-phone", p.phone);
      setVal("edit-cand-exp", p.experience_years);
      setVal("edit-cand-certifications", p.certifications);
      setVal("edit-cand-linkedin", p.linkedin_url);
      setVal("edit-cand-github", p.github_url);
      setVal("edit-cand-portfolio", p.portfolio_url);
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

  async function loadCandidateCodingAssessments() {
    const container = document.getElementById("candidate-coding-assessments-container");
    if (!container || !window.codingAPI) return;

    try {
      const res = await codingAPI.getCandidateAssessments();
      if (res.success && res.data.length > 0) {
        container.innerHTML = `
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="bg-light text-secondary small">
                <tr>
                  <th>Assessment Title</th>
                  <th>Duration</th>
                  <th>Passing Score</th>
                  <th>Status</th>
                  <th>Score</th>
                  <th class="text-end">Action</th>
                </tr>
              </thead>
              <tbody>
                ${res.data.map(item => {
                  const isDev = item.role_type === 'developer' || item.assessment_type === 'coding';
                  const isRecruiter = item.role_type === 'recruiter';
                  const typeLabel = isDev 
                    ? `💻 <strong>Technical Coding Assessment</strong> (${item.questions_count} Coding Challenges)` 
                    : (isRecruiter 
                        ? `📝 <strong>Recruiter Aptitude & Evaluation</strong> (${item.questions_count} Questions)` 
                        : `📝 <strong>Job Role Aptitude Assessment</strong> (${item.questions_count} Questions)`);
                  const typeBadge = isDev 
                    ? `<span class="badge bg-dark border border-info text-info me-1">💻 Coding</span>` 
                    : `<span class="badge bg-dark border border-primary text-primary me-1">📝 Aptitude</span>`;

                  return `
                  <tr>
                    <td class="fw-semibold">
                      ${typeBadge} ${item.title}
                      <div class="small text-muted fw-normal mt-1">${typeLabel}</div>
                    </td>
                    <td>${item.duration_minutes} Mins</td>
                    <td>${item.passing_score}%</td>
                    <td>
                      <span class="badge bg-${item.status === 'Evaluated' ? (item.passed ? 'success' : 'danger') : item.status === 'In Progress' ? 'warning' : 'secondary'}">
                        ${item.status === 'Evaluated' ? (item.passed ? 'Passed ✓' : 'Failed ❌') : item.status}
                      </span>
                    </td>
                    <td>${item.status === 'Evaluated' && item.score !== null && item.score !== undefined ? `${Math.round(item.score)}%` : '—'}</td>
                    <td class="text-end">
                      ${item.status === 'Evaluated' ? `
                        <a href="coding-report.html?attempt_id=${item.attempt_id}" class="btn btn-sm btn-outline-primary fw-semibold">View Result</a>
                      ` : `
                        <a href="coding-assessment.html?assessment_id=${item.id}" class="btn btn-sm btn-primary fw-bold">Start Assessment &rarr;</a>
                      `}
                    </td>
                  </tr>
                `;
              }).join('')}
              </tbody>
            </table>
          </div>
        `;
      } else {
        container.innerHTML = '<div class="text-muted small text-center py-3">No coding assessments assigned to your job applications yet.</div>';
      }
    } catch (err) {
      container.innerHTML = `<div class="text-danger small text-center py-3">Error loading assessments: ${err.message}</div>`;
    }
  }

  async function loadCandidateVoiceInterviews() {
    const container = document.getElementById("candidate-voice-interviews-container");
    if (!container) return;

    try {
      let upcomingList = [];
      if (window.scheduledInterviewsAPI) {
        const schedRes = await scheduledInterviewsAPI.getUpcoming().catch(() => null);
        if (schedRes && schedRes.success) upcomingList = schedRes.data || [];
      }

      let interviewsList = [];
      if (window.interviewsAPI) {
        const intRes = await interviewsAPI.list().catch(() => null);
        if (intRes && intRes.success) interviewsList = intRes.data || [];
      }

      if (upcomingList.length > 0 || interviewsList.length > 0) {
        let html = `
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="bg-light text-secondary small">
                <tr>
                  <th>Job Title</th>
                  <th>Interview Type</th>
                  <th>Scheduled Time</th>
                  <th>Status</th>
                  <th>Score</th>
                  <th class="text-end">Calendar &amp; Actions</th>
                </tr>
              </thead>
              <tbody>
        `;

        // Combine scheduled upcoming items
        upcomingList.forEach(item => {
          const dt = new Date(item.start_time_utc);
          const dtStr = dt.toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' });
          html += `
            <tr>
              <td class="fw-semibold">${item.job_title}</td>
              <td><span class="badge bg-secondary">${item.interview_type}</span></td>
              <td><span class="fw-medium text-dark">${dtStr}</span> <span class="badge bg-light text-dark border">${item.timezone || 'UTC'}</span></td>
              <td><span class="badge bg-${item.status === 'SCHEDULED' ? 'primary' : 'info'}">${item.status}</span></td>
              <td>—</td>
              <td class="text-end">
                <div class="d-inline-flex gap-1 flex-wrap justify-content-end">
                  <a href="${item.join_link}" class="btn btn-sm btn-primary fw-bold shadow-sm">Join Voice Room &rarr;</a>
                  <a href="${item.google_calendar_url}" target="_blank" class="btn btn-sm btn-outline-success fw-semibold" title="Add to Google Calendar">+ Google</a>
                  <a href="${item.outlook_calendar_url}" target="_blank" class="btn btn-sm btn-outline-info fw-semibold" title="Add to Outlook Calendar">+ Outlook</a>
                  <a href="${item.ics_download_url}" class="btn btn-sm btn-outline-secondary fw-semibold" title="Download .ics file">📥 .ICS</a>
                </div>
              </td>
            </tr>
          `;
        });

        // List standard interviews
        interviewsList.forEach(item => {
          if (!upcomingList.some(u => u.interview_id === item.id)) {
            html += `
              <tr>
                <td class="fw-semibold">${item.job ? item.job.title : 'Position'}</td>
                <td><span class="badge bg-secondary">${item.interview_type}</span></td>
                <td>Instant Online Session</td>
                <td>
                  <span class="badge bg-${item.status === 'completed' ? 'success' : item.status === 'in_progress' ? 'warning' : 'info'}">
                    ${item.status}
                  </span>
                </td>
                <td>${item.overall_score !== null && item.overall_score !== undefined ? `${Math.round(item.overall_score)}%` : '—'}</td>
                <td class="text-end">
                  ${item.status === 'completed' ? `
                    <a href="interview-report.html?interview_id=${item.id}" class="btn btn-sm btn-outline-primary fw-semibold">View Evaluation Report</a>
                  ` : `
                    <a href="live-interview-room.html?interview_id=${item.id}" class="btn btn-sm btn-primary fw-bold shadow-sm">Join Voice Room &rarr;</a>
                  `}
                </td>
              </tr>
            `;
          }
        });

        html += `</tbody></table></div>`;
        container.innerHTML = html;
      } else {
        container.innerHTML = '<div class="text-muted small text-center py-3">No live AI voice interviews scheduled for your applications yet.</div>';
      }
    } catch (err) {
      container.innerHTML = `<div class="text-danger small text-center py-3">Error loading voice interviews: ${err.message}</div>`;
    }
  }

  async function loadCandidateScreeningStatus() {
    const container = document.getElementById("candidate-screening-container");
    if (!container) return;
    try {
      const res = await API.get("/applications");
      const apps = res.data || [];
      if (!apps || apps.length === 0) {
        container.innerHTML = '<div class="text-muted small text-center py-3">No active job applications found.</div>';
        return;
      }

      let html = `<div class="table-responsive"><table class="table table-hover align-middle mb-0"><thead class="bg-light text-secondary small"><tr><th>Job Title</th><th>Applied Date</th><th>Screening Channel</th><th>Status</th><th>Pre-Screening Score</th></tr></thead><tbody>`;
      apps.forEach(app => {
        const scStatus = app.screening_status || "in_progress";
        const scoreDisplay = app.overall_score ? `${Math.round(app.overall_score)}%` : (scStatus === "completed" ? "Completed" : "In Progress (WhatsApp/SMS)");
        const statusBadge = scStatus === "completed" ? '<span class="badge bg-success">Completed ✓</span>' : '<span class="badge bg-primary">In Progress</span>';
        html += `
          <tr>
            <td class="fw-semibold">${app.job_title || 'Position'}</td>
            <td class="text-muted small">${new Date(app.applied_at).toLocaleDateString()}</td>
            <td><span class="badge bg-light text-dark border">WhatsApp / SMS</span></td>
            <td>${statusBadge}</td>
            <td class="fw-bold text-primary">${scoreDisplay}</td>
          </tr>
        `;
      });
      html += `</tbody></table></div>`;
      container.innerHTML = html;
    } catch (err) {
      container.innerHTML = `<div class="text-muted small text-center py-3">No active screening sessions.</div>`;
    }
  }

  const refreshVoiceBtn = document.getElementById("btn-refresh-voice-interviews");
  if (refreshVoiceBtn) {
    refreshVoiceBtn.addEventListener("click", loadCandidateVoiceInterviews);
  }

  // Load immediately on script execution
  loadExplorerJobs();
  loadCandidateCodingAssessments();
  loadCandidateVoiceInterviews();
  loadCandidateScreeningStatus();

  document.addEventListener("ar:auth-ready", () => {
    load();
    loadCandidateProfileData();
    loadExplorerJobs();
    loadCandidateCodingAssessments();
    loadCandidateVoiceInterviews();
    loadCandidateScreeningStatus();
  });
})();




