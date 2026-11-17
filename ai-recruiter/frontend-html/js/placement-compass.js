/**
 * placement-compass.js — Controller for Placement Compass Suite
 * Supports:
 * 1. School Career Guidance Platform (After 10th & 12th)
 *    - Career Streams Explorer (5 Pillars)
 *    - Top College Comparator Across 10 Streams
 *    - Course vs Course Comparison Matrix
 *    - AI Career Matcher & Course Recommender
 *    - Entrance Exam Guidance & Calendar Sync
 *    - 5-Phase Admission & Counselling Roadmap
 * 2. Campus Placement & Company Match Predictor (College)
 */

let allSchoolPaths = [];
let allSchoolExams = [];
let allCareerPositions = [];
let allCollegesList = [];
let allComparableCourses = [];
let activeGradeFilter = "all";
let activeCatFilter = "all";
let activeCollegeStreamFilter = "all";
let activeExamStageFilter = "all";
let activePosStageFilter = "all";
let activePosSectorFilter = "all";
let activePosSearchQuery = "";
let currentExamSectionView = "positions";
let currentModalPathId = null;
let currentModalPositionId = null;

// College Placement state
let allCompaniesList = [];
let cachedDrives = [];

document.addEventListener("DOMContentLoaded", async () => {
  setupUserGreeting();

  // Load initial mode
  const savedMode = localStorage.getItem("compass_active_hub") || "school";
  setCompassMode(savedMode);

  // Initialize both engines
  await initSchoolCareerHub();
  await initCollegePlacementHub();
});

function setupUserGreeting() {
  const userGreeting = document.getElementById("user-greeting");
  if (!userGreeting) return;
  const user = typeof Session !== "undefined" ? Session.getUser() : null;
  if (user && user.full_name) {
    userGreeting.textContent = `Welcome, ${user.full_name}`;
  } else if (user && user.email) {
    userGreeting.textContent = user.email;
  }
}

// -------------------------------------------------------------
// TOP HUB SWITCHER (SCHOOL GUIDE vs COLLEGE PLACEMENT)
// -------------------------------------------------------------
function setCompassMode(mode) {
  localStorage.setItem("compass_active_hub", mode);

  const btnSchool = document.getElementById("btn-mode-school");
  const btnCollege = document.getElementById("btn-mode-college");
  const hubSchool = document.getElementById("compass-hub-school");
  const hubCollege = document.getElementById("compass-hub-college");

  if (mode === "school") {
    btnSchool?.classList.add("active");
    btnCollege?.classList.remove("active");
    hubSchool?.classList.remove("d-none");
    hubCollege?.classList.add("d-none");
  } else {
    btnCollege?.classList.add("active");
    btnSchool?.classList.remove("active");
    hubCollege?.classList.remove("d-none");
    hubSchool?.classList.add("d-none");
  }

  window.scrollTo({ top: 0, behavior: "smooth" });
}

// =========================================================================
// PART 1: SCHOOL CAREER GUIDANCE HUB (AFTER 10TH & 12TH)
// =========================================================================

async function initSchoolCareerHub() {
  try {
    // 1. Fetch all school career paths
    const pathsRes = await api.get("/placement-compass/school/paths");
    if (pathsRes && pathsRes.data) {
      allSchoolPaths = pathsRes.data;
      renderSchoolPaths();
    }

    // 2. Fetch Top Colleges directory
    const collegesRes = await api.get("/placement-compass/colleges");
    if (collegesRes && collegesRes.data) {
      allCollegesList = collegesRes.data;
      populateCollegeDropdowns();
      renderCollegesCategoryGrid();
      presetCollegeCompare("engineering");
    }

    // 3. Fetch Comparable Courses
    const coursesRes = await api.get("/placement-compass/courses");
    if (coursesRes && coursesRes.data) {
      allComparableCourses = coursesRes.data;
      populateCourseDropdowns();
      presetCourseCompare("cse_vs_ece_vs_poly");
    }

    // 4. Fetch school entrance exams calendar
    const examsRes = await api.get("/placement-compass/school/exams");
    if (examsRes && examsRes.data) {
      allSchoolExams = examsRes.data;
      renderSchoolExams();
    }

    // 5. Fetch career positions and their relevant entrance examinations
    const posRes = await api.get("/placement-compass/positions");
    if (posRes && posRes.data) {
      allCareerPositions = posRes.data;
      renderCareerPositions();
    }
  } catch (err) {
    console.error("Failed to initialize School Career Hub:", err);
  }
}

// Subnav Tabs in School Mode
function switchSchoolTab(tabId) {
  const tabs = ["explorer", "colleges", "courses", "matcher", "exams", "roadmap"];
  const buttons = document.querySelectorAll("[data-school-tab]");

  buttons.forEach((btn) => {
    if (btn.getAttribute("data-school-tab") === tabId) {
      btn.classList.add("active");
    } else {
      btn.classList.remove("active");
    }
  });

  tabs.forEach((t) => {
    const el = document.getElementById(`school-tab-${t}`);
    if (el) {
      if (t === tabId) {
        el.classList.remove("d-none");
      } else {
        el.classList.add("d-none");
      }
    }
  });

  window.scrollTo({ top: 120, behavior: "smooth" });
}

// -------------------------------------------------------------
// 1. CAREER STREAMS EXPLORER & STAGE SWITCHER
// -------------------------------------------------------------
function filterByStage(stage, btn) {
  document.querySelectorAll("#school-stage-selector .stage-select-btn").forEach((b) => b.classList.remove("active"));
  if (btn) btn.classList.add("active");

  activeGradeFilter = stage;
  activeExamStageFilter = stage;

  // Sync with explorer chips if present
  document.querySelectorAll("[data-filter-type='grade']").forEach((b) => {
    if (b.getAttribute("data-val") === stage) {
      b.classList.add("active");
    } else {
      b.classList.remove("active");
    }
  });

  // Sync with exam stage filter buttons if present
  document.querySelectorAll("#exam-stage-filter-btns button").forEach((b) => {
    if (b.getAttribute("data-exam-stage") === stage) {
      b.classList.remove("btn-outline-primary");
      b.classList.add("btn-primary", "shadow-sm");
    } else {
      b.classList.remove("btn-primary", "shadow-sm");
      b.classList.add("btn-outline-primary");
    }
  });

  // Sync with position stage pills if present
  activePosStageFilter = stage;
  document.querySelectorAll("#position-stage-pills button").forEach((b) => {
    if (b.getAttribute("data-pos-stage") === stage) {
      b.classList.remove("btn-outline-primary");
      b.classList.add("btn-primary", "shadow-sm");
    } else {
      b.classList.remove("btn-primary", "shadow-sm");
      b.classList.add("btn-outline-primary");
    }
  });

  renderSchoolPaths();
  renderCollegesCategoryGrid();
  populateCollegeDropdowns();
  renderSchoolExams();
  renderCareerPositions();
}

function filterExamsByStage(stage, btn) {
  activeExamStageFilter = stage;
  document.querySelectorAll("#exam-stage-filter-btns button").forEach((b) => {
    b.classList.remove("btn-primary", "shadow-sm");
    b.classList.add("btn-outline-primary");
  });
  if (btn) {
    btn.classList.remove("btn-outline-primary");
    btn.classList.add("btn-primary", "shadow-sm");
  }
  renderSchoolExams();
}

function filterPathsByGrade(grade, btn) {
  activeGradeFilter = grade;
  document.querySelectorAll("[data-filter-type='grade']").forEach((b) => b.classList.remove("active"));
  btn.classList.add("active");

  // Sync with master stage switcher
  document.querySelectorAll("#school-stage-selector .stage-select-btn").forEach((b) => {
    const s = b.getAttribute("data-stage");
    if ((grade === "after_10th" && s === "after_10th") || (grade.startsWith("after_12th") && s === "after_12th") || (grade === "all" && s === "all")) {
      b.classList.add("active");
    } else {
      b.classList.remove("active");
    }
  });

  renderSchoolPaths();
}

function filterPathsByCategory(cat, btn) {
  activeCatFilter = cat;
  document.querySelectorAll("[data-filter-type='cat']").forEach((b) => b.classList.remove("active"));
  btn.classList.add("active");
  renderSchoolPaths();
}

