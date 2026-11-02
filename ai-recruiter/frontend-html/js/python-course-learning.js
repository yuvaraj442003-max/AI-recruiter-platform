/**
 * python-course-learning.js — Dedicated Python Course Learning Controller
 * Connects the 10-module, 49-topic Python curriculum:
 * - Stage-gate progression from basics to placement-ready
 * - Comprehensive 5-section lesson studio for each topic
 * - Directory view with real-time search & stage filtering
 * - Completion tracking with localStorage and backend API sync
 */

(function () {
  "use strict";

  // HTML Escape helper
  function escapeHtml(str) {
    if (str === null || str === undefined) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  let modulesData = [];
  let allTopicsList = [];
  let currentTopicIndex = 0;
  let completedTopics = [];
  let activeStageFilter = "all";
  let activeSearchQuery = "";

  // Initialize
  async function initPythonLearning() {
    // 1. Load modules from python-course-data.js
    if (window.PYTHON_COURSE_DATA && Array.isArray(window.PYTHON_COURSE_DATA)) {
      modulesData = window.PYTHON_COURSE_DATA;
    } else {
      console.error("PYTHON_COURSE_DATA not found on window!");
      const container = document.getElementById("lesson-content-container");
      if (container) {
        container.innerHTML = `<div class="alert alert-danger p-4 rounded-4">Error: Python curriculum data could not be loaded.</div>`;
      }
      return;
    }

    // 2. Flatten all topics into indexed array
    allTopicsList = [];
    modulesData.forEach((mod, mIdx) => {
      (mod.topics || []).forEach((top, tIdx) => {
        allTopicsList.push({
          globalIndex: allTopicsList.length,
          topicNum: top.topicNum,
          moduleIdx: mIdx,
          topicIdx: tIdx,
          module: mod,
          topic: top,
          topicId: `python-t-${top.topicNum}`
        });
      });
    });

    const badge = document.getElementById("all-topics-count-badge");
    if (badge) badge.textContent = `${allTopicsList.length} Topics`;

    // 3. Load completed topics from localStorage
    try {
      const stored = localStorage.getItem("python_course_completed_topics");
      if (stored) {
        completedTopics = JSON.parse(stored) || [];
      }
    } catch (e) {
      completedTopics = [];
    }

    // 4. Also fetch student journey from API if authenticated
    try {
      if (typeof api !== "undefined" && api.studyMaterials && typeof api.studyMaterials.getLearningJourney === "function") {
        const journeyRes = await api.studyMaterials.getLearningJourney();
        if (journeyRes && journeyRes.data && Array.isArray(journeyRes.data.completed_topics)) {
          // Merge completed topics
          journeyRes.data.completed_topics.forEach(t => {
            if (!completedTopics.includes(t)) completedTopics.push(t);
          });
        }
      }
    } catch (err) {
      console.warn("Could not sync with backend journey API:", err);
    }

    // 5. Determine active topic from URL query params or first uncompleted
    const urlParams = new URLSearchParams(window.location.search);
    const qTopicNum = urlParams.get("topic");
    const qModuleNum = urlParams.get("module");
    const qTab = urlParams.get("tab");

    if (qTopicNum !== null) {
      const tNum = parseInt(qTopicNum, 10);
      const match = allTopicsList.find(x => x.topicNum === tNum);
      if (match) currentTopicIndex = match.globalIndex;
    } else if (qModuleNum !== null) {
      const mNum = parseInt(qModuleNum, 10);
      const match = allTopicsList.find(x => x.module.moduleNum === mNum);
      if (match) currentTopicIndex = match.globalIndex;
    } else {
      // Find first uncompleted topic
      const firstUncompleted = allTopicsList.find(x => !completedTopics.includes(x.topicId));
      if (firstUncompleted) {
        currentTopicIndex = firstUncompleted.globalIndex;
      } else {
        currentTopicIndex = 0;
      }
    }

    // 6. Render UI
    renderAllTopicsDirectory();
    renderCurrentTopic();
    renderCurriculumOutline();
    updateProgressBars();

    // If tab=studio or topic specified, switch to lesson studio tab
    if (qTab === "studio" || qTopicNum !== null) {
      switchToLessonStudioTab();
    }
  }

  // Render All Topics Directory (Tab 1)
  function renderAllTopicsDirectory() {
    const container = document.getElementById("modules-directory-container");
    if (!container) return;

    let html = "";
    let visibleModulesCount = 0;

    modulesData.forEach((mod, mIdx) => {
      // Filter topics inside module
      const filteredTopics = (mod.topics || []).filter(top => {
        // Stage filter
        if (activeStageFilter !== "all" && mod.stageNum !== parseInt(activeStageFilter, 10)) {
          return false;
        }
        // Search filter
        if (activeSearchQuery) {
          const q = activeSearchQuery.toLowerCase();
          const matchesTitle = (top.title || "").toLowerCase().includes(q);
          const matchesExp = (top.explanation || "").toLowerCase().includes(q);
          const matchesDomain = (top.realTimeProjectTask?.domain || "").toLowerCase().includes(q);
          const matchesComp = (top.realTimeProjectTask?.companies || "").toLowerCase().includes(q);
          return matchesTitle || matchesExp || matchesDomain || matchesComp;
        }
        return true;
      });

      if (filteredTopics.length === 0) return;
      visibleModulesCount++;

      // Count completed topics in module
      const modTopicIds = (mod.topics || []).map(t => `python-t-${t.topicNum}`);
      const modCompletedCount = modTopicIds.filter(id => completedTopics.includes(id)).length;
      const modProgressPct = modTopicIds.length > 0 ? Math.round((modCompletedCount / modTopicIds.length) * 100) : 0;
      const stageColor = mod.stageNum === 1 ? "success" : mod.stageNum === 2 ? "primary" : mod.stageNum === 3 ? "warning" : "danger";

      html += `
        <div class="card border-0 shadow-sm rounded-4 overflow-hidden bg-white mb-3">
          <!-- Module Header -->
          <div class="card-header bg-white border-bottom p-4">
            <div class="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-2">
              <div class="d-flex align-items-center gap-2 flex-wrap">
                <span class="badge bg-${stageColor} text-white px-3 py-1 rounded-pill small fw-bold">
                  ${escapeHtml(mod.stageBadge)}
                </span>
                <span class="badge bg-light text-secondary border px-2.5 py-1 rounded-pill small">
                  Module ${mod.moduleNum} of 10
                </span>
                <span class="badge bg-primary-subtle text-primary border border-primary-subtle rounded-pill px-2.5 py-1 small">
                  <i class="bi bi-briefcase me-1"></i>${escapeHtml(mod.domain)}
                </span>
              </div>
              <!-- Module Completion Stats -->
              <div class="d-flex align-items-center gap-2">
                <span class="small text-muted fw-semibold">${modCompletedCount} / ${modTopicIds.length} Done</span>
                <div class="progress" style="width: 80px; height: 6px;">
                  <div class="progress-bar bg-success" style="width: ${modProgressPct}%;"></div>
                </div>
                <span class="badge ${modProgressPct === 100 ? 'bg-success text-white' : 'bg-light text-secondary border'} rounded-pill small">
                  ${modProgressPct}%
                </span>
              </div>
            </div>
            <h5 class="fw-bold text-dark mb-0">${escapeHtml(mod.title)}</h5>
          </div>

          <!-- Topics Grid / List -->
          <div class="card-body p-3 p-md-4 bg-light bg-opacity-50">
            <div class="row g-3">
      `;

      filteredTopics.forEach(top => {
        const item = allTopicsList.find(x => x.topicNum === top.topicNum);
        const globalIdx = item ? item.globalIndex : 0;
        const topicId = `python-t-${top.topicNum}`;
        const isDone = completedTopics.includes(topicId);

        html += `
          <div class="col-12 col-md-6 col-xxl-6">
            <div class="topic-list-card ${isDone ? 'is-completed' : ''}" onclick="window.openTopicLesson(${globalIdx})">
              <div class="d-flex align-items-center gap-3">
                <span class="badge ${isDone ? 'bg-success text-white' : 'bg-light text-dark border'} rounded-circle d-flex align-items-center justify-content-center" style="width: 34px; height: 34px; font-size: 0.82rem; flex-shrink: 0;">
                  ${isDone ? '<i class="bi bi-check-lg fw-bold"></i>' : top.topicNum}
                </span>
                <div>
                  <div class="fw-bold text-dark mb-0.5" style="font-size: 0.92rem; line-height: 1.4;">
                    ${escapeHtml(top.title)}
                  </div>
                  <div class="d-flex align-items-center gap-2 flex-wrap text-muted" style="font-size: 0.75rem;">
                    <span><i class="bi bi-building me-1"></i>${escapeHtml(top.realTimeProjectTask?.companies || 'Tech Industry')}</span>
                    <span>•</span>
                    <span class="text-primary fw-semibold"><i class="bi bi-code-slash me-1"></i>Code &amp; Exercises</span>
                  </div>
                </div>
              </div>
              <button type="button" class="btn btn-sm ${isDone ? 'btn-outline-success' : 'btn-primary'} rounded-pill px-3 py-1 flex-shrink-0 fw-semibold">
                ${isDone ? '<i class="bi bi-check-circle me-1"></i>Review' : 'Start <i class="bi bi-arrow-right ms-1"></i>'}
              </button>
            </div>
          </div>
        `;
      });

      html += `
            </div>
          </div>
        </div>
      `;
    });

    if (visibleModulesCount === 0) {
      html = `
        <div class="card border-0 shadow-sm p-5 rounded-4 text-center bg-white">
          <div class="fs-1 text-muted mb-2">🔍</div>
          <h5 class="fw-bold text-dark">No topics match your filter</h5>
          <p class="text-muted small">Try searching for a different keyword or reset the stage filter.</p>
          <div>
            <button class="btn btn-outline-primary rounded-pill px-4" onclick="clearTopicSearch(); filterByStage('all');">Reset Filters</button>
          </div>
        </div>
      `;
    }

    container.innerHTML = html;
  }

  // Render Current Topic in Lesson Studio (Tab 2)
  function renderCurrentTopic() {
    const container = document.getElementById("lesson-content-container");
    if (!container || !allTopicsList.length) return;

    const currentItem = allTopicsList[currentTopicIndex];
    if (!currentItem) return;

    const mod = currentItem.module;
    const top = currentItem.topic;
    const isDone = completedTopics.includes(currentItem.topicId);
    const stageColor = mod.stageNum === 1 ? "success" : mod.stageNum === 2 ? "primary" : mod.stageNum === 3 ? "warning" : "danger";

    // Update Header Badges
    const elStageBadge = document.getElementById("page-stage-badge");
    if (elStageBadge) {
      elStageBadge.textContent = mod.stageBadge;
      elStageBadge.className = `badge bg-${stageColor} text-white rounded-pill px-2.5 py-0.5 small`;
    }

    const activeTabLabel = document.getElementById("active-lesson-tab-label");
    if (activeTabLabel) {
      activeTabLabel.textContent = `Lesson Studio: Topic ${top.topicNum} of ${allTopicsList.length}`;
    }

    // Bottom Navigation Buttons
    const elCounter = document.getElementById("bottom-topic-counter");
    if (elCounter) elCounter.textContent = `Topic ${top.topicNum} of ${allTopicsList.length}`;

    const btnPrev = document.getElementById("btn-bottom-prev");
    if (btnPrev) btnPrev.disabled = currentTopicIndex === 0;

    const btnNext = document.getElementById("btn-bottom-next");
    const btnNextText = document.getElementById("btn-bottom-next-text");
    if (btnNext) {
      if (currentTopicIndex === allTopicsList.length - 1) {
        if (btnNextText) btnNextText.innerHTML = "✓ Complete Entire Python Course!";
      } else {
        if (btnNextText) btnNextText.innerHTML = "✓ Complete &amp; Next Topic";
      }
    }

    const btnMarkText = document.getElementById("btn-bottom-mark-text");
    const btnMark = document.getElementById("btn-bottom-mark-toggle");
    if (btnMark && btnMarkText) {
      if (isDone) {
        btnMark.className = "btn btn-success rounded-pill px-3.5 py-2 fw-semibold d-flex align-items-center gap-1.5";
        btnMarkText.textContent = "✓ Completed";
      } else {
        btnMark.className = "btn btn-outline-primary rounded-pill px-3.5 py-2 fw-semibold d-flex align-items-center gap-1.5";
        btnMarkText.textContent = "Mark Complete";
      }
    }

    // Highlight Ladder Pill
    for (let s = 1; s <= 4; s++) {
      const ladder = document.getElementById(`ladder-stage-${s}`);
      if (ladder) {
        if (s === mod.stageNum) {
          ladder.classList.add("active");
        } else {
          ladder.classList.remove("active");
        }
      }
    }

    // Build the 5 Structured Sections
    container.innerHTML = `
      <!-- TOPIC HEADING & BREADCRUMBS -->
      <div class="mb-4">
        <div class="d-flex align-items-center gap-2 text-muted small mb-2 flex-wrap">
          <span class="badge bg-${stageColor} text-white rounded-pill px-2.5 py-0.5" style="font-size: 0.75rem;">
            ${escapeHtml(mod.stageBadge)}
          </span>
          <span>•</span>
          <span class="fw-semibold text-dark">Module ${mod.moduleNum}: ${escapeHtml(mod.title)}</span>
          <span>•</span>
          <span class="badge bg-light text-secondary border">Topic ${top.topicNum} of ${allTopicsList.length}</span>
          ${isDone ? '<span class="badge bg-success text-white rounded-pill"><i class="bi bi-check-circle me-1"></i>Completed</span>' : ''}
        </div>
        <h2 class="fw-bold text-dark mb-2" style="letter-spacing: -0.4px;">
          ${escapeHtml(top.title)}
        </h2>
        <div class="d-flex align-items-center gap-3 text-secondary small flex-wrap">
          <span><i class="bi bi-briefcase me-1 text-primary"></i><strong>Domain:</strong> ${escapeHtml(mod.domain)}</span>
          <span>•</span>
          <span><i class="bi bi-building me-1 text-success"></i><strong>Interview Target:</strong> ${escapeHtml(top.realTimeProjectTask?.companies || 'Top Tech Companies')}</span>
        </div>
      </div>

      <!-- ============================================================== -->
      <!-- SECTION 1: DETAILED EXPLANATION & RUNTIME MECHANICS -->
      <!-- ============================================================== -->
      <div class="card border-0 shadow-sm p-4 mb-4 rounded-4 bg-white" style="border-left: 5px solid #2563eb !important;">
        <div class="d-flex align-items-center justify-content-between mb-3 flex-wrap gap-2">
          <div class="d-flex align-items-center gap-2">
            <span class="fs-4">📘</span>
            <h5 class="fw-bold text-dark mb-0">1. Detailed Explanation &amp; Runtime Mechanics</h5>
          </div>
          <span class="badge bg-primary-subtle text-primary border border-primary-subtle rounded-pill px-3 py-1 fw-semibold small">
            Theoretical Foundations &amp; Architecture
          </span>
        </div>
        <div class="text-dark" style="line-height: 1.85; font-size: 0.94rem; white-space: pre-line;">
          ${escapeHtml(top.explanation)}
        </div>
      </div>

      <!-- ============================================================== -->
      <!-- SECTION 2: PRACTICAL CODING EXAMPLE & OUTPUT -->
      <!-- ============================================================== -->
      <div class="card border-0 shadow-sm p-4 mb-4 rounded-4 bg-white" style="border-left: 5px solid #0891b2 !important;">
        <div class="d-flex align-items-center justify-content-between mb-3 flex-wrap gap-2">
          <div class="d-flex align-items-center gap-2">
            <span class="fs-4">💻</span>
            <h5 class="fw-bold text-dark mb-0">2. Practical Coding Example &amp; Execution Walkthrough</h5>
          </div>
          <span class="badge bg-info-subtle text-info-emphasis border border-info-subtle rounded-pill px-3 py-1 fw-semibold small">
            Runnable Python Implementation
          </span>
        </div>
        <div class="fw-bold text-dark mb-2">${escapeHtml(top.codingExample.title)}</div>
        
        <!-- Code snippet with copy button -->
        <div class="position-relative mb-3">
          <button type="button" class="btn btn-sm btn-outline-light position-absolute top-0 end-0 m-2 rounded-pill px-2.5 py-0.5" style="z-index: 5; font-size: 0.75rem;" onclick="window.copyTextToClipboard('code-block-${top.topicNum}', this)">
            <i class="bi bi-clipboard me-1"></i>Copy Code
          </button>
          <pre class="code-editor-box mb-0" id="code-block-${top.topicNum}">${escapeHtml(top.codingExample.code)}</pre>
        </div>

        <p class="text-secondary small mb-2">
          <strong>Code Walkthrough:</strong> ${escapeHtml(top.codingExample.explanation)}
        </p>

        <!-- Output box -->
        <div class="mt-3">
          <div class="small fw-bold text-muted mb-1"><i class="bi bi-terminal me-1"></i>Standard Output (stdout):</div>
          <pre class="terminal-output-box mb-0">${escapeHtml(top.codingExample.output)}</pre>
        </div>
      </div>

      <!-- ============================================================== -->
      <!-- SECTION 3: HANDS-ON EXERCISE & LIVE SOLUTION -->
      <!-- ============================================================== -->
      <div class="card border-0 shadow-sm p-4 mb-4 rounded-4 bg-white" style="border-left: 5px solid #d97706 !important;">
        <div class="d-flex align-items-center justify-content-between mb-3 flex-wrap gap-2">
          <div class="d-flex align-items-center gap-2">
            <span class="fs-4">🛠️</span>
            <h5 class="fw-bold text-dark mb-0">3. Hands-On Exercise &amp; Live Solution</h5>
          </div>
          <span class="badge bg-warning-subtle text-warning-emphasis border border-warning-subtle rounded-pill px-3 py-1 fw-semibold small">
            Practical Challenge
          </span>
        </div>

        <div class="p-3 bg-light rounded-3 border mb-3">
          <h6 class="fw-bold text-dark mb-1">${escapeHtml(top.handsOnExercise.title)}</h6>
          <p class="text-secondary small mb-0" style="line-height: 1.65;">
            ${escapeHtml(top.handsOnExercise.problem)}
          </p>
        </div>

        <!-- Starter Code Template -->
        <div class="mb-3">
          <div class="small fw-bold text-muted mb-1"><i class="bi bi-code me-1"></i>Starter Template:</div>
          <pre class="code-editor-box mb-0" style="background: #1e293b;">${escapeHtml(top.handsOnExercise.starterCode)}</pre>
        </div>

        <!-- Reveal Solution Toggle -->
        <div class="mt-2">
          <button type="button" class="btn btn-outline-warning text-dark fw-bold rounded-pill px-3.5 py-1.5 shadow-sm d-flex align-items-center gap-2" onclick="window.toggleExerciseSolution(${top.topicNum})">
            <i class="bi bi-eye"></i>
            <span id="solution-toggle-btn-text-${top.topicNum}">Reveal Verified Solution &amp; Explanation</span>
          </button>

          <div id="exercise-solution-panel-${top.topicNum}" class="mt-3 p-3 bg-white border border-warning rounded-3 d-none">
            <div class="d-flex align-items-center justify-content-between mb-2">
              <span class="badge bg-success text-white rounded-pill px-2.5 py-0.5 small fw-bold">
                <i class="bi bi-check-circle me-1"></i>Verified Working Solution
              </span>
              <button type="button" class="btn btn-sm btn-outline-secondary rounded-pill px-2 py-0.5 small" onclick="window.copyTextToClipboard('sol-block-${top.topicNum}', this)">
                <i class="bi bi-clipboard"></i> Copy
              </button>
            </div>
            <pre class="code-editor-box mb-3" id="sol-block-${top.topicNum}">${escapeHtml(top.handsOnExercise.solution)}</pre>
            <div class="p-2.5 bg-light rounded-2 text-dark small" style="line-height: 1.6;">
              <strong>Step-by-Step Logic Breakdown:</strong> ${escapeHtml(top.handsOnExercise.explanation)}
            </div>
          </div>
        </div>
      </div>

      <!-- ============================================================== -->
      <!-- SECTION 4: REAL-TIME PROJECT TASK (HOW & WHERE USED IN INDUSTRY) -->
      <!-- ============================================================== -->
      <div class="card border-0 shadow-sm p-4 mb-4 rounded-4 bg-white" style="border-left: 5px solid #16a34a !important;">
        <div class="d-flex align-items-center justify-content-between mb-3 flex-wrap gap-2">
          <div class="d-flex align-items-center gap-2">
            <span class="fs-4">🚀</span>
            <h5 class="fw-bold text-dark mb-0">4. Real-Time Project Task (How &amp; Where Used in Real-Time Systems)</h5>
          </div>
          <span class="badge bg-success-subtle text-success border border-success-subtle rounded-pill px-3 py-1 fw-bold small">
            Industry Production Blueprint
          </span>
        </div>

        <div class="row g-3 mb-3">
          <div class="col-md-6">
            <div class="p-3 bg-light rounded-3 border h-100">
              <div class="d-flex align-items-center gap-1.5 text-primary fw-bold small mb-1.5">
                <i class="bi bi-building"></i>
                <span>Industry Domain &amp; Leading Companies:</span>
              </div>
              <div class="text-dark fw-semibold small mb-1">
                ${escapeHtml(top.realTimeProjectTask.domain)}
              </div>
              <div class="text-muted small">
                <strong>Employed by:</strong> ${escapeHtml(top.realTimeProjectTask.companies)}
              </div>
            </div>
          </div>

          <div class="col-md-6">
            <div class="p-3 bg-light rounded-3 border h-100">
              <div class="d-flex align-items-center gap-1.5 text-success fw-bold small mb-1.5">
                <i class="bi bi-gear-wide-connected"></i>
                <span>Live Production Scenario:</span>
              </div>
              <div class="text-secondary small" style="line-height: 1.6;">
                ${escapeHtml(top.realTimeProjectTask.productionScenario)}
              </div>
            </div>
          </div>
        </div>

        <div class="p-3 bg-light rounded-3 border mb-3">
          <div class="d-flex align-items-center gap-1.5 text-dark fw-bold small mb-1.5">
            <i class="bi bi-diagram-3"></i>
            <span>Architecture &amp; Implementation Guidance:</span>
          </div>
          <div class="text-secondary small" style="line-height: 1.7;">
            ${escapeHtml(top.realTimeProjectTask.implementationGuidance)}
          </div>
        </div>

        <div class="p-3 rounded-3 border border-danger border-opacity-25" style="background: #fef2f2;">
          <div class="d-flex align-items-center gap-1.5 text-danger fw-bold small mb-1">
            <i class="bi bi-exclamation-triangle-fill"></i>
            <span>Critical Production Safeguard:</span>
          </div>
          <div class="text-danger-emphasis small" style="line-height: 1.6;">
            ${escapeHtml(top.realTimeProjectTask.productionSafeguard)}
          </div>
        </div>
      </div>

      <!-- ============================================================== -->
      <!-- SECTION 5: CAMPUS PLACEMENT & TECHNICAL INTERVIEW PREPARATION -->
      <!-- ============================================================== -->
      <div class="card border-0 shadow-sm p-4 mb-4 rounded-4 bg-white" style="border-left: 5px solid #9333ea !important;">
        <div class="d-flex align-items-center justify-content-between mb-3 flex-wrap gap-2">
          <div class="d-flex align-items-center gap-2">
            <span class="fs-4">🎯</span>
            <h5 class="fw-bold text-dark mb-0">5. Campus Placement &amp; Technical Interview Preparation</h5>
          </div>
          <span class="badge bg-purple text-white rounded-pill px-3 py-1 fw-bold small" style="background: #9333ea;">
            Top Company Hiring Rounds
          </span>
        </div>

        <p class="text-secondary small mb-3">
          High-frequency interview questions asked during technical rounds at leading tech employers, complete with model answers and evaluation tips:
        </p>

        <div class="d-flex flex-column gap-3">
          ${(top.interviewQuestions || []).map((iq, idx) => `
            <div class="p-3.5 bg-light rounded-3 border">
              <div class="d-flex align-items-center justify-content-between mb-2 flex-wrap gap-1">
                <span class="badge bg-dark text-white rounded-pill px-2.5 py-0.5 small fw-bold">
                  <i class="bi bi-building me-1"></i>${escapeHtml(iq.company)} Interview Question
                </span>
                <span class="text-muted small">Question ${idx + 1}</span>
              </div>
              <h6 class="fw-bold text-dark mb-2">${escapeHtml(iq.question)}</h6>
              <div class="p-3 bg-white rounded-2 border text-dark small mb-2" style="line-height: 1.7;">
                <strong class="text-success"><i class="bi bi-chat-left-quote me-1"></i>Model Answer:</strong><br>
                ${escapeHtml(iq.answer)}
              </div>
              <div class="d-flex align-items-center gap-1.5 text-primary small" style="font-size: 0.8rem;">
                <i class="bi bi-lightbulb-fill text-warning"></i>
                <strong>Interviewer Evaluation Tip:</strong>
                <span>${escapeHtml(iq.interviewerTip)}</span>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;

    // Re-render sidebar outline to highlight active item
    renderCurriculumOutline();
  }

  // Render Sidebar Topic Navigation Outline
  function renderCurriculumOutline() {
    const container = document.getElementById("outline-modules-list");
    if (!container) return;

    let html = "";
    modulesData.forEach((mod, mIdx) => {
      const modTopicIds = (mod.topics || []).map(t => `python-t-${t.topicNum}`);
      const modCompletedCount = modTopicIds.filter(id => completedTopics.includes(id)).length;
      const isCurrentModule = allTopicsList[currentTopicIndex]?.moduleIdx === mIdx;

      html += `
        <div class="border rounded-3 p-2 bg-light bg-opacity-50">
          <div class="d-flex align-items-center justify-content-between mb-1.5 px-1">
            <span class="fw-bold text-dark small" style="font-size: 0.8rem;">Module ${mod.moduleNum}: ${escapeHtml(mod.title.slice(0, 30))}...</span>
            <span class="badge ${modCompletedCount === modTopicIds.length ? 'bg-success text-white' : 'bg-secondary bg-opacity-25 text-dark'} rounded-pill" style="font-size: 0.68rem;">
              ${modCompletedCount}/${modTopicIds.length}
            </span>
          </div>
          <div class="d-flex flex-column gap-1">
      `;

      (mod.topics || []).forEach(top => {
        const item = allTopicsList.find(x => x.topicNum === top.topicNum);
        const globalIdx = item ? item.globalIndex : 0;
        const topicId = `python-t-${top.topicNum}`;
        const isDone = completedTopics.includes(topicId);
        const isActive = globalIdx === currentTopicIndex;

        html += `
          <div class="sidebar-topic-item ${isActive ? 'active' : ''} ${isDone ? 'completed' : ''}" onclick="window.openTopicLesson(${globalIdx})">
            <div class="d-flex align-items-center gap-1.5 text-truncate">
              <span class="small fw-bold" style="min-width: 20px;">${top.topicNum}.</span>
              <span class="text-truncate">${escapeHtml(top.title)}</span>
            </div>
            ${isDone ? '<i class="bi bi-check-circle-fill text-success" style="font-size: 0.85rem;"></i>' : '<i class="bi bi-chevron-right text-muted" style="font-size: 0.7rem;"></i>'}
          </div>
        `;
      });

      html += `
          </div>
        </div>
      `;
    });

    container.innerHTML = html;
  }

  // Update Top Progress Bar & Pedagogical Ladder
  function updateProgressBars() {
    const total = allTopicsList.length;
    const completedCount = completedTopics.length;
    const pct = total > 0 ? Math.round((completedCount / total) * 100) : 0;

    const bar = document.getElementById("top-progress-bar");
    if (bar) bar.style.width = `${pct}%`;

    const text = document.getElementById("top-progress-text");
    if (text) text.textContent = `${completedCount} / ${total} (${pct}%)`;

    // Update Pedagogical Ladder
    for (let s = 1; s <= 4; s++) {
      const btn = document.getElementById(`ladder-stage-${s}`);
      if (!btn) continue;
      const stageTopics = allTopicsList.filter(x => x.module.stageNum === s);
      const stageDone = stageTopics.filter(x => completedTopics.includes(x.topicId)).length;
      if (stageTopics.length > 0 && stageDone === stageTopics.length) {
        btn.classList.add("completed");
      }
    }
  }

  // Action: Open Topic in Lesson Studio
  window.openTopicLesson = function (globalIdx) {
    if (globalIdx < 0 || globalIdx >= allTopicsList.length) return;
    currentTopicIndex = globalIdx;

    renderCurrentTopic();
    renderCurriculumOutline();
    switchToLessonStudioTab();

    // Scroll to top of lesson
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  // Action: Toggle Current Topic Complete
  window.toggleCurrentTopicComplete = function () {
    const cur = allTopicsList[currentTopicIndex];
    if (!cur) return;

    const topicId = cur.topicId;
    const idx = completedTopics.indexOf(topicId);

    if (idx === -1) {
      completedTopics.push(topicId);
    } else {
      completedTopics.splice(idx, 1);
    }

    // Save to localStorage
    try {
      localStorage.setItem("python_course_completed_topics", JSON.stringify(completedTopics));
    } catch (e) {}

    // Sync with backend API in background
    try {
      if (typeof api !== "undefined" && api.studyMaterials && typeof api.studyMaterials.completeCurriculumTopic === "function") {
        api.studyMaterials.completeCurriculumTopic({
          course_id: "python",
          topic_id: topicId,
          completed: idx === -1
        }).catch(() => {});
      }
    } catch (err) {}

    renderCurrentTopic();
    renderAllTopicsDirectory();
    renderCurriculumOutline();
    updateProgressBars();
  };

  // Action: Complete and Go to Next Topic
  window.completeAndGoToNextTopic = function () {
    const cur = allTopicsList[currentTopicIndex];
    if (cur) {
      if (!completedTopics.includes(cur.topicId)) {
        completedTopics.push(cur.topicId);
        try {
          localStorage.setItem("python_course_completed_topics", JSON.stringify(completedTopics));
        } catch (e) {}

        try {
          if (typeof api !== "undefined" && api.studyMaterials && typeof api.studyMaterials.completeCurriculumTopic === "function") {
            api.studyMaterials.completeCurriculumTopic({
              course_id: "python",
              topic_id: cur.topicId,
              completed: true
            }).catch(() => {});
          }
        } catch (err) {}
      }
    }

    if (currentTopicIndex < allTopicsList.length - 1) {
      currentTopicIndex++;
      window.openTopicLesson(currentTopicIndex);
    } else {
      renderCurrentTopic();
      updateProgressBars();
      alert("🎉 Outstanding Achievement! You have completed all 49 topics in the Python Programming Placement Track!");
    }
  };

  // Action: Go to Previous Topic
  window.goToPreviousTopic = function () {
    if (currentTopicIndex > 0) {
      currentTopicIndex--;
      window.openTopicLesson(currentTopicIndex);
    }
  };

  // Action: Toggle Exercise Solution Panel
  window.toggleExerciseSolution = function (topicNum) {
    const panel = document.getElementById(`exercise-solution-panel-${topicNum}`);
    const btnText = document.getElementById(`solution-toggle-btn-text-${topicNum}`);
    if (!panel) return;

    if (panel.classList.contains("d-none")) {
      panel.classList.remove("d-none");
      if (btnText) btnText.textContent = "Hide Solution";
    } else {
      panel.classList.add("d-none");
      if (btnText) btnText.textContent = "Reveal Verified Solution & Explanation";
    }
  };

  // Action: Filter Directory by Stage
  window.filterByStage = function (stageNum) {
    activeStageFilter = stageNum;

    // Update filter buttons
    document.querySelectorAll(".stage-filter-btn").forEach(btn => {
      if (btn.getAttribute("data-stage") === String(stageNum)) {
        btn.className = "btn btn-sm btn-primary rounded-pill px-3 fw-semibold stage-filter-btn active";
      } else {
        btn.className = "btn btn-sm btn-outline-secondary rounded-pill px-3 fw-semibold stage-filter-btn";
      }
    });

    // Update ladder buttons
    for (let s = 1; s <= 4; s++) {
      const ladder = document.getElementById(`ladder-stage-${s}`);
      if (ladder) {
        if (String(stageNum) === String(s)) {
          ladder.classList.add("active");
        } else {
          ladder.classList.remove("active");
        }
      }
    }

    renderAllTopicsDirectory();
    switchToAllTopicsTab();
  };

  window.setStageFilter = function (stageNum, btnEl) {
    activeStageFilter = stageNum;
    document.querySelectorAll(".stage-filter-btn").forEach(b => {
      b.className = "btn btn-sm btn-outline-secondary rounded-pill px-3 fw-semibold stage-filter-btn";
    });
    if (btnEl) btnEl.className = "btn btn-sm btn-primary rounded-pill px-3 fw-semibold stage-filter-btn active";
    renderAllTopicsDirectory();
  };

  // Action: Search Filter
  window.handleTopicSearch = function (query) {
    activeSearchQuery = (query || "").trim();
    renderAllTopicsDirectory();
  };

  window.clearTopicSearch = function () {
    const input = document.getElementById("topic-search-input");
    if (input) input.value = "";
    activeSearchQuery = "";
    renderAllTopicsDirectory();
  };

  // Filter Outline Topics in Sidebar
  window.filterOutlineTopics = function (query) {
    const q = (query || "").toLowerCase();
    document.querySelectorAll(".sidebar-topic-item").forEach(item => {
      const txt = item.textContent.toLowerCase();
      item.style.display = txt.includes(q) ? "flex" : "none";
    });
  };

  // Helper: Tab Switching
  window.switchToLessonStudioTab = function () {
    const tabBtn = document.getElementById("tab-lesson-studio-btn");
    if (tabBtn) {
      const bsTab = bootstrap.Tab.getOrCreateInstance(tabBtn);
      bsTab.show();
    }
  };

  window.switchToAllTopicsTab = function () {
    const tabBtn = document.getElementById("tab-all-topics-btn");
    if (tabBtn) {
      const bsTab = bootstrap.Tab.getOrCreateInstance(tabBtn);
      bsTab.show();
    }
  };

  // Helper: Copy Text to Clipboard
  window.copyTextToClipboard = function (elementId, btnEl) {
    const el = document.getElementById(elementId);
    if (!el) return;
    const text = el.innerText || el.textContent;
    navigator.clipboard.writeText(text).then(() => {
      const origHtml = btnEl.innerHTML;
      btnEl.innerHTML = '<i class="bi bi-check2"></i> Copied!';
      setTimeout(() => {
        btnEl.innerHTML = origHtml;
      }, 2000);
    }).catch(err => {
      console.warn("Clipboard copy failed:", err);
    });
  };

  // Auto-init on DOM Ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initPythonLearning);
  } else {
    initPythonLearning();
  }

})();
