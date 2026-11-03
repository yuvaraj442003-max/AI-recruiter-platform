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
  let currentCourseCurriculum = null;
  let currentAllTopicsList = [];
  let currentLearningModuleIdx = 0;
  let currentLearningTopicIdx = 0;

  const COURSE_PROJECT_BADGES = {
    java: "(Spring Boot & Microservices)",
    python: "(FastAPI & Microservices)",
    dsa: "(System Design & High-Throughput Engines)",
    web_dev: "(Full-Stack React & Node Cloud Systems)",
    ai_ml: "(End-to-End ML & Model Deployment)",
    data_science: "(ETL Pipelines & Real-Time Analytics)",
    cloud_computing: "(AWS Serverless Architecture)",
    aws: "(Cloud-Native Architecture & Terraform)",
    cybersecurity: "(Enterprise SIEM & Security Labs)",
    devops: "(CI/CD Pipelines, Docker & Kubernetes)",
    sql_db: "(High-Concurrency PostgreSQL & Sharding)",
    gen_ai: "(LLM Agents, RAG & Vector Databases)",
    deep_learning: "(PyTorch Neural Nets & Vision Models)",
    software_testing: "(Selenium, Playwright & SDET Automation)"
  };

  function computeClientPhaseDates(startDate) {
    const d = startDate ? new Date(startDate) : new Date();
    const addDays = (base, n) => {
      const res = new Date(base);
      res.setDate(res.getDate() + n);
      return res;
    };
    const fmt = (dt) => dt.toLocaleDateString("en-US", { month: "short", day: "2-digit" });
    const p1_start = d;
    const p1_end = addDays(d, 21);
    const p2_start = addDays(p1_end, 1);
    const p2_end = addDays(d, 44);
    const p3_start = addDays(p2_end, 1);
    const p3_end = addDays(d, 67);
    const p4_start = addDays(p3_end, 1);
    const p4_end = addDays(d, 89);
    return [
      `${fmt(p1_start)} - ${fmt(p1_end)}`,
      `${fmt(p2_start)} - ${fmt(p2_end)}`,
      `${fmt(p3_start)} - ${fmt(p3_end)}`,
      `${fmt(p4_start)} - ${fmt(p4_end)}`,
    ];
  }

  const initialDynamicSchedules = computeClientPhaseDates(new Date());

  const FALLBACK_JOURNEY = {
    roadmap_title: "Your 90-Day Roadmap — Java Programming",
    target_track: "Java Programming: Beginner to Placement Ready",
    selected_course: "java",
    is_started: false,
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
        date_range: "",
        subtitle: "Master Java syntax, JVM runtime & core OOP principles",
        progress_percent: 0.0,
        status: "Not Started",
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
        date_range: "",
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
        date_range: "",
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
        date_range: "",
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

    // Calibrate phase schedules ONLY when candidate has actually started the course
    const isCourseStarted = Boolean(
      data.is_started ||
      (data.completed_topics && data.completed_topics.length > 0) ||
      (data.overall_progress_percent && data.overall_progress_percent > 0)
    );
    if (isCourseStarted && data.phases && data.phases.length) {
      const startBase = data.course_started_at ? new Date(data.course_started_at) : new Date();
      const dynDates = computeClientPhaseDates(startBase);
      data.phases.forEach((p, idx) => {
        if (dynDates[idx]) {
          p.date_range = dynDates[idx];
        }
      });
    } else if (data.phases && data.phases.length) {
      // Course not started — clear dates so they don't show stale/fake dates
      data.phases.forEach((p) => {
        p.date_range = "";
        p.status = p.phase_num === 1 ? "Not Started" : "Locked";
        p.progress_percent = 0;
      });
    }

    // 0. Render Target Course Selector Header
    renderCourseTrackSelector(data);

    // 1. Next Step Guidance Banner
    const nextStepTitle = document.getElementById("journey-next-step-title");
    const nextStepGuidance = document.getElementById("journey-next-step-guidance");
    const courseName = (data.course_track && data.course_track.name) || data.selected_course || "your selected course";
    if (isCourseStarted) {
      if (nextStepTitle && data.next_step) nextStepTitle.textContent = data.next_step.title;
      if (nextStepGuidance && data.next_step) nextStepGuidance.textContent = data.next_step.guidance;
    } else {
      if (nextStepTitle) nextStepTitle.textContent = "Ready to Start? Your Journey Begins Now";
      if (nextStepGuidance) nextStepGuidance.textContent = `Click "Start Course" to begin ${escapeHtml(courseName)}. Your 90-day roadmap, progress, phase schedule, and study plan will be dynamically built from your first day of learning.`;
    }

    // 2. CARD 1: Your 90-Day Roadmap Header Overall Badge & Timeline
    const overview = data.schedule_overview || {};
    const expectedCompletionDate = overview.expected_completion_date || data.expected_completion_date || "Feb 01, 2027";
    const startDateText = isCourseStarted 
      ? (overview.start_date || (data.course_started_at ? new Date(data.course_started_at).toLocaleDateString("en-US", { month: "short", day: "2-digit", year: "numeric" }) : "Active Sprint"))
      : "Starts Day 1 on Click (Ready Today)";
    const overallPct = Math.round(data.overall_progress_percent !== undefined ? data.overall_progress_percent : 0);
    const completedCount = (data.completed_topics && data.completed_topics.length) || overview.completed_topics_count || 0;
    const totalTopicsCount = overview.total_topics || 50;
    const daysElapsed = overview.days_elapsed || 0;
    const daysRemaining = overview.days_remaining !== undefined ? overview.days_remaining : 90;
    const currentWeekNum = overview.current_week || 1;

    const overallBadge = document.getElementById("roadmap-overall-badge");
    if (overallBadge) {
      if (isCourseStarted) {
        overallBadge.textContent = `${overallPct}% Total • Day ${daysElapsed}/90`;
        overallBadge.style.background = "#dbeafe";
        overallBadge.style.color = "#1e40af";
      } else {
        overallBadge.textContent = "Not Started • 90-Day Sprint";
        overallBadge.style.background = "#fef3c7";
        overallBadge.style.color = "#92400e";
      }
    }

    const timelineContainer = document.getElementById("journey-roadmap-timeline");
    if (timelineContainer) {
      // 90-Day Schedule Overview Banner (Always visible for all candidates)
      const scheduleBannerHtml = `
        <div class="p-3 mb-3 rounded-4 shadow-sm" style="background: ${isCourseStarted ? 'linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%)' : 'linear-gradient(135deg, #f8faff 0%, #ffffff 100%)'}; border: 1px solid ${isCourseStarted ? '#86efac' : '#cbd5e1'};">
          <div class="d-flex align-items-center justify-content-between mb-2 flex-wrap gap-2">
            <div class="d-flex align-items-center gap-2">
              <span class="fs-5">${isCourseStarted ? '⚡' : '🚀'}</span>
              <div>
                <div class="fw-bold text-dark" style="font-size: 0.88rem; line-height: 1.2;">
                  ${isCourseStarted ? `Sprint Active: Day ${daysElapsed || 1} of 90 (Week ${currentWeekNum} of 12)` : 'Your 90-Day Placement Sprint Roadmap'}
                </div>
                <div class="text-secondary" style="font-size: 0.72rem;">
                  ${isCourseStarted ? `${daysRemaining} days remaining to your target completion` : 'Starts Day 1 when you click Start Course • Fully structured 12-week schedule'}
                </div>
              </div>
            </div>
            <span class="badge ${isCourseStarted ? 'bg-success text-white' : 'bg-warning text-dark'} rounded-pill px-2.5 py-1 fw-bold" style="font-size: 0.7rem;">
              ${isCourseStarted ? 'In Progress' : 'Not Started'}
            </span>
          </div>

          <!-- Calendar Dates Strip: Start Date & Target Completion Date -->
          <div class="row g-2 py-2 my-1 border-top border-bottom" style="border-color: rgba(0,0,0,0.06) !important; font-size: 0.76rem;">
            <div class="col-6">
              <div class="text-muted" style="font-size: 0.7rem;">📅 Journey Start Date:</div>
              <div class="fw-bold text-dark">${escapeHtml(startDateText)}</div>
            </div>
            <div class="col-6">
              <div class="text-muted" style="font-size: 0.7rem;">🎯 Expected Completion Date:</div>
              <div class="fw-bold" style="color: #059669;">${escapeHtml(expectedCompletionDate)}</div>
            </div>
          </div>

          <!-- Weekly Schedule Pace & Overall Progress -->
          <div class="d-flex align-items-center justify-content-between text-secondary mt-2 mb-1" style="font-size: 0.75rem;">
            <span><strong>Weekly Schedule:</strong> 12 Weeks (4 Stages)</span>
            <span><strong>Overall Progress:</strong> <b class="${overallPct > 0 ? 'text-primary' : 'text-dark'}">${overallPct}%</b> (${completedCount}/${totalTopicsCount} Topics)</span>
          </div>
          <div class="progress mb-2.5" style="height: 7px; border-radius: 999px; background: #e2e8f0;">
            <div class="progress-bar ${overallPct >= 100 ? 'bg-success' : 'bg-primary'}" role="progressbar" style="width: ${overallPct}%;" aria-valuenow="${overallPct}" aria-valuemin="0" aria-valuemax="100"></div>
          </div>

          <!-- 1-Click Action Button -->
          ${!isCourseStarted ? `
            <div class="d-flex align-items-center justify-content-between pt-1">
              <div class="text-muted" style="font-size: 0.73rem;">
                Click to begin your 90-day learning journey
              </div>
              <button class="btn btn-sm btn-primary rounded-pill px-3.5 py-1.5 fw-bold shadow-sm d-flex align-items-center gap-1.5" onclick="startCurrentCourse(event)">
                <span>▶ Start Course</span>
              </button>
            </div>
          ` : `
            <div class="d-flex align-items-center justify-content-between pt-1">
              <button class="btn btn-sm btn-link text-primary p-0 text-decoration-none fw-semibold" onclick="openFullRoadmapScheduleModal(event)" style="font-size: 0.75rem;">
                🗓️ View Weekly Calendar
              </button>
              <button class="btn btn-sm btn-outline-primary rounded-pill px-3 py-1 fw-bold d-flex align-items-center gap-1" onclick="startCurrentCourse(event)">
                <span>Continue Learning →</span>
              </button>
            </div>
          `}
        </div>
      `;

      // 4-Stage Roadmap Timeline (Visible for all candidates with dates and topics)
      const phasesHtml = (data.phases || []).map((p) => {
        const isCurrentActive = isCourseStarted && (data.active_phase_num === p.phase_num);
        const isCompleted = isCourseStarted && (p.status === "Completed" || p.progress_percent >= 100);

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
        if (!isCourseStarted) {
          if (p.phase_num === 1) {
            statusBadge = '<span class="badge bg-warning-subtle text-warning border border-warning-subtle rounded-pill" style="font-size: 0.68rem;">Ready to Start</span>';
          } else {
            statusBadge = '<span class="roadmap-badge-upcoming">Locked</span>';
          }
        } else if (isCompleted) {
          statusBadge = '<span class="roadmap-badge-completed">Completed</span>';
        } else if (isCurrentActive) {
          statusBadge = '<span class="roadmap-badge-in-progress">In Progress</span>';
        } else {
          statusBadge = '<span class="roadmap-badge-upcoming">Upcoming</span>';
        }

        const pct = isCourseStarted ? Math.round(p.progress_percent || 0) : 0;
        const barColor = (isCompleted || isCurrentActive) && pct > 0 ? "#10b981" : "#e2e8f0";

        const weeklyScheduleBadge = p.weekly_schedule ? `<span class="badge bg-light text-primary border me-1" style="font-size: 0.68rem; font-weight: 600;">${escapeHtml(p.weekly_schedule)}</span>` : '';
        const topicsCountBadge = p.expected_topics_count ? `<span class="badge bg-light text-secondary border" style="font-size: 0.68rem;">${p.expected_topics_count} Topics</span>` : '';

        const courses = p.courses || [];
        const coursesHtml = courses.length ? `
          <div class="d-flex flex-wrap gap-1.5 mt-1.5">
            ${courses.slice(0, 2).map(c => `
              <span class="badge bg-light text-secondary border px-1.5 py-0.5" style="font-size: 0.65rem; font-weight: 500;">
                ${escapeHtml(c.name)}: <b class="${c.progress_percent > 0 ? 'text-dark' : 'text-muted'}">${isCourseStarted ? Math.round(c.progress_percent || 0) : 0}%</b>
              </span>
            `).join('')}
            ${courses.length > 2 ? `<span class="badge bg-light text-muted border px-1.5 py-0.5" style="font-size: 0.65rem;">+${courses.length - 2} more</span>` : ''}
          </div>
        ` : '';

        return `
          <div class="roadmap-step" onclick="openStageGateModal(${p.phase_num})" style="cursor: pointer;" title="Click to view weekly schedule & topics">
            <span class="roadmap-node ${nodeClass}" title="${escapeHtml(p.name)}"></span>
            
            <div class="d-flex align-items-start gap-2.5 flex-grow-1 me-2">
              <div class="roadmap-icon-box" style="background: ${iconBg};">
                ${iconHtml}
              </div>
              <div class="flex-grow-1">
                <div class="d-flex align-items-center gap-1.5 flex-wrap">
                  <span class="fw-bold text-dark" style="font-size: 0.88rem; line-height: 1.3;">${escapeHtml(p.name)}</span>
                  ${weeklyScheduleBadge}
                  ${topicsCountBadge}
                </div>
                <div class="text-muted" style="font-size: 0.72rem; margin-top: 1px;">📅 ${escapeHtml(p.date_range || '90-Day Sprint')}</div>
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

      timelineContainer.innerHTML = scheduleBannerHtml + phasesHtml;
    }

    // 3. CARD 2: Top Recommendations for You
    const recOverallBadge = document.getElementById("recommendations-overall-badge");
    if (recOverallBadge) {
      if (isCourseStarted) {
        const recAvg = Math.round(data.recommendations_progress_percent !== undefined ? data.recommendations_progress_percent : 0);
        recOverallBadge.textContent = `${recAvg}% Avg Progress`;
        recOverallBadge.style.background = "#dbeafe";
        recOverallBadge.style.color = "#1e40af";
      } else {
        recOverallBadge.textContent = "Not Started";
        recOverallBadge.style.background = "#f1f5f9";
        recOverallBadge.style.color = "#64748b";
      }
    }

    const recsContainer = document.getElementById("journey-recommendations-list");
    if (recsContainer && !isCourseStarted) {
      recsContainer.innerHTML = `
        <div class="text-center py-3 text-muted" style="font-size: 0.82rem;">
          <span style="font-size: 1.2rem;">📚</span><br>
          Personalized recommendations will appear once you start the course.
        </div>
      `;
    } else if (recsContainer && data.recommendations) {
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
      // Only show the actual date once the candidate has started
      if (isCourseStarted) {
        todayDateEl.textContent = data.today_date || new Date().toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
      } else {
        todayDateEl.textContent = "—";
      }
    }

    const todayPlanBadge = document.getElementById("today-plan-progress-badge");
    const todayPct = isCourseStarted ? Math.round(data.today_plan_progress_percent !== undefined ? data.today_plan_progress_percent : 0) : 0;
    if (todayPlanBadge) {
      todayPlanBadge.textContent = isCourseStarted ? `${todayPct}% Completed` : "Not Started";
    }

    const todayProgressBar = document.getElementById("today-plan-progress-bar");
    if (todayProgressBar) {
      todayProgressBar.style.width = isCourseStarted ? `${todayPct}%` : "0%";
    }

    const planContainer = document.getElementById("journey-todays-plan-list");
    if (planContainer && !isCourseStarted) {
      planContainer.innerHTML = `
        <div class="text-center py-3 text-muted" style="font-size: 0.82rem;">
          <span style="font-size: 1.2rem;">📋</span><br>
          Your daily study plan will appear here once you start the course.
        </div>
      `;
    } else if (planContainer && data.today_plan) {
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

    // Dynamic Real-World Projects Badge for active course
    const selectedCourseKey = (track.id || data.selected_course || "java").toLowerCase();
    const elProjectsBadge = document.getElementById("active-course-projects-badge");
    if (elProjectsBadge) {
      elProjectsBadge.textContent = COURSE_PROJECT_BADGES[selectedCourseKey] || `(${track.name} Real-World Systems)`;
    }

    // Dynamic Href on Navigation Links
    const targetLearningUrl = (selectedCourseKey === "python") ? "python-course-learning.html" : `course-learning.html?course=${encodeURIComponent(selectedCourseKey)}`;
    const elHeaderStart = document.getElementById("btn-header-start-course");
    if (elHeaderStart) {
      elHeaderStart.href = targetLearningUrl;
    }
    const elJourneyStart = document.getElementById("btn-journey-start-course");
    if (elJourneyStart) {
      elJourneyStart.href = targetLearningUrl;
    }
    const elSyllabusLink = document.getElementById("btn-header-syllabus-link");
    if (elSyllabusLink) {
      elSyllabusLink.href = targetLearningUrl;
    }

    // Dynamic Start Course / Continue Learning Buttons
    const isStarted = Boolean(data.is_started || (data.overall_progress_percent && data.overall_progress_percent > 0) || (data.completed_topics && data.completed_topics.length > 0));
    const overallPct = Math.round(data.overall_progress_percent || 0);

    const btnHeaderStart = document.getElementById("btn-header-start-course");
    const btnHeaderStartText = document.getElementById("btn-header-start-text");
    const btnHeaderStartIcon = document.getElementById("btn-header-start-icon");
    if (btnHeaderStartText) {
      if (isStarted) {
        btnHeaderStartText.textContent = overallPct > 0 ? `Continue Learning (${overallPct}%)` : "Continue Learning";
        if (btnHeaderStartIcon) btnHeaderStartIcon.textContent = "🚀";
        if (btnHeaderStart) {
          btnHeaderStart.className = "btn btn-primary text-white fw-bold px-3.5 py-2 rounded-pill shadow-sm d-flex align-items-center gap-2";
        }
      } else {
        btnHeaderStartText.textContent = "Start Course";
        if (btnHeaderStartIcon) btnHeaderStartIcon.textContent = "▶️";
        if (btnHeaderStart) {
          btnHeaderStart.className = "btn btn-warning text-dark fw-bold px-3.5 py-2 rounded-pill shadow-sm d-flex align-items-center gap-2";
        }
      }
    }

    const btnJourneyStart = document.getElementById("btn-journey-start-course");
    const btnJourneyStartText = document.getElementById("btn-journey-start-text");
    const btnJourneyStartIcon = document.getElementById("btn-journey-start-icon");
    if (btnJourneyStartText) {
      if (isStarted) {
        btnJourneyStartText.textContent = overallPct > 0 ? `Continue Learning (${overallPct}%)` : "Continue Learning";
        if (btnJourneyStartIcon) btnJourneyStartIcon.textContent = "🚀";
      } else {
        btnJourneyStartText.textContent = "Start Course";
        if (btnJourneyStartIcon) btnJourneyStartIcon.textContent = "▶️";
      }
    }

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
    currentCourseCurriculum = null;
    currentAllTopicsList = [];
    currentLearningModuleIdx = 0;
    currentLearningTopicIdx = 0;

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
      const courseObj = (activeJourneyData.available_courses || []).find(c => c.id === courseId);
      if (courseObj) {
        activeJourneyData.course_track = {
          id: courseObj.id,
          name: courseObj.name,
          title: `${courseObj.name}: Beginner to Placement Ready`,
          icon: courseObj.icon || "📚",
          badge: courseObj.badge || "Placement Track",
          target_role: `${courseObj.name} Engineer / SDE-1`,
          description: `Complete step-by-step guidance from foundational syntax to real-world projects and placement interviews for ${courseObj.name}.`
        };
        activeJourneyData.roadmap_title = `Your 90-Day Roadmap — ${courseObj.name}`;
        activeJourneyData.target_track = `${courseObj.name}: Beginner to Placement Ready`;
        if (courseId === "python" && (!activeJourneyData.phases || !activeJourneyData.phases.length || (activeJourneyData.phases[0].subtitle && activeJourneyData.phases[0].subtitle.includes("Java")))) {
          const dynDates = computeClientPhaseDates(new Date());
          activeJourneyData.phases = [
            {
              id: "phase-1",
              phase_num: 1,
              name: "Phase 1: Foundations",
              date_range: dynDates[0],
              subtitle: "Master Python syntax, memory model & functional basics",
              progress_percent: 0.0,
              status: "In Progress",
              is_locked: false,
              icon: "layers",
              topics_covered: ["Python Syntax, Dynamic Typing & Memory", "List Comprehensions & Dictionaries", "Functions, Closures & Decorators", "Object-Oriented Python (Dunder Methods)"],
              courses: [
                { id: "py-101", name: "Python Syntax, Data Types & Scope", progress_percent: 0.0, status: "Not Started" },
                { id: "py-102", name: "List Comprehensions, Tuples & Sets", progress_percent: 0.0, status: "Not Started" },
                { id: "py-103", name: "Functions, Lambda & Decorators", progress_percent: 0.0, status: "Not Started" },
                { id: "py-104", name: "Object-Oriented Python & Magic Methods", progress_percent: 0.0, status: "Not Started" },
              ],
              action_url: "python-course-learning.html",
              action_text: "Study Python Foundations",
            },
            {
              id: "phase-2",
              phase_num: 2,
              name: "Phase 2: Core Skills",
              date_range: dynDates[1],
              subtitle: "Advanced Data Structures, Asyncio & FastAPI",
              progress_percent: 0.0,
              status: "Upcoming",
              is_locked: true,
              icon: "code",
              topics_covered: ["Python Generators & Memory Profiling", "Asyncio & High-Concurrency I/O", "FastAPI & Pydantic REST APIs", "SQLAlchemy ORM & Database Indexing"],
              courses: [
                { id: "py-201", name: "Advanced Python Data Structures & Algorithmic Patterns", progress_percent: 0.0, status: "Upcoming" },
                { id: "py-202", name: "Asynchronous Programming with Asyncio", progress_percent: 0.0, status: "Upcoming" },
                { id: "py-203", name: "FastAPI Production REST Architectures", progress_percent: 0.0, status: "Upcoming" },
                { id: "py-204", name: "PostgreSQL & SQLAlchemy Asynchronous Session", progress_percent: 0.0, status: "Upcoming" },
              ],
              action_url: "coding-assessment.html?lang=python",
              action_text: "Core Python Lab",
            },
            {
              id: "phase-3",
              phase_num: 3,
              name: "Phase 3: Advanced & Projects",
              date_range: dynDates[2],
              subtitle: "Build production AI agents and distributed backends",
              progress_percent: 0.0,
              status: "Upcoming",
              is_locked: true,
              icon: "briefcase",
              topics_covered: ["FastAPI Microservices Architecture", "Redis Asynchronous Caching & Rate Limiting", "Celery Task Queue & Distributed Workers", "LangChain & AI Agent Orchestration"],
              courses: [
                { id: "py-301", name: "Distributed Microservices with FastAPI & Docker", progress_percent: 0.0, status: "Upcoming" },
                { id: "py-302", name: "Asynchronous Redis & Celery Background Queues", progress_percent: 0.0, status: "Upcoming" },
                { id: "py-303", name: "Autonomous AI Agents with OpenAI & LangChain", progress_percent: 0.0, status: "Upcoming" },
              ],
              action_url: "coding-assessment.html?mode=projects",
              action_text: "Build Python Projects",
            },
            {
              id: "phase-4",
              phase_num: 4,
              name: "Phase 4: Placement Ready",
              date_range: dynDates[3],
              subtitle: "Python technical interview questions & AI mock interviews",
              progress_percent: 0.0,
              status: "Upcoming",
              is_locked: true,
              icon: "award",
              topics_covered: ["Top 50 Python Interview Coding Challenges", "GIL, Memory Management & Deep Internals", "REST API System Design for Python Engineers", "Full-Length Proctored AI Mock Placement Interviews"],
              courses: [
                { id: "py-401", name: "Placement Coding Patterns & GIL Deep Dive", progress_percent: 0.0, status: "Upcoming" },
                { id: "py-402", name: "AI Proctored Python Placement Mock Interview", progress_percent: 0.0, status: "Upcoming" },
              ],
              action_url: "interview.html?track=python",
              action_text: "Python Mock Interview",
            }
          ];
        }
        if (activeJourneyData.next_step) {
          activeJourneyData.next_step.title = "Phase 1: Foundations (0% Completed)";
          if (courseId === "python") {
            activeJourneyData.next_step.guidance = "Welcome to Python Full-Stack! Begin with core syntax, dynamic typing, data structures, and the Python memory model to build strong foundational competence.";
          } else if (courseId === "dsa") {
            activeJourneyData.next_step.guidance = "Welcome to DSA Placement Mastery! Begin with time & space algorithmic complexity, array patterns, and two-pointer techniques to build foundational problem-solving rigor.";
          } else if (courseId === "web_dev") {
            activeJourneyData.next_step.guidance = "Welcome to Full-Stack Web Development! Begin with semantic HTML5, modern CSS layout, and asynchronous JavaScript fundamentals.";
          } else {
            activeJourneyData.next_step.guidance = `Welcome to ${courseObj.name}! Begin with beginner core concepts, fundamentals, and architecture to build strong foundational competence.`;
          }
        }
      }
      renderLearningJourneyDashboard(activeJourneyData);
    }
  };


  // =========================================================================
  // STEP-BY-STEP TOPIC-BY-TOPIC INTERACTIVE LEARNING ENGINE
  // =========================================================================

  function buildAllTopicsList(curData) {
    currentAllTopicsList = [];
    if (!curData || !curData.chapters || !curData.chapters.length) return;
    curData.chapters.forEach((ch, mIdx) => {
      const chNum = ch.chapter_num || (mIdx + 1);
      const topics = (ch.topics && ch.topics.length) ? ch.topics : [ch.title];
      topics.forEach((t, tIdx) => {
        currentAllTopicsList.push({
          moduleIdx: mIdx,
          topicIdx: tIdx,
          chapter: ch,
          chapterNum: chNum,
          topicTitle: t,
          topicId: `topic-${chNum}-${tIdx + 1}`,
          stageNum: ch.progression_stage || (chNum <= 2 ? 1 : chNum <= 5 ? 2 : chNum <= 7 ? 3 : 4),
          stageBadge: ch.stage_badge || (chNum <= 2 ? 'Stage 1: Fundamentals' : chNum <= 5 ? 'Stage 2: Core Engineering' : chNum <= 7 ? 'Stage 3: Advanced Concepts' : 'Stage 4: Real-World Projects')
        });
      });
    });
  }

  window.startCurrentCourse = async function(e, stayOnPage) {
    if (e && e.preventDefault) e.preventDefault();
    const courseId = (activeJourneyData && activeJourneyData.selected_course) ? activeJourneyData.selected_course.toLowerCase().trim() : "java";

    const btn = (e && e.currentTarget) || (e && e.target);
    const origHtml = btn ? btn.innerHTML : "";
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = `<span class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span> Starting...`;
    }

    try {
      if (typeof api !== "undefined" && api.studyMaterials && typeof api.studyMaterials.startCourse === "function") {
        const res = await api.studyMaterials.startCourse({ course_id: courseId });
        if (res && res.data) {
          activeJourneyData = res.data;
        }
      }
    } catch (err) {
      console.warn("Could not start course via API:", err);
    }

    if (stayOnPage) {
      if (typeof loadCandidateLearningJourney === "function") {
        await loadCandidateLearningJourney();
      }
      return;
    }

    // Navigate to dedicated course learning studio
    if (courseId === "python") {
      window.location.href = "python-course-learning.html";
    } else {
      window.location.href = `course-learning.html?course=${encodeURIComponent(courseId)}`;
    }
  };

  window.openFullRoadmapScheduleModal = function(e) {
    if (e && e.preventDefault) e.preventDefault();
    openCourseCurriculumModal("schedule");
  };

  window.renderStepByStepTopic = function(moduleIdx, topicIdx) {
    currentLearningModuleIdx = moduleIdx;
    currentLearningTopicIdx = topicIdx;

    if (!currentCourseCurriculum || !currentCourseCurriculum.chapters) {
      const container = document.getElementById("step-topic-content-container");
      if (container) {
        container.innerHTML = `
          <div class="text-center py-5">
            <div class="fs-1 mb-2">📚</div>
            <h5 class="fw-bold text-dark">Course Curriculum Loading...</h5>
            <p class="text-muted small">Please wait while the structured learning curriculum is being retrieved.</p>
            <button class="btn btn-primary rounded-pill px-4 mt-2" onclick="startCurrentCourse()">Retry Loading</button>
          </div>
        `;
      }
      return;
    }

    if (!currentAllTopicsList || !currentAllTopicsList.length) {
      buildAllTopicsList(currentCourseCurriculum);
    }

    const curItem = currentAllTopicsList.find(x => x.moduleIdx === moduleIdx && x.topicIdx === topicIdx) || currentAllTopicsList[0];
    if (!curItem) return;

    const currentIndex = currentAllTopicsList.indexOf(curItem);
    const totalTopics = currentAllTopicsList.length;
    const completedList = activeJourneyData?.completed_topics || [];
    const isCompleted = completedList.includes(curItem.topicId);
    const completedCount = currentAllTopicsList.filter(x => completedList.includes(x.topicId)).length;
    const progressPct = totalTopics > 0 ? Math.round((completedCount / totalTopics) * 100) : 0;

    // Header metadata
    const courseTrack = activeJourneyData?.course_track || {};
    const elCourseIcon = document.getElementById("step-modal-course-icon");
    const elCourseTitle = document.getElementById("step-modal-course-title");
    const elStageBadge = document.getElementById("step-modal-stage-badge");
    const elModuleBadge = document.getElementById("step-modal-module-badge");
    const elTopicStatus = document.getElementById("step-modal-topic-status");
    const elProgressBar = document.getElementById("step-modal-progress-bar");
    const elNavIndicator = document.getElementById("step-modal-nav-indicator");

    if (elCourseIcon) elCourseIcon.textContent = courseTrack.icon || "📚";
    if (elCourseTitle) elCourseTitle.textContent = currentCourseCurriculum.course_title || courseTrack.title || "Course Track";
    if (elStageBadge) {
      elStageBadge.textContent = curItem.stageBadge;
      elStageBadge.className = `badge ${curItem.stageNum === 1 ? 'bg-success' : curItem.stageNum === 2 ? 'bg-primary' : curItem.stageNum === 3 ? 'bg-warning text-dark' : 'bg-danger'} text-white px-2.5 py-0.5 rounded-pill small fw-bold`;
    }
    if (elModuleBadge) {
      elModuleBadge.textContent = `Module ${curItem.chapterNum} of ${currentCourseCurriculum.chapters.length}`;
    }
    if (elTopicStatus) {
      if (isCompleted) {
        elTopicStatus.className = "badge bg-success text-white rounded-pill px-2.5 py-0.5 small";
        elTopicStatus.innerHTML = "✓ Topic Completed";
      } else {
        elTopicStatus.className = "badge bg-info text-dark rounded-pill px-2.5 py-0.5 small";
        elTopicStatus.innerHTML = "Topic In Progress";
      }
    }
    if (elProgressBar) {
      elProgressBar.style.width = `${Math.max(5, progressPct)}%`;
    }
    if (elNavIndicator) {
      elNavIndicator.textContent = `Topic ${currentIndex + 1} of ${totalTopics} (${progressPct}% Completed)`;
    }

    // Navigation buttons state
    const btnPrev = document.getElementById("btn-step-prev");
    if (btnPrev) {
      btnPrev.disabled = (currentIndex <= 0);
    }
    const btnNext = document.getElementById("btn-step-next");
    const btnNextText = document.getElementById("btn-step-next-text");
    if (btnNext && btnNextText) {
      if (currentIndex >= totalTopics - 1) {
        btnNextText.textContent = isCompleted ? "🎓 Completed Course" : "✓ Complete & Finish Course";
        btnNext.className = "btn btn-warning text-dark rounded-pill px-4 py-2 fw-bold shadow-sm d-flex align-items-center gap-2";
      } else if (isCompleted) {
        btnNextText.textContent = "Next Topic";
        btnNext.className = "btn btn-primary rounded-pill px-4 py-2 fw-bold shadow-sm d-flex align-items-center gap-2";
      } else {
        btnNextText.textContent = "✓ Complete & Next Topic";
        btnNext.className = "btn btn-success rounded-pill px-4 py-2 fw-bold shadow-sm d-flex align-items-center gap-2";
      }
    }

    // Render Lesson Content Viewport
    const container = document.getElementById("step-topic-content-container");
    if (container) {
      const ch = curItem.chapter;
      const realWorld = ch.real_world_application || {};
      const sections = ch.sections || {};
      const concept = sections.concept || ch.key_takeaways || "";
      const examples = sections.solved_examples || [];
      const example = examples.length > 0 ? examples[topicIdx % examples.length] : null;
      const practiceQuestions = sections.practice_questions || [];
      const question = practiceQuestions.length > 0 ? practiceQuestions[topicIdx % practiceQuestions.length] : null;

      container.innerHTML = `
        <!-- BREADCRUMB & TOPIC TITLE -->
        <div class="mb-4">
          <div class="d-flex align-items-center gap-2 text-muted small mb-2 flex-wrap">
            <span class="badge ${curItem.stageNum === 1 ? 'bg-success' : curItem.stageNum === 2 ? 'bg-primary' : curItem.stageNum === 3 ? 'bg-warning text-dark' : 'bg-danger'} text-white rounded-pill px-2.5 py-0.5" style="font-size: 0.7rem;">
              ${escapeHtml(curItem.stageBadge)}
            </span>
            <span>•</span>
            <span class="fw-semibold text-dark">Module ${curItem.chapterNum}: ${escapeHtml(ch.title)}</span>
            <span>•</span>
            <span class="badge bg-light text-secondary border">Topic ${curItem.topicIdx + 1} of ${(ch.topics || []).length}</span>
          </div>
          <h2 class="fw-bold text-dark mb-2" style="letter-spacing: -0.3px;">${escapeHtml(curItem.topicTitle)}</h2>
          <p class="text-secondary small mb-0" style="line-height: 1.6;">
            Study this concept systematically. We begin with core fundamentals, explain how top tech companies deploy it in real-world systems, examine working production code, and test your retention with an interactive practice question.
          </p>
        </div>

        <!-- 1. CORE FUNDAMENTALS & CONCEPTUAL FOUNDATION -->
        <div class="card border-0 shadow-sm p-4 mb-4 rounded-4" style="background: #ffffff; border-left: 5px solid #3b82f6 !important;">
          <div class="d-flex align-items-center justify-content-between mb-3 flex-wrap gap-2">
            <div class="d-flex align-items-center gap-2">
              <span class="fs-4">💡</span>
              <h5 class="fw-bold text-dark mb-0">1. Core Fundamentals &amp; Mechanics</h5>
            </div>
            <span class="badge bg-primary-subtle text-primary border border-primary-subtle rounded-pill px-2.5 py-1 small fw-semibold">Step 1: Theory &amp; Foundations</span>
          </div>
          <div class="text-dark small" style="line-height: 1.8; white-space: pre-line; font-size: 0.93rem;">
            ${escapeHtml(concept)}
          </div>
        </div>

        <!-- 2. REAL-TIME PROJECT APPLICATION: HOW & WHERE USED IN INDUSTRY -->
        <div class="card border-0 shadow-sm p-4 mb-4 rounded-4" style="background: #ffffff; border-left: 5px solid #10b981 !important;">
          <div class="d-flex align-items-center justify-content-between mb-3 flex-wrap gap-2">
            <div class="d-flex align-items-center gap-2">
              <span class="fs-4">🚀</span>
              <h5 class="fw-bold text-dark mb-0">2. Real-World Project Application (How &amp; Where Used in Real-Time Systems)</h5>
            </div>
            <span class="badge bg-success-subtle text-success border border-success-subtle rounded-pill px-3 py-1 fw-bold small">
              🏢 ${escapeHtml(realWorld.domain || 'Enterprise Software & Microservices')}
            </span>
          </div>
          <p class="text-secondary small mb-3">
            Practical industry insights: how senior software engineers design and leverage this concept in live customer-facing systems.
          </p>

          <div class="row g-3 mb-3">
            <div class="col-md-6">
              <div class="p-3 bg-light rounded-3 border h-100">
                <div class="d-flex align-items-center gap-1.5 text-primary fw-bold small mb-1.5">
                  <span>📍</span>
                  <span>Where Applied in Production:</span>
                </div>
                <div class="text-secondary small mb-2" style="line-height: 1.6;">
                  ${escapeHtml(realWorld.where_applied || 'Used throughout service layers, request pipelines, and high-throughput data processors.')}
                </div>
                <div class="text-muted small" style="font-size: 0.78rem;">
                  <strong>Leading Companies:</strong> ${escapeHtml(realWorld.companies || 'Amazon, Google, Netflix, Microsoft, TCS, Infosys')}
                </div>
              </div>
            </div>

            <div class="col-md-6">
              <div class="p-3 bg-light rounded-3 border h-100">
                <div class="d-flex align-items-center gap-1.5 text-success fw-bold small mb-1.5">
                  <span>⚙️</span>
                  <span>How Senior Engineers Implement It:</span>
                </div>
                <div class="text-secondary small mb-2" style="line-height: 1.6;">
                  ${escapeHtml(realWorld.how_applied || 'Implemented using modular patterns, immutable data structures, and defensive boundary validation.')}
                </div>
                <div class="text-muted small" style="font-size: 0.78rem;">
                  <strong>Placement &amp; Interview Focus:</strong> ${escapeHtml(realWorld.interview_relevance || 'Core technical interview staple in software design and coding assessments.')}
                </div>
              </div>
            </div>
          </div>

          <!-- Production Incident Safeguard -->
          <div class="p-3 rounded-3 border bg-warning bg-opacity-10 border-warning border-opacity-25 d-flex align-items-start gap-2.5">
            <span class="fs-5 text-warning">⚠️</span>
            <div>
              <div class="fw-bold text-dark small mb-0.5">Production Incident Safeguard:</div>
              <div class="text-secondary small" style="font-size: 0.82rem; line-height: 1.5;">
                ${escapeHtml(realWorld.production_safeguards || 'Enforce bounds checks, clean memory disposal, and defensive fallback handlers to avoid system outages.')}
              </div>
            </div>
          </div>
        </div>

        <!-- 3. WORKING CODE DEMONSTRATION & IMPLEMENTATION -->
        ${example ? `
          <div class="card border-0 shadow-sm p-4 mb-4 rounded-4" style="background: #ffffff; border-left: 5px solid #8b5cf6 !important;">
            <div class="d-flex align-items-center justify-content-between mb-3 flex-wrap gap-2">
              <div class="d-flex align-items-center gap-2">
                <span class="fs-4">💻</span>
                <div>
                  <h5 class="fw-bold text-dark mb-0">3. Working Code Demonstration &amp; Implementation</h5>
                  <small class="text-muted">${escapeHtml(example.title || 'Step-by-Step Code Walkthrough')}</small>
                </div>
              </div>
              <span class="badge bg-secondary-subtle text-secondary border rounded-pill px-2.5 py-1 small">${escapeHtml(example.difficulty || 'Industry Standard')}</span>
            </div>

            ${example.problem ? `
              <div class="p-3 bg-light rounded-3 border mb-3 small text-secondary">
                <strong>Problem Scenario:</strong> ${escapeHtml(example.problem)}
              </div>
            ` : ''}

            <div class="position-relative mb-3">
              <pre class="p-3.5 bg-dark text-light rounded-3 font-monospace small mb-0 overflow-auto" style="max-height: 280px; font-size: 0.84rem; line-height: 1.6;"><code>${escapeHtml(example.code_or_math || '')}</code></pre>
            </div>

            ${example.explanation ? `
              <div class="alert alert-light border small mb-0 text-secondary">
                <strong>💡 Code Walkthrough:</strong> ${escapeHtml(example.explanation)}
              </div>
            ` : ''}
          </div>
        ` : ''}

        <!-- 4. INTERACTIVE KNOWLEDGE CHECK & PRACTICE CHALLENGE -->
        ${question ? `
          <div class="card border-0 shadow-sm p-4 mb-4 rounded-4" style="background: #ffffff; border-left: 5px solid #f59e0b !important;">
            <div class="d-flex align-items-center justify-content-between mb-3 flex-wrap gap-2">
              <div class="d-flex align-items-center gap-2">
                <span class="fs-4">📝</span>
                <h5 class="fw-bold text-dark mb-0">4. Interactive Knowledge Check &amp; Practice Challenge</h5>
              </div>
              <span class="badge bg-warning-subtle text-dark border border-warning-subtle rounded-pill px-2.5 py-1 small fw-bold">Test Your Understanding</span>
            </div>

            <p class="text-dark fw-semibold small mb-3" style="font-size: 0.92rem;">
              ${escapeHtml(question.question || question.title || 'Review the conceptual challenge below:')}
            </p>

            ${question.options && question.options.length ? `
              <div class="d-flex flex-column gap-2 mb-3">
                ${question.options.map((opt, oIdx) => `
                  <div class="p-2.5 rounded-3 border bg-light d-flex align-items-center gap-2.5 cursor-pointer topic-quiz-option" 
                       onclick="selectTopicQuizOption(this, ${oIdx === question.answer ? 'true' : 'false'})"
                       style="cursor: pointer; transition: all 0.2s ease;">
                    <span class="badge bg-white border text-dark rounded-circle px-2 py-1">${String.fromCharCode(65 + oIdx)}</span>
                    <span class="small text-secondary">${escapeHtml(opt)}</span>
                  </div>
                `).join('')}
              </div>
            ` : ''}

            <div class="d-flex align-items-center gap-2">
              <button type="button" class="btn btn-sm btn-outline-warning rounded-pill px-3 py-1.5 fw-semibold" onclick="toggleTopicSolution(${curItem.chapterNum}, ${curItem.topicIdx})">
                👁️ Reveal Solution &amp; Architectural Explanation
              </button>
            </div>

            <div id="topic-solution-${curItem.chapterNum}-${curItem.topicIdx}" class="mt-3 p-3 bg-light rounded-3 border small" style="display: none;">
              <div class="fw-bold text-success mb-1">✓ Solution &amp; Architectural Explanation:</div>
              <div class="text-secondary" style="line-height: 1.6;">${escapeHtml(question.explanation || question.answer || 'Review key fundamentals and practical safeguards above to solidify this topic.')}</div>
            </div>
          </div>
        ` : ''}

        <!-- BOTTOM NAVIGATION TOOLBAR -->
        <div class="p-3.5 bg-light rounded-4 border d-flex align-items-center justify-content-between flex-wrap gap-2 mt-4">
          <button type="button" class="btn btn-outline-secondary rounded-pill px-3 py-1.5 small fw-semibold" onclick="goToPreviousTopic()" ${currentIndex <= 0 ? 'disabled' : ''}>
            ⬅ Previous Topic
          </button>
          <div class="d-flex align-items-center gap-2">
            <button type="button" class="btn ${isCompleted ? 'btn-success' : 'btn-outline-primary'} rounded-pill px-3 py-1.5 small fw-semibold" onclick="toggleTopicCompleted('${curItem.topicId}', ${curItem.stageNum})">
              ${isCompleted ? '✓ Marked Complete' : 'Mark Complete'}
            </button>
            <button type="button" class="btn btn-primary rounded-pill px-3.5 py-1.5 small fw-bold" onclick="completeAndGoToNextTopic()">
              ${currentIndex >= totalTopics - 1 ? 'Finish Course 🎓' : 'Complete & Next Topic ➔'}
            </button>
          </div>
        </div>
      `;
    }

    // Render Curriculum Outline Sidebar
    const outlineContainer = document.getElementById("step-outline-modules-list");
    if (outlineContainer && currentCourseCurriculum?.chapters) {
      outlineContainer.innerHTML = currentCourseCurriculum.chapters.map((ch, mIdx) => {
        const chNum = ch.chapter_num || (mIdx + 1);
        const topics = (ch.topics && ch.topics.length) ? ch.topics : [ch.title];
        const isCurrentModule = (mIdx === currentLearningModuleIdx);
        const chCompletedCount = topics.filter((_, tIdx) => completedList.includes(`topic-${chNum}-${tIdx + 1}`)).length;
        const isModuleDone = (chCompletedCount === topics.length && topics.length > 0);

        return `
          <div class="card border-0 mb-2 rounded-3 shadow-none ${isCurrentModule ? 'bg-white border-primary shadow-sm' : 'bg-transparent'}">
            <div class="p-2.5 border-bottom d-flex align-items-center justify-content-between cursor-pointer" onclick="toggleModuleOutlineAccordion(${mIdx})" style="cursor: pointer;">
              <div>
                <span class="badge ${ch.progression_stage === 1 ? 'bg-success' : ch.progression_stage === 2 ? 'bg-primary' : ch.progression_stage === 3 ? 'bg-warning text-dark' : 'bg-danger'} rounded-pill px-2 py-0.5 me-1" style="font-size: 0.65rem;">
                  Stage ${ch.progression_stage || (chNum <= 2 ? 1 : chNum <= 5 ? 2 : chNum <= 7 ? 3 : 4)}
                </span>
                <strong class="small text-dark" style="font-size: 0.8rem;">Module ${chNum}</strong>
                <div class="text-truncate text-secondary" style="max-width: 210px; font-size: 0.74rem;">${escapeHtml(ch.title)}</div>
              </div>
              <span class="badge ${isModuleDone ? 'bg-success' : 'bg-light text-muted border'} rounded-pill" style="font-size: 0.68rem;">
                ${chCompletedCount}/${topics.length}
              </span>
            </div>
            <div class="p-1.5 ${isCurrentModule ? 'd-block' : 'd-none'}" id="module-outline-sublist-${mIdx}">
              ${topics.map((t, tIdx) => {
                const tId = `topic-${chNum}-${tIdx + 1}`;
                const isDone = completedList.includes(tId);
                const isActive = (mIdx === currentLearningModuleIdx && tIdx === currentLearningTopicIdx);

                return `
                  <div class="p-2 rounded-2 mb-1 cursor-pointer d-flex align-items-center justify-content-between ${isActive ? 'bg-primary text-white fw-bold shadow-sm' : isDone ? 'bg-success-subtle text-success' : 'hover-bg-light text-secondary'}" 
                       style="font-size: 0.75rem; cursor: pointer; transition: background 0.15s ease;"
                       onclick="selectStepTopic(${mIdx}, ${tIdx})">
                    <div class="d-flex align-items-center gap-1.5 text-truncate me-2">
                      <span>${isDone ? '✓' : isActive ? '▶' : `${tIdx + 1}.`}</span>
                      <span class="text-truncate">${escapeHtml(t)}</span>
                    </div>
                    ${isActive ? '<span class="badge bg-white text-primary rounded-pill" style="font-size: 0.62rem;">Active</span>' : ''}
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        `;
      }).join('');
    }
  };

  window.completeAndGoToNextTopic = async function() {
    if (!currentAllTopicsList || !currentAllTopicsList.length) return;

    const curItem = currentAllTopicsList.find(x => x.moduleIdx === currentLearningModuleIdx && x.topicIdx === currentLearningTopicIdx);
    if (curItem) {
      if (!activeJourneyData.completed_topics) activeJourneyData.completed_topics = [];
      if (!activeJourneyData.completed_topics.includes(curItem.topicId)) {
        activeJourneyData.completed_topics.push(curItem.topicId);
        try {
          if (typeof api !== "undefined" && api.studyMaterials && typeof api.studyMaterials.completeTopic === "function") {
            api.studyMaterials.completeTopic({ topic_id: curItem.topicId, phase_num: curItem.stageNum });
          }
        } catch (e) {
          console.warn("Complete topic API error", e);
        }
      }
    }

    const curIndex = currentAllTopicsList.indexOf(curItem);
    if (curIndex < currentAllTopicsList.length - 1) {
      const nextItem = currentAllTopicsList[curIndex + 1];
      renderStepByStepTopic(nextItem.moduleIdx, nextItem.topicIdx);
      const viewport = document.getElementById("step-lesson-viewport");
      if (viewport) viewport.scrollTop = 0;
    } else {
      alert("🎉 Congratulations! You have completed all curriculum topics in this course from foundational syntax to real-world deployment!");
      renderStepByStepTopic(currentLearningModuleIdx, currentLearningTopicIdx);
    }

    renderLearningJourneyDashboard(activeJourneyData);
  };

  window.goToPreviousTopic = function() {
    if (!currentAllTopicsList || !currentAllTopicsList.length) return;
    const curItem = currentAllTopicsList.find(x => x.moduleIdx === currentLearningModuleIdx && x.topicIdx === currentLearningTopicIdx);
    const curIndex = currentAllTopicsList.indexOf(curItem);
    if (curIndex > 0) {
      const prevItem = currentAllTopicsList[curIndex - 1];
      renderStepByStepTopic(prevItem.moduleIdx, prevItem.topicIdx);
      const viewport = document.getElementById("step-lesson-viewport");
      if (viewport) viewport.scrollTop = 0;
    }
  };

  window.selectStepTopic = function(mIdx, tIdx) {
    renderStepByStepTopic(mIdx, tIdx);
    const viewport = document.getElementById("step-lesson-viewport");
    if (viewport) viewport.scrollTop = 0;
  };

  window.toggleModuleOutlineAccordion = function(mIdx) {
    const el = document.getElementById(`module-outline-sublist-${mIdx}`);
    if (el) {
      if (el.classList.contains("d-none")) {
        el.classList.remove("d-none");
        el.classList.add("d-block");
      } else {
        el.classList.remove("d-block");
        el.classList.add("d-none");
      }
    }
  };

  window.toggleTopicSolution = function(chNum, tIdx) {
    const el = document.getElementById(`topic-solution-${chNum}-${tIdx}`);
    if (el) {
      el.style.display = (el.style.display === "none" || !el.style.display) ? "block" : "none";
    }
  };

  window.selectTopicQuizOption = function(el, isCorrect) {
    const parent = el.closest(".d-flex.flex-column");
    if (parent) {
      parent.querySelectorAll(".topic-quiz-option").forEach(item => {
        item.classList.remove("bg-success-subtle", "border-success", "bg-danger-subtle", "border-danger");
      });
    }
    if (isCorrect) {
      el.classList.add("bg-success-subtle", "border-success");
    } else {
      el.classList.add("bg-danger-subtle", "border-danger");
    }
  };

  window.toggleTopicIndexDrawer = function() {
    const sidebar = document.getElementById("step-topics-sidebar");
    if (sidebar) {
      if (sidebar.style.display === "none") {
        sidebar.style.display = "block";
      } else {
        sidebar.style.display = "none";
      }
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

  
  function getEffectiveWeeklySchedule(curData) {
    if (activeJourneyData && Array.isArray(activeJourneyData.weekly_schedule) && activeJourneyData.weekly_schedule.length > 0) {
      return activeJourneyData.weekly_schedule;
    }
    const chapters = (curData && curData.chapters) ? curData.chapters : [];
    const isStarted = Boolean(activeJourneyData && activeJourneyData.is_started);
    const baseDate = (isStarted && activeJourneyData.course_started_at) ? new Date(activeJourneyData.course_started_at) : new Date();

    const weeks = [];
    for (let w = 1; w <= 12; w++) {
      let wStart, wEnd, daysLabel, weekTitle, phaseNum, phaseName, topicsList;
      if (w <= 10) {
        wStart = new Date(baseDate.getTime() + (w - 1) * 7 * 86400000);
        wEnd = new Date(wStart.getTime() + 6 * 86400000);
        daysLabel = `Days ${(w - 1) * 7 + 1}-${w * 7}`;
        const ch = chapters[w - 1] || {};
        weekTitle = ch.title || `Module ${w}: Core Engineering & Practice`;
        phaseNum = w <= 3 ? 1 : (w <= 7 ? 2 : 3);
        phaseName = phaseNum === 1 ? "Phase 1: Foundations" : (phaseNum === 2 ? "Phase 2: Core Engineering" : "Phase 3: Production Systems");
        topicsList = (ch.topics || []).map((t, tIdx) => ({
          id: `topic-${w}-${tIdx + 1}`,
          title: t,
          is_completed: false,
          order: tIdx + 1
        }));
      } else if (w === 11) {
        wStart = new Date(baseDate.getTime() + 70 * 86400000);
        wEnd = new Date(baseDate.getTime() + 79 * 86400000);
        daysLabel = "Days 71-80";
        weekTitle = "Placement Sprint 1: Company Technical Assessments & Problem Solving Drills";
        phaseNum = 4;
        phaseName = "Phase 4: Placement Ready";
        topicsList = [
          { id: "topic-11-1", title: "High-Frequency Company Coding Challenges & LeetCode Sprints", is_completed: false, order: 1 },
          { id: "topic-11-2", title: "Data Structures & Algorithm Optimization Speed Tests", is_completed: false, order: 2 },
          { id: "topic-11-3", title: "System Design & Enterprise Architecture Walkthroughs", is_completed: false, order: 3 },
          { id: "topic-11-4", title: "Live Timed Technical Coding Assessment Drills", is_completed: false, order: 4 }
        ];
      } else {
        wStart = new Date(baseDate.getTime() + 80 * 86400000);
        wEnd = new Date(baseDate.getTime() + 89 * 86400000);
        daysLabel = "Days 81-90";
        weekTitle = "Placement Sprint 2: AI Proctored Mock Interviews & Final Readiness Verification";
        phaseNum = 4;
        phaseName = "Phase 4: Placement Ready";
        topicsList = [
          { id: "topic-12-1", title: "AI Proctored Technical Mock Interview with Live Audio/Video", is_completed: false, order: 1 },
          { id: "topic-12-2", title: "HR Behavioral Interview & STAR Method Response Mastery", is_completed: false, order: 2 },
          { id: "topic-12-3", title: "ATS Resume Score Optimization & Production Portfolio Review", is_completed: false, order: 3 },
          { id: "topic-12-4", title: "Final Placement Readiness Audit & Direct Job Application Dispatch", is_completed: false, order: 4 }
        ];
      }

      const fmt = (d) => d.toLocaleDateString("en-US", { month: "short", day: "2-digit" });
      const fmtFull = (d) => d.toLocaleDateString("en-US", { month: "short", day: "2-digit", year: "numeric" });

      weeks.push({
        week_num: w,
        days_label: daysLabel,
        phase_num: phaseNum,
        phase_name: phaseName,
        title: weekTitle,
        date_range: `${fmt(wStart)} - ${fmt(wEnd)}`,
        target_completion_date: fmtFull(wEnd),
        topics: topicsList,
        topics_count: topicsList.length,
        completed_topics_count: 0,
        progress_percent: 0.0,
        status: isStarted ? (w === 1 ? "In Progress" : "Upcoming") : (w === 1 ? "Ready to Start" : "Locked"),
        is_current_week: w === 1
      });
    }
    return weeks;
  }

  function renderCurriculumModalContent(curData, courseId) {
    const modalTitle = document.getElementById("curriculum-modal-title");
    const modalRole = document.getElementById("curriculum-modal-role");
    const modalBody = document.getElementById("curriculum-modal-body");

    if (modalTitle) modalTitle.textContent = curData ? curData.course_title : "Course Learning Roadmap & Guidance";
    if (modalRole) modalRole.textContent = curData ? `${curData.target_role} • ${curData.chapters_count || 10} Structured Modules • Fundamentals ➔ Advanced ➔ Real-World Projects` : "Placement Ready Track";

    if (!modalBody) return;

    const chapters = (curData && curData.chapters) ? curData.chapters : [];
    const exercises = (curData && curData.practical_exercises) ? curData.practical_exercises : (activeJourneyData?.practical_exercises || []);
    const projects = (curData && curData.real_world_projects) ? curData.real_world_projects : (activeJourneyData?.real_world_projects || []);
    const placement = (curData && curData.placement_training) ? curData.placement_training : (activeJourneyData?.placement_training || {});
    const progression = curData?.progression_overview || null;

    modalBody.innerHTML = `
      <!-- 4-Stage Pedagogical Stepper Banner -->
      <div class="card border-0 shadow-sm p-3 mb-4 rounded-4" style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #ffffff;">
        <div class="d-flex align-items-center justify-content-between mb-2.5 flex-wrap gap-2">
          <div class="d-flex align-items-center gap-2">
            <span class="badge bg-primary px-3 py-1 rounded-pill small fw-bold">🎯 Learning Progression Ladder</span>
            <span class="fw-bold small text-light">Step-by-Step From Fundamentals to Production Systems</span>
          </div>
          <span class="badge bg-success-subtle text-success border border-success-subtle rounded-pill px-2.5 py-0.5" style="font-size: 0.72rem;">Beginner Friendly ➔ Enterprise Ready</span>
        </div>
        <div class="row g-2 text-center">
          <div class="col-6 col-md-3">
            <div class="p-2.5 rounded-3 border border-secondary h-100" style="background: rgba(255,255,255,0.06);">
              <span class="badge bg-success text-white rounded-pill px-2 py-0.5 mb-1" style="font-size: 0.68rem;">Stage 1</span>
              <div class="fw-bold small text-white">Fundamentals</div>
              <div class="text-white-50" style="font-size: 0.7rem;">Syntax, Runtime &amp; Basics</div>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div class="p-2.5 rounded-3 border border-secondary h-100" style="background: rgba(255,255,255,0.06);">
              <span class="badge bg-primary text-white rounded-pill px-2 py-0.5 mb-1" style="font-size: 0.68rem;">Stage 2</span>
              <div class="fw-bold small text-white">Core Engineering</div>
              <div class="text-white-50" style="font-size: 0.7rem;">Data Structures &amp; OOP</div>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div class="p-2.5 rounded-3 border border-secondary h-100" style="background: rgba(255,255,255,0.06);">
              <span class="badge bg-warning text-dark rounded-pill px-2 py-0.5 mb-1" style="font-size: 0.68rem;">Stage 3</span>
              <div class="fw-bold small text-white">Advanced Concepts</div>
              <div class="text-white-50" style="font-size: 0.7rem;">Concurrency &amp; Optimization</div>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div class="p-2.5 rounded-3 border border-secondary h-100" style="background: rgba(255,255,255,0.06);">
              <span class="badge bg-danger text-white rounded-pill px-2 py-0.5 mb-1" style="font-size: 0.68rem;">Stage 4</span>
              <div class="fw-bold small text-white">Real-World Projects</div>
              <div class="text-white-50" style="font-size: 0.7rem;">Microservices &amp; Deployment</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Schedule Pace Overview Banner -->
      ${(() => {
        const isStarted = Boolean(activeJourneyData && activeJourneyData.is_started);
        const overview = activeJourneyData?.schedule_overview || {};
        const expectedDate = overview.expected_completion_date || activeJourneyData?.expected_completion_date || "Feb 01, 2027";
        const startDate = isStarted ? (overview.start_date || "Active Sprint") : "Starts Day 1 on Click (Ready Today)";
        const overallPct = Math.round(activeJourneyData?.overall_progress_percent || 0);
        const completedCnt = (activeJourneyData?.completed_topics && activeJourneyData.completed_topics.length) || 0;

        return `
          <div class="card border-0 shadow-sm p-4 mb-4 rounded-4" style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #ffffff;">
            <div class="d-flex align-items-center justify-content-between mb-3 flex-wrap gap-2">
              <div class="d-flex align-items-center gap-2">
                <span class="fs-4">${isStarted ? '⚡' : '🚀'}</span>
                <div>
                  <h5 class="fw-bold mb-0 text-white">${isStarted ? 'Sprint Active: 90-Day Placement Journey' : '90-Day Learning Roadmap & Weekly Schedule'}</h5>
                  <div class="small text-white-50">${isStarted ? `Day ${overview.days_elapsed || 1} of 90 • Week ${overview.current_week || 1} of 12` : 'Starts only when you click Start Course • Independent to your candidate account'}</div>
                </div>
              </div>
              <div class="d-flex align-items-center gap-2">
                <span class="badge ${isStarted ? 'bg-success text-white' : 'bg-warning text-dark'} rounded-pill px-3 py-1.5 fw-bold">
                  ${isStarted ? 'In Progress' : 'Ready to Start'}
                </span>
                ${!isStarted ? `
                  <button class="btn btn-sm btn-primary rounded-pill px-3 py-1.5 fw-bold shadow-sm" onclick="startCurrentCourse(event)">
                    ▶ Start Course Now
                  </button>
                ` : `
                  <a href="course-learning.html?course=${encodeURIComponent(courseId)}" class="btn btn-sm btn-outline-light rounded-pill px-3 py-1.5 fw-semibold">
                    Open Course Studio →
                  </a>
                `}
              </div>
            </div>

            <!-- Key Milestones Strip -->
            <div class="row g-2 text-center pt-2 border-top border-white border-opacity-15">
              <div class="col-6 col-md-3">
                <div class="p-2 rounded-3" style="background: rgba(255,255,255,0.06);">
                  <div class="text-white-50" style="font-size: 0.72rem;">📅 JOURNEY START</div>
                  <div class="fw-bold small text-white text-truncate">${escapeHtml(startDate)}</div>
                </div>
              </div>
              <div class="col-6 col-md-3">
                <div class="p-2 rounded-3" style="background: rgba(255,255,255,0.06);">
                  <div class="text-white-50" style="font-size: 0.72rem;">🎯 EXPECTED FINISH</div>
                  <div class="fw-bold small text-success text-truncate">${escapeHtml(expectedDate)}</div>
                </div>
              </div>
              <div class="col-6 col-md-3">
                <div class="p-2 rounded-3" style="background: rgba(255,255,255,0.06);">
                  <div class="text-white-50" style="font-size: 0.72rem;">⏱️ WEEKLY SPRINT PACE</div>
                  <div class="fw-bold small text-white text-truncate">4-5 Topics / Week</div>
                </div>
              </div>
              <div class="col-6 col-md-3">
                <div class="p-2 rounded-3" style="background: rgba(255,255,255,0.06);">
                  <div class="text-white-50" style="font-size: 0.72rem;">📊 OVERALL PROGRESS</div>
                  <div class="fw-bold small text-info text-truncate">${overallPct}% (${completedCnt}/50 Topics)</div>
                </div>
              </div>
            </div>
          </div>
        `;
      })()}

      <!-- Navigation Tabs -->
      <ul class="nav nav-pills nav-fill mb-4 p-1.5 bg-light rounded-4 gap-1 border" id="curriculumTabs" role="tablist">
        <li class="nav-item" role="presentation">
          <button class="nav-link active rounded-pill fw-bold py-2" id="tab-schedule-btn" data-bs-toggle="pill" data-bs-target="#tab-schedule-pane" type="button" role="tab">
            📅 90-Day Weekly Schedule & Calendar (12 Weeks)
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link rounded-pill fw-bold py-2" id="tab-curriculum-btn" data-bs-toggle="pill" data-bs-target="#tab-curriculum-pane" type="button" role="tab">
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
        <!-- TAB 0: 90-DAY WEEKLY SCHEDULE & TOPICS CALENDAR -->
        <div class="tab-pane fade show active" id="tab-schedule-pane" role="tabpanel">
          ${(() => {
            const isStarted = Boolean(activeJourneyData && activeJourneyData.is_started);
            const weeklySchedule = getEffectiveWeeklySchedule(curData);
            const completedTopics = (activeJourneyData?.completed_topics) || [];

            return `
              <div class="alert alert-light border shadow-sm rounded-4 mb-4 p-3 d-flex align-items-center justify-content-between flex-wrap gap-2">
                <div class="d-flex align-items-center gap-2">
                  <span class="fs-4">🗓️</span>
                  <div>
                    <strong class="text-dark">Week-by-Week Placement Sprint Calendar (Weeks 1 to 12)</strong>
                    <div class="small text-secondary">Every week is designed with realistic targets, specific topics to complete, and direct hands-on practice.</div>
                  </div>
                </div>
                <div class="d-flex align-items-center gap-2">
                  <span class="badge bg-primary-subtle text-primary border rounded-pill px-3 py-1">50 Topics Total</span>
                  <span class="badge bg-success-subtle text-success border rounded-pill px-3 py-1">10 Modules + 2 Sprints</span>
                </div>
              </div>

              <!-- 12-Week List -->
              <div class="d-flex flex-column gap-3 mb-4">
                ${weeklySchedule.map((wk) => {
                  const isCurrent = isStarted && wk.is_current_week;
                  const phaseColor = wk.phase_num === 1 ? 'success' : (wk.phase_num === 2 ? 'primary' : (wk.phase_num === 3 ? 'warning text-dark' : 'info text-dark'));
                  const topics = wk.topics || [];

                  return `
                    <div class="card border rounded-4 shadow-sm overflow-hidden ${isCurrent ? 'border-primary' : ''}">
                      <div class="card-header bg-white p-3 d-flex align-items-center justify-content-between flex-wrap gap-2 border-bottom">
                        <div class="d-flex align-items-center gap-2 flex-wrap">
                          <span class="badge bg-dark text-white rounded-pill px-3 py-1 fw-bold" style="font-size: 0.78rem;">
                            Week ${wk.week_num} (${wk.days_label})
                          </span>
                          <span class="badge bg-${phaseColor} rounded-pill px-2.5 py-0.5" style="font-size: 0.7rem;">
                            ${escapeHtml(wk.phase_name)}
                          </span>
                          <span class="fw-bold text-dark" style="font-size: 0.92rem;">
                            ${escapeHtml(wk.title)}
                          </span>
                        </div>
                        <div class="d-flex align-items-center gap-2 flex-shrink-0">
                          <span class="badge bg-light text-secondary border px-2.5 py-1" style="font-size: 0.73rem;">
                            📅 ${escapeHtml(wk.date_range)} • Target: <b>${escapeHtml(wk.target_completion_date)}</b>
                          </span>
                          <span class="badge ${wk.status === 'Completed' ? 'bg-success' : (wk.status === 'In Progress' ? 'bg-primary' : 'bg-secondary')} text-white rounded-pill px-2.5 py-1" style="font-size: 0.68rem;">
                            ${escapeHtml(wk.status)}
                          </span>
                        </div>
                      </div>

                      <div class="card-body p-3 bg-light bg-opacity-50">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                          <div class="small fw-bold text-secondary">Topics to cover in Week ${wk.week_num} (${topics.length} topics):</div>
                          ${!isStarted ? `
                            <button class="btn btn-sm btn-outline-primary rounded-pill px-3 py-0.5 fw-semibold" onclick="startCurrentCourse(event)" style="font-size: 0.73rem;">
                              ▶ Start Course to Unlock
                            </button>
                          ` : `
                            <a href="course-learning.html?course=${encodeURIComponent(courseId)}&module=${wk.week_num - 1}" class="btn btn-sm btn-primary rounded-pill px-3 py-0.5 fw-semibold" style="font-size: 0.73rem;">
                              Learn This Week's Topics →
                            </a>
                          `}
                        </div>

                        <div class="row g-2">
                          ${topics.map((t) => {
                            const isDone = completedTopics.includes(t.id) || t.is_completed;
                            return `
                              <div class="col-12 col-md-6">
                                <div class="p-2 rounded-3 bg-white border d-flex align-items-center gap-2 h-100 shadow-xs">
                                  <span class="flex-shrink-0" style="font-size: 0.95rem;">
                                    ${isDone ? '✅' : '⚪'}
                                  </span>
                                  <div class="flex-grow-1 small ${isDone ? 'text-decoration-line-through text-muted' : 'text-dark'}" style="font-size: 0.78rem; line-height: 1.3;">
                                    <strong>#${t.order || 1}</strong> ${escapeHtml(t.title)}
                                  </div>
                                </div>
                              </div>
                            `;
                          }).join('')}
                        </div>
                      </div>
                    </div>
                  `;
                }).join('')}
              </div>
            `;
          })()}
        </div>

        <!-- TAB 1: CURRICULUM CHAPTERS -->
        <div class="tab-pane fade" id="tab-curriculum-pane" role="tabpanel">
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
                      <div class="d-flex align-items-center gap-2 flex-grow-1 flex-wrap">
                        <span class="badge bg-dark text-white rounded-pill px-2.5 py-1">Module ${chNum}</span>
                        <span class="badge ${ch.progression_stage === 1 ? 'bg-success' : ch.progression_stage === 2 ? 'bg-primary' : ch.progression_stage === 3 ? 'bg-warning text-dark' : 'bg-danger'} rounded-pill px-2.5 py-0.5" style="font-size: 0.68rem;">
                          ${escapeHtml(ch.stage_badge || (chNum <= 2 ? 'Fundamentals' : chNum <= 5 ? 'Core Engineering' : chNum <= 7 ? 'Advanced Concepts' : 'Real-World Projects'))}
                        </span>
                        <span class="fw-bold text-dark">${escapeHtml(ch.title)}</span>
                      </div>
                    </button>
                  </h2>
                  <div id="collapse-ch-${chNum}" class="accordion-collapse collapse ${idx === 0 ? 'show' : ''}" data-bs-parent="#curriculumAccordion">
                    <div class="accordion-body bg-light p-4">
                      <!-- REAL-TIME PROJECT APPLICATION CARD -->
                      ${ch.real_world_application ? `
                        <div class="card border-0 shadow-sm p-3.5 mb-3 rounded-3" style="background: #ffffff; border-left: 4px solid #3b82f6 !important;">
                          <div class="d-flex align-items-center justify-content-between mb-2 flex-wrap gap-2">
                            <div class="d-flex align-items-center gap-2">
                              <span class="fs-5">🚀</span>
                              <h6 class="fw-bold text-dark mb-0" style="font-size: 0.92rem;">Real-Time Project Application (How &amp; Where Used in Industry)</h6>
                            </div>
                            <span class="badge bg-dark text-white rounded-pill px-2.5 py-1" style="font-size: 0.7rem;">🏢 ${escapeHtml(ch.real_world_application.domain || 'Enterprise Software')}</span>
                          </div>
                          <div class="row g-2 mb-2">
                            <div class="col-md-6">
                              <div class="p-2.5 bg-light rounded-2 border">
                                <div class="text-primary fw-bold small mb-1">📍 Where Applied in Production:</div>
                                <div class="text-secondary small" style="font-size: 0.78rem;">${escapeHtml(ch.real_world_application.where_applied || '')}</div>
                                <div class="mt-1 text-muted" style="font-size: 0.7rem;"><strong>Top Companies:</strong> ${escapeHtml(ch.real_world_application.companies || 'Amazon, Google, TCS, Infosys')}</div>
                              </div>
                            </div>
                            <div class="col-md-6">
                              <div class="p-2.5 bg-light rounded-2 border">
                                <div class="text-success fw-bold small mb-1">⚙️ How Engineers Implement It:</div>
                                <div class="text-secondary small" style="font-size: 0.78rem;">${escapeHtml(ch.real_world_application.how_applied || '')}</div>
                                <div class="mt-1 text-muted" style="font-size: 0.7rem;"><strong>Placement Focus:</strong> ${escapeHtml(ch.real_world_application.interview_relevance || '')}</div>
                              </div>
                            </div>
                          </div>
                          <div class="p-2 bg-light rounded-2 border small d-flex align-items-start gap-2">
                            <span class="text-warning">⚠️</span>
                            <div style="font-size: 0.76rem;" class="text-muted">
                              <strong>Production Incident Safeguard:</strong> ${escapeHtml(ch.real_world_application.production_safeguards || 'Enforce bounds, defensive logging, and resource cleanup.')}
                            </div>
                          </div>
                        </div>
                      ` : ''}

                      <div class="mb-3">
                        <h6 class="fw-bold text-dark mb-1">Key Takeaways &amp; Core Concepts:</h6>
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

    const isCourseStarted = Boolean(activeJourneyData && activeJourneyData.is_started);
    const weeklyScheduleBadge = phase.weekly_schedule || `Phase ${phaseNum}`;
    const dateRangeStr = phase.date_range || "90-Day Sprint";

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
      if (!isCourseStarted) {
        modalActions.innerHTML = `
          <button type="button" class="btn btn-outline-primary rounded-pill px-3 fw-bold" onclick="openFullRoadmapScheduleModal(event)">
            🗓️ View Full 12-Week Calendar
          </button>
          <button type="button" class="btn btn-primary rounded-pill px-4 fw-bold" onclick="startCurrentCourse(event)">
            ▶ Start Course Now &rarr;
          </button>
        `;
      } else {
        modalActions.innerHTML = `
          ${!phase.is_locked ? `
            <button type="button" class="btn btn-outline-primary rounded-pill px-3 fw-bold" onclick="openFullRoadmapScheduleModal(event)">
              🗓️ 12-Week Schedule
            </button>
            <a href="${phase.action_url || 'course-learning.html'}" class="btn btn-primary rounded-pill px-4 fw-bold">
              ${escapeHtml(phase.action_text || 'Continue Learning')} &rarr;
            </a>
          ` : `
            <button type="button" class="btn btn-secondary rounded-pill px-4" disabled>
              🔒 Locked (Complete Phase ${phaseNum - 1} First)
            </button>
          `}
        `;
      }
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
  window.startCurrentCourse = startCurrentCourse;
  window.renderStepByStepTopic = renderStepByStepTopic;
  window.completeAndGoToNextTopic = completeAndGoToNextTopic;
  window.goToPreviousTopic = goToPreviousTopic;
  window.selectStepTopic = selectStepTopic;
  window.toggleModuleOutlineAccordion = toggleModuleOutlineAccordion;
  window.toggleTopicSolution = toggleTopicSolution;
  window.selectTopicQuizOption = selectTopicQuizOption;
  window.toggleTopicIndexDrawer = toggleTopicIndexDrawer;

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