function renderSchoolPaths() {
  const grid = document.getElementById("school-paths-grid");
  if (!grid) return;

  let filtered = allSchoolPaths;

  if (activeGradeFilter !== "all") {
    if (activeGradeFilter === "after_10th") {
      filtered = filtered.filter(
        (p) => p.grade_level === "after_10th" || p.grade_level === "after_10th_or_12th"
      );
    } else if (activeGradeFilter === "after_12th") {
      filtered = filtered.filter(
        (p) => p.grade_level.startsWith("after_12th") || p.grade_level === "after_10th_or_12th"
      );
    } else {
      filtered = filtered.filter(
        (p) => p.grade_level === activeGradeFilter || p.grade_level === "after_10th_or_12th"
      );
    }
  }

  if (activeCatFilter !== "all") {
    filtered = filtered.filter((p) => p.category === activeCatFilter);
  }

  if (filtered.length === 0) {
    grid.innerHTML = `
      <div class="col-12 text-center py-5 bg-white rounded-4 border">
        <div class="fs-1 mb-2">🔍</div>
        <h6 class="fw-bold">No career paths match the selected filters.</h6>
        <p class="text-muted small">Try selecting "All Opportunities" or choose a different stream.</p>
        <button class="btn btn-outline-primary btn-sm rounded-pill" onclick="resetSchoolFilters()">Reset Filters</button>
      </div>
    `;
    return;
  }

  grid.innerHTML = filtered
    .map((path) => {
      const examsBadges = path.entrance_exams
        .slice(0, 3)
        .map((e) => `<span class="badge bg-light text-dark border small">${e.name}</span>`)
        .join(" ");

      const collegesList = path.top_colleges.slice(0, 2).join(", ");

      const gradeLabelMap = {
        after_10th: "Direct After 10th (SSLC)",
        after_12th_pcm: "12th Science (PCM)",
        after_12th_pcb: "12th Science (PCB)",
        after_12th_commerce: "12th Commerce",
        after_12th_arts: "12th Arts",
        after_12th_vocational: "12th Vocational",
        after_10th_or_12th: "After 10th or 12th",
      };

      return `
        <div class="col-md-6 col-lg-4">
          <div class="path-card border-${path.category}">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div class="d-flex align-items-center gap-2">
                <span class="fs-2">${path.icon_emoji}</span>
                <div>
                  <h6 class="fw-bold mb-0 text-dark" style="line-height: 1.3;">${path.title}</h6>
                  <span class="badge bg-primary-subtle text-primary border rounded-pill small">${gradeLabelMap[path.grade_level] || path.grade_level}</span>
                </div>
              </div>
            </div>

            <p class="text-secondary small mb-3" style="min-height: 38px;">${path.tagline}</p>

            <div class="bg-light p-2.5 rounded-3 mb-3 small">
              <div class="mb-1"><strong>⏳ Duration:</strong> <span class="text-dark">${path.duration}</span></div>
              <div class="mb-1"><strong>🎓 Eligibility:</strong> <span class="text-muted">${path.eligibility}</span></div>
              <div class="mb-1"><strong>📝 Entrance Exams:</strong> <div class="d-flex flex-wrap gap-1 mt-1">${examsBadges}</div></div>
              <div class="mt-2 pt-2 border-top">
                <strong>🏛️ Top Colleges:</strong> <span class="text-secondary">${collegesList} + more</span>
              </div>
            </div>

            <div class="d-flex justify-content-between align-items-center my-2 py-1 px-2.5 bg-success-subtle rounded-3 small">
              <span class="fw-bold text-success">Starting Salary:</span>
              <span class="fw-bold text-dark">${path.starting_salary_range}</span>
            </div>

            <div class="d-flex gap-2 mt-auto pt-3 border-top">
              <button class="btn btn-primary btn-sm w-70 rounded-pill fw-bold" onclick="openPathwayModal('${path.id}')">
                📖 View Full Guide
              </button>
              <button class="btn btn-outline-secondary btn-sm w-30 rounded-pill fw-semibold" onclick="quickJumpToColleges('${path.category}')">
                🏛️ Colleges
              </button>
            </div>
          </div>
        </div>
      `;
    })
    .join("");
}

function resetSchoolFilters() {
  activeGradeFilter = "all";
  activeCatFilter = "all";
  document.querySelectorAll("[data-filter-type]").forEach((b) => {
    if (b.getAttribute("data-val") === "all") b.classList.add("active");
    else b.classList.remove("active");
  });
  renderSchoolPaths();
}

function quickJumpToColleges(category) {
  switchSchoolTab("colleges");
  const btn = document.querySelector(`[data-college-filter="${category}"]`);
  if (btn) {
    filterCollegesByCategory(category, btn);
  }
}

// -------------------------------------------------------------
// 2. TOP COLLEGE COMPARATOR (ACROSS 10 STREAMS)
// -------------------------------------------------------------
function populateCollegeDropdowns(selectedCategory = "all") {
  const c1 = document.getElementById("college-select-1");
  const c2 = document.getElementById("college-select-2");
  const c3 = document.getElementById("college-select-3");
  if (!c1 || !c2 || !c3) return;

  let pool = allCollegesList;
  if (selectedCategory && selectedCategory !== "all") {
    pool = pool.filter((c) => c.category === selectedCategory);
  }

  const options = pool
    .map((c) => `<option value="${c.id}">${c.logo_emoji} ${c.name} (${c.location.split(",")[0]})</option>`)
    .join("");

  c1.innerHTML = options;
  c2.innerHTML = options;
  c3.innerHTML = `<option value="">None (Compare 2)</option>` + options;

  if (pool.length >= 2) {
    c1.selectedIndex = 0;
    c2.selectedIndex = 1;
  }
  if (pool.length >= 3) {
    c3.selectedIndex = 2;
  }
}

function filterCollegesByCategory(category, btn) {
  activeCollegeStreamFilter = category;
  document.querySelectorAll("[data-college-filter]").forEach((b) => b.classList.remove("active"));
  btn.classList.add("active");

  populateCollegeDropdowns(category);
  renderCollegesCategoryGrid();
  runCollegeComparison();
}

function renderCollegesCategoryGrid() {
  const container = document.getElementById("colleges-category-grid");
  const countIndicator = document.getElementById("colleges-count-indicator");
  if (!container) return;

  let filtered = allCollegesList;
  if (activeCollegeStreamFilter !== "all") {
    filtered = filtered.filter((c) => c.category === activeCollegeStreamFilter);
  }

  if (countIndicator) {
    countIndicator.textContent = `Showing ${filtered.length} premier colleges`;
  }

  container.innerHTML = filtered
    .map(
      (c) => `
      <div class="col-md-6 col-lg-4">
        <div class="p-3 bg-light rounded-4 border h-100 d-flex flex-column">
          <div class="d-flex align-items-center gap-2 mb-2">
            <span class="fs-2">${c.logo_emoji}</span>
            <div>
              <h6 class="fw-bold mb-0 text-dark" style="font-size: 0.95rem;">${c.name}</h6>
              <span class="badge bg-primary-subtle text-primary border small">${c.nirf_ranking.split("|")[0]}</span>
            </div>
          </div>
          <p class="small text-muted mb-2">📍 ${c.location} | ${c.accreditation}</p>

          <div class="bg-white p-2 rounded-3 border small mb-2">
            <div><strong>🎓 Courses:</strong> <span class="text-secondary">${c.flagship_courses.slice(0, 2).join(", ")}</span></div>
            <div><strong>💰 Fees:</strong> <span class="text-success fw-semibold">${c.tuition_fees_per_year.split("(")[0]}</span></div>
            <div><strong>🚀 Placements:</strong> <span class="text-dark fw-bold">Avg ${c.placement_stats.average_package}</span></div>
          </div>

          <div class="d-flex gap-2 mt-auto pt-2 border-top">
            <button class="btn btn-outline-primary btn-sm w-100 rounded-pill fw-semibold" onclick="quickAddCollegeToCompare('${c.id}')">
              ⚖️ Compare This College
            </button>
          </div>
        </div>
      </div>
    `
    )
    .join("");
}

function quickAddCollegeToCompare(collegeId) {
  const c1 = document.getElementById("college-select-1");
  const c2 = document.getElementById("college-select-2");
  if (c1 && c2) {
    if (c1.value !== collegeId) {
      c2.value = collegeId;
    }
  }
  runCollegeComparison();
  document.getElementById("school-tab-colleges")?.scrollIntoView({ behavior: "smooth" });
}

function presetCollegeCompare(stream) {
  const c1 = document.getElementById("college-select-1");
  const c2 = document.getElementById("college-select-2");
  const c3 = document.getElementById("college-select-3");

  if (stream === "engineering") {
    populateCollegeDropdowns("engineering");
    if (c1) c1.value = "iit_madras";
    if (c2) c2.value = "anna_univ_ceg";
    if (c3) c3.value = "nit_trichy";
  } else if (stream === "medical") {
    populateCollegeDropdowns("medical");
    if (c1) c1.value = "madras_medical_college";
    if (c2) c2.value = "stanley_medical_college";
    if (c3) c3.value = "cmc_vellore";
  } else if (stream === "polytechnic") {
    populateCollegeDropdowns("polytechnic_diploma");
    if (c1) c1.value = "cpt_chennai";
    if (c2) c2.value = "psg_polytechnic";
    if (c3) c3.value = "murugappa_poly";
  } else if (stream === "iti") {
    populateCollegeDropdowns("vocational_iti");
    if (c1) c1.value = "govt_iti_guindy";
    if (c2) c2.value = "govt_iti_coimbatore";
    if (c3) c3.value = "";
  } else if (stream === "law") {
    populateCollegeDropdowns("law");
    if (c1) c1.value = "soel_tndalu";
    if (c2) c2.value = "tnnlu_trichy";
    if (c3) c3.value = "";
  }

  runCollegeComparison();
}

async function runCollegeComparison() {
  const c1 = document.getElementById("college-select-1")?.value;
  const c2 = document.getElementById("college-select-2")?.value;
  const c3 = document.getElementById("college-select-3")?.value;

  const ids = [c1, c2, c3].filter((id) => id && id.trim().length > 0);
  const uniqueIds = Array.from(new Set(ids));

  if (uniqueIds.length < 2) {
    alert("Please select at least 2 colleges to compare.");
    return;
  }

  try {
    const res = await api.post("/placement-compass/colleges/compare", {
      college_ids: uniqueIds,
    });

    if (res && res.data && res.data.colleges) {
      renderCollegeComparisonMatrix(res.data.colleges);
    }
  } catch (err) {
    console.error("College comparison failed:", err);
  }
}

