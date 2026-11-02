/**
 * study-materials.js — Powers:
 * 1. Personalized Placement Learning Track & Topic Selection (Java, Python, DSA, SQL, Aptitude, OS, Custom Topics)
 * 2. Daily Placement Assessments (Strict 30s/q speed practice with streak tracking)
 * 3. Dynamic AI Practice Quizzes on chosen topics
 * 4. Placement Roadmaps & 12-Week Milestone Checklist
 * 5. Interactive Practice Drawer with step-by-step solutions
 * 6. Cheatsheets & Company Exam Guides Markdown Reader
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

  const userGreeting = document.getElementById("user-greeting");
  if (userGreeting && user) {
    userGreeting.textContent = `${user.name || "Candidate"} (${user.email || ""})`;
  }

  // DOM Elements - Roadmaps & Guides
  const roadmapsContainer = document.getElementById("roadmaps-container");
  const guidesGrid = document.getElementById("guides-grid");
  const companyGuidesGrid = document.getElementById("company-guides-grid");
  const filterBtns = document.querySelectorAll(".filter-btn");

  // Reader Modal Elements
  const articleModalEl = document.getElementById("articleReaderModal");
  const articleModal = articleModalEl ? new bootstrap.Modal(articleModalEl) : null;
  const modalCategoryBadge = document.getElementById("modal-category-badge");
  const modalArticleTitle = document.getElementById("modal-article-title");
  const modalReadTime = document.getElementById("modal-read-time");
  const modalDifficulty = document.getElementById("modal-difficulty");
  const modalCompanyTag = document.getElementById("modal-company-tag");
  const modalArticleBody = document.getElementById("modal-article-body");

  // Quiz Modal Elements (shared for milestone timed quiz & daily placement assessment)
  const quizModalEl = document.getElementById("milestoneQuizModal");
  const quizModal = quizModalEl ? new bootstrap.Modal(quizModalEl) : null;
  const quizModalBadge = document.getElementById("quiz-modal-badge");
  const quizModalTitle = document.getElementById("quiz-modal-title");
  const quizTimerPill = document.getElementById("quiz-timer-pill");
  const quizTimerText = document.getElementById("quiz-timer-text");
  const quizModalCloseBtn = document.getElementById("quiz-modal-close-btn");

  const quizLoadingView = document.getElementById("quiz-loading-view");
  const quizLoadingTitle = document.getElementById("quiz-loading-title");
  const quizLoadingSubtext = document.getElementById("quiz-loading-subtext");
  const quizTakingView = document.getElementById("quiz-taking-view");
  const quizResultsView = document.getElementById("quiz-results-view");

  const quizQCounter = document.getElementById("quiz-q-counter");
  const quizDifficultyBadge = document.getElementById("quiz-difficulty-badge");
  const quizMarksBadge = document.getElementById("quiz-marks-badge");
  const quizProgressBar = document.getElementById("quiz-progress-bar");
  const quizQText = document.getElementById("quiz-q-text");
  const quizOptionsContainer = document.getElementById("quiz-options-container");
  const quizPrevBtn = document.getElementById("quiz-prev-btn");
  const quizNextBtn = document.getElementById("quiz-next-btn");
  const quizSubmitBtn = document.getElementById("quiz-submit-btn");

  // Quiz Results Elements
  const resultsIcon = document.getElementById("results-icon");
  const resultsStatusBadge = document.getElementById("results-status-badge");
  const resultsTitle = document.getElementById("results-title");
  const resultsFeedbackMessage = document.getElementById("results-feedback-message");
  const resultsScoreDisplay = document.getElementById("results-score-display");
  const resultsPercentageDisplay = document.getElementById("results-percentage-display");
  const resultsTimeDisplay = document.getElementById("results-time-display");
  const resultsProgressAlert = document.getElementById("results-progress-alert");
  const resultsProgressAlertText = document.getElementById("results-progress-alert-text");
  const quizReviewList = document.getElementById("quiz-review-list");
  const resultsCloseBtn = document.getElementById("results-close-btn");
  const resultsAiBtn = document.getElementById("results-ai-btn");
  const resultsRetakeBtn = document.getElementById("results-retake-btn");

  // Practice Drawer Modal Elements
  const drawerModalEl = document.getElementById("milestonePracticeDrawerModal");
  const drawerModal = drawerModalEl ? new bootstrap.Modal(drawerModalEl) : null;
  const drawerSubjectBadge = document.getElementById("drawer-subject-badge");
  const drawerHoursBadge = document.getElementById("drawer-hours-badge");
  const drawerMilestoneTitle = document.getElementById("drawer-milestone-title");
  const drawerSubtopicsContainer = document.getElementById("drawer-subtopics-container");
  const drawerQuestionsCount = document.getElementById("drawer-questions-count");
  const drawerQuestionsContainer = document.getElementById("drawer-questions-container");
  const drawerStartTimedQuizBtn = document.getElementById("drawer-start-timed-quiz-btn");
  const drawerStartAiQuizBtn = document.getElementById("drawer-start-ai-quiz-btn");
  const drawerFooterQuizBtn = document.getElementById("drawer-footer-quiz-btn");
  const drawerFooterAiBtn = document.getElementById("drawer-footer-ai-btn");

  // Topic Selection & Track Elements
  const topicModalEl = document.getElementById("topicSelectorModal");
  const topicModal = topicModalEl ? new bootstrap.Modal(topicModalEl) : null;
  const activeTopicsChipsContainer = document.getElementById("active-topics-chips-container");
  const activeTopicsCount = document.getElementById("active-topics-count");
  const trackDailyStreak = document.getElementById("track-daily-streak");
  const quickCustomTopicInput = document.getElementById("quick-custom-topic-input");
  const curatedMaterialsGrid = document.getElementById("curated-materials-grid");
  const curatedPracticeQuestionsContainer = document.getElementById("curated-practice-questions-container");
  const curatedMaterialsCount = document.getElementById("curated-materials-count");
  const curatedQuestionsCount = document.getElementById("curated-questions-count");
  const modalTopicsCategoriesContainer = document.getElementById("modal-topics-categories-container");
  const modalCustomTopicsContainer = document.getElementById("modal-custom-topics-container");
  const modalSelectedCount = document.getElementById("modal-selected-count");
  const modalCustomTopicInput = document.getElementById("modal-custom-topic-input");

  // Prescribed Textbooks DOM Elements
  const bookChaptersModalEl = document.getElementById("bookChaptersModal");
  const bookChaptersModal = bookChaptersModalEl ? new bootstrap.Modal(bookChaptersModalEl) : null;
  const bookModalIcon = document.getElementById("book-modal-icon");
  const bookModalSubjectBadge = document.getElementById("book-modal-subject-badge");
  const bookModalEditionBadge = document.getElementById("book-modal-edition-badge");
  const bookModalTitle = document.getElementById("book-modal-title");
  const bookModalChaptersCount = document.getElementById("book-modal-chapters-count");
  const bookModalChaptersList = document.getElementById("book-modal-chapters-list");
  const bookModalOpenFullReaderBtn = document.getElementById("book-modal-open-full-reader-btn");
  const bookModalStartExamBtn = document.getElementById("book-modal-start-exam-btn");
  const bookModalFooterReadBtn = document.getElementById("book-modal-footer-read-btn");
  const bookModalFooterExamBtn = document.getElementById("book-modal-footer-exam-btn");
  const prescribedBooksCardsContainer = document.getElementById("prescribed-books-cards-container");

  // Application State
  let cachedRoadmaps = [];
  let allMaterials = [];
  let currentCategory = "all";
  let activeRoadmapSubjectFilter = "all";
  let activeRoadmapSearchQuery = "";
  let activeDrawerMilestone = null;
  let activeBookSubject = "Java";
  let activeBookSlug = "java-prescribed-textbook";
  let prescribedBooksData = [];

  // Topic Preferences State
  let availableTopicsCatalog = [];
  let studentPreferences = {
    selected_topics: [],
    custom_topics: [],
    all_active_topics: [],
    daily_streak: 1,
    last_assessment_date: null,
  };
  let modalDraftSelected = new Set();
  let modalDraftCustom = new Set();
  let modalSearchFilter = "";
  let activeSelectedTopicFilter = "all";

  // Active Quiz State (supports both milestone quiz & daily assessment)
  let activeQuiz = {
    quizType: "milestone", // "milestone" | "daily" | "ai"
    roadmapSlug: null,
    milestoneId: null,
    sessionId: null,
    questions: [],
    currentIndex: 0,
    answers: {},
    timeRemaining: 0,
    timerInterval: null,
    startTime: 0,
  };

  // Initialize
  init();

  async function init() {
    setupQuizModalListeners();
    loadTopicPreferences();
    loadAvailableTopics();
    loadPrescribedBooks();
    loadCuratedFeed();
    loadRoadmaps();
    loadMaterials();
    setupFilters();
    loadCompanyIntelligence();

    // Check if navigating to start learning directly
    const urlParams = new URLSearchParams(window.location.search);
    const startMode = urlParams.get("start") || urlParams.get("mode");
    const courseParam = urlParams.get("course") || urlParams.get("subject");
    if ((startMode === "true" || startMode === "learn") && courseParam) {
      window.location.href = `course-learning.html?course=${encodeURIComponent(courseParam)}`;
      return;
    }

    // Auto-switch tab if URL hash specified (#company-pane, #my-track-pane, etc.)
    const hash = window.location.hash;
    if (hash) {
      const tabTarget = document.querySelector(`[data-bs-target="${hash}"]`);
      if (tabTarget) {
        const tab = bootstrap.Tab.getOrCreateInstance(tabTarget);
        if (tab) tab.show();
      }
    }
  }

  // --------------------------------------------------------------------------
  // TOPIC PREFERENCES & CUSTOM LEARNING TRACK
  // --------------------------------------------------------------------------

  async function loadAvailableTopics() {
    try {
      const res = await api.studyMaterials.getAvailableTopics();
      availableTopicsCatalog = res.data || [];
    } catch (err) {
      console.error("Failed to load available topics catalog:", err);
    }
  }

  async function loadTopicPreferences() {
    try {
      const res = await api.studyMaterials.getTopicPreferences();
      studentPreferences = res.data || {
        selected_topics: ["Java", "Python", "Data Structures & Algorithms (DSA)", "SQL & Database Queries", "Quantitative Aptitude", "Logical Reasoning"],
        custom_topics: [],
        all_active_topics: ["Java", "Python", "Data Structures & Algorithms (DSA)", "SQL & Database Queries", "Quantitative Aptitude", "Logical Reasoning"],
        daily_streak: 1,
      };
      renderActiveTopicsChips();
      if (trackDailyStreak) trackDailyStreak.textContent = studentPreferences.daily_streak || 1;
    } catch (err) {
      console.error("Failed to load topic preferences:", err);
    }
  }

  function renderActiveTopicsChips() {
    if (!activeTopicsChipsContainer) return;
    const allTopics = studentPreferences.all_active_topics || [];
    if (activeTopicsCount) activeTopicsCount.textContent = allTopics.length;

    if (!allTopics.length) {
      activeTopicsChipsContainer.innerHTML = `<span class="text-muted small">No topics selected yet. Click "Choose Topics" to customize your track.</span>`;
      return;
    }

    const allPill = `
      <div 
        class="active-topic-pill all-pill ${activeSelectedTopicFilter === 'all' ? 'active-filter' : ''}" 
        onclick="selectTopicFilter('all')" 
        title="View study materials and questions across all your topics"
      >
        <span>🌟</span>
        <span>All Topics (${allTopics.length})</span>
      </div>
    `;

    const topicPills = allTopics.map(t => {
      const isCustom = (studentPreferences.custom_topics || []).includes(t);
      const isCurrentActive = activeSelectedTopicFilter.toLowerCase() === t.toLowerCase();
      return `
        <div 
          class="active-topic-pill ${isCustom ? 'custom-pill' : ''} ${isCurrentActive ? 'active-filter' : ''}" 
          onclick="selectTopicFilter('${escapeHtml(t)}')"
          title="Click to view ${escapeHtml(t)} materials & practice questions"
        >
          <span>${isCustom ? '✨' : '🎯'}</span>
          <span>${escapeHtml(t)}</span>
          ${isCustom ? '<span class="badge bg-purple-subtle text-purple border-0 small px-1.5" style="font-size: 0.7rem;">Custom</span>' : ''}
          <span class="remove-topic-btn ms-1" onclick="event.stopPropagation(); removeActiveTopic('${escapeHtml(t)}')" title="Remove topic">&times;</span>
        </div>
      `;
    }).join("");

    activeTopicsChipsContainer.innerHTML = allPill + topicPills;
  }

  window.selectTopicFilter = async function (topicName) {
    activeSelectedTopicFilter = topicName || "all";
    renderActiveTopicsChips();
    await loadPrescribedBooks(activeSelectedTopicFilter);
    await loadCuratedFeed(activeSelectedTopicFilter);

    // Smooth scroll down to the related materials section
    const anchor = document.getElementById("curated-materials-section-anchor");
    if (anchor) {
      anchor.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  window.removeActiveTopic = async function (topicName) {
    const newSelected = (studentPreferences.selected_topics || []).filter(t => t !== topicName);
    const newCustom = (studentPreferences.custom_topics || []).filter(t => t !== topicName);

    if (!newSelected.length && !newCustom.length) {
      alert("Please keep at least one learning topic active in your placement track.");
      return;
    }

    try {
      const res = await api.studyMaterials.saveTopicPreferences({
        selected_topics: newSelected,
        custom_topics: newCustom,
      });
      studentPreferences = res.data;
      renderActiveTopicsChips();
      loadCuratedFeed();
    } catch (err) {
      alert("Failed to update topics: " + err.message);
    }
  };

  window.addQuickCustomTopic = async function () {
    if (!quickCustomTopicInput) return;
    const val = quickCustomTopicInput.value.trim();
    if (!val) return;

    const currentSelected = studentPreferences.selected_topics || [];
    const currentCustom = studentPreferences.custom_topics || [];

    if (currentSelected.includes(val) || currentCustom.includes(val)) {
      alert(`"${val}" is already included in your active learning topics!`);
      return;
    }

    const updatedCustom = [...currentCustom, val];
    try {
      const res = await api.studyMaterials.saveTopicPreferences({
        selected_topics: currentSelected,
        custom_topics: updatedCustom,
      });
      studentPreferences = res.data;
      quickCustomTopicInput.value = "";
      renderActiveTopicsChips();
      loadCuratedFeed();
    } catch (err) {
      alert("Failed to add custom topic: " + err.message);
    }
  };

  // --------------------------------------------------------------------------
  // TOPIC SELECTOR MODAL
  // --------------------------------------------------------------------------

  window.openTopicSelectorModal = function () {
    if (!availableTopicsCatalog.length) {
      loadAvailableTopics();
    }

    modalDraftSelected = new Set(studentPreferences.selected_topics || []);
    modalDraftCustom = new Set(studentPreferences.custom_topics || []);
    modalSearchFilter = "";

    const searchInp = document.getElementById("modal-topic-search-input");
    if (searchInp) searchInp.value = "";

    renderModalCategoriesGrid();
    renderModalCustomChips();
    updateModalSelectedCounter();

    if (topicModal) topicModal.show();
  };

  function updateModalSelectedCounter() {
    if (modalSelectedCount) {
      modalSelectedCount.textContent = modalDraftSelected.size + modalDraftCustom.size;
    }
  }

  function renderModalCategoriesGrid() {
    if (!modalTopicsCategoriesContainer) return;

    // Group catalog by category
    const categoriesMap = {};
    availableTopicsCatalog.forEach(t => {
      const cat = t.category || "General Placement Topics";
      if (!categoriesMap[cat]) categoriesMap[cat] = [];
      categoriesMap[cat].push(t);
    });

    const filterQuery = (modalSearchFilter || "").toLowerCase();

    let html = "";
    for (const [catName, topics] of Object.entries(categoriesMap)) {
      const filtered = topics.filter(t => {
        if (!filterQuery) return true;
        const q = filterQuery;
        return t.name.toLowerCase().includes(q) ||
          (t.description || "").toLowerCase().includes(q) ||
          (t.subtopics_preview || []).some(st => st.toLowerCase().includes(q));
      });

      if (!filtered.length) continue;

      html += `
        <div class="mb-4">
          <div class="d-flex align-items-center gap-2 mb-2 pb-1 border-bottom">
            <h6 class="fw-bold text-dark mb-0">${escapeHtml(catName)}</h6>
            <span class="badge bg-light text-muted border small">${filtered.length} Subjects</span>
          </div>
          <div class="row g-3">
            ${filtered.map(t => {
              const isChecked = modalDraftSelected.has(t.name);
              return `
                <div class="col-md-6 col-lg-3">
                  <div 
                    class="topic-selector-card ${isChecked ? 'selected' : ''}" 
                    id="topic-card-${escapeHtml(t.id)}"
                    onclick="toggleModalTopic('${escapeHtml(t.name)}', '${escapeHtml(t.id)}')"
                  >
                    <div>
                      <div class="d-flex justify-content-between align-items-start mb-2">
                        <span class="fs-4">${t.icon || '🎯'}</span>
                        <input 
                          type="checkbox" 
                          class="form-check-input mt-0" 
                          id="topic-check-${escapeHtml(t.id)}"
                          ${isChecked ? 'checked' : ''} 
                          style="pointer-events: none; width: 1.2rem; height: 1.2rem;"
                        />
                      </div>
                      <h6 class="fw-bold text-dark mb-1">${escapeHtml(t.name)}</h6>
                      <p class="text-muted small mb-2 lh-sm" style="font-size: 0.78rem;">${escapeHtml(t.description || '')}</p>
                    </div>

                    <div>
                      <div class="d-flex flex-wrap gap-1">
                        ${(t.subtopics_preview || []).slice(0, 2).map(st => `
                          <span class="badge bg-light text-secondary border" style="font-size: 0.68rem;">${escapeHtml(st)}</span>
                        `).join("")}
                      </div>
                    </div>
                  </div>
                </div>
              `;
            }).join("")}
          </div>
        </div>
      `;
    }

    if (!html) {
      modalTopicsCategoriesContainer.innerHTML = `<div class="text-center py-4 text-muted small">No topics matched "${escapeHtml(modalSearchFilter)}".</div>`;
    } else {
      modalTopicsCategoriesContainer.innerHTML = html;
    }
  }

  window.filterModalTopicsCatalog = function (query) {
    modalSearchFilter = query;
    renderModalCategoriesGrid();
  };

  window.toggleModalTopic = function (topicName, topicId) {
    if (modalDraftSelected.has(topicName)) {
      modalDraftSelected.delete(topicName);
    } else {
      modalDraftSelected.add(topicName);
    }

    const card = document.getElementById(`topic-card-${topicId}`);
    const check = document.getElementById(`topic-check-${topicId}`);
    const isSelected = modalDraftSelected.has(topicName);

    if (card) card.classList.toggle("selected", isSelected);
    if (check) check.checked = isSelected;

    updateModalSelectedCounter();
  };

  function renderModalCustomChips() {
    if (!modalCustomTopicsContainer) return;
    const customs = Array.from(modalDraftCustom);
    if (!customs.length) {
      modalCustomTopicsContainer.innerHTML = `<span class="text-muted small">No custom topics added yet.</span>`;
      return;
    }

    modalCustomTopicsContainer.innerHTML = customs.map(t => `
      <span class="active-topic-pill custom-pill">
        <span>✨ ${escapeHtml(t)}</span>
        <span class="remove-topic-btn ms-1" onclick="removeModalCustomTopic('${escapeHtml(t)}')">&times;</span>
      </span>
    `).join("");
  }

  window.addModalCustomTopic = function () {
    if (!modalCustomTopicInput) return;
    const val = modalCustomTopicInput.value.trim();
    if (!val) return;

    if (modalDraftSelected.has(val) || modalDraftCustom.has(val)) {
      alert(`"${val}" is already selected!`);
      return;
    }

    modalDraftCustom.add(val);
    modalCustomTopicInput.value = "";
    renderModalCustomChips();
    updateModalSelectedCounter();
  };

  window.removeModalCustomTopic = function (topicName) {
    modalDraftCustom.delete(topicName);
    renderModalCustomChips();
    updateModalSelectedCounter();
  };

  window.selectPresetTopics = function (preset) {
    if (preset === "fresher") {
      modalDraftSelected = new Set([
        "Java",
        "Python",
        "Data Structures & Algorithms (DSA)",
        "SQL & Database Queries",
        "Quantitative Aptitude",
        "Logical Reasoning",
      ]);
    } else if (preset === "core_cs") {
      modalDraftSelected = new Set([
        "Java",
        "Python",
        "Data Structures & Algorithms (DSA)",
        "SQL & Database Queries",
        "DBMS (Database Management Systems)",
        "Operating Systems (OS)",
        "Computer Networks (CN)",
        "Object-Oriented Programming (OOP)",
      ]);
    } else if (preset === "ai_data") {
      modalDraftSelected = new Set([
        "Artificial Intelligence & Machine Learning (AI / ML)",
        "Data Engineering & Big Data",
        "Python",
        "SQL & Database Queries",
        "Data Structures & Algorithms (DSA)",
        "Quantitative Aptitude",
      ]);
    } else if (preset === "cloud_architecture") {
      modalDraftSelected = new Set([
        "Cloud Computing & Architecture",
        "Cloud & DevOps Fundamentals",
        "System Design Fundamentals",
        "Operating Systems (OS)",
        "Computer Networks (CN)",
        "Web Development (Full-Stack)",
      ]);
    }
    renderModalCategoriesGrid();
    updateModalSelectedCounter();
  };

  window.clearAllTopicsSelection = function () {
    modalDraftSelected.clear();
    modalDraftCustom.clear();
    renderModalCategoriesGrid();
    renderModalCustomChips();
    updateModalSelectedCounter();
  };

  window.saveTopicPreferencesFromModal = async function () {
    const selectedList = Array.from(modalDraftSelected);
    const customList = Array.from(modalDraftCustom);

    if (!selectedList.length && !customList.length) {
      alert("Please select at least one learning topic for your track.");
      return;
    }

    try {
      const res = await api.studyMaterials.saveTopicPreferences({
        selected_topics: selectedList,
        custom_topics: customList,
      });
      studentPreferences = res.data;
      if (topicModal) topicModal.hide();
      renderActiveTopicsChips();
      loadCuratedFeed();
    } catch (err) {
      alert("Failed to save learning topics: " + err.message);
    }
  };

  // --------------------------------------------------------------------------
  // PERSONALIZED LEARNING FEED (MATERIALS & PRACTICE QUESTIONS)
  // --------------------------------------------------------------------------

  async function loadCuratedFeed(topic = "all") {
    try {
      if (curatedMaterialsGrid) {
        curatedMaterialsGrid.innerHTML = `
          <div class="text-center py-4 text-muted small">
            <div class="spinner-border spinner-border-sm text-primary mb-2" role="status"></div>
            <div>Loading materials for ${escapeHtml(topic === 'all' ? 'your topics' : topic)}...</div>
          </div>
        `;
      }
      const res = await api.studyMaterials.getCuratedFeed(topic);
      const feed = res.data;
      renderCuratedFeed(feed);
    } catch (err) {
      console.error("Failed to load curated feed:", err);
    }
  }

  function renderCuratedFeed(feed) {
    if (!feed) return;

    // Filter Banner
    const bannerContainer = document.getElementById("curated-active-filter-banner-container");
    if (bannerContainer) {
      if (activeSelectedTopicFilter && activeSelectedTopicFilter !== "all") {
        bannerContainer.innerHTML = `
          <div class="alert alert-primary border-primary bg-primary-subtle d-flex flex-column flex-sm-row justify-content-between align-items-sm-center gap-3 mb-4 p-3.5 rounded-4 shadow-sm">
            <div class="d-flex align-items-center gap-3">
              <span class="fs-2">🎯</span>
              <div>
                <div class="fw-bold text-dark fs-6">Focused Learning Materials: <span class="text-primary">${escapeHtml(activeSelectedTopicFilter)}</span></div>
                <div class="text-secondary small">Viewing placement study guides, cheatsheets, and practice questions specific to <strong>${escapeHtml(activeSelectedTopicFilter)}</strong>.</div>
              </div>
            </div>
            <div class="d-flex gap-2 flex-shrink-0">
              ${feed.featured_guide_slug ? `
                <button class="btn btn-sm btn-primary rounded-pill px-3.5 py-1.5 fw-bold shadow-sm" onclick="openArticleModal('${escapeHtml(feed.featured_guide_slug)}')">
                  📖 Open ${escapeHtml(activeSelectedTopicFilter)} Guide &rarr;
                </button>
              ` : `
                <button class="btn btn-sm btn-primary rounded-pill px-3.5 py-1.5 fw-bold shadow-sm" onclick="openTopicGuideModal('${escapeHtml(activeSelectedTopicFilter)}')">
                  ✨ View ${escapeHtml(activeSelectedTopicFilter)} Guide &rarr;
                </button>
              `}
              <button class="btn btn-sm btn-outline-secondary rounded-pill px-3 py-1.5 fw-semibold bg-white" onclick="selectTopicFilter('all')">
                ✕ Show All Topics
              </button>
            </div>
          </div>
        `;
      } else {
        bannerContainer.innerHTML = "";
      }
    }

    // Materials Grid
    if (curatedMaterialsGrid) {
      const materials = feed.matched_materials || [];
      if (curatedMaterialsCount) curatedMaterialsCount.textContent = `${materials.length} Guides`;

      if (!materials.length) {
        curatedMaterialsGrid.innerHTML = `
          <div class="text-center py-4 bg-light rounded-4 border">
            <div class="fs-2 mb-2">📚</div>
            <p class="text-muted small mb-2">No study materials pre-indexed for "${escapeHtml(activeSelectedTopicFilter)}".</p>
            <button class="btn btn-sm btn-outline-primary rounded-pill px-3 fw-bold" onclick="openTopicGuideModal('${escapeHtml(activeSelectedTopicFilter)}')">
              ✨ Generate AI Placement Notes for ${escapeHtml(activeSelectedTopicFilter)}
            </button>
          </div>
        `;
      } else {
        curatedMaterialsGrid.innerHTML = materials.map(m => `
          <div class="p-3 border rounded-3 bg-light d-flex justify-content-between align-items-center gap-3">
            <div>
              <div class="d-flex align-items-center gap-2 mb-1">
                <span class="badge bg-primary-subtle text-primary small text-uppercase">${escapeHtml(m.category.replace('_', ' '))}</span>
                <span class="text-muted small">⏱️ ${escapeHtml(m.estimated_read_time || '10 mins')}</span>
              </div>
              <h6 class="fw-bold text-dark mb-1">${escapeHtml(m.title)}</h6>
              <p class="text-secondary small mb-0 lh-sm">${escapeHtml(m.description || '')}</p>
            </div>
            <button class="btn btn-sm btn-outline-primary rounded-pill fw-semibold px-3 flex-shrink-0" onclick="openArticleModal('${m.slug}')">
              Read Guide &rarr;
            </button>
          </div>
        `).join("");
      }
    }

    // Practice Questions
    if (curatedPracticeQuestionsContainer) {
      const questions = feed.practice_questions_sample || [];
      if (curatedQuestionsCount) curatedQuestionsCount.textContent = `${questions.length} Practice Questions`;

      if (!questions.length) {
        curatedPracticeQuestionsContainer.innerHTML = `
          <div class="text-muted small py-4 text-center bg-light rounded-3 border">
            No sample questions for this topic yet. Click "AI Practice Quiz" above to practice!
          </div>
        `;
      } else {
        curatedPracticeQuestionsContainer.innerHTML = questions.map((q, idx) => {
          const qId = q.id || `feed-q-${idx}`;
          return `
            <div class="p-3 border rounded-3 bg-light">
              <div class="d-flex justify-content-between align-items-center mb-1.5">
                <span class="badge bg-secondary-subtle text-secondary small fw-semibold">${escapeHtml(q.topic || 'Practice')}</span>
                <span class="badge bg-white text-muted border small">${escapeHtml(q.difficulty || 'medium')}</span>
              </div>
              <p class="fw-bold text-dark mb-2 small lh-base">${escapeHtml(q.question)}</p>
              
              <div class="row g-1 mb-2">
                ${(q.options || []).map((opt, oIdx) => `
                  <div class="col-6">
                    <div class="p-1.5 px-2 rounded border bg-white small text-truncate" style="font-size: 0.78rem;">
                      <strong>${String.fromCharCode(65 + oIdx)}.</strong> ${escapeHtml(opt)}
                    </div>
                  </div>
                `).join("")}
              </div>

              <button 
                class="btn btn-sm btn-link text-decoration-none p-0 text-primary small fw-semibold"
                type="button" 
                data-bs-toggle="collapse" 
                data-bs-target="#feed-exp-${qId}"
              >
                💡 View Solution Steps &rarr;
              </button>

              <div class="collapse mt-2" id="feed-exp-${qId}">
                <div class="p-2.5 bg-success-subtle text-dark rounded small border border-success-subtle lh-base" style="font-size: 0.8rem;">
                  <strong>Solution:</strong> Focus on core formulas, syntax nuances, and optimal complexity for placement exams.
                </div>
              </div>
            </div>
          `;
        }).join("");
      }
    }
  }

  window.openTopicGuideModal = async function (topicName) {
    try {
      const res = await api.studyMaterials.getTopicGuide(topicName);
      const article = res.data;
      if (!article) return;

      if (modalCategoryBadge) modalCategoryBadge.textContent = (article.category || "Guide").replace("_", " ").toUpperCase();
      if (modalArticleTitle) modalArticleTitle.textContent = article.title;
      if (modalReadTime) modalReadTime.textContent = `⏱️ ${article.estimated_read_time || '10 mins read'}`;
      if (modalDifficulty) modalDifficulty.textContent = `Difficulty: ${(article.difficulty || 'Intermediate').toUpperCase()}`;
      if (modalCompanyTag) modalCompanyTag.textContent = `Target: ${article.company_tag || 'General Placement'}`;

      if (modalArticleBody) {
        if (typeof marked !== "undefined" && marked.parse) {
          modalArticleBody.innerHTML = marked.parse(article.content_markdown || "");
        } else {
          modalArticleBody.innerHTML = `<pre>${escapeHtml(article.content_markdown || "")}</pre>`;
        }
      }

      if (articleModal) articleModal.show();
    } catch (err) {
      alert("Failed to load topic guide: " + err.message);
    }
  };

  // --------------------------------------------------------------------------
  // DAILY PLACEMENT ASSESSMENT ENGINE (30s per question)
  // --------------------------------------------------------------------------

  window.startTrackDailyAssessment = async function () {
    // Reset quiz state
    if (activeQuiz.timerInterval) clearInterval(activeQuiz.timerInterval);
    activeQuiz = {
      quizType: "daily",
      roadmapSlug: null,
      milestoneId: null,
      sessionId: null,
      questions: [],
      currentIndex: 0,
      answers: {},
      timeRemaining: 0,
      timerInterval: null,
      startTime: Date.now(),
    };

    if (quizModalTitle) quizModalTitle.textContent = "🔥 Daily Placement Assessment";
    if (quizModalBadge) {
      quizModalBadge.textContent = "10 Questions • 30s/q Timer";
      quizModalBadge.className = "badge bg-warning text-dark fw-bold px-3 py-1 rounded-pill";
    }

    if (quizLoadingView) quizLoadingView.style.display = "block";
    if (quizTakingView) quizTakingView.style.display = "none";
    if (quizResultsView) quizResultsView.style.display = "none";

    if (quizLoadingTitle) quizLoadingTitle.textContent = "Synthesizing Today's Placement Assessment...";
    if (quizLoadingSubtext) quizLoadingSubtext.textContent = "Mixing questions across your chosen topics (Java, Python, DSA, SQL, Aptitude, OS, etc.)...";

    if (quizTimerPill) {
      quizTimerPill.classList.remove("urgent");
      if (quizTimerText) quizTimerText.textContent = "05:00";
    }

    if (quizModal) quizModal.show();

    try {
      const res = await api.studyMaterials.startDailyAssessment();
      const data = res.data;
      if (!data || !data.questions || !data.questions.length) {
        throw new Error("Could not generate daily assessment questions.");
      }

      activeQuiz.questions = data.questions;
      activeQuiz.sessionId = data.session_id;
      activeQuiz.currentIndex = 0;
      activeQuiz.answers = {};

      // Strictly 30 seconds per question (10 Qs = 300 seconds = 5 minutes)
      activeQuiz.timeRemaining = data.questions.length * 30;
      activeQuiz.startTime = Date.now();

      startQuizTimer();

      if (quizLoadingView) quizLoadingView.style.display = "none";
      if (quizTakingView) quizTakingView.style.display = "block";

      renderCurrentQuestion();
    } catch (err) {
      alert("Failed to start daily assessment: " + err.message);
      if (quizModal) quizModal.hide();
    }
  };

  window.startTrackAiQuiz = async function () {
    // Generate AI quiz based on student's current active topic mix
    const topics = studentPreferences.all_active_topics || ["Quantitative Aptitude", "Data Structures & Algorithms (DSA)"];
    const targetTopic = topics[Math.floor(Math.random() * topics.length)];

    // Map to milestone or generate AI quiz
    startMilestoneQuiz("campus-60-day-sprint", "m1", true);
  };

  // --------------------------------------------------------------------------
  // ROADMAPS & MILESTONE CHECKLIST
  // --------------------------------------------------------------------------

  async function loadRoadmaps() {
    try {
      const res = await api.studyMaterials.getRoadmaps();
      cachedRoadmaps = res.data || [];
      renderRoadmaps();
    } catch (err) {
      if (roadmapsContainer) {
        roadmapsContainer.innerHTML = `<div class="alert alert-danger">Failed to load learning roadmaps: ${err.message}</div>`;
      }
    }
  }

  function getSubjectColor(subject) {
    const s = (subject || "").toLowerCase();
    if (s.includes("quantitative") || s.includes("aptitude") || s.includes("math")) {
      return { badge: "bg-primary-subtle text-primary border border-primary-subtle", icon: "📐" };
    }
    if (s.includes("logical") || s.includes("reasoning") || s.includes("puzzles") || s.includes("deduction")) {
      return { badge: "bg-purple-subtle text-purple border border-purple-subtle", icon: "🧩" };
    }
    if (s.includes("verbal") || s.includes("english") || s.includes("reading")) {
      return { badge: "bg-info-subtle text-info-emphasis border border-info-subtle", icon: "📖" };
    }
    if (s.includes("data structure") || s.includes("algorithm") || s.includes("coding")) {
      return { badge: "bg-indigo-subtle text-indigo border border-indigo-subtle", icon: "💻" };
    }
    if (s.includes("sql") || s.includes("relational")) {
      return { badge: "bg-warning-subtle text-warning-emphasis border border-warning-subtle", icon: "🗄️" };
    }
    if (s.includes("dbms") || s.includes("database")) {
      return { badge: "bg-warning-subtle text-warning-emphasis border border-warning-subtle", icon: "💾" };
    }
    if (s.includes("operating system") || s.includes("os")) {
      return { badge: "bg-danger-subtle text-danger border border-danger-subtle", icon: "⚙️" };
    }
    if (s.includes("network") || s.includes("protocol") || s.includes("web")) {
      return { badge: "bg-teal-subtle text-teal border border-teal-subtle", icon: "🌐" };
    }
    return { badge: "bg-dark-subtle text-dark border border-dark-subtle", icon: "🎯" };
  }

  function renderRoadmaps() {
    if (!roadmapsContainer) return;
    if (!cachedRoadmaps || !cachedRoadmaps.length) {
      roadmapsContainer.innerHTML = `<div class="text-muted py-4">No roadmaps available yet.</div>`;
      return;
    }

    roadmapsContainer.innerHTML = cachedRoadmaps.map(r => {
      const allMilestones = r.milestones || [];
      const completedIds = r.completed_milestones || [];
      const scoresMap = r.scores || {};

      const filteredMilestones = allMilestones.filter(m => {
        if (!m) return false;
        const subject = (m.subject || "").toLowerCase();
        const title = (m.title || "").toLowerCase();
        const desc = (m.description || "").toLowerCase();
        const topics = (m.topics || []).map(t => t.toLowerCase()).join(" ");
        const subtopics = (m.subtopics || []).map(st => st.toLowerCase()).join(" ");

        if (activeRoadmapSubjectFilter !== "all") {
          const filterKey = activeRoadmapSubjectFilter.toLowerCase();
          const matchesSubject = subject.includes(filterKey) || topics.includes(filterKey) || title.includes(filterKey);
          if (!matchesSubject) return false;
        }

        if (activeRoadmapSearchQuery) {
          const q = activeRoadmapSearchQuery.toLowerCase();
          const matchesQuery = title.includes(q) || desc.includes(q) || topics.includes(q) || subtopics.includes(q) || subject.includes(q);
          if (!matchesQuery) return false;
        }

        return true;
      });

      const totalCount = allMilestones.length;
      const completedCount = completedIds.length;

      return `
        <div class="card border-0 shadow-sm" style="border-radius: 20px; overflow: hidden;">
          <div class="card-header bg-white border-bottom p-4 d-flex flex-column flex-lg-row justify-content-between align-items-lg-center gap-3">
            <div>
              <div class="d-flex align-items-center gap-2 mb-1 flex-wrap">
                <span class="fs-3">${r.icon || '🚀'}</span>
                <h4 class="fw-bold text-dark mb-0">${escapeHtml(r.title)}</h4>
                <span class="badge bg-primary-subtle text-primary fw-semibold px-3 py-1 rounded-pill">${r.estimated_weeks} Weeks Sprint</span>
                <span class="badge bg-success-subtle text-success fw-semibold px-2.5 py-1 rounded-pill">12 High-Yield Topics</span>
              </div>
              <p class="text-muted small mb-0">${escapeHtml(r.description || '')}</p>
            </div>
            
            <div class="text-lg-end" style="min-width: 260px;">
              <div class="d-flex justify-content-between text-muted small fw-bold mb-1.5">
                <span>Milestones Mastered: ${completedCount} / ${totalCount}</span>
                <span id="pct-label-${r.slug}" class="text-primary fw-bold">${r.progress_percentage}%</span>
              </div>
              <div class="progress" style="height: 12px; border-radius: 6px; background-color: #e2e8f0;">
                <div class="progress-bar bg-gradient bg-success" id="progress-bar-${r.slug}" role="progressbar" style="width: ${r.progress_percentage}%" aria-valuenow="${r.progress_percentage}" aria-valuemin="0" aria-valuemax="100"></div>
              </div>
            </div>
          </div>

          <div class="bg-white px-4 pt-3 pb-2 border-bottom">
            <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3 mb-3">
              <div class="d-flex flex-wrap gap-1.5" id="roadmap-filter-pills-${r.slug}">
                <button class="btn btn-sm ${activeRoadmapSubjectFilter === 'all' ? 'btn-primary' : 'btn-outline-secondary'} rounded-pill px-3 py-1 fw-semibold filter-pill" onclick="setRoadmapSubjectFilter('${r.slug}', 'all')">
                  All Topics (${totalCount})
                </button>
                <button class="btn btn-sm ${activeRoadmapSubjectFilter === 'quantitative' ? 'btn-primary' : 'btn-outline-secondary'} rounded-pill px-3 py-1 fw-semibold filter-pill" onclick="setRoadmapSubjectFilter('${r.slug}', 'quantitative')">
                  📐 Aptitude
                </button>
                <button class="btn btn-sm ${activeRoadmapSubjectFilter === 'logical' ? 'btn-primary' : 'btn-outline-secondary'} rounded-pill px-3 py-1 fw-semibold filter-pill" onclick="setRoadmapSubjectFilter('${r.slug}', 'logical')">
                  🧩 Reasoning
                </button>
                <button class="btn btn-sm ${activeRoadmapSubjectFilter === 'verbal' ? 'btn-primary' : 'btn-outline-secondary'} rounded-pill px-3 py-1 fw-semibold filter-pill" onclick="setRoadmapSubjectFilter('${r.slug}', 'verbal')">
                  📖 Verbal
                </button>
                <button class="btn btn-sm ${activeRoadmapSubjectFilter === 'data structures' ? 'btn-primary' : 'btn-outline-secondary'} rounded-pill px-3 py-1 fw-semibold filter-pill" onclick="setRoadmapSubjectFilter('${r.slug}', 'data structures')">
                  💻 Coding &amp; DSA
                </button>
                <button class="btn btn-sm ${activeRoadmapSubjectFilter === 'sql' ? 'btn-primary' : 'btn-outline-secondary'} rounded-pill px-3 py-1 fw-semibold filter-pill" onclick="setRoadmapSubjectFilter('${r.slug}', 'sql')">
                  🗄️ SQL &amp; DBMS
                </button>
                <button class="btn btn-sm ${activeRoadmapSubjectFilter === 'operating' ? 'btn-primary' : 'btn-outline-secondary'} rounded-pill px-3 py-1 fw-semibold filter-pill" onclick="setRoadmapSubjectFilter('${r.slug}', 'operating')">
                  ⚙️ OS &amp; Networks
                </button>
                <button class="btn btn-sm ${activeRoadmapSubjectFilter === 'mock' ? 'btn-primary' : 'btn-outline-secondary'} rounded-pill px-3 py-1 fw-semibold filter-pill" onclick="setRoadmapSubjectFilter('${r.slug}', 'mock')">
                  🎯 Company Mocks
                </button>
              </div>

              <div style="min-width: 250px;">
                <input 
                  type="text" 
                  class="form-control form-control-sm rounded-pill px-3" 
                  placeholder="🔍 Search topics, subtopics..." 
                  value="${escapeHtml(activeRoadmapSearchQuery)}"
                  oninput="handleRoadmapSearch('${r.slug}', this.value)"
                />
              </div>
            </div>
          </div>

          <div class="card-body p-4 bg-light">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <div>
                <h5 class="fw-bold text-dark mb-0">Milestone Checklist &amp; Learning Steps</h5>
                <p class="text-muted small mb-0">Click any topic to practice subtopics, take 30-second timed placement quizzes, or generate fresh AI questions.</p>
              </div>
              <span class="badge bg-white text-muted border px-3 py-1.5 rounded-pill small">
                Showing ${filteredMilestones.length} of ${totalCount} Milestones
              </span>
            </div>

            ${!filteredMilestones.length ? `
              <div class="text-center py-5 bg-white rounded-4 border">
                <div class="fs-2 mb-2">🔍</div>
                <h6 class="fw-bold text-dark">No topics matched your search</h6>
                <p class="text-muted small mb-3">Try clearing your search query or switching subject filters.</p>
                <button class="btn btn-sm btn-outline-primary rounded-pill px-3" onclick="clearRoadmapFilters('${r.slug}')">Reset Filters</button>
              </div>
            ` : `
              <div class="row g-3">
                ${filteredMilestones.map((m, mIdx) => {
                  const mId = m.id || `m-${mIdx}`;
                  const isChecked = Array.isArray(completedIds) && completedIds.includes(mId);
                  const scoreInfo = scoresMap[mId];
                  const subjectMeta = getSubjectColor(m.subject);
                  const subtopics = m.subtopics || [];
                  const practiceQuestions = m.practice_questions || [];

                  let scorePillHtml = `<span class="badge bg-light text-muted border small"><span class="me-1">⏳</span>Not Tested</span>`;
                  if (scoreInfo && scoreInfo.attempts) {
                    const pct = Number(scoreInfo.percentage || 0);
                    if (pct >= 60.0) {
                      scorePillHtml = `<span class="badge bg-success-subtle text-success border border-success-subtle fw-semibold small">
                        <span class="me-1">🏆</span>Best: ${pct}% (Passed)
                      </span>`;
                    } else {
                      scorePillHtml = `<span class="badge bg-warning-subtle text-warning-emphasis border border-warning-subtle fw-semibold small">
                        <span class="me-1">⚠️</span>Score: ${pct}% (Retake to Pass)
                      </span>`;
                    }
                  }

                  return `
                    <div class="col-lg-6">
                      <div class="roadmap-step-card h-100 d-flex flex-column justify-content-between ${isChecked ? 'completed' : ''}" id="step-card-${r.slug}-${mId}">
                        <div>
                          <div class="d-flex align-items-start justify-content-between gap-2 mb-2">
                            <div class="form-check d-flex align-items-center gap-2 mb-0">
                              <input 
                                class="form-check-input mt-0" 
                                type="checkbox" 
                                id="check-${r.slug}-${mId}" 
                                ${isChecked ? 'checked' : ''} 
                                onchange="toggleMilestone('${r.slug}', '${mId}')" 
                                style="cursor: pointer; width: 1.25rem; height: 1.25rem;" 
                              />
                              <label class="form-check-label fw-bold text-dark" for="check-${r.slug}-${mId}" style="cursor: pointer;">
                                <span class="badge bg-light text-dark border me-1">Week ${m.week || (mIdx + 1)}</span>
                                ${escapeHtml(m.title || '')}
                              </label>
                            </div>
                            <div class="flex-shrink-0">
                              ${scorePillHtml}
                            </div>
                          </div>

                          <div class="mb-2">
                            <span class="badge ${subjectMeta.badge} fw-semibold px-2.5 py-1 rounded-pill small">
                              <span class="me-1">${subjectMeta.icon}</span>${escapeHtml(m.subject || 'Placement Prep')}
                            </span>
                            <span class="badge bg-light text-secondary border small ms-1">
                              📝 ${practiceQuestions.length} Practice Questions
                            </span>
                          </div>

                          <p class="text-secondary small mb-3 lh-sm">
                            ${escapeHtml(m.description || '')}
                          </p>

                          <div class="mb-3">
                            <div class="text-muted fw-semibold mb-1" style="font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.5px;">
                              Core Subtopics &amp; Concepts:
                            </div>
                            <div class="d-flex flex-wrap gap-1">
                              ${subtopics.slice(0, 4).map(st => `
                                <span class="subtopic-chip">${escapeHtml(st)}</span>
                              `).join("")}
                              ${subtopics.length > 4 ? `
                                <span class="subtopic-chip bg-light text-muted" style="cursor: pointer;" onclick="openMilestonePracticeDrawer('${r.slug}', '${mId}')">
                                  +${subtopics.length - 4} more...
                                </span>
                              ` : ""}
                            </div>
                          </div>
                        </div>

                        <div class="pt-3 border-top mt-2 d-flex flex-wrap align-items-center justify-content-between gap-2">
                          <button 
                            class="btn btn-sm btn-outline-primary rounded-pill fw-semibold px-3" 
                            onclick="openMilestonePracticeDrawer('${r.slug}', '${mId}')"
                          >
                            📖 View Questions &amp; Subtopics
                          </button>
                          
                          <div class="d-flex gap-1.5">
                            <button 
                              class="btn btn-sm btn-primary rounded-pill fw-bold px-3 d-flex align-items-center gap-1 shadow-sm" 
                              onclick="startMilestoneQuiz('${r.slug}', '${mId}', false)"
                              title="Take a 30-seconds-per-question timed test"
                            >
                              <span>⚡</span>
                              <span>Timed Quiz</span>
                            </button>
                            <button 
                              class="btn btn-sm btn-outline-dark rounded-pill fw-bold px-2.5 d-flex align-items-center gap-1" 
                              onclick="startMilestoneQuiz('${r.slug}', '${mId}', true)"
                              title="Generate fresh AI aptitude questions for this topic"
                            >
                              <span>🤖</span>
                              <span>AI Test</span>
                            </button>
                          </div>
                        </div>

                      </div>
                    </div>
                  `;
                }).join("")}
              </div>
            `}
          </div>
        </div>
      `;
    }).join("");
  }

  window.setRoadmapSubjectFilter = function (slug, subject) {
    activeRoadmapSubjectFilter = subject;
    renderRoadmaps();
  };

  window.handleRoadmapSearch = function (slug, query) {
    activeRoadmapSearchQuery = query;
    renderRoadmaps();
  };

  window.clearRoadmapFilters = function (slug) {
    activeRoadmapSubjectFilter = "all";
    activeRoadmapSearchQuery = "";
    renderRoadmaps();
  };

  window.toggleMilestone = async function (roadmapSlug, milestoneId) {
    const cardEl = document.getElementById(`step-card-${roadmapSlug}-${milestoneId}`);
    const checkEl = document.getElementById(`check-${roadmapSlug}-${milestoneId}`);
    if (cardEl && checkEl) {
      cardEl.classList.toggle("completed", checkEl.checked);
    }

    const checkedInputs = document.querySelectorAll(`input[id^="check-${roadmapSlug}-"]:checked`);
    const completedIds = Array.from(checkedInputs).map(inp => inp.id.replace(`check-${roadmapSlug}-`, ""));

    try {
      const res = await api.studyMaterials.updateRoadmapProgress(roadmapSlug, { completed_milestone_ids: completedIds });
      const updated = res.data;
      if (updated) {
        const r = cachedRoadmaps.find(item => item.slug === roadmapSlug);
        if (r) {
          r.completed_milestones = updated.completed_milestones || [];
          r.progress_percentage = updated.progress_percentage || 0;
        }

        const pctLabel = document.getElementById(`pct-label-${roadmapSlug}`);
        const progressBar = document.getElementById(`progress-bar-${roadmapSlug}`);
        if (pctLabel) pctLabel.textContent = `${updated.progress_percentage}%`;
        if (progressBar) {
          progressBar.style.width = `${updated.progress_percentage}%`;
          progressBar.setAttribute("aria-valuenow", updated.progress_percentage);
        }
      }
    } catch (err) {
      console.error("Failed to update milestone progress:", err);
    }
  };

  // --------------------------------------------------------------------------
  // PRACTICE QUESTIONS & SUBTOPICS DRAWER
  // --------------------------------------------------------------------------

  window.openMilestonePracticeDrawer = function (roadmapSlug, milestoneId) {
    const r = cachedRoadmaps.find(item => item.slug === roadmapSlug);
    if (!r) return;
    const m = (r.milestones || []).find(item => item.id === milestoneId);
    if (!m) return;

    activeDrawerMilestone = { roadmapSlug, milestone: m };

    if (drawerMilestoneTitle) drawerMilestoneTitle.textContent = m.title || "Placement Milestone";
    if (drawerSubjectBadge) drawerSubjectBadge.textContent = m.subject || "Placement Prep";
    if (drawerHoursBadge) drawerHoursBadge.textContent = `⏱️ ${m.estimated_hours || 12} Hours Prep`;

    if (drawerSubtopicsContainer) {
      const subtopics = m.subtopics || [];
      drawerSubtopicsContainer.innerHTML = subtopics.map(st => `
        <span class="subtopic-chip px-3 py-1.5" style="font-size: 0.85rem;">
          ✓ ${escapeHtml(st)}
        </span>
      `).join("") || `<span class="text-muted small">No subtopics listed.</span>`;
    }

    const questions = m.practice_questions || [];
    if (drawerQuestionsCount) drawerQuestionsCount.textContent = `${questions.length} Questions with Solutions`;

    if (drawerQuestionsContainer) {
      if (!questions.length) {
        drawerQuestionsContainer.innerHTML = `<div class="text-muted py-4">No curated questions available for this topic. Use the AI Quiz button to generate new ones.</div>`;
      } else {
        drawerQuestionsContainer.innerHTML = questions.map((q, idx) => {
          const qId = q.id || `q-${idx}`;
          const options = q.options || [];
          const correctIdx = Number(q.correct_option_index || 0);

          return `
            <div class="card border rounded-4 p-4 mb-3 bg-white shadow-sm">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="fw-bold text-primary">Question ${idx + 1}</span>
                <div class="d-flex gap-2">
                  <span class="badge bg-light text-muted border text-capitalize">${escapeHtml(q.difficulty || 'medium')}</span>
                  <span class="badge bg-light text-muted border">${q.marks || 1.0} Mark</span>
                </div>
              </div>

              <h6 class="fw-bold text-dark mb-3 lh-base">${escapeHtml(q.question)}</h6>

              <div class="row g-2 mb-3">
                ${options.map((opt, oIdx) => `
                  <div class="col-md-6">
                    <div class="p-2.5 rounded-3 border bg-light small d-flex align-items-center gap-2">
                      <span class="badge bg-secondary-subtle text-secondary fw-bold rounded-circle" style="width: 24px; height: 24px; display: inline-flex; align-items: center; justify-content: center;">
                        ${String.fromCharCode(65 + oIdx)}
                      </span>
                      <span class="text-dark">${escapeHtml(opt)}</span>
                    </div>
                  </div>
                `).join("")}
              </div>

              <div>
                <button 
                  class="btn btn-sm btn-outline-secondary rounded-pill px-3 fw-semibold" 
                  type="button" 
                  data-bs-toggle="collapse" 
                  data-bs-target="#explanation-${qId}" 
                  aria-expanded="false"
                >
                  💡 Reveal Answer &amp; Step-by-Step Explanation
                </button>

                <div class="collapse mt-3" id="explanation-${qId}">
                  <div class="p-3 bg-success-subtle border border-success-subtle rounded-3">
                    <div class="d-flex align-items-center gap-2 mb-2 text-success fw-bold">
                      <span>✓</span>
                      <span>Correct Answer: Option ${String.fromCharCode(65 + correctIdx)} (${escapeHtml(options[correctIdx] || '')})</span>
                    </div>
                    <div class="text-secondary small lh-base">
                      <strong>Solution Steps:</strong> ${escapeHtml(q.explanation || 'Review conceptual rules.')}
                    </div>
                  </div>
                </div>
              </div>

            </div>
          `;
        }).join("");
      }
    }

    const runTimedQuiz = () => {
      if (drawerModal) drawerModal.hide();
      startMilestoneQuiz(roadmapSlug, milestoneId, false);
    };
    const runAiQuiz = () => {
      if (drawerModal) drawerModal.hide();
      startMilestoneQuiz(roadmapSlug, milestoneId, true);
    };

    if (drawerStartTimedQuizBtn) drawerStartTimedQuizBtn.onclick = runTimedQuiz;
    if (drawerFooterQuizBtn) drawerFooterQuizBtn.onclick = runTimedQuiz;
    if (drawerStartAiQuizBtn) drawerStartAiQuizBtn.onclick = runAiQuiz;
    if (drawerFooterAiBtn) drawerFooterAiBtn.onclick = runAiQuiz;

    if (drawerModal) drawerModal.show();
  };

  // --------------------------------------------------------------------------
  // TIMED QUIZ & AI TEST ENGINE (Shared for milestone & daily assessments)
  // --------------------------------------------------------------------------

  function setupQuizModalListeners() {
    if (quizPrevBtn) quizPrevBtn.onclick = prevQuizQuestion;
    if (quizNextBtn) quizNextBtn.onclick = nextQuizQuestion;
    if (quizSubmitBtn) quizSubmitBtn.onclick = submitCurrentQuiz;

    if (quizModalCloseBtn) {
      quizModalCloseBtn.onclick = () => {
        if (activeQuiz.timerInterval) {
          if (confirm("Are you sure you want to exit? Your quiz attempt will not be saved.")) {
            clearInterval(activeQuiz.timerInterval);
            activeQuiz.timerInterval = null;
            if (quizModal) quizModal.hide();
          }
        } else {
          if (quizModal) quizModal.hide();
        }
      };
    }

    if (resultsCloseBtn) {
      resultsCloseBtn.onclick = () => {
        if (quizModal) quizModal.hide();
      };
    }

    if (resultsRetakeBtn) {
      resultsRetakeBtn.onclick = () => {
        if (activeQuiz.quizType === "company") {
          startCompanyMockExam(activeQuiz.companySlug);
        } else if (activeQuiz.quizType === "daily") {
          startTrackDailyAssessment();
        } else if (activeQuiz.roadmapSlug && activeQuiz.milestoneId) {
          startMilestoneQuiz(activeQuiz.roadmapSlug, activeQuiz.milestoneId, false);
        }
      };
    }

    if (resultsAiBtn) {
      resultsAiBtn.onclick = () => {
        if (activeQuiz.quizType === "company") {
          startCompanyMockExam(activeQuiz.companySlug);
        } else if (activeQuiz.quizType === "daily") {
          startTrackDailyAssessment();
        } else if (activeQuiz.roadmapSlug && activeQuiz.milestoneId) {
          startMilestoneQuiz(activeQuiz.roadmapSlug, activeQuiz.milestoneId, true);
        }
      };
    }
  }

  window.startMilestoneQuiz = async function (roadmapSlug, milestoneId, isAi = false) {
    const r = cachedRoadmaps.find(item => item.slug === roadmapSlug);
    const m = r ? (r.milestones || []).find(item => item.id === milestoneId) : null;
    const milestoneTitle = m ? m.title : "Milestone Test";

    if (activeQuiz.timerInterval) clearInterval(activeQuiz.timerInterval);
    activeQuiz = {
      quizType: "milestone",
      roadmapSlug,
      milestoneId,
      isAi,
      sessionId: null,
      questions: [],
      currentIndex: 0,
      answers: {},
      timeRemaining: 0,
      timerInterval: null,
      startTime: Date.now(),
    };

    if (quizModalTitle) quizModalTitle.textContent = isAi ? `🤖 AI Practice: ${milestoneTitle}` : `⚡ Timed Quiz: ${milestoneTitle}`;
    if (quizModalBadge) {
      quizModalBadge.textContent = isAi ? "AI Generated Test" : (m ? m.subject : "Timed Test");
      quizModalBadge.className = isAi ? "badge bg-dark text-white fw-semibold px-2.5 py-1 rounded-pill" : "badge bg-primary-subtle text-primary fw-semibold px-2.5 py-1 rounded-pill";
    }

    if (quizLoadingView) quizLoadingView.style.display = "block";
    if (quizTakingView) quizTakingView.style.display = "none";
    if (quizResultsView) quizResultsView.style.display = "none";

    if (quizLoadingTitle) quizLoadingTitle.textContent = isAi ? "Generating AI Aptitude & Reasoning Questions..." : "Loading Milestone Placement Quiz...";
    if (quizLoadingSubtext) quizLoadingSubtext.textContent = isAi ? "Synthesizing dynamic questions based on the topics you are studying..." : "Preparing 30-seconds-per-question placement exam environment...";

    if (quizTimerPill) {
      quizTimerPill.classList.remove("urgent");
      if (quizTimerText) quizTimerText.textContent = "00:30";
    }

    if (quizModal) quizModal.show();

    try {
      let res;
      if (isAi) {
        res = await api.studyMaterials.generateMilestoneAiQuiz(roadmapSlug, milestoneId);
      } else {
        res = await api.studyMaterials.getMilestoneQuiz(roadmapSlug, milestoneId);
      }

      const quizData = res.data;
      if (!quizData || !quizData.questions || !quizData.questions.length) {
        throw new Error("No quiz questions could be loaded.");
      }

      activeQuiz.questions = quizData.questions;
      activeQuiz.sessionId = quizData.session_id || null;
      activeQuiz.currentIndex = 0;
      activeQuiz.answers = {};

      activeQuiz.timeRemaining = quizData.questions.length * 30;
      activeQuiz.startTime = Date.now();

      startQuizTimer();

      if (quizLoadingView) quizLoadingView.style.display = "none";
      if (quizTakingView) quizTakingView.style.display = "block";

      renderCurrentQuestion();
    } catch (err) {
      alert("Failed to start milestone quiz: " + err.message);
      if (quizModal) quizModal.hide();
    }
  };

  function startQuizTimer() {
    updateTimerDisplay();
    activeQuiz.timerInterval = setInterval(() => {
      activeQuiz.timeRemaining--;
      updateTimerDisplay();

      if (activeQuiz.timeRemaining <= 10 && quizTimerPill) {
        quizTimerPill.classList.add("urgent");
      }

      if (activeQuiz.timeRemaining <= 0) {
        clearInterval(activeQuiz.timerInterval);
        activeQuiz.timerInterval = null;
        alert("⏰ Time is up! Submitting your answers for evaluation.");
        submitCurrentQuiz();
      }
    }, 1000);
  }

  function updateTimerDisplay() {
    if (!quizTimerText) return;
    const remaining = Math.max(0, activeQuiz.timeRemaining);
    const mins = Math.floor(remaining / 60);
    const secs = remaining % 60;
    quizTimerText.textContent = `${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
  }

  function renderCurrentQuestion() {
    const qList = activeQuiz.questions;
    const index = activeQuiz.currentIndex;
    const q = qList[index];
    if (!q) return;

    if (quizQCounter) quizQCounter.textContent = `Question ${index + 1} of ${qList.length}`;
    if (quizDifficultyBadge) quizDifficultyBadge.textContent = (q.difficulty || "medium").toUpperCase();
    if (quizMarksBadge) quizMarksBadge.textContent = `${q.marks || 1.0} Mark`;

    const progressPct = ((index + 1) / qList.length) * 100;
    if (quizProgressBar) quizProgressBar.style.width = `${progressPct}%`;

    if (quizQText) quizQText.textContent = q.question;

    if (quizOptionsContainer) {
      const options = q.options || [];
      const currentSelected = activeQuiz.answers[q.id];

      quizOptionsContainer.innerHTML = options.map((opt, oIdx) => {
        const isSelected = currentSelected === oIdx;
        return `
          <div 
            class="quiz-option-card ${isSelected ? 'selected' : ''}" 
            onclick="selectQuizOption('${q.id}', ${oIdx})"
            id="opt-card-${q.id}-${oIdx}"
          >
            <input 
              type="radio" 
              name="quiz_choice_${q.id}" 
              id="radio-${q.id}-${oIdx}" 
              value="${oIdx}" 
              ${isSelected ? 'checked' : ''} 
              style="pointer-events: none;"
            />
            <span class="badge ${isSelected ? 'bg-primary text-white' : 'bg-light text-dark border'} fw-bold rounded-circle" style="width: 28px; height: 28px; display: inline-flex; align-items: center; justify-content: center;">
              ${String.fromCharCode(65 + oIdx)}
            </span>
            <span class="fw-medium text-dark">${escapeHtml(opt)}</span>
          </div>
        `;
      }).join("");
    }

    if (quizPrevBtn) {
      quizPrevBtn.style.visibility = index > 0 ? "visible" : "hidden";
    }

    const isLast = index === qList.length - 1;
    if (quizNextBtn) quizNextBtn.style.display = isLast ? "none" : "inline-block";
    if (quizSubmitBtn) quizSubmitBtn.style.display = isLast ? "inline-block" : "none";
  }

  window.selectQuizOption = function (qid, optionIndex) {
    activeQuiz.answers[qid] = optionIndex;

    const q = activeQuiz.questions[activeQuiz.currentIndex];
    if (q && q.options) {
      q.options.forEach((_, idx) => {
        const card = document.getElementById(`opt-card-${qid}-${idx}`);
        const radio = document.getElementById(`radio-${qid}-${idx}`);
        if (card) {
          card.classList.toggle("selected", idx === optionIndex);
        }
        if (radio) {
          radio.checked = (idx === optionIndex);
        }
      });
    }
  };

  function prevQuizQuestion() {
    if (activeQuiz.currentIndex > 0) {
      activeQuiz.currentIndex--;
      renderCurrentQuestion();
    }
  }

  function nextQuizQuestion() {
    if (activeQuiz.currentIndex < activeQuiz.questions.length - 1) {
      activeQuiz.currentIndex++;
      renderCurrentQuestion();
    }
  }

  async function submitCurrentQuiz() {
    if (activeQuiz.timerInterval) {
      clearInterval(activeQuiz.timerInterval);
      activeQuiz.timerInterval = null;
    }

    const timeTaken = Math.max(1, Math.round((Date.now() - activeQuiz.startTime) / 1000));

    if (quizSubmitBtn) {
      quizSubmitBtn.disabled = true;
      quizSubmitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-1" role="status"></span>Evaluating...`;
    }

    try {
      let result;
      if (activeQuiz.quizType === "company") {
        const res = await api.studyMaterials.submitCompanyMockTest(activeQuiz.companySlug, {
          session_id: activeQuiz.sessionId,
          answers: activeQuiz.answers,
          time_taken_seconds: timeTaken,
        });
        result = res.data;
      } else if (activeQuiz.quizType === "daily") {
        const res = await api.studyMaterials.submitDailyAssessment({
          session_id: activeQuiz.sessionId,
          answers: activeQuiz.answers,
          time_taken_seconds: timeTaken,
        });
        result = res.data;
        if (trackDailyStreak && result.daily_streak) {
          trackDailyStreak.textContent = result.daily_streak;
        }
      } else {
        const payload = {
          session_id: activeQuiz.sessionId,
          answers: activeQuiz.answers,
          time_taken_seconds: timeTaken,
        };
        const res = await api.studyMaterials.submitMilestoneQuiz(
          activeQuiz.roadmapSlug,
          activeQuiz.milestoneId,
          payload
        );
        result = res.data;
        loadRoadmaps();
      }

      displayQuizResults(result);
    } catch (err) {
      alert("Submission error: " + err.message);
    } finally {
      if (quizSubmitBtn) {
        quizSubmitBtn.disabled = false;
        quizSubmitBtn.innerHTML = `✓ Submit Test`;
      }
    }
  }

  function displayQuizResults(result) {
    if (quizTakingView) quizTakingView.style.display = "none";
    if (quizResultsView) quizResultsView.style.display = "block";

    const passed = result.passed;

    if (resultsIcon) resultsIcon.textContent = passed ? "🏆" : "💪";
    if (resultsStatusBadge) {
      resultsStatusBadge.textContent = passed ? "PASSED (>= 60%)" : "NEEDS REVISION (< 60%)";
      resultsStatusBadge.className = passed ? "badge bg-success text-white px-3 py-1.5 rounded-pill fw-bold mb-2" : "badge bg-warning text-dark px-3 py-1.5 rounded-pill fw-bold mb-2";
    }

    if (resultsTitle) resultsTitle.textContent = passed ? "Assessment Mastered!" : "Keep Practicing!";
    if (resultsFeedbackMessage) resultsFeedbackMessage.textContent = result.feedback_message || "";

    if (resultsScoreDisplay) resultsScoreDisplay.textContent = `${result.score} / ${result.total_marks}`;
    if (resultsPercentageDisplay) {
      resultsPercentageDisplay.textContent = `${result.percentage}%`;
      resultsPercentageDisplay.className = `h4 fw-bold mb-0 ${passed ? 'text-success' : 'text-warning'}`;
    }
    if (resultsTimeDisplay) resultsTimeDisplay.textContent = `${result.time_taken_seconds}s`;

    if (resultsProgressAlert) {
      if (result.is_milestone_completed) {
        resultsProgressAlert.style.display = "flex";
        if (resultsProgressAlertText) {
          resultsProgressAlertText.textContent = `Milestone unlocked! Overall roadmap progress updated to ${result.updated_roadmap_progress}%.`;
        }
      } else if (result.daily_streak) {
        resultsProgressAlert.style.display = "flex";
        if (resultsProgressAlertText) {
          resultsProgressAlertText.textContent = `Daily placement practice completed! Streak: ${result.daily_streak} Days 🔥`;
        }
      } else {
        resultsProgressAlert.style.display = "none";
      }
    }

    if (quizReviewList) {
      const items = result.review_items || [];
      quizReviewList.innerHTML = items.map((item, idx) => {
        const isCorrect = item.is_correct;
        const options = item.options || [];
        const userChoice = item.user_selected_index !== null ? item.user_selected_index : null;
        const correctChoice = item.correct_option_index;

        return `
          <div class="question-review-card ${isCorrect ? 'correct-card' : 'wrong-card'}">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <span class="fw-bold ${isCorrect ? 'text-success' : 'text-danger'}">
                ${isCorrect ? '✓ Correct' : '✗ Incorrect or Unanswered'} — Question ${idx + 1}
              </span>
              <span class="badge ${isCorrect ? 'bg-success-subtle text-success' : 'bg-danger-subtle text-danger'} small">
                ${isCorrect ? '+1.0 Mark' : '0.0 Marks'}
              </span>
            </div>

            <h6 class="fw-bold text-dark mb-3 lh-base">${escapeHtml(item.question)}</h6>

            <div class="row g-2 mb-3">
              ${options.map((opt, oIdx) => {
                let optClass = "border bg-white";
                let badgeClass = "bg-light text-dark";

                if (oIdx === correctChoice) {
                  optClass = "border-success bg-success-subtle text-success fw-bold";
                  badgeClass = "bg-success text-white";
                } else if (oIdx === userChoice && !isCorrect) {
                  optClass = "border-danger bg-danger-subtle text-danger";
                  badgeClass = "bg-danger text-white";
                }

                return `
                  <div class="col-md-6">
                    <div class="p-2.5 rounded-3 ${optClass} small d-flex align-items-center gap-2">
                      <span class="badge ${badgeClass} rounded-circle" style="width: 24px; height: 24px; display: inline-flex; align-items: center; justify-content: center;">
                        ${String.fromCharCode(65 + oIdx)}
                      </span>
                      <span>${escapeHtml(opt)}</span>
                      ${oIdx === correctChoice ? '<span class="ms-auto badge bg-success text-white">Correct</span>' : ''}
                      ${oIdx === userChoice && !isCorrect ? '<span class="ms-auto badge bg-danger text-white">Your Answer</span>' : ''}
                    </div>
                  </div>
                `;
              }).join("")}
            </div>

            <div class="p-3 bg-light rounded-3 border">
              <div class="fw-bold text-dark small mb-1">📖 Step-by-Step Mathematical / Logical Solution:</div>
              <div class="text-secondary small lh-base">${escapeHtml(item.explanation || 'Review the conceptual guide for detailed formulas.')}</div>
            </div>
          </div>
        `;
      }).join("");
    }
  }

  // --------------------------------------------------------------------------
  // CHEATSHEETS & GUIDES TAB
  // --------------------------------------------------------------------------

  async function loadMaterials() {
    try {
      const res = await api.studyMaterials.list();
      allMaterials = res.data || [];
      renderGuides();
      renderCompanyGuides();
    } catch (err) {
      if (guidesGrid) guidesGrid.innerHTML = `<div class="col-12 text-danger">Failed to load study guides.</div>`;
    }
  }

  function setupFilters() {
    filterBtns.forEach(btn => {
      btn.addEventListener("click", () => {
        filterBtns.forEach(b => b.classList.remove("active", "btn-primary"));
        filterBtns.forEach(b => b.classList.add("btn-outline-primary"));
        btn.classList.add("active", "btn-primary");
        btn.classList.remove("btn-outline-primary");

        currentCategory = btn.dataset.category || "all";
        renderGuides();
      });
    });
  }

  function renderGuides() {
    if (!guidesGrid) return;
    const filtered = allMaterials.filter(m => {
      if (currentCategory === "all") return true;
      return m.category === currentCategory;
    });

    if (!filtered.length) {
      guidesGrid.innerHTML = `<div class="col-12 text-muted py-4">No materials found in this category.</div>`;
      return;
    }

    guidesGrid.innerHTML = filtered.map(m => `
      <div class="col-md-6 col-lg-4">
        <div class="material-card p-4 h-100 d-flex flex-column justify-content-between">
          <div>
            <div class="d-flex justify-content-between align-items-center mb-2">
              <span class="badge bg-primary-subtle text-primary fw-semibold px-2.5 py-1 rounded-pill text-uppercase" style="font-size: 0.75rem;">
                ${escapeHtml(m.category.replace('_', ' '))}
              </span>
              <span class="text-muted small">⏱️ ${escapeHtml(m.estimated_read_time || '10 mins')}</span>
            </div>
            <h5 class="fw-bold text-dark mb-2">${escapeHtml(m.title)}</h5>
            <p class="text-secondary small mb-3">${escapeHtml(m.description || '')}</p>
          </div>

          <div>
            <div class="d-flex flex-wrap gap-1 mb-3">
              ${(m.tags || []).slice(0, 3).map(tag => `<span class="badge bg-light text-muted border">${escapeHtml(tag)}</span>`).join("")}
            </div>
            <button class="btn btn-outline-primary w-100 fw-semibold rounded-pill py-2" onclick="openArticleModal('${m.slug}')">
              📖 Read Guide &rarr;
            </button>
          </div>
        </div>
      </div>
    `).join("");
  }

  // --------------------------------------------------------------------------
  // TOP COMPANY APTITUDE ANALYSIS & EXAM INTELLIGENCE
  // --------------------------------------------------------------------------

  let allCompaniesCatalog = [];
  let activeCompanySlug = "vgen";

  async function loadCompanyIntelligence() {
    const chipsContainer = document.getElementById("company-selector-chips-container");
    const workspace = document.getElementById("company-detail-workspace");
    if (!chipsContainer && !workspace) return;

    try {
      const res = await api.studyMaterials.getCompanies();
      allCompaniesCatalog = res.data || [];
      renderCompanySelectorChips();

      // Check if URL specifies a company or default to first recently hiring company
      const urlParams = new URLSearchParams(window.location.search);
      const targetCompany = urlParams.get("company") || (allCompaniesCatalog[0] ? allCompaniesCatalog[0].slug : "vgen");
      selectCompany(targetCompany);
    } catch (err) {
      console.error("Failed to load companies intelligence:", err);
      if (chipsContainer) {
        chipsContainer.innerHTML = `<span class="text-danger small">Failed to load company catalog.</span>`;
      }
    }
  }

  function renderCompanySelectorChips() {
    const chipsContainer = document.getElementById("company-selector-chips-container");
    if (!chipsContainer) return;
    if (!allCompaniesCatalog.length) {
      chipsContainer.innerHTML = `<span class="text-muted small">No company intelligence available.</span>`;
      return;
    }

    chipsContainer.innerHTML = allCompaniesCatalog.map(c => `
      <button 
        type="button" 
        class="company-selector-chip ${c.slug === activeCompanySlug ? 'active' : ''}"
        id="chip-company-${c.slug}"
        onclick="selectCompany('${c.slug}')"
      >
        <span class="me-1">${c.icon || '🏢'}</span>
        <span class="fw-semibold me-1.5">${escapeHtml(c.name)}</span>
        <span class="company-chip-badge ${c.is_recent_hiring ? 'bg-success text-white fw-bold' : ''}">${escapeHtml(c.badge_text || '')}</span>
      </button>
    `).join("");
  }

  window.selectCompany = async function(slug) {
    activeCompanySlug = slug;
    document.querySelectorAll(".company-selector-chip").forEach(btn => {
      if (btn.id === `chip-company-${slug}`) {
        btn.classList.add("active");
      } else {
        btn.classList.remove("active");
      }
    });

    const workspace = document.getElementById("company-detail-workspace");
    if (!workspace) return;

    workspace.innerHTML = `
      <div class="card border-0 shadow-sm p-5 text-center bg-white" style="border-radius: 20px;">
        <div class="spinner-border text-primary mx-auto mb-3" role="status"></div>
        <h5 class="fw-bold text-dark mb-1">Loading ${escapeHtml(slug.toUpperCase())} Aptitude Analysis...</h5>
        <p class="text-muted small mb-0">Analyzing recurring question patterns, sectional weightages &amp; strategies...</p>
      </div>
    `;

    try {
      const res = await api.studyMaterials.getCompanyDetail(slug);
      const c = res.data;
      if (!c) throw new Error("Company details not found");
      renderCompanyDeepDive(c);
    } catch (err) {
      workspace.innerHTML = `
        <div class="alert alert-danger border-0 shadow-sm rounded-4 p-4 text-center">
          <h5 class="fw-bold mb-1">Error Loading Company Intelligence</h5>
          <p class="mb-0 small">${escapeHtml(err.message)}</p>
        </div>
      `;
    }
  };

  function renderCompanyDeepDive(c) {
    const workspace = document.getElementById("company-detail-workspace");
    if (!workspace) return;

    const quantTrends = c.aptitude_analysis?.quantitative_trends || [];
    const reasoningTrends = c.aptitude_analysis?.reasoning_trends || [];
    const verbalTrends = c.aptitude_analysis?.verbal_trends || [];
    const hiringRoles = c.hiring_roles || [];
    const rounds = c.selection_rounds || [];
    const examPattern = c.exam_pattern || [];
    const prepStrategy = c.preparation_strategy || [];
    const sampleQuestions = c.sample_questions || [];

    workspace.innerHTML = `
      <!-- Company Banner Header -->
      <div class="card border-0 mb-4 p-4 p-md-5 text-white shadow-sm overflow-hidden position-relative" style="border-radius: 24px; background: ${c.gradient || 'linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%)'};">
        <div class="position-absolute" style="top: -50px; right: -50px; width: 250px; height: 250px; background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%); border-radius: 50%; pointer-events: none;"></div>
        
        <div class="d-flex flex-column flex-lg-row justify-content-between align-items-lg-center gap-4 position-relative" style="z-index: 1;">
          <div>
            <div class="d-flex align-items-center gap-2 mb-2 flex-wrap">
              <span class="fs-1">${c.icon || '🏢'}</span>
              <span class="badge bg-white text-dark fw-bold px-3 py-1 rounded-pill">${escapeHtml(c.badge_text || 'Placement Drive')}</span>
              <span class="badge bg-white bg-opacity-20 text-white border border-white border-opacity-25 px-2.5 py-1 rounded-pill small">
                Difficulty: ${escapeHtml(c.overall_difficulty || 'Moderate')}
              </span>
            </div>
            <h2 class="display-6 fw-extrabold mb-2 text-white">${escapeHtml(c.name)}</h2>
            <p class="mb-3 text-light opacity-90 small" style="max-width: 680px; font-size: 1rem; line-height: 1.6;">
              ${escapeHtml(c.tagline || '')}
            </p>
            <div class="d-flex flex-wrap gap-2">
              ${hiringRoles.map(r => `
                <span class="badge bg-white bg-opacity-15 border border-white border-opacity-25 text-white px-3 py-1.5 rounded-pill small">
                  💼 ${escapeHtml(r.title)}: <strong>${escapeHtml(r.package)}</strong>
                </span>
              `).join('')}
            </div>
          </div>

          <div class="d-flex flex-column flex-sm-row flex-lg-column gap-2 flex-shrink-0">
            <button class="btn btn-light text-primary fw-bold rounded-pill px-4 py-2.5 shadow-sm d-flex align-items-center justify-content-center gap-2" onclick="startCompanyMockExam('${c.slug}')">
              <span>⚡</span>
              <span>Take ${escapeHtml(c.slug.toUpperCase())} Timed Mock Test</span>
            </button>
            <button class="btn btn-outline-light fw-semibold rounded-pill px-4 py-2.5 d-flex align-items-center justify-content-center gap-2" onclick="switchTabToMyTrack()">
              <span>📚</span>
              <span>Study Prescribed Textbooks</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Hiring Cadres & Packages Row -->
      <div class="card border-0 shadow-sm p-4 mb-4 bg-white" style="border-radius: 20px;">
        <h5 class="fw-bold text-dark mb-3 d-flex align-items-center gap-2">
          <span>💼</span> Hiring Cadres &amp; Compensation Packages
        </h5>
        <div class="row g-3">
          ${hiringRoles.map(r => `
            <div class="col-md-4">
              <div class="card h-100 border p-3 bg-light" style="border-radius: 14px;">
                <div class="d-flex justify-content-between align-items-center mb-1">
                  <h6 class="fw-bold text-dark mb-0">${escapeHtml(r.title)}</h6>
                  <span class="badge bg-success-subtle text-success fw-bold">${escapeHtml(r.package)}</span>
                </div>
                <div class="text-secondary small mt-2"><strong>Focus:</strong> ${escapeHtml(r.focus || 'Aptitude & Technical Basics')}</div>
              </div>
            </div>
          `).join('')}
        </div>
      </div>

      <!-- Selection Process & Exact Exam Pattern Row -->
      <div class="row g-4 mb-4">
        <!-- Selection Process Rounds -->
        <div class="col-lg-5">
          <div class="card border-0 shadow-sm p-4 h-100 bg-white" style="border-radius: 20px;">
            <h5 class="fw-bold text-dark mb-3 d-flex align-items-center gap-2">
              <span>🎯</span> Selection Pipeline &amp; Rounds
            </h5>
            <div class="d-flex flex-column gap-3">
              ${rounds.map((rd, i) => `
                <div class="p-3 border rounded-3 bg-light">
                  <div class="fw-bold text-dark mb-1 d-flex align-items-center gap-2">
                    <span class="badge bg-primary rounded-circle" style="width: 22px; height: 22px; display: inline-flex; align-items: center; justify-content: center; font-size: 0.75rem;">${i+1}</span>
                    <span>${escapeHtml(rd.round)}</span>
                  </div>
                  <div class="text-secondary small ps-4">${escapeHtml(rd.details)}</div>
                </div>
              `).join('')}
            </div>
          </div>
        </div>

        <!-- Exact Exam Pattern Table -->
        <div class="col-lg-7">
          <div class="card border-0 shadow-sm p-4 h-100 bg-white" style="border-radius: 20px;">
            <h5 class="fw-bold text-dark mb-1 d-flex align-items-center gap-2">
              <span>📊</span> Exact Exam Pattern &amp; Sectional Cutoffs
            </h5>
            <p class="text-muted small mb-3">Official sectional timings and expected qualifying thresholds enforced in campus drives:</p>
            
            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                <thead class="table-light small">
                  <tr>
                    <th>Section</th>
                    <th>Questions</th>
                    <th>Time Limit</th>
                    <th>Marking</th>
                    <th>Cutoff</th>
                  </tr>
                </thead>
                <tbody class="small">
                  ${examPattern.map(p => `
                    <tr>
                      <td class="fw-bold text-dark">${escapeHtml(p.section)}</td>
                      <td><span class="badge bg-secondary-subtle text-secondary">${p.questions} Qs</span></td>
                      <td>⏱️ ${p.time_mins} mins</td>
                      <td class="text-muted">${escapeHtml(p.marking || '+1')}</td>
                      <td><span class="badge bg-success-subtle text-success fw-bold">${escapeHtml(p.cutoff || '65%')}</span></td>
                    </tr>
                  `).join('')}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- IN-DEPTH APTITUDE QUESTION ANALYSIS BY RECRUITER -->
      <div class="card border-0 shadow-sm p-4 mb-4 bg-white" style="border-radius: 20px;">
        <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-2 mb-3 pb-3 border-bottom">
          <div>
            <span class="badge bg-primary text-white fw-bold px-3 py-1 rounded-pill mb-1">Corporate Exam Intelligence</span>
            <h4 class="fw-bold text-dark mb-0">📐 Aptitude Question Analysis &amp; High-Yield Topic Weightages</h4>
            <p class="text-secondary small mb-0">Analysis of real questions asked in ${escapeHtml(c.name)} recruitment drives. Focus your preparation on topics with the highest frequency and weight.</p>
          </div>
          <span class="badge bg-light text-muted border small flex-shrink-0">Updated for 2026 Campus Drive</span>
        </div>

        <div class="row g-4">
          <!-- Quantitative Analysis -->
          <div class="col-lg-4">
            <div class="p-3 border rounded-4 bg-light h-100">
              <div class="d-flex align-items-center gap-2 mb-3">
                <span class="fs-4">📐</span>
                <h6 class="fw-bold text-dark mb-0">Quantitative Ability Trends</h6>
              </div>
              <div class="d-flex flex-column gap-3">
                ${quantTrends.map(t => `
                  <div class="p-2.5 bg-white rounded-3 border">
                    <div class="d-flex justify-content-between align-items-center mb-1">
                      <span class="fw-bold text-dark small">${escapeHtml(t.topic)}</span>
                      <span class="badge ${t.freq === 'Signature' || t.freq === 'Very High' ? 'bg-danger-subtle text-danger' : 'bg-primary-subtle text-primary'} small">${escapeHtml(t.freq)}</span>
                    </div>
                    <div class="progress mb-2" style="height: 5px;">
                      <div class="progress-bar bg-primary" role="progressbar" style="width: ${escapeHtml(t.weight)};"></div>
                    </div>
                    <p class="text-muted small mb-0" style="font-size: 0.78rem;">
                      💡 <strong>Tip:</strong> ${escapeHtml(t.tips)}
                    </p>
                  </div>
                `).join('')}
              </div>
            </div>
          </div>

          <!-- Reasoning Analysis -->
          <div class="col-lg-4">
            <div class="p-3 border rounded-4 bg-light h-100">
              <div class="d-flex align-items-center gap-2 mb-3">
                <span class="fs-4">🧩</span>
                <h6 class="fw-bold text-dark mb-0">Reasoning &amp; Analytical Trends</h6>
              </div>
              <div class="d-flex flex-column gap-3">
                ${reasoningTrends.map(t => `
                  <div class="p-2.5 bg-white rounded-3 border">
                    <div class="d-flex justify-content-between align-items-center mb-1">
                      <span class="fw-bold text-dark small">${escapeHtml(t.topic)}</span>
                      <span class="badge ${t.freq === 'Signature' || t.freq === 'Very High' ? 'bg-danger-subtle text-danger' : 'bg-purple-subtle text-purple'} small" style="${t.freq !== 'Signature' ? 'background: rgba(147, 51, 234, 0.1); color: #7e22ce;' : ''}">${escapeHtml(t.freq)}</span>
                    </div>
                    <div class="progress mb-2" style="height: 5px;">
                      <div class="progress-bar" role="progressbar" style="width: ${escapeHtml(t.weight)}; background-color: #8b5cf6;"></div>
                    </div>
                    <p class="text-muted small mb-0" style="font-size: 0.78rem;">
                      💡 <strong>Tip:</strong> ${escapeHtml(t.tips)}
                    </p>
                  </div>
                `).join('')}
              </div>
            </div>
          </div>

          <!-- Verbal Analysis -->
          <div class="col-lg-4">
            <div class="p-3 border rounded-4 bg-light h-100">
              <div class="d-flex align-items-center gap-2 mb-3">
                <span class="fs-4">📖</span>
                <h6 class="fw-bold text-dark mb-0">Verbal &amp; Communication Trends</h6>
              </div>
              <div class="d-flex flex-column gap-3">
                ${verbalTrends.map(t => `
                  <div class="p-2.5 bg-white rounded-3 border">
                    <div class="d-flex justify-content-between align-items-center mb-1">
                      <span class="fw-bold text-dark small">${escapeHtml(t.topic)}</span>
                      <span class="badge ${t.freq === 'Signature' || t.freq === 'Very High' ? 'bg-danger-subtle text-danger' : 'bg-success-subtle text-success'} small">${escapeHtml(t.freq)}</span>
                    </div>
                    <div class="progress mb-2" style="height: 5px;">
                      <div class="progress-bar bg-success" role="progressbar" style="width: ${escapeHtml(t.weight)};"></div>
                    </div>
                    <p class="text-muted small mb-0" style="font-size: 0.78rem;">
                      💡 <strong>Tip:</strong> ${escapeHtml(t.tips)}
                    </p>
                  </div>
                `).join('')}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 4-WEEK PLACEMENT PREPARATION STRATEGY ROADMAP -->
      <div class="card border-0 shadow-sm p-4 mb-4 bg-white" style="border-radius: 20px;">
        <h5 class="fw-bold text-dark mb-1 d-flex align-items-center gap-2">
          <span>📅</span> 4-Week Placement Preparation Strategy for ${escapeHtml(c.name)}
        </h5>
        <p class="text-secondary small mb-3">Follow this disciplined weekly sprint to clear both the aptitude test and technical interview rounds:</p>
        
        <div class="row g-3">
          ${prepStrategy.map((step, idx) => `
            <div class="col-md-6 col-lg-3">
              <div class="card h-100 border p-3 bg-light" style="border-radius: 14px;">
                <span class="badge bg-primary rounded-pill mb-2 align-self-start fw-bold">Sprint Week ${idx+1}</span>
                <p class="text-dark small mb-0 lh-base">
                  ${escapeHtml(step)}
                </p>
              </div>
            </div>
          `).join('')}
        </div>
      </div>

      <!-- REAL ANALYZED RECENT HIRING APTITUDE QUESTIONS WITH INTERACTIVE DRILL & SOLUTIONS -->
      <div class="card border-0 shadow-sm p-4 mb-4 bg-white" style="border-radius: 20px;">
        <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3 mb-3 pb-3 border-bottom">
          <div>
            <div class="d-flex align-items-center gap-2 mb-1 flex-wrap">
              <span class="badge ${c.is_recent_hiring || c.hired_candidates_count ? 'bg-danger text-white' : 'bg-primary text-white'} fw-bold px-3 py-1 rounded-pill">
                🔥 Recent Hiring Process: ${escapeHtml(c.badge_text || c.recent_hiring_process || 'Campus Placement 2026')}
              </span>
              <span class="badge bg-success-subtle text-success fw-bold px-2.5 py-1 rounded-pill small">
                ✓ Verified Exam Questions
              </span>
              ${c.hired_candidates_count > 0 ? `
                <span class="badge bg-success text-white fw-bold px-2.5 py-1 rounded-pill small">
                  🎯 ${c.hired_candidates_count} Candidates Hired
                </span>
              ` : ''}
            </div>
            <h4 class="fw-bold text-dark mb-1 d-flex align-items-center gap-2">
              <span>📝</span> Aptitude Questions Asked in ${escapeHtml(c.name)}'s Recruitment Process
            </h4>
            <span class="text-secondary small">
              Practice authentic quantitative, reasoning, verbal, and technical aptitude questions asked in recent ${escapeHtml(c.name)} recruitment drives. Click an option to test your accuracy and reveal the step-by-step verified derivation.
            </span>
          </div>
          <div class="d-flex align-items-center gap-2 flex-shrink-0">
            <span class="badge bg-primary px-3 py-2 rounded-pill fw-bold" style="font-size: 0.85rem;" id="company-q-count-badge">
              ${sampleQuestions.length} Questions Available
            </span>
          </div>
        </div>

        ${c.hired_candidates_count > 0 ? `
          <div class="alert alert-success border-0 rounded-4 p-3 mb-4 d-flex align-items-center gap-3 shadow-sm" style="background: rgba(34, 197, 94, 0.12); color: #166534;">
            <span class="fs-3">🏆</span>
            <div>
              <div class="fw-bold mb-0.5">Active Platform Recruiter &amp; Verified Hiring Questions</div>
              <div class="small opacity-90">
                <strong>${escapeHtml(c.name)}</strong> recently conducted hiring on this platform, selecting <strong>${c.hired_candidates_count} candidates</strong> across <strong>${escapeHtml((c.hired_roles || []).join(', ') || 'Engineering Roles')}</strong>. All aptitude questions and screening evaluations asked during this process are listed below with interactive drills and step-by-step solutions.
              </div>
            </div>
          </div>
        ` : ''}

        <!-- Section / Topic Filter Pills -->
        <div class="d-flex flex-wrap gap-2 mb-4 p-2.5 bg-light rounded-4 align-items-center">
          <span class="small fw-bold text-muted ps-2 me-1">Filter by Topic:</span>
          <button type="button" class="btn btn-sm btn-primary rounded-pill px-3 py-1 fw-semibold company-topic-filter-btn active" data-filter="all" onclick="filterCompanyQuestions('all', this)">
            All Topics (${sampleQuestions.length})
          </button>
          <button type="button" class="btn btn-sm btn-outline-secondary rounded-pill px-3 py-1 fw-semibold company-topic-filter-btn" data-filter="Quantitative Ability" onclick="filterCompanyQuestions('Quantitative Ability', this)">
            📐 Quantitative Ability
          </button>
          <button type="button" class="btn btn-sm btn-outline-secondary rounded-pill px-3 py-1 fw-semibold company-topic-filter-btn" data-filter="Logical Reasoning" onclick="filterCompanyQuestions('Logical Reasoning', this)">
            🧩 Logical Reasoning
          </button>
          <button type="button" class="btn btn-sm btn-outline-secondary rounded-pill px-3 py-1 fw-semibold company-topic-filter-btn" data-filter="Verbal Ability" onclick="filterCompanyQuestions('Verbal Ability', this)">
            📖 Verbal Ability
          </button>
          <button type="button" class="btn btn-sm btn-outline-secondary rounded-pill px-3 py-1 fw-semibold company-topic-filter-btn" data-filter="Technical Pseudocode & Puzzles" onclick="filterCompanyQuestions('Technical Pseudocode & Puzzles', this)">
            💻 Technical &amp; Puzzles
          </button>
        </div>

        <!-- Questions List Container -->
        <div class="d-flex flex-column gap-3" id="company-questions-list">
          ${sampleQuestions.map((q, qIndex) => {
            const qId = `q-${c.slug}-${qIndex}`;
            const solId = `sol-${c.slug}-${qIndex}`;
            const secName = q.section || 'Quantitative Ability';
            const diff = (q.difficulty || 'medium').toLowerCase();
            const diffBadgeClass = diff === 'easy' ? 'bg-success-subtle text-success' : (diff === 'hard' ? 'bg-danger-subtle text-danger' : 'bg-warning-subtle text-warning');

            return `
              <div class="p-4 border rounded-4 bg-light company-question-item transition-all" data-section="${escapeHtml(secName)}" id="card-${qId}">
                <div class="d-flex justify-content-between align-items-start gap-2 mb-2.5 flex-wrap">
                  <div class="d-flex align-items-center gap-2 flex-wrap">
                    <span class="badge bg-white text-dark border px-2.5 py-1 small fw-bold">Question ${qIndex + 1} of ${sampleQuestions.length}</span>
                    <span class="badge bg-primary-subtle text-primary fw-semibold px-2.5 py-1">${escapeHtml(secName)}</span>
                    <span class="badge bg-light text-secondary border px-2.5 py-1 small">Topic: ${escapeHtml(q.topic || 'Aptitude')}</span>
                  </div>
                  <div class="d-flex align-items-center gap-1.5 flex-wrap">
                    <span class="badge bg-white text-primary border small fw-semibold">🎯 ${escapeHtml(q.tag || c.name)}</span>
                    <span class="badge ${diffBadgeClass} small fw-bold text-uppercase">${escapeHtml(diff)}</span>
                  </div>
                </div>

                <div class="fw-bold text-dark mb-3 lh-base" style="font-size: 0.98rem; white-space: pre-line;">${escapeHtml(q.question)}</div>

                <!-- Instant Feedback Banner -->
                <div id="feedback-${qId}" class="mb-3" style="display: none;"></div>

                <!-- Interactive Multi-Choice Options -->
                <div class="row g-2 mb-3" id="options-container-${qId}">
                  ${(q.options || []).map((opt, oIdx) => `
                    <div class="col-md-6">
                      <button 
                        type="button" 
                        class="w-100 text-start p-3 bg-white border rounded-3 small text-dark d-flex align-items-center gap-2.5 company-q-opt btn shadow-sm"
                        data-opt-index="${oIdx}"
                        style="transition: all 0.2s ease; border-color: #e2e8f0; font-size: 0.9rem;"
                        onclick="checkCompanyOption('${qId}', ${oIdx}, ${q.correct_option_index || 0}, '${solId}')"
                      >
                        <span class="opt-badge badge bg-light text-dark border fw-bold" style="width: 26px; height: 26px; display: inline-flex; align-items: center; justify-content: center; border-radius: 6px;">${String.fromCharCode(65 + oIdx)}</span>
                        <span class="flex-grow-1">${escapeHtml(opt)}</span>
                      </button>
                    </div>
                  `).join('')}
                </div>

                <!-- Action Toolbar: Solution Reveal & Mock shortcut -->
                <div class="d-flex justify-content-between align-items-center pt-2 border-top">
                  <span class="text-muted small" style="font-size: 0.8rem;">Click an option to test your answer, or reveal the solution directly:</span>
                  <button class="btn btn-sm btn-outline-primary rounded-pill px-3 py-1.5 fw-semibold d-inline-flex align-items-center gap-1.5" onclick="toggleSolution('${solId}')">
                    <span>💡</span>
                    <span>Reveal Step-by-Step Solution</span>
                  </button>
                </div>

                <!-- Hidden Solution Box -->
                <div id="${solId}" class="mt-3 p-3.5 bg-white border border-success border-opacity-50 rounded-4 shadow-sm" style="display: none;">
                  <div class="d-flex align-items-center justify-content-between gap-2 mb-2 pb-2 border-bottom">
                    <div class="d-flex align-items-center gap-2">
                      <span class="badge bg-success text-white fw-bold px-2.5 py-1">✓ Correct Answer: Option ${String.fromCharCode(65 + (q.correct_option_index || 0))}</span>
                      <strong class="text-success small">${escapeHtml(q.options ? q.options[q.correct_option_index || 0] : '')}</strong>
                    </div>
                    <span class="badge bg-light text-muted border small">Verified Recruitment Derivation</span>
                  </div>
                  <div class="text-secondary small lh-base" style="white-space: pre-line; font-size: 0.88rem;">
                    <div class="fw-bold text-dark mb-1">📐 Step-by-Step Mathematical Derivation &amp; Exam Shortcut:</div>
                    ${escapeHtml(q.explanation || 'Review the mathematical formula.')}
                  </div>
                </div>
              </div>
            `;
          }).join('')}
        </div>
      </div>

      <!-- BOTTOM CALLOUT BANNER -->
      <div class="card border-0 p-4 text-white text-center shadow-sm" style="border-radius: 20px; background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%);">
        <h4 class="fw-bold mb-2">Ready to Test Your Readiness for ${escapeHtml(c.name)}?</h4>
        <p class="small text-light opacity-90 mx-auto mb-3" style="max-width: 650px;">
          Take our timed placement exam simulator modeled on the latest 2026 ${escapeHtml(c.name)} exam pattern. Strictly 30 seconds per question with instant scorecard and detailed solutions.
        </p>
        <div class="d-flex justify-content-center gap-2">
          <button class="btn btn-white bg-white text-primary fw-bold rounded-pill px-4 py-2.5 shadow-sm" onclick="startCompanyMockExam('${c.slug}')">
            ⚡ Start Timed ${escapeHtml(c.slug.toUpperCase())} Mock Test
          </button>
        </div>
      </div>
    `;
  }

  window.checkCompanyOption = function(qId, selectedIdx, correctIdx, solId) {
    const container = document.getElementById(`options-container-${qId}`);
    if (!container) return;
    const isCorrect = (selectedIdx === correctIdx);
    const feedbackEl = document.getElementById(`feedback-${qId}`);

    container.querySelectorAll(".company-q-opt").forEach(btn => {
      const idx = parseInt(btn.getAttribute("data-opt-index"), 10);
      btn.disabled = true;
      if (idx === correctIdx) {
        btn.style.background = "#dcfce7";
        btn.style.borderColor = "#22c55e";
        btn.style.color = "#15803d";
        const badge = btn.querySelector(".opt-badge");
        if (badge) {
          badge.style.background = "#22c55e";
          badge.style.color = "#ffffff";
          badge.textContent = "✓";
        }
      } else if (idx === selectedIdx && !isCorrect) {
        btn.style.background = "#fee2e2";
        btn.style.borderColor = "#ef4444";
        btn.style.color = "#b91c1c";
        const badge = btn.querySelector(".opt-badge");
        if (badge) {
          badge.style.background = "#ef4444";
          badge.style.color = "#ffffff";
          badge.textContent = "✗";
        }
      }
    });

    if (feedbackEl) {
      if (isCorrect) {
        feedbackEl.innerHTML = `
          <div class="alert alert-success py-2 px-3 mb-0 rounded-3 small d-flex align-items-center gap-2 border-0" style="background: #ecfdf5; color: #065f46;">
            <span>🎉</span>
            <strong>Correct Answer!</strong> Outstanding accuracy on this ${escapeHtml(activeCompanySlug.toUpperCase())} recruitment question.
          </div>
        `;
      } else {
        feedbackEl.innerHTML = `
          <div class="alert alert-danger py-2 px-3 mb-0 rounded-3 small d-flex align-items-center gap-2 border-0" style="background: #fef2f2; color: #991b1b;">
            <span>❌</span>
            <strong>Incorrect Choice.</strong> The correct answer is highlighted in green. Check the verified derivation below.
          </div>
        `;
      }
      feedbackEl.style.display = "block";
    }

    const solEl = document.getElementById(solId);
    if (solEl) {
      solEl.style.display = "block";
    }
  };

  window.filterCompanyQuestions = function(sectionName, btnEl) {
    document.querySelectorAll(".company-topic-filter-btn").forEach(btn => {
      btn.className = "btn btn-sm btn-outline-secondary rounded-pill px-3 py-1 fw-semibold company-topic-filter-btn";
    });
    if (btnEl) {
      btnEl.className = "btn btn-sm btn-primary rounded-pill px-3 py-1 fw-semibold company-topic-filter-btn active";
    }

    let visibleCount = 0;
    document.querySelectorAll(".company-question-item").forEach(item => {
      const itemSec = item.getAttribute("data-section");
      if (sectionName === "all" || itemSec === sectionName) {
        item.style.display = "block";
        visibleCount++;
      } else {
        item.style.display = "none";
      }
    });

    const countBadge = document.getElementById("company-q-count-badge");
    if (countBadge) {
      countBadge.textContent = `${visibleCount} Questions Displayed`;
    }
  };

  window.toggleSolution = function(id) {
    const el = document.getElementById(id);
    if (el) {
      el.style.display = (el.style.display === "none" || !el.style.display) ? "block" : "none";
    }
  };

  window.switchTabToMyTrack = function() {
    const trackTabBtn = document.getElementById("my-track-tab");
    if (trackTabBtn) {
      bootstrap.Tab.getOrCreateInstance(trackTabBtn).show();
    }
  };

  window.startCompanyMockExam = async function (slug) {
    if (activeQuiz.timerInterval) clearInterval(activeQuiz.timerInterval);
    activeQuiz = {
      quizType: "company",
      companySlug: slug,
      sessionId: null,
      questions: [],
      currentIndex: 0,
      answers: {},
      timeRemaining: 0,
      timerInterval: null,
      startTime: Date.now(),
    };

    if (quizModalTitle) quizModalTitle.textContent = `${slug.toUpperCase()} Placement Mock Exam`;
    if (quizModalBadge) {
      quizModalBadge.textContent = "🏢 Company Pattern • 30s/q Timed Speed";
      quizModalBadge.className = "badge bg-primary text-white fw-bold px-3 py-1 rounded-pill";
    }

    if (quizLoadingView) quizLoadingView.style.display = "block";
    if (quizTakingView) quizTakingView.style.display = "none";
    if (quizResultsView) quizResultsView.style.display = "none";

    const quizLoadingTitle = document.getElementById("quiz-loading-title");
    const quizLoadingSubtext = document.getElementById("quiz-loading-subtext");
    if (quizLoadingTitle) quizLoadingTitle.textContent = `Preparing ${slug.toUpperCase()} Mock Exam...`;
    if (quizLoadingSubtext) quizLoadingSubtext.textContent = `Assembling real questions & patterns modeled on ${slug.toUpperCase()} aptitude cutoffs...`;

    if (milestoneQuizModal) milestoneQuizModal.show();

    try {
      const res = await api.studyMaterials.startCompanyMockTest(slug);
      const data = res.data;
      if (!data || !data.questions || !data.questions.length) {
        throw new Error("No questions available for this company test");
      }

      activeQuiz.sessionId = data.session_id;
      activeQuiz.questions = data.questions;
      activeQuiz.timeRemaining = data.duration_minutes * 60;
      activeQuiz.currentIndex = 0;
      activeQuiz.answers = {};

      if (quizLoadingView) quizLoadingView.style.display = "none";
      if (quizTakingView) quizTakingView.style.display = "block";

      startQuizTimer();
      renderCurrentQuestion();
    } catch (err) {
      alert("Failed to start company mock exam: " + err.message);
      if (milestoneQuizModal) milestoneQuizModal.hide();
    }
  };

  function renderCompanyGuides() {
    loadCompanyIntelligence();
  }

  window.openArticleModal = async function (slug) {
    try {
      const res = await api.studyMaterials.getDetail(slug);
      const article = res.data;
      if (!article) return;

      if (modalCategoryBadge) modalCategoryBadge.textContent = (article.category || "Guide").replace("_", " ").toUpperCase();
      if (modalArticleTitle) modalArticleTitle.textContent = article.title;
      if (modalReadTime) modalReadTime.textContent = `⏱️ ${article.estimated_read_time || '10 mins read'}`;
      if (modalDifficulty) modalDifficulty.textContent = `Difficulty: ${(article.difficulty || 'Intermediate').toUpperCase()}`;
      if (modalCompanyTag) modalCompanyTag.textContent = `Target: ${article.company_tag || 'General Placement'}`;

      if (modalArticleBody) {
        if (typeof marked !== "undefined" && marked.parse) {
          modalArticleBody.innerHTML = marked.parse(article.content_markdown || "");
        } else {
          modalArticleBody.innerHTML = `<pre>${escapeHtml(article.content_markdown || "")}</pre>`;
        }
      }

      if (articleModal) articleModal.show();
    } catch (err) {
      alert("Failed to load article content: " + err.message);
    }
  };

  // --------------------------------------------------------------------------
  // PRESCRIBED COURSEWARE & STUDY TEXTBOOKS
  // --------------------------------------------------------------------------

  async function loadPrescribedBooks(topic = "all") {
    if (!prescribedBooksCardsContainer) return;
    try {
      const res = await api.studyMaterials.getPrescribedBooks(topic);
      prescribedBooksData = res.data || [];
      renderPrescribedBooks(prescribedBooksData);
    } catch (err) {
      console.error("Failed to load prescribed books", err);
      prescribedBooksCardsContainer.innerHTML = `
        <div class="col-12 text-center py-3 text-warning">
          Failed to load prescribed books catalog.
        </div>
      `;
    }
  }

  let activeTextbookCategory = "all";
  window.filterTextbookCategory = function(cat) {
    activeTextbookCategory = cat;
    document.querySelectorAll(".textbook-cat-btn").forEach(btn => {
      if (btn.getAttribute("data-cat") === cat) {
        btn.classList.add("active");
      } else {
        btn.classList.remove("active");
      }
    });

    if (!prescribedBooksData || !prescribedBooksData.length) return;
    if (cat === "all") {
      renderPrescribedBooks(prescribedBooksData);
      return;
    }

    const filtered = prescribedBooksData.filter(b => {
      const s = (b.subject || "").toLowerCase();
      if (cat === "prog") {
        return (
          (s.includes("java") && !s.includes("script")) ||
          s.includes("python") ||
          s.includes("dsa") ||
          s.includes("data structures") ||
          s.includes("javascript") ||
          s.includes("typescript") ||
          s.includes("web") ||
          s.includes("c++") ||
          s.includes("cpp") ||
          s.includes("golang") ||
          s.includes("go ") ||
          s.includes("rust") ||
          s.includes("c programming") ||
          s === "c"
        );
      } else if (cat === "cloud") {
        return (
          s.includes("cloud") ||
          s.includes("aws") ||
          s.includes("amazon") ||
          s.includes("devops") ||
          s.includes("sre")
        );
      } else if (cat === "ai_data" || cat === "data") {
        return (
          s.includes("ai") ||
          s.includes("machine learning") ||
          s.includes("generative") ||
          s.includes("deep learning") ||
          s.includes("data science") ||
          s.includes("data engineering") ||
          s.includes("big data")
        );
      } else if (cat === "security_testing") {
        return (
          s.includes("cyber") ||
          s.includes("security") ||
          s.includes("testing") ||
          s.includes("qa") ||
          s.includes("software testing")
        );
      } else if (cat === "core") {
        return (
          s.includes("operating") ||
          s.includes("os") ||
          s.includes("network") ||
          s.includes("cn") ||
          s.includes("dbms") ||
          s.includes("sql") ||
          s.includes("database")
        );
      } else if (cat === "apt") {
        return (
          s.includes("quant") ||
          s.includes("aptitude") ||
          s.includes("logical") ||
          s.includes("reasoning") ||
          s.includes("verbal") ||
          s.includes("english")
        );
      }
      return true;
    });
    renderPrescribedBooks(filtered);
  };

  function renderPrescribedBooks(books) {
    if (!prescribedBooksCardsContainer) return;
    if (!books || !books.length) {
      prescribedBooksCardsContainer.innerHTML = `<div class="col-12 text-center text-muted">No prescribed books found for this topic filter.</div>`;
      return;
    }

    prescribedBooksCardsContainer.innerHTML = books.map((book) => {
      const subLower = (book.subject || "").toLowerCase();
      let icon = "📚";
      let accentColor = "#6366f1";
      let gradient = "linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.1) 100%)";

      if (subLower.includes("c++") || subLower.includes("cpp")) {
        icon = "⚡";
        accentColor = "#0284c7";
        gradient = "linear-gradient(135deg, rgba(2, 132, 199, 0.18) 0%, rgba(79, 70, 229, 0.12) 100%)";
      } else if (subLower.includes("rust")) {
        icon = "🦀";
        accentColor = "#ea580c";
        gradient = "linear-gradient(135deg, rgba(234, 88, 12, 0.18) 0%, rgba(194, 65, 12, 0.12) 100%)";
      } else if (subLower.includes("golang") || subLower.includes("go ") || subLower.includes("go /")) {
        icon = "🐹";
        accentColor = "#06b6d4";
        gradient = "linear-gradient(135deg, rgba(6, 182, 212, 0.18) 0%, rgba(14, 165, 233, 0.12) 100%)";
      } else if (subLower.includes("c programming") || subLower === "c") {
        icon = "🅒";
        accentColor = "#2563eb";
        gradient = "linear-gradient(135deg, rgba(37, 99, 235, 0.18) 0%, rgba(30, 64, 175, 0.12) 100%)";
      } else if (subLower.includes("java") && !subLower.includes("javascript")) {
        icon = "☕";
        accentColor = "#f97316";
        gradient = "linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(249, 115, 22, 0.1) 100%)";
      } else if (subLower.includes("python")) {
        icon = "🐍";
        accentColor = "#06b6d4";
        gradient = "linear-gradient(135deg, rgba(6, 182, 212, 0.15) 0%, rgba(59, 130, 246, 0.1) 100%)";
      } else if (subLower.includes("dsa") || subLower.includes("data structures")) {
        icon = "💻";
        accentColor = "#3b82f6";
        gradient = "linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(147, 51, 234, 0.1) 100%)";
      } else if (subLower.includes("sql") || subLower.includes("database")) {
        icon = "🗄️";
        accentColor = "#10b981";
        gradient = "linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.1) 100%)";
      } else if (subLower.includes("quant") || subLower.includes("aptitude")) {
        icon = "📐";
        accentColor = "#f59e0b";
        gradient = "linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.1) 100%)";
      } else if (subLower.includes("logical") || subLower.includes("reasoning")) {
        icon = "🧩";
        accentColor = "#8b5cf6";
        gradient = "linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(168, 85, 247, 0.1) 100%)";
      } else if (subLower.includes("javascript") || subLower.includes("typescript") || subLower.includes("js")) {
        icon = "🌐";
        accentColor = "#eab308";
        gradient = "linear-gradient(135deg, rgba(234, 179, 8, 0.15) 0%, rgba(249, 115, 22, 0.1) 100%)";
      } else if (subLower.includes("aws") || subLower.includes("amazon")) {
        icon = "🚀";
        accentColor = "#f59e0b";
        gradient = "linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(217, 119, 6, 0.12) 100%)";
      } else if (subLower.includes("cloud computing") || (subLower.includes("cloud") && !subLower.includes("aws"))) {
        icon = "☁️";
        accentColor = "#38bdf8";
        gradient = "linear-gradient(135deg, rgba(56, 189, 248, 0.2) 0%, rgba(14, 165, 233, 0.12) 100%)";
      } else if (subLower.includes("cybersecurity") || subLower.includes("security")) {
        icon = "🛡️";
        accentColor = "#06b6d4";
        gradient = "linear-gradient(135deg, rgba(6, 182, 212, 0.2) 0%, rgba(14, 165, 233, 0.12) 100%)";
      } else if (subLower.includes("devops") || subLower.includes("sre")) {
        icon = "🔄";
        accentColor = "#3b82f6";
        gradient = "linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(99, 102, 241, 0.12) 100%)";
      } else if (subLower.includes("generative") || subLower.includes("gen ai")) {
        icon = "✨";
        accentColor = "#a855f7";
        gradient = "linear-gradient(135deg, rgba(168, 85, 247, 0.2) 0%, rgba(192, 132, 252, 0.12) 100%)";
      } else if (subLower.includes("deep learning")) {
        icon = "🧠";
        accentColor = "#ec4899";
        gradient = "linear-gradient(135deg, rgba(236, 72, 153, 0.2) 0%, rgba(219, 39, 119, 0.12) 100%)";
      } else if (subLower.includes("software testing") || subLower.includes("testing") || subLower.includes("qa")) {
        icon = "🧪";
        accentColor = "#10b981";
        gradient = "linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.12) 100%)";
      } else if (subLower.includes("data science")) {
        icon = "📊";
        accentColor = "#6366f1";
        gradient = "linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.12) 100%)";
      } else if (subLower.includes("data engineering") || subLower.includes("big data")) {
        icon = "📊";
        accentColor = "#0284c7";
        gradient = "linear-gradient(135deg, rgba(2, 132, 199, 0.15) 0%, rgba(59, 130, 246, 0.1) 100%)";
      } else if (subLower.includes("ai") || subLower.includes("machine learning") || subLower.includes("ml")) {
        icon = "🤖";
        accentColor = "#ec4899";
        gradient = "linear-gradient(135deg, rgba(236, 72, 153, 0.15) 0%, rgba(168, 85, 247, 0.1) 100%)";
      } else if (subLower.includes("operating") || subLower.includes("os")) {
        icon = "⚙️";
        accentColor = "#14b8a6";
        gradient = "linear-gradient(135deg, rgba(20, 184, 166, 0.15) 0%, rgba(13, 148, 136, 0.1) 100%)";
      } else if (subLower.includes("network") || subLower.includes("cn")) {
        icon = "📡";
        accentColor = "#0284c7";
        gradient = "linear-gradient(135deg, rgba(2, 132, 199, 0.15) 0%, rgba(3, 105, 161, 0.1) 100%)";
      } else if (subLower.includes("dbms") || subLower.includes("system design")) {
        icon = "🏛️";
        accentColor = "#8b5cf6";
        gradient = "linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(124, 58, 237, 0.1) 100%)";
      } else if (subLower.includes("verbal") || subLower.includes("english")) {
        icon = "🗣️";
        accentColor = "#ec4899";
        gradient = "linear-gradient(135deg, rgba(236, 72, 153, 0.15) 0%, rgba(219, 39, 119, 0.1) 100%)";
      }

      const accentBorder = accentColor + "55";
      const subject = book.subject;
      const safeId = book.slug.replace(/[^a-zA-Z0-9_-]/g, "");

      return `
        <div class="col-lg-6">
          <div class="card h-100 p-4 border text-white position-relative shadow-sm" style="border-radius: 18px; background: ${gradient}; border-color: ${accentBorder} !important; backdrop-filter: blur(10px);">
            <div class="d-flex justify-content-between align-items-start mb-3">
              <div class="d-flex align-items-center gap-3">
                <div class="fs-1 p-2 rounded-3" style="background: rgba(255,255,255,0.08); line-height: 1;">${icon}</div>
                <div>
                  <div class="d-flex align-items-center gap-2 mb-1 flex-wrap">
                    <span class="badge rounded-pill fw-bold" style="background: ${accentColor}; font-size: 0.75rem;">${escapeHtml(subject.toUpperCase())} TEXTBOOK</span>
                    <span class="badge bg-white text-dark small fw-semibold">${book.chapters_count || 9} Chapters</span>
                    ${book.has_physical_pdf 
                      ? `<span class="badge bg-success-subtle text-success border border-success-subtle small fw-semibold">✅ Master PDF Synced</span>`
                      : `<span class="badge bg-info-subtle text-info border border-info-subtle small fw-semibold">📘 Built-in Knowledge Base</span>`
                    }
                  </div>
                  <h4 class="fw-bold mb-0 text-white" style="cursor: pointer;" onclick="openBookFullReader('${escapeHtml(book.slug)}', '${escapeHtml(subject)}')">${escapeHtml(book.title)}</h4>
                </div>
              </div>
            </div>

            <p class="text-light opacity-90 small mb-3 lh-base">
              ${escapeHtml(book.description || '')}
            </p>

            <!-- Exam Grounding Scope Pills -->
            <div class="p-3 rounded-3 mb-3" style="background: rgba(0,0,0,0.3); border: 1px dashed rgba(255,255,255,0.2);">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="text-uppercase fw-bold text-white-50" style="font-size: 0.72rem; letter-spacing: 0.5px;">
                  🔒 Core Exam Scope &amp; Chapters (Click any to read):
                </span>
                <span class="badge bg-white text-dark" style="font-size: 0.7rem;">Direct Jump</span>
              </div>
              <div class="d-flex flex-wrap gap-1.5">
                ${(book.chapters || []).map(c => `
                  <button 
                    type="button"
                    class="btn btn-xs btn-outline-light rounded-pill py-0.5 px-2.5 text-start text-white border-opacity-25" 
                    style="font-size: 0.73rem; background: rgba(255,255,255,0.08); transition: all 0.2s;"
                    title="Read Chapter ${c.chapter_num}: ${escapeHtml(c.title)}"
                    onclick="openBookToChapter('${escapeHtml(book.slug)}', '${escapeHtml(subject)}', ${c.chapter_num})"
                  >
                    📖 Ch ${c.chapter_num}: ${escapeHtml(c.title)}
                  </button>
                `).join('')}
              </div>
            </div>

            <!-- Action Buttons Row -->
            <div class="d-flex flex-wrap gap-2 mt-auto pt-2 align-items-center">
              <button 
                id="btn-read-book-${safeId}"
                class="btn btn-sm btn-light text-dark fw-bold rounded-pill px-3.5 d-flex align-items-center gap-1.5 shadow-sm"
                onclick="openBookFullReader('${escapeHtml(book.slug)}', '${escapeHtml(subject)}')"
              >
                <span>📖</span>
                <span>Read Full Book (Unabridged)</span>
              </button>
              <button 
                id="btn-view-chapters-${safeId}"
                class="btn btn-sm btn-outline-light rounded-pill px-3 fw-semibold d-flex align-items-center gap-1.5"
                onclick="openBookChaptersModal('${escapeHtml(subject)}')"
              >
                <span>📑</span>
                <span>View Syllabus</span>
              </button>
              <a 
                id="btn-download-book-${safeId}"
                href="${api.studyMaterials.getBookPdfDownloadUrl(book.slug)}"
                target="_blank"
                download
                class="btn btn-sm btn-outline-light rounded-pill px-3 fw-semibold d-flex align-items-center gap-1.5"
                title="Download Master PDF Textbook (${escapeHtml(book.pdf_filename || 'PDF')})"
              >
                <span>📥</span>
                <span>Download PDF</span>
              </a>
              <button 
                id="btn-exam-book-${safeId}"
                class="btn btn-sm btn-primary rounded-pill px-3 fw-bold d-flex align-items-center gap-1.5 shadow-sm"
                onclick="startBookExam('${escapeHtml(subject)}')"
              >
                <span>⚡</span>
                <span>Take Exam</span>
              </button>
              <button 
                id="btn-upload-book-${safeId}"
                class="btn btn-sm btn-outline-light opacity-75 rounded-pill px-2.5 ms-auto small"
                title="Upload custom PDF textbook"
                onclick="document.getElementById('input-upload-book-${safeId}').click()"
              >
                <span>📤 Upload PDF</span>
              </button>
              <input 
                type="file" 
                id="input-upload-book-${safeId}" 
                accept=".pdf" 
                style="display: none;" 
                onchange="handleBookPdfUpload(this, '${escapeHtml(subject)}')"
              />
            </div>
          </div>
        </div>
      `;
    }).join("");
  }

  // Reader font scale state
  let currentBookFontSize = 1.0;

  window.switchBookModalTab = function(tabName) {
    const readerTabBtn = document.getElementById("book-tab-btn-reader");
    const chaptersTabBtn = document.getElementById("book-tab-btn-chapters");
    const readerView = document.getElementById("book-view-reader");
    const chaptersView = document.getElementById("book-view-chapters");

    if (tabName === "chapters") {
      if (chaptersTabBtn) chaptersTabBtn.classList.add("active");
      if (readerTabBtn) readerTabBtn.classList.remove("active");
      if (chaptersView) chaptersView.style.display = "block";
      if (readerView) readerView.style.display = "none";
    } else {
      if (readerTabBtn) readerTabBtn.classList.add("active");
      if (chaptersTabBtn) chaptersTabBtn.classList.remove("active");
      if (readerView) readerView.style.display = "flex";
      if (chaptersView) chaptersView.style.display = "none";
    }
  };

  window.jumpToChapterInReader = function(chNum) {
    switchBookModalTab("reader");
    setTimeout(() => {
      const anchor = document.getElementById(`chapter-${chNum}`);
      if (anchor) {
        anchor.scrollIntoView({ behavior: "smooth", block: "start" });
        anchor.classList.add("highlight-chapter-pulse");
        setTimeout(() => anchor.classList.remove("highlight-chapter-pulse"), 1800);
      }
      document.querySelectorAll("#book-toc-list .book-toc-item").forEach(item => {
        if (item.getAttribute("data-chapter") == chNum) {
          item.classList.add("active");
        } else {
          item.classList.remove("active");
        }
      });
    }, 150);
  };

  window.jumpToChapterSection = function(chNum, sectionType) {
    switchBookModalTab("reader");
    setTimeout(() => {
      const chAnchor = document.getElementById(`chapter-${chNum}`);
      if (chAnchor) {
        let curr = chAnchor.nextElementSibling;
        let found = null;
        while (curr && curr.tagName !== "H2") {
          if (curr.tagName === "H3") {
            const txt = curr.textContent.toLowerCase();
            if (sectionType === "concept" && (txt.includes("concept") || txt.includes("1."))) { found = curr; break; }
            if (sectionType === "formulas" && (txt.includes("formula") || txt.includes("2."))) { found = curr; break; }
            if (sectionType === "solved" && (txt.includes("solved") || txt.includes("3."))) { found = curr; break; }
            if (sectionType === "practice" && (txt.includes("practice") || txt.includes("4."))) { found = curr; break; }
            if (sectionType === "interview" && (txt.includes("interview") || txt.includes("5."))) { found = curr; break; }
          }
          curr = curr.nextElementSibling;
        }

        const target = found || chAnchor;
        target.scrollIntoView({ behavior: "smooth", block: "start" });
        target.classList.add("highlight-chapter-pulse");
        setTimeout(() => target.classList.remove("highlight-chapter-pulse"), 1800);
      }
    }, 150);
  };

  window.filterReaderSection = function(sectionType) {
    document.querySelectorAll(".section-filter-btn").forEach(btn => {
      if (btn.getAttribute("data-filter") === sectionType) {
        btn.classList.add("active");
      } else {
        btn.classList.remove("active");
      }
    });

    const scrollContainer = document.getElementById("book-reader-content-scroll");
    if (!scrollContainer) return;
    if (sectionType === "all") return;

    const h3s = scrollContainer.querySelectorAll("h3");
    let target = null;
    const currentScroll = scrollContainer.scrollTop;

    for (const h of h3s) {
      const txt = h.textContent.toLowerCase();
      let match = false;
      if (sectionType === "concept" && (txt.includes("concept") || txt.includes("1."))) match = true;
      if (sectionType === "formulas" && (txt.includes("formula") || txt.includes("2."))) match = true;
      if (sectionType === "solved" && (txt.includes("solved") || txt.includes("3."))) match = true;
      if (sectionType === "practice" && (txt.includes("practice") || txt.includes("4."))) match = true;
      if (sectionType === "interview" && (txt.includes("interview") || txt.includes("5."))) match = true;

      if (match) {
        if (!target || h.offsetTop >= currentScroll - 50) {
          target = h;
          break;
        }
      }
    }

    if (!target && h3s.length > 0) {
      for (const h of h3s) {
        const txt = h.textContent.toLowerCase();
        if (sectionType === "concept" && (txt.includes("concept") || txt.includes("1."))) { target = h; break; }
        if (sectionType === "formulas" && (txt.includes("formula") || txt.includes("2."))) { target = h; break; }
        if (sectionType === "solved" && (txt.includes("solved") || txt.includes("3."))) { target = h; break; }
        if (sectionType === "practice" && (txt.includes("practice") || txt.includes("4."))) { target = h; break; }
        if (sectionType === "interview" && (txt.includes("interview") || txt.includes("5."))) { target = h; break; }
      }
    }

    if (target) {
      target.scrollIntoView({ behavior: "smooth", block: "start" });
      target.classList.add("highlight-chapter-pulse");
      setTimeout(() => target.classList.remove("highlight-chapter-pulse"), 1800);
    }
  };

  window.openBookToChapter = function(slug, subject, chNum) {
    openBookFullReader(slug, subject, chNum);
  };

  window.openBookChaptersModal = async function(subject) {
    // Locate slug from prescribed books catalog
    let matchedSlug = "java-prescribed-textbook";
    if (prescribedBooksData && prescribedBooksData.length) {
      const match = prescribedBooksData.find(b => (b.subject || "").toLowerCase() === (subject || "").toLowerCase());
      if (match && match.slug) matchedSlug = match.slug;
    }
    await openBookFullReader(matchedSlug, subject);
    switchBookModalTab("chapters");
  };

  window.openBookFullReader = async function(slug, subject, targetChapter = null) {
    activeBookSubject = subject;
    const subLower = (subject || "").toLowerCase();
    
    let icon = "📚";
    if (subLower.includes("c++") || subLower.includes("cpp")) icon = "⚡";
    else if (subLower.includes("rust")) icon = "🦀";
    else if (subLower.includes("golang") || subLower.includes("go ") || subLower.includes("go /")) icon = "🐹";
    else if (subLower.includes("c programming") || subLower === "c") icon = "🅒";
    else if (subLower.includes("java") && !subLower.includes("javascript")) icon = "☕";
    else if (subLower.includes("python")) icon = "🐍";
    else if (subLower.includes("dsa") || subLower.includes("data structures")) icon = "💻";
    else if (subLower.includes("aws") || subLower.includes("amazon")) icon = "🚀";
    else if (subLower.includes("cloud computing") || (subLower.includes("cloud") && !subLower.includes("aws"))) icon = "☁️";
    else if (subLower.includes("cybersecurity") || subLower.includes("security")) icon = "🛡️";
    else if (subLower.includes("devops") || subLower.includes("sre")) icon = "🔄";
    else if (subLower.includes("generative") || subLower.includes("gen ai")) icon = "✨";
    else if (subLower.includes("deep learning")) icon = "🧠";
    else if (subLower.includes("software testing") || subLower.includes("testing") || subLower.includes("qa")) icon = "🧪";
    else if (subLower.includes("data science")) icon = "📊";
    else if (subLower.includes("sql") || subLower.includes("database")) icon = "🗄️";
    else if (subLower.includes("quant") || subLower.includes("aptitude")) icon = "📐";
    else if (subLower.includes("logical") || subLower.includes("reasoning")) icon = "🧩";
    else if (subLower.includes("javascript") || subLower.includes("typescript")) icon = "🌐";
    else if (subLower.includes("operating") || subLower.includes("os")) icon = "⚙️";
    else if (subLower.includes("network") || subLower.includes("cn")) icon = "📡";
    else if (subLower.includes("data engineering") || subLower.includes("big data")) icon = "📊";
    else if (subLower.includes("ai") || subLower.includes("machine learning")) icon = "🤖";
    else if (subLower.includes("verbal") || subLower.includes("english")) icon = "🗣️";

    if (bookModalIcon) bookModalIcon.textContent = icon;
    if (bookModalSubjectBadge) {
      bookModalSubjectBadge.textContent = subject;
      bookModalSubjectBadge.className = "badge bg-primary-subtle text-primary fw-semibold px-2.5 py-1 rounded-pill";
    }

    switchBookModalTab("reader");

    if (bookChaptersModal) bookChaptersModal.show();

    const readerLoading = document.getElementById("book-reader-loading");
    const readerContent = document.getElementById("book-modal-full-text-content");
    const tocList = document.getElementById("book-toc-list");
    const tocBadge = document.getElementById("toc-chapters-badge");
    const scrollContainer = document.getElementById("book-reader-content-scroll");

    if (readerLoading) readerLoading.style.display = "block";
    if (readerContent) readerContent.style.display = "none";
    if (tocList) {
      tocList.innerHTML = `<div class="text-muted small py-3 text-center"><div class="spinner-border spinner-border-sm text-primary mb-1"></div><div>Loading table of contents...</div></div>`;
    }

    try {
      const res = await api.studyMaterials.getDetail(slug);
      const data = res.data;
      if (!data) throw new Error("No study material data returned for " + slug);

      if (bookModalTitle) bookModalTitle.textContent = data.title || `${subject} Master Textbook`;
      activeBookSlug = slug;

      const downloadPdfBtn = document.getElementById("book-modal-download-pdf-btn");
      const footerDownloadPdfBtn = document.getElementById("book-modal-footer-download-btn");
      const pdfUrl = api.studyMaterials.getBookPdfDownloadUrl(slug);
      if (downloadPdfBtn) {
        downloadPdfBtn.href = pdfUrl;
        downloadPdfBtn.setAttribute("download", `${slug}.pdf`);
      }
      if (footerDownloadPdfBtn) {
        footerDownloadPdfBtn.href = pdfUrl;
        footerDownloadPdfBtn.setAttribute("download", `${slug}.pdf`);
      }

      let mdText = data.content_markdown || "";

      let htmlContent = typeof marked !== "undefined" ? marked.parse(mdText) : `<pre>${escapeHtml(mdText)}</pre>`;

      const tempDiv = document.createElement("div");
      tempDiv.innerHTML = htmlContent;

      const headings = tempDiv.querySelectorAll("h1, h2");
      const extractedChapters = [];

      headings.forEach((h) => {
        const text = h.textContent.trim();
        const chMatch = text.match(/Chapter\s+(\d+)[:\s-]*(.*)/i);
        if (chMatch) {
          const num = parseInt(chMatch[1], 10);
          const chTitle = chMatch[2] ? chMatch[2].trim() : text;
          h.id = `chapter-${num}`;
          h.classList.add("pt-4");
          extractedChapters.push({
            num: num,
            title: chTitle || text,
            fullText: text,
            elementId: `chapter-${num}`,
          });
        }
      });

      if (extractedChapters.length === 0) {
        tempDiv.querySelectorAll("h2").forEach((h, idx) => {
          const num = idx + 1;
          h.id = `chapter-${num}`;
          extractedChapters.push({
            num: num,
            title: h.textContent.trim(),
            fullText: h.textContent.trim(),
            elementId: `chapter-${num}`,
          });
        });
      }

      // Inject Chapter Steppers between chapters for seamless reading
      if (extractedChapters.length > 0) {
        const h2Elements = Array.from(tempDiv.querySelectorAll("h2"));
        h2Elements.forEach((h2, idx) => {
          const chData = extractedChapters[idx];
          if (!chData) return;
          const currNum = chData.num;
          const prevNum = idx > 0 ? extractedChapters[idx - 1].num : null;
          const nextNum = idx < extractedChapters.length - 1 ? extractedChapters[idx + 1].num : null;

          const stepperDiv = document.createElement("div");
          stepperDiv.className = "card p-3 my-4 bg-light border-0 d-flex flex-row justify-content-between align-items-center rounded-3 chapter-stepper-card";
          stepperDiv.innerHTML = `
            ${prevNum ? `<button type="button" class="btn btn-outline-secondary btn-sm rounded-pill px-3" onclick="jumpToChapterInReader(${prevNum})">← Chapter ${prevNum}</button>` : `<span></span>`}
            <button type="button" class="btn btn-sm btn-link text-muted text-decoration-none" onclick="jumpToChapterInReader(${currNum})">⬆ Top of Chapter ${currNum}</button>
            ${nextNum ? `<button type="button" class="btn btn-primary btn-sm rounded-pill px-3 fw-bold shadow-sm" onclick="jumpToChapterInReader(${nextNum})">Chapter ${nextNum} →</button>` : `<span class="badge bg-success-subtle text-success border border-success-subtle px-3 py-1.5 rounded-pill">🎉 Complete Syllabus Mastered</span>`}
          `;
          
          if (idx < h2Elements.length - 1) {
            h2Elements[idx + 1].parentNode.insertBefore(stepperDiv, h2Elements[idx + 1]);
          } else {
            tempDiv.appendChild(stepperDiv);
          }
        });
      }

      if (readerContent) {
        readerContent.innerHTML = tempDiv.innerHTML;
        readerContent.style.display = "block";
      }
      if (readerLoading) readerLoading.style.display = "none";

      const filterBar = document.getElementById("reader-section-filter-bar");
      if (filterBar) filterBar.style.display = "flex";

      if (tocBadge) tocBadge.textContent = `${extractedChapters.length} Chapters`;
      if (bookModalChaptersCount) bookModalChaptersCount.textContent = extractedChapters.length;

      if (tocList) {
        tocList.innerHTML = extractedChapters.map((c) => `
          <a 
            href="#${c.elementId}" 
            class="book-toc-item ${targetChapter == c.num ? 'active' : ''}" 
            data-chapter="${c.num}"
            onclick="jumpToChapterInReader(${c.num}); return false;"
          >
            <div class="fw-bold text-dark" style="font-size: 0.78rem;">Chapter ${c.num}</div>
            <div class="text-truncate text-secondary" style="font-size: 0.76rem;" title="${escapeHtml(c.title)}">${escapeHtml(c.title)}</div>
          </a>
        `).join("");
      }

      populateChapterIndexTab(subject, extractedChapters);

      const tocSearch = document.getElementById("book-toc-search-input");
      if (tocSearch) {
        tocSearch.value = "";
        tocSearch.oninput = function() {
          const q = this.value.toLowerCase().trim();
          document.querySelectorAll("#book-toc-list .book-toc-item").forEach(item => {
            const txt = item.textContent.toLowerCase();
            item.style.display = (!q || txt.includes(q)) ? "block" : "none";
          });
        };
      }

      // Font size buttons
      const fontDecBtn = document.getElementById("book-font-decrease");
      const fontIncBtn = document.getElementById("book-font-increase");
      const fontResetBtn = document.getElementById("book-font-reset");

      if (fontDecBtn) {
        fontDecBtn.onclick = () => {
          if (readerContent && currentBookFontSize > 0.8) {
            currentBookFontSize -= 0.1;
            readerContent.style.fontSize = `${currentBookFontSize}rem`;
          }
        };
      }
      if (fontIncBtn) {
        fontIncBtn.onclick = () => {
          if (readerContent && currentBookFontSize < 1.6) {
            currentBookFontSize += 0.1;
            readerContent.style.fontSize = `${currentBookFontSize}rem`;
          }
        };
      }
      if (fontResetBtn) {
        fontResetBtn.onclick = () => {
          if (readerContent) {
            currentBookFontSize = 1.0;
            readerContent.style.fontSize = "1rem";
          }
        };
      }

      if (bookModalStartExamBtn) {
        bookModalStartExamBtn.onclick = () => {
          if (bookChaptersModal) bookChaptersModal.hide();
          startBookExam(subject);
        };
      }
      if (bookModalFooterExamBtn) {
        bookModalFooterExamBtn.onclick = () => {
          if (bookChaptersModal) bookChaptersModal.hide();
          startBookExam(subject);
        };
      }
      if (bookModalFooterReadBtn) {
        bookModalFooterReadBtn.onclick = () => {
          if (scrollContainer) scrollContainer.scrollTo({ top: 0, behavior: "smooth" });
        };
      }

      if (targetChapter) {
        setTimeout(() => {
          jumpToChapterInReader(targetChapter);
        }, 250);
      } else {
        if (scrollContainer) scrollContainer.scrollTop = 0;
      }

    } catch (err) {
      console.error("Failed to load textbook unabridged content", err);
      if (readerLoading) readerLoading.style.display = "none";
      if (readerContent) {
        readerContent.innerHTML = `<div class="alert alert-danger py-4 text-center">Failed to load complete textbook: ${escapeHtml(err.message)}</div>`;
        readerContent.style.display = "block";
      }
    }
  };

  async function populateChapterIndexTab(subject, extractedChapters) {
    if (!bookModalChaptersList) return;
    try {
      const res = await api.studyMaterials.getBookChapters(subject);
      const data = res.data;
      const chapters = (data && data.chapters && data.chapters.length) ? data.chapters : extractedChapters;

      bookModalChaptersList.innerHTML = chapters.map((ch) => {
        const topics = ch.topics || [];
        const chNum = ch.chapter_num || ch.num || 1;
        const chTitle = ch.title || "";
        const takeaways = ch.key_takeaways || `Core examination chapter covering ${chTitle} with complete theory, worked solutions, and practice drills.`;
        const sections = ch.sections || {};
        const solvedCount = sections.solved_examples ? sections.solved_examples.length : 2;
        const practiceCount = sections.practice_questions ? sections.practice_questions.length : 2;
        const interviewCount = sections.interview_questions ? sections.interview_questions.length : 2;

        return `
          <div class="col-md-6 col-lg-4">
            <div class="card h-100 border p-3 bg-light shadow-none d-flex flex-column" style="border-radius: 14px;">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="badge bg-dark text-white rounded-pill small">Chapter ${chNum}</span>
                <span class="badge ${chNum <= 2 ? 'bg-success text-white' : chNum <= 5 ? 'bg-primary text-white' : chNum <= 7 ? 'bg-warning text-dark' : 'bg-danger text-white'} rounded-pill small" style="font-size: 0.68rem;">
                  ${chNum <= 2 ? '🌱 Fundamentals' : chNum <= 5 ? '⚙️ Core Engineering' : chNum <= 7 ? '⚡ Advanced Concepts' : '🚀 Real-World Projects'}
                </span>
              </div>
              <h6 class="fw-bold text-dark mb-1.5">${escapeHtml(chTitle)}</h6>
              <p class="text-secondary small mb-2 fst-italic" style="font-size: 0.78rem;">
                "${escapeHtml(takeaways)}"
              </p>
              
              <!-- Section Content Coverage Badges -->
              <div class="d-flex flex-wrap gap-1 mb-2">
                <span class="badge bg-primary-subtle text-primary border border-primary-subtle" style="font-size: 0.68rem;">📘 Core Concepts</span>
                <span class="badge bg-dark text-white border" style="font-size: 0.68rem;">🚀 Real-World Projects</span>
                <span class="badge bg-warning-subtle text-dark border border-warning-subtle" style="font-size: 0.68rem;">📐 Formulas</span>
                <span class="badge bg-success-subtle text-success border border-success-subtle" style="font-size: 0.68rem;">💡 ${solvedCount} Solved Ex</span>
                <span class="badge bg-info-subtle text-info border border-info-subtle" style="font-size: 0.68rem;">📝 ${practiceCount} Practice Qs</span>
                <span class="badge bg-danger-subtle text-danger border border-danger-subtle" style="font-size: 0.68rem;">💼 ${interviewCount} Interview Qs</span>
              </div>

              <div class="d-flex flex-wrap gap-1 mb-3 pt-1 border-top">
                ${topics.map(t => `<span class="badge bg-white text-secondary border small" style="font-size: 0.7rem;">${escapeHtml(t)}</span>`).join('')}
              </div>

              <div class="d-flex gap-1.5 mt-auto pt-2">
                <button 
                  type="button" 
                  class="btn btn-primary btn-sm rounded-pill flex-grow-1 fw-semibold d-flex align-items-center justify-content-center gap-1 shadow-sm"
                  onclick="jumpToChapterInReader(${chNum})"
                >
                  <span>📖</span>
                  <span>Read Chapter</span>
                </button>
                <button 
                  type="button" 
                  class="btn btn-outline-success btn-sm rounded-pill px-2.5 fw-semibold"
                  title="Jump directly to Solved Examples in Chapter ${chNum}"
                  onclick="jumpToChapterSection(${chNum}, 'solved')"
                >
                  💡 Solved
                </button>
                <button 
                  type="button" 
                  class="btn btn-outline-info text-dark btn-sm rounded-pill px-2.5 fw-semibold"
                  title="Jump directly to Practice Questions in Chapter ${chNum}"
                  onclick="jumpToChapterSection(${chNum}, 'practice')"
                >
                  📝 Practice
                </button>
              </div>
            </div>
          </div>
        `;
      }).join("");
    } catch (err) {
      console.warn("Could not load chapter syllabus metadata", err);
    }
  }

  window.startBookExam = async function(subject) {
    activeQuiz.quizType = "daily";
    activeQuiz.roadmapSlug = null;
    activeQuiz.milestoneId = null;

    if (quizModalBadge) {
      quizModalBadge.textContent = `Strict Exam Grounding: ${subject} Book`;
      quizModalBadge.className = "badge bg-warning text-dark fw-bold px-3 py-1 rounded-pill";
    }
    if (quizModalTitle) quizModalTitle.textContent = `${subject} Prescribed Textbook Assessment`;

    if (quizLoadingView) quizLoadingView.style.display = "block";
    if (quizTakingView) quizTakingView.style.display = "none";
    if (quizResultsView) quizResultsView.style.display = "none";

    if (quizLoadingTitle) quizLoadingTitle.textContent = `Generating ${subject} Exam Questions...`;
    if (quizLoadingSubtext) quizLoadingSubtext.textContent = `All questions are strictly derived only from the 9 chapters in the prescribed ${subject} textbook.`;

    if (quizTimerPill) {
      quizTimerPill.classList.remove("urgent");
      if (quizTimerText) quizTimerText.textContent = "05:00";
    }

    if (quizModal) quizModal.show();

    try {
      const res = await api.studyMaterials.startDailyAssessment(subject);
      const data = res.data;
      if (!data || !data.questions || !data.questions.length) {
        throw new Error(`Could not generate ${subject} textbook assessment questions.`);
      }

      activeQuiz.questions = data.questions;
      activeQuiz.sessionId = data.session_id;
      activeQuiz.currentIndex = 0;
      activeQuiz.answers = {};

      activeQuiz.timeRemaining = data.questions.length * 30;
      activeQuiz.startTime = Date.now();

      startQuizTimer();

      if (quizLoadingView) quizLoadingView.style.display = "none";
      if (quizTakingView) quizTakingView.style.display = "block";

      renderCurrentQuestion();
    } catch (err) {
      alert(`Failed to start ${subject} book exam: ` + err.message);
      if (quizModal) quizModal.hide();
    }
  };

  window.handleBookPdfUpload = async function(input, subject) {
    if (!input || !input.files || !input.files[0]) return;
    const file = input.files[0];
    if (!file.name.toLowerCase().endsWith(".pdf")) {
      alert("Please select a PDF file.");
      input.value = "";
      return;
    }

    const formData = new FormData();
    formData.append("subject", subject.toLowerCase());
    formData.append("file", file);

    try {
      input.disabled = true;
      const res = await api.studyMaterials.uploadPrescribedBook(formData);
      alert(`✅ ${res.message || "Textbook PDF uploaded and synchronized successfully! Exam questions are now grounded in this book."}`);
      await loadPrescribedBooks();
    } catch (err) {
      alert(`Upload failed: ${err.message}`);
    } finally {
      input.disabled = false;
      input.value = "";
    }
  };

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
