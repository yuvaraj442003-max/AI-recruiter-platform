/**
 * candidate-learning-journey.js — Interactive 90-Day Learning Roadmap & Candidate Dashboard
 * Matches the reference design with Stage-Gated Progression:
 * Beginner Level Foundations -> Advanced Core Skills -> Practical Projects -> Placement Interview Ready.
 * Displays dynamic progress percentages in all sections (Roadmap, Courses, Phases, Recommendations, Daily Plan).
 */

if (typeof window.escapeHtml !== "function") {
  window.escapeHtml = function (str) {
    if (str === null || str === undefined) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  };
}
var escapeHtml = window.escapeHtml;

(function () {
  let activeJourneyData = null;

  // Fallback Reference State (in case backend is temporarily unreachable)
  const FALLBACK_JOURNEY = {
    roadmap_title: "Your 90-Day Roadmap",
    active_phase_num: 1,
    active_phase_name: "Phase 1: Foundations",
    overall_progress_percent: 15.0,
    recommendations_progress_percent: 40.0,
    today_plan_progress_percent: 50.0,
    today_date: "Oct 28, 2026",
    next_step: {
      title: "Phase 1: Foundations (60% Completed)",
      guidance: "Strengthen your core concepts. Master beginner foundations first, then advance to Core Skills, Practical Projects, and Course Interview Prep.",
      target_phase: 1,
      action_url: "study-materials.html",
      action_label: "Continue Foundations →",
    },
    phases: [
      {
        id: "phase-1",
        phase_num: 1,
        name: "Phase 1: Foundations",
        date_range: "Oct 15 - Nov 06",
        subtitle: "Strengthen your core concepts",
        progress_percent: 60.0,
        status: "In Progress",
        is_locked: false,
        icon: "layers",
        level: "Beginner Level",
        topics_covered: ["Python & Java Fundamentals", "Variables & Control Structures", "Object-Oriented Programming", "Algorithmic Complexity Basics"],
        courses: [
          { name: "Python Fundamentals", progress_percent: 75.0, status: "In Progress" },
          { name: "Java & OOP Principles", progress_percent: 65.0, status: "In Progress" },
          { name: "Algorithmic Logic Basics", progress_percent: 50.0, status: "In Progress" },
          { name: "Quantitative Aptitude Basics", progress_percent: 50.0, status: "In Progress" },
        ],
        action_url: "study-materials.html",
        action_text: "Study Foundations",
      },
      {
        id: "phase-2",
        phase_num: 2,
        name: "Phase 2: Core Skills",
        date_range: "Nov 07 - Nov 29",
        subtitle: "Build and apply core technical skills",
        progress_percent: 0.0,
        status: "Upcoming",
        is_locked: true,
        icon: "code",
        level: "Advanced Level",
        topics_covered: ["Advanced Data Structures & Algorithms", "System Design Basics", "Database Concurrency & Indexing", "Operating Systems Architecture"],
        courses: [
          { name: "Data Structures & Algorithms", progress_percent: 0.0, status: "Upcoming" },
          { name: "System Design & Distributed Scalability", progress_percent: 0.0, status: "Upcoming" },
          { name: "Database Optimization & SQL", progress_percent: 0.0, status: "Upcoming" },
          { name: "Operating Systems & Concurrency", progress_percent: 0.0, status: "Upcoming" },
        ],
        action_url: "coding-assessment.html",
        action_text: "Core Skills Lab",
      },
      {
        id: "phase-3",
        phase_num: 3,
        name: "Phase 3: Advanced & Projects",
        date_range: "Nov 30 - Dec 22",
        subtitle: "Build real-world projects",
        progress_percent: 0.0,
        status: "Upcoming",
        is_locked: true,
        icon: "briefcase",
        level: "Practical Projects",
        topics_covered: ["Build a Chatbot with LLM (RAG)", "Distributed Cache System", "Full-Stack Recruitment Platform", "High-Throughput Kafka Pipeline"],
        courses: [
          { name: "Build a Chatbot with LLM (RAG)", progress_percent: 0.0, status: "Upcoming" },
          { name: "High-Throughput Kafka Stream Pipeline", progress_percent: 0.0, status: "Upcoming" },
          { name: "Distributed In-Memory Cache System", progress_percent: 0.0, status: "Upcoming" },
          { name: "Full-Stack AI Recruitment Workspace", progress_percent: 0.0, status: "Upcoming" },
        ],
        action_url: "coding-assessment.html?mode=projects",
        action_text: "Build Projects",
      },
      {
        id: "phase-4",
        phase_num: 4,
        name: "Phase 4: Placement Ready",
        date_range: "Dec 23 - Jan 13",
        subtitle: "Resume, interview prep & mock interviews",
        progress_percent: 0.0,
        status: "Upcoming",
        is_locked: true,
        icon: "trophy",
        level: "Placement Ready",
        topics_covered: ["Company Technical Interview Questions", "AI Proctored Mock Interviews", "30s Speed Aptitude Drills", "HR & Behavioral Articulation"],
        courses: [
          { name: "Top 12 Company Technical Interview Questions", progress_percent: 0.0, status: "Upcoming" },
          { name: "AI Proctored Live Mock Interview Simulator", progress_percent: 0.0, status: "Upcoming" },
          { name: "HR Behavioral & STAR Rounds", progress_percent: 0.0, status: "Upcoming" },
          { name: "Speed Aptitude Placement Assessments", progress_percent: 0.0, status: "Upcoming" },
        ],
        action_url: "interview.html",
        action_text: "Take Mock Interview",
      },
    ],
    recommendations: [
      {
        id: "rec-1",
        title: "Machine Learning Specialization",
        provider: "Coursera • Beginner",
        icon: "graduation-cap",
        progress_percent: 45.0,
        action_url: "study-materials.html",
      },
      {
        id: "rec-2",
        title: "Build a Chatbot with LLM",
        provider: "Project • Intermediate",
        icon: "code",
        progress_percent: 30.0,
        action_url: "coding-assessment.html?mode=project",
      },
      {
        id: "rec-3",
        title: "Data Structures & Algorithms",
        provider: "Course • Important",
        icon: "zap",
        progress_percent: 65.0,
        action_url: "study-materials.html",
      },
      {
        id: "rec-4",
        title: "System Design Basics",
        provider: "Course • Advanced",
        icon: "cpu",
        progress_percent: 20.0,
        action_url: "study-materials.html",
      },
    ],
    today_plan: [
      {
        id: "task-1",
        title: "Watch: Intro to Neural Networks",
        duration: "30 min",
        status: "Completed",
        progress_percent: 100.0,
        action_url: "study-materials.html",
      },
      {
        id: "task-2",
        title: "Practice: Python Functions",
        duration: "45 min",
        status: "In Progress",
        progress_percent: 50.0,
        action_url: "coding-assessment.html",
      },
      {
        id: "task-3",
        title: "Read: ML Lifecycle",
        duration: "20 min",
        status: "Pending",
        progress_percent: 0.0,
        action_url: "study-materials.html",
      },
    ],
    recent_progress: {
      courses_completed: 4,
      courses_delta: "+1 this week",
      projects_built: 2,
      projects_delta: "+1 this week",
      hours_learned: 18.5,
      hours_delta: "+4.5 this week",
      streak_days: 7,
    },
    strengths: ["Python", "Problem Solving", "Data Analysis"],
    focus_areas: ["Deep Learning", "System Design", "SQL"],
  };

  async function loadCandidateLearningJourney() {
    const container = document.getElementById("candidate-learning-journey-container");
    if (!container) return;

    try {
      if (typeof api !== "undefined" && api.studyMaterials && typeof api.studyMaterials.getLearningJourney === "function") {
        const res = await api.studyMaterials.getLearningJourney();
        activeJourneyData = (res && res.data) ? res.data : FALLBACK_JOURNEY;
      } else {
        activeJourneyData = FALLBACK_JOURNEY;
      }
      renderLearningJourneyDashboard(activeJourneyData);
    } catch (err) {
      console.warn("Could not load candidate learning journey from API, using fallback state", err);
      activeJourneyData = FALLBACK_JOURNEY;
      renderLearningJourneyDashboard(activeJourneyData);
    }
  }

  function renderLearningJourneyDashboard(data) {
    if (!data) return;

    // 1. Next Step Guidance Banner
    const nextStepTitle = document.getElementById("journey-next-step-title");
    const nextStepGuidance = document.getElementById("journey-next-step-guidance");
    if (nextStepTitle && data.next_step) {
      nextStepTitle.textContent = data.next_step.title;
    }
    if (nextStepGuidance && data.next_step) {
      nextStepGuidance.textContent = data.next_step.guidance;
    }

    // 2. CARD 1: Your 90-Day Roadmap Header Overall Badge & Timeline
    const overallBadge = document.getElementById("roadmap-overall-badge");
    if (overallBadge) {
      const overallPct = Math.round(data.overall_progress_percent !== undefined ? data.overall_progress_percent : 15);
      overallBadge.textContent = `${overallPct}% Total`;
    }

    const timelineContainer = document.getElementById("journey-roadmap-timeline");
    if (timelineContainer && data.phases) {
      timelineContainer.innerHTML = data.phases.map((p) => {
        const isCurrentActive = (data.active_phase_num === p.phase_num);
        const isCompleted = (p.status === "Completed" || p.progress_percent >= 100);

        let nodeClass = "";
        if (isCompleted) nodeClass = "completed";
        else if (isCurrentActive) nodeClass = "active";

        // Icons matching reference image
        let iconHtml = "";
        let iconBg = "#e6fcf5";

        if (p.phase_num === 1) {
          iconBg = "#e6fcf5";
          iconHtml = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>`;
        } else if (p.phase_num === 2) {
          iconBg = "#f3f0ff";
          iconHtml = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7950f2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>`;
        } else if (p.phase_num === 3) {
          iconBg = "#fff4e6";
          iconHtml = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>`;
        } else if (p.phase_num === 4) {
          iconBg = "#e7f5ff";
          iconHtml = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"></path><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"></path><path d="M4 22h16"></path><path d="M10 14.66V17c0 .55-.45 1-1 1H7c-.55 0-1 .45-1 1v1h12v-1c0-.55-.45-1-1-1h-2c-.55 0-1-.45-1-1v-2.34"></path><path d="M18 2H6v7a6 6 0 0 0 12 0V2z"></path></svg>`;
        }

        let statusBadge = "";
        if (isCompleted) {
          statusBadge = '<span class="roadmap-badge-completed">Completed</span>';
        } else if (isCurrentActive) {
          statusBadge = '<span class="roadmap-badge-in-progress">In Progress</span>';
        } else {
          statusBadge = '<span class="roadmap-badge-upcoming">Upcoming</span>';
        }

        const pct = Math.round(p.progress_percent || 0);
        const barColor = (isCompleted || isCurrentActive) && pct > 0 ? "#10b981" : "#e2e8f0";

        // Course Breakdown Pill summary
        const courses = p.courses || [];
        const coursesHtml = courses.length ? `
          <div class="d-flex flex-wrap gap-1.5 mt-1.5">
            ${courses.slice(0, 2).map(c => `
              <span class="badge bg-light text-secondary border px-1.5 py-0.5" style="font-size: 0.65rem; font-weight: 500;">
                ${escapeHtml(c.name)}: <b class="${c.progress_percent > 0 ? 'text-dark' : 'text-muted'}">${Math.round(c.progress_percent || 0)}%</b>
              </span>
            `).join('')}
            ${courses.length > 2 ? `<span class="badge bg-light text-muted border px-1.5 py-0.5" style="font-size: 0.65rem;">+${courses.length - 2} more</span>` : ''}
          </div>
        ` : '';

        return `
          <div class="roadmap-step" onclick="openStageGateModal(${p.phase_num})">
            <span class="roadmap-node ${nodeClass}" title="${escapeHtml(p.name)}"></span>
            
            <div class="d-flex align-items-start gap-2.5 flex-grow-1 me-2">
              <div class="roadmap-icon-box" style="background: ${iconBg};">
                ${iconHtml}
              </div>
              <div class="flex-grow-1">
                <div class="fw-bold text-dark" style="font-size: 0.88rem; line-height: 1.3;">${escapeHtml(p.name)}</div>
                <div class="text-muted" style="font-size: 0.72rem; margin-top: 1px;">${escapeHtml(p.date_range)}</div>
                <div class="text-secondary" style="font-size: 0.75rem; margin-top: 2px;">${escapeHtml(p.subtitle)}</div>
                ${coursesHtml}
              </div>
            </div>

            <div class="d-flex flex-column align-items-end flex-shrink-0" style="min-width: 82px;">
              <div class="mb-2">${statusBadge}</div>
              <div class="d-flex align-items-center gap-1.5 w-100 justify-content-end">
                <span class="fw-bold ${pct > 0 ? 'text-dark' : 'text-muted'}" style="font-size: 0.75rem;">${pct}%</span>
                <div class="roadmap-progress-bar-wrap">
                  <div class="roadmap-progress-fill" style="width: ${pct}%; background: ${barColor};"></div>
                </div>
              </div>
            </div>
          </div>
        `;
      }).join("");
    }

    // 3. CARD 2: Top Recommendations for You
    const recOverallBadge = document.getElementById("recommendations-overall-badge");
    if (recOverallBadge) {
      const recAvg = Math.round(data.recommendations_progress_percent !== undefined ? data.recommendations_progress_percent : 40);
      recOverallBadge.textContent = `${recAvg}% Avg Progress`;
    }

    const recsContainer = document.getElementById("journey-recommendations-list");
    if (recsContainer && data.recommendations) {
      recsContainer.innerHTML = data.recommendations.map(r => {
        let iconBg = "#e7f5ff";
        let iconSvg = "";

        if (r.icon === "graduation-cap") {
          iconBg = "#e7f5ff";
          iconSvg = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#228be6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"></path><path d="M6 12v5c3 3 9 3 12 0v-5"></path></svg>`;
        } else if (r.icon === "code") {
          iconBg = "#e6fcf5";
          iconSvg = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#12b886" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>`;
        } else if (r.icon === "zap") {
          iconBg = "#fff4e6";
          iconSvg = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>`;
        } else if (r.icon === "cpu") {
          iconBg = "#f3f0ff";
          iconSvg = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7950f2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line><line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line><line x1="20" y1="9" x2="23" y2="9"></line><line x1="20" y1="14" x2="23" y2="14"></line><line x1="1" y1="9" x2="4" y2="9"></line><line x1="1" y1="14" x2="4" y2="14"></line></svg>`;
        }

        const recPct = Math.round(r.progress_percent !== undefined ? r.progress_percent : 35);
        const barFillColor = recPct >= 60 ? "#10b981" : (recPct >= 30 ? "#3b82f6" : "#f59e0b");

        return `
          <div class="recommendation-row" onclick="handleRecommendationClick('${escapeHtml(r.action_url)}', '${escapeHtml(r.title)}')">
            <div class="d-flex align-items-center gap-2.5 flex-grow-1 me-2">
              <div class="recommendation-icon-box" style="background: ${iconBg};">
                ${iconSvg}
              </div>
              <div style="min-width: 0;">
                <div class="fw-bold text-dark text-truncate" style="font-size: 0.88rem; max-width: 170px;">${escapeHtml(r.title)}</div>
                <div class="text-muted" style="font-size: 0.74rem;">${escapeHtml(r.provider)}</div>
              </div>
            </div>

            <div class="d-flex align-items-center gap-2 flex-shrink-0">
              <div class="d-flex flex-column align-items-end" style="min-width: 64px;">
                <span class="fw-bold ${recPct > 0 ? 'text-dark' : 'text-muted'}" style="font-size: 0.74rem;">${recPct}%</span>
                <div class="roadmap-progress-bar-wrap" style="width: 58px; height: 5px;">
                  <div class="roadmap-progress-fill" style="width: ${recPct}%; background: ${barFillColor};"></div>
                </div>
              </div>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
            </div>
          </div>
        `;
      }).join("");
    }

    // 4. CARD 3: Today's Plan
    const todayDateEl = document.getElementById("journey-today-date");
    if (todayDateEl) {
      todayDateEl.textContent = data.today_date || new Date().toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
    }

    const todayPlanBadge = document.getElementById("today-plan-progress-badge");
    const todayPct = Math.round(data.today_plan_progress_percent !== undefined ? data.today_plan_progress_percent : 50);
    if (todayPlanBadge) {
      todayPlanBadge.textContent = `${todayPct}% Completed`;
    }

    const todayProgressBar = document.getElementById("today-plan-progress-bar");
    if (todayProgressBar) {
      todayProgressBar.style.width = `${todayPct}%`;
    }

    const planContainer = document.getElementById("journey-todays-plan-list");
    if (planContainer && data.today_plan) {
      planContainer.innerHTML = data.today_plan.map(t => {
        const isDone = (t.status === "Completed");
        const isInProgress = (t.status === "In Progress");

        let circleClass = "pending";
        let circleContent = "";
        let badgeHtml = "";
        let taskPct = isDone ? 100 : (isInProgress ? 50 : 0);
        if (t.progress_percent !== undefined) {
          taskPct = Math.round(t.progress_percent);
        }

        if (isDone) {
          circleClass = "completed";
          circleContent = "✓";
          badgeHtml = `
            <div class="d-flex align-items-center gap-1.5">
              <span class="fw-bold text-success" style="font-size: 0.74rem;">100%</span>
              <span class="today-badge-completed">Completed</span>
            </div>
          `;
        } else if (isInProgress) {
          circleClass = "in-progress";
          badgeHtml = `
            <div class="d-flex align-items-center gap-1.5">
              <span class="fw-bold text-primary" style="font-size: 0.74rem;">${taskPct}%</span>
              <span class="today-badge-in-progress">In Progress</span>
            </div>
          `;
        } else {
          circleClass = "pending";
          badgeHtml = `
            <div class="d-flex align-items-center gap-1.5">
              <span class="fw-bold text-muted" style="font-size: 0.74rem;">0%</span>
              <span class="today-badge-pending">Pending</span>
            </div>
          `;
        }

        return `
          <div class="today-task-row" onclick="toggleJourneyDailyTask('${escapeHtml(t.id)}')">
            <div class="d-flex align-items-center gap-2.5 flex-grow-1 me-2">
              <span class="today-circle ${circleClass}">
                ${circleContent}
              </span>
              <div>
                <div class="fw-semibold text-dark ${isDone ? 'today-task-completed-text text-decoration-line-through text-muted' : ''}" style="font-size: 0.88rem;">
                  ${escapeHtml(t.title)}
                </div>
                <div class="text-muted" style="font-size: 0.74rem;">${escapeHtml(t.duration)}</div>
              </div>
            </div>
            ${badgeHtml}
          </div>
        `;
      }).join("");
    }

    // 5. CARD 4: Recent Progress
    if (data.recent_progress) {
      const elCourses = document.getElementById("journey-stat-courses");
      const elProjects = document.getElementById("journey-stat-projects");
      const elHours = document.getElementById("journey-stat-hours");
      const elStreak = document.getElementById("journey-stat-streak");

      if (elCourses) elCourses.textContent = data.recent_progress.courses_completed;
      if (elProjects) elProjects.textContent = data.recent_progress.projects_built;
      if (elHours) elHours.textContent = data.recent_progress.hours_learned;
      if (elStreak) elStreak.textContent = data.recent_progress.streak_days;
    }

    // 6. CARD 5: Strengths & Focus Areas
    const strengthsContainer = document.getElementById("journey-strengths-pills");
    if (strengthsContainer && data.strengths) {
      strengthsContainer.innerHTML = data.strengths.map(s => `
        <span class="strength-pill">
          ${escapeHtml(s)}
        </span>
      `).join("");
    }

    const focusContainer = document.getElementById("journey-focus-areas-pills");
    if (focusContainer && data.focus_areas) {
      focusContainer.innerHTML = data.focus_areas.map(f => `
        <span 
          class="focus-pill" 
          onclick="openFocusAreaPractice('${escapeHtml(f)}')"
          title="Start targeted placement practice for ${escapeHtml(f)}"
        >
          ${escapeHtml(f)}
        </span>
      `).join("");
    }
  }

  window.handleRecommendationClick = function(url, title) {
    if (url) {
      window.location.href = url;
    } else {
      window.location.href = "study-materials.html";
    }
  };

  window.toggleJourneyDailyTask = async function(taskId) {
    try {
      if (typeof api !== "undefined" && api.studyMaterials && typeof api.studyMaterials.toggleDailyTask === "function") {
        const res = await api.studyMaterials.toggleDailyTask({ task_id: taskId });
        if (res && res.data && res.data.all_journey) {
          activeJourneyData = res.data.all_journey;
          renderLearningJourneyDashboard(activeJourneyData);
          return;
        }
      }
    } catch (err) {
      console.warn("Could not toggle task via API, updating client state", err);
    }

    // Client-side fallback update
    if (activeJourneyData && activeJourneyData.today_plan) {
      const t = activeJourneyData.today_plan.find(item => item.id === taskId);
      if (t) {
        if (t.status === "Completed") {
          t.status = "Pending";
          t.progress_percent = 0.0;
        } else if (t.status === "In Progress") {
          t.status = "Completed";
          t.progress_percent = 100.0;
          if (activeJourneyData.recent_progress) {
            activeJourneyData.recent_progress.hours_learned = +(activeJourneyData.recent_progress.hours_learned + 0.5).toFixed(1);
          }
        } else {
          t.status = "In Progress";
          t.progress_percent = 50.0;
        }
        // Recalculate daily plan percentage
        const taskProgSum = activeJourneyData.today_plan.reduce((sum, item) => sum + (item.progress_percent || 0), 0);
        activeJourneyData.today_plan_progress_percent = Math.round(taskProgSum / activeJourneyData.today_plan.length);
        renderLearningJourneyDashboard(activeJourneyData);
      }
    }
  };

  window.advanceActiveStageProgress = async function() {
    if (!activeJourneyData) await loadCandidateLearningJourney();
    const curPhase = activeJourneyData?.active_phase_num || 1;

    try {
      if (typeof api !== "undefined" && api.studyMaterials && typeof api.studyMaterials.advanceLearningPhase === "function") {
        const res = await api.studyMaterials.advanceLearningPhase({
          phase_num: curPhase,
          delta_percent: 20.0,
        });

        if (res && res.data && res.data.success === false) {
          alert(`🔒 Stage-Gate Rule: ${res.data.message}`);
          return;
        }

        if (res && res.data && res.data.all_journey) {
          activeJourneyData = res.data.all_journey;
          renderLearningJourneyDashboard(activeJourneyData);
          return;
        }
      }
    } catch (err) {
      console.warn("API advance failed, applying local simulation", err);
    }

    // Local simulation
    if (activeJourneyData && activeJourneyData.phases) {
      const p = activeJourneyData.phases[curPhase - 1];
      if (p) {
        p.progress_percent = Math.min(100, p.progress_percent + 20);
        if (p.courses) {
          p.courses.forEach(c => {
            c.progress_percent = Math.min(100, c.progress_percent + 20);
          });
        }
        if (p.progress_percent >= 100) {
          p.status = "Completed";
          if (curPhase < 4) {
            activeJourneyData.phases[curPhase].is_locked = false;
            activeJourneyData.phases[curPhase].status = "In Progress";
            activeJourneyData.active_phase_num = curPhase + 1;
          }
        }
        renderLearningJourneyDashboard(activeJourneyData);
      }
    }
  };

  window.completeCurrentStageGate = async function() {
    if (!activeJourneyData) await loadCandidateLearningJourney();
    const curPhase = activeJourneyData?.active_phase_num || 1;

    try {
      if (typeof api !== "undefined" && api.studyMaterials && typeof api.studyMaterials.advanceLearningPhase === "function") {
        const res = await api.studyMaterials.advanceLearningPhase({
          phase_num: curPhase,
          set_exact_percent: 100.0,
        });

        if (res && res.data && res.data.all_journey) {
          activeJourneyData = res.data.all_journey;
          renderLearningJourneyDashboard(activeJourneyData);
          alert(`🎉 Outstanding! Phase ${curPhase} completed and next level unlocked!`);
          return;
        }
      }
    } catch (err) {
      console.warn("API complete failed", err);
    }

    if (activeJourneyData && activeJourneyData.phases) {
      const p = activeJourneyData.phases[curPhase - 1];
      if (p) {
        p.progress_percent = 100;
        p.status = "Completed";
        if (p.courses) {
          p.courses.forEach(c => {
            c.progress_percent = 100;
            c.status = "Completed";
          });
        }
        if (curPhase < 4) {
          activeJourneyData.phases[curPhase].is_locked = false;
          activeJourneyData.phases[curPhase].status = "In Progress";
          activeJourneyData.active_phase_num = curPhase + 1;
        }
        renderLearningJourneyDashboard(activeJourneyData);
        alert(`🎉 Outstanding! Phase ${curPhase} completed and next level unlocked!`);
      }
    }
  };

  window.resetLearningDashboard = async function() {
    try {
      if (typeof api !== "undefined" && api.studyMaterials && typeof api.studyMaterials.resetLearningJourney === "function") {
        const res = await api.studyMaterials.resetLearningJourney();
        activeJourneyData = (res && res.data) ? res.data : FALLBACK_JOURNEY;
      } else {
        activeJourneyData = JSON.parse(JSON.stringify(FALLBACK_JOURNEY));
      }
      renderLearningJourneyDashboard(activeJourneyData);
    } catch (err) {
      console.warn("Reset failed", err);
      activeJourneyData = JSON.parse(JSON.stringify(FALLBACK_JOURNEY));
      renderLearningJourneyDashboard(activeJourneyData);
    }
  };

  window.openStageGateModal = function(phaseNum) {
    if (!activeJourneyData || !activeJourneyData.phases) return;
    const phase = activeJourneyData.phases.find(p => p.phase_num === phaseNum);
    if (!phase) return;

    const modalTitle = document.getElementById("stage-modal-title");
    const modalLevel = document.getElementById("stage-modal-level-badge");
    const modalBody = document.getElementById("stage-modal-body");
    const modalActions = document.getElementById("stage-modal-actions");
    const modalEl = document.getElementById("stageGateDetailModal");

    if (modalTitle) modalTitle.textContent = phase.name;
    if (modalLevel) modalLevel.textContent = `${phase.level} • ${phase.status}`;

    if (modalBody) {
      const isLocked = phase.is_locked;
      const pct = Math.round(phase.progress_percent || 0);
      const courses = phase.courses || [];

      modalBody.innerHTML = `
        <div class="p-3 rounded-3 mb-3" style="background: ${isLocked ? '#fff5f5' : '#f0fdf4'}; border: 1px solid ${isLocked ? '#ffc9c9' : '#bbf7d0'};">
          <div class="d-flex align-items-center gap-2 mb-1">
            <span class="fs-5">${isLocked ? '🔒' : '🔓'}</span>
            <strong class="${isLocked ? 'text-danger' : 'text-success'}">
              ${isLocked ? 'Prerequisite Stage Gate Enforced' : 'Stage Unlocked & Active'}
            </strong>
          </div>
          <div class="small text-secondary">
            ${isLocked 
              ? `You must complete Phase ${phaseNum - 1} to 100% before starting this stage. Strict stage gating guarantees solid foundations before advanced coursework and placement interview drills.`
              : `You are currently eligible to study and practice topics in this phase.`
            }
          </div>
        </div>

        <div class="mb-4">
          <div class="d-flex justify-content-between small fw-bold text-dark mb-1">
            <span>Overall Phase Completion Progress</span>
            <span>${pct}%</span>
          </div>
          <div class="progress" style="height: 8px; border-radius: 999px;">
            <div class="progress-bar ${pct >= 100 ? 'bg-success' : 'bg-primary'}" style="width: ${pct}%;"></div>
          </div>
        </div>

        <h6 class="fw-bold text-dark mb-2">Individual Courses in this Phase:</h6>
        <div class="d-flex flex-column gap-2 mb-4">
          ${courses.map(c => {
            const cPct = Math.round(c.progress_percent || 0);
            return `
              <div class="p-2.5 rounded-3 border bg-light d-flex align-items-center justify-content-between gap-3">
                <div class="flex-grow-1">
                  <div class="fw-semibold text-dark small mb-1">${escapeHtml(c.name)}</div>
                  <div class="progress" style="height: 5px; border-radius: 999px;">
                    <div class="progress-bar ${cPct >= 100 ? 'bg-success' : 'bg-primary'}" style="width: ${cPct}%;"></div>
                  </div>
                </div>
                <div class="d-flex align-items-center gap-2 flex-shrink-0">
                  <span class="fw-bold text-dark small">${cPct}%</span>
                  <span class="badge ${cPct >= 100 ? 'bg-success-subtle text-success' : (cPct > 0 ? 'bg-primary-subtle text-primary' : 'bg-secondary-subtle text-secondary')} rounded-pill" style="font-size: 0.68rem;">
                    ${cPct >= 100 ? 'Completed' : (cPct > 0 ? 'In Progress' : 'Upcoming')}
                  </span>
                </div>
              </div>
            `;
          }).join('')}
        </div>

        <h6 class="fw-bold text-dark mb-2">Curriculum Topics Covered in this Stage:</h6>
        <div class="d-flex flex-wrap gap-1.5 mb-3">
          ${(phase.topics_covered || []).map(t => `<span class="badge bg-light text-dark border px-2.5 py-1.5">${escapeHtml(t)}</span>`).join('')}
        </div>

        <div class="p-3 rounded-3 bg-light text-secondary small">
          <strong>Placement Preparation Rule:</strong> After completing Beginner and Advanced courses followed by real-world projects, students receive dedicated technical interview preparation, mock interview practice, and campus hiring assessments.
        </div>
      `;
    }

    if (modalActions) {
      modalActions.innerHTML = `
        ${!phase.is_locked ? `
          <a href="${phase.action_url || 'study-materials.html'}" class="btn btn-primary rounded-pill px-4 fw-bold">
            ${escapeHtml(phase.action_text || 'Start Learning')} &rarr;
          </a>
        ` : `
          <button type="button" class="btn btn-secondary rounded-pill px-4" disabled>
            🔒 Locked (Complete Phase ${phaseNum - 1} First)
          </button>
        `}
      `;
    }

    if (modalEl && typeof bootstrap !== "undefined") {
      bootstrap.Modal.getOrCreateInstance(modalEl).show();
    }
  };

  window.openFocusAreaPractice = function(topic) {
    window.location.href = `study-materials.html?topic=${encodeURIComponent(topic)}`;
  };

  // Expose global methods
  window.loadCandidateLearningJourney = loadCandidateLearningJourney;
  window.renderLearningJourneyDashboard = renderLearningJourneyDashboard;

  // Auto-init on load
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", loadCandidateLearningJourney);
  } else {
    loadCandidateLearningJourney();
  }

  document.addEventListener("ar:auth-ready", () => {
    loadCandidateLearningJourney();
  });
})();