function renderCollegeComparisonMatrix(colleges) {
  const container = document.getElementById("college-compare-matrix-container");
  if (!container) return;

  const colWidth = Math.floor(75 / colleges.length);

  container.innerHTML = `
    <table class="table career-compare-table align-middle mb-0">
      <thead>
        <tr>
          <th style="width: 25%;" class="bg-light text-secondary">COLLEGE BENCHMARK</th>
          ${colleges
            .map(
              (c) => `
            <th style="width: ${colWidth}%;" class="text-center">
              <div class="fs-1 mb-1">${c.logo_emoji}</div>
              <h5 class="fw-bold mb-0 text-dark">${c.name}</h5>
              <div class="small text-muted mb-1">📍 ${c.location}</div>
              <span class="badge bg-primary text-white rounded-pill px-2.5 py-1 small fw-bold">
                ${c.nirf_ranking.split("|")[0]}
              </span>
            </th>
          `
            )
            .join("")}
        </tr>
      </thead>
      <tbody>
        <!-- Flagship Courses -->
        <tr class="table-light">
          <td colspan="${colleges.length + 1}" class="fw-bold text-primary small text-uppercase py-2 px-3">
            🎓 Academic Programs &amp; Accreditations
          </td>
        </tr>
        <tr>
          <td class="fw-bold text-secondary">Accreditation &amp; Status</td>
          ${colleges.map((c) => `<td class="text-center small fw-semibold text-dark">${c.accreditation}</td>`).join("")}
        </tr>
        <tr>
          <td class="fw-bold text-secondary">Flagship Degrees / Courses</td>
          ${colleges
            .map(
              (c) => `
            <td class="small">
              <ul class="ps-3 mb-0 text-secondary">
                ${c.flagship_courses.map((cr) => `<li>${cr}</li>`).join("")}
              </ul>
            </td>
          `
            )
            .join("")}
        </tr>

        <!-- Eligibility Criteria -->
        <tr class="table-light">
          <td colspan="${colleges.length + 1}" class="fw-bold text-primary small text-uppercase py-2 px-3">
            📋 Course Eligibility Requirements
          </td>
        </tr>
        <tr>
          <td class="fw-bold text-secondary">Minimum Eligibility Criteria</td>
          ${colleges.map((c) => `<td class="small text-secondary">${c.eligibility_criteria}</td>`).join("")}
        </tr>

        <!-- Entrance Exam & Exam Schedule -->
        <tr class="table-light">
          <td colspan="${colleges.length + 1}" class="fw-bold text-primary small text-uppercase py-2 px-3">
            📝 Entrance Exam Guidance &amp; Exact Schedule
          </td>
        </tr>
        <tr>
          <td class="fw-bold text-secondary">Entrance Exams Accepted</td>
          ${colleges
            .map(
              (c) => `
            <td>
              <div class="d-flex flex-wrap gap-1 justify-content-center">
                ${c.entrance_exams.map((e) => `<span class="badge bg-info-subtle text-dark border small">${e}</span>`).join("")}
              </div>
            </td>
          `
            )
            .join("")}
        </tr>
        <tr>
          <td class="fw-bold text-secondary">Exam Application Dates</td>
          ${colleges
            .map(
              (c) => `
            <td class="small text-center">
              <div><strong>Start:</strong> ${c.exam_schedule.application_start}</div>
              <div class="text-danger"><strong>Last Date:</strong> ${c.exam_schedule.last_date}</div>
            </td>
          `
            )
            .join("")}
        </tr>
        <tr>
          <td class="fw-bold text-secondary">Exam Date &amp; Results</td>
          ${colleges
            .map(
              (c) => `
            <td class="small text-center">
              <div><strong>Exam Date:</strong> ${c.exam_schedule.exam_date}</div>
              <div class="text-success"><strong>Result:</strong> ${c.exam_schedule.result_date}</div>
            </td>
          `
            )
            .join("")}
        </tr>

        <!-- Admission & Counselling Guidance -->
        <tr class="table-light">
          <td colspan="${colleges.length + 1}" class="fw-bold text-primary small text-uppercase py-2 px-3">
            ⚡ Admission &amp; Counselling Procedure
          </td>
        </tr>
        <tr>
          <td class="fw-bold text-secondary">Complete Admission Process</td>
          ${colleges.map((c) => `<td class="small text-secondary" style="line-height: 1.6;">${c.admission_counselling_process}</td>`).join("")}
        </tr>

        <!-- Fees & Scholarships -->
        <tr class="table-light">
          <td colspan="${colleges.length + 1}" class="fw-bold text-primary small text-uppercase py-2 px-3">
            💰 Annual Fees &amp; Scholarship Coverage
          </td>
        </tr>
        <tr>
          <td class="fw-bold text-secondary">Tuition Fees / Year</td>
          ${colleges.map((c) => `<td class="text-center fw-bold text-success small">${c.tuition_fees_per_year}</td>`).join("")}
        </tr>
        <tr>
          <td class="fw-bold text-secondary">Hostel &amp; Mess Fees / Year</td>
          ${colleges.map((c) => `<td class="text-center text-muted small">${c.hostel_mess_fees_per_year}</td>`).join("")}
        </tr>
        <tr>
          <td class="fw-bold text-secondary">Scholarships Available</td>
          ${colleges
            .map(
              (c) => `
            <td class="small">
              <ul class="ps-3 mb-0 text-success">
                ${c.scholarships_available.map((s) => `<li>${s}</li>`).join("")}
              </ul>
            </td>
          `
            )
            .join("")}
        </tr>

        <!-- Placements -->
        <tr class="table-light">
          <td colspan="${colleges.length + 1}" class="fw-bold text-primary small text-uppercase py-2 px-3">
            🚀 Campus Placement Packages &amp; Opportunities
          </td>
        </tr>
        <tr>
          <td class="fw-bold text-secondary">Highest CTC Package</td>
          ${colleges.map((c) => `<td class="text-center fw-bold text-dark">${c.placement_stats.highest_package}</td>`).join("")}
        </tr>
        <tr>
          <td class="fw-bold text-secondary">Average CTC Package</td>
          ${colleges.map((c) => `<td class="text-center fw-bold text-primary fs-6">${c.placement_stats.average_package}</td>`).join("")}
        </tr>
        <tr>
          <td class="fw-bold text-secondary">Placement Success %</td>
          ${colleges.map((c) => `<td class="text-center fw-bold text-success">${c.placement_stats.placement_percentage}</td>`).join("")}
        </tr>
        <tr>
          <td class="fw-bold text-secondary">Top Visiting Recruiters</td>
          ${colleges
            .map(
              (c) => `
            <td>
              <div class="d-flex flex-wrap gap-1 justify-content-center">
                ${c.placement_stats.top_recruiters.map((r) => `<span class="badge bg-secondary-subtle text-dark small">${r}</span>`).join("")}
              </div>
            </td>
          `
            )
            .join("")}
        </tr>

        <!-- Facilities -->
        <tr class="table-light">
          <td colspan="${colleges.length + 1}" class="fw-bold text-primary small text-uppercase py-2 px-3">
            🏛️ Campus Infrastructure &amp; Facilities
          </td>
        </tr>
        <tr>
          <td class="fw-bold text-secondary">Campus Facilities</td>
          ${colleges
            .map(
              (c) => `
            <td class="small">
              <ul class="ps-3 mb-0 text-secondary">
                ${c.campus_facilities.map((f) => `<li>${f}</li>`).join("")}
              </ul>
            </td>
          `
            )
            .join("")}
        </tr>

        <!-- Pros & Cons -->
        <tr class="table-light">
          <td colspan="${colleges.length + 1}" class="fw-bold text-primary small text-uppercase py-2 px-3">
            ⚖️ Key Advantages &amp; Considerations
          </td>
        </tr>
        <tr>
          <td class="fw-bold text-success">Verified Advantages</td>
          ${colleges
            .map(
              (c) => `
            <td class="small">
              <ul class="ps-3 mb-0 text-success">
                ${c.pros.map((p) => `<li>${p}</li>`).join("")}
              </ul>
            </td>
          `
            )
            .join("")}
        </tr>
        <tr>
          <td class="fw-bold text-danger">Considerations</td>
          ${colleges
            .map(
              (c) => `
            <td class="small">
              <ul class="ps-3 mb-0 text-secondary">
                ${c.cons.map((cn) => `<li>${cn}</li>`).join("")}
              </ul>
            </td>
          `
            )
            .join("")}
        </tr>
      </tbody>
    </table>
  `;
}

// -------------------------------------------------------------
// 3. COURSE VS COURSE COMPARISON
// -------------------------------------------------------------
function populateCourseDropdowns() {
  const cr1 = document.getElementById("course-select-1");
  const cr2 = document.getElementById("course-select-2");
  const cr3 = document.getElementById("course-select-3");
  if (!cr1 || !cr2 || !cr3) return;

  const options = allComparableCourses
    .map((cr) => `<option value="${cr.id}">${cr.course_name} (${cr.duration})</option>`)
    .join("");

  cr1.innerHTML = options;
  cr2.innerHTML = options;
  cr3.innerHTML = `<option value="">None (Compare 2)</option>` + options;
}

function presetCourseCompare(preset) {
  const cr1 = document.getElementById("course-select-1");
  const cr2 = document.getElementById("course-select-2");
  const cr3 = document.getElementById("course-select-3");

  if (preset === "cse_vs_ece_vs_poly") {
    if (cr1) cr1.value = "btech_cse";
    if (cr2) cr2.value = "btech_ece";
    if (cr3) cr3.value = "diploma_computer_engg";
  } else if (preset === "mbbs_vs_pharm_vs_nurse") {
    if (cr1) cr1.value = "mbbs_course";
    if (cr2) cr2.value = "b_pharm_course";
    if (cr3) cr3.value = "bsc_nursing_course";
  } else if (preset === "10th_stream_vs_poly_vs_iti") {
    if (cr1) cr1.value = "hsc_bio_maths";
    if (cr2) cr2.value = "diploma_mechanical_engg";
    if (cr3) cr3.value = "iti_electrician_fitter";
  } else if (preset === "law_vs_govt") {
    if (cr1) cr1.value = "ba_llb_law";
    if (cr2) cr2.value = "nda_military";
    if (cr3) cr3.value = "tnpsc_group4_vao";
  }

  runCourseComparison();
}

async function runCourseComparison() {
  const cr1 = document.getElementById("course-select-1")?.value;
  const cr2 = document.getElementById("course-select-2")?.value;
  const cr3 = document.getElementById("course-select-3")?.value;

  const ids = [cr1, cr2, cr3].filter((id) => id && id.trim().length > 0);
  const uniqueIds = Array.from(new Set(ids));

  if (uniqueIds.length < 2) {
    alert("Please select at least 2 courses to compare.");
    return;
  }

  try {
    const res = await api.post("/placement-compass/courses/compare", {
      course_ids: uniqueIds,
    });

    if (res && res.data && res.data.courses) {
      renderCourseComparisonMatrix(res.data.courses);
    }
  } catch (err) {
    console.error("Course comparison error:", err);
  }
}

