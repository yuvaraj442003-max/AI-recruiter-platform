/**
 * placement-compass-section.js
 * Dedicated Controller & Knowledge Base for the Placement Compass Section on the Homepage / Main Portals.
 * Organizes career guidance and related job opportunities strictly by educational qualification:
 * - 10th Standard (SSLC)
 * - 12th Science (PCM / Maths)
 * - 12th Science (PCB / Biology)
 * - 12th Commerce & Accountancy
 * - 12th Arts & Humanities
 * - Polytechnic / Diploma (DOTE)
 * - Undergraduate (B.E / B.Tech / B.Sc / BCA / B.Com)
 */

(function () {
  "use strict";

  const QUALIFICATION_CAREER_MAP = {
    sslc_10th: {
      id: "sslc_10th",
      title: "Completed 10th Standard (SSLC)",
      badge: "📘 5 Distinct Routes in Tamil Nadu",
      icon: "📘",
      theme_color: "#0284c7",
      short_desc: "Choose between 11th & 12th HSC streams, 3-Year Polytechnic Engineering Diplomas, 2-Year ITI Trades, Paramedical Diplomas, or Direct Tamil Nadu Government Jobs.",
      eligibility: "10th Standard (SSLC) Pass from TN State Board, Matriculation, CBSE, or ICSE",
      duration: "1 to 3 Years depending on route",
      starting_salary: "₹2.4 LPA - ₹5.8 LPA",
      senior_salary: "₹6.5 LPA - ₹14.0 LPA",
      portal_name: "DOTE Tamil Nadu & TNPSC",
      portal_url: "https://www.dte.tn.gov.in",
      popular_courses: [
        "3-Year Polytechnic Diploma (Civil, Mech, EEE, ECE, CSE)",
        "2-Year ITI Electrician & Fitter (NCVT Certified)",
        "11th Higher Secondary Bio-Maths / Computer Science",
        "TN DME Paramedical Diplomas (DMLT, Health Inspector)",
        "Direct TNPSC Group 4 & VAO Recruitment"
      ],
      job_opportunities: [
        {
          id: "job_10th_je_diploma",
          title: "Junior Engineer (JE) / Technical Supervisor",
          icon: "🔧",
          sector: "Engineering & Technical Services",
          type: "public",
          starting_salary: "₹3.5 LPA - ₹6.5 LPA",
          senior_salary: "₹8.0 LPA - ₹16.0 LPA",
          description: "Supervises shop floor production, field electrical grids, civil construction sites, and mechanical maintenance in manufacturing plants and state public utilities.",
          hiring_companies: ["TANGEDCO", "TN PWD", "L&T Construction", "Ashok Leyland", "Hyundai Motor", "TVS Motors"],
          key_skills: ["AutoCAD", "PLC / SCADA", "Site Supervision", "Blueprint Reading", "Industrial Safety"],
          progression: "Junior Diploma Engineer → Assistant Engineer (AE) → Executive Engineer",
          gateway: "DOTE 3-Year Polytechnic Diploma → Direct Lateral B.E or TNPSC Combined Technical Exams",
          perks: "Direct lateral entry to 2nd-year B.E / B.Tech at Anna University after 3-year diploma."
        },
        {
          id: "job_10th_vao",
          title: "Village Administrative Officer (VAO)",
          icon: "🏛️",
          sector: "State Revenue Administration",
          type: "public",
          starting_salary: "₹3.2 LPA (TN Pay Matrix Level 10 + DA + HRA)",
          senior_salary: "₹8.5 LPA - ₹14.0 LPA",
          description: "Administrative head of a revenue village in Tamil Nadu, managing land patta records, village revenue collection, caste/income certificates, and disaster relief.",
          hiring_companies: ["Revenue & Disaster Management Dept", "Government of Tamil Nadu", "District Collectorates"],
          key_skills: ["Tamil Drafting", "Revenue Land Rules", "Panchayat Administration", "Public Service"],
          progression: "VAO → Revenue Inspector (RI) → Deputy Tahsildar → Tahsildar",
          gateway: "TNPSC Group 4 & VAO Examination (Single Written Exam, Direct 10th Standard Merit)",
          perks: "100% permanent Government of Tamil Nadu job with pension, job security, and official quarters."
        },
        {
          id: "job_10th_junior_asst",
          title: "Junior Assistant / Typist / Bill Collector",
          icon: "📝",
          sector: "Tamil Nadu Ministerial Services",
          type: "public",
          starting_salary: "₹3.0 LPA (TN Pay Matrix Level 8 + Allowances)",
          senior_salary: "₹7.5 LPA - ₹12.0 LPA",
          description: "Maintains government administrative records, office files, treasury vouchers, and citizen applications across Tamil Nadu Secretariat and district offices.",
          hiring_companies: ["TN Secretariat", "Judicial Ministerial Services", "Registration Dept", "High Court Chambers"],
          key_skills: ["Computer On Office Automation (COA)", "Tamil/English Typewriting", "File Maintenance"],
          progression: "Junior Assistant → Assistant → Superintendent → Under Secretary",
          gateway: "TNPSC Group 4 Examination (Held annually for 7,000+ vacancies across Tamil Nadu)",
          perks: "Direct government employment after 10th standard; eligible for departmental promotional exams."
        },
        {
          id: "job_10th_police_constable",
          title: "Grade II Police Constable / Fireman / Jail Warder",
          icon: "🎖️",
          sector: "Uniformed Public Services",
          type: "public",
          starting_salary: "₹3.2 LPA + Risk Allowance + Uniform Allowance",
          senior_salary: "₹8.0 LPA - ₹15.0 LPA",
          description: "Enforces law and order, manages security patrolling, executes emergency disaster rescue operations, and guards correctional institutions across Tamil Nadu.",
          hiring_companies: ["Tamil Nadu Police (Law & Order / Armed Reserve)", "Fire & Rescue Services", "Prisons Dept"],
          key_skills: ["Physical Endurance", "Tamil Comprehension", "Emergency Rescue", "First Aid"],
          progression: "Police Constable Grade II → Grade I → Head Constable → Special Sub-Inspector (SSI)",
          gateway: "TNUSRB Common Recruitment (Written Exam + Physical Efficiency Test / Endurance Test)",
          perks: "Comprehensive health insurance, free government accommodation, ration allowances."
        },
        {
          id: "job_10th_iti_electrician",
          title: "Skilled Industrial Technician & Electrician / CNC Machinist",
          icon: "🛠️",
          sector: "Automotive & Manufacturing Hubs",
          type: "corporate",
          starting_salary: "₹2.8 LPA - ₹5.5 LPA + Overtime & Performance Bonus",
          senior_salary: "₹6.5 LPA - ₹11.5 LPA",
          description: "Operates high-precision CNC multi-axis machines, maintains industrial electrical switchgear, performs robotic welding, and supervises quality inspections.",
          hiring_companies: ["Maruti Suzuki", "Royal Enfield", "Tata Electronics Hosur", "Saint-Gobain", "Foxconn Sriperumbudur"],
          key_skills: ["CNC Programming", "Wiring Schematics", "Industrial Electrical Maintenance", "Pneumatics"],
          progression: "Technician Trainee → Senior Machine Operator → Maintenance Head",
          gateway: "Tamil Nadu DET ITI Admission (2-Year NCVT Certified National Trade Certificate)",
          perks: "Immediate employment in Sriperumbudur, Oragadam, Coimbatore, and Hosur industrial corridors."
        }
      ]
    },

    computer_science: {
      id: "computer_science",
      title: "12th Science (PCM / Computer Science)",
      badge: "💻 Engineering, AI, Cloud & Defence",
      icon: "💻",
      theme_color: "#6366f1",
      short_desc: "Designed for analytical and problem-solving students. Unlocks premier B.E / B.Tech degrees (Anna University CEG/MIT, IIT Madras, PSG Tech), AI/ML engineering, software architecture, semiconductor VLSI, and armed forces technical cadet schemes.",
      eligibility: "12th Standard Pass with Physics, Chemistry & Mathematics (PCM)",
      duration: "4 Years (B.E/B.Tech) / 3 Years (B.Sc Tech)",
      starting_salary: "₹5.5 LPA - ₹28.0 LPA",
      senior_salary: "₹22.0 LPA - ₹65.0+ LPA",
      portal_name: "TNEA (Anna University) — tneaonline.org",
      portal_url: "https://www.tneaonline.org",
      popular_courses: [
        "B.E / B.Tech Computer Science & Engineering (CSE)",
        "B.Tech Artificial Intelligence & Data Science (AI & DS)",
        "B.E Electronics & Communication Engineering (ECE / VLSI)",
        "B.Tech Information Technology & Cyber Security",
        "B.Arch — Bachelor of Architecture (5 Years via NATA)",
        "Indian Navy 10+2 B.Tech Cadet Scheme (100% Free Scholarship)"
      ],
      job_opportunities: [
        {
          id: "job_cs_sde",
          title: "Software Development Engineer (SDE) / Cloud Architect",
          icon: "💻",
          sector: "Software, Cloud & Internet Products",
          type: "tech",
          starting_salary: "₹6.0 LPA - ₹24.0 LPA",
          senior_salary: "₹25.0 LPA - ₹60.0+ LPA",
          description: "Architects scalable microservices, builds full-stack web platforms, designs resilient cloud infrastructures (AWS/GCP), and optimizes distributed high-performance backend pipelines.",
          hiring_companies: ["Zoho", "Google", "Amazon", "Microsoft", "Freshworks", "TCS Digital", "Infosys", "Kaar Tech"],
          key_skills: ["Data Structures & Algorithms", "Java / Python / Golang", "AWS / Docker", "System Design", "SQL & NoSQL"],
          progression: "SDE I → SDE II → Senior Software Engineer → Technical Lead → Principal Solutions Architect",
          gateway: "TNEA Engineering Counselling / Anna University Placements / TCS NQT / Direct Corporate Drives",
          perks: "Top engineering packages in Chennai OMR IT Corridor and Coimbatore IT SEZs."
        },
        {
          id: "job_cs_aiml",
          title: "AI / Machine Learning Engineer & Data Scientist",
          icon: "🧠",
          sector: "Artificial Intelligence & Analytics",
          type: "tech",
          starting_salary: "₹7.5 LPA - ₹28.0 LPA",
          senior_salary: "₹30.0 LPA - ₹75.0+ LPA",
          description: "Develops deep learning models, fine-tunes generative AI architectures (LLMs), trains computer vision pipelines, and deploys predictive intelligence systems in production.",
          hiring_companies: ["PayPal", "Tiger Analytics", "LatentView", "Zoho AI Labs", "Intel Labs", "Cognizant AI"],
          key_skills: ["PyTorch / TensorFlow", "Generative AI & LLMs", "Python", "Vector Databases", "MLOps"],
          progression: "Junior Data Scientist → Machine Learning Engineer → Head of AI Research",
          gateway: "B.Tech CSE (AI & DS) / M.Tech AI via GATE / Campus Placement",
          perks: "Highest starting salary multiplier among all engineering graduates."
        },
        {
          id: "job_cs_vlsi",
          title: "Semiconductor VLSI Design & Embedded Systems Engineer",
          icon: "⚡",
          sector: "Semiconductors & Hardware Systems",
          type: "tech",
          starting_salary: "₹5.5 LPA - ₹18.0 LPA",
          senior_salary: "₹20.0 LPA - ₹48.0 LPA",
          description: "Designs ultra-low power integrated microchips, synthesizes RTL code using Verilog/VHDL, and builds automotive embedded controllers for 5G telecommunication hardware.",
          hiring_companies: ["Qualcomm", "Texas Instruments", "Synopsys", "L&T Technology Services", "Tata Electronics"],
          key_skills: ["Verilog / SystemVerilog", "FPGA Synthesis", "Embedded C", "Microcontrollers", "ASIC Design"],
          progression: "Design Engineer → Senior VLSI Architect → Chipset Engineering Manager",
          gateway: "B.E ECE / EEE via TNEA Single Window (CEG Campus, MIT Chromepet, PSG Tech)",
          perks: "Surging demand in Sriperumbudur Electronics SEZ and Tamil Nadu Semiconductor Corridor."
        },
        {
          id: "job_cs_defence_officer",
          title: "Commissioned Technical Officer (Indian Army / Navy / Air Force)",
          icon: "🎖️",
          sector: "Armed Forces & Defence Research",
          type: "public",
          starting_salary: "₹14.0 LPA (Level 10 Pay Matrix + MSP + Rations + Housing)",
          senior_salary: "₹28.0 LPA - ₹45.0 LPA",
          description: "Commands cutting-edge missile radar guidance systems, naval warships, fighter aircraft avionics, and military cybersecurity operations for the nation.",
          hiring_companies: ["Indian Navy", "Indian Army", "Indian Air Force", "DRDO Labs", "ISRO Satellite Centre"],
          key_skills: ["Military Leadership", "Naval Engineering", "Avionics", "Radar Operations", "Tactical Defence"],
          progression: "Sub Lieutenant / Lieutenant → Commander / Colonel → Flag Officer / Admiral",
          gateway: "Indian Navy 10+2 B.Tech Cadet Scheme (100% Free Scholarship at INA Ezhimala) / UPSC NDA Exam",
          perks: "100% free B.Tech education, prestigious Gazetted Officer rank, government bungalow, medical coverage."
        }
      ]
    },

    biology: {
      id: "biology",
      title: "12th Science (PCB / Biology)",
      badge: "🧬 Medical, Healthcare, Veterinary & Agriculture",
      icon: "🧬",
      theme_color: "#10b981",
      short_desc: "Structured for students aspiring to clinical healing, surgical medicine, veterinary sciences, and sustainable agricultural development. Unlocks MBBS/BDS in Tamil Nadu's 38+ Government Medical Colleges, TANUVAS, TNAU, and premier paramedical institutions.",
      eligibility: "12th Standard Pass with Physics, Chemistry & Biology (Botany & Zoology)",
      duration: "4.5 to 5.5 Years (MBBS/BVSc) / 4 Years (Agri/Pharm)",
      starting_salary: "₹6.0 LPA - ₹18.0 LPA",
      senior_salary: "₹20.0 LPA - ₹55.0+ LPA",
      portal_name: "TN Medical Selection & TANUVAS / TNAU",
      portal_url: "https://www.tnmedicalselection.net",
      popular_courses: [
        "MBBS — Bachelor of Medicine & Bachelor of Surgery (5.5 Years)",
        "BDS — Bachelor of Dental Surgery (5 Years)",
        "B.V.Sc & A.H — Veterinary Science (TANUVAS Madras Veterinary College)",
        "B.Sc (Hons) Agriculture / Horticulture (TNAU Coimbatore)",
        "B.Pharm — Bachelor of Pharmacy (4 Years)",
        "B.Sc Nursing & Allied Health Sciences (DMLT, Radiography, Perfusion)"
      ],
      job_opportunities: [
        {
          id: "job_bio_doctor",
          title: "Medical Doctor / General Physician & Surgeon (MBBS)",
          icon: "🩺",
          sector: "Clinical Medicine & Hospital Healthcare",
          type: "healthcare",
          starting_salary: "₹8.0 LPA - ₹18.0 LPA",
          senior_salary: "₹24.0 LPA - ₹65.0+ LPA",
          description: "Diagnoses clinical diseases, performs surgical operations, directs critical care units, and manages comprehensive patient treatments across primary healthcare centres and quaternary hospitals.",
          hiring_companies: ["Madras Medical College (MMC)", "Stanley Hospital", "Apollo Hospitals", "Fortis", "TN Dept of Health"],
          key_skills: ["Clinical Diagnosis", "Pharmacology", "Emergency Trauma Care", "Patient Consultation", "Surgical Protocols"],
          progression: "Junior Resident Doctor → Senior Medical Officer → Specialist Consultant → Medical Superintendent",
          gateway: "NEET-UG Exam → Tamil Nadu Medical Selection (85% State Quota across 38+ Govt Medical Colleges)",
          perks: "7.5% Tamil Nadu Govt School Quota offers 100% free tuition, hostel, and food fees."
        },
        {
          id: "job_bio_vet_surgeon",
          title: "Veterinary Surgeon / Animal Husbandry Officer (B.V.Sc & AH)",
          icon: "🐾",
          sector: "Veterinary Medicine & Livestock Governance",
          type: "public",
          starting_salary: "₹7.2 LPA (TNPSC VAS Gazetted Officer Pay + Allowances)",
          senior_salary: "₹18.0 LPA - ₹32.0 LPA",
          description: "Provides medical and surgical care for companion and dairy animals, supervises livestock genetics, controls zoonotic diseases, and inspects public veterinary dispensaries.",
          hiring_companies: ["TN Animal Husbandry Dept", "Madras Veterinary College", "Aavin Dairy", "Zoological Parks", "Dairy MNCs"],
          key_skills: ["Animal Surgery", "Veterinary Pharmacology", "Livestock Management", "Epidemiology"],
          progression: "Veterinary Assistant Surgeon (VAS) → Assistant Director → Joint Director of Animal Husbandry",
          gateway: "TANUVAS Single Window Counselling (Direct 12th Cutoff Merit out of 200, No Entrance Exam)",
          perks: "Direct recruitment as State Gazetted Officer via TNPSC; very high veterinary clinic private practice income."
        },
        {
          id: "job_bio_agri_officer",
          title: "Agricultural Officer (AO) / Farm Research Scientist",
          icon: "🌾",
          sector: "Agricultural Science & Rural Development",
          type: "public",
          starting_salary: "₹5.5 LPA - ₹10.5 LPA",
          senior_salary: "₹14.0 LPA - ₹25.0 LPA",
          description: "Implements sustainable soil health schemes, introduces high-yield drought-resistant crop hybrids, manages organic fertilizers, and inspects seed testing laboratories.",
          hiring_companies: ["TN Agriculture Dept", "TNAU Coimbatore", "NABARD", "ITC Agri Business", "Bayer Crop Science"],
          key_skills: ["Agronomy", "Soil Science", "Plant Pathology", "Precision Agriculture", "Crop Protection"],
          progression: "Agricultural Officer (AO) → Assistant Director of Agriculture (ADA) → Joint Director of Agriculture",
          gateway: "TNAU Single Window Counselling (12th Board Cutoff out of 200) → TNPSC Agricultural Officer Exam",
          perks: "Respected state government service with field allowances, government vehicle, and pension benefits."
        },
        {
          id: "job_bio_clinical_pharmacist",
          title: "Clinical Pharmacist / Drug Inspector (B.Pharm)",
          icon: "💊",
          sector: "Pharmaceuticals & Biotechnology",
          type: "healthcare",
          starting_salary: "₹4.5 LPA - ₹9.0 LPA",
          senior_salary: "₹12.0 LPA - ₹26.0 LPA",
          description: "Formulates new pharmaceutical medicines, inspects pharmaceutical manufacturing plants for regulatory compliance, and manages clinical trials in Chennai pharma hubs.",
          hiring_companies: ["Sun Pharma", "Dr. Reddy's", "Pfizer", "TN Drugs Control Dept", "Apollo Pharmacies"],
          key_skills: ["Pharmaceutics", "Medicinal Chemistry", "Regulatory Compliance (FDA/CDSCO)", "Clinical Trials"],
          progression: "Formulation Pharmacist → Quality Assurance Manager → Government Drug Inspector",
          gateway: "Tamil Nadu Paramedical Counselling (Direct 12th Cutoff) → Drug Inspector Exam via TNPSC",
          perks: "State regulatory powers as Drug Inspector; eligible to establish licensed retail and wholesale pharmacies."
        }
      ]
    },

    commerce: {
      id: "commerce",
      title: "12th Commerce & Accountancy",
      badge: "📊 Chartered Accountancy, Finance & Corporate Law",
      icon: "📊",
      theme_color: "#f59e0b",
      short_desc: "The premier pathway for finance, corporate governance, auditing, and corporate litigation. Unlocks Chartered Accountancy (CA), Cost & Management Accountancy (CMA), Company Secretary (CS), 5-Year Corporate Law at SOEL, and investment banking careers.",
      eligibility: "12th Standard Pass with Commerce, Accountancy, Economics & Business Maths / Computer Applications",
      duration: "3 to 5 Years",
      starting_salary: "₹5.0 LPA - ₹22.0 LPA",
      senior_salary: "₹20.0 LPA - ₹60.0+ LPA",
      portal_name: "TNGASA & ICAI / ICMAI / ICSI / SOEL",
      portal_url: "https://www.icai.org",
      popular_courses: [
        "CA — Chartered Accountancy (Foundation, Intermediate, Final + Articleship)",
        "CMA — Cost & Management Accountancy (ICMAI)",
        "5-Year Integrated B.Com. LL.B (Honours) at TNDALU SOEL",
        "B.Com (General / Corporate Secretaryship / Accounting & Finance)",
        "BBA & Fintech Financial Analytics (Loyola, MCC, PSG CAS)",
        "CS — Company Secretary (ICSI CSEET)"
      ],
      job_opportunities: [
        {
          id: "job_comm_ca",
          title: "Chartered Accountant (CA) / Chief Financial Officer (CFO)",
          icon: "💼",
          sector: "Chartered Accountancy, Auditing & Taxation",
          type: "finance",
          starting_salary: "₹9.5 LPA - ₹30.0 LPA",
          senior_salary: "₹35.0 LPA - ₹90.0+ LPA",
          description: "Directs statutory audits, signs corporate financial statements, plans international tax structures, advises on mergers and acquisitions, and oversees corporate treasury.",
          hiring_companies: ["Big 4 (Deloitte, PwC, EY, KPMG)", "Standard Chartered", "Citi Bank", "Tata Sons", "Reliance"],
          key_skills: ["Indian Accounting Standards (Ind AS)", "Statutory Auditing", "Corporate Taxation", "GST Laws", "Financial Modeling"],
          progression: "Audit Associate → Senior Tax Manager → Partner in Accounting Firm / Corporate CFO",
          gateway: "ICAI CA Foundation Exam (Register immediately post 12th Board) → Intermediate → Articleship → CA Final",
          perks: "The gold standard finance credential globally with statutory signing authority and infinite independent practice potential."
        },
        {
          id: "job_comm_investment_banker",
          title: "Investment Banking Analyst / Equity Research Associate",
          icon: "📈",
          sector: "Investment Banking & Capital Markets",
          type: "finance",
          starting_salary: "₹8.0 LPA - ₹25.0 LPA",
          senior_salary: "₹28.0 LPA - ₹70.0+ LPA",
          description: "Constructs discounted cash flow (DCF) valuation models, evaluates IPO readiness, facilitates venture capital funding rounds, and prepares investor pitch decks.",
          hiring_companies: ["Barclays", "Goldman Sachs", "World Bank Chennai Centre", "Bank of America", "Kotak Mahindra"],
          key_skills: ["Financial Statement Analysis", "DCF Valuation", "Advanced Excel / VBA", "Bloomberg Terminal", "LBO Modeling"],
          progression: "Analyst → Associate → Vice President → Managing Director of Capital Markets",
          gateway: "B.Com / BBA from Premier Colleges (Loyola College, MCC, PSG CAS) + CFA Certification",
          perks: "Prestigious global finance career with exceptional annual performance bonuses."
        },
        {
          id: "job_comm_corporate_lawyer",
          title: "Corporate Legal Counsel / Company Secretary (CS)",
          icon: "⚖️",
          sector: "Corporate Law, M&A & Compliance",
          type: "corporate",
          starting_salary: "₹6.5 LPA - ₹18.0 LPA",
          senior_salary: "₹22.0 LPA - ₹50.0+ LPA",
          description: "Drafts cross-border commercial contracts, manages National Company Law Tribunal (NCLT) corporate litigation, and ensures full SEBI securities compliance.",
          hiring_companies: ["Shardul Amarchand Mangaldas", "Cyril Amarchand Mangaldas", "TVS Group", "Zoho Legal", "Madras High Court"],
          key_skills: ["Companies Act 2013", "Contract Drafting", "SEBI Regulations", "Mergers & Acquisitions", "Intellectual Property"],
          progression: "Legal Associate → Senior Legal Counsel → Head of Legal & Company Secretary",
          gateway: "5-Year Integrated B.Com. LL.B at SOEL (TNDALU Chennai) / CLAT-UG for TNNLU Trichy",
          perks: "Dual business-law qualification; high legal advisory retainer fees from multinational firms."
        },
        {
          id: "job_comm_bank_po",
          title: "Bank Probationary Officer (PO) & Commercial Tax Officer",
          icon: "🏦",
          sector: "Banking & Public Revenue",
          type: "public",
          starting_salary: "₹6.0 LPA - ₹11.5 LPA",
          senior_salary: "₹14.0 LPA - ₹26.0 LPA",
          description: "Evaluates corporate loan credit proposals, inspects collateral assets, manages commercial branch banking operations, and enforces state GST tax collections.",
          hiring_companies: ["State Bank of India (SBI)", "Punjab National Bank", "Canara Bank", "RBI Chennai", "TN Commercial Taxes Dept"],
          key_skills: ["Credit Risk Assessment", "Banking Regulations", "Financial Accounting", "Team Leadership"],
          progression: "Probationary Officer (Scale I) → Branch Chief Manager → Deputy General Manager",
          gateway: "SBI PO / IBPS PO Recruitment Exam / TNPSC Group 2 Commercial Tax Officer",
          perks: "Subsidized housing loans, leased official accommodation, defined pension schemes, high societal respect."
        }
      ]
    },

    arts: {
      id: "arts",
      title: "12th Arts & Humanities",
      badge: "📚 Law, Civil Services (IAS/IPS), Design & Media",
      icon: "📚",
      theme_color: "#ec4899",
      short_desc: "Tailored for thinkers, legal advocates, administrators, and creative designers. Unlocks premier 5-Year Law at TNDALU, UPSC Civil Services (IAS/IPS), TNPSC Group 1 (Deputy Collector/DSP), NIFT Fashion Design, and visual communication.",
      eligibility: "12th Standard Pass with History, Political Science, Economics, Geography / English",
      duration: "3 to 5 Years",
      starting_salary: "₹5.0 LPA - ₹18.0 LPA",
      senior_salary: "₹18.0 LPA - ₹50.0+ LPA",
      portal_name: "TNDALU, TNGASA & NIFT",
      portal_url: "https://www.tndalu.ac.in",
      popular_courses: [
        "5-Year Integrated B.A. LL.B (Honours) at TNDALU School of Excellence in Law",
        "B.A Public Administration / Political Science (Best for UPSC IAS/IPS)",
        "B.Des — Bachelor of Design (NIFT Chennai Fashion / Textile / UX)",
        "B.Sc Visual Communication & Electronic Media (Loyola College, MCC)",
        "B.A Economics (Presidency College, Madras School of Economics)"
      ],
      job_opportunities: [
        {
          id: "job_arts_civil_servant",
          title: "Civil Servant (IAS / IPS / IFS) & State Deputy Collector",
          icon: "🏛️",
          sector: "Indian Administrative & State Executive Services",
          type: "public",
          starting_salary: "₹12.0 LPA (Starting Basic Pay + DA + Govt Bungalow + Security + Car)",
          senior_salary: "₹26.0 LPA - ₹40.0 LPA",
          description: "Executes government public policies, manages law and order as District Magistrate, directs district development budgets, and oversees disaster management.",
          hiring_companies: ["Government of India", "Government of Tamil Nadu", "District Collectorates", "TN Secretariat"],
          key_skills: ["Public Administration", "Constitution of India", "Public Policy Drafting", "Crisis Leadership"],
          progression: "Sub Collector / SDM → District Collector / Magistrate → Secretary to Government → Chief Secretary",
          gateway: "UPSC Civil Services Examination (Preliminary, Mains, Interview) / TNPSC Group 1 Examination",
          perks: "The most prestigious public leadership role in India with supreme administrative authority."
        },
        {
          id: "job_arts_advocate",
          title: "Advocate / High Court Practitioner & Civil Judge",
          icon: "⚖️",
          sector: "Judiciary & Legal Advocacy",
          type: "public",
          starting_salary: "₹5.5 LPA - ₹25.0 LPA",
          senior_salary: "₹25.0 LPA - ₹80.0+ LPA",
          description: "Represents clients in constitutional writs, civil disputes, criminal trials, and appeals before the Madras High Court, District Courts, and Supreme Court of India.",
          hiring_companies: ["Madras High Court", "Madurai Bench", "High Court Chambers", "TN State Judicial Service"],
          key_skills: ["Constitutional Law", "Oral Argumentation", "Legal Research", "Cross Examination", "Statutory Interpretation"],
          progression: "Junior Advocate → Senior Counsel / Government Pleader → District Judge / High Court Judge",
          gateway: "5-Year Integrated B.A. LL.B (TNDALU Single Window / CLAT) → Bar Council Enrolment → Civil Judge Exam",
          perks: "Statutory constitutional authority as Judge; unlimited independent legal practice revenue as Senior Counsel."
        },
        {
          id: "job_arts_designer",
          title: "Lead UX / Product Designer & Creative Director",
          icon: "🎨",
          sector: "Creative Design, Fashion & Digital Products",
          type: "tech",
          starting_salary: "₹6.0 LPA - ₹18.0 LPA",
          senior_salary: "₹20.0 LPA - ₹52.0 LPA",
          description: "Creates intuitive user interfaces for mobile/web apps, conducts user research, directs brand visual design systems, and develops high-fashion apparel lines.",
          hiring_companies: ["Zoho Design Labs", "Swiggy", "Titan Company", "NIFT Alumni Studios", "Ad Agencies in Chennai"],
          key_skills: ["Figma / Adobe Creative Suite", "Design Thinking", "Design Systems", "User Research", "Wireframing"],
          progression: "Junior UX Designer → Senior Product Designer → Head of Design / Creative Director",
          gateway: "B.Des via NIFT Entrance Exam / B.Sc Visual Communication from Loyola College",
          perks: "Rapidly growing demand in tech startups, design studios, and luxury apparel brands in Chennai and Bangalore."
        }
      ]
    },

    diploma: {
      id: "diploma",
      title: "Polytechnic / Diploma (DOTE Technical)",
      badge: "🔧 Direct Lateral Entry to B.E & Industry Supervisors",
      icon: "🔧",
      theme_color: "#0d9488",
      short_desc: "The premier hands-on technical pathway in Tamil Nadu. Offers direct 2nd-Year Lateral Entry into B.E / B.Tech engineering degrees at Anna University, or direct employment as Junior Engineers in TANGEDCO, PWD, and automotive manufacturing corridors.",
      eligibility: "3-Year Polytechnic Diploma (or 2-Year Lateral Entry after 12th Vocational)",
      duration: "2 to 3 Years",
      starting_salary: "₹3.8 LPA - ₹8.5 LPA",
      senior_salary: "₹10.0 LPA - ₹24.0 LPA",
      portal_name: "DOTE Tamil Nadu & Anna University Lateral Entry",
      portal_url: "https://www.dte.tn.gov.in",
      popular_courses: [
        "Direct 2nd-Year Lateral Entry B.E / B.Tech (Join Directly in 3rd Semester)",
        "Advanced Diploma in Industrial Robotics & Mechatronics",
        "Post-Diploma in Tool Design & CNC Manufacturing (CPT Chennai)",
        "Certified PLC / SCADA Automation & Embedded IoT Systems"
      ],
      job_opportunities: [
        {
          id: "job_dip_production_eng",
          title: "Automotive Production Engineer & Shop Floor Lead",
          icon: "⚙️",
          sector: "Automotive & Advanced Manufacturing",
          type: "corporate",
          starting_salary: "₹4.0 LPA - ₹8.5 LPA",
          senior_salary: "₹10.5 LPA - ₹22.0 LPA",
          description: "Controls automated assembly lines, manages industrial robotic spot welders, enforces Lean Six Sigma quality protocols, and oversees production shifts.",
          hiring_companies: ["Hyundai Motor India", "Renault-Nissan", "Royal Enfield", "TVS Motor", "Foxconn Sriperumbudur"],
          key_skills: ["Lean Manufacturing", "Robotic Line Automation", "Quality Assurance (QA/QC)", "AutoCAD / SolidWorks"],
          progression: "Diploma Engineer Trainee (DET) → Line In-Charge → Production Manager → Plant Head",
          gateway: "Direct Campus Recruitment in Premier Polytechnic Colleges (CPT, PSG Poly, Murugappa, CIT Poly)",
          perks: "Highest hands-on machine shop floor credibility; fast promotional tracks to shift management."
        },
        {
          id: "job_dip_tangedco_je",
          title: "Junior Engineer (TANGEDCO / PWD / Highways Dept)",
          icon: "⚡",
          sector: "State Technical Public Utilities",
          type: "public",
          starting_salary: "₹4.5 LPA (TN Pay Matrix Level 11 + Allowances)",
          senior_salary: "₹12.0 LPA - ₹24.0 LPA",
          description: "Supervises electric substation transformers, distribution grid maintenance, government building construction sites, and state highway projects.",
          hiring_companies: ["TANGEDCO (Electricity Board)", "Public Works Department (PWD)", "Highways Dept", "TWAD Board"],
          key_skills: ["Electrical Power Systems", "Structural Surveying", "Measurement Book (MB) Entry", "Contractor Supervision"],
          progression: "Junior Engineer (JE) → Assistant Engineer (AE upon degree) → Executive Engineer",
          gateway: "TNPSC Combined Engineering Subordinate Services / TANGEDCO Direct Recruitment",
          perks: "Permanent government engineering post with excellent work-life balance and state benefits."
        },
        {
          id: "job_dip_software_lateral",
          title: "Full-Stack Software Engineer (Lateral B.E / B.Tech Entry)",
          icon: "💻",
          sector: "Information Technology & Software Services",
          type: "tech",
          starting_salary: "₹5.5 LPA - ₹18.0 LPA",
          senior_salary: "₹20.0 LPA - ₹45.0 LPA",
          description: "Leverages deep hardware/software foundational knowledge to build enterprise web applications, embedded firmware, and cloud backend microservices.",
          hiring_companies: ["Zoho", "TCS", "Cognizant", "Kaar Technologies", "Wipro", "Hexaware"],
          key_skills: ["JavaScript / React / Node.js", "Java / Spring Boot", "SQL Databases", "Git / GitHub"],
          progression: "Software Engineer → Tech Lead → Engineering Manager",
          gateway: "Direct 2nd-Year Lateral Entry B.E at Anna University CEG / MIT / PSG Tech → Campus Placement",
          perks: "Saves 1 year of tuition fees and gains superior hands-on laboratory practical expertise."
        }
      ]
    },

    graduate: {
      id: "graduate",
      title: "Undergraduate Degree (B.E / B.Tech / B.Sc / BCA / B.Com)",
      badge: "🎓 Campus Placement & Direct Industry Hiring",
      icon: "🎓",
      theme_color: "#8b5cf6",
      short_desc: "For college graduates seeking corporate placement drives, high-paying tech roles, management trainee schemes, or public sector competitive exams. Directly matches verified campus hiring drives and Tier-1 employer benchmarks.",
      eligibility: "Completed or Final Year Undergraduate Degree in any discipline",
      duration: "Immediate Employment / Direct Placement",
      starting_salary: "₹4.5 LPA - ₹32.0 LPA",
      senior_salary: "₹18.0 LPA - ₹65.0+ LPA",
      portal_name: "Campus Hub & Placement Compass",
      portal_url: "study-materials.html",
      popular_courses: [
        "Campus Placement Ready Training (Aptitude, Coding & DSA)",
        "Full-Stack Web Development & Cloud DevOps Certifications",
        "MBA — Master of Business Administration (CAT / TANCET)",
        "M.E / M.Tech in Artificial Intelligence / Data Science (GATE)"
      ],
      job_opportunities: [
        {
          id: "job_grad_sde",
          title: "Full-Stack Developer & Cloud DevOps Engineer",
          icon: "💻",
          sector: "Enterprise Software & Cloud Platforms",
          type: "tech",
          starting_salary: "₹6.5 LPA - ₹26.0 LPA",
          senior_salary: "₹24.0 LPA - ₹60.0 LPA",
          description: "Builds responsive client-facing web applications, designs robust REST and GraphQL APIs, deploys cloud infrastructure on AWS/GCP, and automates CI/CD deployment pipelines.",
          hiring_companies: ["Zoho", "Amazon", "Freshworks", "TCS Digital", "Cognizant GenC Next", "Accenture Advanced Tech"],
          key_skills: ["React / TypeScript", "Node.js / Python / Java", "Docker & Kubernetes", "CI/CD Pipelines", "System Design"],
          progression: "Associate SDE → SDE II → Lead Engineer → Director of Engineering",
          gateway: "Verified Sandbox Assessments & Campus Placement Drives",
          perks: "Hybrid work flexibility, tech stock options (ESOPs), and rapid bi-annual merit appraisals."
        },
        {
          id: "job_grad_data_engineer",
          title: "Data Analytics Engineer & Business Intelligence Lead",
          icon: "📊",
          sector: "Big Data & Financial Analytics",
          type: "tech",
          starting_salary: "₹6.0 LPA - ₹18.0 LPA",
          senior_salary: "₹20.0 LPA - ₹48.0 LPA",
          description: "Constructs automated ETL data pipelines, manages snowflake cloud data warehouses, writes optimized SQL analytical queries, and powers executive business dashboards.",
          hiring_companies: ["Tiger Analytics", "LatentView", "Standard Chartered GBS", "Deloitte USI", "Mu Sigma"],
          key_skills: ["Advanced SQL", "Python / PySpark", "Snowflake / BigQuery", "Power BI / Tableau", "Data Modeling"],
          progression: "Data Analyst → Analytics Consultant → Lead Data Architect",
          gateway: "Direct Recruitment Drives / Technical Assessment on Recruiter Platform",
          perks: "High corporate visibility with direct strategic reporting to C-suite executive leaders."
        },
        {
          id: "job_grad_tnpsc_group1",
          title: "Deputy Collector / DSP (TNPSC Group 1 Officer)",
          icon: "🏛️",
          sector: "Tamil Nadu State Civil Services",
          type: "public",
          starting_salary: "₹12.0 LPA (TN Pay Matrix Level 22 + All State Perks)",
          senior_salary: "₹25.0 LPA - ₹42.0 LPA",
          description: "Top state executive administration role managing district revenue sub-divisions, police sub-divisions, law and order enforcement, and state development projects.",
          hiring_companies: ["Government of Tamil Nadu", "District Collectorates", "Tamil Nadu Police", "Secretariat"],
          key_skills: ["Administrative Leadership", "Tamil Essay Writing", "General Studies", "Public Governance"],
          progression: "Deputy Collector (Training) → Revenue Divisional Officer (RDO) → District Revenue Officer (DRO) → District Collector",
          gateway: "TNPSC Group 1 Examination (Open to Any Graduate Degree Holder)",
          perks: "Highest ranked state public appointment with official bungalow, security detail, and vehicle."
        }
      ]
    }
  };

  let activeQualificationKey = "computer_science";
  let activeJobFilter = "all";

  function initPlacementCompassSection() {
    const container = document.getElementById("compass-qualification-dossier");
    if (!container) return;

    // Attach event listeners to qualification selector pills
    const pills = document.querySelectorAll("[data-qualification-pill]");
    pills.forEach((pill) => {
      pill.addEventListener("click", function (e) {
        e.preventDefault();
        const qualKey = this.getAttribute("data-qualification-pill");
        selectQualification(qualKey);
      });
    });

    // Check URL parameter for qualification
    const urlParams = new URLSearchParams(window.location.search);
    const initialQual = urlParams.get("qualification") || "computer_science";
    selectQualification(initialQual);

    // Setup live search / filter inputs if present
    const searchInput = document.getElementById("compass-job-search-input");
    if (searchInput) {
      searchInput.addEventListener("input", function () {
        renderJobsGrid(this.value.trim().toLowerCase());
      });
    }

    const filterBtns = document.querySelectorAll("[data-job-filter-btn]");
    filterBtns.forEach((btn) => {
      btn.addEventListener("click", function () {
        filterBtns.forEach((b) => b.classList.remove("active", "btn-primary", "btn-dark"));
        filterBtns.forEach((b) => b.classList.add("btn-outline-secondary"));
        this.classList.remove("btn-outline-secondary");
        this.classList.add("active", "btn-primary");
        activeJobFilter = this.getAttribute("data-job-filter-btn");
        renderJobsGrid();
      });
    });
  }

  function selectQualification(qualKey) {
    if (!QUALIFICATION_CAREER_MAP[qualKey]) {
      qualKey = "computer_science";
    }
    activeQualificationKey = qualKey;

    // Update Pills visual state
    document.querySelectorAll("[data-qualification-pill]").forEach((pill) => {
      const k = pill.getAttribute("data-qualification-pill");
      if (k === qualKey) {
        pill.classList.add("active");
        pill.style.borderColor = "#6366f1";
        pill.style.boxShadow = "0 8px 24px rgba(99, 102, 241, 0.25)";
      } else {
        pill.classList.remove("active");
        pill.style.borderColor = "";
        pill.style.boxShadow = "";
      }
    });

    renderQualificationDossier();
  }

  function renderQualificationDossier() {
    const data = QUALIFICATION_CAREER_MAP[activeQualificationKey];
    if (!data) return;

    // 1. Update Hero Dossier Summary
    const heroTitle = document.getElementById("dossier-hero-title");
    const heroBadge = document.getElementById("dossier-hero-badge");
    const heroDesc = document.getElementById("dossier-hero-desc");
    const heroEligibility = document.getElementById("dossier-hero-eligibility");
    const heroDuration = document.getElementById("dossier-hero-duration");
    const heroSalary = document.getElementById("dossier-hero-salary");
    const heroPortalBtn = document.getElementById("dossier-hero-portal-btn");
    const heroSubcoursesContainer = document.getElementById("dossier-subcourses-pills");

    if (heroTitle) heroTitle.innerHTML = `${data.icon} ${data.title}`;
    if (heroBadge) heroBadge.textContent = data.badge;
    if (heroDesc) heroDesc.textContent = data.short_desc;
    if (heroEligibility) heroEligibility.textContent = data.eligibility;
    if (heroDuration) heroDuration.textContent = data.duration;
    if (heroSalary) heroSalary.textContent = `${data.starting_salary} (Starting) → ${data.senior_salary} (Senior)`;
    if (heroPortalBtn) {
      heroPortalBtn.href = data.portal_url;
      heroPortalBtn.innerHTML = `<span>🏛️</span> Official Portal: ${data.portal_name} &rarr;`;
    }

    if (heroSubcoursesContainer && data.popular_courses) {
      heroSubcoursesContainer.innerHTML = data.popular_courses
        .map(
          (c) => `
          <span class="badge bg-white bg-opacity-10 border border-white border-opacity-15 text-light fw-medium px-3 py-1.5 rounded-pill small hover-lift cursor-pointer" onclick="filterJobsByCourse('${c.replace(/'/g, "\\'")}')">
            ${c}
          </span>
        `
        )
        .join(" ");
    }

    // 2. Render Jobs Grid
    renderJobsGrid();

    // 3. Render Courses Tab
    renderCoursesGrid();
  }

  function renderJobsGrid(searchQuery = "") {
    const grid = document.getElementById("compass-jobs-grid");
    if (!grid) return;

    const data = QUALIFICATION_CAREER_MAP[activeQualificationKey];
    if (!data || !data.job_opportunities) {
      grid.innerHTML = `<div class="col-12 text-center text-muted py-4">No jobs mapped for this qualification.</div>`;
      return;
    }

    let jobs = data.job_opportunities;

    // Filter by type
    if (activeJobFilter !== "all") {
      if (activeJobFilter === "public") {
        jobs = jobs.filter((j) => j.type === "public");
      } else if (activeJobFilter === "tech") {
        jobs = jobs.filter((j) => j.type === "tech");
      } else if (activeJobFilter === "high_package") {
        jobs = jobs.filter((j) => {
          const num = parseFloat(j.starting_salary.replace(/[^0-9.]/g, ""));
          return num >= 6.0;
        });
      }
    }

    // Filter by search query
    if (searchQuery) {
      jobs = jobs.filter((j) => {
        const text = `${j.title} ${j.description} ${j.sector} ${(j.hiring_companies || []).join(" ")} ${(j.key_skills || []).join(" ")}`.toLowerCase();
        return text.includes(searchQuery);
      });
    }

    // Update count badge
    const countBadge = document.getElementById("compass-jobs-count-badge");
    if (countBadge) {
      countBadge.textContent = `${jobs.length} Verified Career Opportunities`;
    }

    if (jobs.length === 0) {
      grid.innerHTML = `
        <div class="col-12 py-5 text-center text-muted bg-dark bg-opacity-25 rounded-4 border border-secondary border-opacity-25">
          <div class="fs-2 mb-2">🔍</div>
          <h6 class="fw-bold text-light">No job opportunities match your search filter</h6>
          <p class="small text-secondary mb-3">Try clearing your search keyword or switch to "All Roles".</p>
          <button class="btn btn-outline-primary btn-sm rounded-pill px-4 fw-bold" onclick="resetJobFilters()">Reset Filters</button>
        </div>
      `;
      return;
    }

    grid.innerHTML = jobs
      .map((job) => {
        const typeBadge =
          job.type === "public"
            ? `<span class="badge bg-warning bg-opacity-15 text-warning border border-warning border-opacity-25 rounded-pill px-2.5 py-1 small">🏛️ Govt / Public Sector</span>`
            : job.type === "tech"
            ? `<span class="badge bg-primary bg-opacity-15 text-info border border-info border-opacity-25 rounded-pill px-2.5 py-1 small">💻 Tech &amp; Software</span>`
            : job.type === "healthcare"
            ? `<span class="badge bg-success bg-opacity-15 text-success border border-success border-opacity-25 rounded-pill px-2.5 py-1 small">🩺 Clinical Healthcare</span>`
            : `<span class="badge bg-info bg-opacity-15 text-info border border-info border-opacity-25 rounded-pill px-2.5 py-1 small">💼 Corporate &amp; Finance</span>`;

        const skillsBadges = (job.key_skills || [])
          .map((s) => `<span class="badge bg-white bg-opacity-10 text-light border border-white border-opacity-10 small rounded-pill px-2 py-1">${s}</span>`)
          .join(" ");

        const companiesList = (job.hiring_companies || []).slice(0, 5).join(" • ");

        return `
        <div class="col-md-6 col-lg-6">
          <div class="card border-0 shadow-lg rounded-4 h-100 p-4 transition-all hover-lift" style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.1) !important;">
            <div class="d-flex justify-content-between align-items-start gap-2 mb-3">
              <div>
                <div class="d-flex align-items-center gap-2 mb-1.5 flex-wrap">
                  ${typeBadge}
                  <span class="badge bg-secondary bg-opacity-25 text-light border border-secondary border-opacity-25 rounded-pill px-2 py-0.5 small">${job.sector}</span>
                </div>
                <h5 class="fw-bold text-white mb-1 d-flex align-items-center gap-2" style="letter-spacing: -0.01em;">
                  <span>${job.icon}</span> ${job.title}
                </h5>
              </div>
            </div>

            <p class="text-light opacity-75 small mb-3" style="line-height: 1.6; min-height: 48px;">
              ${job.description}
            </p>

            <!-- Salary Metrics Box -->
            <div class="p-3 rounded-3 mb-3" style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08);">
              <div class="row g-2 text-center text-md-start">
                <div class="col-6 border-end border-secondary border-opacity-25">
                  <div class="text-secondary small fw-semibold">Entry / Fresher Package</div>
                  <div class="fw-bold text-success fs-6 mt-0.5">${job.starting_salary}</div>
                </div>
                <div class="col-6 ps-md-3">
                  <div class="text-secondary small fw-semibold">Senior (5-8 Yrs) Ceiling</div>
                  <div class="fw-bold text-warning fs-6 mt-0.5">${job.senior_salary}</div>
                </div>
              </div>
            </div>

            <!-- Top Hiring Employers -->
            <div class="mb-3">
              <div class="small fw-semibold text-secondary mb-1">🏛️ Top Hiring Organizations &amp; Corridors:</div>
              <div class="small text-light opacity-90 fw-medium">${companiesList}</div>
            </div>

            <!-- In-Demand Skills -->
            <div class="mb-3">
              <div class="small fw-semibold text-secondary mb-1.5">⚡ Key Verified Skills:</div>
              <div class="d-flex flex-wrap gap-1">${skillsBadges}</div>
            </div>

            <!-- Career Progression -->
            <div class="p-2.5 rounded-3 mb-3 small" style="background: rgba(99, 102, 241, 0.08); border: 1px solid rgba(99, 102, 241, 0.2);">
              <span class="text-indigo-subtle fw-bold">🚀 Promotion Ladder:</span>
              <span class="text-light opacity-90">${job.progression}</span>
            </div>

            <!-- Action Buttons -->
            <div class="d-flex gap-2 mt-auto pt-2 border-top border-secondary border-opacity-25 flex-wrap">
              <a href="jobs.html?keyword=${encodeURIComponent(job.title.split("/")[0].trim())}" class="btn btn-primary btn-sm rounded-pill fw-bold px-3 flex-grow-1 shadow-sm">
                🔍 Browse Live Jobs &rarr;
              </a>
              <a href="placement-compass.html" class="btn btn-outline-light btn-sm rounded-pill fw-semibold px-3 flex-grow-1">
                🧭 Open Full Compass
              </a>
              <a href="study-materials.html" class="btn btn-outline-warning btn-sm rounded-pill fw-semibold px-3" title="Prepare For Placement Drives">
                🧠 Practice Lab
              </a>
            </div>
          </div>
        </div>
      `;
      })
      .join("");
  }

  function renderCoursesGrid() {
    const grid = document.getElementById("compass-courses-grid");
    if (!grid) return;

    const data = QUALIFICATION_CAREER_MAP[activeQualificationKey];
    if (!data) return;

    // Use bundled static data paths if matching
    let matchingPaths = [];
    if (typeof window !== "undefined" && window.COMPASS_STATIC_DATA && window.COMPASS_STATIC_DATA.paths) {
      const allPaths = window.COMPASS_STATIC_DATA.paths;
      matchingPaths = allPaths.filter((p) => {
        if (activeQualificationKey === "sslc_10th") {
          return p.grade_level === "after_10th" || p.grade_level === "after_10th_or_12th";
        } else if (activeQualificationKey === "computer_science") {
          return p.grade_level === "after_12th_pcm" || p.category === "engineering";
        } else if (activeQualificationKey === "biology") {
          return p.grade_level === "after_12th_pcb" || p.category === "medical" || p.category === "agriculture";
        } else if (activeQualificationKey === "commerce") {
          return p.grade_level === "after_12th_commerce";
        } else if (activeQualificationKey === "arts") {
          return p.grade_level === "after_12th_arts" || p.category === "law";
        } else if (activeQualificationKey === "diploma") {
          return p.category === "diploma_polytechnic" || p.category === "engineering";
        } else {
          return p.grade_level.startsWith("after_12th");
        }
      });
    }

    if (matchingPaths.length === 0) {
      grid.innerHTML = (data.popular_courses || [])
        .map(
          (c) => `
        <div class="col-md-6 col-lg-4">
          <div class="p-3 rounded-4 bg-dark bg-opacity-50 border border-secondary border-opacity-25 h-100">
            <h6 class="fw-bold text-white mb-1">🎓 ${c}</h6>
            <p class="small text-secondary mb-2">Accredited degree pathway with single-window state admissions in Tamil Nadu.</p>
            <a href="placement-compass.html" class="text-primary small fw-semibold text-decoration-none">Explore Admission Cutoffs &rarr;</a>
          </div>
        </div>
      `
        )
        .join("");
      return;
    }

    grid.innerHTML = matchingPaths
      .slice(0, 6)
      .map(
        (p) => `
      <div class="col-md-6 col-lg-4">
        <div class="card border-0 shadow-sm p-4 rounded-4 h-100" style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.08) !important;">
          <div class="d-flex align-items-center gap-2 mb-2">
            <span class="fs-2">${p.icon_emoji}</span>
            <div>
              <h6 class="fw-bold text-white mb-0" style="font-size: 0.95rem;">${p.title}</h6>
              <span class="badge bg-primary bg-opacity-20 text-info border border-info border-opacity-25 rounded-pill small">${p.duration}</span>
            </div>
          </div>
          <p class="text-light opacity-75 small mb-3" style="min-height: 40px;">${p.tagline}</p>
          <div class="p-2.5 rounded-3 bg-white bg-opacity-5 small text-light opacity-90 mb-3">
            <div><strong>🎓 Eligibility:</strong> <span class="text-secondary">${p.eligibility}</span></div>
            <div><strong>🏛️ Campuses:</strong> <span class="text-secondary">${(p.top_colleges || []).slice(0, 2).join(", ")}</span></div>
          </div>
          <div class="d-flex gap-2 mt-auto">
            <button class="btn btn-primary btn-sm rounded-pill fw-bold w-100 shadow-sm" onclick="openPathwayModal('${p.id}')">
              📖 Explore Deep Dive &rarr;
            </button>
            <a href="placement-compass.html" class="btn btn-outline-info btn-sm rounded-pill fw-semibold text-nowrap">
              Portal
            </a>
          </div>
        </div>
      </div>
    `
      )
      .join("");
  }

  function filterJobsByCourse(courseName) {
    const searchInput = document.getElementById("compass-job-search-input");
    if (searchInput) {
      // Pick first word or major keyword
      const keyword = courseName.split(" ")[0].replace(/[^a-zA-Z]/g, "").toLowerCase();
      searchInput.value = keyword;
      renderJobsGrid(keyword);
    }
  }

  function resetJobFilters() {
    activeJobFilter = "all";
    const searchInput = document.getElementById("compass-job-search-input");
    if (searchInput) searchInput.value = "";
    document.querySelectorAll("[data-job-filter-btn]").forEach((b) => {
      if (b.getAttribute("data-job-filter-btn") === "all") {
        b.classList.remove("btn-outline-secondary");
        b.classList.add("active", "btn-primary");
      } else {
        b.classList.remove("active", "btn-primary");
        b.classList.add("btn-outline-secondary");
      }
    });
    renderJobsGrid();
  }

  // Export functions to window
  window.PlacementCompassSection = {
    init: initPlacementCompassSection,
    selectQualification: selectQualification,
    filterJobsByCourse: filterJobsByCourse,
    resetJobFilters: resetJobFilters
  };

  // Auto initialize on DOMContentLoaded
  document.addEventListener("DOMContentLoaded", initPlacementCompassSection);
})();

