/**
 * aptitude-test.js — Powers the interactive Aptitude Practice Lab,
 * Test Runner, Timer, and Scorecard Modal.
 */
(function () {
  if (!Session.isLoggedIn()) {
    window.location.href = "login.html";
    return;
  }

  const user = Session.getUser();
  if (user && user.role !== "candidate") {
    window.location.href = dashboardUrlForRole(user.role);
    return;
  }

  // DOM Elements - Lobby
  const lobbyView = document.getElementById("lobby-view");
  const runnerView = document.getElementById("runner-view");
  const companyTestsList = document.getElementById("company-tests-list");
  const topicsList = document.getElementById("topics-list");
  const historyBody = document.getElementById("attempt-history-body");
  const dailySprintBtn = document.getElementById("start-daily-sprint-btn");
  const weeklySprintBtn = document.getElementById("start-weekly-sprint-btn");
  const alertBox = document.getElementById("aptitude-alert");

  // DOM Elements - Runner
  const qNumBadge = document.getElementById("runner-q-num-badge");
  const subtopicBadge = document.getElementById("runner-subtopic-badge");
  const difficultyBadge = document.getElementById("runner-difficulty-badge");
  const companyTag = document.getElementById("runner-company-tag");
  const qText = document.getElementById("runner-question-text");
  const optionsContainer = document.getElementById("runner-options-container");
  const paletteContainer = document.getElementById("runner-palette-container");
  const timerDisplay = document.getElementById("runner-timer-display");
  const prevBtn = document.getElementById("runner-prev-btn");
  const nextBtn = document.getElementById("runner-next-btn");
  const clearBtn = document.getElementById("runner-clear-btn");
  const submitBtn = document.getElementById("runner-submit-btn");
  const quitBtn = document.getElementById("runner-quit-btn");

  // DOM Elements - Result Modal
  const resultModalEl = document.getElementById("testResultModal");
  const resultModal = new bootstrap.Modal(resultModalEl);
  const resultScoreText = document.getElementById("result-score-text");
  const resultPassedBadge = document.getElementById("result-passed-badge");
  const resultFeedbackText = document.getElementById("result-feedback-text");
  const resCorrectCount = document.getElementById("res-correct-count");
  const resWrongCount = document.getElementById("res-wrong-count");
  const resPercentile = document.getElementById("res-percentile");
  const resultReviewList = document.getElementById("result-review-list");

  // State
  let currentTest = null;
  let questions = [];
  let currentIndex = 0;
  let answers = {}; // question_id -> option_index
  let timerInterval = null;
  let secondsRemaining = 0;
  let totalTestSeconds = 0;

  // Initialize
  loadLobbyData();

  if (dailySprintBtn) {
    dailySprintBtn.addEventListener("click", startDailySprint);
  }
  if (weeklySprintBtn) {
    weeklySprintBtn.addEventListener("click", startWeeklySprint);
  }

  if (prevBtn) prevBtn.addEventListener("click", () => navigateQuestion(currentIndex - 1));
  if (nextBtn) nextBtn.addEventListener("click", () => navigateQuestion(currentIndex + 1));
  if (clearBtn) clearBtn.addEventListener("click", clearCurrentResponse);
  if (submitBtn) submitBtn.addEventListener("click", () => confirmSubmit());
  if (quitBtn) quitBtn.addEventListener("click", () => confirmQuit());

  // Check URL params for weekly challenge or topic direct launch
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get("mode") === "weekly") {
    setTimeout(startWeeklySprint, 100);
  }
  const topicParam = urlParams.get("topic");
  if (topicParam) {
    setTimeout(() => startTopicPractice(topicParam, topicParam), 150);
  }

  window.returnToLobby = function () {
    resultModal.hide();
    runnerView.classList.add("d-none");
    lobbyView.classList.remove("d-none");
    loadLobbyData();
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  let loadedTopics = [];
  let currentTopicFilter = "all";

  async function loadLobbyData() {
    try {
      // 0. Load Weekly Overview for Banner & Schedule
      try {
        if (api.weekly) {
          const wkRes = await api.weekly.getOverview();
          const wk = wkRes?.data;
          if (wk?.schedule) {
            const sBadge = document.getElementById("weekly-apt-schedule-badge");
            if (sBadge) sBadge.textContent = `🔄 Updated Weekly Once • Refreshes in ${wk.schedule.days_remaining}d ${wk.schedule.hours_remaining}h`;
          }
          if (wk?.aptitude) {
            const badge = document.getElementById("weekly-apt-lobby-badge");
            if (badge) badge.textContent = wk.week_label || wk.current_week_code;
            const title = document.getElementById("weekly-apt-lobby-title");
            if (title && wk.aptitude.title) title.textContent = wk.aptitude.title;
            const descEl = document.getElementById("weekly-apt-lobby-desc");
            if (descEl && wk.aptitude.description) descEl.textContent = wk.aptitude.description;
            const durationEl = document.getElementById("weekly-apt-lobby-duration");
            if (durationEl) {
              const mins = wk.aptitude.duration_minutes || Math.ceil((wk.aptitude.total_questions * 30) / 60) || 5;
              durationEl.textContent = `⏱️ ${mins} Mins (30s / question)`;
            }
            const qCountEl = document.getElementById("weekly-apt-lobby-qcount");
            if (qCountEl) {
              qCountEl.textContent = `📝 ${wk.aptitude.total_questions || 10} Questions`;
            }
            const statusBadge = document.getElementById("weekly-apt-lobby-user-status");
            if (statusBadge && wk.aptitude.user_completed) {
              statusBadge.className = `badge ${wk.aptitude.user_passed ? 'bg-success' : 'bg-warning text-dark'} py-1 px-2.5 rounded-pill small`;
              statusBadge.textContent = `Completed (${wk.aptitude.user_score_percentage}%)`;
              if (weeklySprintBtn) weeklySprintBtn.textContent = "🔄 Retake Weekly Challenge";
            }
          }
          // Populate Weekly Focus Badge
          const focusObj = wk?.aptitude_weekly_focus || wk?.schedule?.aptitude_weekly_focus;
          const focusBadge = document.getElementById("weekly-apt-focus-badge");
          if (focusBadge && focusObj) {
            focusBadge.textContent = `🎯 Active Topic: ${focusObj.name} (${focusObj.chapters || focusObj.section || ''})`;
          }
        }
      } catch (e) {
        // Fallback gracefully
      }

      // 1. Load Company & Grand Mock Tests
      const testsRes = await api.aptitude.getTests();
      renderCompanyTests(testsRes.data || []);

      // 2. Load Topics (Prefer weekly curated tracks if available)
      let topics = [];
      try {
        if (api.weekly?.getAptitudeTopics) {
          const weeklyAptRes = await api.weekly.getAptitudeTopics();
          topics = weeklyAptRes?.data || [];
        }
      } catch (e) {}

      if (!topics.length) {
        const topicsRes = await api.aptitude.getTopics();
        topics = topicsRes.data || [];
      }
      loadedTopics = topics;
      const countEl = document.getElementById("apt-topics-count-badge");
      if (countEl) countEl.textContent = `${loadedTopics.length} Placement Tracks Aligned with RS Aggarwal Aptitude & Reasoning Syllabus (41 Chapters)`;
      
      initTopicFilters();
      applyTopicFilter();

      // 3. Load Past Attempt History
      const historyRes = await api.aptitude.getHistory();
      renderHistory(historyRes.data || []);

      // 4. Load Weekly Syllabus Modal Content
      loadSyllabusModal();
    } catch (err) {
      showError(err.message || "Failed to load practice tests.");
    }
  }

  function initTopicFilters() {
    const filterBtns = document.querySelectorAll(".apt-filter-btn");
    filterBtns.forEach(btn => {
      btn.onclick = () => {
        filterBtns.forEach(b => {
          b.classList.remove("active", "btn-primary");
          b.classList.add("btn-outline-secondary");
        });
        btn.classList.add("active", "btn-primary");
        btn.classList.remove("btn-outline-secondary");
        currentTopicFilter = btn.dataset.filter || "all";
        applyTopicFilter();
      };
    });
  }

  function applyTopicFilter() {
    let filtered = loadedTopics;
    if (currentTopicFilter !== "all") {
      filtered = loadedTopics.filter(t => {
        const sec = (t.section || "").toLowerCase();
        const filt = currentTopicFilter.toLowerCase();
        return sec.includes(filt) || filt.includes(sec);
      });
    }
    renderTopics(filtered);
  }

  async function loadSyllabusModal() {
    try {
      let curr = null;
      if (api.weekly?.getCurriculum) {
        const res = await api.weekly.getCurriculum();
        curr = res?.data;
      }
      if (!curr) return;

      const badge = document.getElementById("syllabus-active-week-badge");
      if (badge) badge.textContent = `Current Active: Week ${curr.week_number}`;

      const listEl = document.getElementById("syllabus-timeline-list");
      if (listEl && curr.full_curriculum) {
        listEl.innerHTML = curr.full_curriculum.map(track => {
          const isActive = (track.slug === curr.current_focus?.slug);
          return `
          <div class="list-group-item list-group-item-action p-3 rounded-3 mb-2 border ${isActive ? 'border-primary bg-primary bg-opacity-10 shadow-sm' : 'border-light bg-light'}">
            <div class="d-flex justify-content-between align-items-center mb-1 flex-wrap gap-1">
              <span class="badge ${isActive ? 'bg-primary fw-bold' : 'bg-secondary'} rounded-pill">
                ${isActive ? '🔥 ACTIVE FOCUS THIS WEEK' : `Rotation Track Cycle ${track.week_cycle}`}
              </span>
              <span class="badge bg-light text-dark border small">${escapeHtml(track.section)}</span>
            </div>
            <h6 class="fw-bold text-dark mb-1 d-flex align-items-center gap-2">
              <span>${track.icon}</span> ${escapeHtml(track.name)}
              <small class="text-muted fw-normal">(${escapeHtml(track.chapters)})</small>
            </h6>
            <p class="text-muted small mb-2">${escapeHtml(track.description)}</p>
            <div class="d-flex flex-wrap gap-1 mb-2">
              ${(track.subtopics || []).map(s => `<span class="badge bg-white text-secondary border small" style="font-size: 0.68rem;">${escapeHtml(s)}</span>`).join(' ')}
            </div>
            <div class="d-flex justify-content-between align-items-center pt-2 border-top flex-wrap gap-2">
              <div class="d-flex gap-1 flex-wrap">
                ${(track.company_focus || []).map(c => `<span class="badge bg-info-subtle text-info border small" style="font-size: 0.65rem;">${escapeHtml(c)}</span>`).join(' ')}
              </div>
              <button class="btn btn-sm ${isActive ? 'btn-primary' : 'btn-outline-primary'} rounded-pill px-3 py-1" onclick="startTopicPractice('${track.slug}', '${escapeHtml(track.name)}')">
                Practice Track &rarr;
              </button>
            </div>
          </div>
          `;
        }).join("");
      }

      const startActBtn = document.getElementById("syllabus-start-active-btn");
      if (startActBtn) {
        startActBtn.onclick = () => {
          setTimeout(startWeeklySprint, 200);
        };
      }
    } catch (e) {
      console.warn("Could not load curriculum modal", e);
    }
  }

  function renderCompanyTests(tests) {
    if (!companyTestsList) return;
    if (!tests || !tests.length) {
      companyTestsList.innerHTML = `<div class="col-12 text-muted">No mock tests configured yet.</div>`;
      return;
    }

    companyTestsList.innerHTML = tests.map(t => {
      const isRecruiter = t.category === "recruiter_test";
      const badgeText = isRecruiter ? "🎯 Recruiter Assessment" : (t.company_name || "Campus Drive");
      const badgeClass = isRecruiter ? "bg-success-subtle text-success border border-success-subtle" : "bg-primary-subtle text-primary";
      const topicsHtml = (t.topics && t.topics.length)
        ? `<div class="mb-2 d-flex flex-wrap gap-1">${t.topics.slice(0, 3).map(top => `<span class="badge bg-light text-dark border small">${escapeHtml(top)}</span>`).join('')}${t.topics.length > 3 ? `<span class="badge bg-light text-muted border small">+${t.topics.length - 3}</span>` : ''}</div>`
        : '';
      const totalMarks = t.total_marks ? t.total_marks.toFixed(1) : (t.total_questions * (t.marks_per_question || 1)).toFixed(1);
      const durationMins = t.duration_minutes || Math.ceil((t.total_questions * 30) / 60) || 15;

      return `
      <div class="col-md-4">
        <div class="card h-100 border-0 shadow-sm hover-lift" style="border-radius: 16px;">
          <div class="card-body p-4 d-flex flex-column justify-content-between">
            <div>
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="badge ${badgeClass} fw-semibold px-2.5 py-1 rounded-pill">${escapeHtml(badgeText)}</span>
                <span class="text-muted small">⏱️ ${durationMins} mins</span>
              </div>
              <h5 class="fw-bold text-dark mb-2">${escapeHtml(t.title)}</h5>
              <p class="text-secondary small mb-2">${escapeHtml(t.description || "Comprehensive aptitude assessment.")}</p>
              ${topicsHtml}
            </div>
            <div class="d-flex justify-content-between align-items-center pt-3 border-top mt-auto">
              <span class="text-muted small"><strong>${t.total_questions}</strong> Qs • <strong>${totalMarks}</strong> Marks</span>
              <button class="btn btn-outline-primary btn-sm fw-semibold rounded-pill px-3" onclick="startTestById('${t.id}')">
                Take Test &rarr;
              </button>
            </div>
          </div>
        </div>
      </div>
    `;
    }).join("");
  }

  function renderTopics(topics) {
    if (!topicsList) return;
    if (!topics || !topics.length) {
      topicsList.innerHTML = `<div class="col-12 text-muted">No topics found in this category.</div>`;
      return;
    }

    topicsList.innerHTML = topics.map(top => {
      const coBadges = (top.company_focus || []).slice(0, 3)
        .map(c => `<span class="badge bg-primary-subtle text-primary border small" style="font-size: 0.68rem;">${escapeHtml(c)}</span>`)
        .join(' ');
      const subBadges = (top.subtopics || []).slice(0, 3)
        .map(s => `<span class="badge bg-light text-secondary border small" style="font-size: 0.68rem;">${escapeHtml(s)}</span>`)
        .join(' ');

      const isCurrentWeek = Boolean(top.is_current_week);

      return `
      <div class="col-md-6 col-lg-3">
        <div class="card h-100 border-0 shadow-sm text-center p-3 hover-lift d-flex flex-column justify-content-between ${isCurrentWeek ? 'border-primary border-2 shadow' : ''}" style="border-radius: 16px; ${isCurrentWeek ? 'border: 2px solid #4f46e5 !important;' : ''}">
          <div>
            ${isCurrentWeek ? '<div class="badge bg-warning text-dark fw-bold mb-2 shadow-sm rounded-pill px-2.5 py-1" style="font-size: 0.72rem;">🔥 Active Focus: This Week</div>' : ''}
            <div class="fs-1 mb-1">${top.icon || "📊"}</div>
            <h6 class="fw-bold text-dark mb-1">${escapeHtml(top.name)}</h6>
            ${top.chapters ? `<div class="badge bg-primary-subtle text-primary border small mb-1" style="font-size: 0.68rem;">${escapeHtml(top.chapters)}</div>` : ''}
            ${top.section ? `<div class="badge bg-light text-secondary border small mb-2 d-block mx-auto" style="font-size: 0.65rem; max-width: fit-content;">${escapeHtml(top.section)}</div>` : ''}
            <p class="text-muted small mb-2" style="min-height: 38px; line-height: 1.35; font-size: 0.8rem;">${escapeHtml(top.description || "")}</p>
            ${subBadges ? `<div class="d-flex flex-wrap justify-content-center gap-1 mb-2">${subBadges}</div>` : ''}
            ${coBadges ? `<div class="d-flex flex-wrap justify-content-center gap-1 mb-2">${coBadges}</div>` : ''}
          </div>
          <div>
            <div class="badge bg-light text-dark fw-medium py-1.5 px-3 rounded-pill mb-2 w-100">
              ${top.question_count || 10}+ Practice Questions
            </div>
            <button class="btn btn-sm ${isCurrentWeek ? 'btn-primary' : 'btn-outline-primary'} fw-semibold rounded-pill w-100 hover-lift" onclick="startTopicPractice('${top.slug || top.id}', '${escapeHtml(top.name)}')">
              Practice Track &rarr;
            </button>
          </div>
        </div>
      </div>
    `;
    }).join("");
  }

  function renderHistory(attempts) {
    if (!historyBody) return;
    if (!attempts || !attempts.length) {
      historyBody.innerHTML = `<tr><td colspan="6" class="text-center text-muted py-4">No tests attempted yet. Click 'Start Daily Sprint' above to test your skills!</td></tr>`;
      return;
    }

    historyBody.innerHTML = attempts.map(a => `
      <tr>
        <td class="fw-semibold text-dark">${escapeHtml(a.topic_name)}</td>
        <td>
          <span class="badge ${a.score_percentage >= 65 ? 'bg-success-subtle text-success' : 'bg-warning-subtle text-warning'} fw-bold px-2 py-1">
            ${a.score_percentage}%
          </span>
        </td>
        <td>${a.correct_count} / ${a.total_questions}</td>
        <td>${Math.round(a.time_taken_seconds / 60)}m ${a.time_taken_seconds % 60}s</td>
        <td>
          <span class="badge ${a.is_passed ? 'bg-success' : 'bg-secondary'} rounded-pill">
            ${a.is_passed ? 'Passed' : 'Needs Practice'}
          </span>
        </td>
        <td class="text-muted small">${a.created_at ? new Date(a.created_at).toLocaleDateString() : '-'}</td>
      </tr>
    `).join("");
  }

  window.startTopicPractice = async function (topicIdOrSlug, topicName) {
    clearError();
    try {
      if (api.weekly?.getTopicAptitudeQuestions && (topicIdOrSlug.includes("-") || ["quantitative-aptitude", "logical-reasoning", "verbal-ability", "data-interpretation-cs"].includes(topicIdOrSlug))) {
        try {
          const qRes = await api.weekly.getTopicAptitudeQuestions(topicIdOrSlug);
          const qList = qRes?.data || [];
          if (qList.length > 0) {
            currentTest = {
              id: topicIdOrSlug,
              title: topicName || "Placement Aptitude Practice",
              duration_minutes: Math.ceil((qList.length * 30) / 60) || 5,
              total_questions: qList.length,
              marks_per_question: 1,
              negative_marking: 0,
              passing_percentage: 60,
            };
            questions = qList;
            launchRunner();
            return;
          }
        } catch (subErr) {
          console.warn("Weekly topic fetch fallback:", subErr);
        }
      }

      const res = await api.aptitude.getTopicPractice(topicIdOrSlug);
      currentTest = res.data?.test;
      questions = res.data?.questions || [];
      launchRunner();
    } catch (err) {
      showError(err.message || `Failed to load questions for ${topicName || "topic"}.`);
    }
  };

  window.startTestById = async function (testId) {
    clearError();
    try {
      const res = await api.aptitude.getTest(testId);
      currentTest = res.data?.test;
      questions = res.data?.questions || [];
      launchRunner();
    } catch (err) {
      showError(err.message || "Failed to load the selected test.");
    }
  };

  async function startDailySprint() {
    clearError();
    try {
      const res = await api.aptitude.getDailySprint();
      currentTest = res.data?.test;
      questions = res.data?.questions || [];
      launchRunner();
    } catch (err) {
      showError(err.message || "Failed to start daily sprint.");
    }
  }

  async function startWeeklySprint() {
    clearError();
    try {
      const res = await api.weekly.getAptitudeCurrent();
      currentTest = res.data?.test;
      if (currentTest) currentTest.isWeekly = true;
      questions = res.data?.questions || [];
      launchRunner();
    } catch (err) {
      showError(err.message || "Failed to start weekly challenge.");
    }
  }

  function launchRunner() {
    clearError();
    if (!questions || !questions.length) {
      showError("This test has no questions configured.");
      return;
    }

    // Reset test state
    currentIndex = 0;
    answers = {};
    // Rule: Exactly 30 seconds per aptitude question (e.g. 10 questions = 300s = 5 mins)
    const secondsPerQuestion = 30;
    secondsRemaining = (questions && questions.length > 0)
      ? questions.length * secondsPerQuestion
      : ((currentTest?.duration_minutes || 5) * 60);
    totalTestSeconds = secondsRemaining;

    lobbyView.classList.add("d-none");
    runnerView.classList.remove("d-none");
    window.scrollTo({ top: 0, behavior: "smooth" });

    const titleEl = document.getElementById("runner-test-title");
    if (titleEl) titleEl.textContent = currentTest?.title || "Aptitude Assessment";
    const subTitleEl = document.getElementById("runner-test-subtitle");
    if (subTitleEl) subTitleEl.textContent = `${questions.length} Questions • Pace: 30s per question • Passing Cutoff: ${currentTest?.passing_percentage || 60}%`;

    renderPalette();
    renderQuestion(currentIndex);
    startTimer();
  }

  function startTimer() {
    clearInterval(timerInterval);
    updateTimerDisplay();

    timerInterval = setInterval(() => {
      secondsRemaining--;
      updateTimerDisplay();

      if (secondsRemaining <= 0) {
        clearInterval(timerInterval);
        alert("Time is up! Submitting your test automatically...");
        submitTest(true);
      }
    }, 1000);
  }

  function updateTimerDisplay() {
    const mins = Math.floor(secondsRemaining / 60);
    const secs = secondsRemaining % 60;
    timerDisplay.textContent = `${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;

    if (secondsRemaining < 30) {
      timerDisplay.className = "display-6 fw-bold font-monospace text-danger animate-pulse";
    } else if (secondsRemaining < 60) {
      timerDisplay.className = "display-6 fw-bold font-monospace text-warning";
    } else {
      timerDisplay.className = "display-6 fw-bold font-monospace text-white";
    }
  }

  function renderPalette() {
    if (!paletteContainer) return;
    paletteContainer.innerHTML = (questions || []).map((q, idx) => {
      if (!q) return "";
      const qId = q.id != null ? q.id : `q-${idx}`;
      const isAnswered = answers[qId] !== undefined;
      return `
        <button type="button" class="q-palette-btn ${idx === currentIndex ? 'current' : ''} ${isAnswered ? 'answered' : ''}" id="pal-btn-${idx}" onclick="navigateQuestion(${idx})">
          ${idx + 1}
        </button>
      `;
    }).join("");
  }

  function renderQuestion(index) {
    if (index < 0 || index >= questions.length) return;
    currentIndex = index;

    const q = questions[currentIndex];
    if (!q) return;

    qNumBadge.textContent = `Question ${currentIndex + 1} of ${questions.length} • ⏱️ 30s / question pace`;
    subtopicBadge.textContent = q.subtopic || "General";
    difficultyBadge.textContent = (q.difficulty || "medium").toUpperCase();
    companyTag.textContent = q.company_tag || "General Pattern";
    qText.textContent = q.question || "";

    // Render Options
    const qId = q.id != null ? q.id : `q-${currentIndex}`;
    optionsContainer.innerHTML = (q.options || []).map((opt, optIdx) => {
      const isSelected = answers[qId] === optIdx;
      return `
        <div class="test-option-card ${isSelected ? 'selected' : ''}" onclick="selectOption('${qId}', ${optIdx})">
          <div class="d-flex align-items-center gap-3">
            <span class="badge rounded-circle ${isSelected ? 'bg-primary text-white' : 'bg-light text-dark border'}" style="width: 28px; height: 28px; display: inline-flex; align-items: center; justify-content: center; font-weight: 700;">
              ${String.fromCharCode(65 + optIdx)}
            </span>
            <span class="fs-6 text-dark">${escapeHtml(opt)}</span>
          </div>
        </div>
      `;
    }).join("");

    // Update buttons
    prevBtn.disabled = currentIndex === 0;
    nextBtn.textContent = currentIndex === questions.length - 1 ? "Review & Finish" : "Next →";

    // Update palette focus ONLY within paletteContainer
    if (paletteContainer) {
      paletteContainer.querySelectorAll(".q-palette-btn").forEach((btn, idx) => {
        btn.classList.toggle("current", idx === currentIndex);
        const item = questions[idx];
        const itemId = item?.id != null ? item.id : `q-${idx}`;
        const isAnswered = answers[itemId] !== undefined;
        btn.classList.toggle("answered", isAnswered);
      });
    }
  }

  window.navigateQuestion = function (idx) {
    if (idx >= 0 && idx < questions.length) {
      renderQuestion(idx);
    }
  };

  window.selectOption = function (questionId, optionIndex) {
    if (questionId != null) {
      answers[questionId] = optionIndex;
    }
    renderQuestion(currentIndex);
  };

  function clearCurrentResponse() {
    const q = questions[currentIndex];
    const qId = q?.id != null ? q.id : `q-${currentIndex}`;
    delete answers[qId];
    renderQuestion(currentIndex);
  }

  function confirmQuit() {
    if (confirm("Are you sure you want to exit? Your current test progress will be lost.")) {
      clearInterval(timerInterval);
      runnerView.classList.add("d-none");
      lobbyView.classList.remove("d-none");
    }
  }

  function confirmSubmit() {
    const answeredCount = Object.keys(answers).length;
    const unansweredCount = questions.length - answeredCount;
    const msg = unansweredCount > 0
      ? `You have answered ${answeredCount} of ${questions.length} questions (${unansweredCount} unanswered). Do you want to submit now?`
      : `You have answered all ${questions.length} questions. Ready to submit?`;

    if (confirm(msg)) {
      submitTest();
    }
  }

  async function submitTest(isAuto = false) {
    clearInterval(timerInterval);
    const timeTaken = Math.max(1, totalTestSeconds - secondsRemaining);

    submitBtn.disabled = true;
    submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span> Evaluating...`;

    try {
      let res;
      if (currentTest?.isWeekly) {
        res = await api.weekly.submitAptitude({
          answers: answers,
          time_taken_seconds: timeTaken,
        });
      } else {
        const payload = {
          test_id: currentTest?.id ? String(currentTest.id) : null,
          topic_name: currentTest?.title || "Practice Test",
          time_taken_seconds: timeTaken,
          answers: answers,
          question_ids: (questions || []).map(q => q.id).filter(Boolean),
        };
        res = await api.aptitude.submit(payload);
      }
      showResultModal(res.data);
    } catch (err) {
      alert("Submission error: " + (err.message || "Failed to submit test."));
      submitBtn.disabled = false;
      submitBtn.textContent = "✓ Finish & Submit Test";
    }
  }

  function showResultModal(data) {
    submitBtn.disabled = false;
    submitBtn.textContent = "✓ Finish & Submit Test";

    resultScoreText.textContent = `${data.score_percentage}%`;
    resultPassedBadge.className = `badge ${data.is_passed ? 'bg-success' : 'bg-warning'} px-3 py-1 mb-2 fs-6`;
    resultPassedBadge.textContent = data.is_passed ? "PASSED CUTOFF" : "NEEDS PRACTICE";
    resultFeedbackText.textContent = data.feedback_message || "";

    resCorrectCount.textContent = data.correct_count;
    resWrongCount.textContent = data.wrong_count;
    resPercentile.textContent = `${data.percentile_estimate}%`;

    // Render Detailed Solutions
    resultReviewList.innerHTML = (data.questions_review || []).map((rev, idx) => {
      const isCorrect = rev.is_correct;
      const userChoiceStr = rev.user_selected_index !== null
        ? `${String.fromCharCode(65 + rev.user_selected_index)}. ${rev.options[rev.user_selected_index] || ''}`
        : "Unanswered";
      const correctChoiceStr = `${String.fromCharCode(65 + rev.correct_option_index)}. ${rev.options[rev.correct_option_index] || ''}`;

      return `
        <div class="card border ${isCorrect ? 'border-success-subtle bg-success-subtle/10' : 'border-danger-subtle bg-danger-subtle/10'} p-3" style="border-radius: 12px;">
          <div class="d-flex justify-content-between align-items-center mb-2">
            <span class="badge ${isCorrect ? 'bg-success' : 'bg-danger'} rounded-pill">
              Question ${idx + 1}: ${isCorrect ? '✓ Correct' : '✕ Incorrect'}
            </span>
            <span class="text-muted small">${escapeHtml(rev.subtopic || '')}</span>
          </div>
          <div class="fw-semibold text-dark mb-2">${escapeHtml(rev.question)}</div>
          <div class="small mb-1">
            <strong>Your Choice:</strong> <span class="${isCorrect ? 'text-success fw-bold' : 'text-danger'}">${escapeHtml(userChoiceStr)}</span>
          </div>
          <div class="small mb-2">
            <strong>Correct Answer:</strong> <span class="text-success fw-bold">${escapeHtml(correctChoiceStr)}</span>
          </div>
          ${rev.explanation ? `
            <div class="p-2.5 bg-white rounded border small text-secondary mt-2">
              <strong>💡 Explanation:</strong> ${escapeHtml(rev.explanation)}
            </div>
          ` : ''}
        </div>
      `;
    }).join("");

    resultModal.show();
  }

  function clearError() {
    if (!alertBox) return;
    alertBox.className = "alert alert-danger py-2 mb-4 d-none";
    alertBox.textContent = "";
  }

  function showError(msg) {
    if (!alertBox) return;
    alertBox.className = "alert alert-danger py-2 mb-4";
    alertBox.textContent = msg;
    alertBox.classList.remove("d-none");
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function escapeHtml(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }
})();