function renderCourseComparisonMatrix(courses) {
  const container = document.getElementById("course-compare-matrix-container");
  if (!container) return;

  const colWidth = Math.floor(75 / courses.length);

  container.innerHTML = `
    <table class="table career-compare-table align-middle mb-0">
      <thead>
        <tr>
          <th style="width: 25%;" class="bg-light text-secondary">COURSE COMPARISON</th>
          ${courses
            .map(
              (cr) => `
            <th style="width: ${colWidth}%;" class="text-center">
              <h5 class="fw-bold mb-1 text-dark">${cr.course_name}</h5>
              <span class="badge bg-primary-subtle text-primary border rounded-pill px-2.5 py-1 small fw-bold">
                ${cr.duration}
              </span>
            </th>
          `
            )
            .join("")}
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="fw-bold text-secondary">Eligibility Criteria</td>
          ${courses.map((cr) => `<td class="small text-secondary">${cr.eligibility}</td>`).join("")}
        </tr>
        <tr>
          <td class="fw-bold text-secondary">Required Entrance Exams</td>
          ${courses
            .map(
              (cr) => `
            <td>
              <div class="d-flex flex-wrap gap-1 justify-content-center">
                ${cr.entrance_exams.map((e) => `<span class="badge bg-light text-dark border small">${e}</span>`).join("")}
              </div>
            </td>
          `
            )
            .join("")}
        </tr>
        <tr>
          <td class="fw-bold text-secondary">Average Starting Salary</td>
          ${courses.map((cr) => `<td class="text-center fw-bold text-success fs-6">${cr.avg_starting_salary}</td>`).join("")}
        </tr>
        <tr>
          <td class="fw-bold text-secondary">Top Roles &amp; Opportunities</td>
          ${courses
            .map(
              (cr) => `
            <td class="small">
              <ul class="ps-3 mb-0 text-secondary">
                ${cr.top_roles.map((r) => `<li>${r}</li>`).join("")}
              </ul>
            </td>
          `
            )
            .join("")}
        </tr>
        <tr>
          <td class="fw-bold text-secondary">Future Scopes &amp; Lateral Entry</td>
          ${courses
            .map(
              (cr) => `
            <td class="small">
              <ul class="ps-3 mb-0 text-secondary">
                ${cr.future_scopes.map((f) => `<li>${f}</li>`).join("")}
              </ul>
            </td>
          `
            )
            .join("")}
        </tr>
        <tr>
          <td class="fw-bold text-secondary">Why Choose This Course</td>
          ${courses.map((cr) => `<td class="small text-dark fw-medium">${cr.why_choose}</td>`).join("")}
        </tr>
      </tbody>
    </table>
  `;
}

// -------------------------------------------------------------
// 4. PATHWAY DETAIL MODAL
// -------------------------------------------------------------
function openPathwayModal(pathId) {
  const path = allSchoolPaths.find((p) => p.id === pathId);
  if (!path) return;
  currentModalPathId = pathId;

  document.getElementById("modal-path-icon").textContent = path.icon_emoji;
  document.getElementById("modal-path-title").textContent = path.title;
  document.getElementById("modal-path-category").textContent = path.category.toUpperCase().replace("_", " ");
  document.getElementById("modal-path-duration").textContent = path.duration;

  const examsHtml = path.entrance_exams
    .map(
      (e) => `
      <div class="p-3 bg-light rounded-3 border mb-2">
        <div class="d-flex justify-content-between align-items-center mb-1">
          <strong class="text-dark">${e.name}</strong>
          <span class="badge bg-primary text-white">${e.level}</span>
        </div>
        <p class="small text-secondary mb-1">${e.description}</p>
        ${e.official_portal ? `<a href="${e.official_portal}" target="_blank" rel="noopener noreferrer" class="small text-primary fw-bold text-decoration-none">🔗 Official Portal: ${e.official_portal} &rarr;</a>` : ""}
      </div>
    `
    )
    .join("");

  const collegesHtml = path.top_colleges.map((c) => `<li class="mb-1">${c}</li>`).join("");
  const scholarshipsHtml = path.scholarships.map((s) => `<li class="mb-1 text-success fw-medium">${s}</li>`).join("");
  const careersHtml = path.career_opportunities.map((co) => `<li class="mb-1">${co}</li>`).join("");
  const futureHtml = path.future_study_options.map((f) => `<li class="mb-1">${f}</li>`).join("");

  document.getElementById("modal-path-body").innerHTML = `
    <div class="mb-4">
      <h6 class="fw-bold text-secondary text-uppercase small">Overview &amp; Focus</h6>
      <p class="fs-6 text-dark">${path.tagline}</p>
      <div class="alert alert-primary py-2 px-3 small rounded-3">
        <strong>🎓 Eligibility Criteria:</strong> ${path.eligibility}
      </div>
    </div>

    <!-- Entrance Exams -->
    <div class="mb-4">
      <h6 class="fw-bold text-secondary text-uppercase small mb-2">Required Entrance Exams</h6>
      ${examsHtml}
    </div>

    <!-- Step by Step Admission Procedure -->
    <div class="mb-4">
      <h6 class="fw-bold text-secondary text-uppercase small mb-2">How to Apply &amp; Admission Procedure</h6>
      <div class="p-3 bg-white border rounded-3 text-secondary small" style="line-height: 1.7;">
        ${path.admission_procedure}
      </div>
    </div>

    <!-- Colleges & Universities -->
    <div class="row g-3 mb-4">
      <div class="col-md-6">
        <div class="p-3 bg-light rounded-3 border h-100">
          <h6 class="fw-bold text-dark small mb-2">🏛️ Available Premier Colleges &amp; Universities</h6>
          <ul class="ps-3 mb-0 small text-secondary">
            ${collegesHtml}
          </ul>
        </div>
      </div>
      <div class="col-md-6">
        <div class="p-3 bg-light rounded-3 border h-100">
          <h6 class="fw-bold text-dark small mb-2">💰 Course Fees &amp; Financial Aid</h6>
          <div class="small mb-2">
            <strong>Government Seat:</strong> <span class="text-success fw-bold">${path.estimated_fees.govt_college}</span>
          </div>
          <div class="small mb-3">
            <strong>Private Seat:</strong> <span class="text-dark fw-bold">${path.estimated_fees.private_college}</span>
          </div>
          <h6 class="fw-bold text-success small mb-1">Scholarships &amp; Waivers:</h6>
          <ul class="ps-3 mb-0 small text-secondary">
            ${scholarshipsHtml}
          </ul>
        </div>
      </div>
    </div>

    <!-- Career Opportunities & Starting Salary -->
    <div class="row g-3">
      <div class="col-md-6">
        <div class="p-3 bg-success-subtle rounded-3 border border-success-subtle h-100">
          <h6 class="fw-bold text-success small mb-2">💼 Career Opportunities &amp; Job Profiles</h6>
          <ul class="ps-3 mb-2 small text-dark">
            ${careersHtml}
          </ul>
          <div class="fw-bold text-dark small pt-2 border-top border-success-subtle">
            Starting Salary: <span class="badge bg-success text-white">${path.starting_salary_range}</span>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="p-3 bg-light rounded-3 border h-100">
          <h6 class="fw-bold text-primary small mb-2">🚀 Future Higher Education Options</h6>
          <ul class="ps-3 mb-0 small text-secondary">
            ${futureHtml}
          </ul>
        </div>
      </div>
    </div>
  `;

  const modalEl = document.getElementById("pathwayDetailModal");
  const modal = new bootstrap.Modal(modalEl);
  modal.show();
}

function addCurrentModalPathToCompare() {
  if (currentModalPathId) {
    const p = allSchoolPaths.find((item) => item.id === currentModalPathId);
    if (p) {
      quickJumpToColleges(p.category);
    }
    const modalEl = document.getElementById("pathwayDetailModal");
    const modalInstance = bootstrap.Modal.getInstance(modalEl);
    if (modalInstance) modalInstance.hide();
  }
}

// -------------------------------------------------------------
// 5. AI CAREER MATCHER & COURSE FINDER
// -------------------------------------------------------------
function toggleInterest(chip) {
  chip.classList.toggle("selected");
}

async function handleCareerMatcherSubmit(event) {
  event.preventDefault();

  const grade = document.getElementById("matcher-grade").value;
  const pct = parseFloat(document.getElementById("matcher-percentage").value) || 85.0;
  const budget = document.getElementById("matcher-budget").value;

  const selectedChips = document.querySelectorAll("#matcher-interests-container .interest-tag-btn.selected");
  const interests = Array.from(selectedChips).map((c) => c.getAttribute("data-interest"));

  if (interests.length === 0) {
    alert("Please select at least 1 interest or passion tag.");
    return;
  }

  try {
    const res = await api.post("/placement-compass/school/recommend", {
      current_grade: grade,
      percentage: pct,
      interests: interests,
      budget_preference: budget,
      preferred_location: "All India",
    });

    if (res && res.data) {
      renderMatcherResults(res.data);
    }
  } catch (err) {
    console.error("Career matcher failed:", err);
    alert("Could not evaluate recommendations. Please try again.");
  }
}

function renderMatcherResults(data) {
  const section = document.getElementById("matcher-results-section");
  const guidanceEl = document.getElementById("matcher-guidance-text");
  const cardsContainer = document.getElementById("matcher-results-cards");

  if (!section || !cardsContainer) return;

  section.classList.remove("d-none");
  if (guidanceEl) guidanceEl.textContent = data.stream_guidance;

  cardsContainer.innerHTML = data.top_recommendations
    .map((rec) => {
      const p = rec.path;
      const reasonsList = rec.fit_reasons.map((r) => `<li>${r}</li>`).join("");
      const actionList = rec.action_plan.map((a) => `<li>${a}</li>`).join("");

      return `
        <div class="col-lg-6">
          <div class="card border-0 shadow-sm p-4 rounded-4 bg-white h-100">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div class="d-flex align-items-center gap-2">
                <span class="fs-2">${p.icon_emoji}</span>
                <div>
                  <h6 class="fw-bold mb-0 text-dark">${p.title}</h6>
                  <small class="text-muted">${p.duration} | ${p.category.toUpperCase()}</small>
                </div>
              </div>
              <div class="text-center p-2 rounded-3 bg-primary-subtle border border-primary-subtle" style="min-width: 60px;">
                <div class="fw-bold text-primary fs-5 lh-1">${rec.match_percentage}%</div>
                <small class="text-primary fw-semibold" style="font-size: 0.68rem;">MATCH</small>
              </div>
            </div>

            <p class="text-secondary small mb-3">${p.tagline}</p>

            <div class="bg-light p-3 rounded-3 mb-3">
              <h6 class="fw-bold text-dark small mb-1">🎯 Why This Fits You:</h6>
              <ul class="ps-3 mb-0 small text-secondary">
                ${reasonsList}
              </ul>
            </div>

            <div class="p-3 bg-success-subtle rounded-3 mb-3 border border-success-subtle">
              <h6 class="fw-bold text-success small mb-1">⚡ Recommended Action Plan:</h6>
              <ul class="ps-3 mb-0 small text-dark">
                ${actionList}
              </ul>
            </div>

            <div class="d-flex gap-2 mt-auto pt-2 border-top">
              <button class="btn btn-outline-primary btn-sm w-50 rounded-pill fw-semibold" onclick="openPathwayModal('${p.id}')">
                📖 View Guide
              </button>
              <button class="btn btn-outline-secondary btn-sm w-50 rounded-pill fw-semibold" onclick="quickJumpToColleges('${p.category}')">
                🏛️ Compare Colleges
              </button>
            </div>
          </div>
        </div>
      `;
    })
    .join("");

  section.scrollIntoView({ behavior: "smooth", block: "start" });
}