// Standalone Modal handler for Placement Compass Course Deep Dive on Homepage
if (typeof window !== "undefined" && !window.openPathwayModal) {
  window.openPathwayModal = function(pathId) {
    if (typeof window.COMPASS_STATIC_DATA === "undefined" || !window.COMPASS_STATIC_DATA.paths) {
      window.location.href = "placement-compass.html";
      return;
    }
    const path = window.COMPASS_STATIC_DATA.paths.find(p => p.id === pathId) || window.COMPASS_STATIC_DATA.paths[0];
    if (!path) {
      window.location.href = "placement-compass.html";
      return;
    }

    const iconEl = document.getElementById("modal-path-icon");
    const titleEl = document.getElementById("modal-path-title");
    const catEl = document.getElementById("modal-path-category");
    const durEl = document.getElementById("modal-path-duration");
    if (iconEl) iconEl.textContent = path.icon_emoji || "🎓";
    if (titleEl) titleEl.textContent = path.title || "Career Pathway";
    if (catEl) catEl.textContent = (path.category || "GENERAL").toUpperCase().replace("_", " ");
    if (durEl) durEl.textContent = path.duration || "Multi-Year";

    const skillsList = path.key_skills_needed || ["Foundational Science", "Practical Laboratory Training", "Industry Problem Solving", "Professional Ethics"];
    const skillsBadges = skillsList.map(s => `<span class="badge bg-primary-subtle text-primary border border-primary-subtle py-1.5 px-3 rounded-pill small fw-bold me-1 mb-1">🛠️ ${s}</span>`).join("");
    const collegesHtml = (path.top_colleges || []).map(c => `<li class="mb-1 text-dark small fw-medium">🏛️ ${c}</li>`).join("");
    const scholarshipsHtml = (path.scholarships || []).map(s => `<li class="mb-1 text-success fw-bold small">✅ ${s}</li>`).join("");

    const examsHtml = (path.entrance_exams || [])
      .map(e => `
        <div class="p-3 bg-white rounded-3 border mb-2 shadow-xs">
          <div class="d-flex justify-content-between align-items-center mb-1">
            <strong class="text-dark">${e.name}</strong>
            <span class="badge bg-primary text-white">${e.level}</span>
          </div>
          <p class="small text-secondary mb-1">${e.description}</p>
          ${e.official_portal ? `<a href="${e.official_portal}" target="_blank" rel="noopener noreferrer" class="small text-primary fw-bold text-decoration-none">🔗 Official Portal: ${e.official_portal} &rarr;</a>` : ""}
        </div>
      `)
      .join("");

    const bodyEl = document.getElementById("modal-path-body");
    if (bodyEl) {
      bodyEl.innerHTML = `
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

        <div class="card border-0 shadow-sm p-4 mb-4 rounded-4 bg-white">
          <h5 class="fw-bold text-dark mb-2">🎓 2. Academic Eligibility &amp; Tamil Nadu Cutoff Rules</h5>
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

        <div class="card border-0 shadow-sm p-4 mb-4 rounded-4 bg-white">
          <h5 class="fw-bold text-dark mb-2">📚 3. What Students Will Learn (Syllabus &amp; Tools)</h5>
          <div class="d-flex flex-wrap gap-1 mb-3">
            ${skillsBadges}
          </div>
          <div class="p-3 bg-light rounded-3 border small text-secondary">
            <strong>📋 Practical Training:</strong> Hands-on workshops, real-time industrial problem solving, software laboratories, team projects, and case-study presentations.
          </div>
        </div>

        <div class="card border-0 shadow-sm p-4 mb-4 rounded-4 bg-white">
          <h5 class="fw-bold text-dark mb-3">🎁 4. Academic, Financial &amp; Tamil Nadu Government Benefits</h5>
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

        <div class="card border-0 shadow-sm p-4 mb-4 rounded-4 bg-white border-top border-4 border-info">
          <h5 class="fw-bold text-dark mb-2">🗺️ 5. Interactive Visual Career Roadmap</h5>
          <div class="d-flex flex-column gap-2">
            <div class="p-2.5 rounded-3 bg-light border d-flex align-items-center gap-3">
              <span class="badge bg-primary rounded-circle p-2 fs-6">1</span>
              <div>
                <div class="fw-bold text-dark small">School Phase: 10th / 12th Board Exams</div>
                <div class="text-muted small">Score high marks for single-window counseling cutoffs.</div>
              </div>
            </div>
            <div class="text-center text-primary fs-5" style="line-height: 1;">&darr;</div>
            <div class="p-2.5 rounded-3 bg-light border d-flex align-items-center gap-3">
              <span class="badge bg-info text-white rounded-circle p-2 fs-6">2</span>
              <div>
                <div class="fw-bold text-dark small">Admission Phase: TNEA / TN DME / TNGASA Counseling</div>
                <div class="text-muted small">Secure seat allotment with 7.5% Govt School Free Quota if eligible.</div>
              </div>
            </div>
            <div class="text-center text-primary fs-5" style="line-height: 1;">&darr;</div>
            <div class="p-2.5 rounded-3 bg-light border d-flex align-items-center gap-3">
              <span class="badge bg-warning text-dark rounded-circle p-2 fs-6">3</span>
              <div>
                <div class="fw-bold text-dark small">College Phase: Labs, Projects &amp; Internships</div>
                <div class="text-muted small">Gain hands-on competencies and industrial summer training.</div>
              </div>
            </div>
            <div class="text-center text-primary fs-5" style="line-height: 1;">&darr;</div>
            <div class="p-2.5 rounded-3 bg-success-subtle border border-success-subtle d-flex align-items-center gap-3">
              <span class="badge bg-success rounded-circle p-2 fs-6">4</span>
              <div>
                <div class="fw-bold text-success small">Placement Phase: Graduate Career Appointment (${path.starting_salary_range})</div>
                <div class="text-muted small">Join top companies or permanent Tamil Nadu state public services.</div>
              </div>
            </div>
          </div>
        </div>

        <div class="card border-0 shadow-sm p-4 mb-3 rounded-4 bg-white">
          <h5 class="fw-bold text-dark mb-2">🎯 6. Required Entrance Exams &amp; Portals</h5>
          ${examsHtml}
          <div class="p-3 bg-light border rounded-3 text-secondary small mt-2">
            <strong>Admission Procedure:</strong> ${path.admission_procedure}
          </div>
        </div>
      `;
    }

    const modalEl = document.getElementById("pathwayDetailModal");
    if (modalEl && typeof bootstrap !== "undefined") {
      const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
      modal.show();
    }
  };
}
