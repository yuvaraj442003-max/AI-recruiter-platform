/**
 * candidate-learning-journey.js — Interactive 90-Day Learning Roadmap & Candidate Dashboard
 * Supports Course Selection (Java Programming, Python Full Stack, DSA, Full-Stack Web Development)
 * with complete step-by-step guidance:
 * - Comprehensive chapter-by-chapter curriculum & study materials
 * - Practical coding exercises with starter code & test cases
 * - Real-world enterprise project blueprints (e.g. Spring Boot Microservices, Kafka, Redis)
 * - Campus placement training (Top company interview Q&A, speed aptitude, live AI mock interview)
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
  let cachedCurriculumData = {};

  const FALLBACK_JOURNEY = {
    roadmap_title: "Your 90-Day Roadmap — Java Programming",
    target_track: "Java Programming: Beginner to Placement Ready",
    selected_course: "java",
    course_track: {
      id: "java",
      name: "Java Programming",
      title: "Java Programming: Beginner to Placement Ready",
      icon: "☕",
      badge: "Most Popular for Placements",
      target_role: "Java Backend Developer / SDE-1 / Enterprise Engineer",
      description: "Complete step-by-step guidance from Java basics and JVM memory management to Collections, Concurrency, Spring Boot REST microservices, real-world projects, and campus placement interviews.",
    },
    available_courses: [
      { id: "java", name: "Java Programming", icon: "☕", badge: "Most Popular for Placements", is_selected: true },
      { id: "python", name: "Python Full-Stack", icon: "🐍", badge: "AI & Fast-Track", is_selected: false },
      { id: "dsa", name: "DSA Placement Mastery", icon: "⚡", badge: "Placement Essential", is_selected: false },
      { id: "web_dev", name: "Full-Stack Web Dev", icon: "🌐", badge: "High Demand", is_selected: false },
      { id: "ai_ml", name: "AI and Machine Learning", icon: "🤖", badge: "Future-Ready AI", is_selected: false },
      { id: "data_science", name: "Data Science", icon: "📊", badge: "High Salary Roles", is_selected: false },
      { id: "cloud_computing", name: "Cloud Computing", icon: "☁️", badge: "Cloud Architect Track", is_selected: false },
      { id: "aws", name: "AWS (Amazon Web Services)", icon: "🚀", badge: "Top Cloud Certification", is_selected: false },
      { id: "cybersecurity", name: "Cybersecurity", icon: "🛡️", badge: "High Demand Security", is_selected: false },
      { id: "devops", name: "DevOps", icon: "🔄", badge: "CI/CD & Kubernetes Mastery", is_selected: false },
      { id: "sql_db", name: "SQL & Database Management", icon: "🗄️", badge: "Core Placement Skill", is_selected: false },
      { id: "gen_ai", name: "Generative AI", icon: "✨", badge: "Cutting-Edge & High Salary", is_selected: false },
      { id: "deep_learning", name: "Deep Learning", icon: "🧠", badge: "Advanced AI & Research", is_selected: false },
      { id: "software_testing", name: "Software Testing & QA", icon: "🧪", badge: "QA Automation & SDET", is_selected: false },
    ],
    active_phase_num: 1,
    active_phase_name: "Phase 1: Foundations",
    overall_progress_percent: 0.0,
    recommendations_progress_percent: 0.0,
    today_plan_progress_percent: 0.0,
    today_date: new Date().toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }),
    next_step: {
      title: "Phase 1: Foundations (0% Completed)",
      guidance: "Welcome to Java Programming! Begin with beginner core concepts, variables, and JVM/runtime mechanics to build strong foundational competence.",
      target_phase: 1,
      action_url: "study-materials.html?subject=java",
      action_label: "Start Foundations →",
    },
    phases: [
      {
        id: "phase-1",
        phase_num: 1,
        name: "Phase 1: Foundations",
        date_range: "Day 1 - 22",
        subtitle: "Master Java syntax, JVM runtime & core OOP principles",
        progress_percent: 0.0,
        status: "In Progress",
        is_locked: false,
        icon: "layers",
        level: "Beginner Level",
        topics_covered: ["Java Syntax & Primitive Data Types", "JVM Architecture & Memory (Heap vs Stack)", "Flow Control, Loops & Arrays", "OOP Principles: Classes, Encapsulation & Inheritance"],
        courses: [
          { id: "java-101", name: "Java Syntax & Variables Mechanics", progress_percent: 0.0, status: "Not Started" },
          { id: "java-102", name: "JVM Architecture & Heap vs Stack", progress_percent: 0.0, status: "Not Started" },
          { id: "java-103", name: "Algorithmic Logic & Loops in Java", progress_percent: 0.0, status: "Not Started" },
          { id: "java-104", name: "Core OOP: Classes, Encapsulation & Polymorphism", progress_percent: 0.0, status: "Not Started" },
        ],
        action_url: "study-materials.html?subject=java",
        action_text: "Study Java Foundations",
      },
      {
        id: "phase-2",
        phase_num: 2,
        name: "Phase 2: Core Skills",
        date_range: "Day 23 - 45",
        subtitle: "Collections Framework, Concurrency & Modern Streams API",
        progress_percent: 0.0,
        status: "Upcoming",
        is_locked: true,
        icon: "code",
        level: "Advanced Level",
        topics_covered: ["Java Collections (ArrayList, HashMap, PriorityQueue)", "Exception Handling & Robust Architecture", "Multithreading, Concurrency & ExecutorService", "Java 8+ Streams API, Lambdas & JDBC"],
        courses: [
          { id: "java-201", name: "Java Collections Deep Dive & HashMap Internals", progress_percent: 0.0, status: "Upcoming" },
          { id: "java-202", name: "Multithreading, Locks & Thread Safety", progress_percent: 0.0, status: "Upcoming" },
          { id: "java-203", name: "Java 8+ Streams & Functional Programming", progress_percent: 0.0, status: "Upcoming" },
          { id: "java-204", name: "JDBC, SQL Queries & Database Transactions", progress_percent: 0.0, status: "Upcoming" },
        ],
        action_url: "coding-assessment.html?lang=java",
        action_text: "Core Java Coding Lab",
      },
      {
        id: "phase-3",
        phase_num: 3,
        name: "Phase 3: Advanced & Projects",
        date_range: "Day 46 - 68",
        subtitle: "Build production enterprise applications with Spring Boot",
        progress_percent: 0.0,
        status: "Upcoming",
        is_locked: true,
        icon: "briefcase",
        level: "Practical Projects",
        topics_covered: ["Spring Boot 3 RESTful Microservices", "Spring Data JPA & Hibernate ORM", "Distributed Caching with Redis", "High-Throughput Kafka Event Pipelines"],
        courses: [
          { id: "java-301", name: "Spring Boot RESTful Microservice Architecture", progress_percent: 0.0, status: "Upcoming" },
          { id: "java-302", name: "High-Throughput Kafka Message Pipeline", progress_percent: 0.0, status: "Upcoming" },
          { id: "java-303", name: "Distributed In-Memory Cache with Redis", progress_percent: 0.0, status: "Upcoming" },
          { id: "java-304", name: "Full-Stack AI Recruitment Portal in Java", progress_percent: 0.0, status: "Upcoming" },
        ],
        action_url: "coding-assessment.html?mode=projects&lang=java",
        action_text: "Build Java Projects",
      },
      {
        id: "phase-4",
        phase_num: 4,
        name: "Phase 4: Placement Ready",
        date_range: "Day 69 - 90",
        subtitle: "Company Java technical interview questions & AI mock interviews",
        progress_percent: 0.0,
        status: "Upcoming",
        is_locked: true,
        icon: "trophy",
        level: "Placement Ready",
        topics_covered: ["Top 50 Java Technical Interview Q&A (TCS, Infosys, Amazon)", "Java Concurrency & JVM Tuning Scenarios", "Speed Quantitative & Reasoning Drills", "Live AI Java Technical Mock Interview"],
        courses: [
          { id: "java-401", name: "Top 12 Company Java Technical Interview Questions", progress_percent: 0.0, status: "Upcoming" },
          { id: "java-402", name: "AI Proctored Live Java Mock Interview Simulator", progress_percent: 0.0, status: "Upcoming" },
          { id: "java-403", name: "HR Behavioral & STAR Scenario Practice", progress_percent: 0.0, status: "Upcoming" },
          { id: "java-404", name: "Company Speed Aptitude & Reasoning Drills", progress_percent: 0.0, status: "Upcoming" },
        ],
        action_url: "interview.html?track=java",
        action_text: "Take Java Mock Interview",
      },
    ],
    recommendations: [
      {
        id: "rec-j1",
        title: "Java Masterclass: Core to OOP",
        provider: "Curriculum • Beginner",
        icon: "graduation-cap",
        type: "course",
        category: "Beginner Level Course",
        progress_percent: 0.0,
        action_url: "study-materials.html?subject=java",
      },
      {
        id: "rec-j2",
        title: "Spring Boot RESTful Microservice",
        provider: "Project • Intermediate",
        icon: "code",
        type: "project",
        category: "Practical Project",
        progress_percent: 0.0,
        action_url: "coding-assessment.html?mode=project&lang=java",
      },
      {
        id: "rec-j3",
        title: "Java Collections & Concurrency",
        provider: "Course • Important",
        icon: "zap",
        type: "core",
        category: "Placement Essential",
        progress_percent: 0.0,
        action_url: "study-materials.html?subject=java",
      },
      {
        id: "rec-j4",
        title: "Java Low-Level System Design",
        provider: "Course • Advanced",
        icon: "cpu",
        type: "advanced",
        category: "Advanced Level",
        progress_percent: 0.0,
        action_url: "study-materials.html?subject=java",
      },
    ],
    today_plan: [
      {
        id: "task-j1",
        title: "Watch: JVM Memory Architecture (Heap vs Stack)",
        duration: "30 min",
        status: "Pending",
        progress_percent: 0.0,
        action_url: "study-materials.html?subject=java",
      },
      {
        id: "task-j2",
        title: "Practice: Java Arrays & Two-Pointer Mechanics",
        duration: "45 min",
        status: "Pending",
        progress_percent: 0.0,
        action_url: "coding-assessment.html?lang=java",
      },
      {
        id: "task-j3",
        title: "Read: OOP Principles & Encapsulation in Java",
        duration: "20 min",
        status: "Pending",
        progress_percent: 0.0,
        action_url: "study-materials.html?subject=java",
      },
    ],
    recent_progress: {
      courses_completed: 0,
      courses_delta: "0 completed",
      projects_built: 0,
      projects_delta: "0 built",
      hours_learned: 0.0,
      hours_delta: "Start today",
      streak_days: 1,
    },
    strengths: ["Logical Reasoning", "Problem Solving", "Basic Coding"],
    focus_areas: ["Java OOP", "Collections Framework", "Spring Boot", "JVM Concurrency"],
    completed_topics: [],
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

    // 0. Render Target Course Selector Header
    renderCourseTrackSelector(data);

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
      const overallPct = Math.round(data.overall_progress_percent !== undefined ? data.overall_progress_percent : 0);
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

        let iconBg = "#e6fcf5";
        let iconHtml = "";

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
      const recAvg = Math.round(data.recommendations_progress_percent !== undefined ? data.recommendations_progress_percent : 0);
      recOverallBadge.textContent = `${recAvg}% Avg Progress`;
    }

    const recsContainer = document.getElementById("journey-recommendations-list");
    if (recsContainer && data.recommendations) {
      recsContainer.innerHTML = data.recommendations.map(r => {
        let iconBg = "#e7f5ff";
        let iconSvg = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#228be6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"></path><path d="M6 12v5c3 3 9 3 12 0v-5"></path></svg>`;

        if (r.icon === "code" || r.type === "project") {
          iconBg = "#e6fcf5";
          iconSvg = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#12b886" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>`;
        } else if (r.icon === "zap") {
          iconBg = "#fff4e6";
          iconSvg = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>`;
        } else if (r.icon === "cpu") {
          iconBg = "#f3f0ff";
          iconSvg = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7950f2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line></svg>`;
        }

        const recPct = Math.round(r.progress_percent !== undefined ? r.progress_percent : 0);
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
    const todayPct = Math.round(data.today_plan_progress_percent !== undefined ? data.today_plan_progress_percent : 0);
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

  function renderCourseTrackSelector(data) {
    const track = data.course_track || {
      id: "java",
      name: "Java Programming",
      title: "Java Programming: Beginner to Placement Ready",
      icon: "☕",
      badge: "Most Popular for Placements",
      target_role: "Java Backend Developer / SDE-1",
      description: "Complete step-by-step guidance from basics and JVM memory management to Collections, Concurrency, Spring Boot REST microservices, real-world projects, and campus placement interviews.",
    };

    const elIcon = document.getElementById("active-course-icon");
    const elTitle = document.getElementById("active-course-title");
    const elDesc = document.getElementById("active-course-desc");
    const elBadge = document.getElementById("active-course-role-badge");

    if (elIcon) elIcon.textContent = track.icon || "☕";
    if (elTitle) elTitle.textContent = track.title || track.name;
    if (elDesc) elDesc.textContent = track.description;
    if (elBadge) elBadge.textContent = track.target_role || "Target Track";

    // Update Dropdown Items Active State with Custom Reference Layout & Search
    const dropdownMenu = document.getElementById("courseTrackDropdownList");
    if (dropdownMenu && data.available_courses) {
      const selectedId = data.selected_course || "java";
      dropdownMenu.innerHTML = `
        <li class="px-2 pb-2 pt-1 border-bottom border-light mb-2">
          <div class="d-flex align-items-center justify-content-between mb-1">
            <span class="dropdown-header text-uppercase fw-bold text-muted p-0" style="font-size: 0.74rem; letter-spacing: 0.8px;">CHOOSE TARGET COURSE TRACK</span>
            <span class="badge bg-light text-secondary rounded-pill border" style="font-size: 0.68rem;">${data.available_courses.length} Tracks</span>
          </div>
          <div class="input-group input-group-sm mt-1">
            <span class="input-group-text bg-white border-end-0 py-1 ps-2 pe-1 text-muted"><i class="bi bi-search" style="font-size: 0.75rem;"></i></span>
            <input type="text" class="form-control form-control-sm border-start-0 py-1 shadow-none" id="searchCourseTrackInput" placeholder="Search track or skill..." oninput="filterCourseTracks(this.value)" onclick="event.stopPropagation();" style="font-size: 0.8rem; background: #fff;">
          </div>
        </li>
        <div id="courseTrackOptionsList">
          ${data.available_courses.map(c => {
            const isSel = (c.id === selectedId);
            return `
              <li class="course-track-item" data-search="${escapeHtml(((c.name || '') + ' ' + (c.badge || '')).toLowerCase())}">
                <a class="dropdown-item ${isSel ? 'active' : ''}" 
                   href="#" 
                   onclick="switchCandidateCourse('${escapeHtml(c.id)}'); return false;">
                  <span class="course-icon">${escapeHtml(c.icon || '📚')}</span>
                  <div class="flex-grow-1">
                    <div class="course-title">${escapeHtml(c.name)}</div>
                    <small class="course-subtitle">${escapeHtml(c.badge || '')}</small>
                  </div>
                  ${isSel ? '<span class="ms-2 text-white small"><i class="bi bi-check2"></i></span>' : ''}
                </a>
              </li>
            `;
          }).join('')}
          <li id="courseTrackEmptyNotice" class="text-center py-3 text-muted small" style="display: none;">
            No tracks found matching your search.
          </li>
        </div>
      `;
    }
  }

  window.filterCourseTracks = function(query) {
    const q = (query || "").trim().toLowerCase();
    const items = document.querySelectorAll("#courseTrackOptionsList .course-track-item");
    let visibleCount = 0;
    items.forEach(item => {
      const text = item.getAttribute("data-search") || "";
      if (!q || text.includes(q)) {
        item.style.display = "";
        visibleCount++;
      } else {
        item.style.display = "none";
      }
    });
    const emptyNotice = document.getElementById("courseTrackEmptyNotice");
    if (emptyNotice) {
      emptyNotice.style.display = visibleCount === 0 ? "block" : "none";
    }
  };

  window.switchCandidateCourse = async function(courseId) {
    try {
      if (typeof api !== "undefined" && api.studyMaterials && typeof api.studyMaterials.selectCourseTrack === "function") {
        const res = await api.studyMaterials.selectCourseTrack({ course_id: courseId });
        if (res && res.data) {
          activeJourneyData = res.data;
          renderLearningJourneyDashboard(activeJourneyData);
          alert(`🎯 Successfully switched target course to ${activeJourneyData.course_track?.name || courseId}! Your 90-day roadmap, study materials, practical exercises, and interview prep are now personalized for this track.`);
          return;
        }
      }
    } catch (err) {
      console.warn("Could not switch course via API, updating locally", err);
    }

    if (activeJourneyData) {
      activeJourneyData.selected_course = courseId;
      renderLearningJourneyDashboard(activeJourneyData);
    }
  };

  window.openCourseCurriculumModal = async function() {
    const courseId = (activeJourneyData && activeJourneyData.selected_course) ? activeJourneyData.selected_course : "java";
    let curData = cachedCurriculumData[courseId];

    if (!curData) {
      try {
        if (typeof api !== "undefined" && api.studyMaterials && typeof api.studyMaterials.getCourseCurriculum === "function") {
          const res = await api.studyMaterials.getCourseCurriculum(courseId);
          if (res && res.data) {
            curData = res.data;
            cachedCurriculumData[courseId] = curData;
          }
        }
      } catch (err) {
        console.warn("Could not fetch curriculum details via API", err);
      }
    }

    renderCurriculumModalContent(curData, courseId);
    const modalEl = document.getElementById("courseCurriculumModal");
    if (modalEl && typeof bootstrap !== "undefined") {
      bootstrap.Modal.getOrCreateInstance(modalEl).show();
    }
  };

  function renderCurriculumModalContent(curData, courseId) {
    const modalTitle = document.getElementById("curriculum-modal-title");
    const modalRole = document.getElementById("curriculum-modal-role");
    const modalBody = document.getElementById("curriculum-modal-body");

    if (modalTitle) modalTitle.textContent = curData ? curData.course_title : "Course Learning Roadmap & Guidance";
    if (modalRole) modalRole.textContent = curData ? `${curData.target_role} • ${curData.chapters_count || 10} Comprehensive Modules` : "Placement Ready Track";

    if (!modalBody) return;

    const chapters = (curData && curData.chapters) ? curData.chapters : [];
    const exercises = (curData && curData.practical_exercises) ? curData.practical_exercises : (activeJourneyData?.practical_exercises || []);
    const projects = (curData && curData.real_world_projects) ? curData.real_world_projects : (activeJourneyData?.real_world_projects || []);
    const placement = (curData && curData.placement_training) ? curData.placement_training : (activeJourneyData?.placement_training || {});

    modalBody.innerHTML = `
      <!-- Navigation Tabs -->
      <ul class="nav nav-pills nav-fill mb-4 p-1.5 bg-light rounded-4 gap-1 border" id="curriculumTabs" role="tablist">
        <li class="nav-item" role="presentation">
          <button class="nav-link active rounded-pill fw-bold py-2" id="tab-curriculum-btn" data-bs-toggle="pill" data-bs-target="#tab-curriculum-pane" type="button" role="tab">
            📚 All Topics & Study Materials (${chapters.length})
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link rounded-pill fw-bold py-2" id="tab-exercises-btn" data-bs-toggle="pill" data-bs-target="#tab-exercises-pane" type="button" role="tab">
            💻 Practical Coding Exercises (${exercises.length})
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link rounded-pill fw-bold py-2" id="tab-projects-btn" data-bs-toggle="pill" data-bs-target="#tab-projects-pane" type="button" role="tab">
            🚀 Real-World Projects (${projects.length})
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link rounded-pill fw-bold py-2" id="tab-placement-btn" data-bs-toggle="pill" data-bs-target="#tab-placement-pane" type="button" role="tab">
            🎯 Campus Placement Training
          </button>
        </li>
      </ul>

      <!-- Tab Contents -->
      <div class="tab-content" id="curriculumTabContent">
        <!-- TAB 1: CURRICULUM CHAPTERS -->
        <div class="tab-pane fade show active" id="tab-curriculum-pane" role="tabpanel">
          <div class="alert alert-info border-0 rounded-3 mb-3 d-flex align-items-center gap-2 small">
            <span>💡</span>
            <div><strong>Step-by-Step Learning Guidance:</strong> Study each module in sequence. Complete the solved examples and quizzes to master beginner foundations and advanced principles.</div>
          </div>
          <div class="accordion accordion-flush border rounded-3 overflow-hidden shadow-sm" id="curriculumAccordion">
            ${chapters.map((ch, idx) => {
              const chNum = ch.chapter_num || (idx + 1);
              const topics = ch.topics || [];
              const sections = ch.sections || {};
              const concept = sections.concept || ch.key_takeaways || "";
              const examples = sections.solved_examples || [];

              return `
                <div class="accordion-item border-bottom">
                  <h2 class="accordion-header" id="heading-ch-${chNum}">
                    <button class="accordion-button ${idx === 0 ? '' : 'collapsed'} fw-bold text-dark py-3" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-ch-${chNum}">
                      <div class="d-flex align-items-center gap-2 flex-grow-1">
                        <span class="badge bg-primary text-white rounded-pill px-2.5 py-1">Module ${chNum}</span>
                        <span>${escapeHtml(ch.title)}</span>
                      </div>
                    </button>
                  </h2>
                  <div id="collapse-ch-${chNum}" class="accordion-collapse collapse ${idx === 0 ? 'show' : ''}" data-bs-parent="#curriculumAccordion">
                    <div class="accordion-body bg-light p-4">
                      <div class="mb-3">
                        <h6 class="fw-bold text-dark mb-1">Key Takeaways & Core Concepts:</h6>
                        <div class="small text-secondary" style="white-space: pre-line;">${escapeHtml(concept)}</div>
                      </div>

                      <h6 class="fw-bold text-dark mb-2">Detailed Syllabus Topics:</h6>
                      <ul class="list-group list-group-flush rounded-3 border mb-3 small">
                        ${topics.map((t, tIdx) => {
                          const topicId = `topic-${chNum}-${tIdx + 1}`;
                          const isDone = (activeJourneyData?.completed_topics || []).includes(topicId);
                          return `
                            <li class="list-group-item d-flex align-items-center justify-content-between py-2">
                              <span>${tIdx + 1}. ${escapeHtml(t)}</span>
                              <button class="btn btn-sm ${isDone ? 'btn-success' : 'btn-outline-primary'} rounded-pill py-0.5 px-2.5 fw-semibold" 
                                      style="font-size: 0.72rem;" 
                                      onclick="toggleTopicCompleted('${topicId}', 1)">
                                ${isDone ? '✓ Completed' : 'Mark Complete'}
                              </button>
                            </li>
                          `;
                        }).join('')}
                      </ul>

                      ${examples.length ? `
                        <h6 class="fw-bold text-dark mb-2">Step-by-Step Solved Coding Example:</h6>
                        <div class="p-3 bg-dark text-white rounded-3 small font-monospace overflow-auto mb-3" style="max-height: 220px;">
                          <pre class="mb-0 text-light" style="font-size: 0.82rem;">${escapeHtml(examples[0].code_or_math || '')}</pre>
                        </div>
                      ` : ''}

                      <div class="d-flex justify-content-end">
                        <a href="study-materials.html?subject=${encodeURIComponent(courseId)}" class="btn btn-sm btn-primary rounded-pill px-3 fw-bold">
                          Study Full Chapter Notes &rarr;
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        </div>

        <!-- TAB 2: PRACTICAL CODING EXERCISES -->
        <div class="tab-pane fade" id="tab-exercises-pane" role="tabpanel">
          <div class="d-flex flex-column gap-3">
            ${exercises.map((ex, idx) => `
              <div class="p-3.5 rounded-3 border bg-white shadow-sm hover-lift">
                <div class="d-flex justify-content-between align-items-start gap-2 mb-2">
                  <div>
                    <span class="badge bg-primary-subtle text-primary border rounded-pill px-2.5 py-0.5 small fw-bold">Exercise ${idx + 1}</span>
                    <span class="badge bg-light text-secondary border rounded-pill px-2.5 py-0.5 small">${escapeHtml(ex.difficulty)}</span>
                    <h6 class="fw-bold text-dark mb-0 mt-1">${escapeHtml(ex.title)}</h6>
                  </div>
                  <span class="text-muted small fw-medium">⏱️ ${escapeHtml(ex.expected_time || '25 mins')}</span>
                </div>
                <p class="text-secondary small mb-2">${escapeHtml(ex.description)}</p>
                <div class="p-2.5 bg-dark text-light rounded-3 font-monospace small mb-3" style="max-height: 120px; overflow-y: auto;">
                  <pre class="mb-0 text-success" style="font-size: 0.78rem;">${escapeHtml(ex.starter_code || '// Starter code available in coding lab')}</pre>
                </div>
                <div class="d-flex justify-content-between align-items-center">
                  <button class="btn btn-sm btn-outline-success rounded-pill px-3 fw-semibold" onclick="toggleTopicCompleted('${ex.id}', ${ex.phase || 2})">
                    ${(activeJourneyData?.completed_topics || []).includes(ex.id) ? '✓ Exercise Done' : 'Mark as Solved'}
                  </button>
                  <a href="${escapeHtml(ex.action_url || 'coding-assessment.html')}" class="btn btn-sm btn-primary rounded-pill px-3 fw-bold">
                    Run in Coding Lab &rarr;
                  </a>
                </div>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- TAB 3: REAL-WORLD PROJECTS -->
        <div class="tab-pane fade" id="tab-projects-pane" role="tabpanel">
          <div class="d-flex flex-column gap-3">
            ${projects.map((proj, idx) => `
              <div class="p-4 rounded-3 border bg-white shadow-sm">
                <div class="d-flex justify-content-between align-items-start gap-2 mb-2 flex-wrap">
                  <div>
                    <span class="badge bg-warning text-dark fw-bold rounded-pill px-2.5 py-0.5 small">${escapeHtml(proj.badge || 'Enterprise Project')}</span>
                    <span class="badge bg-secondary-subtle text-secondary rounded-pill px-2 py-0.5 small">Phase ${proj.phase || 3}</span>
                    <h5 class="fw-bold text-dark mb-1 mt-1.5">${escapeHtml(proj.title)}</h5>
                  </div>
                  <a href="${escapeHtml(proj.action_url || 'coding-assessment.html?mode=projects')}" class="btn btn-sm btn-primary rounded-pill px-3 fw-bold">
                    Build Project &rarr;
                  </a>
                </div>
                <p class="text-secondary small mb-3">${escapeHtml(proj.description)}</p>
                <div class="p-3 bg-light rounded-3 border mb-3">
                  <div class="fw-bold text-dark small mb-1">Architecture & Tech Stack:</div>
                  <div class="d-flex flex-wrap gap-1.5 mb-2">
                    ${(proj.tech_stack || []).map(t => `<span class="badge bg-white text-dark border px-2 py-1">${escapeHtml(t)}</span>`).join('')}
                  </div>
                  <div class="text-muted small">${escapeHtml(proj.architecture || '')}</div>
                </div>
                <h6 class="fw-bold text-dark small mb-1.5">Production Features:</h6>
                <ul class="text-secondary small ps-3 mb-0">
                  ${(proj.key_features || []).map(f => `<li>${escapeHtml(f)}</li>`).join('')}
                </ul>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- TAB 4: CAMPUS PLACEMENT TRAINING -->
        <div class="tab-pane fade" id="tab-placement-pane" role="tabpanel">
          <div class="p-3.5 rounded-3 border bg-gradient shadow-sm mb-4" style="background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%); color: #ffffff;">
            <div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
              <div>
                <span class="badge bg-warning text-dark fw-bold px-2.5 py-0.5 rounded-pill small mb-1">Placement Accelerator</span>
                <h5 class="fw-bold text-white mb-1">AI Proctored Live Mock Interview Simulator</h5>
                <p class="text-white-50 small mb-0">Practice speaking and coding in a timed, proctored campus placement round with real-time AI feedback.</p>
              </div>
              <a href="interview.html?track=${encodeURIComponent(courseId)}" class="btn btn-light rounded-pill px-4 py-2 fw-bold text-primary shadow-sm">
                Launch Live Mock Interview &rarr;
              </a>
            </div>
          </div>

          <h6 class="fw-bold text-dark mb-3">Frequently Asked Placement Interview Questions:</h6>
          <div class="accordion accordion-flush border rounded-3 overflow-hidden shadow-sm mb-4" id="placementQuestionsAccordion">
            ${(placement.top_interview_questions || []).map((qItem, idx) => `
              <div class="accordion-item border-bottom">
                <h2 class="accordion-header" id="heading-pq-${idx}">
                  <button class="accordion-button ${idx === 0 ? '' : 'collapsed'} fw-bold text-dark py-3" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-pq-${idx}">
                    <div class="d-flex align-items-center gap-2 flex-grow-1 me-2">
                      <span class="badge bg-light text-primary border rounded-pill px-2.5 py-1 small">${escapeHtml(qItem.company || 'Placement Drive')}</span>
                      <span>${escapeHtml(qItem.q)}</span>
                    </div>
                  </button>
                </h2>
                <div id="collapse-pq-${idx}" class="accordion-collapse collapse ${idx === 0 ? 'show' : ''}" data-bs-parent="#placementQuestionsAccordion">
                  <div class="accordion-body bg-light p-3.5 small text-secondary">
                    <strong class="text-dark d-block mb-1">Model Placement Answer:</strong>
                    ${escapeHtml(qItem.a)}
                  </div>
                </div>
              </div>
            `).join('')}
          </div>

          <h6 class="fw-bold text-dark mb-2">Speed Placement Aptitude Drills:</h6>
          <div class="row g-3">
            ${(placement.speed_aptitude_drills || []).map(drill => `
              <div class="col-12 col-md-6">
                <div class="p-3 rounded-3 border bg-light h-100 d-flex flex-column justify-content-between">
                  <div>
                    <div class="fw-bold text-dark small">${escapeHtml(drill.title)}</div>
                    <div class="text-muted small mt-1">${escapeHtml(drill.topics)}</div>
                  </div>
                  <div class="mt-2.5 d-flex justify-content-between align-items-center">
                    <span class="badge bg-white text-secondary border">${drill.questions_count || 20} Questions</span>
                    <a href="${escapeHtml(drill.action_url || 'study-materials.html?topic=aptitude')}" class="btn btn-sm btn-outline-primary rounded-pill px-2.5 fw-semibold">
                      Start Drill &rarr;
                    </a>
                  </div>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      </div>
    `;
  }

  window.toggleTopicCompleted = async function(topicId, phaseNum) {
    try {
      if (typeof api !== "undefined" && api.studyMaterials && typeof api.studyMaterials.completeTopic === "function") {
        const res = await api.studyMaterials.completeTopic({ topic_id: topicId, phase_num: phaseNum || 1 });
        if (res && res.data && res.data.all_journey) {
          activeJourneyData = res.data.all_journey;
          renderLearningJourneyDashboard(activeJourneyData);
          return;
        }
      }
    } catch (err) {
      console.warn("Could not toggle topic completion via API, updating locally", err);
    }

    if (activeJourneyData) {
      if (!activeJourneyData.completed_topics) activeJourneyData.completed_topics = [];
      const idx = activeJourneyData.completed_topics.indexOf(topicId);
      if (idx >= 0) activeJourneyData.completed_topics.splice(idx, 1);
      else activeJourneyData.completed_topics.push(topicId);
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
          <button type="button" class="btn btn-outline-primary rounded-pill px-3 fw-bold" onclick="openCourseCurriculumModal()">
            📖 Full Curriculum & Exercises
          </button>
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

    if (activeJourneyData && activeJourneyData.today_plan) {
      const t = activeJourneyData.today_plan.find(item => item.id === taskId);
      if (t) {
        if (t.status === "Completed") {
          t.status = "Pending";
          t.progress_percent = 0.0;
        } else if (t.status === "In Progress") {
          t.status = "Completed";
          t.progress_percent = 100.0;
        } else {
          t.status = "In Progress";
          t.progress_percent = 50.0;
        }
        renderLearningJourneyDashboard(activeJourneyData);
      }
    }
  };

  window.advanceActiveStageProgress = async function() {
    if (!activeJourneyData) return;
    const curPhase = activeJourneyData.active_phase_num || 1;
    try {
      if (typeof api !== "undefined" && api.studyMaterials && typeof api.studyMaterials.advanceLearningPhase === "function") {
        const res = await api.studyMaterials.advanceLearningPhase({ phase_num: curPhase, delta_percent: 20.0 });
        if (res && res.data && res.data.all_journey) {
          activeJourneyData = res.data.all_journey;
          renderLearningJourneyDashboard(activeJourneyData);
          return;
        }
      }
    } catch (err) {
      console.warn("API advance failed, updating client fallback", err);
    }

    if (activeJourneyData && activeJourneyData.phases) {
      const p = activeJourneyData.phases.find(item => item.phase_num === curPhase);
      if (p) {
        p.progress_percent = Math.min(100.0, (p.progress_percent || 0) + 20.0);
        if (p.progress_percent >= 100.0) {
          p.status = "Completed";
          const nextP = activeJourneyData.phases.find(item => item.phase_num === curPhase + 1);
          if (nextP) {
            nextP.is_locked = false;
            nextP.status = "In Progress";
            activeJourneyData.active_phase_num = nextP.phase_num;
            activeJourneyData.active_phase_name = nextP.name;
          }
        }
        renderLearningJourneyDashboard(activeJourneyData);
      }
    }
  };

  window.completeCurrentStageGate = async function() {
    if (!activeJourneyData) return;
    const curPhase = activeJourneyData.active_phase_num || 1;
    try {
      if (typeof api !== "undefined" && api.studyMaterials && typeof api.studyMaterials.advanceLearningPhase === "function") {
        const res = await api.studyMaterials.advanceLearningPhase({ phase_num: curPhase, set_exact_percent: 100.0 });
        if (res && res.data && res.data.all_journey) {
          activeJourneyData = res.data.all_journey;
          renderLearningJourneyDashboard(activeJourneyData);
          alert(`🎉 Outstanding! Phase ${curPhase} completed and next level unlocked!`);
          return;
        }
      }
    } catch (err) {
      console.warn("Stage gate unlock API failed", err);
    }

    if (activeJourneyData && activeJourneyData.phases) {
      const p = activeJourneyData.phases.find(item => item.phase_num === curPhase);
      if (p) {
        p.progress_percent = 100.0;
        p.status = "Completed";
        const nextP = activeJourneyData.phases.find(item => item.phase_num === curPhase + 1);
        if (nextP) {
          nextP.is_locked = false;
          nextP.status = "In Progress";
          activeJourneyData.active_phase_num = nextP.phase_num;
          activeJourneyData.active_phase_name = nextP.name;
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