// -------------------------------------------------------------
// 6. ENTRANCE EXAMS CALENDAR & 1-CLICK SYNC
// -------------------------------------------------------------
function renderSchoolExams() {
  const container = document.getElementById("school-exams-list");
  if (!container) return;

  let filtered = allSchoolExams;
  if (activeExamStageFilter === "after_10th") {
    filtered = allSchoolExams.filter((e) => e.target_stage === "after_10th");
  } else if (activeExamStageFilter === "after_12th") {
    filtered = allSchoolExams.filter((e) => e.target_stage === "after_12th");
  }

  if (!filtered || filtered.length === 0) {
    container.innerHTML = `
      <div class="col-12 text-center py-5 bg-white rounded-4 border">
        <div class="fs-1 mb-2">📋</div>
        <h6 class="fw-bold text-dark">No admission schedules found for this stage.</h6>
        <p class="text-muted small mb-0">Switch to "All Schedules" or change the filter above.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = filtered
    .map(
      (e) => {
        const isMerit = e.admission_type && e.admission_type.includes("No Entrance Exam");
        const admissionBadge = isMerit
          ? `<span class="badge bg-success text-white small rounded-pill px-2.5 py-1">Direct Cutoff Merit</span>`
          : `<span class="badge bg-warning text-dark small rounded-pill px-2.5 py-1">Entrance Exam</span>`;
        const stageBadge = e.target_stage === "after_10th"
          ? `<span class="badge bg-info bg-opacity-25 text-info-emphasis fw-bold rounded-pill small px-2.5 py-1">📘 After 10th (SSLC)</span>`
          : `<span class="badge bg-primary bg-opacity-25 text-primary-emphasis fw-bold rounded-pill small px-2.5 py-1">🎓 After 12th (HSC)</span>`;

        const calBtn = e.google_calendar_url
          ? `<a href="${e.google_calendar_url}" target="_blank" rel="noopener noreferrer" class="btn btn-outline-danger btn-sm rounded-pill fw-bold d-flex align-items-center justify-content-center gap-2 shadow-sm">
              <span>📅</span> Sync to Google Calendar
            </a>`
          : `<div class="text-center small text-muted py-1 fw-semibold border rounded-pill bg-light">
              <span>🔔</span> Dates published officially post-Board results
            </div>`;

        const cleanDomain = e.official_url ? e.official_url.replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0] : "tn.gov.in";

        return `
      <div class="col-md-6 col-lg-4">
        <div class="card border-0 shadow-sm p-4 rounded-4 bg-white h-100 d-flex flex-column transition-all hover-shadow">
          <div class="d-flex justify-content-between align-items-start gap-2 mb-2">
            <div>
              <div class="mb-1">${stageBadge} ${admissionBadge}</div>
              <h6 class="fw-bold text-dark mb-0">${e.exam_name}</h6>
            </div>
          </div>

          <div class="small text-muted mb-2">
            <strong>🏛️ Conducting Body:</strong> <span class="text-secondary">${e.conducting_body}</span>
          </div>

          <div class="p-3 bg-light rounded-3 mb-2 small border">
            <div class="fw-semibold text-secondary mb-1.5">
              <strong class="text-dark">🎯 Target Courses:</strong> <span class="text-dark">${e.target_courses.join(", ")}</span>
            </div>
            <div class="fw-semibold text-danger mb-1.5">
              <strong>⏳ Application Window:</strong> <span>${e.registration_start} &rarr; ${e.registration_deadline}</span>
            </div>
            <div class="fw-semibold text-success mb-1.5">
              <strong>🗓️ Exam / Counselling Date:</strong> <span>${e.exam_date}</span>
            </div>
            <div class="text-muted">
              <strong>🎓 Eligibility:</strong> <span class="text-dark">${e.eligibility_summary}</span>
            </div>
          </div>

          <p class="small text-secondary mb-3 flex-grow-1">
            <strong>Key Process / Syllabus:</strong> ${e.syllabus_highlights}
          </p>

          <div class="d-flex flex-column gap-2 pt-2 border-top">
            ${calBtn}
            <a href="${e.official_url}" target="_blank" rel="noopener noreferrer" class="btn btn-outline-primary btn-sm rounded-pill fw-semibold text-center shadow-sm">
              🔗 Official TN Portal (${cleanDomain})
            </a>
          </div>
        </div>
      </div>
    `;
      }
    )
    .join("");
}

// -------------------------------------------------------------
// 7. CAREER POSITIONS & RELEVANT ENTRANCE EXAMS DIRECTORY
// -------------------------------------------------------------

function switchExamSectionView(view) {
  currentExamSectionView = view;
  const posContainer = document.getElementById("positions-view-container");
  const calContainer = document.getElementById("calendars-view-container");
  const posBtn = document.getElementById("view-mode-positions-btn");
  const calBtn = document.getElementById("view-mode-calendars-btn");

  if (view === "positions") {
    if (posContainer) posContainer.classList.remove("d-none");
    if (calContainer) calContainer.classList.add("d-none");
    if (posBtn) {
      posBtn.classList.remove("btn-light", "text-secondary");
      posBtn.classList.add("btn-primary", "fw-bold", "shadow-sm");
    }
    if (calBtn) {
      calBtn.classList.remove("btn-primary", "fw-bold", "shadow-sm");
      calBtn.classList.add("btn-light", "text-secondary");
    }
    renderCareerPositions();
  } else {
    if (posContainer) posContainer.classList.add("d-none");
    if (calContainer) calContainer.classList.remove("d-none");
    if (calBtn) {
      calBtn.classList.remove("btn-light", "text-secondary");
      calBtn.classList.add("btn-primary", "fw-bold", "shadow-sm");
    }
    if (posBtn) {
      posBtn.classList.remove("btn-primary", "fw-bold", "shadow-sm");
      posBtn.classList.add("btn-light", "text-secondary");
    }
    renderSchoolExams();
  }
}

function filterPositionsByStage(stage, btn) {
  activePosStageFilter = stage;
  document.querySelectorAll("#position-stage-pills button").forEach((b) => {
    b.classList.remove("btn-primary", "shadow-sm");
    b.classList.add("btn-outline-primary");
  });
  if (btn) {
    btn.classList.remove("btn-outline-primary");
    btn.classList.add("btn-primary", "shadow-sm");
  }
  renderCareerPositions();
}

function filterPositionsBySector(sector) {
  activePosSectorFilter = sector;
  renderCareerPositions();
}

function handlePositionSearch(query) {
  activePosSearchQuery = (query || "").toLowerCase().trim();
  renderCareerPositions();
}

function renderCareerPositions() {
  const container = document.getElementById("career-positions-list");
  if (!container) return;

  let filtered = allCareerPositions;

  // Filter by qualification stage
  if (activePosStageFilter === "after_10th") {
    filtered = filtered.filter(
      (p) => p.qualification_stage === "after_10th" || p.qualification_stage === "after_10th_12th"
    );
  } else if (activePosStageFilter === "after_12th") {
    filtered = filtered.filter(
      (p) => p.qualification_stage === "after_12th" || p.qualification_stage === "after_10th_12th"
    );
  } else if (activePosStageFilter === "diploma_graduate") {
    filtered = filtered.filter((p) => p.qualification_stage === "diploma_graduate");
  }

  // Filter by sector
  if (activePosSectorFilter && activePosSectorFilter !== "all") {
    filtered = filtered.filter(
      (p) => (p.sector || "").toLowerCase() === activePosSectorFilter.toLowerCase()
    );
  }

  // Filter by search query
  if (activePosSearchQuery) {
    const q = activePosSearchQuery;
    filtered = filtered.filter((p) => {
      const posText = `${p.position_title} ${p.sector} ${p.position_description} ${p.qualification_badge} ${(p.salary_range || "")}`.toLowerCase();
      const orgsText = (p.recruiting_organizations || []).join(" ").toLowerCase();
      const examsText = (p.relevant_entrance_exams || [])
        .map((e) => `${e.exam_name} ${e.conducting_body} ${e.exam_category}`)
        .join(" ")
        .toLowerCase();
      return posText.includes(q) || orgsText.includes(q) || examsText.includes(q);
    });
  }

  // Update counter badge
  const countBadge = document.getElementById("positions-count-badge");
  if (countBadge) {
    countBadge.innerHTML = `Showing <strong>${filtered.length}</strong> of <strong>${allCareerPositions.length}</strong> Career Positions &amp; Their Qualifying Entrance Exams`;
  }

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="col-12 text-center py-5 bg-white rounded-4 border">
        <div class="fs-1 mb-2">🔍</div>
        <h5 class="fw-bold text-dark">No Career Positions Match Your Current Filters</h5>
        <p class="text-secondary small mb-3">Try adjusting your search keyword or switching qualification stage / sector.</p>
        <button class="btn btn-sm btn-outline-primary rounded-pill px-4 fw-bold" onclick="resetPositionFilters()">
          🔄 Reset All Filters
        </button>
      </div>
    `;
    return;
  }

  container.innerHTML = filtered
    .map((pos) => {
      // Determine stage styling
      let stageBadgeClass = "bg-primary text-white";
      if (pos.qualification_stage === "after_10th") {
        stageBadgeClass = "bg-success text-white";
      } else if (pos.qualification_stage === "after_12th") {
        stageBadgeClass = "bg-info text-dark";
      } else if (pos.qualification_stage === "diploma_graduate") {
        stageBadgeClass = "bg-warning text-dark";
      }

      // Format exams preview
      const examsHtml = (pos.relevant_entrance_exams || [])
        .map((ex) => {
          const isMerit = ex.exam_category && ex.exam_category.toLowerCase().includes("cutoff");
          const badgeType = isMerit ? "bg-success" : "bg-primary";
          const cleanUrl = ex.official_portal
            ? ex.official_portal.replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]
            : "gov.in";

          return `
          <div class="p-2.5 rounded-3 bg-white border mb-2 shadow-xs">
            <div class="d-flex justify-content-between align-items-start gap-2 mb-1">
              <span class="fw-bold text-dark small">${ex.exam_name}</span>
              <span class="badge ${badgeType} small rounded-pill">${ex.exam_category.split("(")[0].trim()}</span>
            </div>
            <div class="small text-secondary mb-1">
              <strong>🏛️ Conducting Body:</strong> <span>${ex.conducting_body}</span>
            </div>
            <div class="small text-muted mb-1.5">
              <strong>⚡ Selection Process:</strong> <span>${ex.selection_stages}</span>
            </div>
            <div class="d-flex justify-content-between align-items-center pt-1 border-top small">
              <span class="text-danger fw-semibold">⏳ ${ex.registration_window || "Upcoming"}</span>
              <a href="${ex.official_portal}" target="_blank" rel="noopener noreferrer" class="text-primary text-decoration-none fw-bold small">
                🔗 ${cleanUrl} &rarr;
              </a>
            </div>
          </div>
        `;
        })
        .join("");

      // Recruiting org chips
      const orgChips = (pos.recruiting_organizations || [])
        .slice(0, 3)
        .map((org) => `<span class="badge bg-light text-secondary border small rounded-pill">${org}</span>`)
        .join(" ");

      return `
      <div class="col-lg-6">
        <div class="card border-0 shadow-sm p-4 rounded-4 bg-white h-100 d-flex flex-column transition-all hover-shadow">
          <!-- Header -->
          <div class="d-flex justify-content-between align-items-start gap-2 mb-2">
            <div>
              <div class="d-flex gap-1.5 flex-wrap mb-1.5">
                <span class="badge bg-primary bg-opacity-10 text-primary small rounded-pill fw-bold">${pos.sector}</span>
                <span class="badge ${stageBadgeClass} small rounded-pill fw-bold">${pos.qualification_badge}</span>
              </div>
              <h5 class="fw-bold text-dark mb-0">${pos.position_title}</h5>
            </div>
          </div>

          <div class="text-success small fw-bold mb-2">
            💰 Pay Scale / Salary: <span class="text-dark">${pos.salary_range}</span>
          </div>

          <p class="small text-secondary mb-3">
            ${pos.position_description}
          </p>

          <!-- Top Recruiters -->
          <div class="mb-3">
            <div class="small fw-bold text-muted mb-1">Top Recruiting Bodies &amp; Employers:</div>
            <div class="d-flex gap-1 flex-wrap">
              ${orgChips}
            </div>
          </div>

          <!-- Relevant Entrance Exams Box -->
          <div class="p-3 bg-light rounded-4 mb-3 border flex-grow-1">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <span class="small fw-bold text-dark text-uppercase tracking-wider">
                📝 Qualifying Entrance / Selection Exams (${(pos.relevant_entrance_exams || []).length})
              </span>
            </div>
            ${examsHtml}
          </div>

          <!-- Card Actions -->
          <div class="d-flex gap-2 pt-2 border-top mt-auto">
            <button class="btn btn-primary btn-sm rounded-pill fw-bold px-3 flex-grow-1 shadow-sm" onclick="openPositionExamModal('${pos.id}')">
              🔍 Full Exam Blueprint &amp; Syllabus &rarr;
            </button>
            <a href="${pos.relevant_entrance_exams && pos.relevant_entrance_exams[0] ? pos.relevant_entrance_exams[0].official_portal : '#'}" target="_blank" rel="noopener noreferrer" class="btn btn-outline-secondary btn-sm rounded-pill fw-semibold px-3 text-nowrap">
              🌐 Official Portal
            </a>
          </div>
        </div>
      </div>
    `;
    })
    .join("");
}

