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

  let profileCompletionChartInstance = null;

  function renderProfileCompletionChart(percent) {
    const canvas = document.getElementById("chart-profile-completion");
    if (!canvas) return;

    if (profileCompletionChartInstance) {
      profileCompletionChartInstance.destroy();
      profileCompletionChartInstance = null;
    }
    const existingChart = typeof Chart !== "undefined" && Chart.getChart ? Chart.getChart(canvas) : null;
    if (existingChart) {
      existingChart.destroy();
    }

    profileCompletionChartInstance = new Chart(canvas, {
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

  let appsStatusChartInstance = null;

  function renderApplicationsStatusChart(byStatus) {
    const labels = Object.keys(byStatus);
    const values = Object.values(byStatus);
    const hasData = values.some((v) => v > 0);

    const canvasEl = document.getElementById("chart-applications-status");
    const emptyEl = document.getElementById("chart-applications-status-empty");
    if (!canvasEl) return;

    if (!hasData) {
      canvasEl.classList.add("d-none");
      if (emptyEl) emptyEl.classList.remove("d-none");
      return;
    }
    canvasEl.classList.remove("d-none");
    if (emptyEl) emptyEl.classList.add("d-none");

    if (appsStatusChartInstance) {
      appsStatusChartInstance.destroy();
      appsStatusChartInstance = null;
    }
    const existingChart = typeof Chart !== "undefined" && Chart.getChart ? Chart.getChart(canvasEl) : null;
    if (existingChart) {
      existingChart.destroy();
    }

    const colorMap = {
      applied: "#94a3ff",
      under_review: "#f59e0b",
      shortlisted: "#3b82f6",
      interview: "#8b5cf6",
      selected: "#10b981",
      rejected: "#ef4444",
    };
    const bgColors = labels.map(l => colorMap[l.toLowerCase()] || "#64748b");

    appsStatusChartInstance = new Chart(canvasEl, {
      type: "doughnut",
      data: {
        labels: labels.map((l) => l.replace("_", " ").toUpperCase()),
        datasets: [
          {
            data: values,
            backgroundColor: bgColors,
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
      
      const elShortlisted = document.getElementById("stat-shortlisted-count");
      if (elShortlisted) elShortlisted.textContent = data.shortlisted_count ?? (data.applications_by_status?.shortlisted || 0);

      const elSelected = document.getElementById("stat-selected-count");
      if (elSelected) elSelected.textContent = data.selected_count ?? (data.applications_by_status?.selected || 0);

      const elInt = document.getElementById("stat-interviews-count") || document.getElementById("stat-interview-status");
      if (elInt) elInt.textContent = interviewStatusLabel ? interviewStatusLabel(data.interview_status) : data.applications_count;

      renderProfileCompletionChart(data.profile_completion);
      renderApplicationsStatusChart(data.applications_by_status);
      loadCandidateApplications();

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

      // Load Candidate Portfolio Website Status
      loadCandidatePortfolioStatus();
    } catch (err) {
      showAlert(err.message, "danger");
    }
  }

  async function loadCandidatePortfolioStatus() {
    try {
      const portRes = await portfolioAPI.getMyPortfolio();
      const port = portRes?.data;

      const card = document.getElementById("dash-portfolio-card");
      const statusBadge = document.getElementById("dash-portfolio-status-badge");
      const themeBadge = document.getElementById("dash-portfolio-theme-badge");
      const descEl = document.getElementById("dash-portfolio-desc");
      const urlContainer = document.getElementById("dash-portfolio-url-container");
      const urlLink = document.getElementById("dash-portfolio-url-link");
      const btnCopy = document.getElementById("dash-btn-copy-link");
      const btnView = document.getElementById("dash-btn-view-portfolio");
      const btnDelete = document.getElementById("dash-btn-delete-portfolio");
      const actionText = document.getElementById("dash-portfolio-action-text");

      if (port) {
        if (btnDelete) {
          btnDelete.classList.remove("d-none");
          btnDelete.disabled = false;
          btnDelete.textContent = "🗑️ Delete";
          btnDelete.onclick = async () => {
            if (confirm("Are you sure you want to permanently delete your portfolio? This action cannot be undone.")) {
              btnDelete.disabled = true;
              btnDelete.textContent = "Deleting...";
              try {
                await portfolioAPI.deleteMyPortfolio();
                await loadCandidatePortfolioStatus();
              } catch (err) {
                alert("Failed to delete portfolio: " + (err.message || "Unknown error"));
                btnDelete.disabled = false;
                btnDelete.textContent = "🗑️ Delete";
              }
            }
          };
        }
        if (themeBadge) {
          themeBadge.textContent = `Theme: ${(port.theme_id || 'Modern').toUpperCase()}`;
          themeBadge.classList.remove("d-none");
        }
        if (actionText) actionText.textContent = "Edit Portfolio";

        if (port.is_published) {
          if (statusBadge) {
            statusBadge.textContent = "Published Live";
            statusBadge.className = "badge bg-success text-white px-2 py-1 small rounded-pill";
          }
          if (descEl) descEl.textContent = `Your portfolio is published and viewable by recruiters! Views: ${port.views_count || 0}`;
          if (urlContainer) {
            urlContainer.classList.remove("d-none");
            urlLink.href = `/portfolio/${port.slug}`;
            urlLink.textContent = `/portfolio/${port.slug}`;
          }
          if (btnCopy) {
            btnCopy.classList.remove("d-none");
            btnCopy.onclick = () => {
              navigator.clipboard.writeText(`${window.location.origin}/portfolio/${port.slug}`);
              btnCopy.textContent = "✓ Copied!";
              setTimeout(() => { btnCopy.textContent = "📋 Copy Link"; }, 2000);
            };
          }
          if (btnView) {
            btnView.classList.remove("d-none");
            btnView.href = `/portfolio/${port.slug}`;
          }
        } else {
          if (statusBadge) {
            statusBadge.textContent = "Draft";
            statusBadge.className = "badge bg-secondary-subtle text-secondary px-2 py-1 small rounded-pill";
          }
          if (descEl) descEl.textContent = "Your portfolio is saved in draft mode. Click 'Edit Portfolio' to customize and publish it.";
          if (urlContainer) urlContainer.classList.add("d-none");
          if (btnCopy) btnCopy.classList.add("d-none");
          if (btnView) btnView.classList.add("d-none");
        }
      } else {
        if (btnDelete) btnDelete.classList.add("d-none");
        if (urlContainer) urlContainer.classList.add("d-none");
        if (btnCopy) btnCopy.classList.add("d-none");
        if (btnView) btnView.classList.add("d-none");
        if (statusBadge) {
          statusBadge.textContent = "Not Created";
          statusBadge.className = "badge bg-light text-muted border px-2 py-1 small rounded-pill";
        }
        if (themeBadge) themeBadge.classList.add("d-none");
        if (descEl) descEl.textContent = "You haven't created a portfolio yet. Build your professional portfolio in 1 click!";
        if (actionText) actionText.textContent = "Build Portfolio";
      }
    } catch (err) {
      console.debug("Portfolio status not loaded:", err);
    }
  }

  async function loadATSAnalysis() {
    try {
      const meRes = await API.get("/resumes/me");
      if (!meRes || !meRes.data || !meRes.data.id) return;
      const candId = meRes.data.id;
      const jobsRes = await jobsAPI.list();
      const jobs = jobsRes?.data || [];
      if (!jobs || !jobs.length || !jobs[0] || !jobs[0].id) return;

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
      let p = {};
      try {
        const res = await API.get("/resumes/me");
        p = res?.data || {};
      } catch (e) {
        p = {};
      }
      const user = Session.getUser();

      // Candidate name MUST come directly from the uploaded resume as single source of truth, fallback to registered user name
      const candidateName = p.name || p.full_name || (user ? user.name : "Candidate");

      const nameEl = document.getElementById("cand-name-display");
      if (nameEl) nameEl.textContent = candidateName;
      const headlineEl = document.getElementById("cand-headline-display");
      if (headlineEl) headlineEl.textContent = p.headline || p.current_role || "";
      const locEl = document.getElementById("cand-location-display");
      if (locEl) locEl.textContent = p.location ? `📍 ${p.location}` : "📍 Location Not Specified";
      const expEl = document.getElementById("cand-experience-display");
      if (expEl) expEl.textContent = `💼 ${p.experience_years || 0} Years Experience`;

      const photoEl = document.getElementById("cand-profile-photo");
      if (photoEl) {
        if (p.profile_photo) {
          photoEl.src = p.profile_photo;
        } else {
          const nameEnc = encodeURIComponent(candidateName);
          photoEl.src = `https://ui-avatars.com/api/?name=${nameEnc}&background=2f5fff&color=fff&size=128`;
        }
      }

      // Update header greeting with candidate resume name
      const greeting = document.getElementById("user-greeting");
      if (greeting) {
        greeting.textContent = `${candidateName} • Candidate`;
        greeting.classList.remove("skeleton");
      }

      // Synchronize session user name with resume name throughout app
      if (user && candidateName && user.name !== candidateName) {
        user.name = candidateName;
        Session.setUser(user);
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

      // Populate Edit Form with all candidate and academic credentials
      await populateEditModalFromProfile();

      // Load College Student Academic Details Display
      try {
        const studRes = await api.student.getProfile();
        const sp = studRes?.data;
        if (sp) {
          if (sp.name && sp.name !== "Candidate") {
            const nameEl = document.getElementById("cand-name-display");
            if (nameEl) nameEl.textContent = sp.name;
            const photoEl = document.getElementById("cand-profile-photo");
            if (photoEl && !p.profile_photo) {
              photoEl.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(sp.name)}&background=2f5fff&color=fff&size=128`;
            }
          }
          const colEl = document.getElementById("cand-college-display");
          if (colEl) colEl.textContent = sp.college_name ? `🏛️ ${cleanInstitutionName(sp.college_name)}` : "🏛️ College / University";
          const degEl = document.getElementById("cand-degree-display");
          if (degEl) degEl.textContent = sp.degree && sp.branch ? `${sp.degree} (${sp.branch})` : (sp.degree || "Degree & Branch");
          const cgpaEl = document.getElementById("cand-cgpa-display");
          if (cgpaEl) cgpaEl.textContent = sp.cgpa ? `CGPA: ${sp.cgpa}` : "CGPA: —";
        }
      } catch (e) {
        // Fallback
      }

      // Load Placement Readiness Metrics
      try {
        const readRes = await api.student.getReadiness();
        const rd = readRes?.data;
        if (rd) {
          const badge = document.getElementById("readiness-score-badge");
          if (badge) badge.textContent = `${rd.overall_readiness_score}/100 Readiness`;
          const streak = document.getElementById("readiness-streak-badge");
          if (streak) streak.textContent = `🔥 ${rd.streak_days} Day Streak`;
          const pBar = document.getElementById("readiness-progress-bar");
          if (pBar) {
            pBar.style.width = `${rd.overall_readiness_score}%`;
            pBar.setAttribute("aria-valuenow", rd.overall_readiness_score);
          }
          const pctText = document.getElementById("readiness-pct-text");
          if (pctText) pctText.textContent = `${rd.overall_readiness_score}% Placement Ready`;

          const aptEl = document.getElementById("stat-readiness-aptitude");
          if (aptEl) aptEl.textContent = `${rd.aptitude_score_avg}%`;
          const testsEl = document.getElementById("stat-readiness-tests");
          if (testsEl) testsEl.textContent = `${rd.tests_completed} Tests`;
          const codeEl = document.getElementById("stat-readiness-coding");
          if (codeEl) codeEl.textContent = `${rd.coding_challenges_completed} Solved`;
          const intEl = document.getElementById("stat-readiness-interviews");
          if (intEl) intEl.textContent = `${rd.mock_interviews_completed} Done`;
        }
      } catch (e) {
        // Fallback
      }
    } catch (e) {
      // Ignore if resume not uploaded yet
    }
  }

  // =========================================================================
  // Candidate Profile 2-Step Navigation (Personal Details -> Basic Information)
  // Retains form data seamlessly without page refresh
  // =========================================================================
  let currentProfileStep = 1;

  function switchCandidateProfileStep(step) {
    currentProfileStep = step;
    const sec1 = document.getElementById("section-personal-details");
    const sec2 = document.getElementById("section-basic-info");
    const tab1 = document.getElementById("tab-step-personal");
    const tab2 = document.getElementById("tab-step-basic");
    const badge1 = document.getElementById("badge-step-1");
    const badge2 = document.getElementById("badge-step-2");
    const subtitle = document.getElementById("profile-step-subtitle");

    if (step === 1) {
      if (sec1) sec1.classList.remove("d-none");
      if (sec2) sec2.classList.add("d-none");
      if (tab1) {
        tab1.className = "btn btn-sm rounded-pill fw-bold flex-fill py-2 btn-primary text-white shadow-sm";
      }
      if (tab2) {
        tab2.className = "btn btn-sm rounded-pill fw-bold flex-fill py-2 btn-outline-secondary border-0 text-muted";
      }
      if (badge1) {
        badge1.className = "badge bg-white text-primary rounded-circle me-1";
      }
      if (badge2) {
        badge2.className = "badge bg-secondary text-white rounded-circle me-1";
      }
      if (subtitle) {
        subtitle.textContent = "Step 1 of 2: Enter Personal Details, then proceed to Basic Information";
      }
    } else {
      if (sec1) sec1.classList.add("d-none");
      if (sec2) sec2.classList.remove("d-none");
      if (tab1) {
        tab1.className = "btn btn-sm rounded-pill fw-bold flex-fill py-2 btn-outline-secondary border-0 text-muted";
      }
      if (tab2) {
        tab2.className = "btn btn-sm rounded-pill fw-bold flex-fill py-2 btn-primary text-white shadow-sm";
      }
      if (badge1) {
        badge1.className = "badge bg-secondary text-white rounded-circle me-1";
      }
      if (badge2) {
        badge2.className = "badge bg-white text-primary rounded-circle me-1";
      }
      if (subtitle) {
        subtitle.textContent = "Step 2 of 2: Professional & Academic Information";
      }
    }

    const modalBody = document.querySelector("#editCandProfileModal .modal-body");
    if (modalBody) {
      modalBody.scrollTo({ top: 0, behavior: "smooth" });
    }
  }

  // Next: Basic Information Button (No page refresh, retains all form data)
  const nextToBasicBtn = document.getElementById("btn-next-to-basic");
  if (nextToBasicBtn) {
    nextToBasicBtn.addEventListener("click", (e) => {
      if (e) {
        e.preventDefault();
        e.stopPropagation();
      }
      const nameVal = document.getElementById("edit-cand-name")?.value?.trim();
      const user = Session.getUser();
      if (nameVal && user) {
        user.name = nameVal;
      }
      switchCandidateProfileStep(2);
    });
  }

  // Back: Personal Details Button (No page refresh, retains all form data)
  const backToPersonalBtn = document.getElementById("btn-back-to-personal");
  if (backToPersonalBtn) {
    backToPersonalBtn.addEventListener("click", (e) => {
      if (e) {
        e.preventDefault();
        e.stopPropagation();
      }
      switchCandidateProfileStep(1);
    });
  }

  // Direct pill tab clicks
  const tabPersonal = document.getElementById("tab-step-personal");
  if (tabPersonal) {
    tabPersonal.addEventListener("click", (e) => {
      if (e) e.preventDefault();
      switchCandidateProfileStep(1);
    });
  }
  const tabBasic = document.getElementById("tab-step-basic");
  if (tabBasic) {
    tabBasic.addEventListener("click", (e) => {
      if (e) e.preventDefault();
      switchCandidateProfileStep(2);
    });
  }

  // Helper to clean institution/school names (removes trailing commas, hyphens, dangling dates)
  function cleanInstitutionName(val) {
    if (!val || typeof val !== "string") return "";
    let s = val.trim();
    s = s.replace(/^(?:college|university|school|institution)\s*[:\-–—]?\s*/i, "");
    s = s.replace(/[\s,–—|•;:/]+\s*(?:from|between|during)?\s*(?:19\d{2}|20\d{2})\s*[-–—to]+\s*(?:19\d{2}|20\d{2}|present|current)?\b.*$/i, "");
    s = s.replace(/[\s,–—|•;:/]+\s*(?:from|between|during)\b.*$/i, "");
    s = s.replace(/[\s,–—|•;:.\\]+$/g, "");
    return s.trim();
  }

  // Auto-populates all candidate personal and academic fields in modal from backend profiles
  async function populateEditModalFromProfile() {
    try {
      const user = Session.getUser() || {};
      let p = {};
      try {
        const res = await API.get("/resumes/me");
        p = res?.data || {};
      } catch (e) {
        p = {};
      }

      let sp = {};
      try {
        const studRes = await api.student.getProfile();
        sp = studRes?.data || {};
      } catch (e) {
        sp = {};
      }

      const setVal = (id, val) => {
        const el = document.getElementById(id);
        if (!el) return;
        if (document.activeElement === el) return;
        el.value = (val !== undefined && val !== null) ? val : "";
      };

      const candidateName = p.full_name || p.name || sp.name || user.name || "";
      const regEmail = user.email || "";
      const resumeEmail = p.resume_email || sp.resume_email || (p.email && p.email !== regEmail ? p.email : "");

      // Step 1: Personal Details
      setVal("edit-cand-name", candidateName);
      setVal("edit-cand-email", regEmail);
      setVal("edit-cand-phone", p.phone || sp.phone || "");
      setVal("edit-cand-location", p.location || sp.location || "");
      setVal("edit-cand-photo", p.profile_photo || "");
      setVal("edit-cand-linkedin", p.linkedin_url || sp.linkedin_url || "");
      setVal("edit-cand-github", p.github_url || sp.github_url || "");
      setVal("edit-cand-portfolio", p.portfolio_url || sp.portfolio_url || "");

      // Step 2: Basic Professional & Academic Information
      setVal("edit-cand-resume-email", resumeEmail);
      setVal("edit-cand-headline", p.headline || sp.current_role || "");
      setVal("edit-cand-role", p.current_role || sp.current_role || p.headline || "");
      setVal("edit-cand-exp", p.experience_years !== undefined && p.experience_years !== null ? p.experience_years : (sp.experience_years !== undefined ? sp.experience_years : ""));
      const skillsVal = (p.skills && p.skills.length) ? p.skills.join(", ") : ((sp.skills && sp.skills.length) ? sp.skills.join(", ") : "");
      setVal("edit-cand-skills", skillsVal);
      setVal("edit-cand-summary", p.summary || sp.summary || "");
      setVal("edit-cand-certifications", p.certifications || sp.certifications || "");

      // College & Academics
      const rawCollege = p.college_name || sp.college_name || "";
      setVal("edit-cand-college", cleanInstitutionName(rawCollege));
      setVal("edit-cand-degree", p.degree || sp.degree || "");
      setVal("edit-cand-branch", p.branch || sp.branch || "");
      setVal("edit-cand-grad-year", p.graduation_year || sp.graduation_year || "");
      setVal("edit-cand-cgpa", p.cgpa !== undefined && p.cgpa !== null ? p.cgpa : (sp.cgpa !== undefined ? sp.cgpa : ""));

      // 12th & 10th
      const raw12School = p.twelfth_school || sp.twelfth_school || "";
      setVal("edit-cand-12th-school", cleanInstitutionName(raw12School));
      setVal("edit-cand-12th-board", p.twelfth_board || sp.twelfth_board || "");
      setVal("edit-cand-12th-year", p.twelfth_year || sp.twelfth_year || "");
      setVal("edit-cand-12th-marks", p.twelfth_percentage !== undefined && p.twelfth_percentage !== null ? p.twelfth_percentage : (sp.twelfth_percentage !== undefined ? sp.twelfth_percentage : ""));

      const raw10School = p.tenth_school || sp.tenth_school || "";
      setVal("edit-cand-10th-school", cleanInstitutionName(raw10School));
      setVal("edit-cand-10th-board", p.tenth_board || sp.tenth_board || "");
      setVal("edit-cand-10th-year", p.tenth_year || sp.tenth_year || "");
      setVal("edit-cand-10th-marks", p.tenth_percentage !== undefined && p.tenth_percentage !== null ? p.tenth_percentage : (sp.tenth_percentage !== undefined ? sp.tenth_percentage : ""));
    } catch (err) {
      console.warn("Could not populate edit modal:", err);
    }
  }

  // Resume Upload Auto-Fill for Candidate Profile & Details Modal
  function initResumeAutofillInModal() {
    const triggerBtn = document.getElementById("btn-trigger-resume-autofill");
    const fileInput = document.getElementById("autofill-resume-file");
    const btnText = document.getElementById("autofill-btn-text");
    const spinner = document.getElementById("autofill-spinner");
    const statusAlert = document.getElementById("autofill-status-alert");
    const statusMsg = document.getElementById("autofill-status-msg");

    if (!triggerBtn || !fileInput) return;

    triggerBtn.addEventListener("click", () => {
      fileInput.click();
    });

    fileInput.addEventListener("change", async (e) => {
      const file = e.target.files?.[0];
      if (!file) return;

      if (statusAlert) statusAlert.classList.add("d-none");
      if (triggerBtn) triggerBtn.disabled = true;
      if (btnText) btnText.textContent = "Extracting Info...";
      if (spinner) spinner.classList.remove("d-none");

      try {
        const resAPI = window.resumesAPI || window.resumeAPI;
        if (!resAPI || !resAPI.extractDetails) {
          throw new Error("Resume extraction service is unavailable.");
        }
        const res = await resAPI.extractDetails(file);
        const data = res?.data || {};

        let filledCount = 0;
        const setVal = (id, val) => {
          const el = document.getElementById(id);
          if (el && val !== undefined && val !== null && String(val).trim() !== "") {
            el.value = val;
            el.classList.add("border-success", "bg-success-subtle", "bg-opacity-10");
            setTimeout(() => el.classList.remove("border-success", "bg-success-subtle", "bg-opacity-10"), 4000);
            filledCount++;
          }
        };

        // Populate Step 1 (Personal Details)
        setVal("edit-cand-name", data.name);
        // Do NOT overwrite account registration email with resume email
        if (data.email) setVal("edit-cand-resume-email", data.email);
        setVal("edit-cand-phone", data.phone);
        setVal("edit-cand-location", data.location);
        setVal("edit-cand-linkedin", data.linkedin_url);
        setVal("edit-cand-github", data.github_url);
        setVal("edit-cand-portfolio", data.portfolio_url);

        // Populate Step 2 (Basic Professional & Academic Information)
        setVal("edit-cand-headline", data.headline);
        setVal("edit-cand-role", data.current_role);
        setVal("edit-cand-exp", data.experience_years);
        setVal("edit-cand-skills", data.skills);
        setVal("edit-cand-summary", data.summary);
        setVal("edit-cand-certifications", data.certifications);
        setVal("edit-cand-college", cleanInstitutionName(data.college));
        setVal("edit-cand-degree", data.degree);
        setVal("edit-cand-branch", data.branch);
        setVal("edit-cand-grad-year", data.graduation_year);
        setVal("edit-cand-cgpa", data.cgpa);

        // Populate 12th & 10th Grade Credentials
        setVal("edit-cand-12th-school", cleanInstitutionName(data.twelfth_school));
        setVal("edit-cand-12th-board", data.twelfth_board);
        setVal("edit-cand-12th-year", data.twelfth_year);
        setVal("edit-cand-12th-marks", data.twelfth_percentage);

        setVal("edit-cand-10th-school", cleanInstitutionName(data.tenth_school));
        setVal("edit-cand-10th-board", data.tenth_board);
        setVal("edit-cand-10th-year", data.tenth_year);
        setVal("edit-cand-10th-marks", data.tenth_percentage);

        // Update Session user name if extracted
        const user = Session.getUser();
        if (user && data.name) {
          user.name = data.name;
          if (typeof Session.setUser === "function") {
            Session.setUser(user);
          } else if (typeof Session.save === "function") {
            Session.save({ user });
          } else if (typeof safeStorage !== "undefined") {
            safeStorage.setItem("ar_user", JSON.stringify(user));
          }
        }

        if (statusAlert && statusMsg) {
          statusAlert.className = "alert alert-success py-2 px-3 mb-0 mt-3 d-flex align-items-center justify-content-between small shadow-xs";
          statusMsg.innerHTML = `<span><strong>🎉 Resume Extracted!</strong> Successfully auto-filled <strong>${filledCount} fields</strong> and generated your portfolio.</span>`;
          statusAlert.classList.remove("d-none");
        }

        // Live update portfolio status on dashboard
        loadCandidatePortfolioStatus();
      } catch (err) {
        if (statusAlert && statusMsg) {
          statusAlert.className = "alert alert-danger py-2 px-3 mb-0 mt-3 d-flex align-items-center justify-content-between small shadow-xs";
          statusMsg.innerHTML = `<span><strong>Extraction failed:</strong> ${err.message || "Could not read resume. Please verify the file is a valid PDF or DOCX."}</span>`;
          statusAlert.classList.remove("d-none");
        }
      } finally {
        if (triggerBtn) triggerBtn.disabled = false;
        if (btnText) btnText.textContent = "Upload Resume";
        if (spinner) spinner.classList.add("d-none");
        fileInput.value = "";
      }
    });
  }

  initResumeAutofillInModal();

  function checkPendingResumeAutofill() {
    let raw = null;
    if (typeof safeStorage !== "undefined") {
      raw = safeStorage.getItem("pending_resume_autofill");
      safeStorage.removeItem("pending_resume_autofill");
    } else {
      try {
        raw = localStorage.getItem("pending_resume_autofill");
        localStorage.removeItem("pending_resume_autofill");
      } catch (e) {}
    }
    if (!raw) return;

    try {
      const data = JSON.parse(raw);
      if (!data) return;

      const setVal = (id, val) => {
        const el = document.getElementById(id);
        if (el && val !== undefined && val !== null && String(val).trim() !== "") {
          el.value = val;
          el.classList.add("border-success", "bg-success-subtle", "bg-opacity-10");
        }
      };

      // Populate Step 1 (Personal Details)
      setVal("edit-cand-name", data.name);
      // Do NOT overwrite account registration email with resume email
      if (data.email) setVal("edit-cand-resume-email", data.email);
      setVal("edit-cand-phone", data.phone);
      setVal("edit-cand-location", data.location);
      setVal("edit-cand-linkedin", data.linkedin_url);
      setVal("edit-cand-github", data.github_url);
      setVal("edit-cand-portfolio", data.portfolio_url);

      // Populate Step 2 (Basic Professional & Academic Information)
      setVal("edit-cand-headline", data.headline);
      setVal("edit-cand-role", data.current_role);
      setVal("edit-cand-exp", data.experience_years);
      setVal("edit-cand-skills", data.skills);
      setVal("edit-cand-summary", data.summary);
      setVal("edit-cand-certifications", data.certifications);
      setVal("edit-cand-college", cleanInstitutionName(data.college));
      setVal("edit-cand-degree", data.degree);
      setVal("edit-cand-branch", data.branch);
      setVal("edit-cand-grad-year", data.graduation_year);
      setVal("edit-cand-cgpa", data.cgpa);

      // Populate 12th & 10th Grade Credentials
      setVal("edit-cand-12th-school", cleanInstitutionName(data.twelfth_school));
      setVal("edit-cand-12th-board", data.twelfth_board);
      setVal("edit-cand-12th-year", data.twelfth_year);
      setVal("edit-cand-12th-marks", data.twelfth_percentage);

      setVal("edit-cand-10th-school", cleanInstitutionName(data.tenth_school));
      setVal("edit-cand-10th-board", data.tenth_board);
      setVal("edit-cand-10th-year", data.tenth_year);
      setVal("edit-cand-10th-marks", data.tenth_percentage);

      const statusAlert = document.getElementById("autofill-status-alert");
      const statusMsg = document.getElementById("autofill-status-msg");
      if (statusAlert && statusMsg) {
        statusAlert.className = "alert alert-success py-2 px-3 mb-0 mt-3 d-flex align-items-center justify-content-between small shadow-xs";
        statusMsg.innerHTML = `<span><strong>🎉 Welcome!</strong> Details extracted from your resume have been populated into Personal Details & Basic Information.</span>`;
        statusAlert.classList.remove("d-none");
      }
    } catch (e) {
      console.warn("Could not parse pending resume autofill:", e);
    }
  }

  checkPendingResumeAutofill();


  // Reset to Step 1 and re-populate latest details whenever modal opens
  const editModalEl = document.getElementById("editCandProfileModal");
  if (editModalEl) {
    editModalEl.addEventListener("show.bs.modal", () => {
      switchCandidateProfileStep(1);
      populateEditModalFromProfile();
    });
  }

  // Auto-prompt candidate profile wizard on first onboarding or incomplete profile
  setTimeout(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const u = Session.getUser();
    if (urlParams.get("onboarding") === "1" || (u && u.is_profile_complete === false)) {
      const modalEl = document.getElementById("editCandProfileModal");
      if (modalEl && window.bootstrap) {
        const m = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
        m.show();
      }
    }
  }, 600);

  // Form submission handler (saves both sections without refreshing the page)
  const candForm = document.getElementById("edit-cand-profile-form");
  async function handleCandidateProfileSave(e) {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    const saveBtn = document.getElementById("save-cand-profile-btn");
    const saveText = document.getElementById("save-cand-profile-text");
    const saveSpinner = document.getElementById("save-cand-profile-spinner");
    if (saveBtn) saveBtn.disabled = true;
    if (saveText) saveText.textContent = "Saving...";
    if (saveSpinner) saveSpinner.classList.remove("d-none");

    const expVal = document.getElementById("edit-cand-exp")?.value;
    const nameVal = document.getElementById("edit-cand-name")?.value?.trim() || null;
    const skillsStr = document.getElementById("edit-cand-skills")?.value?.trim() || "";
    const skillsArr = skillsStr ? skillsStr.split(",").map(s => s.trim()).filter(Boolean) : undefined;

    const payload = {
      name: nameVal,
      full_name: nameVal,
      headline: document.getElementById("edit-cand-headline")?.value?.trim() || null,
      current_role: document.getElementById("edit-cand-role")?.value?.trim() || null,
      profile_photo: document.getElementById("edit-cand-photo")?.value?.trim() || null,
      location: document.getElementById("edit-cand-location")?.value?.trim() || null,
      summary: document.getElementById("edit-cand-summary")?.value?.trim() || null,
      phone: document.getElementById("edit-cand-phone")?.value?.trim() || null,
      experience_years: expVal ? Number(expVal) : null,
      skills: skillsArr,
      certifications: document.getElementById("edit-cand-certifications")?.value?.trim() || null,
      linkedin_url: document.getElementById("edit-cand-linkedin")?.value?.trim() || null,
      github_url: document.getElementById("edit-cand-github")?.value?.trim() || null,
      portfolio_url: document.getElementById("edit-cand-portfolio")?.value?.trim() || null,
    };

    const collegeVal = document.getElementById("edit-cand-college")?.value?.trim() || null;
    const degreeVal = document.getElementById("edit-cand-degree")?.value?.trim() || null;
    const branchVal = document.getElementById("edit-cand-branch")?.value?.trim() || null;
    const gradYearVal = document.getElementById("edit-cand-grad-year")?.value ? Number(document.getElementById("edit-cand-grad-year").value) : null;
    const cgpaVal = document.getElementById("edit-cand-cgpa")?.value ? Number(document.getElementById("edit-cand-cgpa").value) : null;

    const twelfthSchoolVal = document.getElementById("edit-cand-12th-school")?.value?.trim() || null;
    const twelfthBoardVal = document.getElementById("edit-cand-12th-board")?.value?.trim() || null;
    const twelfthYearVal = document.getElementById("edit-cand-12th-year")?.value ? Number(document.getElementById("edit-cand-12th-year").value) : null;
    const twelfthMarksVal = document.getElementById("edit-cand-12th-marks")?.value ? Number(document.getElementById("edit-cand-12th-marks").value) : null;

    const tenthSchoolVal = document.getElementById("edit-cand-10th-school")?.value?.trim() || null;
    const tenthBoardVal = document.getElementById("edit-cand-10th-board")?.value?.trim() || null;
    const tenthYearVal = document.getElementById("edit-cand-10th-year")?.value ? Number(document.getElementById("edit-cand-10th-year").value) : null;
    const tenthMarksVal = document.getElementById("edit-cand-10th-marks")?.value ? Number(document.getElementById("edit-cand-10th-marks").value) : null;
    const resumeEmailVal = document.getElementById("edit-cand-resume-email")?.value?.trim() || null;

    payload.resume_email = resumeEmailVal;
    payload.college_name = collegeVal;
    payload.degree = degreeVal;
    payload.branch = branchVal;
    payload.graduation_year = gradYearVal;
    payload.cgpa = cgpaVal;
    payload.twelfth_school = twelfthSchoolVal;
    payload.twelfth_board = twelfthBoardVal;
    payload.twelfth_year = twelfthYearVal;
    payload.twelfth_percentage = twelfthMarksVal;
    payload.tenth_school = tenthSchoolVal;
    payload.tenth_board = tenthBoardVal;
    payload.tenth_year = tenthYearVal;
    payload.tenth_percentage = tenthMarksVal;

    try {
      await API.put("/resumes/me", payload);
      await api.student.updateProfile({
        name: nameVal,
        resume_email: resumeEmailVal,
        phone: payload.phone,
        location: payload.location,
        summary: payload.summary,
        experience_years: payload.experience_years,
        skills: payload.skills,
        certifications: payload.certifications,
        college_name: collegeVal,
        degree: degreeVal,
        branch: branchVal,
        graduation_year: gradYearVal,
        cgpa: cgpaVal,
        twelfth_school: twelfthSchoolVal,
        twelfth_board: twelfthBoardVal,
        twelfth_year: twelfthYearVal,
        twelfth_percentage: twelfthMarksVal,
        tenth_school: tenthSchoolVal,
        tenth_board: tenthBoardVal,
        tenth_year: tenthYearVal,
        tenth_percentage: tenthMarksVal,
        target_role: payload.headline || payload.current_role,
        is_student: true,
      });

      // Update session with new name and is_profile_complete flag
      const curUser = Session.getUser() || {};
      const newName = document.getElementById("edit-cand-name")?.value?.trim();
      if (newName) curUser.name = newName;
      curUser.is_profile_complete = true;
      Session.save({
        access_token: Session.getAccessToken(),
        refresh_token: (typeof safeStorage !== "undefined" ? safeStorage.getItem("ar_refresh_token") : localStorage.getItem("ar_refresh_token")),
        user: curUser,
      });

      // Gracefully close modal without reloading the page
      const modalEl = document.getElementById("editCandProfileModal");
      if (window.bootstrap && modalEl) {
        const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
        modal.hide();
      }

      // Live update dashboard UI
      loadCandidateProfileData();
      await loadCandidatePortfolioStatus();

      // Show in-page success alert
      const dashAlert = document.getElementById("dashboard-alert");
      if (dashAlert) {
        dashAlert.className = "alert alert-success alert-dismissible fade show py-2 mb-4 fw-semibold shadow-sm";
        dashAlert.innerHTML = `🎉 Candidate profile and academic details saved successfully! <button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
        dashAlert.classList.remove("d-none");
        setTimeout(() => dashAlert.classList.add("d-none"), 5000);
      }
    } catch (err) {
      alert(err.message || "Failed to save profile. Please try again.");
    } finally {
      if (saveBtn) saveBtn.disabled = false;
      if (saveText) saveText.textContent = "Save Profile ✓";
      if (saveSpinner) saveSpinner.classList.add("d-none");
    }
  }

  if (candForm) {
    candForm.addEventListener("submit", handleCandidateProfileSave);
  }
  const saveProfileBtn = document.getElementById("save-cand-profile-btn");
  if (saveProfileBtn) {
    saveProfileBtn.addEventListener("click", handleCandidateProfileSave);
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
      if (!meRes || !meRes.data || !meRes.data.id) throw new Error("Please upload a resume first.");
      const candId = meRes.data.id;
      const jobsRes = await jobsAPI.list();
      const jobs = jobsRes?.data || [];
      if (!jobs || !jobs.length || !jobs[0] || !jobs[0].id) throw new Error("No open jobs available for comparison.");
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
                  if (!item || !item.id) return "";
                  const isFrontend = item.role_type === 'frontend_developer';
                  const isAI = item.role_type === 'ai_developer';
                  const isDev = item.role_type === 'developer' || isFrontend || isAI || item.assessment_type === 'coding';
                  const isRecruiter = item.role_type === 'recruiter';
                  const typeLabel = isFrontend
                    ? `🎨 <strong>Frontend Developer Coding Assessment</strong> (${item.questions_count} Coding Challenges)`
                    : (isAI
                        ? `🤖 <strong>AI Developer Coding Assessment</strong> (${item.questions_count} Coding Challenges)`
                        : (isDev 
                            ? `💻 <strong>Technical Coding Assessment</strong> (${item.questions_count} Coding Challenges)` 
                            : (isRecruiter 
                                ? `📝 <strong>Recruiter Aptitude & Evaluation</strong> (${item.questions_count} Questions)` 
                                : `📝 <strong>Job Role Aptitude Assessment</strong> (${item.questions_count} Questions)`)));
                  const typeBadge = isFrontend
                    ? `<span class="badge bg-dark border border-warning text-warning me-1">🎨 Frontend</span>`
                    : (isAI
                        ? `<span class="badge bg-dark border border-info text-info me-1">🤖 AI Dev</span>`
                        : (isDev 
                            ? `<span class="badge bg-dark border border-info text-info me-1">💻 Coding</span>` 
                            : `<span class="badge bg-dark border border-primary text-primary me-1">📝 Aptitude</span>`));

                  const isTerminated = item.status === 'Terminated';
                  const isExpired = item.status === 'Expired';
                  const statusBadge = isTerminated
                    ? `<span class="badge bg-danger text-white"><i class="bi bi-x-circle me-1"></i>Disqualified</span>`
                    : (isExpired
                        ? `<span class="badge bg-secondary text-white"><i class="bi bi-clock-history me-1"></i>Time Expired</span>`
                        : (item.status === 'Evaluated' 
                            ? `<span class="badge bg-${item.passed ? 'success' : 'danger'}">${item.passed ? 'Passed ✓' : 'Failed ❌'}</span>`
                            : `<span class="badge bg-${item.status === 'In Progress' ? 'warning text-dark' : 'secondary'}">${item.status}</span>`));

                  const actionBtn = (isTerminated || isExpired)
                    ? `<a href="coding-assessment.html?assessment_id=${item.id}&reset=true" class="btn btn-sm ${isExpired ? 'btn-primary' : 'btn-outline-warning'} fw-semibold"><i class="bi bi-arrow-repeat me-1"></i>Retake Test &rarr;</a>`
                    : (item.status === 'Evaluated'
                        ? `<a href="coding-report.html?attempt_id=${item.attempt_id}" class="btn btn-sm btn-outline-primary fw-semibold">View Result</a>`
                        : `<a href="coding-assessment.html?assessment_id=${item.id}" class="btn btn-sm btn-primary fw-bold">Start Assessment &rarr;</a>`);

                  return `
                  <tr>
                    <td class="fw-semibold">
                      ${typeBadge} ${item.title}
                      <div class="small text-muted fw-normal mt-1">${typeLabel}</div>
                    </td>
                    <td>${item.duration_minutes} Mins</td>
                    <td>${item.passing_score}%</td>
                    <td>${statusBadge}</td>
                    <td>${item.status === 'Evaluated' && item.score !== null && item.score !== undefined ? `${Math.round(item.score)}%` : (isTerminated ? '<span class="text-danger fw-bold">0%</span>' : '—')}</td>
                    <td class="text-end">${actionBtn}</td>
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
          if (!item || !item.id) return;
          if (!upcomingList.some(u => u && u.interview_id === item.id)) {
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

  function safeEscape(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  async function loadCandidateApplications() {
    const container = document.getElementById("candidate-applications-container");
    const banner = document.getElementById("dash-status-alert-banner");
    const badge = document.getElementById("dash-apps-badge");
    if (!container) return;

    try {
      const res = await applicationsAPI.mine();
      const apps = res?.data || [];

      if (badge) {
        badge.textContent = `${apps.length} Application${apps.length === 1 ? '' : 's'}`;
      }

      // Update counters based on real-time applications
      const selectedApps = apps.filter(a => {
        const st = (a.status?.value || a.status || "").toLowerCase().trim();
        return st === "selected";
      });

      const shortlistedApps = apps.filter(a => {
        const st = (a.status?.value || a.status || "").toLowerCase().trim();
        return st === "shortlisted" || (a.is_shortlisted && st !== "selected" && st !== "rejected");
      });

      const selectedCount = selectedApps.length;
      const shortlistedCount = shortlistedApps.length;

      const elShortlisted = document.getElementById("stat-shortlisted-count");
      if (elShortlisted) elShortlisted.textContent = shortlistedCount;

      const elSelected = document.getElementById("stat-selected-count");
      if (elSelected) elSelected.textContent = selectedCount;

      const elAppsCount = document.getElementById("stat-applications-count");
      if (elAppsCount) elAppsCount.textContent = apps.length;

      // Status Alert Celebration Banner
      if (banner) {
        if (selectedApps.length > 0) {
          const topApp = selectedApps[0];
          const compName = topApp.company_name || "the hiring team";
          const moreSelected = selectedApps.length > 1 ? ` (and ${selectedApps.length - 1} other position)` : '';
          banner.className = "alert alert-success d-flex align-items-center justify-content-between flex-wrap gap-3 py-3 px-4 mb-4 border-0 shadow-sm";
          banner.style.background = "linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%)";
          banner.style.borderLeft = "6px solid #10b981";
          banner.innerHTML = `
            <div class="d-flex align-items-center gap-3">
              <span class="fs-1">🎉</span>
              <div>
                <h6 class="fw-bold text-success mb-1">Congratulations! You've been Officially Selected!</h6>
                <p class="text-dark small mb-0">The recruiter has selected your application for <strong>${safeEscape(topApp.job_title || 'the role')}</strong> at <strong>${safeEscape(compName)}</strong>${moreSelected}. Look out for onboarding next steps.</p>
                ${shortlistedCount > 0 ? `<div class="mt-1 small text-primary fw-semibold">⭐ You also have ${shortlistedCount} other active application(s) shortlisted by recruiters!</div>` : ''}
              </div>
            </div>
            <div class="d-flex gap-2 align-items-center">
              <button class="btn btn-sm btn-success fw-bold px-3 py-2 shadow-sm msg-rec-btn" data-job-id="${topApp.job_id}">💬 Chat with Recruiter</button>
              <a href="my-applications.html" class="btn btn-sm btn-outline-success fw-semibold px-3 py-2">View Offer &amp; Details &rarr;</a>
            </div>
          `;
          banner.classList.remove("d-none");
        } else if (shortlistedApps.length > 0) {
          const topApp = shortlistedApps[0];
          const compName = topApp.company_name || "the hiring team";
          const moreShortlisted = shortlistedApps.length > 1 ? ` (and ${shortlistedApps.length - 1} other position)` : '';
          banner.className = "alert alert-primary d-flex align-items-center justify-content-between flex-wrap gap-3 py-3 px-4 mb-4 border-0 shadow-sm";
          banner.style.background = "linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%)";
          banner.style.borderLeft = "6px solid #3b82f6";
          banner.innerHTML = `
            <div class="d-flex align-items-center gap-3">
              <span class="fs-1">⭐</span>
              <div>
                <h6 class="fw-bold text-primary mb-1">Great News! Your Application is Shortlisted!</h6>
                <p class="text-dark small mb-0">The hiring team has shortlisted your application for <strong>${safeEscape(topApp.job_title || 'Position')}</strong> at <strong>${safeEscape(compName)}</strong>${moreShortlisted}.</p>
              </div>
            </div>
            <div class="d-flex gap-2 align-items-center">
              <a href="my-applications.html" class="btn btn-sm btn-primary fw-bold px-3 py-2 shadow-sm">View Status &amp; Next Steps &rarr;</a>
            </div>
          `;
          banner.classList.remove("d-none");
        } else {
          banner.classList.add("d-none");
        }
      }

      if (!apps.length) {
        container.innerHTML = `
          <div class="text-center py-4 text-muted">
            <div class="fs-2 mb-2">📋</div>
            <h6 class="fw-bold text-dark">No Job Applications Yet</h6>
            <p class="small text-secondary mb-3">Apply to open job positions to track your recruiter shortlisting, interview invitations, and offers in real-time.</p>
            <a href="jobs.html" class="btn btn-sm btn-primary fw-semibold px-3">Browse Open Jobs &rarr;</a>
          </div>
        `;
        return;
      }

      const rowsHtml = apps.map(app => {
        const rawStatus = (app.status?.value || app.status || "applied").toLowerCase().trim();
        let statusBadgeHtml = "";

        if (rawStatus === "selected") {
          statusBadgeHtml = `<span class="badge bg-success text-white px-3 py-1.5 rounded-pill fw-bold shadow-sm" style="font-size: 0.8rem;">🎉 Selected / Offer</span>`;
        } else if (rawStatus === "shortlisted" || (app.is_shortlisted && rawStatus !== "rejected")) {
          statusBadgeHtml = `<span class="badge bg-primary text-white px-3 py-1.5 rounded-pill fw-bold shadow-sm" style="font-size: 0.8rem;">⭐ Shortlisted by Recruiter</span>`;
        } else if (rawStatus === "interview") {
          statusBadgeHtml = `<span class="badge bg-warning text-dark px-3 py-1.5 rounded-pill fw-semibold" style="font-size: 0.8rem;">🎙️ Interview Scheduled</span>`;
        } else if (rawStatus === "under_review") {
          statusBadgeHtml = `<span class="badge bg-info text-dark px-3 py-1.5 rounded-pill fw-semibold" style="font-size: 0.8rem;">⏳ Under Review</span>`;
        } else if (rawStatus === "rejected") {
          statusBadgeHtml = `<span class="badge bg-danger text-white px-3 py-1.5 rounded-pill fw-semibold" style="font-size: 0.8rem;">❌ Not Selected</span>`;
        } else {
          statusBadgeHtml = `<span class="badge bg-secondary text-white px-3 py-1.5 rounded-pill fw-semibold" style="font-size: 0.8rem;">📝 Applied</span>`;
        }

        const atsScore = app.ats_score != null ? Math.round(app.ats_score) : (app.match_score != null ? Math.round(app.match_score) : null);
        const atsBadge = atsScore != null ? `
          <span class="badge ${atsScore >= 80 ? 'bg-success-subtle text-success border border-success' : atsScore >= 60 ? 'bg-primary-subtle text-primary border border-primary' : 'bg-secondary-subtle text-secondary border'} px-2.5 py-1 rounded-pill small fw-semibold">
            ${atsScore}% ATS Match
          </span>
        ` : `<span class="text-muted small">—</span>`;

        const appliedDate = app.applied_at ? new Date(app.applied_at).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }) : "Recent";
        const compDisplay = app.company_name || "Direct Employer";

        let actionBtn = "";
        if (rawStatus === "selected") {
          actionBtn = `<button class="btn btn-sm btn-success fw-bold px-3 shadow-sm msg-rec-btn" data-job-id="${app.job_id}">💬 Message Recruiter</button>`;
        } else if (rawStatus === "shortlisted" || (app.is_shortlisted && rawStatus !== "rejected")) {
          actionBtn = `<a href="my-applications.html" class="btn btn-sm btn-primary fw-semibold shadow-sm px-3">🚀 Next Steps</a>`;
        } else if (rawStatus === "interview") {
          actionBtn = `<a href="interview.html?job_id=${app.job_id}" class="btn btn-sm btn-warning text-dark fw-semibold shadow-sm px-3">🎙️ Join Interview</a>`;
        } else {
          actionBtn = `<a href="my-applications.html" class="btn btn-sm btn-outline-secondary fw-semibold px-2.5">Details &rarr;</a>`;
        }

        return `
          <tr class="${rawStatus === 'selected' ? 'table-success bg-opacity-10' : (rawStatus === 'shortlisted' ? 'table-primary bg-opacity-10' : '')}">
            <td class="ps-3 py-3">
              <div class="fw-bold text-dark fs-6">${safeEscape(app.job_title || 'Position')}</div>
              <div class="small text-muted d-flex align-items-center gap-1 mt-0.5">
                🏢 ${safeEscape(compDisplay)} ${app.job_location ? `• 📍 ${safeEscape(app.job_location)}` : ''}
              </div>
              ${app.override_reason ? `<div class="small text-secondary fst-italic mt-1">📌 Recruiter Note: ${safeEscape(app.override_reason)}</div>` : ''}
            </td>
            <td class="py-3">${atsBadge}</td>
            <td class="py-3">${statusBadgeHtml}</td>
            <td class="py-3 small text-muted">${appliedDate}</td>
            <td class="text-end pe-3 py-3">${actionBtn}</td>
          </tr>
        `;
      }).join("");

      container.innerHTML = `
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="bg-light fs-7 text-uppercase text-secondary">
              <tr>
                <th class="ps-3 py-2.5">Job Title &amp; Company</th>
                <th class="py-2.5">ATS Match</th>
                <th class="py-2.5">Recruiter Status</th>
                <th class="py-2.5">Applied Date</th>
                <th class="text-end pe-3 py-2.5">Action</th>
              </tr>
            </thead>
            <tbody>
              ${rowsHtml}
            </tbody>
          </table>
        </div>
      `;

      container.querySelectorAll(".msg-rec-btn").forEach(btn => {
        btn.addEventListener("click", () => {
          if (window.openChatWithUser) {
            window.openChatWithUser();
          } else {
            window.location.href = "messages.html";
          }
        });
      });

    } catch (err) {
      container.innerHTML = `<div class="alert alert-danger py-2 small mb-0">Could not load applications: ${err.message}</div>`;
    }
  }

  const refreshVoiceBtn = document.getElementById("btn-refresh-voice-interviews");
  if (refreshVoiceBtn) {
    refreshVoiceBtn.addEventListener("click", loadCandidateVoiceInterviews);
  }

  const btnRefreshApps = document.getElementById("btn-refresh-my-apps");
  if (btnRefreshApps) {
    btnRefreshApps.addEventListener("click", async () => {
      btnRefreshApps.disabled = true;
      btnRefreshApps.innerHTML = `<span class="spinner-border spinner-border-sm" role="status"></span> Refreshing…`;
      await loadCandidateApplications();
      await load();
      btnRefreshApps.disabled = false;
      btnRefreshApps.innerHTML = `🔄 Refresh Status`;
    });
  }

  // --- WEEKLY PLACEMENT ARENA LOGIC ---
  async function loadWeeklyArena() {
    try {
      if (!api.weekly) return;
      const res = await api.weekly.getOverview();
      const data = res?.data;
      if (!data) return;

      const weekBadge = document.getElementById("weekly-week-badge");
      if (weekBadge) weekBadge.textContent = data.week_label || data.current_week_code;

      // Aptitude Section
      const apt = data.aptitude;
      if (apt) {
        const aptTitle = document.getElementById("dash-weekly-apt-title");
        if (aptTitle && apt.title) aptTitle.textContent = apt.title;
        const aptDuration = document.getElementById("dash-weekly-apt-duration");
        if (aptDuration) {
          const totalQ = apt.total_questions || 10;
          const mins = apt.duration_minutes || Math.max(1, Math.ceil((totalQ * 30) / 60));
          aptDuration.textContent = `⏱️ ${mins} Mins (30s/q)`;
        }
        const aptQCount = document.getElementById("dash-weekly-apt-qcount");
        if (aptQCount) {
          aptQCount.textContent = `📝 ${apt.total_questions || 10} Questions`;
        }

        const aptStatus = document.getElementById("dash-weekly-apt-status");
        const aptScore = document.getElementById("dash-weekly-apt-score");
        const aptBtn = document.getElementById("dash-weekly-apt-action-btn");

        if (apt.user_completed) {
          if (aptStatus) {
            aptStatus.className = `badge ${apt.user_passed ? 'bg-success' : 'bg-warning text-dark'} px-2.5 py-1.5 rounded-pill small`;
            aptStatus.textContent = apt.user_passed ? "✓ Passed" : "Needs Practice";
          }
          if (aptScore) {
            aptScore.innerHTML = `<span class="${apt.user_passed ? 'text-success' : 'text-warning'}">${apt.user_score_percentage}%</span> <span class="small text-white-50">(${apt.user_passed ? 'Passed 🎉' : 'Below Cutoff'})</span>`;
          }
          if (aptBtn) {
            aptBtn.innerHTML = `👁️ Review Solutions &amp; Explanations &rarr;`;
            aptBtn.href = "aptitude-test.html?mode=weekly&view=review";
          }
        } else {
          if (aptStatus) {
            aptStatus.className = "badge bg-secondary px-2.5 py-1.5 rounded-pill small";
            aptStatus.textContent = "Not Started";
          }
          if (aptScore) aptScore.textContent = "— (10 Questions)";
          if (aptBtn) {
            aptBtn.innerHTML = `🚀 Start Weekly Aptitude &rarr;`;
            aptBtn.href = "aptitude-test.html?mode=weekly";
          }
        }
      }

      // Coding Section
      const coding = data.coding;
      if (coding) {
        const codingTitle = document.getElementById("dash-weekly-coding-title");
        if (codingTitle && coding.title) codingTitle.textContent = coding.title;

        const codingStatus = document.getElementById("dash-weekly-coding-status");
        const codingScore = document.getElementById("dash-weekly-coding-score");
        const codingBtn = document.getElementById("dash-weekly-coding-action-btn");

        if (coding.user_completed) {
          if (codingStatus) {
            codingStatus.className = `badge ${coding.user_passed ? 'bg-success' : 'bg-warning text-dark'} px-2.5 py-1.5 rounded-pill small`;
            codingStatus.textContent = coding.user_passed ? "✓ Completed" : "Attempted";
          }
          if (codingScore) {
            codingScore.innerHTML = `<span class="${coding.user_passed ? 'text-success' : 'text-warning'}">${coding.user_score} / ${coding.total_score}</span> <span class="small text-white-50">(${coding.user_passed ? 'Passed 🎉' : 'Needs Practice'})</span>`;
          }
          if (codingBtn) {
            codingBtn.innerHTML = `👁️ Review Coding Submissions &rarr;`;
            codingBtn.href = "coding-assessment.html?mode=weekly&view=report";
          }
        } else {
          if (codingStatus) {
            codingStatus.className = "badge bg-secondary px-2.5 py-1.5 rounded-pill small";
            codingStatus.textContent = "Not Started";
          }
          if (codingScore) codingScore.textContent = "— (3 Problems)";
          if (codingBtn) {
            codingBtn.innerHTML = `🚀 Start Coding Challenge &rarr;`;
            codingBtn.href = "coding-assessment.html?mode=weekly";
          }
        }
      }

      // Schedule Badge
      const schedBadge = document.getElementById("weekly-schedule-badge");
      if (schedBadge && data.schedule) {
        const s = data.schedule;
        schedBadge.textContent = `🔄 Updated Weekly Once • Refreshes in ${s.days_remaining}d ${s.hours_remaining}h`;
        schedBadge.title = s.cadence || "Refreshes every Monday at 00:00 UTC";
      }

      // Programming Topics for Coding Practice Grid
      const codingGrid = document.getElementById("dash-programming-topics-grid");
      if (codingGrid) {
        try {
          let topics = [];
          if (api.weekly.getCodingTopics) {
            const cRes = await api.weekly.getCodingTopics();
            topics = cRes?.data || [];
          }
          if (!topics.length && data.coding_topics_summary) {
            topics = data.coding_topics_summary;
          }

          const counter = document.getElementById("dash-coding-topics-counter");
          if (counter) counter.textContent = `${topics.length} Core DSA Topics`;

          if (!topics.length) {
            codingGrid.innerHTML = `<div class="col-12 text-white-50 small text-center py-3">No programming topics found.</div>`;
          } else {
            codingGrid.innerHTML = topics.map(t => {
              const diffPills = Object.entries(t.difficulty_distribution || {})
                .map(([diff, cnt]) => {
                  const bg = diff.toLowerCase() === 'easy' ? 'bg-success' : diff.toLowerCase() === 'medium' ? 'bg-warning text-dark' : 'bg-danger';
                  return `<span class="badge ${bg} px-1.5 py-0.5 rounded-pill" style="font-size: 0.65rem;">${cnt} ${diff}</span>`;
                }).join(' ');

              const subBadges = (t.subtopics || []).slice(0, 3)
                .map(st => `<span class="badge bg-white bg-opacity-10 text-white-50 border border-white border-opacity-10 rounded-pill small" style="font-size: 0.68rem;">${escapeHtml(st)}</span>`)
                .join(' ');

              return `
              <div class="col-md-6 col-xl-4">
                <div class="p-3 rounded-3 h-100 d-flex flex-column justify-content-between" style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); transition: all 0.2s ease;">
                  <div>
                    <div class="d-flex justify-content-between align-items-start mb-2">
                      <div class="d-flex align-items-center gap-2">
                        <span class="fs-4">${t.icon || "💻"}</span>
                        <div>
                          <h6 class="fw-bold text-white mb-0" style="font-size: 0.92rem;">${escapeHtml(t.name)}</h6>
                          <span class="badge bg-light bg-opacity-10 text-white-50" style="font-size: 0.65rem;">${escapeHtml(t.category)}</span>
                        </div>
                      </div>
                      ${t.popular ? '<span class="badge bg-warning text-dark px-1.5 py-0.5 rounded-pill" style="font-size: 0.65rem;">🔥 High Yield</span>' : ''}
                    </div>
                    <p class="text-white-50 small mb-2" style="font-size: 0.78rem; line-height: 1.35; min-height: 32px;">${escapeHtml(t.description)}</p>
                    <div class="d-flex flex-wrap gap-1 mb-2">${subBadges}</div>
                    <div class="d-flex align-items-center gap-1.5 mb-2">${diffPills}</div>
                  </div>
                  <div class="d-flex justify-content-between align-items-center pt-2 border-top border-white border-opacity-10 mt-auto">
                    <span class="text-white-50 small" style="font-size: 0.75rem;"><strong>${t.problem_count}</strong> Problems</span>
                    <a href="coding-assessment.html?mode=practice&topic=${encodeURIComponent(t.slug)}" class="btn btn-sm btn-outline-success rounded-pill px-2.5 py-1 fw-semibold text-nowrap" style="font-size: 0.75rem;">
                      Practice Topic &rarr;
                    </a>
                  </div>
                </div>
              </div>`;
            }).join('');
          }
        } catch (cErr) {
          console.warn("Failed to render programming topics grid:", cErr);
        }
      }

      // Aptitude Preparation Tracks Grid
      const aptGrid = document.getElementById("dash-aptitude-topics-grid");
      if (aptGrid) {
        try {
          let tracks = [];
          if (api.weekly.getAptitudeTopics) {
            const aRes = await api.weekly.getAptitudeTopics();
            tracks = aRes?.data || [];
          }
          if (!tracks.length && data.aptitude_topics_summary) {
            tracks = data.aptitude_topics_summary;
          }

          const aCounter = document.getElementById("dash-aptitude-topics-counter");
          if (aCounter) aCounter.textContent = `${tracks.length} Placement Tracks`;

          if (!tracks.length) {
            aptGrid.innerHTML = `<div class="col-12 text-white-50 small text-center py-3">No aptitude preparation tracks found.</div>`;
          } else {
            aptGrid.innerHTML = tracks.map(track => {
              const coBadges = (track.company_focus || []).slice(0, 4)
                .map(c => `<span class="badge bg-primary bg-opacity-25 text-info border border-info border-opacity-25 rounded-pill" style="font-size: 0.65rem;">${escapeHtml(c)}</span>`)
                .join(' ');

              const subBadges = (track.subtopics || []).slice(0, 3)
                .map(s => `<span class="badge bg-white bg-opacity-10 text-white-50 border border-white border-opacity-10 rounded-pill" style="font-size: 0.68rem;">${escapeHtml(s)}</span>`)
                .join(' ');

              const isCurrent = Boolean(track.is_current_week);
              return `
              <div class="col-md-6 col-xl-3">
                <div class="p-3 rounded-3 h-100 d-flex flex-column justify-content-between" style="background: ${isCurrent ? 'rgba(99, 102, 241, 0.12)' : 'rgba(255, 255, 255, 0.04)'}; border: ${isCurrent ? '1.5px solid #818cf8' : '1px solid rgba(255, 255, 255, 0.08)'}; transition: all 0.2s ease;">
                  <div>
                    ${isCurrent ? '<div class="badge bg-warning text-dark fw-bold mb-2 rounded-pill px-2 py-0.5" style="font-size: 0.65rem;">🔥 Active Weekly Focus</div>' : ''}
                    <div class="d-flex align-items-center gap-2 mb-2">
                      <span class="fs-4">${track.icon || "🧠"}</span>
                      <div>
                        <h6 class="fw-bold text-white mb-0" style="font-size: 0.92rem;">${escapeHtml(track.name)}</h6>
                        ${track.chapters ? `<span class="badge bg-white bg-opacity-10 text-info small" style="font-size: 0.62rem;">${escapeHtml(track.chapters)}</span>` : ''}
                      </div>
                    </div>
                    <p class="text-white-50 small mb-2" style="font-size: 0.78rem; line-height: 1.35; min-height: 40px;">${escapeHtml(track.description)}</p>
                    <div class="d-flex flex-wrap gap-1 mb-2">${subBadges}</div>
                    <div class="d-flex flex-wrap gap-1 mb-2">${coBadges}</div>
                  </div>
                  <div class="d-flex justify-content-between align-items-center pt-2 border-top border-white border-opacity-10 mt-auto">
                    <span class="text-white-50 small" style="font-size: 0.75rem;"><strong>${track.question_count || 10}+</strong> Questions</span>
                    <a href="aptitude-test.html?topic=${encodeURIComponent(track.slug)}" class="btn btn-sm ${isCurrent ? 'btn-primary' : 'btn-outline-primary'} rounded-pill px-2.5 py-1 fw-semibold text-nowrap" style="font-size: 0.75rem;">
                      Prepare Track &rarr;
                    </a>
                  </div>
                </div>
              </div>`;
            }).join('');
          }
        } catch (aErr) {
          console.warn("Failed to render aptitude tracks grid:", aErr);
        }
      }
    } catch (err) {
      console.warn("Weekly Arena load warning:", err);
    }
  }

  // Load Leaderboards
  async function loadWeeklyLeaderboard() {
    const aptTbody = document.getElementById("lb-apt-tbody");
    const codingTbody = document.getElementById("lb-coding-tbody");

    try {
      const [aptRes, codingRes] = await Promise.all([
        api.weekly.getAptitudeLeaderboard(),
        api.weekly.getCodingLeaderboard()
      ]);

      const renderEntries = (entries) => {
        if (!entries || !entries.length) {
          return `<tr><td colspan="5" class="text-center py-4 text-muted">No attempts recorded this week yet. Be the first to top the leaderboard!</td></tr>`;
        }
        return entries.map(e => {
          let rankBadge = `<span class="badge bg-light text-dark fw-bold border">${e.rank}</span>`;
          if (e.rank === 1) rankBadge = `<span class="badge bg-warning text-dark fw-bold">🥇 1st</span>`;
          else if (e.rank === 2) rankBadge = `<span class="badge bg-secondary-subtle text-dark fw-bold border">🥈 2nd</span>`;
          else if (e.rank === 3) rankBadge = `<span class="badge bg-danger-subtle text-danger fw-bold border">🥉 3rd</span>`;

          const mins = Math.floor(e.time_taken_seconds / 60);
          const secs = e.time_taken_seconds % 60;
          const timeStr = `${mins}m ${secs}s`;

          return `
            <tr class="${e.is_current_user ? 'table-primary fw-bold' : ''}">
              <td>${rankBadge}</td>
              <td>${escapeHtml(e.candidate_name)}</td>
              <td><span class="fw-bold ${e.is_passed ? 'text-success' : 'text-primary'}">${e.score}%</span></td>
              <td class="text-muted small">${timeStr}</td>
              <td><span class="badge ${e.is_passed ? 'bg-success' : 'bg-secondary'} small">${e.is_passed ? 'Passed' : 'Attempted'}</span></td>
            </tr>
          `;
        }).join("");
      };

      if (aptTbody) aptTbody.innerHTML = renderEntries(aptRes?.data?.entries);
      if (codingTbody) codingTbody.innerHTML = renderEntries(codingRes?.data?.entries);
    } catch (e) {
      if (aptTbody) aptTbody.innerHTML = `<tr><td colspan="5" class="text-danger py-3 text-center">Failed to load leaderboard.</td></tr>`;
      if (codingTbody) codingTbody.innerHTML = `<tr><td colspan="5" class="text-danger py-3 text-center">Failed to load leaderboard.</td></tr>`;
    }
  }

  // Load History
  async function loadWeeklyHistory() {
    const aptTbody = document.getElementById("hist-apt-tbody");
    const codingTbody = document.getElementById("hist-coding-tbody");

    try {
      const [aptRes, codingRes] = await Promise.all([
        api.weekly.getAptitudeHistory(),
        api.weekly.getCodingHistory()
      ]);

      const aptAttempts = aptRes?.data || [];
      if (aptTbody) {
        if (!aptAttempts.length) {
          aptTbody.innerHTML = `<tr><td colspan="6" class="text-center py-4 text-muted">No past weekly aptitude attempts yet.</td></tr>`;
        } else {
          aptTbody.innerHTML = aptAttempts.map(a => `
            <tr>
              <td><span class="badge bg-primary-subtle text-primary border">${escapeHtml(a.week_code)}</span></td>
              <td class="fw-semibold">${escapeHtml(a.title)}</td>
              <td><span class="fw-bold ${a.is_passed ? 'text-success' : 'text-danger'}">${a.score_percentage}%</span></td>
              <td>${a.correct_count} / ${a.total_questions}</td>
              <td class="text-muted small">${Math.floor(a.time_taken_seconds / 60)}m ${a.time_taken_seconds % 60}s</td>
              <td class="text-muted small">${a.created_at ? new Date(a.created_at).toLocaleDateString() : '—'}</td>
            </tr>
          `).join("");
        }
      }

      const codingAttempts = codingRes?.data || [];
      if (codingTbody) {
        if (!codingAttempts.length) {
          codingTbody.innerHTML = `<tr><td colspan="6" class="text-center py-4 text-muted">No past weekly coding attempts yet.</td></tr>`;
        } else {
          codingTbody.innerHTML = codingAttempts.map(c => `
            <tr>
              <td><span class="badge bg-success-subtle text-success border">${escapeHtml(c.week_code)}</span></td>
              <td class="fw-semibold">${escapeHtml(c.title)}</td>
              <td><span class="fw-bold ${c.passed ? 'text-success' : 'text-danger'}">${c.percentage}%</span></td>
              <td><span class="badge ${c.passed ? 'bg-success' : 'bg-secondary'}">${c.passed ? 'PASSED' : 'ATTEMPTED'}</span></td>
              <td class="text-muted small">${Math.floor(c.time_taken_seconds / 60)}m ${c.time_taken_seconds % 60}s</td>
              <td class="text-muted small">${c.created_at ? new Date(c.created_at).toLocaleDateString() : '—'}</td>
            </tr>
          `).join("");
        }
      }
    } catch (e) {
      if (aptTbody) aptTbody.innerHTML = `<tr><td colspan="6" class="text-danger py-3 text-center">Failed to load history.</td></tr>`;
      if (codingTbody) codingTbody.innerHTML = `<tr><td colspan="6" class="text-danger py-3 text-center">Failed to load history.</td></tr>`;
    }
  }

  const lbModalEl = document.getElementById("weeklyLeaderboardModal");
  if (lbModalEl) {
    lbModalEl.addEventListener("show.bs.modal", loadWeeklyLeaderboard);
  }

  const histModalEl = document.getElementById("weeklyHistoryModal");
  if (histModalEl) {
    histModalEl.addEventListener("show.bs.modal", loadWeeklyHistory);
  }

  // =========================================================================
  // CANDIDATE LEARNING JOURNEY DASHBOARD & STAGE-GATED ROADMAP (REFERENCE UI)
  // Handled modularly by js/candidate-learning-journey.js
  // =========================================================================
  function loadCandidateLearningJourney() {
    if (typeof window.loadCandidateLearningJourney === "function") {
      window.loadCandidateLearningJourney();
    }
  }

  // Load immediately on script execution
  loadCandidateLearningJourney();
  loadWeeklyArena();
  loadCandidateApplications();
  loadExplorerJobs();
  loadCandidateCodingAssessments();
  loadCandidateVoiceInterviews();
  loadCandidateScreeningStatus();

  document.addEventListener("ar:auth-ready", () => {
    load();
    loadCandidateLearningJourney();
    loadWeeklyArena();
    loadCandidateApplications();
    loadCandidateProfileData();
    loadExplorerJobs();
    loadCandidateCodingAssessments();
    loadCandidateVoiceInterviews();
    loadCandidateScreeningStatus();
  });

  // Auto-sync status updates every 10 seconds so recruiter selection/shortlisting displays immediately
  setInterval(() => {
    loadCandidateApplications();
  }, 10000);

  // Sync immediately when candidate returns to dashboard tab
  window.addEventListener("focus", () => {
    loadCandidateApplications();
    loadWeeklyArena();
    load();
  });
})();




