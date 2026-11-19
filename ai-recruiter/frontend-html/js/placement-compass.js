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
let activeAcademicGroup = "all";
let activePosStageFilter = "all";
let activePosSectorFilter = "all";
let activePosSearchQuery = "";
let currentExamSectionView = "calendars";
let currentModalPathId = null;
let currentModalPositionId = null;

// College Placement state
let allCompaniesList = [];
let cachedDrives = [];

// Immediate Static Data Ingestion (ensures zero empty states)
if (typeof window !== "undefined" && window.COMPASS_STATIC_DATA) {
  const d = window.COMPASS_STATIC_DATA;
  if (d.paths) allSchoolPaths = [...d.paths];
  if (d.exams) allSchoolExams = [...d.exams];
  if (d.colleges) allCollegesList = [...d.colleges];
  if (d.courses) allComparableCourses = [...d.courses];
  if (d.positions) allCareerPositions = [...d.positions];
}

function hydrateFromStaticData() {
  if (typeof window !== "undefined" && window.COMPASS_STATIC_DATA) {
    const d = window.COMPASS_STATIC_DATA;
    if ((!allSchoolPaths || allSchoolPaths.length === 0) && d.paths) allSchoolPaths = [...d.paths];
    if ((!allSchoolExams || allSchoolExams.length === 0) && d.exams) allSchoolExams = [...d.exams];
    if ((!allCollegesList || allCollegesList.length === 0) && d.colleges) allCollegesList = [...d.colleges];
    if ((!allComparableCourses || allComparableCourses.length === 0) && d.courses) allComparableCourses = [...d.courses];
    if ((!allCareerPositions || allCareerPositions.length === 0) && d.positions) allCareerPositions = [...d.positions];

    try { renderSchoolPaths(); } catch (e) { console.warn(e); }
    try { populateCollegeDropdowns(); } catch (e) { console.warn(e); }
    try { renderCollegesCategoryGrid(); } catch (e) { console.warn(e); }
    try { presetCollegeCompare("engineering"); } catch (e) { console.warn(e); }
    try { populateCourseDropdowns(); } catch (e) { console.warn(e); }
    try { presetCourseCompare("cse_vs_ece_vs_poly"); } catch (e) { console.warn(e); }
    try { renderSchoolExams(); } catch (e) { console.warn(e); }
    try { renderCareerPositions(); } catch (e) { console.warn(e); }
    try { renderTwelfthGroupGuidance("computer_science"); } catch (e) { console.warn(e); }
    try { renderTenthGuidanceRoutes(); } catch (e) { console.warn(e); }
    try { updateCutoffCalculatorInputs(); } catch (e) { console.warn(e); }
  }
}

function showCompassToast(message, type = "info") {
  let toastEl = document.getElementById("compass-live-toast");
  if (!toastEl) {
    toastEl = document.createElement("div");
    toastEl.id = "compass-live-toast";
    toastEl.style.position = "fixed";
    toastEl.style.top = "80px";
    toastEl.style.right = "24px";
    toastEl.style.zIndex = "10050";
    toastEl.style.maxWidth = "480px";
    toastEl.style.transition = "all 0.3s ease-in-out";
    document.body.appendChild(toastEl);
  }

  const bgClass = type === "warning" ? "bg-warning text-dark" : type === "success" ? "bg-success text-white" : "bg-primary text-white";
  toastEl.innerHTML = `
    <div class="card border-0 shadow-lg ${bgClass} rounded-4 p-3 d-flex flex-row align-items-center gap-3 animate__animated animate__fadeInDown">
      <span class="fs-4">🧭</span>
      <div class="small fw-semibold flex-grow-1">${message}</div>
      <button type="button" class="btn-close ${type === 'warning' ? '' : 'btn-close-white'} ms-2" onclick="this.closest('#compass-live-toast').style.display='none'"></button>
    </div>
  `;
  toastEl.style.display = "block";
  toastEl.style.opacity = "1";

  if (window._toastTimeout) clearTimeout(window._toastTimeout);
  window._toastTimeout = setTimeout(() => {
    if (toastEl) {
      toastEl.style.opacity = "0";
      setTimeout(() => { toastEl.style.display = "none"; }, 300);
    }
  }, 4500);
}
window.showCompassToast = showCompassToast;