function resetPositionFilters() {
  activePosStageFilter = "all";
  activePosSectorFilter = "all";
  activePosSearchQuery = "";

  const searchInput = document.getElementById("position-search-input");
  if (searchInput) searchInput.value = "";

  const sectorSelect = document.getElementById("position-sector-select");
  if (sectorSelect) sectorSelect.value = "all";

  document.querySelectorAll("#position-stage-pills button").forEach((b) => {
    if (b.getAttribute("data-pos-stage") === "all") {
      b.classList.remove("btn-outline-primary");
      b.classList.add("btn-primary", "shadow-sm");
    } else {
      b.classList.remove("btn-primary", "shadow-sm");
      b.classList.add("btn-outline-primary");
    }
  });

  renderCareerPositions();
}

function openPositionExamModal(posId) {
  currentModalPositionId = posId;
  const pos = allCareerPositions.find((p) => p.id === posId);
  if (!pos) return;

  const sectorBadge = document.getElementById("pos-modal-sector-badge");
  const modalTitle = document.getElementById("pos-modal-title");
  const modalSubtitle = document.getElementById("pos-modal-subtitle");
  const modalBody = document.getElementById("pos-modal-body");
  const modalLinks = document.getElementById("pos-modal-portal-links");

  if (sectorBadge) {
    sectorBadge.innerHTML = `
      <span class="badge bg-primary bg-opacity-10 text-primary rounded-pill small fw-bold px-3 py-1">${pos.sector}</span>
      <span class="badge bg-success bg-opacity-15 text-success rounded-pill small fw-bold px-3 py-1 ms-1">${pos.qualification_badge}</span>
    `;
  }

  if (modalTitle) modalTitle.textContent = pos.position_title;
  if (modalSubtitle) modalSubtitle.textContent = `Pay Scale: ${pos.salary_range}`;

  // Build Exams Breakdown HTML
  const detailedExamsHtml = (pos.relevant_entrance_exams || [])
    .map(
      (ex, idx) => `
      <div class="card border p-3 rounded-4 mb-3 bg-white shadow-xs">
        <div class="d-flex justify-content-between align-items-start gap-2 mb-2">
          <div>
            <span class="badge bg-primary rounded-pill small me-1">Exam #${idx + 1}</span>
            <span class="badge bg-light text-secondary border rounded-pill small">${ex.exam_category}</span>
            <h6 class="fw-bold text-dark mt-1 mb-0">${ex.exam_name}</h6>
          </div>
          <a href="${ex.official_portal}" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-outline-primary rounded-pill px-3 fw-bold">
            Apply / Visit Portal &rarr;
          </a>
        </div>

        <div class="row g-2 mb-2 small">
          <div class="col-md-6">
            <span class="text-muted fw-bold">🏛️ Conducting Authority:</span>
            <div class="text-dark fw-semibold">${ex.conducting_body}</div>
          </div>
          <div class="col-md-6">
            <span class="text-muted fw-bold">⏳ Typical Registration Window:</span>
            <div class="text-danger fw-semibold">${ex.registration_window || "Upcoming"}</div>
          </div>
        </div>

        <div class="p-2.5 bg-light rounded-3 mb-2 small">
          <div class="mb-1.5">
            <strong>🎯 Detailed Selection Stages:</strong>
            <p class="text-secondary mb-0">${ex.selection_stages}</p>
          </div>
          <div class="mb-1.5">
            <strong>📋 Examination Pattern &amp; Marks:</strong>
            <p class="text-secondary mb-0">${ex.exam_pattern}</p>
          </div>
          <div>
            <strong>💡 Recommended Preparation &amp; Syllabus:</strong>
            <p class="text-success mb-0 fw-semibold">${ex.how_to_prepare}</p>
          </div>
        </div>
      </div>
    `
    )
    .join("");

  // Build Career Progression HTML
  const careerLadderHtml = (pos.future_career_growth || [])
    .map((step) => `<li class="mb-1 text-secondary">${step}</li>`)
    .join("");

  // Build Employers HTML
  const employersHtml = (pos.recruiting_organizations || [])
    .map((org) => `<span class="badge bg-secondary bg-opacity-10 text-dark border rounded-pill px-3 py-1.5 small">${org}</span>`)
    .join(" ");

  if (modalBody) {
    modalBody.innerHTML = `
      <!-- Role Summary -->
      <div class="p-3 bg-light rounded-4 border mb-4">
        <h6 class="fw-bold text-dark mb-1">💼 Role Overview &amp; Responsibilities</h6>
        <p class="text-secondary small mb-2">${pos.position_description}</p>
        <div class="small fw-semibold text-primary">
          <strong>Compensation / Perks:</strong> ${pos.salary_range}
        </div>
      </div>

      <!-- Government Schemes & Quotas -->
      <div class="alert alert-warning border-0 rounded-4 p-3 mb-4 d-flex align-items-start gap-3">
        <span class="fs-4">🏛️</span>
        <div class="small">
          <strong class="text-dark">Tamil Nadu Reservation, Schemes &amp; Benefits:</strong>
          <p class="mb-0 text-secondary mt-1">${pos.government_perks_quotas}</p>
        </div>
      </div>

      <!-- Relevant Entrance Examinations -->
      <div class="mb-4">
        <h6 class="fw-bold text-dark mb-3">📝 Qualifying Entrance Examinations &amp; Selection Blueprints (${(pos.relevant_entrance_exams || []).length})</h6>
        ${detailedExamsHtml}
      </div>

      <!-- Career Progression Ladder -->
      <div class="card border p-3 rounded-4 mb-4 bg-white">
        <h6 class="fw-bold text-dark mb-2">📈 Career Promotion &amp; Growth Ladder</h6>
        <ul class="small mb-0 ps-3">
          ${careerLadderHtml}
        </ul>
      </div>

      <!-- Employers / Recruiting Bodies -->
      <div>
        <h6 class="fw-bold text-dark mb-2">🏢 Top Recruiting Organizations &amp; Departments</h6>
        <div class="d-flex gap-1.5 flex-wrap">
          ${employersHtml}
        </div>
      </div>
    `;
  }

  // Set modal footer links
  if (modalLinks) {
    const portals = (pos.relevant_entrance_exams || []).map(
      (e) => `
      <a href="${e.official_portal}" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-sm rounded-pill fw-bold px-3">
        🔗 ${e.exam_name.split("(")[0].trim()} Portal
      </a>
    `
    );
    modalLinks.innerHTML = portals.join(" ");
  }

  const modalEl = document.getElementById("positionDetailModal");
  if (modalEl && typeof bootstrap !== "undefined") {
    const modalInstance = bootstrap.Modal.getOrCreateInstance(modalEl);
    modalInstance.show();
  }
}

