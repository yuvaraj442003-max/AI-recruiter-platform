/**
 * course-learning.js — Course Learning Studio & All Topics Directory
 * Systematically displays all topics of the selected course, from fundamentals to advanced concepts,
 * with real-world practical project applications, working code walkthroughs, and knowledge checks.
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
  let activeCourseId = "python";
  let curriculumData = null;
  let allTopicsList = [];
  let currentModuleIdx = 0;
  let currentTopicIdx = 0;
  let completedTopics = [];
  let activeFilterStage = "all";

  const ALL_TRACKS = [
    { id: "python", name: "Python Full-Stack", icon: "🐍", badge: "AI & Fast-Track" },
    { id: "java", name: "Java Programming", icon: "☕", badge: "Most Popular for Placements" },
    { id: "dsa", name: "DSA Placement Mastery", icon: "⚡", badge: "Placement Essential" },
    { id: "web_dev", name: "Full-Stack Web Dev", icon: "🌐", badge: "High Demand" },
    { id: "ai_ml", name: "AI and Machine Learning", icon: "🤖", badge: "Future-Ready AI" },
    { id: "data_science", name: "Data Science", icon: "📊", badge: "High Salary Roles" },
    { id: "cloud_computing", name: "Cloud Computing", icon: "☁️", badge: "Cloud Architect Track" },
    { id: "aws", name: "AWS (Amazon Web Services)", icon: "🚀", badge: "Top Cloud Certification" },
    { id: "cybersecurity", name: "Cybersecurity", icon: "🛡️", badge: "High Demand Security" },
    { id: "devops", name: "DevOps", icon: "🔄", badge: "CI/CD & Kubernetes Mastery" },
    { id: "sql_db", name: "SQL & Database Management", icon: "🗄️", badge: "Core Placement Skill" },
    { id: "gen_ai", name: "Generative AI", icon: "✨", badge: "Cutting-Edge & High Salary" },
    { id: "deep_learning", name: "Deep Learning", icon: "🧠", badge: "Advanced AI & Research" },
    { id: "software_testing", name: "Software Testing & QA", icon: "🧪", badge: "QA Automation & SDET" },
  ];

  async function initCourseLearning() {
    const urlParams = new URLSearchParams(window.location.search);
    const courseParam = urlParams.get("course") || urlParams.get("subject");
    if (courseParam) {
      activeCourseId = courseParam.toLowerCase().trim();
    }

    renderCourseDropdown();

    // 1. Fetch Student Journey State (for completed topics)
    try {
      if (typeof api !== "undefined" && api.studyMaterials && typeof api.studyMaterials.getLearningJourney === "function") {
        const journeyRes = await api.studyMaterials.getLearningJourney();
        if (journeyRes && journeyRes.data) {
          completedTopics = journeyRes.data.completed_topics || [];
          if (!courseParam && journeyRes.data.selected_course) {
            activeCourseId = journeyRes.data.selected_course.toLowerCase().trim();
          }
        }
      }
    } catch (err) {
      console.warn("Could not load journey state:", err);
    }

    // 2. Fetch Course Curriculum
    try {
      if (typeof api !== "undefined" && api.studyMaterials && typeof api.studyMaterials.getCourseCurriculum === "function") {
        const res = await api.studyMaterials.getCourseCurriculum(activeCourseId);
        if (res && res.data) {
          curriculumData = res.data;
        }
      }
    } catch (err) {
      console.error("Failed to load curriculum from API:", err);
    }

    if (!curriculumData) {
      renderErrorState("Could not load curriculum data for " + activeCourseId);
      return;
    }

    // 3. Flatten Topic List
    buildTopicsList(curriculumData);

    // 4. Determine initial topic
    const qModule = urlParams.get("module");
    const qTopic = urlParams.get("topic");
    const autoStart = urlParams.get("start") === "true";

    if (qModule !== null && qTopic !== null) {
      currentModuleIdx = Math.max(0, parseInt(qModule, 10));
      currentTopicIdx = Math.max(0, parseInt(qTopic, 10));
    } else {
      const firstUncompleted = allTopicsList.find(t => !completedTopics.includes(t.topicId));
      if (firstUncompleted) {
        currentModuleIdx = firstUncompleted.moduleIdx;
        currentTopicIdx = firstUncompleted.topicIdx;
      } else {
        currentModuleIdx = 0;
        currentTopicIdx = 0;
      }
    }

    // Update Top & Directory Metadata
    updateHeaderMetadata();
    renderAllTopicsDirectory();
    renderCurrentTopic();
    renderCurriculumOutline();
    updateProgressBars();

    // If start=true or module specified, switch directly to lesson studio tab
    if (autoStart || qModule !== null) {
      openTopicLesson(currentModuleIdx, currentTopicIdx);
    }
  }

  function buildTopicsList(data) {
    allTopicsList = [];
    if (!data || !data.chapters) return;

    data.chapters.forEach((ch, mIdx) => {
      const chNum = ch.chapter_num || (mIdx + 1);
      const stageNum = ch.progression_stage || (chNum <= 2 ? 1 : chNum <= 5 ? 2 : chNum <= 7 ? 3 : 4);
      const stageBadge = ch.stage_badge || (stageNum === 1 ? 'Stage 1: Fundamentals' : stageNum === 2 ? 'Stage 2: Core Engineering' : stageNum === 3 ? 'Stage 3: Advanced Concepts' : 'Stage 4: Real-World Projects');
      const topics = (ch.topics && ch.topics.length) ? ch.topics : [ch.title];

      topics.forEach((t, tIdx) => {
        allTopicsList.push({
          moduleIdx: mIdx,
          topicIdx: tIdx,
          chapter: ch,
          chapterNum: chNum,
          topicTitle: t,
          topicId: `topic-${chNum}-${tIdx + 1}`,
          stageNum: stageNum,
          stageBadge: stageBadge,
        });
      });
    });
  }

  function updateHeaderMetadata() {
    const trackObj = ALL_TRACKS.find(t => t.id === activeCourseId) || { icon: "📚", name: "Course" };
    const courseTitle = curriculumData.course_title || `${trackObj.name}: Beginner to Placement Ready`;

    const elIcon = document.getElementById("page-course-icon");
    const elTitle = document.getElementById("page-course-title");
    const elModule = document.getElementById("page-module-badge");
    const countBadge = document.getElementById("all-topics-count-badge");
    const dirTitle = document.getElementById("dir-course-title");
    const dirDesc = document.getElementById("dir-course-desc");
    const dirStat = document.getElementById("dir-total-topics-stat");

    if (elIcon) elIcon.textContent = trackObj.icon;
    if (elTitle) elTitle.textContent = courseTitle;
    if (elModule) elModule.textContent = `${curriculumData.chapters.length} Modules`;
    if (countBadge) countBadge.textContent = `${allTopicsList.length} Topics`;
    if (dirTitle) dirTitle.textContent = courseTitle;
    if (dirDesc && curriculumData.target_role) {
      dirDesc.textContent = `${curriculumData.target_role} • Step-by-step complete syllabus from fundamental syntax and mechanics to real-world deployment.`;
    }
    if (dirStat) dirStat.textContent = `${curriculumData.chapters.length} Modules • ${allTopicsList.length} Topics`;

    const textbookLink = document.getElementById("link-course-textbook");
    if (textbookLink) {
      textbookLink.href = `study-materials.html?subject=${encodeURIComponent(activeCourseId)}`;
    }
  }

  function renderCourseDropdown() {
    const list = document.getElementById("courseTrackDropdownList");
    if (!list) return;

    list.innerHTML = `
      <li class="px-2 pb-2 pt-1 border-bottom mb-2">
        <span class="dropdown-header text-uppercase fw-bold text-muted p-0" style="font-size: 0.72rem; letter-spacing: 0.8px;">TARGET COURSE TRACKS</span>
      </li>
      ${ALL_TRACKS.map(t => {
        const isSel = (t.id === activeCourseId);
        return `
          <li>
            <a class="dropdown-item d-flex align-items-center gap-2 py-2 rounded-2 ${isSel ? 'active fw-bold' : ''}" 
               href="course-learning.html?course=${encodeURIComponent(t.id)}">
              <span class="fs-5">${escapeHtml(t.icon)}</span>
              <div class="flex-grow-1">
                <div class="small mb-0">${escapeHtml(t.name)}</div>
                <small class="${isSel ? 'text-white-50' : 'text-muted'}" style="font-size: 0.7rem;">${escapeHtml(t.badge)}</small>
              </div>
              ${isSel ? '<span class="ms-1 text-white"><i class="bi bi-check2"></i></span>' : ''}
            </a>
          </li>
        `;
      }).join('')}
    `;
  }

  // =========================================================================
  // VIEW 1: ALL TOPICS DIRECTORY
  // =========================================================================

  function renderAllTopicsDirectory() {
    const container = document.getElementById("all-modules-directory-list");
    if (!container || !curriculumData?.chapters) return;

    container.innerHTML = curriculumData.chapters.map((ch, mIdx) => {
      const chNum = ch.chapter_num || (mIdx + 1);
      const stageNum = ch.progression_stage || (chNum <= 2 ? 1 : chNum <= 5 ? 2 : chNum <= 7 ? 3 : 4);
      const stageBadge = ch.stage_badge || (stageNum === 1 ? 'Stage 1: Fundamentals' : stageNum === 2 ? 'Stage 2: Core Engineering' : stageNum === 3 ? 'Stage 3: Advanced Concepts' : 'Stage 4: Real-World Projects');
      const stageColor = stageNum === 1 ? 'success' : stageNum === 2 ? 'primary' : stageNum === 3 ? 'warning' : 'danger';
      const topics = (ch.topics && ch.topics.length) ? ch.topics : [ch.title];
      const realWorld = ch.real_world_application || {};

      const chCompletedCount = topics.filter((_, tIdx) => completedTopics.includes(`topic-${chNum}-${tIdx + 1}`)).length;
      const isModuleDone = (chCompletedCount === topics.length && topics.length > 0);

      return `
        <div class="card border-0 shadow-sm rounded-4 bg-white overflow-hidden dir-module-card" data-stage="${stageNum}">
          <!-- Module Header Bar -->
          <div class="p-3.5 px-4 border-bottom bg-light d-flex align-items-center justify-content-between flex-wrap gap-2">
            <div class="d-flex align-items-center gap-2.5 flex-wrap">
              <span class="badge bg-${stageColor} ${stageNum === 3 ? 'text-dark' : 'text-white'} stage-badge-pill">
                ${escapeHtml(stageBadge)}
              </span>
              <h5 class="fw-bold text-dark mb-0">Module ${chNum}: ${escapeHtml(ch.title)}</h5>
            </div>
            <div class="d-flex align-items-center gap-2">
              <span class="badge ${isModuleDone ? 'bg-success' : 'bg-white text-muted border'} rounded-pill px-3 py-1 small">
                ${chCompletedCount}/${topics.length} Topics Solved
              </span>
              ${realWorld.domain ? `
                <span class="badge bg-secondary-subtle text-secondary border rounded-pill px-2.5 py-1 small">
                  🏢 ${escapeHtml(realWorld.domain)}
                </span>
              ` : ''}
            </div>
          </div>

          <div class="card-body p-4">
            <!-- Real-World Application Snippet -->
            ${realWorld.where_applied ? `
              <div class="p-3 mb-3.5 rounded-3 bg-light border small">
                <div class="d-flex align-items-center gap-2 mb-1">
                  <span class="text-primary fw-bold">📍 Real-World Project Application:</span>
                  <span class="text-muted" style="font-size: 0.78rem;">(${escapeHtml(realWorld.companies || 'Industry Enterprise')})</span>
                </div>
                <div class="text-secondary" style="font-size: 0.82rem; line-height: 1.5;">${escapeHtml(realWorld.where_applied)}</div>
              </div>
            ` : ''}

            <!-- Topics List for this Module -->
            <div class="d-flex flex-column gap-2 mb-2">
              ${topics.map((t, tIdx) => {
                const topicId = `topic-${chNum}-${tIdx + 1}`;
                const isDone = completedTopics.includes(topicId);
                const isCurrent = (mIdx === currentModuleIdx && tIdx === currentTopicIdx);

                return `
                  <div class="topic-list-item ${isDone ? 'is-completed' : ''} dir-topic-row" data-topic-search="${escapeHtml(t.toLowerCase())}">
                    <div class="d-flex align-items-center gap-3 flex-grow-1">
                      <span class="badge ${isDone ? 'bg-success text-white' : 'bg-light text-secondary border'} rounded-circle d-flex align-items-center justify-content-center" style="width: 28px; height: 28px; font-size: 0.75rem;">
                        ${isDone ? '✓' : `${tIdx + 1}`}
                      </span>
                      <div>
                        <div class="fw-semibold text-dark small mb-0">${escapeHtml(t)}</div>
                        <small class="text-muted" style="font-size: 0.72rem;">Module ${chNum} &bull; ${escapeHtml(stageBadge)}</small>
                      </div>
                    </div>

                    <div class="d-flex align-items-center gap-2 flex-shrink-0">
                      ${isDone ? `
                        <span class="badge bg-success-subtle text-success border border-success-subtle rounded-pill px-2.5 py-1 small">Completed</span>
                      ` : ''}
                      <button type="button" class="btn btn-sm ${isCurrent ? 'btn-primary' : 'btn-outline-primary'} rounded-pill px-3 py-1 fw-bold" onclick="openTopicLesson(${mIdx}, ${tIdx})">
                        <span>Learn Topic</span>
                        <span>➔</span>
                      </button>
                    </div>
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        </div>
      `;
    }).join('');
  }

  window.filterDirectoryStage = function (stage, btn) {
    activeFilterStage = String(stage);
    document.querySelectorAll(".filter-stage-btn").forEach(b => {
      b.classList.remove("btn-primary", "btn-success", "btn-warning", "btn-danger", "active");
      b.classList.add("btn-outline-secondary");
    });
    btn.classList.remove("btn-outline-secondary");
    btn.classList.add("btn-primary", "active");

    const cards = document.querySelectorAll(".dir-module-card");
    cards.forEach(c => {
      const cStage = c.getAttribute("data-stage");
      if (activeFilterStage === "all" || cStage === activeFilterStage) {
        c.style.display = "block";
      } else {
        c.style.display = "none";
      }
    });
  };

  window.searchDirectoryTopics = function (q) {
    const query = (q || "").trim().toLowerCase();
    const rows = document.querySelectorAll(".dir-topic-row");
    rows.forEach(r => {
      const text = r.getAttribute("data-topic-search") || "";
      if (!query || text.includes(query)) {
        r.style.display = "flex";
      } else {
        r.style.display = "none";
      }
    });
  };

  // =========================================================================
  // VIEW 2: STEP-BY-STEP LESSON STUDIO (Interactive Player)
  // =========================================================================

  function renderCurrentTopic() {
    if (!curriculumData || !allTopicsList.length) return;

    const curItem = allTopicsList.find(x => x.moduleIdx === currentModuleIdx && x.topicIdx === currentTopicIdx) || allTopicsList[0];
    if (!curItem) return;

    const currentIndex = allTopicsList.indexOf(curItem);
    const totalTopics = allTopicsList.length;
    const isCompleted = completedTopics.includes(curItem.topicId);

    // Update Stage Badge & Tab Label
    const elStage = document.getElementById("page-stage-badge");
    const elStatus = document.getElementById("page-topic-status-badge");
    const activeTabLabel = document.getElementById("active-lesson-tab-label");

    if (elStage) {
      elStage.textContent = curItem.stageBadge;
      elStage.className = `badge ${curItem.stageNum === 1 ? 'bg-success' : curItem.stageNum === 2 ? 'bg-primary' : curItem.stageNum === 3 ? 'bg-warning text-dark' : 'bg-danger'} text-white px-2.5 py-0.5 rounded-pill small fw-bold`;
    }
    if (elStatus) {
      if (isCompleted) {
        elStatus.className = "badge bg-success text-white rounded-pill px-2.5 py-0.5 small";
        elStatus.innerHTML = "✓ Completed";
      } else {
        elStatus.className = "badge bg-info text-dark rounded-pill px-2.5 py-0.5 small";
        elStatus.innerHTML = "In Progress";
      }
    }
    if (activeTabLabel) {
      activeTabLabel.textContent = `Lesson Studio: Topic ${currentIndex + 1}`;
    }

    // Active Stage Ladder Highlight
    for (let s = 1; s <= 4; s++) {
      const ladderItem = document.getElementById(`stage-ladder-${s}`);
      if (ladderItem) {
        if (s === curItem.stageNum) {
          ladderItem.style.background = "rgba(59, 130, 246, 0.25)";
          ladderItem.style.borderColor = "#3b82f6";
        } else if (s < curItem.stageNum) {
          ladderItem.style.background = "rgba(16, 185, 129, 0.15)";
          ladderItem.style.borderColor = "#10b981";
        } else {
          ladderItem.style.background = "rgba(255, 255, 255, 0.06)";
          ladderItem.style.borderColor = "rgba(255, 255, 255, 0.15)";
        }
      }
    }

    // Render Lesson Container
    const container = document.getElementById("lesson-content-container");
    if (container) {
      const ch = curItem.chapter;
      const realWorld = ch.real_world_application || {};
      const sections = ch.sections || {};
      const concept = sections.concept || ch.key_takeaways || "";
      const examples = sections.solved_examples || [];
      const example = examples.length > 0 ? examples[currentTopicIdx % examples.length] : null;
      const practiceQuestions = sections.practice_questions || [];
      const question = practiceQuestions.length > 0 ? practiceQuestions[currentTopicIdx % practiceQuestions.length] : null;

      container.innerHTML = `
        <!-- BREADCRUMBS & TOPIC HEADING -->
        <div class="mb-4">
          <div class="d-flex align-items-center gap-2 text-muted small mb-2 flex-wrap">
            <span class="badge ${curItem.stageNum === 1 ? 'bg-success' : curItem.stageNum === 2 ? 'bg-primary' : curItem.stageNum === 3 ? 'bg-warning text-dark' : 'bg-danger'} text-white rounded-pill px-2.5 py-0.5" style="font-size: 0.72rem;">
              ${escapeHtml(curItem.stageBadge)}
            </span>
            <span>•</span>
            <span class="fw-semibold text-dark">Module ${curItem.chapterNum}: ${escapeHtml(ch.title)}</span>
            <span>•</span>
            <span class="badge bg-light text-secondary border">Topic ${curItem.topicIdx + 1} of ${(ch.topics || []).length}</span>
          </div>
          <h2 class="fw-bold text-dark mb-2" style="letter-spacing: -0.4px;">${escapeHtml(curItem.topicTitle)}</h2>
          <p class="text-secondary small mb-0" style="line-height: 1.65; max-width: 900px;">
            Step-by-step topic mastery: begin with core syntax and engineering fundamentals, examine how top tech companies deploy it in production, walk through working implementation code, and test your retention.
          </p>
        </div>

        <!-- SECTION 1: CORE FUNDAMENTALS & CONCEPTUAL FOUNDATION -->
        <div class="card border-0 shadow-sm p-4 mb-4 rounded-4" style="background: #ffffff; border-left: 5px solid #3b82f6 !important;">
          <div class="d-flex align-items-center justify-content-between mb-3 flex-wrap gap-2">
            <div class="d-flex align-items-center gap-2">
              <span class="fs-4">💡</span>
              <h5 class="fw-bold text-dark mb-0">1. Core Fundamentals &amp; Mechanics</h5>
            </div>
            <span class="badge bg-primary-subtle text-primary border border-primary-subtle rounded-pill px-2.5 py-1 small fw-semibold">Step 1: Theory &amp; Foundations</span>
          </div>
          <div class="text-dark small" style="line-height: 1.85; white-space: pre-line; font-size: 0.94rem;">
            ${escapeHtml(concept)}
          </div>
        </div>

        <!-- SECTION 2: REAL-WORLD PROJECT APPLICATION (HOW & WHERE USED IN INDUSTRY) -->
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
            Practical engineering insights: how senior software engineers architect and leverage this concept in live customer-facing systems.
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

        <!-- SECTION 3: WORKING CODE DEMONSTRATION & IMPLEMENTATION -->
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
              <pre class="p-3.5 bg-dark text-light rounded-3 font-monospace small mb-0 overflow-auto" style="max-height: 320px; font-size: 0.85rem; line-height: 1.6;"><code>${escapeHtml(example.code_or_math || '')}</code></pre>
            </div>

            ${example.explanation ? `
              <div class="alert alert-light border small mb-0 text-secondary">
                <strong>💡 Code Walkthrough:</strong> ${escapeHtml(example.explanation)}
              </div>
            ` : ''}
          </div>
        ` : ''}

        <!-- SECTION 4: INTERACTIVE KNOWLEDGE CHECK & PRACTICE CHALLENGE -->
        ${question ? `
          <div class="card border-0 shadow-sm p-4 mb-4 rounded-4" style="background: #ffffff; border-left: 5px solid #f59e0b !important;">
            <div class="d-flex align-items-center justify-content-between mb-3 flex-wrap gap-2">
              <div class="d-flex align-items-center gap-2">
                <span class="fs-4">📝</span>
                <h5 class="fw-bold text-dark mb-0">4. Interactive Knowledge Check &amp; Practice Challenge</h5>
              </div>
              <span class="badge bg-warning-subtle text-dark border border-warning-subtle rounded-pill px-2.5 py-1 small fw-bold">Test Understanding</span>
            </div>

            <p class="text-dark fw-semibold small mb-3" style="font-size: 0.93rem;">
              ${escapeHtml(question.question || question.title || 'Review the conceptual challenge below:')}
            </p>

            ${question.options && question.options.length ? `
              <div class="d-flex flex-column gap-2 mb-3">
                ${question.options.map((opt, oIdx) => `
                  <div class="quiz-option-btn" 
                       onclick="selectQuizOption(this, ${oIdx === question.answer ? 'true' : 'false'})">
                    <span class="badge bg-white border text-dark rounded-circle px-2 py-1">${String.fromCharCode(65 + oIdx)}</span>
                    <span class="small text-secondary flex-grow-1">${escapeHtml(opt)}</span>
                  </div>
                `).join('')}
              </div>
            ` : ''}

            <div class="d-flex align-items-center gap-2">
              <button type="button" class="btn btn-sm btn-outline-warning rounded-pill px-3 py-1.5 fw-semibold" onclick="toggleSolutionBox(${curItem.chapterNum}, ${curItem.topicIdx})">
                👁️ Reveal Solution &amp; Architectural Explanation
              </button>
            </div>

            <div id="solution-box-${curItem.chapterNum}-${curItem.topicIdx}" class="mt-3 p-3 bg-light rounded-3 border small" style="display: none;">
              <div class="fw-bold text-success mb-1">✓ Solution &amp; Architectural Explanation:</div>
              <div class="text-secondary" style="line-height: 1.6;">${escapeHtml(question.explanation || question.answer || 'Review key fundamentals and practical safeguards above to solidify this topic.')}</div>
            </div>
          </div>
        ` : ''}
      `;
    }

    // Bottom Navigation Bar
    const btnPrev = document.getElementById("btn-bottom-prev");
    if (btnPrev) {
      btnPrev.disabled = (currentIndex <= 0);
    }

    const counter = document.getElementById("bottom-topic-counter");
    if (counter) {
      counter.textContent = `Topic ${currentIndex + 1} of ${totalTopics} • ${Math.round((completedTopics.length / totalTopics) * 100)}% Completed`;
    }

    const btnMarkToggle = document.getElementById("btn-bottom-mark-toggle");
    if (btnMarkToggle) {
      if (isCompleted) {
        btnMarkToggle.className = "btn btn-success rounded-pill px-3 py-2 fw-semibold";
        btnMarkToggle.innerHTML = "<span>✓ Completed</span>";
      } else {
        btnMarkToggle.className = "btn btn-outline-primary rounded-pill px-3 py-2 fw-semibold";
        btnMarkToggle.innerHTML = "<span>Mark Complete</span>";
      }
    }

    const btnNext = document.getElementById("btn-bottom-next");
    const btnNextText = document.getElementById("btn-bottom-next-text");
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
  }

  function renderCurriculumOutline() {
    const container = document.getElementById("outline-modules-list");
    if (!container || !curriculumData?.chapters) return;

    const stats = document.getElementById("outline-summary-stats");
    if (stats) {
      stats.textContent = `${curriculumData.chapters.length} Modules • ${allTopicsList.length} Topics`;
    }

    container.innerHTML = curriculumData.chapters.map((ch, mIdx) => {
      const chNum = ch.chapter_num || (mIdx + 1);
      const topics = (ch.topics && ch.topics.length) ? ch.topics : [ch.title];
      const isCurrentModule = (mIdx === currentModuleIdx);
      const chCompletedCount = topics.filter((_, tIdx) => completedTopics.includes(`topic-${chNum}-${tIdx + 1}`)).length;
      const isModuleDone = (chCompletedCount === topics.length && topics.length > 0);

      return `
        <div class="card border rounded-3 mb-2 outline-module-card ${isCurrentModule ? 'border-primary shadow-sm bg-white' : 'bg-light'}">
          <div class="p-2.5 d-flex align-items-center justify-content-between cursor-pointer" onclick="toggleOutlineModule(${mIdx})" style="cursor: pointer;">
            <div>
              <span class="badge ${ch.progression_stage === 1 ? 'bg-success' : ch.progression_stage === 2 ? 'bg-primary' : ch.progression_stage === 3 ? 'bg-warning text-dark' : 'bg-danger'} rounded-pill px-2 py-0.5 me-1" style="font-size: 0.65rem;">
                Stage ${ch.progression_stage || (chNum <= 2 ? 1 : chNum <= 5 ? 2 : chNum <= 7 ? 3 : 4)}
              </span>
              <strong class="small text-dark" style="font-size: 0.8rem;">Module ${chNum}</strong>
              <div class="text-truncate text-secondary" style="max-width: 200px; font-size: 0.74rem;">${escapeHtml(ch.title)}</div>
            </div>
            <span class="badge ${isModuleDone ? 'bg-success' : 'bg-white text-muted border'} rounded-pill" style="font-size: 0.68rem;">
              ${chCompletedCount}/${topics.length}
            </span>
          </div>

          <div class="p-1.5 border-top ${isCurrentModule ? 'd-block' : 'd-none'}" id="outline-sublist-${mIdx}">
            ${topics.map((t, tIdx) => {
              const tId = `topic-${chNum}-${tIdx + 1}`;
              const isDone = completedTopics.includes(tId);
              const isActive = (mIdx === currentModuleIdx && tIdx === currentTopicIdx);

              return `
                <div class="topic-nav-sidebar-item ${isActive ? 'active' : isDone ? 'completed' : ''}" 
                     data-search="${escapeHtml(t.toLowerCase())}"
                     onclick="openTopicLesson(${mIdx}, ${tIdx})">
                  <div class="d-flex align-items-center gap-1.5 text-truncate me-2">
                    <span>${isDone ? '✓' : isActive ? '▶' : `${tIdx + 1}.`}</span>
                    <span class="text-truncate">${escapeHtml(t)}</span>
                  </div>
                  ${isActive ? '<span class="badge bg-white text-primary rounded-pill small" style="font-size: 0.62rem;">Active</span>' : ''}
                </div>
              `;
            }).join('')}
          </div>
        </div>
      `;
    }).join('');
  }

  function updateProgressBars() {
    const total = allTopicsList.length || 1;
    const completedCount = completedTopics.filter(id => allTopicsList.some(t => t.topicId === id)).length;
    const pct = Math.min(100, Math.round((completedCount / total) * 100));

    const topBar = document.getElementById("top-progress-bar");
    const topPct = document.getElementById("top-progress-percent");
    if (topBar) topBar.style.width = `${pct}%`;
    if (topPct) topPct.textContent = `${pct}%`;
  }

  function renderErrorState(msg) {
    const container = document.getElementById("all-modules-directory-list");
    if (container) {
      container.innerHTML = `
        <div class="text-center py-5">
          <div class="fs-1 text-danger mb-2">⚠️</div>
          <h5 class="fw-bold text-dark">Course Curriculum Unavailable</h5>
          <p class="text-muted small">${escapeHtml(msg)}</p>
          <a href="candidate-dashboard.html" class="btn btn-primary rounded-pill px-4 mt-2">Return to Dashboard</a>
        </div>
      `;
    }
  }

  // =========================================================================
  // ACTIONS & NAVIGATION
  // =========================================================================

  window.openTopicLesson = function (mIdx, tIdx) {
    currentModuleIdx = mIdx;
    currentTopicIdx = tIdx;

    renderCurrentTopic();
    renderCurriculumOutline();
    updateProgressBars();

    // Switch to Lesson Studio Tab
    const lessonTabBtn = document.getElementById("tab-lesson-studio-btn");
    if (lessonTabBtn && typeof bootstrap !== "undefined") {
      const tab = bootstrap.Tab.getOrCreateInstance(lessonTabBtn);
      tab.show();
    }
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  window.switchToAllTopicsTab = function () {
    const allTabBtn = document.getElementById("tab-all-topics-btn");
    if (allTabBtn && typeof bootstrap !== "undefined") {
      const tab = bootstrap.Tab.getOrCreateInstance(allTabBtn);
      tab.show();
    }
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  window.startLearningFromBeginning = function () {
    const firstUncompleted = allTopicsList.find(t => !completedTopics.includes(t.topicId));
    if (firstUncompleted) {
      openTopicLesson(firstUncompleted.moduleIdx, firstUncompleted.topicIdx);
    } else {
      openTopicLesson(0, 0);
    }
  };

  window.completeAndGoToNextTopic = async function () {
    if (!allTopicsList.length) return;

    const curItem = allTopicsList.find(x => x.moduleIdx === currentModuleIdx && x.topicIdx === currentTopicIdx);
    if (curItem) {
      if (!completedTopics.includes(curItem.topicId)) {
        completedTopics.push(curItem.topicId);
        try {
          if (typeof api !== "undefined" && api.studyMaterials && typeof api.studyMaterials.completeTopic === "function") {
            api.studyMaterials.completeTopic({ topic_id: curItem.topicId, phase_num: curItem.stageNum });
          }
        } catch (e) {
          console.warn("Failed to mark topic complete via API:", e);
        }
      }
    }

    const currentIndex = allTopicsList.indexOf(curItem);
    if (currentIndex < allTopicsList.length - 1) {
      const nextItem = allTopicsList[currentIndex + 1];
      openTopicLesson(nextItem.moduleIdx, nextItem.topicIdx);
    } else {
      alert("🎉 Fantastic achievement! You have mastered all topics in this course from core foundations to enterprise-scale deployment!");
      renderCurrentTopic();
      renderAllTopicsDirectory();
      renderCurriculumOutline();
      updateProgressBars();
    }
  };

  window.goToPreviousTopic = function () {
    if (!allTopicsList.length) return;
    const curItem = allTopicsList.find(x => x.moduleIdx === currentModuleIdx && x.topicIdx === currentTopicIdx);
    const currentIndex = allTopicsList.indexOf(curItem);
    if (currentIndex > 0) {
      const prevItem = allTopicsList[currentIndex - 1];
      openTopicLesson(prevItem.moduleIdx, prevItem.topicIdx);
    }
  };

  window.toggleCurrentTopicComplete = async function () {
    if (!allTopicsList.length) return;
    const curItem = allTopicsList.find(x => x.moduleIdx === currentModuleIdx && x.topicIdx === currentTopicIdx);
    if (!curItem) return;

    const idx = completedTopics.indexOf(curItem.topicId);
    if (idx >= 0) {
      completedTopics.splice(idx, 1);
    } else {
      completedTopics.push(curItem.topicId);
    }

    try {
      if (typeof api !== "undefined" && api.studyMaterials && typeof api.studyMaterials.completeTopic === "function") {
        api.studyMaterials.completeTopic({ topic_id: curItem.topicId, phase_num: curItem.stageNum });
      }
    } catch (e) {
      console.warn("API toggle error:", e);
    }

    renderCurrentTopic();
    renderAllTopicsDirectory();
    renderCurriculumOutline();
    updateProgressBars();
  };

  window.toggleOutlineModule = function (mIdx) {
    const el = document.getElementById(`outline-sublist-${mIdx}`);
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

  window.toggleSolutionBox = function (chNum, tIdx) {
    const el = document.getElementById(`solution-box-${chNum}-${tIdx}`);
    if (el) {
      el.style.display = (el.style.display === "none" || !el.style.display) ? "block" : "none";
    }
  };

  window.selectQuizOption = function (el, isCorrect) {
    const parent = el.closest(".d-flex.flex-column");
    if (parent) {
      parent.querySelectorAll(".quiz-option-btn").forEach(item => {
        item.classList.remove("selected-correct", "selected-incorrect");
      });
    }
    if (isCorrect) {
      el.classList.add("selected-correct");
    } else {
      el.classList.add("selected-incorrect");
    }
  };

  window.filterOutlineTopics = function (query) {
    const q = (query || "").trim().toLowerCase();
    const items = document.querySelectorAll(".topic-nav-sidebar-item");
    items.forEach(item => {
      const text = item.getAttribute("data-search") || "";
      if (!q || text.includes(q)) {
        item.style.display = "flex";
      } else {
        item.style.display = "none";
      }
    });
  };

  // Auto-init on page load
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initCourseLearning);
  } else {
    initCourseLearning();
  }

  document.addEventListener("ar:auth-ready", () => {
    initCourseLearning();
  });
})();