document.addEventListener("DOMContentLoaded", async () => {
  setupUserGreeting();

  // Load initial mode
  const savedMode = localStorage.getItem("compass_active_hub") || "school";
  setCompassMode(savedMode);

  // Synchronously hydrate from static pre-bundled data first
  hydrateFromStaticData();

  // Initialize both engines asynchronously
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
  // Always guarantee 12th-Grade Group Guidance and 10th-Standard Compass render
  try { renderTwelfthGroupGuidance("computer_science"); } catch (e) {}
  try { renderTenthGuidanceRoutes(); } catch (e) {}
  try { updateCutoffCalculatorInputs(); } catch (e) {}

  // 1. Fetch all school career paths
  try {
    const pathsRes = await api.get("/placement-compass/school/paths");
    if (pathsRes && pathsRes.data && pathsRes.data.length > 0) {
      allSchoolPaths = pathsRes.data;
      renderSchoolPaths();
    }
  } catch (err) {
    console.warn("Using bundled school paths data:", err);
  }

  // 2. Fetch Top Colleges directory
  try {
    const collegesRes = await api.get("/placement-compass/colleges");
    if (collegesRes && collegesRes.data && collegesRes.data.length > 0) {
      allCollegesList = collegesRes.data;
      populateCollegeDropdowns();
      renderCollegesCategoryGrid();
    }
  } catch (err) {
    console.warn("Using bundled colleges data:", err);
  }

  // 3. Fetch Comparable Courses
  try {
    const coursesRes = await api.get("/placement-compass/courses");
    if (coursesRes && coursesRes.data && coursesRes.data.length > 0) {
      allComparableCourses = coursesRes.data;
      populateCourseDropdowns();
    }
  } catch (err) {
    console.warn("Using bundled courses data:", err);
  }

  // 4. Fetch school entrance exams calendar
  try {
    const examsRes = await api.get("/placement-compass/school/exams");
    if (examsRes && examsRes.data && examsRes.data.length > 0) {
      allSchoolExams = examsRes.data;
      renderSchoolExams();
    }
  } catch (err) {
    console.warn("Using bundled school exams data:", err);
  }

  // 5. Fetch career positions and their relevant entrance examinations
  try {
    const posRes = await api.get("/placement-compass/positions");
    if (posRes && posRes.data && posRes.data.length > 0) {
      allCareerPositions = posRes.data;
      renderCareerPositions();
    }
  } catch (err) {
    console.warn("Using bundled career positions data:", err);
  }
}

// Subnav Tabs in School Mode
function switchSchoolTab(tabId) {
  const tabs = ["explorer", "twelfth_groups", "tenth_compass", "colleges", "courses", "matcher", "exams", "roadmap"];
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

  if (stage === "after_10th") {
    filterExamsByAcademicGroup("sslc_10th");
    switchSchoolTab("tenth_compass");
  } else if (stage === "after_12th") {
    if (activeAcademicGroup === "sslc_10th") {
      filterExamsByAcademicGroup("computer_science");
    }
    switchSchoolTab("twelfth_groups");
  } else if (stage === "all") {
    filterExamsByAcademicGroup("all");
    switchSchoolTab("explorer");
  } else {
    renderSchoolExams();
    renderCareerPositions();
  }
}

// =========================================================================
// 12th-GRADE GROUP-WISE COURSE & CAREER GUIDANCE KNOWLEDGE BASE
// =========================================================================
const TWELFTH_GROUP_GUIDANCE = {
  computer_science: {
    group_name: "Group 1: Computer Science & Mathematics Stream",
    subjects: "Physics, Chemistry, Mathematics & Computer Science",
    badge: "💻 Engineering, Technology & Mathematics",
    description: "Designed for analytical and problem-solving students aiming for premier engineering degrees, software architecture, robotics, semiconductor VLSI, architecture, and armed forces technical cadet schemes in Tamil Nadu.",
    cutoff_formula: "TNEA Engineering Cutoff = Maths (100) + [Physics (100) / 2] + [Chemistry (100) / 2] = Total out of 200",
    top_degree_courses: [
      {
        course: "B.E / B.Tech Computer Science & Engineering (CSE / AI & Data Science)",
        duration: "4 Years",
        cutoff: "190 - 199.5 for Premier Colleges (CEG, MIT, PSG Tech, GCT)",
        portal: "TNEA (Anna University) — tneaonline.org",
        overview: "The #1 high-demand engineering branch in Tamil Nadu. Focuses on algorithms, scalable cloud architecture, deep learning models, generative AI, and high-performance software development.",
        path_id: "btech_cse_ai"
      },
      {
        course: "B.E Electronics & Communication Engineering (ECE / VLSI Design)",
        duration: "4 Years",
        cutoff: "185 - 197.5 (Anna Univ CEG, SSN, CIT, Thiagarajar Madurai)",
        portal: "TNEA (Anna University) — tneaonline.org",
        overview: "Covers semiconductor microchips, FPGA architecture, 5G wireless networks, embedded systems, and automotive electronics in Tamil Nadu's hardware hubs.",
        path_id: "btech_ece_vlsi"
      },
      {
        course: "B.Sc Computer Science / Artificial Intelligence / Data Science",
        duration: "3 Years",
        cutoff: "85%+ aggregate in 12th PCM",
        portal: "TNGASA (tngasa.in) & Autonomous Portals (Loyola, MCC, PSG CAS)",
        overview: "Fast-track 3-year pure tech program leading into software development, data analytics, and cloud engineering with very low government-subsidized tuition.",
        path_id: "bsc_cs_datascience"
      },
      {
        course: "B.Arch — Bachelor of Architecture",
        duration: "5 Years",
        cutoff: "12th PCM 50% + NATA Qualifying Score",
        portal: "Anna University SAP Single Window Counseling",
        overview: "Council of Architecture (CoA) approved professional degree for urban infrastructure, green building designs, and smart city architecture.",
        path_id: "barch_architecture"
      },
      {
        course: "Indian Navy 10+2 B.Tech Cadet Scheme (Executive & Technical)",
        duration: "4 Years (100% Free Scholarship)",
        cutoff: "70% in PCM + JEE Main Rank",
        portal: "joinindiannavy.gov.in",
        overview: "100% free B.Tech at Indian Naval Academy (INA) Ezhimala + permanent commission as Sub Lieutenant in the Indian Navy.",
        path_id: "nda_armed_forces_12th"
      }
    ],
    career_opportunities: [
      {
        role: "Software Development Engineer (SDE) / Cloud Architect",
        starting_salary: "₹6.0 LPA - ₹24.0 LPA",
        top_hiring_zones: "Chennai OMR IT Corridor, Guindy Tech Parks, Coimbatore IT SEZ",
        progression: "Junior SDE → Senior Tech Lead → Principal Software Architect"
      },
      {
        role: "Machine Learning Engineer & Data Scientist",
        starting_salary: "₹7.5 LPA - ₹28.0 LPA",
        top_hiring_zones: "Fintech, Global In-house Centers (GICs), AI Labs in Chennai",
        progression: "Data Analyst → ML Model Engineer → Head of Data Science"
      },
      {
        role: "Semiconductor VLSI Design & Embedded Systems Engineer",
        starting_salary: "₹5.5 LPA - ₹18.0 LPA",
        top_hiring_zones: "Sriperumbudur Electronics SEZ, Hosur Tech Corridor",
        progression: "FPGA Designer → Senior VLSI Architect → Chip Design Lead"
      },
      {
        role: "Commissioned Technical Officer (Defence / Armed Forces)",
        starting_salary: "₹14.0 LPA (Level 10 Pay Matrix + Military Service Pay)",
        top_hiring_zones: "Indian Army, Indian Navy, Indian Air Force, DRDO Labs",
        progression: "Sub Lieutenant / Lieutenant → Commander / Colonel → Flag Officer"
      }
    ],
    tn_colleges: [
      "IIT Madras (NIRF #1 Engineering in India)",
      "CEG Campus, Anna University, Guindy (NIRF #13)",
      "NIT Tiruchirappalli (NIRF #9)",
      "MIT Campus, Anna University, Chromepet",
      "PSG College of Technology, Coimbatore",
      "Thiagarajar College of Engineering (TCE), Madurai",
      "Government College of Technology (GCT), Coimbatore",
      "SSN College of Engineering, Chennai"
    ],
    next_steps: [
      "Step 1: Calculate your TNEA Cutoff (out of 200) as soon as 12th Board marks are declared.",
      "Step 2: Register on tneaonline.org for Tamil Nadu Engineering Single Window Counseling.",
      "Step 3: Keep 7.5% Government School Study Certificate ready if studied in TN Govt schools from 6th to 12th (100% free tuition, hostel, and books).",
      "Step 4: Prepare choice list with top Anna University departments and autonomous colleges for Round 1/2 counseling."
    ]
  },

  biology: {
    group_name: "Group 2: Biology / Pure Science Stream",
    subjects: "Physics, Chemistry, Biology / Botany & Zoology (with or without Maths)",
    badge: "🧬 Medical, Healthcare, Veterinary & Agricultural Sciences",
    description: "Tailored for compassionate, research-minded students aiming to heal human lives, advance biomedical sciences, care for animals, or lead sustainable agricultural development in Tamil Nadu.",
    cutoff_formula: "MBBS/BDS: NEET-UG Score out of 720; Agri/Vet: Cutoff out of 200 = Biology (100) + [Physics (100)/2] + [Chemistry (100)/2]",
    top_degree_courses: [
      {
        course: "MBBS — Bachelor of Medicine & Bachelor of Surgery",
        duration: "5.5 Years (incl. 1 Yr Internship)",
        cutoff: "NEET-UG Score (Govt Medical Colleges: 580 - 660+ / 720; 7.5% Quota: 350 - 480+)",
        portal: "TN Medical Selection (tnmedicalselection.net) — 85% State Quota",
        overview: "The primary clinical medical degree for doctors, surgeons, and healthcare directors across 38+ Tamil Nadu Government Medical Colleges.",
        path_id: "mbbs_medicine"
      },
      {
        course: "BDS — Bachelor of Dental Surgery",
        duration: "5 Years",
        cutoff: "NEET-UG Score (Govt Dental College Chennai: 540 - 610 / 720)",
        portal: "TN Medical Selection (tnmedicalselection.net)",
        overview: "Specialized dental, maxillofacial and oral surgery healthcare degree with high private clinic practice and overseas licensing opportunities.",
        path_id: "bds_dental"
      },
      {
        course: "B.V.Sc & A.H — Bachelor of Veterinary Science & Animal Husbandry",
        duration: "5.5 Years",
        cutoff: "Cutoff out of 200: Typically 192 - 198 (TANUVAS Single Window)",
        portal: "TANUVAS Chennai — tanuvas.ac.in",
        overview: "Premier veterinary medicine degree in Madras Veterinary College and TANUVAS regional campuses. Direct recruitment for Veterinary Assistant Surgeon (VAS) via TNPSC.",
        path_id: "bvsc_veterinary"
      },
      {
        course: "B.Sc (Hons) Agriculture / Horticulture",
        duration: "4 Years",
        cutoff: "Cutoff out of 200: 188 - 198 (TNAU Coimbatore)",
        portal: "Tamil Nadu Agricultural University (TNAU) — tnau.ac.in",
        overview: "Agronomy, seed technology, horticulture, and sustainable soil science. Direct recruitment for Agricultural Officer (AO) via TNPSC.",
        path_id: "agriculture_icar_tnau"
      },
      {
        course: "B.Tech Biotechnology & Biomedical Engineering (Bio-Tech)",
        duration: "4 Years",
        cutoff: "180 - 196 / 200 (TNEA Anna University / AC Tech)",
        portal: "TNEA (Anna University) — tneaonline.org",
        overview: "Direct engineering degree for Biology students! Focuses on vaccine tech, biomedical devices, genetic engineering, and biopharma manufacturing.",
        path_id: "btech_biotech_biomedical"
      },
      {
        course: "B.Sc Nursing & Allied Health Sciences (BPT, BOT, B.Sc Radiology, B.Pharm)",
        duration: "4 Years",
        cutoff: "Direct 12th Biology + Physics + Chemistry Merit (No NEET required)",
        portal: "TN DME Selection Paramedical Counselling",
        overview: "High-growth clinical professions with immense global demand across UK, Middle East, USA, and top multi-specialty hospital chains in Tamil Nadu.",
        path_id: "allied_health_sciences_tn"
      }
    ],
    career_opportunities: [
      {
        role: "Medical Doctor / Surgeon / Specialist Physician",
        starting_salary: "₹8.0 LPA - ₹30.0 LPA",
        top_hiring_zones: "Government Hospitals, Apollo, MIOT, Fortis Malar, Private Clinics across TN",
        progression: "Junior Resident (CRRI) → Medical Officer → MD/MS Specialist Consultant"
      },
      {
        role: "Veterinary Assistant Surgeon (VAS) / Animal Healthcare Specialist",
        starting_salary: "₹6.5 LPA - ₹14.0 LPA",
        top_hiring_zones: "TN Animal Husbandry Department, Aavin Dairy, Veterinary Polyclinics",
        progression: "Veterinary Assistant Surgeon → Assistant Director → Joint Director of Animal Husbandry"
      },
      {
        role: "Agricultural Officer (AO) / Agronomist / Plant Breeder",
        starting_salary: "₹5.0 LPA - ₹12.5 LPA",
        top_hiring_zones: "TN Agriculture Dept, ICAR, Seed & Agri-biotech MNCs",
        progression: "Agricultural Officer → Assistant Director of Agriculture → District Joint Director"
      },
      {
        role: "Clinical Specialist / Head Nurse / Biomedical Scientist",
        starting_salary: "₹4.5 LPA - ₹16.0 LPA (Domestic) / ₹24 LPA+ (UK/Gulf/US)",
        top_hiring_zones: "Tertiary Hospitals in Chennai/Coimbatore & Global Healthcare Corridors",
        progression: "Staff Nurse/Technologist → Clinical Supervisor → Hospital Operations Director"
      }
    ],
    tn_colleges: [
      "Madras Medical College (MMC), Chennai (NIRF #11 in India)",
      "Stanley Medical College, Chennai",
      "Christian Medical College (CMC), Vellore (NIRF #3)",
      "Madras Veterinary College (TANUVAS), Vepery, Chennai",
      "Tamil Nadu Agricultural University (TNAU), Coimbatore",
      "Government Mohan Kumaramangalam Medical College, Salem",
      "PSG College of Nursing & Allied Health, Coimbatore"
    ],
    next_steps: [
      "Step 1: Appear for NEET-UG for MBBS/BDS, or calculate your 12th PCB Cutoff for Paramedical/TNAU/TANUVAS.",
      "Step 2: Register on tnmedicalselection.net immediately after NEET results for Tamil Nadu 85% State Quota.",
      "Step 3: Register on tnau.ac.in and tanuvas.ac.in for Agriculture & Veterinary single-window counseling.",
      "Step 4: Check eligibility for TN 7.5% Government School Reservation (100% free tuition, hostel, and food)."
    ]
  },

  
  pure_science: {
    group_name: "Group 3: Pure Science Stream (Botany & Zoology)",
    subjects: "Physics, Chemistry, Botany & Zoology (No Higher Mathematics)",
    badge: "🔬 Life Sciences, Medical, Agriculture, Veterinary & Pharmacy",
    description: "Dedicated for nature, life sciences, healthcare, botanical research, and agricultural enthusiasts who have studied Biology split into Botany & Zoology. Qualifies for all medical, dental, veterinary, agriculture, forestry, pharmacy, and paramedical admissions in Tamil Nadu.",
    cutoff_formula: "NEET UG for MBBS/BDS (Score out of 720); Paramedical/TNAU/TANUVAS Cutoff out of 200 = Biology (100) + [Physics (100)/2] + [Chemistry (100)/2]",
    top_degree_courses: [
      {
        course: "MBBS — Bachelor of Medicine & Surgery (TN DME 85% Quota)",
        duration: "5.5 Years",
        cutoff: "NEET-UG Score: 580 - 660+ / 720 (7.5% Govt School Quota: 350 - 480+)",
        portal: "TN Medical Selection — tnmedicalselection.net",
        overview: "Clinical medical doctor degree across 38+ Tamil Nadu Government Medical Colleges with 100% free education under 7.5% reservation.",
        path_id: "mbbs_medicine"
      },
      {
        course: "B.V.Sc & A.H — Veterinary Science & Animal Husbandry",
        duration: "5.5 Years",
        cutoff: "192 - 198 / 200 Cutoff (TANUVAS Single Window)",
        portal: "TANUVAS Chennai — tanuvas.ac.in",
        overview: "Madras Veterinary College and TANUVAS regional campuses. Direct recruitment for Veterinary Assistant Surgeon (VAS) via TNPSC.",
        path_id: "bvsc_veterinary"
      },
      {
        course: "B.Sc (Hons) Agriculture / Horticulture / Forestry",
        duration: "4 Years",
        cutoff: "188 - 198 / 200 Cutoff (TNAU Coimbatore)",
        portal: "Tamil Nadu Agricultural University — tnau.ac.in",
        overview: "Agronomy, seed tech, botanical genetics, and horticulture. Direct recruitment for Agricultural Officer (AO) via TNPSC.",
        path_id: "agriculture_icar_tnau"
      },
      {
        course: "B.Pharm — Bachelor of Pharmacy (TN DME Paramedical)",
        duration: "4 Years",
        cutoff: "12th PCB Cutoff Merit (No NEET required)",
        portal: "TN DME Selection — tnmedicalselection.net",
        overview: "Formulation chemistry, pharmacology, clinical trials, and drug manufacturing in Chennai's pharmaceutical manufacturing corridor.",
        path_id: "bpharm_pharmacy"
      },
      {
        course: "B.Sc Allied Health Sciences (Cardiac, Radiology, Dialysis)",
        duration: "4 Years (incl. 1 Yr Hospital Internship)",
        cutoff: "12th PCB Aggregate Cutoff (No NEET required)",
        portal: "TN DME Paramedical Single-Window Counselling",
        overview: "Direct patient care and high-tech diagnostics in cardiac cath labs, ICU suites, MRI/CT scanners, and dialysis units across corporate hospital chains.",
        path_id: "allied_health_sciences_tn"
      },
      {
        course: "B.Sc Nursing — 4-Year Professional Hospital Degree",
        duration: "4 Years",
        cutoff: "12th PCB Merit Selection via TN DME",
        portal: "TN DME Selection Committee",
        overview: "Clinical nursing, emergency trauma care, and surgical assistance with high worldwide demand in the UK, Middle East, and USA.",
        path_id: "bsc_nursing"
      }
    ],
    career_opportunities: [
      {
        role: "Medical Doctor / Surgeon / Specialist Physician",
        starting_salary: "₹8.0 LPA - ₹30.0 LPA",
        top_hiring_zones: "Government Hospitals, Apollo, MIOT, Fortis Malar, Private Clinics across TN",
        progression: "Junior Resident (CRRI) → Medical Officer → MD/MS Specialist Consultant"
      },
      {
        role: "Veterinary Assistant Surgeon (VAS) / Livestock Specialist",
        starting_salary: "₹6.5 LPA - ₹14.0 LPA",
        top_hiring_zones: "TN Animal Husbandry Department, Aavin Dairy, Regional Polyclinics",
        progression: "Veterinary Assistant Surgeon → Assistant Director → Joint Director"
      },
      {
        role: "Agricultural Officer (AO) / Agronomist / Plant Breeder",
        starting_salary: "₹5.0 LPA - ₹12.5 LPA",
        top_hiring_zones: "TN Agriculture Dept, ICAR, Seed & Agri-biotech MNCs",
        progression: "Agricultural Officer → Assistant Director of Agriculture → District Joint Director"
      },
      {
        role: "Clinical Specialist / Hospital Pharmacist / Healthcare Director",
        starting_salary: "₹4.5 LPA - ₹16.0 LPA",
        top_hiring_zones: "Tertiary Hospitals in Chennai/Coimbatore & Global Healthcare Corridors",
        progression: "Healthcare Technologist → Clinical Specialist → Department Head"
      }
    ],
    tn_colleges: [
      "Madras Medical College (MMC), Chennai (NIRF #11)",
      "Stanley Medical College, Chennai",
      "Madras Veterinary College (TANUVAS), Chennai",
      "Tamil Nadu Agricultural University (TNAU), Coimbatore",
      "Madras Medical College School of Pharmacy, Chennai",
      "Government Mohan Kumaramangalam Medical College, Salem"
    ],
    next_steps: [
      "Step 1: Appear for NEET-UG for MBBS/BDS, or calculate your 12th PCB Cutoff for Paramedical/TNAU/TANUVAS.",
      "Step 2: Register on tnmedicalselection.net immediately after NEET results for Tamil Nadu 85% State Quota.",
      "Step 3: Register on tnau.ac.in and tanuvas.ac.in for Agriculture & Veterinary single-window counseling.",
      "Step 4: Check eligibility for TN 7.5% Government School Reservation (100% free tuition, hostel, and food)."
    ]
  },

  commerce: {
    group_name: "Group 3: Commerce & Accountancy Stream",
    subjects: "Commerce, Accountancy, Economics & Business Mathematics / Computer Applications",
    badge: "📊 Banking, Chartered Accountancy, Corporate Law & Fintech",
    description: "Engineered for students with a keen sense for numbers, trade, investments, economic policies, and business management aiming for financial leadership in India and globally.",
    cutoff_formula: "TNGASA Commerce Cutoff = Aggregate of Commerce (100) + Accountancy (100) + Economics (100) + Business Maths/Computer Applications (100) = Total out of 400",
    top_degree_courses: [
      {
        course: "Chartered Accountancy (CA) — Foundation, Intermediate & Final",
        duration: "4 - 5 Years (Parallel with B.Com)",
        cutoff: "12th Standard Pass + Register with ICAI",
        portal: "Institute of Chartered Accountants of India (ICAI) — icai.org",
        overview: "The most prestigious financial qualification in India. Statutorily authorized to audit company balance sheets and advise on direct & indirect corporate taxation."
      },
      {
        course: "B.Com (General / Professional Accounting / Corporate Secretaryship / Honours)",
        duration: "3 Years",
        cutoff: "370 - 398 / 400 for Loyola, MCC, Ethiraj, Stella Maris, PSG CAS",
        portal: "TNGASA (tngasa.in) & Autonomous College Portals",
        overview: "Foundational business degree covering financial accounting, corporate law, income tax laws, and business analytics."
      },
      {
        course: "Cost & Management Accountancy (CMA) / Company Secretary (CS)",
        duration: "3 - 4 Years",
        cutoff: "12th Standard Pass + ICMAI / ICSI Registration",
        portal: "ICMAI (icmai.in) & ICSI (icsi.edu)",
        overview: "High-paying corporate finance roles focusing on manufacturing cost control, budgeting, corporate governance, and SEBI compliance."
      },
      {
        course: "5-Year Integrated B.Com. LL.B (Honours) — Corporate Law",
        duration: "5 Years",
        cutoff: "12th Marks (80%+) / CLAT Score",
        portal: "School of Excellence in Law (SOEL) TNDALU & TNNLU Trichy",
        overview: "Blends business acumen with corporate law, mergers & acquisitions, intellectual property, and National Company Law Tribunal (NCLT) litigation."
      },
      {
        course: "BBA (Bachelor of Business Administration) & Fintech Analytics",
        duration: "3 Years",
        cutoff: "12th Merit in Commerce / Maths",
        portal: "TNGASA & Autonomous Campuses",
        overview: "Focuses on operational management, marketing strategies, venture capital, and fintech operations."
      }
    ],
    career_opportunities: [
      {
        role: "Chartered Accountant (CA) / Chief Financial Officer (CFO)",
        starting_salary: "₹9.5 LPA - ₹30.0 LPA",
        top_hiring_zones: "Big 4 Accounting Firms (Deloitte, EY, PwC, KPMG), Banks, MNCs in Chennai",
        progression: "Audit Associate → Manager Financial Planning → Partner / CFO"
      },
      {
        role: "Investment Banker / Equity Research Analyst",
        starting_salary: "₹8.0 LPA - ₹25.0 LPA",
        top_hiring_zones: "Global Investment Banks (Standard Chartered, Citi, Barclays, World Bank Chennai)",
        progression: "Financial Analyst → Portfolio Manager → Director of Investment"
      },
      {
        role: "Corporate Lawyer / Company Secretary (CS)",
        starting_salary: "₹6.5 LPA - ₹18.0 LPA",
        top_hiring_zones: "Corporate Law Firms, Stock Exchanges, Conglomerates in TN",
        progression: "Legal Compliance Associate → Head of Legal & Secretarial → Corporate Legal General Counsel"
      },
      {
        role: "Commercial Tax Officer / Bank Probationary Officer (SBI/IBPS)",
        starting_salary: "₹6.0 LPA - ₹11.5 LPA",
        top_hiring_zones: "Public Sector Banks, RBI Chennai, TN Commercial Taxes Dept",
        progression: "Probationary Officer → Branch Chief Manager → General Manager"
      }
    ],
    tn_colleges: [
      "Loyola College, Chennai (NIRF #7 Overall / Arts & Commerce)",
      "Madras Christian College (MCC), Tambaram, Chennai",
      "PSG College of Arts and Science (PSG CAS), Coimbatore",
      "Ethiraj College for Women, Chennai",
      "Stella Maris College, Chennai",
      "Presidency College, Chennai (NIRF #3)",
      "School of Excellence in Law (SOEL), TNDALU, Chennai"
    ],
    next_steps: [
      "Step 1: Calculate your 12th 4-subject Commerce aggregate (out of 400).",
      "Step 2: Register on tngasa.in for Government Arts & Science single-window admission.",
      "Step 3: Register for ICAI CA Foundation exam before registration window closes.",
      "Step 4: Apply to autonomous premier colleges (Loyola, MCC, PSG CAS) within 5 days of 12th result publication."
    ]
  },

  arts: {
    group_name: "Group 4: Arts & Humanities Stream",
    subjects: "History, Political Science, Economics, Geography / English Literature / Advanced Tamil",
    badge: "📚 Law, Civil Services (IAS/IPS), Public Policy & Media",
    description: "Crafted for students passionate about societal governance, legal advocacy, journalism, international relations, design, and public administration.",
    cutoff_formula: "TNGASA Arts Cutoff = Aggregate of 4 core subjects out of 400; Law: 12th Percentage (TNDALU Merit)",
    top_degree_courses: [
      {
        course: "5-Year Integrated B.A. LL.B (Honours) — Constitutional & Criminal Law",
        duration: "5 Years",
        cutoff: "85%+ in 12th (TNDALU Single Window) / CLAT Rank for TNNLU",
        portal: "Tamil Nadu Dr. Ambedkar Law University (TNDALU) — tndalu.ac.in",
        overview: "The premier professional legal education pathway in Tamil Nadu leading to High Court and Supreme Court practice, judicial services, and public prosecutor roles."
      },
      {
        course: "B.A Public Administration / Political Science / Economics",
        duration: "3 Years",
        cutoff: "Direct 12th Merit (TNGASA)",
        portal: "TNGASA (tngasa.in) & University of Madras / Presidency College",
        overview: "The most strategically aligned undergraduate foundation for cracking the UPSC Civil Services (IAS / IPS / IFS) and TNPSC Group 1 (Deputy Collector / DSP)."
      },
      {
        course: "B.Des — Bachelor of Design (Fashion / Textile / Accessory Design)",
        duration: "4 Years",
        cutoff: "NIFT Entrance Exam Score",
        portal: "National Institute of Fashion Technology (NIFT Chennai) — nift.ac.in",
        overview: "Premier creative design degree with strong industrial placement in Chennai and Tirupur apparel & fashion manufacturing hubs."
      },
      {
        course: "B.Sc Visual Communication / Electronic Media & Journalism",
        duration: "3 Years",
        cutoff: "12th Merit + Creative Aptitude Test",
        portal: "Loyola College Chennai, Anna University Media Sciences, Madras Christian College",
        overview: "Digital cinema, film making, broadcast journalism, advertisement agency directing, and UX design."
      }
    ],
    career_opportunities: [
      {
        role: "Civil Servant (IAS / IPS / IFS / IRS) & State Deputy Collector",
        starting_salary: "₹12.0 LPA (Starting Basic Pay + DA + Govt House & Car)",
        top_hiring_zones: "Government of India, Government of Tamil Nadu Secretariat & District Collectorates",
        progression: "Assistant Collector (Training) → District Collector → Chief Secretary to Government"
      },
      {
        role: "Advocate / Civil & Criminal Lawyer / Corporate Legal Counsel",
        starting_salary: "₹5.5 LPA - ₹25.0 LPA",
        top_hiring_zones: "Madras High Court, Madurai Bench, District Courts, Corporate Law Chambers",
        progression: "Junior Advocate → Senior Counsel → High Court Judge / District Judge"
      },
      {
        role: "Creative Director / Fashion Stylist / Media Producer",
        starting_salary: "₹5.0 LPA - ₹18.0 LPA",
        top_hiring_zones: "South Indian Cinema Industry, Ad Agencies, Digital Streaming Platforms (OTT)",
        progression: "Assistant Director/Designer → Lead Creative Producer → Executive Media Director"
      },
      {
        role: "Economist / Policy Researcher / Think Tank Analyst",
        starting_salary: "₹6.0 LPA - ₹16.0 LPA",
        top_hiring_zones: "Madras School of Economics (MSE), World Bank, UN Agencies, State Planning Commission",
        progression: "Research Associate → Senior Policy Economist → Government Advisor"
      }
    ],
    tn_colleges: [
      "School of Excellence in Law (SOEL), TNDALU, Chennai",
      "Tamil Nadu National Law University (TNNLU), Tiruchirappalli",
      "Presidency College, Chennai (NIRF #3)",
      "Loyola College, Chennai (Visual Comm & Economics)",
      "Madras School of Economics (MSE), Chennai",
      "NIFT, Taramani, Chennai",
      "Government Law College (Madurai, Coimbatore, Tiruchirappalli, Tirunelveli)"
    ],
    next_steps: [
      "Step 1: Check your 12th Arts marks and register on tndalu.ac.in for Law admissions.",
      "Step 2: Register on tngasa.in for Government Arts & Science colleges single-window portal.",
      "Step 3: Begin foundational NCERT & TN State Board reading if targeting UPSC Civil Services / TNPSC Group 1.",
      "Step 4: Check 7.5% Tamil Nadu Government school quota eligibility for Law and Arts degrees."
    ]
  },

  vocational: {
    group_name: "Group 5: Vocational Higher Secondary Stream",
    subjects: "General Machinist, Electrical Machines, Automotive Technology, Agricultural Practices, Textile Technology",
    badge: "⚙️ Direct Technical Engineering & Lateral Admissions",
    description: "Specially structured for students who have studied vocational practical trades in 11th and 12th standard, providing special quota seats in engineering and direct lateral entry.",
    cutoff_formula: "TNEA Vocational Cutoff = Vocational Theory & Practicals scaled to 200",
    top_degree_courses: [
      {
        course: "B.E / B.Tech via TNEA Vocational Quota (Special 2% Reserved Seats)",
        duration: "4 Years",
        cutoff: "Vocational Cutoff out of 200 (170 - 195+ for Top Colleges)",
        portal: "TNEA (Anna University) — tneaonline.org",
        overview: "Exclusive 2% quota across all engineering colleges in Tamil Nadu reserved specifically for 12th Vocational HSC students."
      },
      {
        course: "Direct 2nd-Year Lateral Entry Polytechnic Diploma (DOTE TN)",
        duration: "2 Years (Direct into 3rd Semester)",
        cutoff: "12th Standard Vocational Pass",
        portal: "DOTE Tamil Nadu Centralized Admissions",
        overview: "Save 1 full year and earn a Government Polytechnic Diploma in just 2 years with hands-on shop-floor skills."
      },
      {
        course: "B.Voc — Bachelor of Vocation (Robotics, Mechatronics, Automotive)",
        duration: "3 Years",
        cutoff: "12th Vocational Pass",
        portal: "UGC approved autonomous colleges (PSG Tech B.Voc, Loyola B.Voc)",
        overview: "Dual-track work-integrated degree combining classroom theory with industrial apprenticeship in manufacturing hubs."
      }
    ],
    career_opportunities: [
      {
        role: "Production Engineer / Shop Floor QA Supervisor",
        starting_salary: "₹4.0 LPA - ₹9.0 LPA",
        top_hiring_zones: "Automotive Corridors in Sriperumbudur, Oragadam, Hosur, Coimbatore",
        progression: "Junior Trainee → Line Supervisor → Plant Operations Manager"
      },
      {
        role: "Automotive Automation & CNC Programmer",
        starting_salary: "₹4.2 LPA - ₹10.5 LPA",
        top_hiring_zones: "Hyundai, Renault-Nissan, Royal Enfield, TVS Motors, Ashok Leyland",
        progression: "CNC Specialist → Automation Lead → Tooling Design Engineer"
      }
    ],
    tn_colleges: [
      "PSG College of Technology (Vocational Quota & B.Voc), Coimbatore",
      "Government College of Technology (GCT), Coimbatore",
      "Alagappa Chettiar Government College of Engineering and Technology (ACCET), Karaikudi",
      "Central Polytechnic College (CPT), Chennai"
    ],
    next_steps: [
      "Step 1: Apply under the 'Vocational Stream' category in TNEA engineering registration.",
      "Step 2: Alternatively, apply for Direct 2nd-Year Polytechnic Lateral Entry on DOTE portal.",
      "Step 3: Collect your vocational practical mark certificates from your school."
    ]
  }
};

// =========================================================================
// 10th-STANDARD FUTURE PATH FINDER KNOWLEDGE BASE
// =========================================================================
const TENTH_GUIDANCE_DATA = {
  routes: [
    {
      id: "hsc_11th_12th",
      icon: "🎓",
      title: "Route 1: Higher Secondary (11th & 12th Standards)",
      duration: "2 Years",
      best_for: "Students aiming for University Degrees (B.Tech, MBBS, CA, Law, B.Com, B.Sc) after 2 years.",
      tamil_nadu_streams: [
        "Group 1 (Bio-Maths): Opens Engineering (TNEA), Medical (NEET), Agriculture (TNAU), Veterinary (TANUVAS).",
        "Group 2 (Computer Science-Maths): Opens Software, AI, Robotics, Architecture, Navy B.Tech Cadet.",
        "Group 3 (Commerce & Accountancy): Opens Chartered Accountancy (CA), B.Com, Corporate Finance, Banking.",
        "Group 4 (Arts & Humanities): Opens 5-Year Law (TNDALU), UPSC Civil Services (IAS/IPS), Journalism.",
        "Group 5 (Vocational HSC): Practical trade with 2% reserved engineering quota."
      ],
      admission_portal: "Direct admission in TN Government, Government-Aided, and Matriculation Higher Secondary Schools.",
      salary_potential: "Leads to Graduate Salaries: ₹4.5 LPA - ₹25+ LPA after degree completion.",
      path_id: "hsc_stream_selection_10th"
    },
    {
      id: "polytechnic_diploma",
      icon: "🔧",
      title: "Route 2: 3-Year Polytechnic Engineering Diploma",
      duration: "3 Years",
      best_for: "Students who love practical, hands-on engineering and want job readiness at age 18-19 OR want to join 2nd-Year B.E/B.Tech via Lateral Entry without 11th/12th.",
      tamil_nadu_streams: [
        "Diploma in Computer Engineering & Artificial Intelligence",
        "Diploma in Mechanical & Automation Engineering",
        "Diploma in Electrical & Electronics Engineering (EEE)",
        "Diploma in Electronics & Communication Engineering (ECE)",
        "Diploma in Civil Engineering"
      ],
      admission_portal: "Centralized DOTE Tamil Nadu Polytechnic Admission Portal.",
      salary_potential: "Junior Engineer: ₹2.8 LPA - ₹5.2 LPA. Plus 10% reserved seats for Direct 2nd-Year B.E/B.Tech Lateral Entry (TNEA Anna Univ)!",
      path_id: "diploma_mechanical_civil_eee"
    },
    {
      id: "iti_trades",
      icon: "🛠️",
      title: "Route 3: 1 to 2-Year ITI Technical Trades",
      duration: "1 to 2 Years",
      best_for: "Students wanting the fastest, lowest-cost route to certified technical employment with central/state public sector corporations.",
      tamil_nadu_streams: [
        "Electrician (2 Years) — High demand in TANGEDCO/TNEB & building infrastructure",
        "Fitter & Turner (2 Years) — Precision mechanical manufacturing in Chennai/Coimbatore",
        "Welder & Machinist (1 Year) — Automotive and fabrication industries",
        "Wireman & Electronics Mechanic"
      ],
      admission_portal: "Directorate of Employment & Training (DET TN) Online ITI Admission.",
      salary_potential: "Certified Technician: ₹2.2 LPA - ₹4.0 LPA + NCVT National Trade Certificate + Railway Apprentice eligibility.",
      path_id: "iti_vocational_trades_10th"
    },
    {
      id: "direct_govt_jobs",
      icon: "🎖️",
      title: "Route 4: Direct Tamil Nadu Government Jobs (10th Pass)",
      duration: "Immediate Recruitment",
      best_for: "Students seeking permanent Tamil Nadu state government employment with job security, pension benefits, and promotional avenues.",
      tamil_nadu_streams: [
        "TNPSC Group 4 & VAO: Village Administrative Officer, Junior Assistant, Typist, Steno-Typist, Bill Collector",
        "TNUSRB Grade II Police Constable, Jail Warden & Fireman",
        "Indian Army Soldier General Duty & Tradesman",
        "Indian Navy Matric Recruit (MR)"
      ],
      admission_portal: "TNPSC (tnpsc.gov.in) & TNUSRB (tnusrb.tn.gov.in) Official Notification Portals.",
      salary_potential: "Level 8 / Level 3 State Pay Scale: ₹22,000 - ₹35,000/month (₹3.0 LPA - ₹4.5 LPA) with lifelong government job security.",
      path_id: "direct_govt_jobs_10th"
    },
    {
      id: "paramedical_diploma",
      icon: "🩺",
      title: "Route 5: Paramedical & Healthcare Diplomas",
      duration: "2 Years",
      best_for: "Students passionate about healthcare and medical diagnostics without waiting for a 5-year MBBS degree.",
      tamil_nadu_streams: [
        "Diploma in Medical Laboratory Technology (DMLT)",
        "Diploma in Health Inspector / Sanitary Inspector",
        "Diploma in Dental Mechanic / Dental Hygienist",
        "Diploma in Radio Diagnosis (X-Ray & Imaging)"
      ],
      admission_portal: "TN Directorate of Medical Education (TN DME) Selection Committee.",
      salary_potential: "Healthcare Specialist: ₹2.5 LPA - ₹4.8 LPA in diagnostic labs, private hospitals, and Corporation health departments.",
      path_id: "paramedical_diploma_10th"
    },
    {
      id: "skill_based_technical",
      icon: "⚡",
      title: "Route 6: Skill-Based & Technical Training (TNSDC & Naan Mudhalvan)",
      duration: "3 to 12 Months",
      best_for: "Students seeking 100% free government technical training, monthly stipends under NAPS, and immediate jobs in electric vehicles, solar, CNC machining, and telecom.",
      tamil_nadu_streams: [
        "CNC Machine Operator & Precision Machinist (Guindy / Ambattur / Coimbatore)",
        "Electric Vehicle (EV) Assembly & Battery Service Technician",
        "Solar PV Installation & Maintenance Technician",
        "Industrial Automation & PLC Technician",
        "Telecom & Fiber Optic Cable Splicing Technician"
      ],
      admission_portal: "Tamil Nadu Skill Development Corporation (TNSDC) & Naan Mudhalvan Portal.",
      salary_potential: "Certified Specialist: ₹2.2 LPA - ₹4.5 LPA (₹15,000 - ₹35,000/month) + NAPS monthly stipend during training.",
      path_id: "skill_based_technical"
    }
  ]
};

// -------------------------------------------------------------
// DYNAMIC RENDERERS FOR 12th GROUPS AND 10th ROUTES
// -------------------------------------------------------------
function renderTwelfthGroupGuidance(groupKey) {
  const container = document.getElementById("twelfth-group-guidance-dossier");
  if (!container) return;

  const g = TWELFTH_GROUP_GUIDANCE[groupKey] || TWELFTH_GROUP_GUIDANCE["computer_science"];

  const coursesHtml = g.top_degree_courses.map((c) => `
    <div class="col-lg-6">
      <div class="card border-0 shadow-sm p-3.5 rounded-4 bg-white h-100 border-start border-3 border-primary d-flex flex-column">
        <div class="d-flex justify-content-between align-items-start gap-2 mb-2">
          <h6 class="fw-bold text-dark mb-0">${c.course}</h6>
          <span class="badge bg-primary-subtle text-primary border rounded-pill px-2.5 py-1 small fw-bold text-nowrap">${c.duration}</span>
        </div>
        <div class="mb-2">
          <span class="badge bg-danger-subtle text-danger border small me-1">Cutoff: ${c.cutoff}</span>
          <span class="badge bg-light text-secondary border small">Portal: ${c.portal}</span>
        </div>
        <p class="small text-secondary mb-3">${c.overview}</p>
        <div class="mt-auto pt-2 border-top">
          <button class="btn btn-primary btn-sm rounded-pill fw-bold w-100 shadow-sm" onclick="openPathwayModal('${c.path_id || 'btech_cse_ai'}')">
            📖 Explore Full Course Details, Careers &amp; Roadmap &rarr;
          </button>
        </div>
      </div>
    </div>
  `).join("");

  const careersHtml = g.career_opportunities.map((car) => `
    <div class="col-md-6">
      <div class="p-3 bg-light rounded-3 border h-100">
        <div class="d-flex justify-content-between align-items-center mb-1">
          <strong class="text-dark">${car.role}</strong>
          <span class="badge bg-success text-white fw-bold">${car.starting_salary}</span>
        </div>
        <div class="small text-muted mb-1">📍 <strong>Top Hiring Hubs:</strong> ${car.top_hiring_zones}</div>
        <div class="small text-primary">📈 <strong>Career Ladder:</strong> ${car.progression}</div>
      </div>
    </div>
  `).join("");

  const collegesBadges = g.tn_colleges.map((col) => `
    <span class="badge bg-white text-dark border p-2 rounded-3 shadow-xs small fw-semibold">🏛️ ${col}</span>
  `).join("");

  const nextStepsHtml = g.next_steps.map((st) => `
    <li class="mb-2 text-dark small fw-medium">${st}</li>
  `).join("");

  container.innerHTML = `
    <!-- Group Overview Banner -->
    <div class="card border-0 shadow-sm p-4 mb-4 rounded-4 bg-white">
      <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-2 mb-2">
        <h5 class="fw-bold text-dark mb-0">${g.group_name}</h5>
        <span class="badge bg-primary text-white rounded-pill px-3 py-1.5 fw-bold">${g.badge}</span>
      </div>
      <div class="text-muted small fw-semibold mb-2">Core 12th Subjects: ${g.subjects}</div>
      <p class="text-secondary small mb-3">${g.description}</p>
      <div class="alert alert-info py-2.5 px-3 rounded-3 mb-0 small border-0 bg-info bg-opacity-10 text-dark">
        <strong>🧮 Official Tamil Nadu Cutoff Formula:</strong> ${g.cutoff_formula}
      </div>
    </div>

    <!-- Section 1: Suitable Degree Courses -->
    <div class="card border-0 shadow-sm p-4 mb-4 rounded-4 bg-white">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <div>
          <h5 class="fw-bold mb-0 text-dark">🎓 Top Suitable Undergraduate Degrees &amp; Courses in Tamil Nadu</h5>
          <small class="text-muted">Courses designed specifically for your 12th-grade academic background.</small>
        </div>
      </div>
      <div class="row g-3">
        ${coursesHtml}
      </div>
    </div>

    <!-- Section 2: Future Career Opportunities & Salaries -->
    <div class="card border-0 shadow-sm p-4 mb-4 rounded-4 bg-white">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <div>
          <h5 class="fw-bold mb-0 text-dark">💼 Target Career Roles, Progression &amp; Salary Packages</h5>
          <small class="text-muted">Expected starting salaries and career growth corridors across Tamil Nadu and globally.</small>
        </div>
      </div>
      <div class="row g-3">
        ${careersHtml}
      </div>
    </div>

    <!-- Section 3: Premier Tamil Nadu Colleges -->
    <div class="card border-0 shadow-sm p-4 mb-4 rounded-4 bg-white">
      <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-2 mb-3">
        <div>
          <h5 class="fw-bold mb-0 text-dark">🏛️ Premier Tamil Nadu Colleges &amp; Universities for this Group</h5>
          <small class="text-muted">Government, Government-Aided, and NIRF-ranked institutions.</small>
        </div>
        <button class="btn btn-outline-primary btn-sm rounded-pill fw-bold" onclick="switchSchoolTab('colleges')">
          🏛️ Launch College Comparator
        </button>
      </div>
      <div class="d-flex flex-wrap gap-2">
        ${collegesBadges}
      </div>
    </div>

    <!-- Section 4: Next Steps & Action Plan -->
    <div class="card border-0 shadow-sm p-4 mb-4 rounded-4 bg-white border-start border-4 border-warning">
      <h5 class="fw-bold mb-2 text-dark">🚀 Step-by-Step Next Steps &amp; Action Plan for Students</h5>
      <p class="text-secondary small mb-3">Follow this checklist to ensure smooth admission into Tamil Nadu's top institutions without missing deadlines:</p>
      <ul class="ps-3 mb-3">
        ${nextStepsHtml}
      </ul>
      <div class="d-flex gap-2 flex-wrap">
        <button class="btn btn-primary btn-sm rounded-pill fw-bold px-3.5 shadow-sm" onclick="scrollToCutoffCalculator()">
          🧮 Check My Cutoff &amp; Eligibility
        </button>
        <button class="btn btn-outline-success btn-sm rounded-pill fw-bold px-3.5" onclick="switchSchoolTab('exams')">
          🎯 View Official Exam Dates &amp; Portals
        </button>
        <button class="btn btn-outline-secondary btn-sm rounded-pill fw-bold px-3.5" onclick="switchSchoolTab('roadmap')">
          🗺️ View Admission &amp; Counseling Roadmap
        </button>
      </div>
    </div>
  `;
}

function selectTwelfthGuidanceGroup(groupKey, btn) {
  document.querySelectorAll("#twelfth-group-buttons-container .academic-group-btn").forEach((b) => {
    if (b.getAttribute("data-twelfth-group") === groupKey) {
      b.classList.add("active");
    } else {
      b.classList.remove("active");
    }
  });
  renderTwelfthGroupGuidance(groupKey);
}
window.selectTwelfthGuidanceGroup = selectTwelfthGuidanceGroup;

function renderTenthGuidanceRoutes() {
  const container = document.getElementById("tenth-routes-cards-grid");
  if (!container) return;

  container.innerHTML = TENTH_GUIDANCE_DATA.routes.map((r) => `
    <div class="col-lg-6">
      <div class="card border-0 shadow-sm p-4 rounded-4 bg-white h-100 border-start border-4 border-primary d-flex flex-column">
        <div class="d-flex justify-content-between align-items-start gap-2 mb-2">
          <div class="d-flex align-items-center gap-2">
            <span class="fs-2">${r.icon}</span>
            <div>
              <h6 class="fw-bold text-dark mb-0">${r.title}</h6>
              <small class="badge bg-light text-primary border rounded-pill px-2.5 py-0.5 fw-bold">${r.duration}</small>
            </div>
          </div>
        </div>
        <p class="text-secondary small mb-2"><strong>🎯 Best For:</strong> ${r.best_for}</p>
        
        <div class="bg-light p-2.5 rounded-3 mb-2 small">
          <div class="fw-bold text-dark mb-1">Key Branches &amp; Streams in Tamil Nadu:</div>
          <ul class="ps-3 mb-0 text-secondary" style="font-size: 0.82rem;">
            ${r.tamil_nadu_streams.map((s) => `<li>${s}</li>`).join("")}
          </ul>
        </div>

        <div class="mb-2 small text-muted">
          <strong>🏛️ Official Admission:</strong> <span class="text-secondary">${r.admission_portal}</span>
        </div>

        <div class="p-2 bg-success-subtle rounded-3 border border-success-subtle small mb-3">
          <strong class="text-success">💰 Salary &amp; Future Scope:</strong> <span class="text-dark">${r.salary_potential}</span>
        </div>

        <div class="mt-auto pt-2 border-top d-flex gap-2">
          <button class="btn btn-primary btn-sm rounded-pill fw-bold w-100 shadow-sm" onclick="openPathwayModal('${r.path_id || 'hsc_stream_selection_10th'}')">
            📖 View Complete 10th Pathway Deep Dive &rarr;
          </button>
          <button class="btn btn-outline-secondary btn-sm rounded-pill fw-semibold text-nowrap" onclick="quickFilterExplorerTo10th()">
            Filter Explorer
          </button>
        </div>
      </div>
    </div>
  `).join("");
}

function scrollToCutoffCalculator() {
  switchSchoolTab("twelfth_groups");
  setTimeout(() => {
    document.getElementById("tn-cutoff-calculator-card")?.scrollIntoView({ behavior: "smooth", block: "start" });
  }, 100);
}
window.scrollToCutoffCalculator = scrollToCutoffCalculator;

function quickFilterExplorerTo10th() {
  switchSchoolTab("explorer");
  filterPathsByGrade("after_10th", null);
  document.getElementById("school-tab-explorer")?.scrollIntoView({ behavior: "smooth", block: "start" });
}
window.quickFilterExplorerTo10th = quickFilterExplorerTo10th;

// -------------------------------------------------------------
// TAMIL NADU 12th CUTOFF CALCULATOR
// -------------------------------------------------------------
function updateCutoffCalculatorInputs() {
  const stream = document.getElementById("cutoff-stream-select")?.value || "engineering";
  const inputsRow = document.getElementById("cutoff-marks-inputs-row");
  if (!inputsRow) return;

  if (stream === "engineering") {
    inputsRow.innerHTML = `
      <div class="row g-2 align-items-end">
        <div class="col-md-3">
          <label class="form-label small fw-bold text-secondary mb-1">Maths (/100)</label>
          <input type="number" id="cutoff-maths" class="form-control form-control-sm fw-bold" min="0" max="100" value="95">
        </div>
        <div class="col-md-3">
          <label class="form-label small fw-bold text-secondary mb-1">Physics (/100)</label>
          <input type="number" id="cutoff-physics" class="form-control form-control-sm fw-bold" min="0" max="100" value="90">
        </div>
        <div class="col-md-3">
          <label class="form-label small fw-bold text-secondary mb-1">Chemistry (/100)</label>
          <input type="number" id="cutoff-chemistry" class="form-control form-control-sm fw-bold" min="0" max="100" value="92">
        </div>
        <div class="col-md-3">
          <button class="btn btn-success btn-sm w-100 fw-bold rounded-pill shadow-sm" onclick="calculateTamilNaduCutoff()">
            🧮 Calculate Cutoff
          </button>
        </div>
      </div>
    `;
  } else if (stream === "agriculture_veterinary") {
    inputsRow.innerHTML = `
      <div class="row g-2 align-items-end">
        <div class="col-md-3">
          <label class="form-label small fw-bold text-secondary mb-1">Biology (/100)</label>
          <input type="number" id="cutoff-biology" class="form-control form-control-sm fw-bold" min="0" max="100" value="96">
        </div>
        <div class="col-md-3">
          <label class="form-label small fw-bold text-secondary mb-1">Physics (/100)</label>
          <input type="number" id="cutoff-physics" class="form-control form-control-sm fw-bold" min="0" max="100" value="88">
        </div>
        <div class="col-md-3">
          <label class="form-label small fw-bold text-secondary mb-1">Chemistry (/100)</label>
          <input type="number" id="cutoff-chemistry" class="form-control form-control-sm fw-bold" min="0" max="100" value="90">
        </div>
        <div class="col-md-3">
          <button class="btn btn-success btn-sm w-100 fw-bold rounded-pill shadow-sm" onclick="calculateTamilNaduCutoff()">
            🧮 Calculate Cutoff
          </button>
        </div>
      </div>
    `;
  } else if (stream === "commerce_arts") {
    inputsRow.innerHTML = `
      <div class="row g-2 align-items-end">
        <div class="col-md-2">
          <label class="form-label small fw-bold text-secondary mb-1">Commerce (/100)</label>
          <input type="number" id="cutoff-sub1" class="form-control form-control-sm fw-bold" min="0" max="100" value="95">
        </div>
        <div class="col-md-2">
          <label class="form-label small fw-bold text-secondary mb-1">Accountancy (/100)</label>
          <input type="number" id="cutoff-sub2" class="form-control form-control-sm fw-bold" min="0" max="100" value="94">
        </div>
        <div class="col-md-2">
          <label class="form-label small fw-bold text-secondary mb-1">Economics (/100)</label>
          <input type="number" id="cutoff-sub3" class="form-control form-control-sm fw-bold" min="0" max="100" value="90">
        </div>
        <div class="col-md-3">
          <label class="form-label small fw-bold text-secondary mb-1">Maths / Comp (/100)</label>
          <input type="number" id="cutoff-sub4" class="form-control form-control-sm fw-bold" min="0" max="100" value="92">
        </div>
        <div class="col-md-3">
          <button class="btn btn-success btn-sm w-100 fw-bold rounded-pill shadow-sm" onclick="calculateTamilNaduCutoff()">
            🧮 Calculate Cutoff
          </button>
        </div>
      </div>
    `;
  }
}
window.updateCutoffCalculatorInputs = updateCutoffCalculatorInputs;

function calculateTamilNaduCutoff() {
  const stream = document.getElementById("cutoff-stream-select")?.value || "engineering";
  const resultBox = document.getElementById("cutoff-result-container");
  if (!resultBox) return;

  resultBox.classList.remove("d-none");

  if (stream === "engineering") {
    const m = parseFloat(document.getElementById("cutoff-maths")?.value || 0);
    const p = parseFloat(document.getElementById("cutoff-physics")?.value || 0);
    const c = parseFloat(document.getElementById("cutoff-chemistry")?.value || 0);
    const cutoff = (m + (p / 2) + (c / 2)).toFixed(2);

    let tierMsg = "";
    if (cutoff >= 195) {
      tierMsg = "🌟 Top 1% in Tamil Nadu! High probability for Anna University CEG Campus, MIT Chromepet, and PSG Tech CSE/ECE.";
    } else if (cutoff >= 185) {
      tierMsg = "🚀 Tier-1 Engineering Admission! Eligible for GCT Coimbatore, CIT, SSN, Thiagarajar Madurai, and Core Tech branches.";
    } else if (cutoff >= 165) {
      tierMsg = "✅ Excellent Regional Autonomous Colleges! Eligible for top engineering colleges across Chennai, Coimbatore & Madurai zones.";
    } else {
      tierMsg = "📘 Qualified for TNEA Single Window Counseling across 440+ affiliated engineering colleges in Tamil Nadu.";
    }

    resultBox.innerHTML = `
      <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-2 mb-2">
        <div>
          <span class="badge bg-primary text-white px-3 py-1.5 rounded-pill fw-bold">TNEA Engineering Cutoff</span>
          <h4 class="fw-bold text-dark mb-0 mt-1">${cutoff} / 200</h4>
        </div>
        <div class="text-md-end">
          <div class="small text-muted">Formula: Maths (${m}) + Physics/2 (${(p/2).toFixed(1)}) + Chem/2 (${(c/2).toFixed(1)})</div>
        </div>
      </div>
      <p class="small text-dark mb-2 fw-medium">${tierMsg}</p>
      <div class="d-flex gap-2 flex-wrap">
        <button class="btn btn-outline-primary btn-sm rounded-pill fw-bold" onclick="switchSchoolTab('colleges')">Compare CEG vs MIT vs PSG</button>
        <button class="btn btn-outline-success btn-sm rounded-pill fw-bold" onclick="switchSchoolTab('roadmap')">Check TNEA Counseling Schedule</button>
      </div>
    `;
  } else if (stream === "agriculture_veterinary") {
    const b = parseFloat(document.getElementById("cutoff-biology")?.value || 0);
    const p = parseFloat(document.getElementById("cutoff-physics")?.value || 0);
    const c = parseFloat(document.getElementById("cutoff-chemistry")?.value || 0);
    const cutoff = (b + (p / 2) + (c / 2)).toFixed(2);

    let msg = "";
    if (cutoff >= 193) {
      msg = "🌟 Top TNAU & TANUVAS Category! Eligible for B.Sc (Hons) Agriculture Coimbatore and B.V.Sc & A.H Madras Veterinary College.";
    } else if (cutoff >= 180) {
      msg = "🌾 Strong admission chances across TNAU constituent colleges (Madurai, Killikulam, Eachangkottai) and TANUVAS regional campuses.";
    } else {
      msg = "📘 Eligible for Private Affiliated Agriculture Colleges and Allied Health Diplomas.";
    }

    resultBox.innerHTML = `
      <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-2 mb-2">
        <div>
          <span class="badge bg-success text-white px-3 py-1.5 rounded-pill fw-bold">TNAU / TANUVAS Cutoff</span>
          <h4 class="fw-bold text-dark mb-0 mt-1">${cutoff} / 200</h4>
        </div>
        <div class="text-md-end">
          <div class="small text-muted">Formula: Biology (${b}) + Physics/2 (${(p/2).toFixed(1)}) + Chem/2 (${(c/2).toFixed(1)})</div>
        </div>
      </div>
      <p class="small text-dark mb-2 fw-medium">${msg}</p>
      <button class="btn btn-outline-success btn-sm rounded-pill fw-bold" onclick="switchSchoolTab('exams')">View TNAU / TANUVAS Admission Portals</button>
    `;
  } else if (stream === "commerce_arts") {
    const s1 = parseFloat(document.getElementById("cutoff-sub1")?.value || 0);
    const s2 = parseFloat(document.getElementById("cutoff-sub2")?.value || 0);
    const s3 = parseFloat(document.getElementById("cutoff-sub3")?.value || 0);
    const s4 = parseFloat(document.getElementById("cutoff-sub4")?.value || 0);
    const total = (s1 + s2 + s3 + s4).toFixed(0);
    const pct = ((total / 400) * 100).toFixed(1);

    resultBox.innerHTML = `
      <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-2 mb-2">
        <div>
          <span class="badge bg-info text-dark px-3 py-1.5 rounded-pill fw-bold">TNGASA Arts &amp; Commerce Aggregate</span>
          <h4 class="fw-bold text-dark mb-0 mt-1">${total} / 400 (${pct}%)</h4>
        </div>
        <div class="text-md-end">
          <div class="small text-muted">Direct sum of 4 core subjects</div>
        </div>
      </div>
      <p class="small text-dark mb-2 fw-medium">
        ${total >= 380 ? '🌟 Outstanding Score! Eligible for Day 1 Merit B.Com / B.A admissions at Loyola College, Madras Christian College, Presidency, and PSG CAS.' : '✅ Eligible for Government and Aided Arts & Science Colleges across Tamil Nadu via tngasa.in.'}
      </p>
      <button class="btn btn-outline-primary btn-sm rounded-pill fw-bold" onclick="switchSchoolTab('colleges')">Compare Premier Arts &amp; Commerce Colleges</button>
    `;
  }
}
window.calculateTamilNaduCutoff = calculateTamilNaduCutoff;

function filterExamsByStage(stage, btn) {
  activeExamStageFilter = stage;
  document.querySelectorAll("#exam-stage-filter-btns button").forEach((b) => {
    b.classList.remove("btn-primary", "shadow-sm");
    b.classList.add("btn-outline-primary");
  });
  if (btn) {
    btn.classList.remove("btn-outline-primary");
    btn.classList.add("btn-primary", "shadow-sm");
  } else {
    document.querySelectorAll("#exam-stage-filter-btns button").forEach((b) => {
      if (b.getAttribute("data-exam-stage") === stage) {
        b.classList.remove("btn-outline-primary");
        b.classList.add("btn-primary", "shadow-sm");
      }
    });
  }

  // Smart Sync with Academic Group:
  if (stage === "after_10th" && activeAcademicGroup !== "sslc_10th") {
    activeAcademicGroup = "sslc_10th";
  } else if (stage === "after_12th" && activeAcademicGroup === "sslc_10th") {
    activeAcademicGroup = "all";
  }

  // Update group selector buttons
  document.querySelectorAll("#exam-academic-group-selector .academic-group-btn").forEach((b) => {
    if (b.getAttribute("data-group") === activeAcademicGroup) {
      b.classList.add("active");
    } else {
      b.classList.remove("active");
    }
  });

  renderSchoolExams();
  renderCareerPositions();
}

function filterPathsByGrade(grade, btn) {
  activeGradeFilter = grade;
  document.querySelectorAll("[data-filter-type='grade']").forEach((b) => b.classList.remove("active"));
  if (btn) btn.classList.add("active");

  // Check if current activeCatFilter has any paths under this newly selected grade
  if (activeCatFilter !== "all") {
    const hasCatMatch = allSchoolPaths.some((p) => {
      const matchCat = (p.category === activeCatFilter);
      let matchGrade = false;
      if (grade === "all") matchGrade = true;
      else if (grade === "after_10th") matchGrade = (p.grade_level === "after_10th" || p.grade_level === "after_10th_or_12th" || (p.eligible_grades && p.eligible_grades.includes("after_10th")));
      else if (grade === "after_12th") matchGrade = (p.grade_level.startsWith("after_12th") || p.grade_level === "after_10th_or_12th" || (p.eligible_grades && p.eligible_grades.some((g) => g.startsWith("after_12th"))));
      else matchGrade = (p.grade_level === grade || p.grade_level === "after_10th_or_12th" || (p.eligible_grades && p.eligible_grades.includes(grade)));
      return matchCat && matchGrade;
    });

    // If active category has 0 courses in this new grade, auto-reset category to "all"!
    if (!hasCatMatch) {
      activeCatFilter = "all";
      document.querySelectorAll("[data-filter-type='cat']").forEach((b) => {
        if (b.getAttribute("data-val") === "all") {
          b.classList.add("active");
        } else {
          b.classList.remove("active");
        }
      });
    }
  }

  // Update Category buttons visual state
  updateCategoryChipsAvailability(grade);

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

function updateCategoryChipsAvailability(grade) {
  document.querySelectorAll("[data-filter-type='cat']").forEach((btn) => {
    const cat = btn.getAttribute("data-val");
    if (cat === "all") return;

    const count = allSchoolPaths.filter((p) => {
      const matchCat = (p.category === cat);
      let matchGrade = false;
      if (grade === "all") matchGrade = true;
      else if (grade === "after_10th") matchGrade = (p.grade_level === "after_10th" || p.grade_level === "after_10th_or_12th" || (p.eligible_grades && p.eligible_grades.includes("after_10th")));
      else if (grade === "after_12th") matchGrade = (p.grade_level.startsWith("after_12th") || p.grade_level === "after_10th_or_12th" || (p.eligible_grades && p.eligible_grades.some((g) => g.startsWith("after_12th"))));
      else matchGrade = (p.grade_level === grade || p.grade_level === "after_10th_or_12th" || (p.eligible_grades && p.eligible_grades.includes(grade)));
      return matchCat && matchGrade;
    }).length;

    if (count === 0 && grade !== "all") {
      btn.style.opacity = "0.45";
      btn.title = `Requires switching stream. Click to auto-switch to eligible group.`;
    } else {
      btn.style.opacity = "1";
      btn.title = `${count} opportunities available for your selected grade`;
    }
  });
}

function filterPathsByCategory(cat, btn) {
  // Check if this category has paths in the current activeGradeFilter
  let matchingPaths = allSchoolPaths.filter((p) => {
    const matchCat = (cat === "all" || p.category === cat);
    let matchGrade = false;
    if (activeGradeFilter === "all") matchGrade = true;
    else if (activeGradeFilter === "after_10th") matchGrade = (p.grade_level === "after_10th" || p.grade_level === "after_10th_or_12th" || (p.eligible_grades && p.eligible_grades.includes("after_10th")));
    else if (activeGradeFilter === "after_12th") matchGrade = (p.grade_level.startsWith("after_12th") || p.grade_level === "after_10th_or_12th" || (p.eligible_grades && p.eligible_grades.some((g) => g.startsWith("after_12th"))));
    else matchGrade = (p.grade_level === activeGradeFilter || p.grade_level === "after_10th_or_12th" || (p.eligible_grades && p.eligible_grades.includes(activeGradeFilter)));
    return matchCat && matchGrade;
  });

  // If user selected a category that has 0 paths for their current grade filter:
  // Auto-switch to the appropriate grade filter with a smooth, helpful transition!
  if (matchingPaths.length === 0 && cat !== "all") {
    if (cat === "engineering") {
      if (activeGradeFilter === "after_10th") {
        cat = "diploma_polytechnic";
        showCompassToast("Selected Polytechnic / Diploma — the direct technical engineering pathway after 10th Standard.", "info");
      } else if (activeGradeFilter === "after_12th_commerce" || activeGradeFilter === "after_12th_arts") {
        cat = "arts_science";
        showCompassToast("B.E/B.Tech requires 12th Mathematics. Showing BCA & Financial Technology — the premier software, computing & tech pathways for your group!", "info");
      } else {
        activeGradeFilter = "after_12th_pcm";
        showCompassToast("Switched to 12th Science (PCM / Maths) — Engineering (B.E/B.Tech) admissions in Tamil Nadu require Higher Secondary Mathematics.", "info");
      }
    } else if (cat === "medical") {
      activeGradeFilter = "after_12th_pcb";
      showCompassToast("Switched to 12th Science (PCB / Biology) — MBBS/BDS Medical admissions require Higher Secondary Biology.", "info");
    } else if (cat === "diploma_polytechnic" || cat === "vocational_iti") {
      activeGradeFilter = "after_10th";
      showCompassToast("Switched to After 10th Standard — Polytechnic Diplomas & ITI Trades are direct admissions after 10th SSLC.", "info");
    } else if (cat === "agriculture") {
      activeGradeFilter = "after_12th_pcb";
      showCompassToast("Switched to 12th Science (PCB / Biology) — TNAU Agriculture & TANUVAS Veterinary require Biology.", "info");
    }

    // Update grade filter UI buttons
    document.querySelectorAll("[data-filter-type='grade']").forEach((b) => {
      if (b.getAttribute("data-val") === activeGradeFilter) {
        b.classList.add("active");
      } else {
        b.classList.remove("active");
      }
    });

    updateCategoryChipsAvailability(activeGradeFilter);
  }

  activeCatFilter = cat;
  document.querySelectorAll("[data-filter-type='cat']").forEach((b) => {
    if (b.getAttribute("data-val") === cat) {
      b.classList.add("active");
    } else {
      b.classList.remove("active");
    }
  });

  renderSchoolPaths();
}

function renderSchoolPaths() {
  const grid = document.getElementById("school-paths-grid");
  if (!grid) return;

  if (!allSchoolPaths || allSchoolPaths.length === 0) {
    if (typeof window !== "undefined" && window.COMPASS_STATIC_DATA && window.COMPASS_STATIC_DATA.paths) {
      allSchoolPaths = window.COMPASS_STATIC_DATA.paths;
    }
  }

  let filtered = allSchoolPaths || [];

  if (activeGradeFilter !== "all") {
    if (activeGradeFilter === "after_10th") {
      filtered = filtered.filter(
        (p) => p.grade_level === "after_10th" || p.grade_level === "after_10th_or_12th" || (p.eligible_grades && p.eligible_grades.includes("after_10th"))
      );
    } else if (activeGradeFilter === "after_12th") {
      filtered = filtered.filter(
        (p) => p.grade_level.startsWith("after_12th") || p.grade_level === "after_10th_or_12th" || (p.eligible_grades && p.eligible_grades.some((g) => g.startsWith("after_12th")))
      );
    } else {
      filtered = filtered.filter(
        (p) => p.grade_level === activeGradeFilter || p.grade_level === "after_10th_or_12th" || (p.eligible_grades && p.eligible_grades.includes(activeGradeFilter))
      );
    }
  }

  if (activeCatFilter !== "all") {
    filtered = filtered.filter((p) => p.category === activeCatFilter);
  }

  if (!filtered || filtered.length === 0) {
    let explanationHtml = "";
    if (activeGradeFilter === "after_12th_pcb" && activeCatFilter === "engineering") {
      explanationHtml = `
        <div class="col-12 py-5 bg-white rounded-4 border shadow-sm text-center">
          <div class="fs-1 mb-2">⚙️🩺</div>
          <h5 class="fw-bold text-dark">Engineering (B.E / B.Tech) Requires Mathematics (PCM) in 12th Standard</h5>
          <p class="text-secondary small mb-3" style="max-width: 620px; margin: 0 auto;">
            In Tamil Nadu, single-window engineering admissions (TNEA / Anna University) require Higher Secondary Mathematics.
            As a <strong>12th Science (PCB / Biology)</strong> student, you are directly eligible for premier professional paths in <strong>Medicine (MBBS/BDS), Paramedical Sciences, Veterinary (BVSc at TANUVAS), Agriculture (TNAU), and Pharmacy</strong>.
          </p>
          <div class="d-flex justify-content-center gap-2 flex-wrap">
            <button class="btn btn-primary btn-sm rounded-pill px-4 fw-bold shadow-sm" onclick="filterPathsByCategory('medical', null)">
              🩺 View Medical &amp; Paramedical Paths
            </button>
            <button class="btn btn-success btn-sm rounded-pill px-4 fw-bold shadow-sm" onclick="filterPathsByCategory('agriculture', null)">
              🌾 View Agriculture &amp; Veterinary Paths
            </button>
            <button class="btn btn-info btn-sm text-white rounded-pill px-4 fw-bold shadow-sm" onclick="filterPathsByGrade('after_12th_pcm', null)">
              ⚙️ Switch to 12th PCM for Engineering
            </button>
            <button class="btn btn-outline-secondary btn-sm rounded-pill px-3" onclick="resetSchoolFilters()">
              🌐 Show All PCB Opportunities
            </button>
          </div>
        </div>
      `;
    } else if (activeGradeFilter === "after_12th_commerce" && activeCatFilter === "engineering") {
      explanationHtml = `
        <div class="col-12 py-5 bg-white rounded-4 border shadow-sm text-center">
          <div class="fs-1 mb-2">📊⚙️</div>
          <h5 class="fw-bold text-dark">Engineering is Not Open to Commerce Stream Students</h5>
          <p class="text-secondary small mb-3" style="max-width: 620px; margin: 0 auto;">
            Engineering requires Physics, Chemistry &amp; Mathematics in Higher Secondary.
            As a <strong>12th Commerce</strong> student, you qualify for high-impact careers in <strong>Chartered Accountancy (CA), Cost &amp; Management Accountancy (CMA), Corporate Law (B.Com LL.B at SOEL), and Professional Finance</strong>.
          </p>
          <div class="d-flex justify-content-center gap-2 flex-wrap">
            <button class="btn btn-primary btn-sm rounded-pill px-4 fw-bold shadow-sm" onclick="filterPathsByCategory('arts_science', null)">
              📊 View Commerce &amp; CA/CMA Opportunities
            </button>
            <button class="btn btn-outline-primary btn-sm rounded-pill px-4 fw-bold shadow-sm" onclick="filterPathsByCategory('law', null)">
              ⚖️ View 5-Year Integrated B.Com. LL.B Law
            </button>
            <button class="btn btn-info btn-sm text-white rounded-pill px-4 fw-bold shadow-sm" onclick="filterPathsByGrade('after_12th_pcm', null)">
              ⚙️ Switch to 12th PCM for Engineering
            </button>
            <button class="btn btn-outline-secondary btn-sm rounded-pill px-3" onclick="resetSchoolFilters()">
              🌐 Show All Commerce Opportunities
            </button>
          </div>
        </div>
      `;
    } else {
      explanationHtml = `
        <div class="col-12 text-center py-5 bg-white rounded-4 border shadow-sm">
          <div class="fs-1 mb-2">🔍</div>
          <h5 class="fw-bold text-dark">No career paths match the selected filters</h5>
          <p class="text-secondary small mb-3">Try viewing all streams for this grade, or reset filters.</p>
          <div class="d-flex justify-content-center gap-2 flex-wrap">
            <button class="btn btn-primary btn-sm rounded-pill px-4 fw-bold shadow-sm" onclick="filterPathsByCategory('all', null)">
              Show All Courses for My Grade
            </button>
            <button class="btn btn-outline-secondary btn-sm rounded-pill px-4 fw-bold" onclick="resetSchoolFilters()">
              Reset All Filters
            </button>
            <button class="btn btn-outline-primary btn-sm rounded-pill px-4 fw-bold" onclick="switchSchoolTab('twelfth_groups')">
              🎓 View 12th Group Guidance
            </button>
          </div>
        </div>
      `;
    }
    grid.innerHTML = explanationHtml;
    return;
  }

  const noticeHtml = (activeGradeFilter === "after_12th_pcb" && activeCatFilter === "engineering") ? `
    <div class="col-12 mb-3">
      <div class="alert alert-info py-2.5 px-3 rounded-4 d-flex align-items-center gap-3 mb-0 shadow-xs">
        <span class="fs-3">🧬</span>
        <div class="small">
          <strong class="text-primary">Bio-Engineering Pathways for 12th Biology:</strong> B.Tech Biotechnology &amp; Biomedical Engineering in Tamil Nadu admit 12th Biology students directly via Anna University / TNEA and premier universities. <em>(For conventional CSE/ECE/Mechanical, 12th PCM with Mathematics is required via TNEA).</em>
        </div>
      </div>
    </div>
  ` : "";

  grid.innerHTML = noticeHtml + filtered
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
  updateCategoryChipsAvailability("all");
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

  let collegesToRender = null;
  try {
    const res = await api.post("/placement-compass/colleges/compare", {
      college_ids: uniqueIds,
    });

    if (res && res.data && res.data.colleges) {
      collegesToRender = res.data.colleges;
    }
  } catch (err) {
    console.warn("Using local college comparison fallback:", err);
  }

  if (!collegesToRender || collegesToRender.length === 0) {
    if (!allCollegesList || allCollegesList.length === 0) {
      if (typeof window !== "undefined" && window.COMPASS_STATIC_DATA && window.COMPASS_STATIC_DATA.colleges) {
        allCollegesList = window.COMPASS_STATIC_DATA.colleges;
      }
    }
    collegesToRender = (allCollegesList || []).filter((c) => uniqueIds.includes(c.id));
  }

  if (collegesToRender && collegesToRender.length >= 2) {
    renderCollegeComparisonMatrix(collegesToRender);
  }
}

function renderCollegeComparisonMatrix(colleges) {
  const container = document.getElementById("college-compare-matrix-container");
  if (!container) return;

  container.innerHTML = `
    <table class="table career-compare-table align-middle mb-0" id="college-comparison-table">
      <thead>
        <tr>
          <th class="benchmark-col" style="position: sticky; left: 0; z-index: 2; background: #f8fafc;">
            <div class="fw-bold text-secondary text-uppercase small">College Benchmark</div>
            <div class="text-muted" style="font-size: 0.72rem;">Comparing ${colleges.length} TN Institutions</div>
          </th>
          ${colleges
            .map(
              (c) => `
            <th class="college-data-col text-center">
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
        <tr class="compare-section-header">
          <td colspan="${colleges.length + 1}" class="fw-bold text-primary small text-uppercase py-2 px-3">
            🎓 Academic Programs &amp; Accreditations
          </td>
        </tr>
        <tr>
          <td class="benchmark-col fw-bold text-secondary">Accreditation &amp; Status</td>
          ${colleges.map((c) => `<td class="college-data-col text-center small fw-semibold text-dark">${c.accreditation}</td>`).join("")}
        </tr>
        <tr>
          <td class="benchmark-col fw-bold text-secondary">Flagship Degrees / Courses</td>
          ${colleges
            .map(
              (c) => `
            <td class="college-data-col small">
              <ul class="ps-3 mb-0 text-secondary">
                ${c.flagship_courses.map((cr) => `<li>${cr}</li>`).join("")}
              </ul>
            </td>
          `
            )
            .join("")}
        </tr>

        <!-- Eligibility Criteria -->
        <tr class="compare-section-header">
          <td colspan="${colleges.length + 1}" class="fw-bold text-primary small text-uppercase py-2 px-3">
            📋 Course Eligibility Requirements
          </td>
        </tr>
        <tr>
          <td class="benchmark-col fw-bold text-secondary">Minimum Eligibility Criteria</td>
          ${colleges.map((c) => `<td class="college-data-col small text-secondary">${c.eligibility_criteria}</td>`).join("")}
        </tr>

        <!-- Entrance Exam & Exam Schedule -->
        <tr class="compare-section-header">
          <td colspan="${colleges.length + 1}" class="fw-bold text-primary small text-uppercase py-2 px-3">
            📝 Entrance Exam Guidance &amp; Exact Schedule
          </td>
        </tr>
        <tr>
          <td class="benchmark-col fw-bold text-secondary">Entrance Exams Accepted</td>
          ${colleges
            .map(
              (c) => `
            <td class="college-data-col">
              <div class="d-flex flex-wrap gap-1 justify-content-center">
                ${c.entrance_exams.map((e) => `<span class="badge bg-info-subtle text-dark border small">${e}</span>`).join("")}
              </div>
            </td>
          `
            )
            .join("")}
        </tr>
        <tr>
          <td class="benchmark-col fw-bold text-secondary">Exam Application Dates</td>
          ${colleges
            .map(
              (c) => `
            <td class="college-data-col small text-center">
              <div><strong>Start:</strong> ${c.exam_schedule.application_start}</div>
              <div class="text-danger"><strong>Last Date:</strong> ${c.exam_schedule.last_date}</div>
            </td>
          `
            )
            .join("")}
        </tr>
        <tr>
          <td class="benchmark-col fw-bold text-secondary">Exam Date &amp; Results</td>
          ${colleges
            .map(
              (c) => `
            <td class="college-data-col small text-center">
              <div><strong>Exam Date:</strong> ${c.exam_schedule.exam_date}</div>
              <div class="text-success"><strong>Result:</strong> ${c.exam_schedule.result_date}</div>
            </td>
          `
            )
            .join("")}
        </tr>

        <!-- Admission & Counselling Guidance -->
        <tr class="compare-section-header">
          <td colspan="${colleges.length + 1}" class="fw-bold text-primary small text-uppercase py-2 px-3">
            ⚡ Admission &amp; Counselling Procedure
          </td>
        </tr>
        <tr>
          <td class="benchmark-col fw-bold text-secondary">Complete Admission Process</td>
          ${colleges.map((c) => `<td class="college-data-col small text-secondary" style="line-height: 1.6;">${c.admission_counselling_process}</td>`).join("")}
        </tr>

        <!-- Fees & Scholarships -->
        <tr class="compare-section-header">
          <td colspan="${colleges.length + 1}" class="fw-bold text-primary small text-uppercase py-2 px-3">
            💰 Annual Fees &amp; Scholarship Coverage
          </td>
        </tr>
        <tr>
          <td class="benchmark-col fw-bold text-secondary">Tuition Fees / Year</td>
          ${colleges.map((c) => `<td class="college-data-col text-center fw-bold text-success small">${c.tuition_fees_per_year}</td>`).join("")}
        </tr>
        <tr>
          <td class="benchmark-col fw-bold text-secondary">Hostel &amp; Mess Fees / Year</td>
          ${colleges.map((c) => `<td class="college-data-col text-center text-muted small">${c.hostel_mess_fees_per_year}</td>`).join("")}
        </tr>
        <tr>
          <td class="benchmark-col fw-bold text-secondary">Scholarships Available</td>
          ${colleges
            .map(
              (c) => `
            <td class="college-data-col small">
              <ul class="ps-3 mb-0 text-success">
                ${c.scholarships_available.map((s) => `<li>${s}</li>`).join("")}
              </ul>
            </td>
          `
            )
            .join("")}
        </tr>

        <!-- Placements -->
        <tr class="compare-section-header">
          <td colspan="${colleges.length + 1}" class="fw-bold text-primary small text-uppercase py-2 px-3">
            🚀 Campus Placement Packages &amp; Opportunities
          </td>
        </tr>
        <tr>
          <td class="benchmark-col fw-bold text-secondary">Highest CTC Package</td>
          ${colleges.map((c) => `<td class="college-data-col text-center fw-bold text-dark">${c.placement_stats.highest_package}</td>`).join("")}
        </tr>
        <tr>
          <td class="benchmark-col fw-bold text-secondary">Average CTC Package</td>
          ${colleges.map((c) => `<td class="college-data-col text-center fw-bold text-primary fs-6">${c.placement_stats.average_package}</td>`).join("")}
        </tr>
        <tr>
          <td class="benchmark-col fw-bold text-secondary">Placement Success %</td>
          ${colleges.map((c) => `<td class="college-data-col text-center fw-bold text-success">${c.placement_stats.placement_percentage}</td>`).join("")}
        </tr>
        <tr>
          <td class="benchmark-col fw-bold text-secondary">Top Visiting Recruiters</td>
          ${colleges
            .map(
              (c) => `
            <td class="college-data-col">
              <div class="d-flex flex-wrap gap-1 justify-content-center">
                ${c.placement_stats.top_recruiters.map((r) => `<span class="badge bg-secondary-subtle text-dark small">${r}</span>`).join("")}
              </div>
            </td>
          `
            )
            .join("")}
        </tr>

        <!-- Facilities -->
        <tr class="compare-section-header">
          <td colspan="${colleges.length + 1}" class="fw-bold text-primary small text-uppercase py-2 px-3">
            🏛️ Campus Infrastructure &amp; Facilities
          </td>
        </tr>
        <tr>
          <td class="benchmark-col fw-bold text-secondary">Campus Facilities</td>
          ${colleges
            .map(
              (c) => `
            <td class="college-data-col small">
              <ul class="ps-3 mb-0 text-secondary">
                ${c.campus_facilities.map((f) => `<li>${f}</li>`).join("")}
              </ul>
            </td>
          `
            )
            .join("")}
        </tr>

        <!-- Pros & Cons -->
        <tr class="compare-section-header">
          <td colspan="${colleges.length + 1}" class="fw-bold text-primary small text-uppercase py-2 px-3">
            ⚖️ Key Advantages &amp; Considerations
          </td>
        </tr>
        <tr>
          <td class="benchmark-col fw-bold text-success">Verified Advantages</td>
          ${colleges
            .map(
              (c) => `
            <td class="college-data-col small">
              <ul class="ps-3 mb-0 text-success">
                ${c.pros.map((p) => `<li>${p}</li>`).join("")}
              </ul>
            </td>
          `
            )
            .join("")}
        </tr>
        <tr>
          <td class="benchmark-col fw-bold text-danger">Considerations</td>
          ${colleges
            .map(
              (c) => `
            <td class="college-data-col small">
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

  if (preset === "be_cs_vs_bsc_cs") {
    if (cr1) cr1.value = "btech_cse";
    if (cr2) cr2.value = "bsc_cs";
    if (cr3) cr3.value = "";
  } else if (preset === "bca_vs_bsc_cs") {
    if (cr1) cr1.value = "bca_course";
    if (cr2) cr2.value = "bsc_cs";
    if (cr3) cr3.value = "";
  } else if (preset === "bcom_vs_bba") {
    if (cr1) cr1.value = "bcom_general";
    if (cr2) cr2.value = "bba_management";
    if (cr3) cr3.value = "";
  } else if (preset === "mbbs_vs_allied") {
    if (cr1) cr1.value = "mbbs_course";
    if (cr2) cr2.value = "allied_health_course";
    if (cr3) cr3.value = "";
  } else if (preset === "poly_vs_11th_12th") {
    if (cr1) cr1.value = "diploma_mechanical_engg";
    if (cr2) cr2.value = "hsc_bio_maths";
    if (cr3) cr3.value = "";
  } else if (preset === "iti_vs_poly") {
    if (cr1) cr1.value = "iti_electrician_fitter";
    if (cr2) cr2.value = "diploma_mechanical_engg";
    if (cr3) cr3.value = "";
  } else if (preset === "cse_vs_ece_vs_poly") {
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

  let coursesToRender = null;
  try {
    const res = await api.post("/placement-compass/courses/compare", {
      course_ids: uniqueIds,
    });

    if (res && res.data && res.data.courses) {
      coursesToRender = res.data.courses;
    }
  } catch (err) {
    console.warn("Using local course comparison fallback:", err);
  }

  if (!coursesToRender || coursesToRender.length === 0) {
    if (!allComparableCourses || allComparableCourses.length === 0) {
      if (typeof window !== "undefined" && window.COMPASS_STATIC_DATA && window.COMPASS_STATIC_DATA.courses) {
        allComparableCourses = window.COMPASS_STATIC_DATA.courses;
      }
    }
    coursesToRender = (allComparableCourses || []).filter((c) => uniqueIds.includes(c.id));
  }

  if (coursesToRender && coursesToRender.length >= 2) {
    renderCourseComparisonMatrix(coursesToRender);
  }
}

function renderCourseComparisonMatrix(courses) {
  const container = document.getElementById("course-compare-matrix-container");
  if (!container) return;

  container.innerHTML = `
    <table class="table career-compare-table align-middle mb-0" id="course-comparison-table">
      <thead>
        <tr>
          <th class="benchmark-col" style="position: sticky; left: 0; z-index: 2; background: #f8fafc;">
            <div class="fw-bold text-secondary text-uppercase small">Course Benchmark</div>
            <div class="text-muted" style="font-size: 0.72rem;">Comparing ${courses.length} Academic Pathways</div>
          </th>
          ${courses
            .map(
              (cr) => `
            <th class="course-data-col text-center">
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
          <td class="benchmark-col fw-bold text-secondary">Eligibility Criteria</td>
          ${courses.map((cr) => `<td class="course-data-col small text-secondary">${cr.eligibility}</td>`).join("")}
        </tr>
        <tr>
          <td class="benchmark-col fw-bold text-secondary">Required Entrance Exams</td>
          ${courses
            .map(
              (cr) => `
            <td class="course-data-col">
              <div class="d-flex flex-wrap gap-1 justify-content-center">
                ${cr.entrance_exams.map((e) => `<span class="badge bg-light text-dark border small">${e}</span>`).join("")}
              </div>
            </td>
          `
            )
            .join("")}
        </tr>
        <tr>
          <td class="benchmark-col fw-bold text-secondary">Average Starting Salary</td>
          ${courses.map((cr) => `<td class="course-data-col text-center fw-bold text-success fs-6">${cr.avg_starting_salary}</td>`).join("")}
        </tr>
        <tr>
          <td class="benchmark-col fw-bold text-secondary">Top Roles &amp; Opportunities</td>
          ${courses
            .map(
              (cr) => `
            <td class="course-data-col small">
              <ul class="ps-3 mb-0 text-secondary">
                ${cr.top_roles.map((r) => `<li>${r}</li>`).join("")}
              </ul>
            </td>
          `
            )
            .join("")}
        </tr>
        <tr>
          <td class="benchmark-col fw-bold text-secondary">Future Scopes &amp; Lateral Entry</td>
          ${courses
            .map(
              (cr) => `
            <td class="course-data-col small">
              <ul class="ps-3 mb-0 text-secondary">
                ${cr.future_scopes.map((f) => `<li>${f}</li>`).join("")}
              </ul>
            </td>
          `
            )
            .join("")}
        </tr>
        <tr>
          <td class="benchmark-col fw-bold text-secondary">Why Choose This Course</td>
          ${courses.map((cr) => `<td class="course-data-col small text-dark fw-medium">${cr.why_choose}</td>`).join("")}
        </tr>
      </tbody>
    </table>
  `;
}

// -------------------------------------------------------------
// HORIZONTAL SCROLL & FULL PAGE / WIDE VIEW HANDLERS
// -------------------------------------------------------------
function scrollCompareTable(type, direction) {
  const container = document.getElementById(type === "college" ? "college-compare-matrix-container" : "course-compare-matrix-container");
  if (container) {
    const shift = direction === "next" ? 340 : -340;
    container.scrollBy({ left: shift, behavior: "smooth" });
  }
}
window.scrollCompareTable = scrollCompareTable;

function toggleFullPageCompare(type) {
  const boxId = type === "college" ? "college-compare-view-box" : "course-compare-view-box";
  const box = document.getElementById(boxId);
  if (!box) return;

  const isFull = box.classList.toggle("compare-fullpage-modal");
  const btn = document.getElementById(type === "college" ? "colleges-fs-btn" : "courses-fs-btn");
  const icon = document.getElementById(type === "college" ? "colleges-fs-icon" : "courses-fs-icon");
  const label = document.getElementById(type === "college" ? "colleges-fs-label" : "courses-fs-label");

  let floatBtn = document.getElementById("compare-floating-exit-btn");

  if (isFull) {
    document.body.style.overflow = "hidden";
    if (icon) icon.textContent = "✕";
    if (label) label.textContent = "Exit Full Page View";
    if (btn) {
      btn.classList.remove("btn-primary", "btn-outline-primary");
      btn.classList.add("btn-danger");
    }
    box.scrollTop = 0;

    if (!floatBtn) {
      floatBtn = document.createElement("button");
      floatBtn.id = "compare-floating-exit-btn";
      floatBtn.className = "btn btn-danger btn-sm rounded-pill px-3 py-2 fw-bold shadow-lg position-fixed";
      floatBtn.style.cssText = "top: 20px; right: 28px; z-index: 10600; cursor: pointer;";
      floatBtn.innerHTML = "✕ Exit Full Page View (Esc)";
      floatBtn.onclick = () => toggleFullPageCompare(type);
      document.body.appendChild(floatBtn);
    }
  } else {
    document.body.style.overflow = "";
    if (icon) icon.textContent = "⛶";
    if (label) label.textContent = "Full Page View";
    if (btn) {
      btn.classList.remove("btn-danger");
      btn.classList.add("btn-primary");
    }
    if (floatBtn) {
      floatBtn.remove();
    }
  }
}
window.toggleFullPageCompare = toggleFullPageCompare;

// Escape key listener to exit full page comparison
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    const modals = document.querySelectorAll(".compare-fullpage-modal");
    if (modals.length > 0) {
      modals.forEach((m) => m.classList.remove("compare-fullpage-modal"));
      document.body.style.overflow = "";
      const floatBtn = document.getElementById("compare-floating-exit-btn");
      if (floatBtn) floatBtn.remove();
      ["colleges", "courses"].forEach((prefix) => {
        const btn = document.getElementById(`${prefix}-fs-btn`);
        const icon = document.getElementById(`${prefix}-fs-icon`);
        const label = document.getElementById(`${prefix}-fs-label`);
        if (btn) {
          btn.classList.remove("btn-danger");
          btn.classList.add("btn-primary");
        }
        if (icon) icon.textContent = "⛶";
        if (label) label.textContent = "Full Page View";
      });
    }
  }
});

// -------------------------------------------------------------
// 4. PATHWAY DETAIL MODAL
// -------------------------------------------------------------
// -------------------------------------------------------------
// 4. COMPREHENSIVE COURSE DEEP DIVE MODAL & CAREER ROADMAP
// -------------------------------------------------------------

function showPlacementToast(msg) {
  let toastContainer = document.getElementById("compass-toast-container");
  if (!toastContainer) {
    toastContainer = document.createElement("div");
    toastContainer.id = "compass-toast-container";
    toastContainer.style.cssText = "position: fixed; bottom: 25px; right: 25px; z-index: 10999; display: flex; flex-direction: column; gap: 10px;";
    document.body.appendChild(toastContainer);
  }
  const toast = document.createElement("div");
  toast.className = "toast align-items-center text-white bg-dark border-0 show shadow-lg rounded-4 p-3";
  toast.style.cssText = "min-width: 320px; max-width: 440px; animation: fadeIn 0.3s ease;";
  toast.innerHTML = `
    <div class="d-flex align-items-center justify-content-between">
      <div class="toast-body p-0 small fw-semibold">
        ${msg}
      </div>
      <button type="button" class="btn-close btn-close-white btn-sm ms-2" onclick="this.parentElement.parentElement.remove()"></button>
    </div>
  `;
  toastContainer.appendChild(toast);
  setTimeout(() => {
    toast.remove();
  }, 4500);
}
window.showPlacementToast = showPlacementToast;

function applyForPlacementJob(jobTitle) {
  showPlacementToast(`💼 Application Submitted! You have applied for "<strong>${jobTitle}</strong>". Our automated recruitment matching engine will prioritize your qualification profile.`);
}
window.applyForPlacementJob = applyForPlacementJob;

function openPathwayModal(pathId) {
  let path = (allSchoolPaths || []).find((p) => p.id === pathId);
  if (!path && typeof window !== "undefined" && window.COMPASS_STATIC_DATA && window.COMPASS_STATIC_DATA.paths) {
    path = window.COMPASS_STATIC_DATA.paths.find((p) => p.id === pathId);
  }
  if (!path && typeof window !== "undefined" && window.COMPASS_STATIC_DATA && window.COMPASS_STATIC_DATA.courses) {
    const cr = window.COMPASS_STATIC_DATA.courses.find((c) => c.id === pathId);
    if (cr) {
      path = {
        id: cr.id,
        title: cr.course_name,
        category: cr.category,
        grade_level: "after_12th",
        icon_emoji: cr.category === "engineering" ? "💻" : cr.category === "medical" ? "🩺" : "📊",
        tagline: cr.why_choose,
        duration: cr.duration,
        eligibility: cr.eligibility,
        entrance_exams: (cr.entrance_exams || []).map(e => ({ name: e, level: "State/National", description: "Official entrance exam" })),
        top_colleges: ["Anna University / Madras University Flagship Campuses", "Premier Autonomous Institutions in Tamil Nadu"],
        admission_procedure: "Single-window online counselling through official Tamil Nadu portal with 7.5% Government School free tuition and hostel quota.",
        estimated_fees: { govt_college: "₹3,500 - ₹9,500 / year", private_college: "₹45,000 - ₹95,000 / year" },
        scholarships: ["Pudhumai Penn (₹1,000/mo for girls)", "Tamil Puthalvan (₹1,000/mo for boys)", "Post-Matric SC/ST 100% Free Scholarship"],
        career_opportunities: cr.top_roles || ["Associate Professional", "Junior Specialist"],
        starting_salary_range: cr.avg_starting_salary || "₹3.6 LPA - ₹8.0 LPA",
        future_study_options: cr.future_scopes || ["Master's Degree (M.E/M.Tech/MBA/M.Sc)"],
        key_skills_needed: ["Core Domain Expertise", "Practical Analytical Skills", "Industry Software Tools", "Professional Communication"]
      };
    }
  }

  if (!path) {
    console.warn("Could not find pathway or course with ID:", pathId);
    return;
  }
  currentModalPathId = path.id;

  const iconEl = document.getElementById("modal-path-icon");
  const titleEl = document.getElementById("modal-path-title");
  const catEl = document.getElementById("modal-path-category");
  const durEl = document.getElementById("modal-path-duration");
  if (iconEl) iconEl.textContent = path.icon_emoji || "🎓";
  if (titleEl) titleEl.textContent = path.title || "Career Pathway";
  if (catEl) catEl.textContent = (path.category || "GENERAL").toUpperCase().replace("_", " ");
  if (durEl) durEl.textContent = path.duration || "Multi-Year";

  const bodyEl = document.getElementById("modal-path-body");
  if (bodyEl) {
    bodyEl.innerHTML = renderPathwayDeepDiveContent(path);
  }

  const modalEl = document.getElementById("pathwayDetailModal");
  if (modalEl) {
    const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
    modal.show();
  }
}
window.openPathwayModal = openPathwayModal;

function renderPathwayDeepDiveContent(path) {
  // 1. Entrance exams HTML
  const examsHtml = (path.entrance_exams || [])
    .map(
      (e) => `
      <div class="p-3 bg-white rounded-3 border mb-2 shadow-xs">
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

  // 2. Colleges & Scholarships HTML
  const collegesHtml = (path.top_colleges || []).map((c) => `<li class="mb-1 text-dark small fw-medium">🏛️ ${c}</li>`).join("");
  const scholarshipsHtml = (path.scholarships || []).map((s) => `<li class="mb-1 text-success fw-bold small">✅ ${s}</li>`).join("");

  // 3. What Students Will Learn (Syllabus & Practical Skills)
  const skillsList = path.key_skills_needed || ["Foundational Science", "Practical Laboratory Training", "Industry Problem Solving", "Professional Ethics"];
  const skillsBadges = skillsList.map(s => `<span class="badge bg-primary-subtle text-primary border border-primary-subtle py-1.5 px-3 rounded-pill small fw-bold me-1 mb-1">🛠️ ${s}</span>`).join("");

  // 4. Live Placement Jobs Matching This Pathway
  let matchingJobsHtml = "";
  const allPositions = (typeof allCareerPositions !== "undefined" && allCareerPositions.length > 0)
    ? allCareerPositions
    : (typeof window !== "undefined" && window.COMPASS_STATIC_DATA && window.COMPASS_STATIC_DATA.positions)
      ? window.COMPASS_STATIC_DATA.positions
      : [];

  const matchedPositions = allPositions.filter(pos => {
    if (path.category === "engineering" && (pos.target_group === "computer_science" || pos.sector?.toLowerCase().includes("engineer"))) return true;
    if (path.category === "medical" && (pos.target_group === "biology" || pos.sector?.toLowerCase().includes("health") || pos.sector?.toLowerCase().includes("medical"))) return true;
    if (path.category === "commerce" && (pos.target_group === "commerce" || pos.sector?.toLowerCase().includes("finance") || pos.sector?.toLowerCase().includes("commerce"))) return true;
    if (path.category === "law" && (pos.target_group === "arts" || pos.sector?.toLowerCase().includes("law"))) return true;
    if (path.category === "iti" && (pos.target_group === "sslc_10th" || pos.target_group === "vocational")) return true;
    if (path.category === "defence_govt" && (pos.target_group === "sslc_10th" || pos.target_group === "arts")) return true;
    return (pos.target_groups || []).includes(path.grade_level?.replace("after_12th_", "")) || (pos.target_groups || []).includes(path.category);
  });

  const jobsToDisplay = (matchedPositions.length > 0 ? matchedPositions : allPositions).slice(0, 3);
  matchingJobsHtml = jobsToDisplay.map(job => `
    <div class="col-md-4">
      <div class="card border border-primary border-opacity-25 rounded-4 p-3 bg-white h-100 shadow-xs d-flex flex-column">
        <div class="d-flex justify-content-between align-items-start gap-1 mb-2">
          <h6 class="fw-bold text-dark mb-0 small">${job.position_title}</h6>
          <span class="badge bg-success-subtle text-success small fw-bold">${job.salary_range?.split("->")[0]?.trim() || "Competitive"}</span>
        </div>
        <p class="text-secondary small mb-2" style="font-size: 0.78rem; line-height: 1.4;">${job.position_description?.slice(0, 110)}...</p>
        <div class="small text-muted mb-2" style="font-size: 0.75rem;">
          <strong>🏢 Top Recruiters:</strong> ${(job.recruiting_organizations || []).slice(0, 3).join(", ")}
        </div>
        <div class="mt-auto pt-2 border-top">
          <button class="btn btn-outline-primary btn-sm rounded-pill fw-bold w-100 shadow-xs" onclick="applyForPlacementJob('${job.position_title.replace(/'/g, "\\'")}')">
            ⚡ Quick Apply Now
          </button>
        </div>
      </div>
    </div>
  `).join("");

  return `
    <!-- Header Overview Banner -->
    <div class="card border-0 shadow-sm p-4 mb-4 rounded-4" style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);">
      <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-2 mb-2">
        <h4 class="fw-bold text-dark mb-0">${path.title}</h4>
        <span class="badge bg-primary text-white rounded-pill px-3 py-1.5 fw-bold">${path.starting_salary_range}</span>
      </div>
      <p class="text-secondary fs-6 mb-3 fw-medium">${path.tagline}</p>
      <div class="d-flex flex-wrap gap-2">
        <span class="badge bg-white text-primary border py-1.5 px-3 rounded-pill small fw-bold">🎓 Category: ${path.category.toUpperCase().replace("_", " ")}</span>
        <span class="badge bg-white text-dark border py-1.5 px-3 rounded-pill small fw-bold">⏳ Duration: ${path.duration}</span>
        <span class="badge bg-white text-success border py-1.5 px-3 rounded-pill small fw-bold">🎯 Eligible: ${path.grade_level?.replace("_", " ")?.toUpperCase() || "10th / 12th"}</span>
      </div>
    </div>

    <!-- Section 1: Course Overview -->
    <div class="card border-0 shadow-sm p-4 mb-4 rounded-4 bg-white border-start border-4 border-primary">
      <h5 class="fw-bold text-dark mb-2">📖 1. Course Overview &amp; What It Is</h5>
      <p class="text-secondary small mb-3" style="line-height: 1.7;">
        This curriculum is specifically engineered to bridge the transition from school education to professional excellence. 
        Students undergo rigorous theoretical instruction paired with extensive laboratory experiments, industrial project mentorship, and specialized clinical or corporate internships across Tamil Nadu's premiere centers.
      </p>
      <div class="alert alert-info py-2.5 px-3 rounded-3 mb-0 small border-0 bg-info bg-opacity-10 text-dark">
        <strong>💡 Student-Friendly Focus:</strong> ${path.tagline}
      </div>
    </div>

    <!-- Section 2: Why Choose This Course? -->
    <div class="card border-0 shadow-sm p-4 mb-4 rounded-4 bg-white">
      <h5 class="fw-bold text-dark mb-2">💡 2. Why Choose This Course &amp; Suitability</h5>
      <div class="row g-3">
        <div class="col-md-4">
          <div class="p-3 bg-light rounded-3 h-100 border">
            <div class="fs-4 mb-1">🚀</div>
            <strong class="text-dark small d-block mb-1">High Industry Demand</strong>
            <p class="text-muted small mb-0">Consistent placement records across state and multinational recruiters with attractive starting compensation packages.</p>
          </div>
        </div>
        <div class="col-md-4">
          <div class="p-3 bg-light rounded-3 h-100 border">
            <div class="fs-4 mb-1">🌐</div>
            <strong class="text-dark small d-block mb-1">Global Mobility &amp; Scope</strong>
            <p class="text-muted small mb-0">Direct eligibility for overseas higher studies (M.S./MBA in USA, Germany, UK) and international licensing examinations.</p>
          </div>
        </div>
        <div class="col-md-4">
          <div class="p-3 bg-light rounded-3 h-100 border">
            <div class="fs-4 mb-1">🧠</div>
            <strong class="text-dark small d-block mb-1">Ideal Student Profile</strong>
            <p class="text-muted small mb-0">Tailored for analytical problem solvers, inquisitive thinkers, and disciplined students aiming for long-term career leadership.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Section 3: Eligibility & Cutoff Criteria -->
    <div class="card border-0 shadow-sm p-4 mb-4 rounded-4 bg-white">
      <h5 class="fw-bold text-dark mb-2">🎓 3. Academic Eligibility &amp; Tamil Nadu Cutoff Rules</h5>
      <div class="alert alert-primary py-3 px-3 rounded-3 small mb-3 border-0 bg-primary bg-opacity-10 text-dark">
        <div class="fw-bold mb-1">✅ Minimum Subject Eligibility:</div>
        <div class="mb-2">${path.eligibility}</div>
        <div class="fw-bold mb-1">🧮 Admission Cutoff Standard:</div>
        <div>Tamil Nadu Single-Window Online Counselling (TNEA / TN DME / TNGASA / TANUVAS / TNAU / DOTE) based strictly on prescribed 12th/10th marks cutoff without donation.</div>
      </div>
      <div class="p-3 bg-success-subtle rounded-3 border border-success-subtle small">
        <strong class="text-success">🎁 7.5% Tamil Nadu Government School Reservation:</strong>
        <span class="text-dark">Eligible government school students receive 100% free tuition fees, free hostel accommodation, free food, and zero counselling fees under the Tamil Nadu Government 7.5% Horizontal Quota!</span>
      </div>
    </div>

    <!-- Section 4: Course Duration & Academic Structure -->
    <div class="card border-0 shadow-sm p-4 mb-4 rounded-4 bg-white">
      <h5 class="fw-bold text-dark mb-3">⏳ 4. Course Duration &amp; Academic Milestones</h5>
      <div class="row g-3">
        <div class="col-md-4">
          <div class="p-3 bg-light rounded-3 border h-100">
            <span class="badge bg-primary text-white mb-2">Phase 1: Foundation</span>
            <div class="fw-bold small text-dark mb-1">Semesters 1 &amp; 2 (Year 1)</div>
            <p class="text-secondary small mb-0">Core engineering/medical sciences, foundational mathematics, laboratory techniques, and computing fundamentals.</p>
          </div>
        </div>
        <div class="col-md-4">
          <div class="p-3 bg-light rounded-3 border h-100">
            <span class="badge bg-info text-white mb-2">Phase 2: Core &amp; Electives</span>
            <div class="fw-bold small text-dark mb-1">Semesters 3 &amp; 4 (Year 2)</div>
            <p class="text-secondary small mb-0">Advanced departmental specialization, domain software tools, hands-on mini-projects, and mid-term assessments.</p>
          </div>
        </div>
        <div class="col-md-4">
          <div class="p-3 bg-light rounded-3 border h-100">
            <span class="badge bg-success text-white mb-2">Phase 3: Internship &amp; Placements</span>
            <div class="fw-bold small text-dark mb-1">Semesters 5 to Final (Year 3/4)</div>
            <p class="text-secondary small mb-0">Industrial internship, capstone project, on-campus recruiting interviews, and state/national licensing examinations.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Section 5: What Students Will Learn -->
    <div class="card border-0 shadow-sm p-4 mb-4 rounded-4 bg-white">
      <h5 class="fw-bold text-dark mb-2">📚 5. What Students Will Learn (Syllabus &amp; Tools)</h5>
      <p class="text-secondary small mb-3">Master modern industry methodologies, software packages, and technical competencies:</p>
      <div class="d-flex flex-wrap gap-1 mb-3">
        ${skillsBadges}
      </div>
      <div class="p-3 bg-light rounded-3 border small text-secondary">
        <strong>📋 Practical Training:</strong> Hands-on workshops, real-time industrial problem solving, software laboratories, team projects, and case-study presentations.
      </div>
    </div>

    <!-- Section 6: Academic, Financial & Government Benefits -->
    <div class="card border-0 shadow-sm p-4 mb-4 rounded-4 bg-white">
      <h5 class="fw-bold text-dark mb-3">🎁 6. Academic, Financial &amp; Tamil Nadu Government Benefits</h5>
      <div class="row g-3 mb-3">
        <div class="col-md-6">
          <div class="p-3 bg-light rounded-3 border h-100">
            <h6 class="fw-bold text-dark small mb-2">🏛️ Available Premier Tamil Nadu Campuses</h6>
            <ul class="ps-3 mb-0 small text-secondary">
              ${collegesHtml}
            </ul>
          </div>
        </div>
        <div class="col-md-6">
          <div class="p-3 bg-light rounded-3 border h-100">
            <h6 class="fw-bold text-dark small mb-2">💰 Fee Structure &amp; Scholarships</h6>
            <div class="small mb-1"><strong>Govt College:</strong> <span class="text-success fw-bold">${path.estimated_fees?.govt_college || "₹3,500 - ₹9,500/year"}</span></div>
            <div class="small mb-2"><strong>Private College:</strong> <span class="text-dark fw-bold">${path.estimated_fees?.private_college || "₹45,000 - ₹95,000/year"}</span></div>
            <h6 class="fw-bold text-success small mb-1">State Scholarships &amp; Waivers:</h6>
            <ul class="ps-3 mb-0 small text-secondary">
              ${scholarshipsHtml}
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Section 7, 8, 9: Career Opportunities (Govt & Private) -->
    <div class="card border-0 shadow-sm p-4 mb-4 rounded-4 bg-white">
      <h5 class="fw-bold text-dark mb-3">💼 7. Career Opportunities: Entry Roles, Govt &amp; Private Sectors</h5>
      <div class="row g-3">
        <div class="col-md-6">
          <div class="p-3 bg-success-subtle rounded-3 border border-success-subtle h-100">
            <h6 class="fw-bold text-success small mb-2">🏢 Private Corporate &amp; Industrial Roles</h6>
            <ul class="ps-3 mb-2 small text-dark">
              ${(path.career_opportunities || []).map(co => `<li class="mb-1">💼 ${co}</li>`).join("")}
            </ul>
            <div class="small text-muted mb-2">📍 <strong>Top Hiring Hubs:</strong> Chennai OMR IT Corridor, Guindy, Coimbatore SEZ, Sriperumbudur Automotive Hub</div>
            <div class="fw-bold text-dark small pt-2 border-top border-success-subtle">
              Starting Salary: <span class="badge bg-success text-white">${path.starting_salary_range}</span>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="p-3 bg-light rounded-3 border h-100">
            <h6 class="fw-bold text-primary small mb-2">🏛️ Government Jobs &amp; Public Sector Opportunities</h6>
            <ul class="ps-3 mb-2 small text-secondary">
              <li class="mb-1"><strong>TNPSC:</strong> Assistant Engineer / Combined Technical Exams / Group 1 &amp; Group 2</li>
              <li class="mb-1"><strong>Central Govt &amp; UPSC:</strong> IES, Civil Services, Combined Defence Services (CDS), NDA</li>
              <li class="mb-1"><strong>PSUs &amp; State Corporations:</strong> BHEL Trichy, ISRO, DRDO, TANGEDCO, ONGC, NLC Neyveli</li>
              <li class="mb-1"><strong>Banking &amp; SSC:</strong> SBI Specialist Officer, IBPS PO, SSC CGL / CHSL / JE</li>
            </ul>
            <div class="small text-success fw-bold">Permanent pension, quarters, and job stability in Central/State public utilities.</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Section 10: Higher Studies & Specializations -->
    <div class="card border-0 shadow-sm p-4 mb-4 rounded-4 bg-white">
      <h5 class="fw-bold text-dark mb-2">🚀 8. Higher Studies &amp; Advanced Specializations</h5>
      <p class="text-secondary small mb-2">Progression avenues after degree graduation:</p>
      <div class="row g-2">
        ${(path.future_study_options || []).map(f => `
          <div class="col-md-6">
            <div class="p-2.5 bg-light rounded-3 border small fw-medium text-dark">
              🎓 ${f}
            </div>
          </div>
        `).join("")}
      </div>
    </div>

    <!-- Section 11: Step-by-Step Interactive Visual Career Roadmap -->
    <div class="card border-0 shadow-sm p-4 mb-4 rounded-4 bg-white border-top border-4 border-info">
      <h5 class="fw-bold text-dark mb-2">🗺️ 9. Interactive Visual Career Roadmap</h5>
      <p class="text-secondary small mb-3">From school graduation to high-earning senior leadership — visual milestones:</p>
      
      <div class="d-flex flex-column gap-2">
        <div class="p-3 rounded-3 bg-light border d-flex align-items-center gap-3">
          <span class="badge bg-primary rounded-circle p-2 fs-6">1</span>
          <div>
            <div class="fw-bold text-dark small">Milestone 1: 10th / 12th Standard Board Exams</div>
            <div class="text-muted small" style="font-size: 0.8rem;">Score high marks in state board/CBSE exams to secure competitive cutoff for single-window counseling.</div>
          </div>
        </div>

        <div class="text-center text-primary fs-5" style="line-height: 1;">&darr;</div>

        <div class="p-3 rounded-3 bg-light border d-flex align-items-center gap-3">
          <span class="badge bg-info text-white rounded-circle p-2 fs-6">2</span>
          <div>
            <div class="fw-bold text-dark small">Milestone 2: Entrance Exams &amp; Tamil Nadu Single-Window Admission</div>
            <div class="text-muted small" style="font-size: 0.8rem;">Register on official portals (TNEA / TN DME / TNGASA / TANUVAS / TNAU). Claim 7.5% Govt School quota if eligible.</div>
          </div>
        </div>

        <div class="text-center text-primary fs-5" style="line-height: 1;">&darr;</div>

        <div class="p-3 rounded-3 bg-light border d-flex align-items-center gap-3">
          <span class="badge bg-warning text-dark rounded-circle p-2 fs-6">3</span>
          <div>
            <div class="fw-bold text-dark small">Milestone 3: College Academic Foundation (Years 1 &amp; 2)</div>
            <div class="text-muted small" style="font-size: 0.8rem;">Build mathematical rigor, domain foundations, programming or laboratory techniques, and join technical clubs.</div>
          </div>
        </div>

        <div class="text-center text-primary fs-5" style="line-height: 1;">&darr;</div>

        <div class="p-3 rounded-3 bg-light border d-flex align-items-center gap-3">
          <span class="badge bg-secondary text-white rounded-circle p-2 fs-6">4</span>
          <div>
            <div class="fw-bold text-dark small">Milestone 4: Industrial Summer Internship &amp; Portfolio Capstone</div>
            <div class="text-muted small" style="font-size: 0.8rem;">Complete hands-on internships across Chennai/Coimbatore manufacturing, tech, hospital, or financial corridors.</div>
          </div>
        </div>

        <div class="text-center text-primary fs-5" style="line-height: 1;">&darr;</div>

        <div class="p-3 rounded-3 bg-success-subtle border border-success-subtle d-flex align-items-center gap-3">
          <span class="badge bg-success rounded-circle p-2 fs-6">5</span>
          <div>
            <div class="fw-bold text-success small">Milestone 5: Campus Placement Recruitment &amp; Graduate Role (${path.starting_salary_range})</div>
            <div class="text-muted small" style="font-size: 0.8rem;">Secure full-time corporate appointment or permanent state/central government service commission.</div>
          </div>
        </div>

        <div class="text-center text-success fs-5" style="line-height: 1;">&darr;</div>

        <div class="p-3 rounded-3 bg-dark text-white d-flex align-items-center gap-3">
          <span class="badge bg-light text-dark rounded-circle p-2 fs-6">6</span>
          <div>
            <div class="fw-bold text-white small">Milestone 6: Senior Technical / Clinical Leadership (₹15 - ₹35+ LPA)</div>
            <div class="text-light opacity-75 small" style="font-size: 0.8rem;">Promoted to Solutions Architect, Medical Consultant, Chief Financial Officer (CFO), or Executive Engineer.</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Section 12: Live Placement Compass Matching Jobs -->
    <div class="card border-0 shadow-sm p-4 mb-4 rounded-4 bg-white border-start border-4 border-success">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <div>
          <h5 class="fw-bold text-dark mb-0">💼 10. Live Matching Jobs in Placement Compass</h5>
          <small class="text-muted">Instant matching positions currently open for candidates with this educational profile.</small>
        </div>
        <span class="badge bg-success text-white rounded-pill px-3 py-1 fw-bold">Live Hiring</span>
      </div>
      <div class="row g-3">
        ${matchingJobsHtml}
      </div>
    </div>

    <!-- Entrance Exams Accordion -->
    <div class="card border-0 shadow-sm p-4 mb-3 rounded-4 bg-white">
      <h5 class="fw-bold text-dark mb-2">🎯 11. Required Entrance Exams &amp; Single-Window Portals</h5>
      ${examsHtml}
      <div class="p-3 bg-light border rounded-3 text-secondary small mt-2" style="line-height: 1.7;">
        <strong>Admission Procedure:</strong> ${path.admission_procedure}
      </div>
    </div>
  `;
}

function addCurrentModalPathToCompare() {
  if (currentModalPathId) {
    const cr1 = document.getElementById("course-select-1");
    if (cr1) {
      if (allComparableCourses && allComparableCourses.length > 0) {
        const matchCr = allComparableCourses.find(c => c.id === currentModalPathId || c.category === (allSchoolPaths.find(p => p.id === currentModalPathId)?.category));
        if (matchCr) {
          cr1.value = matchCr.id;
          runCourseComparison();
        }
      }
    }
    const modalEl = document.getElementById("pathwayDetailModal");
    const modalInstance = bootstrap.Modal.getInstance(modalEl);
    if (modalInstance) modalInstance.hide();
    switchSchoolTab("courses");
    document.getElementById("school-tab-courses")?.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}
window.addCurrentModalPathToCompare = addCurrentModalPathToCompare;


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

  if (!allSchoolExams || allSchoolExams.length === 0) {
    if (typeof window !== "undefined" && window.COMPASS_STATIC_DATA && window.COMPASS_STATIC_DATA.exams) {
      allSchoolExams = window.COMPASS_STATIC_DATA.exams;
    }
  }

  // Sanity check: Ensure activeExamStageFilter matches activeAcademicGroup
  if (activeAcademicGroup === "sslc_10th") {
    activeExamStageFilter = "after_10th";
  } else if (activeAcademicGroup && activeAcademicGroup !== "all" && activeExamStageFilter === "after_10th") {
    activeExamStageFilter = "after_12th";
  }

  // Update #exam-stage-filter-btns button visual states
  document.querySelectorAll("#exam-stage-filter-btns button").forEach((b) => {
    const bStage = b.getAttribute("data-exam-stage");
    const isTarget = (activeAcademicGroup === "sslc_10th") ? (bStage === "after_10th") : (bStage === activeExamStageFilter);
    if (isTarget) {
      b.classList.remove("btn-outline-primary");
      b.classList.add("btn-primary", "shadow-sm");
    } else {
      b.classList.remove("btn-primary", "shadow-sm");
      b.classList.add("btn-outline-primary");
    }
  });

  let filtered = allSchoolExams || [];

  // 1. Group Filtering (Computer Science vs Biology vs Commerce vs Arts vs Vocational vs 10th)
  if (activeAcademicGroup && activeAcademicGroup !== "all") {
    filtered = filtered.filter((e) => {
      const groups = (e.target_groups || []).map((g) => g.toLowerCase());
      return groups.includes(activeAcademicGroup.toLowerCase());
    });
  }

  // 2. Stage Filtering (After 10th vs After 12th)
  if (activeAcademicGroup === "sslc_10th") {
    filtered = filtered.filter((e) => e.target_stage === "after_10th");
  } else if (activeExamStageFilter === "after_10th") {
    filtered = filtered.filter((e) => e.target_stage === "after_10th");
  } else if (activeExamStageFilter === "after_12th") {
    filtered = filtered.filter((e) => e.target_stage === "after_12th");
  }

  // 3. Fallback Auto-Heal: If zero exams resulted from a stage filter mismatch with the selected group
  if ((!filtered || filtered.length === 0) && activeAcademicGroup && activeAcademicGroup !== "all") {
    if (activeAcademicGroup === "sslc_10th") {
      filtered = (allSchoolExams || []).filter((e) => {
        const groups = (e.target_groups || []).map((g) => g.toLowerCase());
        return groups.includes("sslc_10th") || e.target_stage === "after_10th";
      });
      activeExamStageFilter = "after_10th";
    } else {
      const groupMatches = (allSchoolExams || []).filter((e) => {
        const groups = (e.target_groups || []).map((g) => g.toLowerCase());
        return groups.includes(activeAcademicGroup.toLowerCase());
      });
      if (groupMatches.length > 0) {
        filtered = groupMatches;
        activeExamStageFilter = "after_12th";
      }
    }
    document.querySelectorAll("#exam-stage-filter-btns button").forEach((b) => {
      if (b.getAttribute("data-exam-stage") === activeExamStageFilter) {
        b.classList.remove("btn-outline-primary");
        b.classList.add("btn-primary", "shadow-sm");
      } else {
        b.classList.remove("btn-primary", "shadow-sm");
        b.classList.add("btn-outline-primary");
      }
    });
  }

  // Update count badge
  const countBadge = document.getElementById("active-group-count-badge");
  if (countBadge) {
    countBadge.textContent = `${filtered.length} Exams Available`;
  }

  if (!filtered || filtered.length === 0) {
    container.innerHTML = `
      <div class="col-12 text-center py-5 bg-white rounded-4 border">
        <div class="fs-1 mb-2">📋</div>
        <h6 class="fw-bold text-dark">No entrance exams found for this group.</h6>
        <p class="text-muted small mb-0">Switch your selected academic group above to see exams.</p>
        <button class="btn btn-sm btn-outline-primary rounded-pill px-4 mt-3 fw-bold" onclick="filterExamsByAcademicGroup('all', null)">
          🌐 Show All Groups
        </button>
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
          : `<span class="badge bg-primary bg-opacity-25 text-primary-emphasis fw-bold rounded-pill small px-2.5 py-1">🎓 12th Grade (HSC)</span>`;

        const groupTag = e.group_badge
          ? `<span class="badge bg-light text-primary border small rounded-pill fw-semibold">${e.group_badge}</span>`
          : "";

        const calBtn = e.google_calendar_url
          ? `<a href="${e.google_calendar_url}" target="_blank" rel="noopener noreferrer" class="btn btn-outline-danger btn-sm rounded-pill fw-bold d-flex align-items-center justify-content-center gap-2 shadow-sm">
              <span>📅</span> Sync to Google Calendar
            </a>`
          : `<div class="text-center small text-muted py-1 fw-semibold border rounded-pill bg-light">
              <span>🔔</span> Dates published officially post-Board results
            </div>`;

        const cleanDomain = e.official_url ? e.official_url.replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0] : "tn.gov.in";

        // Positions Badges (Up to 4)
        const positionsList = (e.career_positions || []).slice(0, 4);
        const positionsHtml = positionsList.length > 0
          ? `
            <div class="mb-2.5 p-2.5 bg-primary bg-opacity-10 border border-primary-subtle rounded-3">
              <div class="small fw-bold text-primary mb-1.5 d-flex align-items-center gap-1">
                <span>💼</span> Target Positions &amp; Career Opportunities:
              </div>
              <div class="d-flex flex-wrap gap-1">
                ${positionsList.map((p) => `<span class="badge bg-white text-dark border small fw-semibold py-1 px-2 rounded-pill shadow-xs">${p}</span>`).join("")}
              </div>
            </div>
          `
          : "";

        const salaryHtml = e.average_salary_package
          ? `<div class="small mb-1"><strong class="text-success">💰 Avg Starting Package:</strong> <span class="fw-bold text-success">${e.average_salary_package}</span></div>`
          : "";

        const collegesHtml = (e.top_colleges_tn && e.top_colleges_tn.length > 0)
          ? `<div class="small mb-1"><strong class="text-dark">🏛️ Top TN Campuses:</strong> <span class="text-secondary">${e.top_colleges_tn.slice(0, 3).join(", ")}</span></div>`
          : "";

        const perksHtml = e.tn_quota_perks
          ? `<div class="p-2 bg-warning bg-opacity-10 border border-warning-subtle rounded-3 small mb-2 text-dark">
              <strong>🌟 Tamil Nadu Perks &amp; Quotas:</strong> ${e.tn_quota_perks}
            </div>`
          : "";

        const schedule = e.exam_schedule_breakdown || {};
        const counsellingHtml = schedule.counselling_schedule
          ? `<div class="fw-semibold text-secondary mb-1">
              <strong>🏆 Counselling / Results:</strong> <span class="text-dark">${schedule.counselling_schedule}</span>
            </div>`
          : "";

        return `
      <div class="col-md-6 col-lg-4">
        <div class="card border-0 shadow-sm p-4 rounded-4 bg-white h-100 d-flex flex-column transition-all hover-shadow">
          <div class="d-flex justify-content-between align-items-start gap-2 mb-2">
            <div>
              <div class="d-flex gap-1 flex-wrap mb-1">${stageBadge} ${admissionBadge}</div>
              <h5 class="fw-bold text-dark mb-1" style="font-size: 1.05rem;">${e.exam_name}</h5>
              <div class="mb-1">${groupTag}</div>
            </div>
          </div>

          <div class="small text-muted mb-2">
            <strong>🏛️ Conducting Body:</strong> <span class="text-secondary">${e.conducting_body}</span>
          </div>

          <!-- Exam Dates & Schedule Box -->
          <div class="p-3 bg-light rounded-3 mb-2 small border">
            <div class="fw-semibold text-secondary mb-1.5">
              <strong class="text-dark">🎓 Degree Courses:</strong> <span class="text-dark">${e.target_courses.join(", ")}</span>
            </div>
            <div class="fw-semibold text-danger mb-1.5">
              <strong>⏳ Application Window:</strong> <span>${e.registration_start} &rarr; ${e.registration_deadline}</span>
            </div>
            <div class="fw-semibold text-primary mb-1.5">
              <strong>🗓️ Examination Date(s):</strong> <span>${e.exam_date}</span>
            </div>
            ${counsellingHtml}
            <div class="text-muted">
              <strong>🎓 Eligibility:</strong> <span class="text-dark">${e.eligibility_summary}</span>
            </div>
          </div>

          <!-- Career Opportunities & Positions -->
          ${positionsHtml}
          ${salaryHtml}
          ${collegesHtml}
          ${perksHtml}

          <p class="small text-secondary mb-3 flex-grow-1">
            <strong>Key Process / Syllabus:</strong> ${e.syllabus_highlights}
          </p>

          <div class="d-flex flex-column gap-2 pt-2 border-top mt-auto">
            ${calBtn}
            <a href="${e.official_url}" target="_blank" rel="noopener noreferrer" class="btn btn-outline-primary btn-sm rounded-pill fw-semibold text-center shadow-sm">
              🔗 Official Portal (${cleanDomain})
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
// 7. ACADEMIC GROUP FILTERING (COMPUTER SCIENCE vs BIOLOGY etc)
// -------------------------------------------------------------

function filterExamsByAcademicGroup(group, btn) {
  activeAcademicGroup = group || "all";

  // Smart Synchronize with Stage Filter:
  // If 10th standard SSLC is picked, stage filter becomes "after_10th"
  // If any 12th group is picked, stage filter becomes "after_12th"
  // If "all" is picked, stage filter becomes "all"
  if (activeAcademicGroup === "sslc_10th") {
    activeExamStageFilter = "after_10th";
  } else if (activeAcademicGroup !== "all") {
    activeExamStageFilter = "after_12th";
  } else {
    activeExamStageFilter = "all";
  }

  // Update #exam-stage-filter-btns button visual states
  document.querySelectorAll("#exam-stage-filter-btns button").forEach((b) => {
    if (b.getAttribute("data-exam-stage") === activeExamStageFilter) {
      b.classList.remove("btn-outline-primary");
      b.classList.add("btn-primary", "shadow-sm");
    } else {
      b.classList.remove("btn-primary", "shadow-sm");
      b.classList.add("btn-outline-primary");
    }
  });

  // Update #btn-12th-only-toggle button visual state
  const btn12 = document.getElementById("btn-12th-only-toggle");
  if (btn12) {
    if (activeExamStageFilter === "after_12th") {
      btn12.classList.remove("btn-outline-primary");
      btn12.classList.add("btn-primary", "shadow-sm");
    } else {
      btn12.classList.remove("btn-primary", "shadow-sm");
      btn12.classList.add("btn-outline-primary");
    }
  }

  // Update button active states
  document.querySelectorAll("#exam-academic-group-selector .academic-group-btn").forEach((b) => {
    if (b.getAttribute("data-group") === activeAcademicGroup) {
      b.classList.add("active");
    } else {
      b.classList.remove("active");
    }
  });

  // Update Banner Content
  const iconEl = document.getElementById("active-group-icon");
  const titleEl = document.getElementById("active-group-title");
  const descEl = document.getElementById("active-group-desc");
  const headingEl = document.getElementById("exams-section-heading");
  const subHeadingEl = document.getElementById("exams-section-subheading");

  const groupInfo = {
    computer_science: {
      icon: "💻",
      title: "Showing Engineering & Technology Entrance Exams for: 12th Computer Science & Maths Group",
      desc: "Displaying exclusively JEE Main, JEE Advanced, TNEA (Anna University), BITSAT, NATA Architecture, Navy 10+2 B.Tech Cadet Scheme, and UPSC NDA. Unlocks Software Engineer, AI/ML Specialist, Systems Architect, VLSI, and Defence Officer careers. Medical exams (NEET-UG) are strictly hidden.",
      heading: "💻 Engineering & Technology Entrance Exams (JEE, TNEA, BITSAT, NATA, Navy Cadet)",
      subheading: "Only entrance exams and single-window counselling portals open to Computer Science & Maths stream students."
    },
    biology: {
      icon: "🧬",
      title: "Showing Healthcare, Medical & Life Sciences Entrance Exams for: 12th Biology / Pure Science Group",
      desc: "Displaying exclusively NEET-UG (MBBS/BDS TN DME 85% Quota), Paramedical & B.Sc Nursing, TANUVAS Veterinary (BVSc & AH), TNAU Agriculture (B.Sc Agri), and TN B.Pharm. Unlocks Doctor, Dental Surgeon, Veterinary Surgeon, Agricultural Officer, and Clinical Specialist positions. Engineering exams (JEE/TNEA) are strictly hidden.",
      heading: "🧬 Medical, Dental, Veterinary & Agri Entrance Exams (NEET-UG, TANUVAS, TNAU, Nursing)",
      subheading: "Only medical, nursing, paramedical, veterinary, and agriculture admission channels open to Biology students."
    },
    commerce: {
      icon: "📊",
      title: "Showing Professional Finance, Accounting & Corporate Law Exams for: 12th Commerce Group",
      desc: "Displaying exclusively ICAI CA Foundation, ICMAI CMA Foundation, ICSI CSEET, TNGASA Commerce, and TNDALU B.Com. LL.B. Unlocks Chartered Accountant (CA), Cost Accountant, Company Secretary, Financial Analyst, and Investment Banker positions.",
      heading: "📊 Professional Commerce, Chartered Accountancy & Finance Exams (CA, CMA, CS, B.Com)",
      subheading: "National professional qualifications and university admission streams open to Commerce students."
    },
    arts: {
      icon: "📚",
      title: "Showing Law, Humanities, Civil Services & Design Exams for: 12th Arts & Humanities Group",
      desc: "Displaying exclusively TNDALU 5-Year Law, CLAT-UG (TNNLU Trichy), TNGASA Arts, NIFT Fashion Design, and UPSC NDA Army. Unlocks High Court Advocate, Civil Services (IAS/IPS), Fashion Designer, Policy Analyst, and Journalist positions.",
      heading: "📚 Arts, Humanities, Law & Design Entrance Exams (TNDALU Law, CLAT, NIFT, TNGASA)",
      subheading: "Single-window admissions and competitive exams open to Humanities & Arts stream students."
    },
    vocational: {
      icon: "⚙️",
      title: "Showing Lateral Entry & Technical Single-Window Admissions for: 12th Vocational HSC Stream",
      desc: "Displaying exclusively DOTE Lateral Entry Polytechnic Admissions and TNEA Vocational Engineering Quota. Unlocks Junior QA Engineer, Shop Floor Supervisor, and Direct B.E Degree seats.",
      heading: "⚙️ Vocational & Technical Single-Window Admissions (DOTE Lateral & TNEA Vocational)",
      subheading: "Direct 2nd year polytechnic lateral entry and specialized government technical admissions."
    },
    sslc_10th: {
      icon: "📘",
      title: "Showing Admissions & Recruitment Exams After: 10th Standard (SSLC Pass)",
      desc: "Displaying exclusively DOTE 3-Year Polytechnic, DET ITI, TNPSC Group 4 & VAO, and TNUSRB Police Constable.",
      heading: "📘 Direct Higher Education & Recruitment Exams After 10th Standard",
      subheading: "Government polytechnic diplomas, technical trade certifications, and permanent state public services."
    },
    all: {
      icon: "🌐",
      title: "Showing All Higher Education Entrance Exams for: 12th Grade Students",
      desc: "Select your specific 12th-grade academic group above (Computer Science, Biology, Commerce, Arts, or Vocational) to filter exclusively to your eligible exams and career positions.",
      heading: "📅 12th Grade Entrance Exams & Career Gateways (All Streams)",
      subheading: "Official registration windows, syllabus blueprints, and 1-click Google Calendar sync across all streams."
    }
  };

  const info = groupInfo[activeAcademicGroup] || groupInfo["all"];
  if (iconEl) iconEl.textContent = info.icon;
  if (titleEl) titleEl.textContent = info.title;
  if (descEl) descEl.textContent = info.desc;
  if (headingEl) headingEl.textContent = info.heading;
  if (subHeadingEl) subHeadingEl.textContent = info.subheading;

  // Sync position sector filter to match chosen group
  const sectorMap = {
    computer_science: "Engineering & Technology",
    biology: "Medical & Healthcare",
    commerce: "Banking, Finance & Commerce",
    arts: "Law & Judiciary"
  };
  if (sectorMap[activeAcademicGroup]) {
    activePosSectorFilter = sectorMap[activeAcademicGroup];
    const sectorSelect = document.getElementById("position-sector-select");
    if (sectorSelect) sectorSelect.value = sectorMap[activeAcademicGroup];
  } else if (activeAcademicGroup === "all") {
    activePosSectorFilter = "all";
    const sectorSelect = document.getElementById("position-sector-select");
    if (sectorSelect) sectorSelect.value = "all";
  }

  renderSchoolExams();
  renderCareerPositions();
}

function filterExamsByGradeStage(stage, btn) {
  activeExamStageFilter = stage;
  if (stage === "after_12th" && activeAcademicGroup === "sslc_10th") {
    activeAcademicGroup = "computer_science";
  }

  const btn12 = document.getElementById("btn-12th-only-toggle");
  if (btn12) {
    if (stage === "after_12th") {
      btn12.classList.remove("btn-outline-primary");
      btn12.classList.add("btn-primary", "shadow-sm");
    } else {
      btn12.classList.remove("btn-primary", "shadow-sm");
      btn12.classList.add("btn-outline-primary");
    }
  }

  document.querySelectorAll("#exam-academic-group-selector .academic-group-btn").forEach((b) => {
    if (b.getAttribute("data-group") === activeAcademicGroup) {
      b.classList.add("active");
    } else {
      b.classList.remove("active");
    }
  });

  filterExamsByAcademicGroup(activeAcademicGroup);
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

  // Filter by academic group
  if (activeAcademicGroup && activeAcademicGroup !== "all") {
    filtered = filtered.filter((p) => {
      if (p.target_group && p.target_group.toLowerCase() === activeAcademicGroup.toLowerCase()) {
        return true;
      }
      const pGroups = (p.target_groups || []).map((g) => g.toLowerCase());
      return pGroups.includes(activeAcademicGroup.toLowerCase());
    });
  }

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
  activeAcademicGroup = "all";

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

  document.querySelectorAll(".academic-group-btn").forEach((btn) => {
    if (btn.getAttribute("data-academic-group") === "all") {
      btn.classList.add("active");
    } else {
      btn.classList.remove("active");
    }
  });

  renderSchoolExams();
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