// =========================================================================
// PART 2: CAMPUS PLACEMENT PREDICTOR ENGINE (COLLEGE)
// =========================================================================

async function initCollegePlacementHub() {
  try {
    await loadBenchmarkCompanies();
    await runPredictionEvaluation();
    await loadPlacementDrives();
    await loadMockTrajectory();
    await loadDocumentVault();
    if (allCompaniesList.length > 0) {
      loadCompanyReviews(allCompaniesList[0].id);
    }
  } catch (err) {
    console.error("College Hub initialization error:", err);
  }
}

function switchCollegeTab(tabId) {
  const buttons = document.querySelectorAll("[data-college-tab]");
  buttons.forEach((btn) => {
    if (btn.getAttribute("data-college-tab") === tabId) {
      btn.classList.add("active");
    } else {
      btn.classList.remove("active");
    }
  });

  const tabs = ["predictor", "comparator", "drives", "trajectory", "vault", "reviews"];
  tabs.forEach((t) => {
    const el = document.getElementById(`college-tab-${t}`);
    if (el) {
      if (t === tabId) {
        el.classList.remove("d-none");
      } else {
        el.classList.add("d-none");
      }
    }
  });

  window.scrollTo({ top: 120, behavior: "smooth" });
}

async function loadBenchmarkCompanies() {
  try {
    const res = await api.get("/placement-compass/companies");
    if (res && res.data) {
      allCompaniesList = res.data;
      populateCompanyDropdowns();
    }
  } catch (err) {
    console.warn("Could not fetch benchmark companies:", err);
  }
}

function populateCompanyDropdowns() {
  const c1 = document.getElementById("compare-select-1");
  const c2 = document.getElementById("compare-select-2");
  const c3 = document.getElementById("compare-select-3");
  const rSelect = document.getElementById("review-company-select");

  if (!c1 || !c2 || !c3) return;

  const optionsHtml = allCompaniesList
    .map((c) => `<option value="${c.id}">${c.logo_emoji} ${c.name} (${c.ctc_range})</option>`)
    .join("");

  c1.innerHTML = optionsHtml;
  c2.innerHTML = optionsHtml;
  c3.innerHTML = `<option value="">None (Compare 2)</option>` + optionsHtml;

  if (allCompaniesList.length >= 2) {
    c1.selectedIndex = 0;
    c2.selectedIndex = 1;
  }
  if (allCompaniesList.length >= 3) {
    c3.selectedIndex = 3;
  }
  if (rSelect) rSelect.innerHTML = optionsHtml;
}

async function runPredictionEvaluation() {
  const cgpa = parseFloat(document.getElementById("pred-cgpa")?.value || 8.4) || 8.4;
  const apt = parseFloat(document.getElementById("pred-aptitude")?.value || 82) || 82;
  const coding = document.getElementById("pred-coding")?.value || "intermediate";

  try {
    const res = await api.post("/placement-compass/predict", {
      cgpa: cgpa,
      aptitude_score: apt,
      coding_level: coding,
      branch: "Computer Science / IT",
      target_role: "Software Engineer",
    });

    if (res && res.data) {
      renderPredictionResults(res.data);
    }
  } catch (err) {
    console.error("Prediction evaluation failed:", err);
  }
}

function renderPredictionResults(data) {
  const guideEl = document.getElementById("prediction-guidance-text");
  if (guideEl && data.summary_guidance) guideEl.textContent = data.summary_guidance;

  const safeCountEl = document.getElementById("safe-tier-count");
  const targetCountEl = document.getElementById("target-tier-count");
  const dreamCountEl = document.getElementById("dream-tier-count");
  if (safeCountEl) safeCountEl.textContent = `(${data.safe_matches.length})`;
  if (targetCountEl) targetCountEl.textContent = `(${data.target_matches.length})`;
  if (dreamCountEl) dreamCountEl.textContent = `(${data.dream_matches.length})`;

  renderCompanyCards("safe-matches-list", data.safe_matches, "safe");
  renderCompanyCards("target-matches-list", data.target_matches, "target");
  renderCompanyCards("dream-matches-list", data.dream_matches, "dream");
}

function renderCompanyCards(containerId, list, tier) {
  const container = document.getElementById(containerId);
  if (!container) return;

  if (!list || list.length === 0) {
    container.innerHTML = `<div class="text-muted small p-3 text-center bg-white rounded-3 border">No matching companies for current cutoffs.</div>`;
    return;
  }

  container.innerHTML = list
    .map((c) => {
      const matchScore = c.match_percentage || 0;
      let circleBadge = matchScore >= 80 ? "bg-success" : matchScore >= 60 ? "bg-primary" : "bg-danger";

      const gapsHtml =
        c.skill_gaps && c.skill_gaps.length > 0
          ? `<div class="p-2 rounded bg-warning-subtle text-dark small mt-2">
               <div class="fw-bold text-danger small mb-1">⚠️ Cutoff / Skill Gap:</div>
               <ul class="mb-0 ps-3 small text-secondary">
                 ${c.skill_gaps.map((g) => `<li>${g}</li>`).join("")}
               </ul>
             </div>`
          : `<div class="p-2 rounded bg-success-subtle text-success small mt-2 fw-semibold d-flex align-items-center gap-1.5">
               <span>✅</span> All Minimum Cutoffs Met
             </div>`;

      return `
        <div class="card border-0 shadow-sm p-3 rounded-4 bg-white">
          <div class="d-flex justify-content-between align-items-start mb-2">
            <div class="d-flex align-items-center gap-2">
              <span class="fs-3">${c.logo_emoji}</span>
              <div>
                <h6 class="fw-bold mb-0 text-dark">${c.name}</h6>
                <small class="text-muted">${c.industry}</small>
              </div>
            </div>
            <span class="badge ${circleBadge} text-white fs-6 px-2.5 py-1 rounded-pill">${matchScore}%</span>
          </div>

          <div class="d-flex justify-content-between align-items-center my-2 py-1 px-2.5 bg-light rounded-3 small">
            <span class="text-muted fw-bold">OFFER CTC:</span>
            <span class="fw-bold text-dark">${c.ctc_range}</span>
          </div>

          <div class="small text-secondary mb-2">
            <div><strong>Cutoffs:</strong> CGPA &ge; ${c.min_cgpa.toFixed(1)} | Apt &ge; ${c.min_aptitude.toFixed(0)}%</div>
          </div>

          ${gapsHtml}

          <div class="d-flex gap-2 mt-auto pt-3 border-top">
            <button class="btn btn-sm btn-outline-primary w-50 rounded-pill fw-semibold" onclick="quickAddToCompare('${c.id}')">
              ⚖️ Compare
            </button>
            <button class="btn btn-sm btn-outline-secondary w-50 rounded-pill fw-semibold" onclick="quickReadReviews('${c.id}')">
              💬 Reviews
            </button>
          </div>
        </div>
      `;
    })
    .join("");
}

function quickAddToCompare(companyId) {
  const c1 = document.getElementById("compare-select-1");
  const c2 = document.getElementById("compare-select-2");
  if (c1 && c2 && c1.value !== companyId) {
    c2.value = companyId;
  }
  switchCollegeTab("comparator");
  runComparison();
}

function quickReadReviews(companyId) {
  const rSelect = document.getElementById("review-company-select");
  if (rSelect) rSelect.value = companyId;
  switchCollegeTab("reviews");
  loadCompanyReviews(companyId);
}

async function runComparison() {
  const c1 = document.getElementById("compare-select-1")?.value;
  const c2 = document.getElementById("compare-select-2")?.value;
  const c3 = document.getElementById("compare-select-3")?.value;

  const ids = [c1, c2, c3].filter((id) => id && id.trim().length > 0);
  const uniqueIds = Array.from(new Set(ids));

  if (uniqueIds.length < 2) {
    alert("Please select at least 2 distinct companies to compare.");
    return;
  }

  try {
    const res = await api.post("/placement-compass/compare", {
      company_ids: uniqueIds,
    });
    if (res && res.data && res.data.companies) {
      renderComparisonMatrix(res.data.companies);
    }
  } catch (err) {
    console.error("Comparison failed:", err);
  }
}

function presetComparison(type) {
  const c1 = document.getElementById("compare-select-1");
  const c2 = document.getElementById("compare-select-2");
  const c3 = document.getElementById("compare-select-3");

  if (type === "dream") {
    if (c1) c1.value = "google";
    if (c2) c2.value = "amazon";
    if (c3) c3.value = "microsoft";
  } else if (type === "target") {
    if (c1) c1.value = "zoho";
    if (c2) c2.value = "thoughtworks";
    if (c3) c3.value = "tcs";
  }
  runComparison();
}

function renderComparisonMatrix(companies) {
  const container = document.getElementById("comparison-matrix-container");
  if (!container) return;

  const colWidth = Math.floor(80 / companies.length);

  container.innerHTML = `
    <table class="table comparison-table align-middle mb-0">
      <thead>
        <tr>
          <th style="width: 20%;" class="bg-light text-secondary">CRITERIA</th>
          ${companies
            .map(
              (c) => `
            <th style="width: ${colWidth}%;" class="text-center">
              <div class="fs-1 mb-1">${c.logo_emoji}</div>
              <h5 class="fw-bold mb-0 text-dark">${c.name}</h5>
              <span class="badge bg-primary text-white rounded-pill px-2.5 py-1 small">${c.tier}</span>
            </th>
          `
            )
            .join("")}
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="fw-bold text-secondary">Total CTC Package</td>
          ${companies.map((c) => `<td class="text-center fw-bold text-success fs-5">${c.compensation.total_ctc}</td>`).join("")}
        </tr>
        <tr>
          <td class="fw-bold text-secondary">In-Hand Base Salary</td>
          ${companies.map((c) => `<td class="text-center fw-semibold text-dark">${c.compensation.base_salary}</td>`).join("")}
        </tr>
        <tr>
          <td class="fw-bold text-secondary">Work Policy</td>
          ${companies.map((c) => `<td class="text-center small">${c.work_policy}</td>`).join("")}
        </tr>
        <tr>
          <td class="fw-bold text-secondary">Culture &amp; Learning Rating</td>
          ${companies.map((c) => `<td class="text-center"><span class="fw-bold text-warning">★ ${c.culture_rating}</span> / 5.0</td>`).join("")}
        </tr>
        <tr>
          <td class="fw-bold text-secondary">Work-Life Balance</td>
          ${companies.map((c) => `<td class="text-center"><span class="fw-bold text-info">★ ${c.work_life_balance}</span> / 5.0</td>`).join("")}
        </tr>
      </tbody>
    </table>
  `;
}

// Drives, Mocks, Documents, Reviews
async function loadPlacementDrives() {
  try {
    const res = await api.get("/placement-compass/drives");
    if (res && res.data) {
      cachedDrives = res.data;
      renderDrives(cachedDrives);
    }
  } catch (err) {
    console.error("Drives load error:", err);
  }
}

function filterDrives(type, btn) {
  btn.parentElement.querySelectorAll("button").forEach((b) => b.classList.remove("active"));
  btn.classList.add("active");
  if (type === "all") renderDrives(cachedDrives);
  else renderDrives(cachedDrives.filter((d) => d.drive_type === type));
}

function renderDrives(drives) {
  const container = document.getElementById("placement-drives-list");
  if (!container) return;

  container.innerHTML = drives
    .map(
      (d) => `
      <div class="col-md-6 col-lg-4">
        <div class="card border-0 shadow-sm p-4 rounded-4 bg-white h-100 d-flex flex-column">
          <div class="d-flex justify-content-between align-items-start mb-2">
            <div class="d-flex align-items-center gap-2">
              <span class="fs-2">${d.logo_emoji}</span>
              <div>
                <h6 class="fw-bold mb-0 text-dark">${d.company_name}</h6>
                <small class="text-muted">${d.role_title}</small>
              </div>
            </div>
            <span class="badge bg-primary-subtle text-primary border rounded-pill small">${d.drive_type}</span>
          </div>

          <div class="mb-3">
            <div class="small fw-semibold text-secondary mb-1">
              <strong>🗓️ Date:</strong> <span>${d.event_date} (${d.event_time})</span>
            </div>
            <div class="small fw-semibold text-danger mb-1">
              <strong>⏳ Deadline:</strong> <span>${d.registration_deadline}</span>
            </div>
          </div>

          <p class="small text-secondary mb-3 flex-grow-1">${d.description}</p>

          <div class="d-flex flex-column gap-2 pt-2 border-top">
            <a href="${d.google_calendar_url}" target="_blank" rel="noopener noreferrer" class="btn btn-outline-danger btn-sm rounded-pill fw-bold">
              📅 Add to Google Calendar
            </a>
          </div>
        </div>
      </div>
    `
    )
    .join("");
}

async function loadMockTrajectory() {
  try {
    const res = await api.get("/placement-compass/mock-tests");
    if (res && res.data) {
      renderTrajectory(res.data);
    }
  } catch (err) {
    console.error("Trajectory load error:", err);
  }
}

function renderTrajectory(data) {
  const highestEl = document.getElementById("trajectory-highest-score");
  const readinessEl = document.getElementById("trajectory-readiness-label");
  const avgEl = document.getElementById("trajectory-avg-score");
  const latestEl = document.getElementById("trajectory-latest-score");
  const countEl = document.getElementById("trajectory-total-count");

  if (highestEl) highestEl.textContent = `${data.highest_score}%`;
  if (readinessEl) readinessEl.textContent = data.readiness_level;
  if (avgEl) avgEl.textContent = `${data.average_score}%`;
  if (latestEl) latestEl.textContent = `${data.latest_score}%`;
  if (countEl) countEl.textContent = `${data.total_attempts} tests`;

  const benchContainer = document.getElementById("cleared-benchmarks-list");
  if (benchContainer) {
    benchContainer.innerHTML = (data.company_benchmarks_cleared || [])
      .map((b) => `<span class="badge bg-success-subtle text-success border border-success-subtle px-2.5 py-1 rounded-pill">✅ ${b}</span>`)
      .join(" ");
  }

  const tbody = document.getElementById("mock-attempts-tbody");
  if (tbody) {
    tbody.innerHTML = (data.attempts || [])
      .map(
        (att) => `
        <tr>
          <td class="small text-muted">${att.date}</td>
          <td class="fw-semibold text-dark">${att.test_name}</td>
          <td class="small">${att.quantitative_score}%</td>
          <td class="small">${att.logical_score}%</td>
          <td class="small">${att.verbal_score}%</td>
          <td><span class="fw-bold text-success">${att.total_percentage}%</span></td>
          <td><span class="badge bg-light text-dark border small">Logged</span></td>
        </tr>
      `
      )
      .join("");
  }
}

async function handleMockSubmit(event) {
  event.preventDefault();
  const title = document.getElementById("mock-form-title")?.value;
  const quant = parseFloat(document.getElementById("mock-form-quant")?.value || 0);
  const logical = parseFloat(document.getElementById("mock-form-logical")?.value || 0);
  const verbal = parseFloat(document.getElementById("mock-form-verbal")?.value || 0);
  const total = Math.round((quant + logical + verbal) / 3);

  try {
    const res = await api.post("/placement-compass/mock-tests", {
      test_name: title,
      date: new Date().toISOString().split("T")[0],
      quantitative_score: quant,
      logical_score: logical,
      verbal_score: verbal,
      total_percentage: total,
    });

    if (res && res.data) {
      renderTrajectory(res.data);
      const modalEl = document.getElementById("logMockModal");
      const modalInstance = bootstrap.Modal.getInstance(modalEl);
      if (modalInstance) modalInstance.hide();
      alert("Mock test score added!");
    }
  } catch (err) {
    console.error("Mock test submit error:", err);
  }
}

async function loadDocumentVault() {
  try {
    const res = await api.get("/placement-compass/documents");
    if (res && res.data) renderDocumentVault(res.data);
  } catch (err) {
    console.error("Document vault load error:", err);
  }
}

function renderDocumentVault(data) {
  const pctEl = document.getElementById("vault-readiness-pct");
  const barEl = document.getElementById("vault-progress-bar");
  const pct = data.readiness_percentage || 0;
  if (pctEl) pctEl.textContent = `${pct}%`;
  if (barEl) barEl.style.width = `${pct}%`;

  const container = document.getElementById("document-checklist-items");
  if (!container) return;

  container.innerHTML = data.checklist
    .map(
      (doc) => `
      <div class="p-3 bg-light rounded-3 border d-flex justify-content-between align-items-center mb-2">
        <div class="d-flex align-items-center gap-3">
          <input class="form-check-input fs-5 mt-0" type="checkbox" ${doc.is_ready ? "checked" : ""} onclick="toggleDocItem('${doc.id}', this.checked)">
          <div>
            <div class="fw-bold ${doc.is_ready ? "text-success text-decoration-line-through" : "text-dark"}">${doc.title}</div>
            <small class="text-muted">${doc.description}</small>
          </div>
        </div>
        <span class="badge ${doc.is_ready ? "bg-success" : "bg-secondary"} text-white">${doc.is_ready ? "Ready" : "Pending"}</span>
      </div>
    `
    )
    .join("");
}

async function toggleDocItem(docId, nextState) {
  try {
    const res = await api.post("/placement-compass/documents/toggle", {
      doc_id: docId,
      is_ready: nextState,
    });
    if (res && res.data) renderDocumentVault(res.data);
  } catch (err) {
    console.error("Toggle document error:", err);
  }
}

async function loadCompanyReviews(companyId) {
  if (!companyId) return;
  try {
    const res = await api.get(`/placement-compass/reviews/${companyId}`);
    if (res && res.data) {
      renderCompanyReviews(res.data);
    }
  } catch (err) {
    console.error("Reviews load error:", err);
  }
}

function renderCompanyReviews(data) {
  const container = document.getElementById("dual-review-display");
  if (!container) return;

  const reddit = data.reddit_reviews || {};
  const glassdoor = data.glassdoor_reviews || {};

  container.innerHTML = `
    <div class="col-lg-6">
      <div class="card border-0 shadow-sm p-4 rounded-4 bg-white h-100">
        <h6 class="fw-bold mb-2">🤖 Reddit &amp; Blind Community Voice</h6>
        <p class="small text-secondary mb-3">${reddit.summary || "No recent posts."}</p>
        <div class="small fw-bold text-dark mb-1">Insider Tips:</div>
        <ul class="ps-3 small text-secondary">
          ${(reddit.insider_tips || []).map((t) => `<li>${t}</li>`).join("")}
        </ul>
      </div>
    </div>
    <div class="col-lg-6">
      <div class="card border-0 shadow-sm p-4 rounded-4 bg-white h-100">
        <h6 class="fw-bold mb-2">🏢 Glassdoor &amp; AmbitionBox Verified Metrics</h6>
        <p class="small text-secondary mb-3">${glassdoor.summary || "No verified reviews."}</p>
        <div class="small fw-bold text-success mb-1">Top Pros:</div>
        <ul class="ps-3 small text-secondary">
          ${(glassdoor.verified_pros || []).map((p) => `<li>${p}</li>`).join("")}
        </ul>
      </div>
    </div>
  `;
}
