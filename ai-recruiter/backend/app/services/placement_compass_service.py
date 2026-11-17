"""
placement_compass_service.py — Service layer for the Placement Compass suite.
Provides:
1. Company & placement eligibility prediction (Safe, Target, Dream tiers).
2. 3-way Side-by-side company comparison matrix.
3. Upcoming placement drive timeline with 1-click Google Calendar sync.
4. Mock test score trajectory and performance tracking.
5. Pre-placement document and background check readiness vault.
6. Dual-source sentiment reviews (Reddit vs Glassdoor).
"""
import urllib.parse
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import uuid

# Pre-curated recruitment and placement benchmark repository
BENCHMARK_COMPANIES: List[Dict[str, Any]] = [
    # TIER 1: DREAM PRODUCT GIANTS (18 - 50+ LPA)
    {
        "id": "google",
        "name": "Google",
        "category": "dream",
        "logo_emoji": "🌐",
        "industry": "Search, Cloud & AI Systems",
        "ctc_range": "36 - 55 LPA",
        "min_cgpa": 8.0,
        "min_aptitude": 85.0,
        "difficulty": "High",
        "hiring_status": "Active Hiring",
        "rounds_count": 5,
        "interview_rounds": [
            "Online Coding Assessment (2 LeetCode Medium/Hard)",
            "Technical Round 1: Data Structures & Algorithms",
            "Technical Round 2: Algorithmic Problem Solving",
            "Technical Round 3: System Design & Concurrency",
            "Googliness & Leadership Principles"
        ],
        "core_skills": ["Advanced Algorithms", "Dynamic Programming", "Graphs & Trees", "Distributed Systems", "C++ / Java / Python"],
        "locations": ["Bangalore", "Hyderabad", "Pune", "Gurgaon"],
        "compensation": {
            "total_ctc": "45.0 LPA",
            "base_salary": "18.5 LPA",
            "variable_bonus": "3.0 LPA",
            "joining_bonus": "5.0 LPA",
            "stocks_esops": "18.5 LPA (Vested over 4 yrs)"
        },
        "work_policy": "Hybrid (3 Days Office / 2 Days Remote)",
        "selection_process": {
            "focus": "Deep DSA & Problem Solving, zero tolerance on edge cases",
            "avg_timeline": "4 - 6 Weeks",
            "coding_cutoff": "100% test cases on OA"
        },
        "tech_stack": ["Go", "C++", "Python", "Kubernetes", "Borg", "Spanner", "TensorFlow"],
        "culture_rating": 4.6,
        "work_life_balance": 4.3,
        "pros": ["Industry-leading engineering mentorship", "Exceptional perks and food", "Huge resume value"],
        "cons": ["High internal competition", "Bureaucracy in large teams"],
        "reddit_summary": "Expect strict graph and DP questions on LeetCode hard difficulty. Focus heavily on code cleanliness and time complexity analysis during live rounds.",
        "glassdoor_summary": "Top-tier benefits, supportive peer engineers, and world-class developer tooling with high baseline compensation."
    },
    {
        "id": "amazon",
        "name": "Amazon",
        "category": "dream",
        "logo_emoji": "📦",
        "industry": "E-Commerce & AWS Cloud",
        "ctc_range": "32 - 45 LPA",
        "min_cgpa": 7.5,
        "min_aptitude": 80.0,
        "difficulty": "High",
        "hiring_status": "Active Campus Drive",
        "rounds_count": 4,
        "interview_rounds": [
            "Online Assessment (Debugging + 2 DSA + Work Style Assessment)",
            "Technical Round 1: Data Structures & Problem Solving",
            "Technical Round 2: Trees, Graphs, Hashing + LP",
            "Bar Raiser Round: Leadership Principles & Architecture"
        ],
        "core_skills": ["Data Structures", "Trees & Graphs", "Object-Oriented Design", "AWS Fundamentals", "Leadership Principles"],
        "locations": ["Bangalore", "Hyderabad", "Chennai", "Delhi NCR"],
        "compensation": {
            "total_ctc": "44.0 LPA",
            "base_salary": "16.5 LPA",
            "variable_bonus": "2.5 LPA",
            "joining_bonus": "9.5 LPA (Year 1 & 2)",
            "stocks_esops": "15.5 LPA (5% / 15% / 40% / 40%)"
        },
        "work_policy": "Office Centric (3-5 Days On-Site)",
        "selection_process": {
            "focus": "16 Leadership Principles combined with DSA execution",
            "avg_timeline": "3 - 5 Weeks",
            "coding_cutoff": "2/2 optimal DSA solution"
        },
        "tech_stack": ["Java", "AWS (EC2, S3, DynamoDB)", "Python", "TypeScript", "React"],
        "culture_rating": 4.1,
        "work_life_balance": 3.4,
        "pros": ["Massive scale handling millions of TPS", "Steep learning curve and ownership"],
        "cons": ["On-call duty can be intense", "Aggressive performance review PIP metrics"],
        "reddit_summary": "STAR format answers for Leadership Principles are just as critical as the DSA solutions. Prepare 2 concrete stories for each principle.",
        "glassdoor_summary": "High compensation package, very fast-paced environment, high autonomy on project deliverables."
    },
    {
        "id": "microsoft",
        "name": "Microsoft",
        "category": "dream",
        "logo_emoji": "💻",
        "industry": "Enterprise Software & Azure Cloud",
        "ctc_range": "35 - 50 LPA",
        "min_cgpa": 7.5,
        "min_aptitude": 82.0,
        "difficulty": "High",
        "hiring_status": "Active Hiring",
        "rounds_count": 4,
        "interview_rounds": [
            "Online Assessment (Codility 3 Problems)",
            "Technical Round 1: DSA & Edge-Case Handling",
            "Technical Round 2: Low-Level Design & Concurrency",
            "AA (As Appropriate) Director Round: Behavioral & Vision"
        ],
        "core_skills": ["C# / C++ / Java", "System Design", "Algorithms", "Concurrency", "Azure"],
        "locations": ["Hyderabad", "Bangalore", "Noida"],
        "compensation": {
            "total_ctc": "48.0 LPA",
            "base_salary": "17.0 LPA",
            "variable_bonus": "3.5 LPA",
            "joining_bonus": "6.0 LPA",
            "stocks_esops": "21.5 LPA (Vested over 4 yrs)"
        },
        "work_policy": "Flexible Hybrid (50% Remote Permitted)",
        "selection_process": {
            "focus": "Production-ready coding with modular OOP and error handling",
            "avg_timeline": "3 - 4 Weeks",
            "coding_cutoff": "Complete edge case coverage"
        },
        "tech_stack": ["C#", ".NET Core", "Azure", "TypeScript", "React", "Python"],
        "culture_rating": 4.5,
        "work_life_balance": 4.4,
        "pros": ["Superb work-life balance", "Empathetic leadership and growth", "Generous equity grants"],
        "cons": ["Slower promotion cycles compared to startups"],
        "reddit_summary": "Interviewers are very collaborative. They will give hints; how you adapt to suggestions is a key grading metric.",
        "glassdoor_summary": "Great culture of continuous learning, excellent health benefits, and humane engineering timelines."
    },
    {
        "id": "atlassian",
        "name": "Atlassian",
        "category": "dream",
        "logo_emoji": "🔷",
        "industry": "Developer Productivity Software (Jira, Confluence)",
        "ctc_range": "30 - 42 LPA",
        "min_cgpa": 7.0,
        "min_aptitude": 80.0,
        "difficulty": "High",
        "hiring_status": "National Placement Drive",
        "rounds_count": 4,
        "interview_rounds": [
            "HackerRank Assessment (DSA + Data Modeling)",
            "Coding & Data Structures Round",
            "System Design & Architecture Workshop",
            "Values & Culture Fit Interview"
        ],
        "core_skills": ["Java / Kotlin", "Distributed Architecture", "REST APIs", "React", "Cloud Native"],
        "locations": ["Bangalore", "Remote First (Anywhere in India)"],
        "compensation": {
            "total_ctc": "40.0 LPA",
            "base_salary": "18.0 LPA",
            "variable_bonus": "3.0 LPA",
            "joining_bonus": "4.0 LPA",
            "stocks_esops": "15.0 LPA"
        },
        "work_policy": "Team Anywhere (100% Remote Option)",
        "selection_process": {
            "focus": "Clean code structure, testability, and Atlassian Values",
            "avg_timeline": "3 - 5 Weeks",
            "coding_cutoff": "Production-quality code implementation"
        },
        "tech_stack": ["Kotlin", "Java", "AWS", "React", "GraphQL", "Kafka"],
        "culture_rating": 4.7,
        "work_life_balance": 4.6,
        "pros": ["Work from anywhere in India", "Generous annual stipends", "Transparent culture"],
        "cons": ["Asynchronous communication requires high self-discipline"],
        "reddit_summary": "Values interview is an actual eliminator round. Read 'Open company, no bullshit' and other core values thoroughly.",
        "glassdoor_summary": "Unmatched flexibility, strong engineering craft, supportive teams, and great base pay."
    },

    # TIER 2: TARGET TECH INNOVATORS & PRODUCT SERVICES (7.5 - 18 LPA)
    {
        "id": "zoho",
        "name": "Zoho Corporation",
        "category": "target",
        "logo_emoji": "🦎",
        "industry": "SaaS & Cloud Business Suite",
        "ctc_range": "8.5 - 14 LPA",
        "min_cgpa": 6.5,
        "min_aptitude": 70.0,
        "difficulty": "Medium",
        "hiring_status": "Active Campus Drive",
        "rounds_count": 5,
        "interview_rounds": [
            "Round 1: Basic Programming Aptitude & C/Java Output Tracing",
            "Round 2: Basic Programming (Strings, Arrays, Pointers)",
            "Round 3: Advanced Programming (Mini Application / Snake Game / Railway Booking)",
            "Round 4: Technical HR / Core Concepts",
            "Round 5: General HR & Behavioral"
        ],
        "core_skills": ["C", "Java", "Object-Oriented Design", "Data Structures", "Terminal Logic"],
        "locations": ["Chennai", "Tenkasi", "Salem", "Coimbatore"],
        "compensation": {
            "total_ctc": "10.5 LPA",
            "base_salary": "8.5 LPA",
            "variable_bonus": "1.0 LPA",
            "joining_bonus": "1.0 LPA",
            "stocks_esops": "Nil (Private Company profit-sharing)"
        },
        "work_policy": "On-Site Studio Campus",
        "selection_process": {
            "focus": "Pure problem solving without built-in library shortcuts",
            "avg_timeline": "1 - 2 Days (Fast Track)",
            "coding_cutoff": "Clean runnable console application"
        },
        "tech_stack": ["Java", "C", "PostgreSQL", "React", "In-house Infrastructure"],
        "culture_rating": 4.4,
        "work_life_balance": 4.5,
        "pros": ["Zero dependency on outside venture capital", "Superb food and campus facilities", "High job security"],
        "cons": ["Relocation to Tamil Nadu campuses required", "Custom in-house framework learning"],
        "reddit_summary": "Round 3 is the decider: you must build a complete console app from scratch without libraries like ArrayList in C/Java.",
        "glassdoor_summary": "Peaceful work atmosphere, transparent leaders, family-friendly culture and very solid stability."
    },
    {
        "id": "thoughtworks",
        "name": "Thoughtworks",
        "category": "target",
        "logo_emoji": "💡",
        "industry": "High-End Technology & Consulting",
        "ctc_range": "9.5 - 13 LPA",
        "min_cgpa": 7.0,
        "min_aptitude": 72.0,
        "difficulty": "Medium",
        "hiring_status": "Upcoming Drive",
        "rounds_count": 4,
        "interview_rounds": [
            "Round 1: Code Pairing Session (Refactoring & Clean Code)",
            "Round 2: Technical Deep Dive & OOP Design",
            "Round 3: Social Change & Leadership Conversation",
            "Round 4: Leadership Fit & Cultural Dialogue"
        ],
        "core_skills": ["TDD (Test-Driven Development)", "Clean Code", "Design Patterns", "Java / Python / JS", "Agile Methodologies"],
        "locations": ["Bangalore", "Pune", "Chennai", "Hyderabad", "Gurgaon"],
        "compensation": {
            "total_ctc": "11.2 LPA",
            "base_salary": "9.5 LPA",
            "variable_bonus": "1.2 LPA",
            "joining_bonus": "0.5 LPA",
            "stocks_esops": "Nil"
        },
        "work_policy": "Hybrid / Client Site",
        "selection_process": {
            "focus": "Test-Driven Development (TDD) and pairing etiquette",
            "avg_timeline": "2 - 3 Weeks",
            "coding_cutoff": "Clean refactored solution with unit tests"
        },
        "tech_stack": ["Java", "Python", "Node.js", "Docker", "Kubernetes", "AWS"],
        "culture_rating": 4.6,
        "work_life_balance": 4.2,
        "pros": ["Best place to learn industry-standard clean architecture", "Progressive social culture", "High exposure"],
        "cons": ["Consulting model means client projects vary in tech quality"],
        "reddit_summary": "Never write code without tests in the pairing round. Talk out loud and ask interviewer for feedback continuously.",
        "glassdoor_summary": "Exceptional learning curve, flat hierarchy, brilliant engineers, and deep engineering discipline."
    },
    {
        "id": "juspay",
        "name": "Juspay",
        "category": "target",
        "logo_emoji": "⚡",
        "industry": "FinTech Payments Infrastructure",
        "ctc_range": "15 - 27 LPA",
        "min_cgpa": 7.0,
        "min_aptitude": 78.0,
        "difficulty": "High",
        "hiring_status": "Active National Challenge",
        "rounds_count": 4,
        "interview_rounds": [
            "Round 1: Online Assessment (3 Graph & Tree Problems)",
            "Round 2: 24-Hour Hackathon / Functional Coding Assignment",
            "Round 3: Technical Deep-Dive on Assignment & Concurrency",
            "Round 4: Founder / Leadership Fit"
        ],
        "core_skills": ["Functional Programming (Haskell / PureScript)", "Algorithms", "Graph Theory", "High Concurrency", "Java / C++"],
        "locations": ["Bangalore"],
        "compensation": {
            "total_ctc": "21.0 LPA",
            "base_salary": "14.0 LPA",
            "variable_bonus": "2.0 LPA",
            "joining_bonus": "2.0 LPA",
            "stocks_esops": "3.0 LPA"
        },
        "work_policy": "In-Office Bangalore Hub",
        "selection_process": {
            "focus": "Graph theory, functional programming paradigms, low latency",
            "avg_timeline": "2 - 3 Weeks",
            "coding_cutoff": "Passing complex graph edge cases"
        },
        "tech_stack": ["Haskell", "PureScript", "Clojure", "Rust", "PostgreSQL", "Kafka"],
        "culture_rating": 4.2,
        "work_life_balance": 3.2,
        "pros": ["Engineers handle over 100M+ transactions daily", "Deep functional programming expertise"],
        "cons": ["Challenging work hours during UPI peak events"],
        "reddit_summary": "Graph BFS/DFS with cycle detection and maximum flow questions dominate their hiring rounds.",
        "glassdoor_summary": "Cutting-edge payment architecture, brilliant peer group, high impact on India's digital economy."
    },
    {
        "id": "persistent",
        "name": "Persistent Systems",
        "category": "target",
        "logo_emoji": "⚙️",
        "industry": "Digital Engineering & Cloud Modernization",
        "ctc_range": "7.5 - 9.5 LPA",
        "min_cgpa": 6.8,
        "min_aptitude": 68.0,
        "difficulty": "Medium",
        "hiring_status": "Campus Drive Active",
        "rounds_count": 3,
        "interview_rounds": [
            "Online Assessment: Aptitude, English, and 2 Coding Problems",
            "Advanced Technical Interview: DSA, DBMS, Cloud Basics",
            "HR & Managerial Discussion"
        ],
        "core_skills": ["Java", "Python", "SQL", "Data Structures", "Cloud Architecture"],
        "locations": ["Pune", "Hyderabad", "Goa", "Bangalore"],
        "compensation": {
            "total_ctc": "8.5 LPA",
            "base_salary": "7.2 LPA",
            "variable_bonus": "0.8 LPA",
            "joining_bonus": "0.5 LPA",
            "stocks_esops": "Nil"
        },
        "work_policy": "Hybrid (2 Days Office / 3 Days Remote)",
        "selection_process": {
            "focus": "Balanced aptitude, strong SQL queries, and core DSA",
            "avg_timeline": "1 - 2 Weeks",
            "coding_cutoff": "1.5/2 coding problems solved"
        },
        "tech_stack": ["Java", "Spring Boot", "AWS", "Angular", "MySQL"],
        "culture_rating": 4.1,
        "work_life_balance": 4.0,
        "pros": ["Good project diversity in health tech and banking", "Friendly management", "Decent entry package"],
        "cons": ["Moderate salary increments post Year 2"],
        "reddit_summary": "Brush up on SQL joins, indexing, and standard string/array manipulation for their technical round.",
        "glassdoor_summary": "Stable company, good work-life balance, collaborative managers, and supportive team leads."
    },

    # TIER 3: SAFE & SCALABLE HIGH-INTAKE MASS RECRUITERS (4 - 9.5 LPA)
    {
        "id": "tcs",
        "name": "Tata Consultancy Services (TCS)",
        "category": "safe",
        "logo_emoji": "🏢",
        "industry": "Global IT Services & Consulting",
        "ctc_range": "3.6 - 9.0 LPA (Ninja / Digital / Prime)",
        "min_cgpa": 6.0,
        "min_aptitude": 60.0,
        "difficulty": "Moderate",
        "hiring_status": "National Qualifier Test (NQT)",
        "rounds_count": 3,
        "interview_rounds": [
            "TCS NQT: Numerical, Reasoning, Verbal + 2 Coding Problems",
            "Technical Interview: C/Java/Python, DBMS, Academic Projects",
            "Managerial & HR Interview"
        ],
        "core_skills": ["C / Java / Python", "SQL & DBMS", "Aptitude Fundamentals", "Object-Oriented Programming", "Communication"],
        "locations": ["Chennai", "Bangalore", "Mumbai", "Hyderabad", "Kolkata", "Delhi NCR"],
        "compensation": {
            "total_ctc": "7.2 LPA (Digital Tier)",
            "base_salary": "6.2 LPA",
            "variable_bonus": "0.6 LPA",
            "joining_bonus": "0.4 LPA",
            "stocks_esops": "Nil"
        },
        "work_policy": "Hybrid / Campus Office",
        "selection_process": {
            "focus": "High speed and accuracy on NQT aptitude questions and clean syntax",
            "avg_timeline": "2 - 4 Weeks",
            "coding_cutoff": "1/2 coding questions for Digital tier"
        },
        "tech_stack": ["Java", "Python", "SQL", "Cloud", "Spring", "Angular"],
        "culture_rating": 4.0,
        "work_life_balance": 4.1,
        "pros": ["Unmatched job security in Tata Group", "Massive global mobility potential", "Continuous certification incentives"],
        "cons": ["Large organization hierarchy", "Project allocation can take time"],
        "reddit_summary": "Aptitude speed is paramount in NQT. Practice non-verbal reasoning and elementary math speed tricks.",
        "glassdoor_summary": "Very stable employer, great safety net for fresh graduates, and reliable on-time salary."
    },
    {
        "id": "infosys",
        "name": "Infosys",
        "category": "safe",
        "logo_emoji": "🏢",
        "industry": "Global Next-Gen Digital Services",
        "ctc_range": "3.6 - 9.5 LPA (SE / DSE / Specialist)",
        "min_cgpa": 6.0,
        "min_aptitude": 60.0,
        "difficulty": "Moderate",
        "hiring_status": "Active Campus & InfyTQ",
        "rounds_count": 3,
        "interview_rounds": [
            "Online Test: Reasoning, Quantitative, Verbal, Pseudocode, Puzzle Solving",
            "Technical Interview: Core CS Subjects, Data Structures, Resume Projects",
            "HR Discussion & Verification"
        ],
        "core_skills": ["Java / Python", "OOP Concepts", "Data Structures", "SQL", "Basic Web Tech"],
        "locations": ["Bangalore", "Mysore", "Pune", "Chennai", "Hyderabad"],
        "compensation": {
            "total_ctc": "6.8 LPA (DSE Tier)",
            "base_salary": "5.8 LPA",
            "variable_bonus": "0.6 LPA",
            "joining_bonus": "0.4 LPA",
            "stocks_esops": "Nil"
        },
        "work_policy": "Hybrid Working",
        "selection_process": {
            "focus": "Pseudocode debugging and quantitative reasoning",
            "avg_timeline": "2 - 3 Weeks",
            "coding_cutoff": "Pseudocode accuracy above 70%"
        },
        "tech_stack": ["Java", "Python", ".NET", "AWS", "React", "Oracle"],
        "culture_rating": 3.9,
        "work_life_balance": 3.9,
        "pros": ["Mysore training campus is world class", "Structured foundational training", "Strong brand recognition"],
        "cons": ["Service agreement bond terms", "Strict shift schedules on support accounts"],
        "reddit_summary": "The pseudocode section has negative marking in some editions. Be very certain before guessing output loops.",
        "glassdoor_summary": "World-class Mysore training facility, helpful peers, clear career bands for early starters."
    },
    {
        "id": "accenture",
        "name": "Accenture",
        "category": "safe",
        "logo_emoji": "🌐",
        "industry": "Strategy, Consulting & Cloud Solutions",
        "ctc_range": "4.5 - 6.5 LPA (ASE / Advanced ASE)",
        "min_cgpa": 6.5,
        "min_aptitude": 62.0,
        "difficulty": "Moderate",
        "hiring_status": "Campus Drive Active",
        "rounds_count": 3,
        "interview_rounds": [
            "Cognitive & Technical Assessment (Aptitude, Cloud, MS Office, Security)",
            "Coding Assessment (2 Questions: Strings, Arrays)",
            "Communication Assessment (Automated AI Speaking & Listening)",
            "Virtual Interview: Technical & Behavioral"
        ],
        "core_skills": ["Python / Java / C++", "Cloud Computing Basics", "Database Queries", "Communication", "Problem Solving"],
        "locations": ["Bangalore", "Hyderabad", "Pune", "Chennai", "Gurgaon"],
        "compensation": {
            "total_ctc": "6.5 LPA (Advanced ASE)",
            "base_salary": "5.6 LPA",
            "variable_bonus": "0.6 LPA",
            "joining_bonus": "0.3 LPA",
            "stocks_esops": "Nil"
        },
        "work_policy": "Flexible Hybrid",
        "selection_process": {
            "focus": "Communication clarity + clean basic coding syntax",
            "avg_timeline": "2 - 3 Weeks",
            "coding_cutoff": "Passing both coding test cases"
        },
        "tech_stack": ["Java", "Python", "Cloud (AWS/Azure)", "Salesforce", "ServiceNow"],
        "culture_rating": 4.1,
        "work_life_balance": 3.8,
        "pros": ["Modern technology practice adoption", "Diverse team culture", "Fast career progression paths"],
        "cons": ["Fast rotations across enterprise clients"],
        "reddit_summary": "Do not overlook the communication round. Practice speaking into a quiet microphone with clear enunciation.",
        "glassdoor_summary": "Vibrant workplace, excellent learning budget for cloud certifications, great modern offices."
    },
    {
        "id": "cognizant",
        "name": "Cognizant",
        "category": "safe",
        "logo_emoji": "💼",
        "industry": "Digital Business & Enterprise Systems",
        "ctc_range": "4.0 - 6.75 LPA (GenC / GenC Elevate / Next)",
        "min_cgpa": 6.0,
        "min_aptitude": 60.0,
        "difficulty": "Moderate",
        "hiring_status": "Active National Qualifier",
        "rounds_count": 3,
        "interview_rounds": [
            "Round 1: Quantitative, Analytical, Verbal, and Domain Coding",
            "Round 2: Technical Interview (Code Debugging & Core CS)",
            "Round 3: HR & Document Verification"
        ],
        "core_skills": ["C / Java", "SQL", "Web Basics", "Aptitude", "Debugging"],
        "locations": ["Chennai", "Coimbatore", "Bangalore", "Kolkata", "Hyderabad"],
        "compensation": {
            "total_ctc": "5.5 LPA (GenC Elevate)",
            "base_salary": "4.8 LPA",
            "variable_bonus": "0.4 LPA",
            "joining_bonus": "0.3 LPA",
            "stocks_esops": "Nil"
        },
        "work_policy": "Hybrid (3 Days Office)",
        "selection_process": {
            "focus": "Core fundamentals and project walkthrough",
            "avg_timeline": "2 - 3 Weeks",
            "coding_cutoff": "1/2 coding questions for Elevate tier"
        },
        "tech_stack": ["Java", "SQL", "React", "Python", "Cloud"],
        "culture_rating": 3.9,
        "work_life_balance": 3.9,
        "pros": ["Great entry point for freshers", "Clear technical bands", "Supportive training cohort"],
        "cons": ["Notice period is 90 days"],
        "reddit_summary": "Be ready to explain your final year project end-to-end including database schema design.",
        "glassdoor_summary": "Friendly peers, structured onboarding, lots of projects across healthcare and banking."
    }
]

# Placement Drive schedule fixtures
PLACEMENT_DRIVES = [
    {
        "id": "drive_google_2027",
        "company_name": "Google",
        "logo_emoji": "🌐",
        "role_title": "Software Engineering Graduate (2026/2027)",
        "ctc": "36 - 55 LPA",
        "drive_type": "Campus & National Off-Campus",
        "event_date": "2026-12-10",
        "event_time": "10:00 AM IST",
        "registration_deadline": "2026-11-30",
        "eligibility_criteria": "CGPA 8.0+, No active backlogs, CSE/IT/ECE",
        "description": "Online coding assessment followed by 3 algorithmic DSA rounds."
    },
    {
        "id": "drive_amazon_2027",
        "company_name": "Amazon",
        "logo_emoji": "📦",
        "role_title": "SDE-1 (Full-Time & 6-Month Intern)",
        "ctc": "32 - 45 LPA",
        "drive_type": "National Placement Drive",
        "event_date": "2026-12-15",
        "event_time": "02:00 PM IST",
        "registration_deadline": "2026-12-05",
        "eligibility_criteria": "CGPA 7.5+, B.Tech/M.Tech all branches with coding proficiency",
        "description": "Amazon Online Assessment slot with debugging and data structures."
    },
    {
        "id": "drive_tcs_nqt",
        "company_name": "Tata Consultancy Services (TCS)",
        "logo_emoji": "🏢",
        "role_title": "TCS NQT National Drive (Ninja & Digital Tiers)",
        "ctc": "3.6 - 9.0 LPA",
        "drive_type": "National Qualifier Test (NQT)",
        "event_date": "2026-12-20",
        "event_time": "09:30 AM IST",
        "registration_deadline": "2026-12-08",
        "eligibility_criteria": "CGPA 6.0+, Up to 1 backlog permitted at registration",
        "description": "Comprehensive aptitude and coding slot with Digital and Prime upgrades."
    },
    {
        "id": "drive_zoho_2027",
        "company_name": "Zoho Corporation",
        "logo_emoji": "🦎",
        "role_title": "Software Developer (Level 1 to 3)",
        "ctc": "8.5 - 14.0 LPA",
        "drive_type": "Campus Pooled Drive",
        "event_date": "2027-01-05",
        "event_time": "11:00 AM IST",
        "registration_deadline": "2026-12-24",
        "eligibility_criteria": "No minimum CGPA required; pure programming skill evaluation",
        "description": "Fast-track 5-round programming drive with console application building."
    },
    {
        "id": "drive_atlassian_2027",
        "company_name": "Atlassian",
        "logo_emoji": "🔷",
        "role_title": "Associate Software Engineer (Team Anywhere)",
        "ctc": "30 - 42 LPA",
        "drive_type": "Online National Challenge",
        "event_date": "2027-01-12",
        "event_time": "04:00 PM IST",
        "registration_deadline": "2027-01-02",
        "eligibility_criteria": "CGPA 7.0+, Strong OOP and web/cloud interest",
        "description": "HackerRank OA followed by paired architecture refactoring sessions."
    },
    {
        "id": "drive_accenture_2027",
        "company_name": "Accenture",
        "logo_emoji": "🌐",
        "role_title": "Advanced Application Software Engineer",
        "ctc": "4.5 - 6.5 LPA",
        "drive_type": "Campus Placement Drive",
        "event_date": "2027-01-18",
        "event_time": "01:30 PM IST",
        "registration_deadline": "2027-01-10",
        "eligibility_criteria": "CGPA 6.5+, All B.E/B.Tech engineering streams eligible",
        "description": "Cognitive assessment, coding round, and automated AI communication test."
    }
]

# Baseline standard document verification checklist
STANDARD_DOCUMENT_CHECKLIST: List[Dict[str, Any]] = [
    {
        "id": "doc_10th_marksheet",
        "title": "10th Standard / SSC Marksheet",
        "description": "Original marksheet verifying Date of Birth and secondary education aggregate (60%+ required for most recruiters).",
        "is_ready": True,
        "importance": "Critical",
        "category": "Academics"
    },
    {
        "id": "doc_12th_marksheet",
        "title": "12th Standard / HSC / Diploma Marksheet",
        "description": "Higher secondary certificate confirming Math/Physics eligibility and academic continuity with zero gaps.",
        "is_ready": True,
        "importance": "Critical",
        "category": "Academics"
    },
    {
        "id": "doc_sem_marksheets",
        "title": "All Semester Grade Cards (Sem 1 to current)",
        "description": "Official transcript or internet copies attested by Controller of Examinations confirming current CGPA.",
        "is_ready": True,
        "importance": "Critical",
        "category": "Academics"
    },
    {
        "id": "doc_govt_id",
        "title": "Government Photo ID (Aadhaar Card / PAN / Passport)",
        "description": "Clear government proof with matching name spelling for security gate pass and background verification (BGV).",
        "is_ready": True,
        "importance": "Critical",
        "category": "Identity"
    },
    {
        "id": "doc_pan_card",
        "title": "Permanent Account Number (PAN Card)",
        "description": "Mandatory for payroll registration and stipend processing prior to internship onboarding.",
        "is_ready": False,
        "importance": "Important",
        "category": "Identity"
    },
    {
        "id": "doc_resume_locked",
        "title": "Standardized 1-Page Placement Resume (PDF)",
        "description": "Clean single-page ATS-verified resume without typos, verified project links, and accurate CGPA.",
        "is_ready": True,
        "importance": "Critical",
        "category": "Portfolio"
    },
    {
        "id": "doc_portfolio_link",
        "title": "Live Interactive Portfolio Website Link",
        "description": "Working public portfolio URL displaying projects, skills, and certifications for interviewer review.",
        "is_ready": True,
        "importance": "Important",
        "category": "Portfolio"
    },
    {
        "id": "doc_github_code",
        "title": "Verified GitHub Profile with Pinned Repositories",
        "description": "Clean commit history on key projects with README documentation and live demo URLs.",
        "is_ready": True,
        "importance": "Important",
        "category": "Portfolio"
    },
    {
        "id": "doc_bonafide_cert",
        "title": "College Bonafide / Provisional Certificate",
        "description": "Issued by college Dean/Principal stating expected year of graduation and medium of instruction.",
        "is_ready": False,
        "importance": "Recommended",
        "category": "Legal"
    },
    {
        "id": "doc_passport_photos",
        "title": "Formal Passport Size Photographs (Digital & Print)",
        "description": "White background formal headshots for enterprise ID card generation and joining dossier.",
        "is_ready": True,
        "importance": "Recommended",
        "category": "Identity"
    }
]

# In-memory candidate mock test store (keyed by candidate_id)
_CANDIDATE_MOCKS_STORE: Dict[str, List[Dict[str, Any]]] = {}
_CANDIDATE_DOCS_STORE: Dict[str, List[Dict[str, Any]]] = {}


def generate_google_calendar_url(event: Dict[str, Any]) -> str:
    """Constructs a 1-click Google Calendar event creation URL."""
    title = f"{event['company_name']} - {event['role_title']} ({event['drive_type']})"
    details = (
        f"Event: {title}\n"
        f"CTC Package: {event['ctc']}\n"
        f"Eligibility: {event['eligibility_criteria']}\n"
        f"Registration Deadline: {event['registration_deadline']}\n\n"
        f"Details: {event['description']}\n\n"
        "Managed via AI Recruiter Placement Compass"
    )
    location = "Online / Campus Placement Lab"

    # Compute start & end time
    try:
        dt = datetime.strptime(f"{event['event_date']} 10:00", "%Y-%m-%d %H:%M")
    except Exception:
        dt = datetime.now() + timedelta(days=7)

    dt_start = dt.strftime("%Y%m%dT%H%M00Z")
    dt_end = (dt + timedelta(hours=3)).strftime("%Y%m%dT%H%M00Z")

    params = {
        "action": "TEMPLATE",
        "text": title,
        "details": details,
        "location": location,
        "dates": f"{dt_start}/{dt_end}",
    }
    return f"https://calendar.google.com/calendar/render?{urllib.parse.urlencode(params)}"


def get_all_benchmark_companies() -> List[Dict[str, Any]]:
    """Returns all curated benchmark companies."""
    return BENCHMARK_COMPANIES


def predict_company_matches(
    cgpa: float,
    aptitude_score: float,
    coding_level: str = "intermediate",
    branch: str = "Computer Science / IT",
    target_role: str = "Software Engineer"
) -> Dict[str, Any]:
    """
    Evaluates candidate credentials against real placement cutoffs and assigns companies
    into Safe, Target, and Dream categories with concrete match percentages and skill gaps.
    """
    coding_multipliers = {
        "beginner": 0.70,
        "intermediate": 0.85,
        "advanced": 1.0
    }
    coding_factor = coding_multipliers.get(coding_level.lower(), 0.85)

    safe_list = []
    target_list = []
    dream_list = []

    for comp in BENCHMARK_COMPANIES:
        # 1. Eligibility Check
        cgpa_gap = max(0.0, comp["min_cgpa"] - cgpa)
        apt_gap = max(0.0, comp["min_aptitude"] - aptitude_score)

        # 2. Match Score calculation (0 - 100)
        cgpa_score = max(0.0, min(100.0, (cgpa / comp["min_cgpa"]) * 40.0))
        apt_score = max(0.0, min(100.0, (aptitude_score / comp["min_aptitude"]) * 40.0))
        skill_score = 20.0 * coding_factor

        match_pct = int(min(98, round(cgpa_score + apt_score + skill_score)))

        # Skill gap identification
        gaps = []
        if cgpa_gap > 0:
            gaps.append(f"CGPA is {cgpa:.2f} (Cutoff: {comp['min_cgpa']:.1f})")
        if apt_gap > 0:
            gaps.append(f"Aptitude score is {aptitude_score:.0f}% (Cutoff: {comp['min_aptitude']:.0f}%)")
        if comp["category"] == "dream" and coding_level == "beginner":
            gaps.append("Requires Advanced DSA (Dynamic Programming, Graphs, System Design)")
        elif comp["category"] == "target" and coding_level == "beginner":
            gaps.append("Requires Intermediate Coding (Trees, Recursion, OOP Design)")

        item = dict(comp)
        item["match_percentage"] = match_pct
        item["skill_gaps"] = gaps

        # Tier sorting
        cat = comp["category"]
        if cat == "safe":
            safe_list.append(item)
        elif cat == "target":
            target_list.append(item)
        else:
            dream_list.append(item)

    # Sort each tier by match percentage descending
    safe_list.sort(key=lambda x: x["match_percentage"], reverse=True)
    target_list.sort(key=lambda x: x["match_percentage"], reverse=True)
    dream_list.sort(key=lambda x: x["match_percentage"], reverse=True)

    summary_guidance = (
        f"Based on your {cgpa:.2f} CGPA and {aptitude_score:.0f}% aptitude benchmark, you are strongly positioned "
        f"for {len(safe_list)} Safe companies ({safe_list[0]['ctc_range']}) and competitive for {len(target_list)} Target tech firms. "
        "Strengthening Dynamic Programming and System Design will unlock Tier-1 Dream product offers."
    )

    return {
        "candidate_cgpa": cgpa,
        "candidate_aptitude": aptitude_score,
        "total_evaluated": len(BENCHMARK_COMPANIES),
        "safe_matches": safe_list,
        "target_matches": target_list,
        "dream_matches": dream_list,
        "summary_guidance": summary_guidance
    }


def list_all_companies() -> List[Dict[str, Any]]:
    """Returns directory of all benchmark companies available for comparison."""
    return [
        {
            "id": c["id"],
            "name": c["name"],
            "category": c["category"],
            "logo_emoji": c["logo_emoji"],
            "industry": c["industry"],
            "ctc_range": c["ctc_range"],
            "difficulty": c["difficulty"],
            "min_cgpa": c["min_cgpa"],
            "min_aptitude": c["min_aptitude"],
            "locations": c["locations"]
        }
        for c in BENCHMARK_COMPANIES
    ]


def compare_companies(company_ids: List[str]) -> List[Dict[str, Any]]:
    """Generates 3-way comparative matrix for selected company IDs."""
    results = []
    comp_map = {c["id"]: c for c in BENCHMARK_COMPANIES}

    for cid in company_ids[:3]:
        comp = comp_map.get(cid)
        if comp:
            results.append({
                "id": comp["id"],
                "name": comp["name"],
                "logo_emoji": comp["logo_emoji"],
                "tier": comp["category"].upper(),
                "compensation": comp["compensation"],
                "work_policy": comp["work_policy"],
                "selection_process": comp["selection_process"],
                "tech_stack": comp["tech_stack"],
                "culture_rating": comp["culture_rating"],
                "work_life_balance": comp["work_life_balance"],
                "pros": comp["pros"],
                "cons": comp["cons"],
                "reddit_summary": comp["reddit_summary"],
                "glassdoor_summary": comp["glassdoor_summary"]
            })

    return results


def get_placement_drives() -> List[Dict[str, Any]]:
    """Returns live and upcoming placement drive timeline with Google Calendar URLs."""
    drives = []
    for d in PLACEMENT_DRIVES:
        item = dict(d)
        item["google_calendar_url"] = generate_google_calendar_url(item)
        item["ics_download_filename"] = f"{item['company_name'].lower().replace(' ', '_')}_drive.ics"
        drives.append(item)
    return drives


def get_candidate_mock_trajectory(candidate_id: str) -> Dict[str, Any]:
    """Returns candidate's mock test score history or generates realistic seed trajectory."""
    mocks = _CANDIDATE_MOCKS_STORE.get(candidate_id)
    if not mocks:
        # Default realistic progression seed for candidates
        mocks = [
            {
                "id": str(uuid.uuid4())[:8],
                "test_name": "TCS NQT National Mock #1",
                "date": (datetime.now() - timedelta(days=21)).strftime("%Y-%m-%d"),
                "quantitative_score": 64.0,
                "logical_score": 70.0,
                "verbal_score": 68.0,
                "technical_score": 60.0,
                "total_percentage": 65.5,
                "max_score": 100.0,
                "notes": "Good logical speed; need to improve time-and-work math questions."
            },
            {
                "id": str(uuid.uuid4())[:8],
                "test_name": "Infosys Comprehensive Assessment #2",
                "date": (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d"),
                "quantitative_score": 72.0,
                "logical_score": 76.0,
                "verbal_score": 74.0,
                "technical_score": 68.0,
                "total_percentage": 72.5,
                "max_score": 100.0,
                "notes": "Pseudocode loops answered accurately; improved time management."
            },
            {
                "id": str(uuid.uuid4())[:8],
                "test_name": "Cognizant GenC Elevate Diagnostic #3",
                "date": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
                "quantitative_score": 78.0,
                "logical_score": 82.0,
                "verbal_score": 80.0,
                "technical_score": 75.0,
                "total_percentage": 78.8,
                "max_score": 100.0,
                "notes": "Strong performance. Met cutoffs for TCS Digital and Persistent Systems."
            },
            {
                "id": str(uuid.uuid4())[:8],
                "test_name": "Amazon SDE-1 Diagnostic Mock #4",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "quantitative_score": 84.0,
                "logical_score": 86.0,
                "verbal_score": 82.0,
                "technical_score": 80.0,
                "total_percentage": 83.0,
                "max_score": 100.0,
                "notes": "Cleared Tier-2 cutoffs (Zoho, Thoughtworks). Nearing Tier-1 benchmark."
            }
        ]
        _CANDIDATE_MOCKS_STORE[candidate_id] = mocks

    scores = [m["total_percentage"] for m in mocks]
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0.0
    latest = scores[-1] if scores else 0.0
    highest = max(scores) if scores else 0.0

    cleared = []
    if highest >= 60.0: cleared.append("TCS Ninja (60%)")
    if highest >= 60.0: cleared.append("Infosys SE (60%)")
    if highest >= 62.0: cleared.append("Accenture ASE (62%)")
    if highest >= 70.0: cleared.append("TCS Digital (70%)")
    if highest >= 70.0: cleared.append("Zoho Corporation (70%)")
    if highest >= 72.0: cleared.append("Thoughtworks (72%)")
    if highest >= 80.0: cleared.append("Amazon OA Benchmark (80%)")
    if highest >= 85.0: cleared.append("Google OA Benchmark (85%)")

    readiness = "Tier-1 Ready (Dream Product)" if latest >= 82.0 else ("Tier-2 Ready (Target Innovators)" if latest >= 70.0 else "Tier-3 Ready (Safe Enablers)")

    return {
        "total_attempts": len(mocks),
        "average_score": avg_score,
        "latest_score": latest,
        "highest_score": highest,
        "readiness_level": readiness,
        "company_benchmarks_cleared": cleared,
        "attempts": mocks
    }


def add_candidate_mock_test(candidate_id: str, entry: Dict[str, Any]) -> Dict[str, Any]:
    """Saves a new mock test score and returns updated trajectory."""
    if candidate_id not in _CANDIDATE_MOCKS_STORE:
        get_candidate_mock_trajectory(candidate_id)

    new_id = str(uuid.uuid4())[:8]
    item = {
        "id": new_id,
        "test_name": entry.get("test_name") or "Placement Mock Attempt",
        "date": entry.get("date") or datetime.now().strftime("%Y-%m-%d"),
        "quantitative_score": float(entry.get("quantitative_score", 0)),
        "logical_score": float(entry.get("logical_score", 0)),
        "verbal_score": float(entry.get("verbal_score", 0)),
        "technical_score": float(entry.get("technical_score", 0)),
        "total_percentage": float(entry.get("total_percentage", 0)),
        "max_score": float(entry.get("max_score", 100)),
        "notes": entry.get("notes", "")
    }

    _CANDIDATE_MOCKS_STORE[candidate_id].append(item)
    return get_candidate_mock_trajectory(candidate_id)


def get_candidate_document_checklist(candidate_id: str) -> Dict[str, Any]:
    """Returns candidate document readiness checklist."""
    docs = _CANDIDATE_DOCS_STORE.get(candidate_id)
    if not docs:
        docs = [dict(d) for d in STANDARD_DOCUMENT_CHECKLIST]
        _CANDIDATE_DOCS_STORE[candidate_id] = docs

    ready_count = sum(1 for d in docs if d["is_ready"])
    pct = round((ready_count / len(docs)) * 100, 1) if docs else 0.0

    return {
        "total_documents": len(docs),
        "ready_count": ready_count,
        "readiness_percentage": pct,
        "checklist": docs
    }


def toggle_candidate_document_status(candidate_id: str, doc_id: str, is_ready: bool) -> Dict[str, Any]:
    """Updates ready status of a document item."""
    if candidate_id not in _CANDIDATE_DOCS_STORE:
        get_candidate_document_checklist(candidate_id)

    docs = _CANDIDATE_DOCS_STORE[candidate_id]
    for d in docs:
        if d["id"] == doc_id:
            d["is_ready"] = is_ready
            break

    return get_candidate_document_checklist(candidate_id)


def get_company_review_insights(company_id: str) -> Dict[str, Any]:
    """Returns segregated Reddit vs Glassdoor reviews for a company."""
    comp = next((c for c in BENCHMARK_COMPANIES if c["id"] == company_id), None)
    if not comp:
        comp = BENCHMARK_COMPANIES[0]

    return {
        "company_id": comp["id"],
        "company_name": comp["name"],
        "logo_emoji": comp["logo_emoji"],
        "tier": comp["category"].upper(),
        "culture_rating": comp["culture_rating"],
        "work_life_balance": comp["work_life_balance"],
        "reddit_reviews": {
            "source": "Reddit & Blind Community (Unfiltered Candidate Feedback)",
            "summary": comp["reddit_summary"],
            "difficulty_rating": comp["difficulty"],
            "insider_tips": [
                f"Coding problems focus on {', '.join(comp['core_skills'][:3])}.",
                f"Typical interview process takes {comp['selection_process']['avg_timeline']}.",
                "Expect live code execution and testing for all boundary conditions."
            ]
        },
        "glassdoor_reviews": {
            "source": "Glassdoor & AmbitionBox (Verified Employee Ratings)",
            "summary": comp["glassdoor_summary"],
            "overall_rating": f"{comp['culture_rating']} / 5.0",
            "work_life_rating": f"{comp['work_life_balance']} / 5.0",
            "verified_pros": comp["pros"],
            "verified_cons": comp["cons"]
        }
    }


# =====================================================================
# SCHOOL CAREER GUIDANCE DATABASE & SERVICES (AFTER 10TH & 12TH) — TAMIL NADU FOCUS
# =====================================================================

SCHOOL_CAREER_PATHS: List[Dict[str, Any]] = [
    # ==================== A. DIRECT NEXT STEPS AFTER 10TH GRADE (SSLC) ====================
    {
        "id": "hsc_stream_selection_10th",
        "title": "11th & 12th Higher Secondary Stream Chooser (Tamil Nadu Board / CBSE)",
        "category": "arts_science",
        "grade_level": "after_10th",
        "icon_emoji": "🏫",
        "tagline": "Choose the Right 11th Group (Bio-Maths, Computer Science, Commerce, Arts) to Unlock Your College Degree",
        "duration": "2 Years (Classes 11 & 12)",
        "eligibility": "10th Standard (SSLC) Pass from Tamil Nadu State Board, Matriculation, CBSE, or ICSE.",
        "entrance_exams": [
            {"name": "Tamil Nadu Higher Secondary School Admissions", "level": "State", "official_portal": "https://www.tnschools.gov.in", "description": "Merit-based admission into Tamil Nadu Govt, Govt-Aided, and Private Higher Secondary Schools based on 10th SSLC marks."}
        ],
        "top_colleges": [
            "Tamil Nadu Government Model Higher Secondary Schools (Across all 38 districts)",
            "Presidency Girls / Boys Higher Secondary School, Chennai",
            "St. Bede's / Don Bosco / Santhome Higher Secondary School, Chennai",
            "PSG Sarvajana Higher Secondary School, Coimbatore"
        ],
        "admission_procedure": "Submit 10th mark sheet at school -> Choose preferred Subject Group: Group 1 (Bio-Maths) unlocks Engineering + MBBS + Agriculture; Group 2 (Computer Science & Maths) unlocks B.Tech CSE + Robotics; Group 3 (Pure Science) unlocks Medical + Veterinary + Pharmacy; Group 4 (Commerce & Accountancy) unlocks B.Com + CA + Law; Group 5 (Arts) unlocks Law + Civil Services.",
        "estimated_fees": {
            "govt_school": "100% FREE (Free Tuition, Free Textbooks, Free Uniforms, Free Bicycle & Midday Meals)",
            "govt_aided_school": "₹500 - ₹2,000 / year",
            "private_matric_cbse": "₹25,000 - ₹75,000 / year"
        },
        "scholarships": [
            "Tamil Nadu 7.5% Horizontal Reservation eligibility in professional colleges for students studying in TN Govt schools from 6th to 12th",
            "Pudhumai Penn & Tamil Puthalvan scheme eligibility for college (₹1,000/month after completing 12th)",
            "National Means-cum-Merit Scholarship (NMMS) & Chief Minister's Talent Exam Award"
        ],
        "career_opportunities": [
            "Opens pathway to B.E / B.Tech, MBBS, BDS, Nursing, B.Pharm, TNAU Agriculture, TANUVAS Veterinary",
            "Opens pathway to B.Com, Chartered Accountancy (CA), CMA, CS, Corporate Banking",
            "Opens pathway to 5-Year Integrated Honours Law (SOEL TNDALU & TNNLU)",
            "Direct eligibility for NDA Officer Exam, Indian Air Force, and TNPSC Group 4"
        ],
        "starting_salary_range": "Foundation stage preparing for ₹4.5 LPA - ₹42.0 LPA university career pathways",
        "future_study_options": ["Undergraduate Degrees in Engineering, Medical, Law, Commerce, Arts & Science"],
        "key_skills_needed": ["Conceptual Understanding in Science & Maths", "Consistent Daily Homework", "Time Management", "Language Fluency in Tamil & English"]
    },
    {
        "id": "diploma_mechanical_civil_eee",
        "title": "3-Year Polytechnic Diploma in Core Engineering (DOTE Tamil Nadu)",
        "category": "diploma_polytechnic",
        "grade_level": "after_10th",
        "icon_emoji": "🔧",
        "tagline": "Practical Core Engineering, CNC Machining, EV Manufacturing & Lateral Entry into 2nd Year B.E",
        "duration": "3 Years (6 Semesters of Practical Workshop & Laboratory Training)",
        "eligibility": "10th Standard (SSLC) Pass with Science & Mathematics from Tamil Nadu State Board or equivalent. Zero entrance exam required.",
        "entrance_exams": [
            {"name": "DOTE Tamil Nadu Centralized Polytechnic Admissions", "level": "State", "official_portal": "https://www.tnpoly.in", "description": "Directorate of Technical Education (DOTE) single-window merit admission based purely on 10th SSLC marks."}
        ],
        "top_colleges": [
            "Central Polytechnic College (CPT), Taramani, Chennai (Est. 1916)",
            "PSG Polytechnic College (Autonomous), Coimbatore",
            "Murugappa Polytechnic College (Autonomous), Avadi, Chennai",
            "Government Polytechnic College, Coimbatore",
            "Government Polytechnic College, Trichy",
            "Ramakrishna Mission Polytechnic College, Mylapore, Chennai"
        ],
        "admission_procedure": "Register online at tnpoly.in right after 10th results -> Select branch & college choices -> Merit rank list based on 10th marks -> Online seat allotment. 7.5% Horizontal Reservation for TN Govt School students with 100% Free Tuition, Hostel & Mess. Pudhumai Penn & Tamil Puthalvan ₹1,000/mo applies. After diploma, get Direct 2nd Year Lateral Entry into B.E at Anna University / PSG Tech via TNEA!",
        "estimated_fees": {
            "govt_polytechnic": "₹2,482 / year (Fixed by Govt of Tamil Nadu — 100% Free under 7.5% quota)",
            "govt_aided_polytechnic": "₹10,500 - ₹18,000 / year (PSG Poly / Murugappa Poly)",
            "private_polytechnic": "₹35,000 - ₹65,000 / year"
        },
        "scholarships": [
            "Tamil Nadu 7.5% Govt School Horizontal Reservation (100% Free Tuition, Hostel, Mess)",
            "Pudhumai Penn Scheme (₹1,000/month for female students from TN Govt schools)",
            "Tamil Puthalvan Scheme (₹1,000/month for male students from TN Govt schools)",
            "Free Government Laptop Scheme for Govt & Aided Polytechnic students",
            "AICTE Pragati Scholarship for Girls in Technical Diplomas (₹50,000/year)"
        ],
        "career_opportunities": [
            "Junior Engineer (JE) in Southern Railway (RRB Chennai / Trichy)",
            "Production & Maintenance Technician (Hyundai, Ashok Leyland, TVS, Royal Enfield)",
            "CNC Programmer & Tool Room Specialist in Ambattur & Sriperumbudur Industrial Belts",
            "Substation & Distribution Technician in TANGEDCO / TANTRANSCO"
        ],
        "starting_salary_range": "₹3.2 LPA - ₹6.8 LPA",
        "future_study_options": ["Direct 2nd Year Lateral Entry B.E / B.Tech via TNEA Counselling at Anna University CEG/MIT/PSG Tech", "AMIE Certification"],
        "key_skills_needed": ["Engineering Drawing & CAD", "CNC Machine Operation", "Industrial Safety", "Troubleshooting & Electrical Circuits"]
    },
    {
        "id": "diploma_computer_engineering",
        "title": "3-Year Polytechnic Diploma in Computer Engineering & IT (DOTE TN)",
        "category": "diploma_polytechnic",
        "grade_level": "after_10th",
        "icon_emoji": "🖥️",
        "tagline": "Software Programming, Hardware Networking, Web Development & Lateral Entry into B.Tech CSE",
        "duration": "3 Years (6 Semesters)",
        "eligibility": "10th Standard (SSLC) Pass from Tamil Nadu State Board or equivalent.",
        "entrance_exams": [
            {"name": "DOTE Tamil Nadu Polytechnic Admissions", "level": "State", "official_portal": "https://www.tnpoly.in", "description": "Single-window online merit admission based on 10th marks."}
        ],
        "top_colleges": [
            "Central Polytechnic College (CPT), Chennai",
            "PSG Polytechnic College, Coimbatore",
            "Murugappa Polytechnic College, Chennai",
            "Government Polytechnic College, Trichy",
            "Government Polytechnic College, Nagercoil"
        ],
        "admission_procedure": "Apply online at tnpoly.in based on 10th marks. 7.5% Horizontal Reservation for TN Govt School students with 100% Free Tuition, Hostel & Mess.",
        "estimated_fees": {
            "govt_polytechnic": "₹2,482 / year",
            "aided_polytechnic": "₹12,000 / year",
            "private_polytechnic": "₹35,000 - ₹60,000 / year"
        },
        "scholarships": [
            "7.5% TN Govt School Free Quota",
            "Pudhumai Penn & Tamil Puthalvan (₹1,000/mo)",
            "AICTE Pragati Scholarship for Girls (₹50,000/yr)"
        ],
        "career_opportunities": [
            "Network Support Technician (Cisco / ACT Fibernet / Airtel)",
            "Junior Web Developer & Python Programmer",
            "IT Helpdesk & System Support Specialist in Chennai IT Corridor",
            "Hardware & Cloud Server Maintenance Associate"
        ],
        "starting_salary_range": "₹3.0 LPA - ₹6.5 LPA",
        "future_study_options": ["Direct 2nd Year Lateral Entry B.Tech Computer Science / IT via TNEA Counselling at Anna University / SSN", "BCA"],
        "key_skills_needed": ["Computer Hardware", "Networking (LAN/WAN/TCP-IP)", "Python / JavaScript", "Linux Operating Systems"]
    },
    {
        "id": "iti_vocational_trades_10th",
        "title": "2-Year ITI Technical Trades (Directorate of Employment & Training DET TN)",
        "category": "vocational_iti",
        "grade_level": "after_10th",
        "icon_emoji": "🛠️",
        "tagline": "Electrician, Fitter, Wireman, Motor Mechanic, Welder with Paid Industrial Apprenticeship",
        "duration": "1 to 2 Years (NSQF Level 4/5 Practical Industrial Training)",
        "eligibility": "10th Standard (SSLC) Pass from recognized board. Age: Minimum 14 years.",
        "entrance_exams": [
            {"name": "Tamil Nadu DET ITI Centralized Online Admissions", "level": "State", "official_portal": "https://skilltraining.tn.gov.in", "description": "Directorate of Employment and Training (DET) Tamil Nadu single-window admission based on 10th marks."}
        ],
        "top_colleges": [
            "Government ITI Guindy, Chennai (Premier Technical Training Hub in TN)",
            "Government ITI Coimbatore (Close linkage with textile & motor manufacturing)",
            "Government ITI Tiruchirappalli (Tie-ups with BHEL Trichy)",
            "Government ITI Madurai",
            "Government ITI Salem"
        ],
        "admission_procedure": "Apply online at skilltraining.tn.gov.in after 10th results -> District-wise counselling based on 10th marks -> Seat allotment in Govt or Private ITI. 100% Free Training in Govt ITIs with Free Uniform, Free Bus Pass, Free Bicycle and ₹750/month training allowance from Govt of Tamil Nadu!",
        "estimated_fees": {
            "govt_iti": "100% FREE (Zero tuition fee + ₹750/month Govt stipend + Free Bus Pass & Bicycle)",
            "private_iti": "₹15,000 - ₹30,000 / year"
        },
        "scholarships": [
            "Tamil Nadu Government Monthly Training Stipend of ₹750 / month for all Govt ITI students",
            "Free Laptop / Bi-cycle scheme provided by Government of Tamil Nadu",
            "National Apprenticeship Promotion Scheme (NAPS) stipend (₹8,000 - ₹12,000/month during apprenticeship)"
        ],
        "career_opportunities": [
            "Licensed Wireman & Electrical Maintenance Technician (TANGEDCO / Factories)",
            "Machinist & Fitter in Chennai Automotive Corridors (Hyundai, Renault, TVS)",
            "Railway Technician Grade III (Southern Railway via RRB)",
            "Heavy Vehicle / Motor Mechanic & Welder in Shipbuilding and Aerospace hubs"
        ],
        "starting_salary_range": "₹2.8 LPA - ₹5.5 LPA",
        "future_study_options": ["Direct Lateral Entry into 2nd Year Polytechnic Diploma (DOTE TN)", "National Craft Instructor Certificate (NCIC)"],
        "key_skills_needed": ["Electrical Wiring & Circuit Testing", "Lathe & Milling Machine Operation", "Welding & Precision Measurement", "Industrial Safety Protocols"]
    },
    {
        "id": "paramedical_diploma_10th",
        "title": "Paramedical Diplomas (DMLT, Health Inspector, X-Ray Tech — TN DME)",
        "category": "medical",
        "grade_level": "after_10th",
        "icon_emoji": "🔬",
        "tagline": "Medical Laboratory Technology (DMLT), Health Inspector & Radiography Technician",
        "duration": "2 Years (Including Hospital Clinical Postings)",
        "eligibility": "10th Standard Pass (for Health Inspector / Multi-Purpose Hospital Worker) or 12th Pass (for DMLT).",
        "entrance_exams": [
            {"name": "Tamil Nadu DME Paramedical Diploma Admissions", "level": "State", "official_portal": "https://www.tnmedicalselection.net", "description": "Selection Committee, Directorate of Medical Education Tamil Nadu centralized counselling based on board marks."}
        ],
        "top_colleges": [
            "King Institute of Preventive Medicine & Research, Guindy, Chennai",
            "Madras Medical College (Paramedical Wing), Chennai",
            "Stanley Medical College (Paramedical Courses), Chennai",
            "Madurai Medical College, Madurai"
        ],
        "admission_procedure": "Apply at tnmedicalselection.net -> Merit ranking based on qualifying marks -> Single window counselling for seats in Government Medical Colleges.",
        "estimated_fees": {
            "govt_medical_college": "₹2,500 / year (Govt Regulated - Virtually Free)",
            "private_institution": "₹25,000 - ₹50,000 / year"
        },
        "scholarships": [
            "Pudhumai Penn & Tamil Puthalvan (₹1,000/mo)",
            "Post-Matric Scholarship for SC/ST"
        ],
        "career_opportunities": [
            "Medical Lab Technician (DMLT) in Govt General Hospitals & Diagnostic Labs",
            "Health Inspector in City Municipal Corporations (Greater Chennai Corporation GCC, Coimbatore, Madurai)",
            "Radiography / X-Ray & ECG Technician",
            "Dialysis & Operation Theatre Assistant"
        ],
        "starting_salary_range": "₹2.8 LPA - ₹5.8 LPA",
        "future_study_options": ["B.Sc Medical Laboratory Technology (B.Sc MLT)", "B.Sc Radiology & Imaging"],
        "key_skills_needed": ["Blood Sample Analysis", "Microbiology Testing", "Radiation Safety", "Public Sanitation & Health Tracking"]
    },
    {
        "id": "direct_govt_jobs_10th",
        "title": "TNPSC Group 4 & VAO / TNUSRB Grade II Police Constable (Direct 10th Pass)",
        "category": "defence_govt",
        "grade_level": "after_10th",
        "icon_emoji": "🏛️",
        "tagline": "Direct Permanent Tamil Nadu State Government Job Right After 10th Standard Pass",
        "duration": "Direct Employment into Tamil Nadu State Government Service with Lifelong Job Security",
        "eligibility": "10th Standard (SSLC) Pass with Tamil language from Tamil Nadu State Board or equivalent. Age: 21 - 32 years (Relaxed to 42 for BC/MBC/SC/ST). Age 18-26 for Police Constable.",
        "entrance_exams": [
            {"name": "TNPSC Group 4 & VAO Examination", "level": "State", "official_portal": "https://www.tnpsc.gov.in", "description": "Single-stage written examination (200 Questions / 300 Marks: General Tamil 100 Qs + General Studies & Aptitude 100 Qs)."},
            {"name": "TNUSRB Police Constable Recruitment", "level": "State", "official_portal": "https://www.tnusrb.tn.gov.in", "description": "Written exam + Physical Efficiency Test (PET) for Grade II Police Constable, Jail Warder & Fireman."}
        ],
        "top_colleges": [
            "Civil Services Training Institute, Bhavanisagar, Erode (Foundation Training Hub)",
            "Tamil Nadu Police Academy (TNPA), Oonamanchery, Vandalur, Chennai",
            "Multi-Disciplinary Zonal Training Institute (MDZTI), Southern Railway, Trichy"
        ],
        "admission_procedure": "Apply on TNPSC (tnpsc.gov.in) or TNUSRB (tnusrb.tn.gov.in) -> Written Examination -> Certificate verification and counselling in Chennai -> Instant Appointment Order into Tamil Nadu Government Service.",
        "estimated_fees": {
            "application_fee": "₹100 (100% Free for SC/ST/PwD/Destitute Widows and 3 Free Chances for BC/MBC)"
        },
        "scholarships": [
            "Free TNPSC & TNUSRB Coaching provided across all 38 District Employment Exchanges in Tamil Nadu",
            "Naan Mudhalvan competitive exam monthly guidance"
        ],
        "career_opportunities": [
            "Village Administrative Officer (VAO — Revenue Department)",
            "Junior Assistant (JA) in Collectorates, Registration, Commercial Taxes, Treasuries, Courts",
            "Typist & Steno-Typist in Govt Departments",
            "Grade II Police Constable / Fireman / Jail Warder"
        ],
        "starting_salary_range": "₹3.0 LPA - ₹5.0 LPA (Monthly: ₹24,000 - ₹38,000 with Govt Quarters & Pension)",
        "future_study_options": ["Departmental Promotion to Revenue Inspector (RI), Tahsildar, Head Constable & Sub-Inspector", "Distance Degree via University of Madras IDE"],
        "key_skills_needed": ["General Tamil Grammar & Literature", "Tamil Nadu History & Culture", "Basic Arithmetic & Mental Ability", "Public Administration Integrity"]
    },

    # ==================== B. DIRECT NEXT STEPS AFTER 12TH GRADE (HSC) ====================
    {
        "id": "btech_cse_ai",
        "title": "B.E / B.Tech Computer Science & AI / Data Science (TNEA & Anna Univ)",
        "category": "engineering",
        "grade_level": "after_12th_pcm",
        "icon_emoji": "💻",
        "tagline": "Software Engineering, Cloud Systems, Machine Learning & Cyber Systems in Tamil Nadu IT Hubs",
        "duration": "4 Years (8 Semesters)",
        "eligibility": "12th Pass with Physics, Chemistry & Mathematics (PCM). TNEA Cutoff out of 200 (Maths + Physics/2 + Chemistry/2).",
        "entrance_exams": [
            {"name": "TNEA (Tamil Nadu Engineering Admissions)", "level": "State", "official_portal": "https://www.tneaonline.org", "description": "Single-window online counselling based purely on 12th PCM marks. Zero entrance exam."},
            {"name": "JEE Main (for IIT Madras / NIT Trichy)", "level": "National", "official_portal": "https://jeemain.nta.nic.in", "description": "For admission into IIT Madras & NIT Trichy (50% Home State Tamil Nadu Quota)."}
        ],
        "top_colleges": [
            "IIT Madras, Chennai",
            "College of Engineering Guindy (CEG), Anna University, Chennai",
            "NIT Tiruchirappalli (Trichy)",
            "Madras Institute of Technology (MIT Chromepet), Anna University, Chennai",
            "PSG College of Technology, Coimbatore",
            "SSN College of Engineering, Chennai",
            "Coimbatore Institute of Technology (CIT), Coimbatore",
            "Thiagarajar College of Engineering (TCE), Madurai"
        ],
        "admission_procedure": "Register on TNEA portal (tneaonline.org) -> Certificate verification at TFC centres -> Rank list published -> 4-Round Online Choice Filling -> Seat allotment based on 12th PCM cutoff. 7.5% Horizontal Reservation for TN Govt School students with 100% Free Tuition, Hostel & Mess fees funded by TN Govt.",
        "estimated_fees": {
            "govt_college": "₹31,000 / year (Anna Univ CEG/MIT - 100% Free for 7.5% Govt School & First Gen Graduate)",
            "govt_aided_college": "₹45,000 - ₹85,000 / year (PSG Tech / CIT / TCE Madurai)",
            "private_college": "₹1,20,000 - ₹2,50,000 / year (SSN / SASTRA)"
        },
        "scholarships": [
            "Tamil Nadu 7.5% Govt School Horizontal Reservation (100% Free Tuition, Hostel, Mess)",
            "Pudhumai Penn Scheme (₹1,000/month for female students from TN Govt Schools)",
            "Tamil Puthalvan Scheme (₹1,000/month for male students from TN Govt Schools)",
            "First Generation Graduate Tuition Fee Concession (₹25,000 - ₹27,500/year waiver)",
            "Post-Matric Scholarship for SC/SCA/ST"
        ],
        "career_opportunities": [
            "Full Stack Software Engineer (Zoho, Freshworks, Microsoft Chennai)",
            "AI / ML Engineer & Data Scientist",
            "Cloud Solutions Architect (AWS / Azure)",
            "Product Developer & Fintech Systems Engineer"
        ],
        "starting_salary_range": "₹6.5 LPA - ₹42.0 LPA (Average: ₹9.8 LPA in top TN colleges)",
        "future_study_options": ["M.E / M.Tech at Anna University / IITM / NIT Trichy", "MS in USA / Germany", "GATE for PSU (ISRO / BHEL)"],
        "key_skills_needed": ["Problem Solving", "Data Structures & Algorithms", "Python / C++ / Java", "System Design"]
    },
    {
        "id": "btech_ece_vlsi",
        "title": "B.E Electronics & Communication Engineering (ECE / VLSI)",
        "category": "engineering",
        "grade_level": "after_12th_pcm",
        "icon_emoji": "⚡",
        "tagline": "Semiconductors, 5G Wireless, Embedded Firmware & Automotive Electronics Corridor",
        "duration": "4 Years (8 Semesters)",
        "eligibility": "12th Pass with PCM. TNEA Cutoff out of 200.",
        "entrance_exams": [
            {"name": "TNEA (Tamil Nadu Engineering Admissions)", "level": "State", "official_portal": "https://www.tneaonline.org", "description": "Single-window online counselling for Anna University & affiliated institutions."}
        ],
        "top_colleges": [
            "IIT Madras, Chennai",
            "NIT Tiruchirappalli",
            "Anna University (CEG Campus), Chennai",
            "PSG College of Technology, Coimbatore",
            "SSN College of Engineering, Chennai",
            "Thiagarajar College of Engineering, Madurai"
        ],
        "admission_procedure": "TNEA online single-window counselling based on 12th PCM marks. 7.5% Govt school reservation applies with 100% free fees.",
        "estimated_fees": {
            "govt_college": "₹31,000 / year (Anna University CEG)",
            "govt_aided_college": "₹45,000 / year (PSG Tech)",
            "private_college": "₹1,20,000 - ₹2,00,000 / year"
        },
        "scholarships": [
            "Tamil Nadu 7.5% Govt School Free Education Scheme",
            "First Generation Graduate Concession",
            "Pudhumai Penn & Tamil Puthalvan (₹1,000/mo)"
        ],
        "career_opportunities": [
            "VLSI Chip Design Engineer (Qualcomm, Texas Instruments, Intel)",
            "Embedded Systems Engineer (Robert Bosch, Continental, Visteon Chennai)",
            "5G / Wireless Telecom Specialist (Airtel, Ericsson, Nokia)",
            "Hardware & IoT Firmware Developer"
        ],
        "starting_salary_range": "₹5.5 LPA - ₹32.0 LPA",
        "future_study_options": ["M.Tech in VLSI / Microelectronics at IIT Madras", "MS in Germany / Taiwan / USA"],
        "key_skills_needed": ["Circuit Design", "Verilog / VHDL", "C / Embedded C", "Microcontrollers"]
    },
    {
        "id": "btech_mechanical_robotics",
        "title": "B.E Mechanical, Automation & EV Engineering (TNEA)",
        "category": "engineering",
        "grade_level": "after_12th_pcm",
        "icon_emoji": "🚗",
        "tagline": "Automotive Engineering (Chennai-Detroit of Asia), Robotics, EV & Precision Manufacturing",
        "duration": "4 Years (8 Semesters)",
        "eligibility": "12th Pass with PCM. TNEA Cutoff out of 200.",
        "entrance_exams": [
            {"name": "TNEA (Tamil Nadu Engineering Admissions)", "level": "State", "official_portal": "https://www.tneaonline.org", "description": "Single-window online counselling."}
        ],
        "top_colleges": [
            "Anna University (MIT Campus), Chromepet, Chennai",
            "PSG College of Technology, Coimbatore",
            "College of Engineering Guindy (CEG), Chennai",
            "NIT Tiruchirappalli",
            "Government College of Engineering (GCE), Salem"
        ],
        "admission_procedure": "TNEA Online Single Window Counselling via tneaonline.org. 7.5% Govt School reservation applies with 100% free fees.",
        "estimated_fees": {
            "govt_college": "₹31,000 / year (Anna University MIT)",
            "govt_aided_college": "₹42,000 / year (PSG Tech Regular/Sandwich)",
            "private_college": "₹90,000 - ₹1,80,000 / year"
        },
        "scholarships": [
            "7.5% TN Govt School Free Seats (Tuition, Hostel, Mess)",
            "First Graduate Concession (₹25,000/yr)",
            "Pudhumai Penn / Tamil Puthalvan (₹1,000/mo)"
        ],
        "career_opportunities": [
            "Automotive Design Engineer (Hyundai, Renault-Nissan, TVS, Ashok Leyland)",
            "Electric Vehicle (EV) Powertrain Engineer (Ola Electric, Ather Energy TN plant)",
            "Robotics & Mechatronics Automation Engineer",
            "Plant Operations & Quality Control Manager"
        ],
        "starting_salary_range": "₹4.5 LPA - ₹18.0 LPA",
        "future_study_options": ["M.Tech Robotics / Automobile at Anna University", "GATE for BHEL Trichy"],
        "key_skills_needed": ["CAD/CAM (SolidWorks/CATIA)", "Thermodynamics", "Automation & PLC", "FEA Analysis"]
    },
    {
        "id": "mbbs_medicine",
        "title": "MBBS — Bachelor of Medicine and Bachelor of Surgery (TN DME Selection)",
        "category": "medical",
        "grade_level": "after_12th_pcb",
        "icon_emoji": "🩺",
        "tagline": "Clinical Diagnosis, Surgery, Healthcare & Patient Lifesaving across 36 TN Govt Medical Colleges",
        "duration": "5.5 Years (4.5 Years Academics + 1 Year CRRI Internship)",
        "eligibility": "12th Pass with Physics, Chemistry & Biology (PCB). Minimum 50% aggregate (40% for BC/BCM/MBC/SC/ST). Valid NEET-UG score.",
        "entrance_exams": [
            {"name": "NEET-UG (National Eligibility cum Entrance Test)", "level": "National", "official_portal": "https://neet.nta.nic.in", "description": "Mandatory national entrance exam for medical admissions across India."}
        ],
        "top_colleges": [
            "Madras Medical College (MMC), Chennai (Est. 1835)",
            "Stanley Medical College, Royapuram, Chennai",
            "Christian Medical College (CMC), Vellore (NIRF Rank #3)",
            "Government Kilpauk Medical College (KMC), Chennai",
            "Madurai Medical College, Madurai",
            "Coimbatore Medical College, Coimbatore"
        ],
        "admission_procedure": "Write NEET-UG in May -> Register for Tamil Nadu State Quota (85%) conducted by the Selection Committee, Directorate of Medical Education (DME), Kilpauk, Chennai (tnmedicalselection.net) -> State Merit Rank list -> Online Choice Filling & Seat Allotment. Crucial: 7.5% Horizontal Reservation for Tamil Nadu Govt School students with 100% Free Tuition, Hostel & Mess fees paid by TN Govt.",
        "estimated_fees": {
            "govt_college": "₹13,610 / year (Fixed by Govt of Tamil Nadu across all 36 GMCs - 100% Free under 7.5% quota)",
            "private_govt_quota": "₹4,00,000 - ₹4,50,000 / year (Govt Quota in Private Medical Colleges)"
        },
        "scholarships": [
            "Tamil Nadu 7.5% Govt School Horizontal Reservation (100% Free Tuition, Books, Hostel, Mess)",
            "Pudhumai Penn Scheme (₹1,000/month for female TN Govt school students)",
            "Tamil Puthalvan Scheme (₹1,000/month for male TN Govt school students)",
            "Post-Matric Scholarship for SC/ST/SCA students"
        ],
        "career_opportunities": [
            "Medical Officer (Tamil Nadu Medical Services Recruitment Board - MRB)",
            "Resident Doctor / General Physician in Government & Private Hospitals",
            "Medical Consultant in Apollo, SIMS, MIOT Chennai",
            "Clinical Researcher & Public Health Specialist"
        ],
        "starting_salary_range": "₹9.0 LPA - ₹18.0 LPA (CRRI Internship Stipend: ₹25,000/month)",
        "future_study_options": ["MD / MS via NEET-PG", "DNB Super-Specialty", "MRCP / USMLE"],
        "key_skills_needed": ["Clinical Acumen", "Empathy", "Biological Physiology", "High Stress Resilience", "Patience"]
    },
    {
        "id": "bds_dental",
        "title": "BDS — Bachelor of Dental Surgery (TN Medical Selection)",
        "category": "medical",
        "grade_level": "after_12th_pcb",
        "icon_emoji": "🦷",
        "tagline": "Oral Health, Maxillofacial Surgery, Orthodontics & Cosmetic Dentistry in Tamil Nadu",
        "duration": "5 Years (4 Years Academics + 1 Year Paid Rotatory Internship)",
        "eligibility": "12th Standard Pass with Physics, Chemistry & Biology. Qualified in NEET-UG.",
        "entrance_exams": [
            {"name": "NEET-UG", "level": "National", "official_portal": "https://neet.nta.nic.in", "description": "Mandatory entrance exam."}
        ],
        "top_colleges": [
            "Tamil Nadu Government Dental College & Hospital, Chennai (Est. 1953)",
            "SRM Dental College, Ramapuram, Chennai",
            "Saveetha Dental College, Chennai (NIRF Top Ranked Dental)",
            "Ragas Dental College and Hospital, Chennai"
        ],
        "admission_procedure": "Selection Committee DME Tamil Nadu conducts centralized online counselling (tnmedicalselection.net) based on NEET-UG rank. 7.5% TN Govt school reservation applies with 100% free tuition & hostel.",
        "estimated_fees": {
            "govt_college": "₹11,610 / year (Tamil Nadu Govt Dental College Chennai)",
            "private_govt_quota": "₹2,50,000 / year"
        },
        "scholarships": [
            "7.5% TN Govt School Horizontal Reservation (100% Free Tuition, Hostel & Mess)",
            "Pudhumai Penn / Tamil Puthalvan (₹1,000/month)",
            "Post-Matric Scholarship for SC/SCA/ST"
        ],
        "career_opportunities": [
            "Dental Surgeon in Govt Primary Health Centres (TN MRB)",
            "Private Dental Clinic Owner / Orthodontist",
            "Maxillofacial Trauma Consultant",
            "Cosmetic Smile Designer & Implantologist"
        ],
        "starting_salary_range": "₹4.5 LPA - ₹12.0 LPA",
        "future_study_options": ["MDS (Master of Dental Surgery) via NEET-MDS"],
        "key_skills_needed": ["Fine Motor Dexterity", "Aesthetic Sense", "Surgical Precision", "Patient Management"]
    },
    {
        "id": "bsc_nursing",
        "title": "B.Sc Nursing (Tamil Nadu Paramedical Counselling)",
        "category": "medical",
        "grade_level": "after_12th_pcb",
        "icon_emoji": "💉",
        "tagline": "Critical Patient Care, ICU Nursing, Healthcare Administration & Global Hospital Opportunities",
        "duration": "4 Years (8 Semesters including Clinical Rotations)",
        "eligibility": "12th Pass with Physics, Chemistry & Biology with min 45-50% aggregate. Both Female & Male candidates eligible.",
        "entrance_exams": [
            {"name": "Tamil Nadu Paramedical / Nursing Single Window Counselling", "level": "State", "official_portal": "https://www.tnmedicalselection.net", "description": "Single-window online merit admission based on 12th PCB marks."}
        ],
        "top_colleges": [
            "College of Nursing, Madras Medical College (MMC), Chennai",
            "College of Nursing, Christian Medical College (CMC), Vellore",
            "Stanley Medical College School of Nursing, Chennai",
            "Government Mohan Kumaramangalam Medical College Nursing, Salem",
            "Apollo College of Nursing, Chennai"
        ],
        "admission_procedure": "Selection Committee DME Tamil Nadu publishes Paramedical notification -> Apply online at tnmedicalselection.net with 12th marks -> Merit list based on Cutoff out of 200 (PCB) -> Centralized Online Allotment.",
        "estimated_fees": {
            "govt_college": "₹3,500 / year (Govt Medical Colleges in TN)",
            "private_college": "₹65,000 - ₹1,20,000 / year"
        },
        "scholarships": [
            "Pudhumai Penn Scheme (₹1,000/month for female TN Govt school students)",
            "Tamil Puthalvan Scheme (₹1,000/month for male students)",
            "7.5% Govt School Free Seat Scheme"
        ],
        "career_opportunities": [
            "Staff Nurse (Tamil Nadu MRB Hospital Recruitment)",
            "ICU / Critical Care Specialist Nurse",
            "Overseas Nursing Officer (NHS UK, Germany, USA NCLEX-RN, Gulf countries)",
            "Nurse Educator & Hospital Nursing Superintendent"
        ],
        "starting_salary_range": "₹3.8 LPA - ₹9.0 LPA (Overseas: ₹28 LPA - ₹48 LPA)",
        "future_study_options": ["M.Sc Nursing", "Nurse Practitioner in Critical Care (NPCC)", "Hospital Administration (MHA)"],
        "key_skills_needed": ["Patient Empathy", "Clinical Procedures", "Emergency Response", "Medication Safety"]
    },
    {
        "id": "bpharm_pharmacy",
        "title": "B.Pharm — Bachelor of Pharmacy (Tamil Nadu Paramedical Counselling)",
        "category": "medical",
        "grade_level": "after_12th_pcb",
        "icon_emoji": "💊",
        "tagline": "Pharmaceutical Formulation, Drug Discovery, Clinical Trials & Industrial Pharma Corridor in TN",
        "duration": "4 Years (8 Semesters)",
        "eligibility": "12th Pass with Physics, Chemistry and Biology / Mathematics with min 50%.",
        "entrance_exams": [
            {"name": "Tamil Nadu Paramedical / B.Pharm Counselling", "level": "State", "official_portal": "https://www.tnmedicalselection.net", "description": "Single-window online counselling based on 12th PCM / PCB marks."}
        ],
        "top_colleges": [
            "Madras Medical College (College of Pharmacy), Chennai",
            "Madurai Medical College (College of Pharmacy), Madurai",
            "PSG College of Pharmacy, Coimbatore",
            "JSS College of Pharmacy, Ooty (The Nilgiris, Tamil Nadu)",
            "SRM College of Pharmacy, Kattankulathur, Chennai"
        ],
        "admission_procedure": "Selection Committee DME Tamil Nadu conducts online single-window counselling for B.Pharm seats. 7.5% Govt school reservation applies.",
        "estimated_fees": {
            "govt_college": "₹4,500 / year (MMC & Madurai Medical College)",
            "private_govt_quota": "₹38,000 / year"
        },
        "scholarships": [
            "Tamil Nadu 7.5% Govt School Free Education",
            "Pudhumai Penn & Tamil Puthalvan (₹1,000/mo)",
            "AICTE GPAT Scholarship (for PG)"
        ],
        "career_opportunities": [
            "Drug Inspector (Tamil Nadu Drugs Control Dept / TNPSC)",
            "Formulation & Quality Control Scientist (Sun Pharma, Cipla, Dr. Reddy's TN plants)",
            "Clinical Research Associate (CROs in OMR Chennai)",
            "Hospital & Community Pharmacist"
        ],
        "starting_salary_range": "₹4.0 LPA - ₹9.5 LPA",
        "future_study_options": ["M.Pharm (Pharmaceutics/Pharmacology)", "Pharm.D (Post-Baccalaureate)"],
        "key_skills_needed": ["Organic Chemistry", "Pharmacology", "Drug Synthesis", "GMP Standards"]
    },
    {
        "id": "bvsc_veterinary",
        "title": "B.V.Sc & A.H — Bachelor of Veterinary Science (TANUVAS Chennai)",
        "category": "agriculture",
        "grade_level": "after_12th_pcb",
        "icon_emoji": "🐾",
        "tagline": "Animal Healthcare, Dairy Science, Livestock Breeding & Wildlife Veterinary at TANUVAS",
        "duration": "5.5 Years (4.5 Years Academics + 1 Year Internship)",
        "eligibility": "12th Standard Pass from TN State Board / CBSE with Physics, Chemistry & Biology. High 12th PCB Cutoff out of 200 (~190-197/200).",
        "entrance_exams": [
            {"name": "TANUVAS Undergraduate Counselling", "level": "State", "official_portal": "https://tanuvas.ac.in", "description": "Tamil Nadu Veterinary and Animal Sciences University centralized admission based on 12th marks."}
        ],
        "top_colleges": [
            "Madras Veterinary College (TANUVAS), Vepery, Chennai (Est. 1876)",
            "Veterinary College and Research Institute (VC&RI), Namakkal",
            "Veterinary College and Research Institute, Tirunelveli",
            "Veterinary College and Research Institute, Orathanadu (Thanjavur)",
            "Veterinary College and Research Institute, Thalaivasal (Salem)"
        ],
        "admission_procedure": "Apply online at tanuvas.ac.in -> Merit rank list based on 12th PCB aggregate -> Single window counselling. 7.5% Horizontal Reservation for TN Govt School students with 100% Free Tuition, Hostel & Mess fees paid by Tamil Nadu Govt.",
        "estimated_fees": {
            "govt_college": "₹18,500 / year (Govt constituent colleges of TANUVAS)"
        },
        "scholarships": [
            "7.5% TN Govt School Free Higher Education Scheme",
            "Pudhumai Penn & Tamil Puthalvan (₹1,000/mo)",
            "ICAR National Talent Scholarship (NTS)"
        ],
        "career_opportunities": [
            "Veterinary Assistant Surgeon (VAS) via TNPSC (Gazetted Govt Officer)",
            "Dairy & Livestock Manager (Aavin, Hatsun Agro, Milky Mist)",
            "Poultry Health Consultant in Namakkal Poultry Belt (Suguna, Shanthi Feeds)",
            "Zoo & Wildlife Veterinarian (Arignar Anna Zoological Park Vandalur)"
        ],
        "starting_salary_range": "₹6.5 LPA - ₹15.0 LPA (Govt VAS: ₹65,000 - ₹90,000/month)",
        "future_study_options": ["M.V.Sc (Veterinary Surgery/Medicine/Gynecology)"],
        "key_skills_needed": ["Animal Handling", "Pathology", "Surgical Precision", "Epidemiology"]
    },
    {
        "id": "agriculture_icar_tnau",
        "title": "B.Sc (Hons) Agriculture / Horticulture (TNAU Coimbatore)",
        "category": "agriculture",
        "grade_level": "after_12th_pcb",
        "icon_emoji": "🌾",
        "tagline": "Sustainable Agronomy, Crop Biotechnology, Precision Farming & Agribusiness at TNAU",
        "duration": "4 Years (8 Semesters)",
        "eligibility": "12th Pass with Physics, Chemistry & Biology (PCB) or Botany & Zoology. TNAU Cutoff out of 200.",
        "entrance_exams": [
            {"name": "TNAU Undergraduate Single Window Counselling", "level": "State", "official_portal": "https://tnau.ac.in", "description": "Single-window online counselling conducted by Tamil Nadu Agricultural University, Coimbatore based on 12th marks."}
        ],
        "top_colleges": [
            "Tamil Nadu Agricultural University (TNAU Main Campus), Coimbatore (Est. 1906)",
            "Agricultural College and Research Institute (AC&RI), Madurai",
            "Agricultural College and Research Institute, Killikulam (Thoothukudi)",
            "Anbil Dharmalingam Agricultural College and Research Institute (ADAC&RI), Trichy",
            "Forest College and Research Institute (FC&RI), Mettupalayam, Coimbatore"
        ],
        "admission_procedure": "Register at tnau.ac.in -> Online single-window counselling based on 12th marks. 7.5% Horizontal Reservation for Tamil Nadu Government School students with 100% Free Tuition, Hostel & Mess fees paid by TN Govt.",
        "estimated_fees": {
            "govt_constituent_campus": "₹48,000 / year (100% Free under 7.5% reservation)",
            "affiliated_private_college": "₹1,20,000 / year"
        },
        "scholarships": [
            "Tamil Nadu 7.5% Govt School Horizontal Reservation (100% Free)",
            "Pudhumai Penn & Tamil Puthalvan (₹1,000/mo)",
            "ICAR National Talent Scholarship (NTS)"
        ],
        "career_opportunities": [
            "Agricultural Officer (AO) & Horticultural Officer (HO) via TNPSC",
            "Agricultural Field Officer (AFO) in Nationalized Commercial Banks (IBPS)",
            "Seed & Agrochemical Scientist (ITC Agri, Godrej Agrovet, Syngenta)",
            "Organic Farm Entrepreneur & Export Specialist"
        ],
        "starting_salary_range": "₹5.0 LPA - ₹12.0 LPA (Govt AO: ₹56,000 - ₹75,000/month)",
        "future_study_options": ["M.Sc (Agri) at TNAU / IARI New Delhi via ICAR AIEEA"],
        "key_skills_needed": ["Soil Chemistry", "Crop Genetics", "Farm Mechanization", "Pest Management"]
    },
    {
        "id": "bsc_cs_datascience",
        "title": "B.Sc Computer Science / Data Science (TNGASA & Autonomous)",
        "category": "arts_science",
        "grade_level": "after_12th_pcm",
        "icon_emoji": "📊",
        "tagline": "Algorithms, Data Analytics, Python Systems & Cloud Computing at Premier TN Colleges",
        "duration": "3 Years (6 Semesters)",
        "eligibility": "12th Pass with Mathematics / Computer Science. Cutoff based on 12th Board marks.",
        "entrance_exams": [
            {"name": "TNGASA (Tamil Nadu Govt Arts & Science Colleges Admissions)", "level": "State", "official_portal": "https://www.tngasa.in", "description": "Single-window online admission portal for 164+ Govt Arts & Science colleges across TN."},
            {"name": "Autonomous College Direct Merit", "level": "State", "official_portal": "https://www.loyolacollege.edu", "description": "Direct application for Loyola, MCC, Presidency, PSG CAS based on 12th marks."}
        ],
        "top_colleges": [
            "Loyola College (Autonomous), Chennai (NIRF Rank #8)",
            "Presidency College (Autonomous), Chennai (NIRF Rank #3)",
            "Madras Christian College (MCC), Tambaram, Chennai",
            "PSG College of Arts & Science, Coimbatore",
            "Bishop Heber College, Tiruchirappalli"
        ],
        "admission_procedure": "Apply via TNGASA portal (tngasa.in) for Govt Colleges or college website for Autonomous Colleges -> Merit list published based on 12th marks. 7.5% priority for TN Govt School students; Pudhumai Penn / Tamil Puthalvan applies.",
        "estimated_fees": {
            "govt_college": "₹2,400 / year (Presidency College Chennai - virtually free)",
            "aided_seat": "₹18,000 - ₹35,000 / year (Loyola / MCC / PSG CAS Day Shift)",
            "self_financed": "₹45,000 - ₹85,000 / year"
        },
        "scholarships": [
            "Pudhumai Penn Scheme (₹1,000/mo for female students from TN Govt schools)",
            "Tamil Puthalvan Scheme (₹1,000/mo for male students)",
            "Post-Matric Scholarship for SC/ST students"
        ],
        "career_opportunities": [
            "Data Analyst & Business Intelligence Specialist (Zoho, Freshworks Chennai)",
            "Junior Software Developer & QA Automation Engineer",
            "Database Administrator & Cloud Operations Associate",
            "Tech Support & IT Operations Specialist (TCS, Infosys, Cognizant, Wipro)"
        ],
        "starting_salary_range": "₹3.8 LPA - ₹10.5 LPA",
        "future_study_options": ["MCA at Anna University CEG / NIT Trichy via TANCET / NIMCET", "M.Sc Data Science"],
        "key_skills_needed": ["SQL & Database Querying", "Python", "Data Visualization", "Statistics"]
    },
    {
        "id": "bcom_ca_finance",
        "title": "B.Com — Accounting, Finance & Corporate Secretaryship",
        "category": "arts_science",
        "grade_level": "after_12th_commerce",
        "icon_emoji": "📈",
        "tagline": "Financial Accounting, Corporate Law, Taxation, CA Foundation & Banking in Chennai Financial Hub",
        "duration": "3 Years (6 Semesters)",
        "eligibility": "12th Standard Pass from TN State Board / CBSE with Commerce, Accountancy, Economics & Business Maths. High cutoff for top colleges (90%+).",
        "entrance_exams": [
            {"name": "CA Foundation / CMA Foundation", "level": "National", "official_portal": "https://www.icai.org", "description": "Professional accounting exam pursued concurrently during B.Com."},
            {"name": "TNGASA / Autonomous College Merit", "level": "State", "official_portal": "https://www.tngasa.in", "description": "Single window & autonomous college merit based on 12th Commerce marks."}
        ],
        "top_colleges": [
            "Loyola College (Autonomous), Chennai",
            "Madras Christian College (MCC), Chennai",
            "PSG College of Arts & Science, Coimbatore",
            "Ramakrishna Mission Vivekananda College, Chennai",
            "Stella Maris College (for Women), Chennai"
        ],
        "admission_procedure": "Online application on college portal (Loyola, MCC, PSG CAS) or TNGASA (tngasa.in). Shortlisting purely on 12th commerce & accountancy aggregate.",
        "estimated_fees": {
            "govt_college": "₹2,200 / year (Govt Arts Colleges in TN)",
            "aided_seat": "₹20,000 - ₹38,000 / year (Loyola / MCC Aided)",
            "self_financed": "₹55,000 - ₹95,000 / year"
        },
        "scholarships": [
            "Pudhumai Penn Scheme (₹1,000/month for female students)",
            "Tamil Puthalvan Scheme (₹1,000/month for male students)",
            "Post-Matric Scholarship for SC/ST"
        ],
        "career_opportunities": [
            "Financial Analyst (Deloitte, EY, KPMG, PwC Chennai/Bengaluru)",
            "Audit Associate & Tax Consultant",
            "Corporate Accountant in Manufacturing & IT Firms",
            "Probationary Officer (State Bank of India, Indian Overseas Bank, Canara Bank)"
        ],
        "starting_salary_range": "₹3.6 LPA - ₹12.0 LPA (With CA Inter: ₹8.5 LPA - ₹15.0 LPA)",
        "future_study_options": ["Chartered Accountancy (CA / CMA)", "M.Com / MBA in Finance", "CFA"],
        "key_skills_needed": ["Double Entry Bookkeeping", "GST & Income Tax Laws", "Financial Modeling (Excel)", "Corporate Law"]
    },
    {
        "id": "ba_economics_public_policy",
        "title": "B.A Economics & Public Administration",
        "category": "arts_science",
        "grade_level": "after_12th_arts",
        "icon_emoji": "🏛️",
        "tagline": "Economic Policy, Civil Services (TNPSC / UPSC) Foundation, Public Finance & Econometrics",
        "duration": "3 Years (6 Semesters)",
        "eligibility": "12th Standard Pass in Arts, Commerce or Science stream.",
        "entrance_exams": [
            {"name": "TNGASA Online Admissions", "level": "State", "official_portal": "https://www.tngasa.in", "description": "Single-window admission for all Tamil Nadu Govt Arts & Science Colleges."}
        ],
        "top_colleges": [
            "Presidency College (Autonomous), Chennai (NIRF Rank #3)",
            "Loyola College (Autonomous), Chennai",
            "Madras Christian College (MCC), Chennai",
            "Stella Maris College, Chennai",
            "Madras School of Economics (MSE), Chennai"
        ],
        "admission_procedure": "TNGASA online application (tngasa.in) or autonomous college portal. 100% Free under Pudhumai Penn / Tamil Puthalvan for TN Govt School students.",
        "estimated_fees": {
            "govt_college": "₹2,100 / year",
            "aided_seat": "₹16,000 - ₹32,000 / year"
        },
        "scholarships": [
            "Pudhumai Penn & Tamil Puthalvan (₹1,000/mo)",
            "Tamil Nadu Govt UPSC/TNPSC Free Coaching Scheme (All India Civil Services Coaching Centre, Chennai)"
        ],
        "career_opportunities": [
            "TNPSC Group 1 Deputy Collector / DSP Aspirant",
            "Economic Research Analyst (RBI, NITI Aayog, Madras School of Economics)",
            "Policy Consultant & NGO Project Manager",
            "Data & Market Research Associate"
        ],
        "starting_salary_range": "₹3.5 LPA - ₹9.0 LPA",
        "future_study_options": ["M.A Economics at Madras School of Economics (MSE)", "UPSC / TNPSC Civil Services"],
        "key_skills_needed": ["Econometric Modeling", "Public Policy Analysis", "Statistical Software", "Critical Writing"]
    },
    {
        "id": "integrated_law_clat",
        "title": "5-Year Integrated B.A. LL.B / B.Com. LL.B (SOEL & TNDALU)",
        "category": "law",
        "grade_level": "after_12th_arts",
        "icon_emoji": "⚖️",
        "tagline": "Corporate Law, Constitutional Litigation, Cyber Law & Judiciary at TNDALU Chennai & TNNLU Trichy",
        "duration": "5 Years (10 Semesters)",
        "eligibility": "12th Standard Pass from recognized board with min 70% for SOEL (60% for SC/ST) or valid CLAT score for TNNLU.",
        "entrance_exams": [
            {"name": "TNDALU Law Admissions (SOEL & Govt Law Colleges)", "level": "State", "official_portal": "https://www.tndalu.ac.in", "description": "Single-window online counselling conducted by Tamil Nadu Dr. Ambedkar Law University based purely on 12th marks."},
            {"name": "CLAT (Common Law Admission Test)", "level": "National", "official_portal": "https://consortiumofnlus.ac.in", "description": "For admission to Tamil Nadu National Law University (TNNLU Trichy - 50% TN State Domicile Quota)."}
        ],
        "top_colleges": [
            "School of Excellence in Law (SOEL) — TNDALU, Chennai",
            "Tamil Nadu National Law University (TNNLU), Tiruchirappalli",
            "Dr. Ambedkar Government Law College (Madras Law College), Chennai (Est. 1891)",
            "Government Law College, Madurai",
            "Government Law College, Coimbatore"
        ],
        "admission_procedure": "Apply online at tndalu.ac.in for SOEL (Honours degree) and 14 Govt Law Colleges -> Cutoff calculated on 12th marks -> Online single-window counselling. For TNNLU, appear for CLAT exam in December. 7.5% Horizontal Reservation for TN Govt School students with 100% Free Tuition, Hostel & Mess fees paid by Tamil Nadu Govt.",
        "estimated_fees": {
            "govt_law_college": "₹2,100 / year (Govt Law Colleges in TN - virtually free)",
            "soel_chennai": "₹85,000 / year (Honours Law Degree)",
            "tnnlu_trichy": "₹1,85,000 / year (National Law University residential campus)"
        },
        "scholarships": [
            "Tamil Nadu 7.5% Govt School Horizontal Reservation (100% Free Tuition, Hostel, Mess)",
            "Pudhumai Penn & Tamil Puthalvan (₹1,000/month)",
            "Bar Council of Tamil Nadu Advocate Welfare Fund"
        ],
        "career_opportunities": [
            "Advocate at Madras High Court & Subordinate Courts",
            "Civil Judge / Magistrate (Tamil Nadu State Judicial Services Exam via TNPSC)",
            "Corporate Legal Counsel (Cyril Amarchand Mangaldas, Shardul Amarchand, Fox Mandal)",
            "Public Prosecutor & Legal Advisor to TN Govt Departments"
        ],
        "starting_salary_range": "₹5.5 LPA - ₹18.0 LPA",
        "future_study_options": ["LL.M at TNDALU / NLUs", "Tamil Nadu Judicial Academy Training"],
        "key_skills_needed": ["Legal Reasoning", "Moot Court Oral Advocacy", "Case Precedent Analysis", "Contract Drafting"]
    },
    {
        "id": "barch_architecture",
        "title": "B.Arch — Bachelor of Architecture (Anna University SAP)",
        "category": "architecture",
        "grade_level": "after_12th_pcm",
        "icon_emoji": "📐",
        "tagline": "Sustainable Urban Habitat, Structural Design, Landscape & BIM at SAP Anna University",
        "duration": "5 Years (10 Semesters including 1-Year Architectural Internship)",
        "eligibility": "12th Pass with Physics, Chemistry & Mathematics (min 50% aggregate) + Qualified in NATA (National Aptitude Test in Architecture). Merit calculated out of 400 (200 from 12th PCM + 200 from NATA).",
        "entrance_exams": [
            {"name": "NATA (National Aptitude Test in Architecture)", "level": "National", "official_portal": "https://www.nata.in", "description": "Conducted by Council of Architecture (CoA) assessing drawing, visual perception & architectural aptitude."},
            {"name": "Anna University SAP B.Arch Single Window Counselling", "level": "State", "official_portal": "https://www.annauniv.edu", "description": "Single-window online counselling for B.Arch seats across Tamil Nadu."}
        ],
        "top_colleges": [
            "School of Architecture and Planning (SAP), Anna University, Chennai (Est. 1957)",
            "MEASI Academy of Architecture (Autonomous), Royapettah, Chennai",
            "Department of Architecture, Thiagarajar College of Engineering, Madurai",
            "McGAN'S Ooty School of Architecture, Nilgiris, Tamil Nadu"
        ],
        "admission_procedure": "Take NATA exam -> Register on Anna University B.Arch counselling portal -> Combined rank out of 400 published -> Single-window counselling seat allotment. 7.5% Govt school reservation applies with 100% free fees.",
        "estimated_fees": {
            "govt_sap_anna_univ": "₹42,000 / year (SAP Anna University)",
            "govt_aided_seat": "₹55,000 / year (TCE Madurai)",
            "private_college": "₹1,25,000 - ₹2,20,000 / year (MEASI / McGAN'S)"
        },
        "scholarships": [
            "Tamil Nadu 7.5% Govt School Free Education Scheme",
            "First Generation Graduate Concession",
            "Pudhumai Penn & Tamil Puthalvan (₹1,000/mo)"
        ],
        "career_opportunities": [
            "Licensed Architect (Registered with Council of Architecture - COA)",
            "Urban Planner with Chennai Metropolitan Development Authority (CMDA) / DTCP",
            "BIM & Sustainable Green Building Specialist (L&T Realty, CRN Architects)",
            "Interior & Heritage Conservation Architect"
        ],
        "starting_salary_range": "₹4.8 LPA - ₹15.0 LPA",
        "future_study_options": ["M.Arch in Urban Design / Landscape at SAP Anna University"],
        "key_skills_needed": ["Freehand Sketching", "3D Modeling (AutoCAD, Revit, Rhino)", "Spatial Planning", "Building Bye-laws"]
    },
    {
        "id": "bdes_fashion_product_design",
        "title": "B.Des / M.Sc Electronic Media (NIFT Chennai & Anna Univ)",
        "category": "design",
        "grade_level": "after_12th_arts",
        "icon_emoji": "🎨",
        "tagline": "Apparel & Textile Design, Industrial Products, UI/UX & Media Production in Chennai",
        "duration": "4 Years for B.Des / 5 Years for Integrated M.Sc Electronic Media",
        "eligibility": "12th Standard Pass in any stream from a recognized board.",
        "entrance_exams": [
            {"name": "NIFT Entrance Exam (CAT + GAT + Situation Test)", "level": "National", "official_portal": "https://www.nift.ac.in", "description": "National entrance exam for NIFT Chennai (includes State Domicile Quota for Tamil Nadu students)."},
            {"name": "Anna University Integrated Media Entrance", "level": "State", "official_portal": "https://www.annauniv.edu", "description": "For 5-Year Integrated M.Sc Electronic Media at CEG Campus."}
        ],
        "top_colleges": [
            "National Institute of Fashion Technology (NIFT), Taramani, Chennai",
            "DJ Academy of Design, Coimbatore",
            "Department of Media Sciences, CEG Anna University, Chennai"
        ],
        "admission_procedure": "For NIFT: Appear for Creative Ability Test (CAT) & General Ability Test (GAT) in February -> Situation Test -> Centralized Seat Allocation. State Domicile quota for Tamil Nadu. For Anna Univ Media: Merit-based single window admission.",
        "estimated_fees": {
            "anna_univ_media": "₹32,000 / year (Govt CEG Campus)",
            "nift_chennai": "₹1,90,000 / year (Central Govt Institute)",
            "djad_coimbatore": "₹2,10,000 / year"
        },
        "scholarships": [
            "SARTHAK Financial Assistance Scheme at NIFT (Up to 100% Tuition Fee Subsidy)",
            "Pudhumai Penn & Tamil Puthalvan (₹1,000/mo)",
            "Post-Matric Scholarship for SC/ST"
        ],
        "career_opportunities": [
            "Fashion & Textile Designer (Arvind, Madura Fashion, Raymond, FabIndia)",
            "UI/UX Product Designer (Zoho, Freshworks, Cognizant Interactive Chennai)",
            "Visual Effects & Animation Director (Media production studios in Kollywood / Chennai)",
            "Footwear & Leather Goods Specialist in Ambur-Ranipet Leather Corridor"
        ],
        "starting_salary_range": "₹4.5 LPA - ₹16.0 LPA",
        "future_study_options": ["M.Des at NIFT / IDC IIT Bombay"],
        "key_skills_needed": ["Visual Storytelling", "Color Theory", "Figma / Adobe Creative Suite", "Material Prototyping"]
    },
    {
        "id": "lateral_entry_diploma_12th",
        "title": "Direct 2nd-Year Lateral Entry Polytechnic Diploma (DOTE TN)",
        "category": "diploma_polytechnic",
        "grade_level": "after_12th_pcm",
        "icon_emoji": "⚡",
        "tagline": "Save 1 Year: Direct Admission into 2nd Year Diploma for 12th PCM / Vocational / ITI Students",
        "duration": "2 Years (Direct Entry into 3rd Semester)",
        "eligibility": "12th Standard Pass with Physics, Chemistry & Maths / 12th Vocational / 2-Year ITI Pass with 60%+.",
        "entrance_exams": [
            {"name": "DOTE Tamil Nadu Lateral Entry Admissions", "level": "State", "official_portal": "https://www.tnpoly.in", "description": "Directorate of Technical Education single-window merit admission based on 12th PCM / Vocational marks."}
        ],
        "top_colleges": [
            "Central Polytechnic College (CPT), Chennai",
            "PSG Polytechnic College, Coimbatore",
            "Murugappa Polytechnic College, Avadi, Chennai",
            "Government Polytechnic College, Coimbatore"
        ],
        "admission_procedure": "Apply online at tnpoly.in under Lateral Entry category -> Merit rank generated on 12th marks -> Single window seat allotment into 2nd year. 7.5% Govt School Free Quota applies.",
        "estimated_fees": {
            "govt_polytechnic": "₹2,482 / year",
            "aided_polytechnic": "₹12,000 / year"
        },
        "scholarships": [
            "Tamil Nadu 7.5% Govt School Free Quota",
            "Pudhumai Penn & Tamil Puthalvan (₹1,000/mo)",
            "Post-Matric Scholarship for SC/ST"
        ],
        "career_opportunities": [
            "Junior Engineer in Southern Railway (RRB)",
            "Automotive Assembly & EV Technician (Hyundai, Ashok Leyland)",
            "Substation Operator in TANGEDCO",
            "Direct Lateral Entry into 2nd Year B.E after Diploma completion"
        ],
        "starting_salary_range": "₹3.5 LPA - ₹6.8 LPA",
        "future_study_options": ["Direct Lateral Entry B.E / B.Tech via TNEA Counselling"],
        "key_skills_needed": ["Technical Schematics", "Circuit Analysis", "Workshop Safety", "Diagnostics"]
    },
    {
        "id": "nda_armed_forces_12th",
        "title": "National Defence Academy (NDA) & Indian Navy 10+2 B.Tech Cadet Scheme",
        "category": "defence_govt",
        "grade_level": "after_12th_pcm",
        "icon_emoji": "🎖️",
        "tagline": "100% Free Military College Degree + Commission as Lieutenant / Sub-Lieutenant / Flying Officer",
        "duration": "3 to 4 Years Military & B.Tech Degree (100% Free with Monthly Cadet Stipend)",
        "eligibility": "12th Pass with Physics, Chemistry & Mathematics (for Air Force, Navy & Naval Academy) or any stream (for Army). Unmarried male & female candidates. Age: 16.5 - 19.5 Years.",
        "entrance_exams": [
            {"name": "UPSC NDA & NA Examination", "level": "National", "official_portal": "https://www.upsc.gov.in", "description": "National Defence Academy written exam conducted twice a year (NDA I in April & NDA II in September)."},
            {"name": "Indian Navy 10+2 (B.Tech) Cadet Entry", "level": "National", "official_portal": "https://www.joinindiannavy.gov.in", "description": "Direct 4-Year B.Tech Degree at Indian Naval Academy Ezhimala based on JEE Main CRL Rank."}
        ],
        "top_colleges": [
            "National Defence Academy (NDA), Khadakwasla / Indian Naval Academy",
            "Air Force Administrative College (AFAC), Coimbatore, Tamil Nadu",
            "Sainik School Amaravathinagar, Udumalpet, Tiruppur, Tamil Nadu",
            "INS Rajali Naval Air Station, Arakkonam, Tamil Nadu"
        ],
        "admission_procedure": "Qualify UPSC NDA Written Exam (Mathematics 300 Marks + General Ability Test 600 Marks) -> 5-Day SSB Interview -> Strict Military Medical Board -> All India Merit List. Training is 100% Free with all boarding, food, uniforms, and books provided by Government of India!",
        "estimated_fees": {
            "defence_academy": "100% FREE (Zero tuition, free boarding, uniform, mess, medical & books provided by Govt of India)"
        },
        "scholarships": [
            "Cadet Training Stipend: ₹56,100 / month during final year military training",
            "Tamil Nadu Government Cash Award for inducted defence officers"
        ],
        "placement_stats": {
            "highest_package": "₹19.0 LPA (Starting Basic Pay ₹56,100 + MSP ₹15,500 + DA + Free Officer Quarters)",
            "average_package": "₹15.5 LPA",
            "median_package": "₹14.5 LPA",
            "placement_percentage": "100%",
            "top_recruiters": ["Indian Army, Indian Navy, Indian Air Force (Commissioned as Gazetted Officer)"]
        },
        "career_opportunities": [
            "Lieutenant in Indian Army (Commanding Infantry / Armoured / Artillery / Signals Platoon)",
            "Flying Officer in Indian Air Force (Fighter / Transport / Helicopter Pilot)",
            "Sub-Lieutenant in Indian Navy (Warship Executive / Technical Engineer Officer)",
            "Military Diplomat & Defence Strategist"
        ],
        "starting_salary_range": "₹14.5 LPA - ₹19.0 LPA (Basic Pay: ₹56,100 + MSP ₹15,500 + DA + Free Accommodation + Lifetime Pension)",
        "future_study_options": ["Defence Services Staff College (DSSC), Wellington, Nilgiris, Tamil Nadu"],
        "key_skills_needed": ["Officer Like Qualities (OLQ)", "Courage & Integrity", "Physical Stamina", "Mental Agility under Pressure"]
    }
]


# =====================================================================
# SCHOOL ENTRANCE EXAM CALENDAR (TAMIL NADU NEXT-STEP FOCUS)
# =====================================================================

SCHOOL_ENTRANCE_EXAMS: List[Dict[str, Any]] = [
    {
        "id": "exam_tnea_2027",
        "exam_name": "TNEA (Tamil Nadu Engineering Admissions)",
        "target_stage": "after_12th",
        "stage_badge": "After 12th (HSC PCM)",
        "admission_type": "Single-Window Counselling (No Entrance Exam)",
        "target_courses": ["B.E / B.Tech across Anna University (CEG, MIT, ACT), PSG Tech, CIT, SSN & 450+ TN Colleges"],
        "conducting_body": "Directorate of Technical Education (DOTE), Chennai, Tamil Nadu",
        "registration_start": "May 2027 (Post-12th Results)",
        "registration_deadline": "June 2027",
        "exam_date": "No Entrance Exam (Cutoff out of 200: Maths 100 + Physics 50 + Chemistry 50)",
        "official_url": "https://www.tneaonline.org",
        "eligibility_summary": "12th Standard Pass with Physics, Chemistry & Mathematics. 7.5% Govt School 100% Free Tuition & Hostel Quota.",
        "syllabus_highlights": "Tamil Nadu 12th State Board / CBSE PCM curriculum. Single-window online choice filling across 4 rounds based on aggregate cutoff."
    },
    {
        "id": "exam_tn_medical_neet_2027",
        "exam_name": "NEET-UG & Tamil Nadu Medical Selection (85% State Quota)",
        "target_stage": "after_12th",
        "stage_badge": "After 12th (HSC PCB)",
        "admission_type": "National Entrance Exam + State Counselling",
        "target_courses": ["MBBS & BDS across 36 Govt Medical Colleges in TN (MMC, Stanley, KMC, Madurai MC)"],
        "conducting_body": "National Testing Agency (NTA) & Selection Committee, Directorate of Medical Education (DME) TN",
        "registration_start": "February 2027",
        "registration_deadline": "March 2027",
        "exam_date": "May 2027 (First Sunday)",
        "official_url": "https://www.tnmedicalselection.net",
        "eligibility_summary": "12th Pass with Physics, Chemistry & Biology + Valid NEET-UG Score. 7.5% Horizontal Reservation for TN Govt School Students with 100% Free Education.",
        "syllabus_highlights": "NEET-UG 720 Marks (Biology 360, Physics 180, Chemistry 180). TN State Rank list published exclusively for 85% State Quota seats."
    },
    {
        "id": "exam_dote_polytechnic_2027",
        "exam_name": "DOTE Tamil Nadu Centralized Polytechnic Admissions",
        "target_stage": "after_10th",
        "stage_badge": "After 10th (SSLC) / 12th Lateral",
        "admission_type": "Single-Window Counselling (No Entrance Exam)",
        "target_courses": ["Regular 3-Yr Diploma (after 10th) & Direct 2nd-Yr Lateral Entry (after 12th/ITI) in Mechanical, Auto, EEE, CSE, Civil"],
        "conducting_body": "Directorate of Technical Education (DOTE), Tamil Nadu",
        "registration_start": "May 2027 (Post-10th Results)",
        "registration_deadline": "June 2027",
        "exam_date": "No Entrance Exam (Direct 10th SSLC Merit Admission)",
        "official_url": "https://www.tnpoly.in",
        "eligibility_summary": "10th SSLC Pass for Regular 3-Year Diploma; 12th PCM / Vocational / 2-Year ITI for Direct 2nd Year Lateral Entry.",
        "syllabus_highlights": "Single-window online seat allocation across CPT Chennai, PSG Poly, Murugappa Poly, Coimbatore Govt Poly with 7.5% free quota."
    },
    {
        "id": "exam_det_iti_2027",
        "exam_name": "Tamil Nadu DET ITI Admissions (Direct Technical Trades)",
        "target_stage": "after_10th",
        "stage_badge": "After 10th (SSLC Pass)",
        "admission_type": "Direct Merit Allotment (No Entrance Exam)",
        "target_courses": ["Electrician, Fitter, Wireman, Motor Mechanic, Welder across 100+ Govt ITIs in Tamil Nadu"],
        "conducting_body": "Directorate of Employment and Training (DET), Government of Tamil Nadu",
        "registration_start": "May 2027",
        "registration_deadline": "June 2027",
        "exam_date": "No Entrance Exam (Direct 10th SSLC Merit Admission)",
        "official_url": "https://skilltraining.tn.gov.in",
        "eligibility_summary": "10th Standard (SSLC) Pass. 100% Free Training + ₹750/month Govt Stipend + Free Laptop & Bus Pass.",
        "syllabus_highlights": "District-wise single-window online counselling for government industrial training institutes with direct campus apprenticeship."
    },
    {
        "id": "exam_tngasa_2027",
        "exam_name": "TNGASA (Tamil Nadu Govt Arts & Science Colleges Admissions)",
        "target_stage": "after_12th",
        "stage_badge": "After 12th (Any Stream)",
        "admission_type": "Single-Window Counselling (No Entrance Exam)",
        "target_courses": ["B.Sc Computer Science, B.Com, B.A Economics, B.Sc Maths/Physics across 164+ TN Govt Colleges"],
        "conducting_body": "Directorate of Collegiate Education (DCE), Tamil Nadu",
        "registration_start": "May 2027 (Post-12th Results)",
        "registration_deadline": "June 2027",
        "exam_date": "No Entrance Exam (Merit Cutoff based on 12th Marks)",
        "official_url": "https://www.tngasa.in",
        "eligibility_summary": "12th Standard Pass in relevant stream. 100% Free Education for female students under Pudhumai Penn and male under Tamil Puthalvan.",
        "syllabus_highlights": "Single-window centralized application for all 38 districts of Tamil Nadu. Annual tuition fees as low as ₹2,200/year in Govt Colleges."
    },
    {
        "id": "exam_tndalu_law_2027",
        "exam_name": "TNDALU 5-Year Law Admissions (SOEL & 14 Govt Law Colleges)",
        "target_stage": "after_12th",
        "stage_badge": "After 12th (Any Stream)",
        "admission_type": "Single-Window Counselling (No Entrance Exam)",
        "target_courses": ["5-Year Integrated B.A. LL.B (Hons), B.Com. LL.B, B.B.A. LL.B, B.C.A. LL.B"],
        "conducting_body": "Tamil Nadu Dr. Ambedkar Law University (TNDALU), Chennai",
        "registration_start": "May 2027",
        "registration_deadline": "June 2027",
        "exam_date": "No Entrance Exam (Merit Cutoff based on 12th Aggregate)",
        "official_url": "https://www.tndalu.ac.in",
        "eligibility_summary": "12th Standard Pass with min 70% for SOEL (60% for SC/ST). 7.5% Govt School Horizontal Reservation applies.",
        "syllabus_highlights": "Single-window online counselling for School of Excellence in Law (Chennai) and 14 Government Law Colleges across Tamil Nadu."
    },
    {
        "id": "exam_tnau_2027",
        "exam_name": "TNAU Undergraduate Admissions (Agriculture & Horticulture)",
        "target_stage": "after_12th",
        "stage_badge": "After 12th (PCB / PCM)",
        "admission_type": "Single-Window Counselling (No Entrance Exam)",
        "target_courses": ["B.Sc (Hons) Agriculture, B.Sc (Hons) Horticulture, B.Tech Agricultural Engineering"],
        "conducting_body": "Tamil Nadu Agricultural University (TNAU), Coimbatore",
        "registration_start": "May 2027",
        "registration_deadline": "June 2027",
        "exam_date": "No Entrance Exam (Merit Cutoff based on 12th Marks)",
        "official_url": "https://tnau.ac.in",
        "eligibility_summary": "12th Pass with PCB / Botany & Zoology. TNAU Cutoff calculated out of 200. 7.5% Govt School Free Quota.",
        "syllabus_highlights": "Online rank list and choice filling for constituent agricultural campuses in Coimbatore, Madurai, Killikulam, Trichy."
    },
    {
        "id": "exam_tanuvas_2027",
        "exam_name": "TANUVAS Veterinary Admissions (BVSc & AH / B.Tech)",
        "target_stage": "after_12th",
        "stage_badge": "After 12th (PCB Stream)",
        "admission_type": "Single-Window Counselling (No Entrance Exam)",
        "target_courses": ["B.V.Sc & A.H (5.5 Years) & B.Tech Food Technology / Poultry Technology"],
        "conducting_body": "Tamil Nadu Veterinary and Animal Sciences University (TANUVAS), Chennai",
        "registration_start": "June 2027",
        "registration_deadline": "July 2027",
        "exam_date": "No Entrance Exam (Merit Cutoff based on 12th Marks)",
        "official_url": "https://tanuvas.ac.in",
        "eligibility_summary": "12th Pass with PCB (Cutoff out of 200). 7.5% Horizontal Reservation for TN Govt School students with 100% Free Fees.",
        "syllabus_highlights": "Admission to historic Madras Veterinary College (Chennai), VC&RI Namakkal, Tirunelveli, Orathanadu, and Salem."
    },
    {
        "id": "exam_tnpsc_group4_2027",
        "exam_name": "TNPSC Group 4 & VAO Recruitment (Direct 10th Pass)",
        "target_stage": "after_10th",
        "stage_badge": "After 10th (SSLC Pass)",
        "admission_type": "State Competitive Written Exam",
        "target_courses": ["Village Administrative Officer (VAO), Junior Assistant, Typist, Bill Collector across TN Govt Departments"],
        "conducting_body": "Tamil Nadu Public Service Commission (TNPSC), Chennai",
        "registration_start": "January 2027",
        "registration_deadline": "February 2027",
        "exam_date": "June 2027",
        "official_url": "https://www.tnpsc.gov.in",
        "eligibility_summary": "Minimum 10th Standard (SSLC) Pass with Tamil language. Age: 21 - 32 years (Relaxed to 42 for BC/MBC/SC/ST). Permanent TN Govt Post.",
        "syllabus_highlights": "Single paper: 200 Questions / 300 Marks (Part A General Tamil 100 Qs + Part B General Studies & Aptitude 100 Qs)."
    },
    {
        "id": "exam_tnusrb_constable_2027",
        "exam_name": "TNUSRB Grade II Police Constable & Fireman (Direct 10th Pass)",
        "target_stage": "after_10th",
        "stage_badge": "After 10th (SSLC Pass)",
        "admission_type": "State Written Exam + Physical Test (PET)",
        "target_courses": ["Grade II Police Constable (Armed Reserve, TSP), Jail Warder & Fireman in Tamil Nadu"],
        "conducting_body": "Tamil Nadu Uniformed Services Recruitment Board (TNUSRB), Chennai",
        "registration_start": "August 2027",
        "registration_deadline": "September 2027",
        "exam_date": "December 2027",
        "official_url": "https://www.tnusrb.tn.gov.in",
        "eligibility_summary": "10th Standard (SSLC) Pass. Physical standards & endurance test required. Permanent TN Police Service.",
        "syllabus_highlights": "Part 1 Tamil Eligibility Test (80 Marks) + Part 2 Main Written Exam (General Knowledge & Psychology 70 Marks) + PET."
    },
    {
        "id": "exam_nda_upsc_2027",
        "exam_name": "UPSC NDA & NA Exam (Direct Commission After 12th)",
        "target_stage": "after_12th",
        "stage_badge": "After 12th (PCM / Any)",
        "admission_type": "National Written Exam + SSB Interview",
        "target_courses": ["Indian Army (Any Stream), Indian Air Force & Indian Navy (12th PCM) Officer Cadets"],
        "conducting_body": "Union Public Service Commission (UPSC)",
        "registration_start": "December 2026 (NDA I) / May 2027 (NDA II)",
        "registration_deadline": "January 2027 (NDA I) / June 2027 (NDA II)",
        "exam_date": "April 2027 (NDA I) / September 2027 (NDA II)",
        "official_url": "https://www.upsc.gov.in",
        "eligibility_summary": "Unmarried male/female candidates aged 16.5 to 19.5 years. 12th Pass or appearing in final year.",
        "syllabus_highlights": "Paper 1 Mathematics (300 Marks, 120 Qs) + Paper 2 General Ability Test (600 Marks, 150 Qs: English & GK) followed by 5-Day SSB Interview."
    }
]


def generate_school_exam_calendar_url(exam_dict: Dict[str, Any]) -> str:
    """Generates 1-click Google Calendar link only when a confirmed official date is available; otherwise empty."""
    exam_date = str(exam_dict.get("exam_date", "")).strip()
    reg_deadline = str(exam_dict.get("registration_deadline", "")).strip()
    
    # If unannounced or merit-based without specific calendar date, do not create speculative calendar link
    if "upcoming" in exam_date.lower() or "upcoming" in reg_deadline.lower() or "no entrance exam" in exam_date.lower() or "no exam" in exam_date.lower():
        return ""

    title = urllib.parse.quote(f"{exam_dict['exam_name']} — Registration Deadline")
    details = urllib.parse.quote(
        f"Official Portal: {exam_dict.get('official_url', '')}\n"
        f"Conducting Body: {exam_dict.get('conducting_body', '')}\n"
        f"Eligibility: {exam_dict.get('eligibility_summary', '')}\n"
        f"Courses: {', '.join(exam_dict.get('target_courses', []))}\n"
        f"Syllabus: {exam_dict.get('syllabus_highlights', '')}"
    )
    location = urllib.parse.quote(exam_dict.get("conducting_body", "Tamil Nadu, India"))
    return (
        f"https://calendar.google.com/calendar/render?action=TEMPLATE"
        f"&text={title}"
        f"&details={details}"
        f"&location={location}"
    )


def list_school_career_paths(category: Optional[str] = None, grade_level: Optional[str] = None) -> List[Dict[str, Any]]:
    """Returns curated directory of career paths in Tamil Nadu, optionally filtered."""
    results = SCHOOL_CAREER_PATHS
    if category and category != "all":
        results = [p for p in results if p["category"] == category]
    if grade_level and grade_level != "all":
        if grade_level == "after_10th":
            results = [p for p in results if p["grade_level"] == "after_10th" or p["grade_level"] == "after_10th_or_12th"]
        elif grade_level == "after_12th":
            results = [p for p in results if "after_12th" in p["grade_level"] or p["grade_level"] == "after_10th_or_12th"]
        else:
            results = [p for p in results if p["grade_level"] == grade_level or p["grade_level"] == "after_10th_or_12th"]
    return results


def get_school_career_path(path_id: str) -> Optional[Dict[str, Any]]:
    """Returns details for a single career path."""
    return next((p for p in SCHOOL_CAREER_PATHS if p["id"] == path_id), None)


def compare_school_career_paths(path_ids: List[str]) -> List[Dict[str, Any]]:
    """Returns up to 3 paths for side-by-side comparison."""
    path_map = {p["id"]: p for p in SCHOOL_CAREER_PATHS}
    return [path_map[pid] for pid in path_ids[:3] if pid in path_map]


def recommend_school_career_paths(
    current_grade: str,
    percentage: float,
    interests: List[str],
    budget_preference: Optional[str] = "any",
    preferred_location: Optional[str] = "Tamil Nadu"
) -> Dict[str, Any]:
    """AI logic that ranks best-fit career pathways in Tamil Nadu based on grade, marks and student interests."""
    scored_items = []
    interests_lower = [i.lower() for i in interests]

    for path in SCHOOL_CAREER_PATHS:
        p_grade = path["grade_level"]
        grade_match = False
        if current_grade == "10th":
            grade_match = (p_grade in ["after_10th", "after_10th_or_12th"])
        elif current_grade == "12th_pcm":
            grade_match = (p_grade in ["after_12th_pcm", "after_10th_or_12th", "after_12th_arts", "after_12th_commerce"])
        elif current_grade == "12th_pcb":
            grade_match = (p_grade in ["after_12th_pcb", "after_10th_or_12th", "after_12th_arts", "after_12th_commerce"])
        elif current_grade == "12th_commerce":
            grade_match = (p_grade in ["after_12th_commerce", "after_10th_or_12th", "after_12th_arts"])
        elif current_grade == "12th_arts":
            grade_match = (p_grade in ["after_12th_arts", "after_10th_or_12th"])
        elif current_grade == "12th_vocational":
            grade_match = (p_grade in ["after_12th_pcm", "after_10th", "after_10th_or_12th"])
        else:
            grade_match = True

        if not grade_match:
            continue

        score = 50

        if percentage >= 85:
            score += 20
        elif percentage >= 70:
            score += 15
        elif percentage >= 55:
            score += 10
        else:
            score += 5

        reasons = []
        action_plan = []
        path_text = (path["title"] + " " + path["tagline"] + " " + " ".join(path["career_opportunities"])).lower()

        matched_interests_count = 0
        for interest in interests_lower:
            if interest in path_text or interest in path["category"]:
                matched_interests_count += 1
                reasons.append(f"Direct alignment with your interest in '{interest.title()}'.")

        score += min(25, matched_interests_count * 10)

        if budget_preference == "govt_merit":
            if "100% Free" in path["estimated_fees"].get("govt_college", "") or "₹2,482" in path["estimated_fees"].get("govt_polytechnic", "") or "₹31,000" in path["estimated_fees"].get("govt_college", "") or "100% FREE" in str(path["estimated_fees"]):
                score += 5
                reasons.append("Eligible for Tamil Nadu 7.5% Govt School 100% Free Tuition & Hostel Quota.")

        final_match_pct = min(98, max(45, score))

        if not reasons:
            reasons.append(f"Excellent next-step pathway matching your {current_grade.replace('_', ' ').upper()} academic standing in Tamil Nadu.")

        action_plan.append(f"Aim for high cutoff in your 10th / 12th board examinations.")
        if path["entrance_exams"]:
            action_plan.append(f"Monitor {path['entrance_exams'][0]['name']} notifications on {path['entrance_exams'][0].get('official_portal', 'official site')}.")
        action_plan.append(f"Prepare applications for premier Tamil Nadu institutions like {path['top_colleges'][0]}.")

        scored_items.append({
            "path": path,
            "match_percentage": final_match_pct,
            "fit_reasons": reasons,
            "action_plan": action_plan
        })

    scored_items.sort(key=lambda x: x["match_percentage"], reverse=True)

    stream_guidance = (
        f"For a school student currently completing {current_grade.replace('_', ' ').upper()} with {percentage:.1f}% marks in Tamil Nadu, "
        f"we have identified {len(scored_items)} direct next-step educational pathways. "
        "Take full advantage of Tamil Nadu Single Window Counselling (TNEA, TN Medical Selection, DOTE Polytechnic, DET ITI, TNGASA, TNDALU, TNAU) "
        "along with the 7.5% Govt School 100% Free Quota, Pudhumai Penn, and Tamil Puthalvan financial assistance schemes."
    )

    return {
        "current_grade": current_grade,
        "percentage": percentage,
        "total_matches": len(scored_items),
        "top_recommendations": scored_items[:6],
        "stream_guidance": stream_guidance
    }


def get_school_entrance_exams_list() -> List[Dict[str, Any]]:
    """Returns upcoming school entrance exams with Google Calendar sync URLs."""
    results = []
    for exam in SCHOOL_ENTRANCE_EXAMS:
        item = dict(exam)
        item["google_calendar_url"] = generate_school_exam_calendar_url(item)
        results.append(item)
    return results


# =====================================================================
# TOP COLLEGE COMPARISON DATABASE (100% EXCLUSIVELY TAMIL NADU NEXT-STEPS)
# =====================================================================

TOP_COLLEGES_DATABASE: List[Dict[str, Any]] = [
    # ---------------- 1. ENGINEERING (TAMIL NADU — DIRECT AFTER 12TH PCM) ----------------
    {
        "id": "iit_madras",
        "name": "IIT Madras — Indian Institute of Technology Madras",
        "category": "engineering",
        "logo_emoji": "🏛️",
        "location": "Sardar Patel Road, Chennai, Tamil Nadu",
        "nirf_ranking": "NIRF Rank #1 (Overall & Engineering — Consecutive 8 Years in India)",
        "accreditation": "Institute of National Importance (Government of India)",
        "flagship_courses": ["B.Tech Computer Science & Engineering", "B.Tech AI & Data Analytics", "B.Tech Electrical / VLSI", "Dual Degree Aerospace / Robotics"],
        "eligibility_criteria": "Direct After 12th: 12th Pass with PCM, minimum 75% aggregate (65% for SC/ST/PwD) + Qualifying JEE Main and ranking top in JEE Advanced.",
        "entrance_exams": ["JEE Main (Session 1 & 2)", "JEE Advanced"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "Upcoming",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "1. Write JEE Main and qualify in top 2.5 lakh candidates. 2. Appear for JEE Advanced. 3. Register on JoSAA portal in June. 4. Fill choices in priority order. 5. Online document verification and seat acceptance fee.",
        "tuition_fees_per_year": "₹2,20,000 / year (100% Tuition Fee Waiver for SC/ST/PwD and family income < ₹1 Lakh; 66% waiver for income ₹1L - ₹5L)",
        "hostel_mess_fees_per_year": "₹45,000 / year",
        "scholarships_available": [
            "Institute Merit-cum-Means (MCM) Scholarship (Free tuition + ₹1,000/mo allowance)",
            "National Scholarship Portal Central Sector Scheme",
            "IITM Alumni Heritage Endowment Scholarships"
        ],
        "placement_stats": {
            "highest_package": "₹1.31 Crore / annum (International) | ₹66 LPA (Domestic)",
            "average_package": "₹21.48 LPA",
            "median_package": "₹17.0 LPA",
            "placement_percentage": "92.8%",
            "top_recruiters": ["Google", "Microsoft", "Apple", "Qualcomm", "NVIDIA", "Texas Instruments", "ISRO", "Goldman Sachs"]
        },
        "campus_facilities": [
            "IITM Research Park (India's premier deep-tech incubation ecosystem)",
            "Virgo Supercomputing Cluster & 5G Testbed Lab",
            "24x7 Central Library with 500,000+ technical volumes",
            "Olympic-size swimming pool, stadium, and lush green 630-acre campus"
        ],
        "pros": ["#1 Ranked Engineering Institute in India", "Direct access to IITM Research Park startup ecosystem", "World-class faculty and global alumni network"],
        "cons": ["Extremely high competitive cutoff (Top 1000 JEE Advanced Rank)", "Rigorous academic curriculum with heavy workload"]
    },
    {
        "id": "anna_univ_ceg",
        "name": "College of Engineering Guindy (CEG), Anna University",
        "category": "engineering",
        "logo_emoji": "🏛️",
        "location": "Sardar Patel Road, Guindy, Chennai, Tamil Nadu",
        "nirf_ranking": "NIRF Rank #13 (Engineering) | Est. 1794 (Oldest Technical Institution in India)",
        "accreditation": "NBA & NAAC A++ (State University Flagship Campus)",
        "flagship_courses": ["B.E Computer Science & Engineering", "B.E Electronics & Communication (ECE)", "B.Tech Information Technology", "B.E Mechanical Engineering"],
        "eligibility_criteria": "Direct After 12th: 12th Standard Pass from TN State Board / CBSE with PCM. TNEA Cutoff out of 200 (Typically 195 - 199.5 for Top Branches).",
        "entrance_exams": ["TNEA (Tamil Nadu Engineering Admissions — Purely 12th Marks Normalization)"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "No Entrance Exam (Merit Cutoff based on 12th Marks)",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "1. Register on TNEA portal (tneaonline.org). 2. Certificate verification at TFC centres. 3. TNEA General Rank list published. 4. Online Single-Window Counselling. 5. Crucial: 7.5% Horizontal Reservation for TN Govt School students with 100% Free Tuition, Hostel & Mess fees funded by TN Govt.",
        "tuition_fees_per_year": "₹31,000 / year (Govt Subsidized — ₹0 for First Generation Graduates & 7.5% Govt School Quota)",
        "hostel_mess_fees_per_year": "₹32,000 / year",
        "scholarships_available": [
            "Tamil Nadu 7.5% Govt School Horizontal Reservation (100% Free Tuition, Hostel, Mess)",
            "First Generation Graduate Tuition Fee Concession (₹25,000/year waiver)",
            "Pudhumai Penn & Tamil Puthalvan Schemes (₹1,000/month stipend)",
            "BC/MBC & SC/ST Post-Matric Welfare Scholarships"
        ],
        "placement_stats": {
            "highest_package": "₹40.0 LPA",
            "average_package": "₹10.8 LPA",
            "median_package": "₹8.5 LPA",
            "placement_percentage": "94.2%",
            "top_recruiters": ["Microsoft", "Cisco", "Amazon", "Caterpillar", "Zoho", "TVS Motors", "PayPal", "L&T"]
        },
        "campus_facilities": [
            "Historical 220-acre lush green Guindy campus in heart of Chennai",
            "State-of-the-art Robotics, AI, High Voltage & Automotive Labs",
            "Center for Aerospace Research & Drone Innovation",
            "Kurukshetra — India's first UNESCO-patronized techno-management fest"
        ],
        "pros": ["Lowest tuition fees in India for premier engineering (₹31k/yr)", "Top brand recognition across Tamil Nadu and global IT hubs", "Strong alumni network spanning 230+ years"],
        "cons": ["Requires near-perfect 12th cutoff (196+ out of 200 for CSE)", "Hostel infrastructure is historic and traditional"]
    },
    {
        "id": "nit_trichy",
        "name": "NIT Tiruchirappalli — National Institute of Technology Trichy",
        "category": "engineering",
        "logo_emoji": "🏛️",
        "location": "Thuvakudi, Tiruchirappalli (Trichy), Tamil Nadu",
        "nirf_ranking": "NIRF Rank #9 (Engineering) | #1 among all 31 NITs in India",
        "accreditation": "Institute of National Importance (Government of India)",
        "flagship_courses": ["B.Tech Computer Science & Engineering", "B.Tech Electronics & Communication", "B.Tech Electrical & Electronics", "B.Tech Mechanical Engineering"],
        "eligibility_criteria": "Direct After 12th: 12th Pass with PCM, minimum 75% aggregate + Qualifying JEE Main. 50% Home State Quota reserved for Tamil Nadu students.",
        "entrance_exams": ["JEE Main (Session 1 & Session 2)"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "Upcoming",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "1. Write JEE Main. 2. Register for JoSAA online counselling in June. 3. Select NIT Trichy under Home State (Tamil Nadu) quota. 4. Seat allotment based on All India Rank (AIR).",
        "tuition_fees_per_year": "₹1,45,000 / year (100% Tuition waiver for SC/ST and family income < ₹1 Lakh; 66% waiver for ₹1L - ₹5L)",
        "hostel_mess_fees_per_year": "₹42,000 / year",
        "scholarships_available": [
            "Central Sector Scheme of Scholarships for College and University Students",
            "Merit-Cum-Means (MCM) Scholarship",
            "ONGC / FAEA Scholarships"
        ],
        "placement_stats": {
            "highest_package": "₹52.8 LPA",
            "average_package": "₹15.7 LPA",
            "median_package": "₹12.0 LPA",
            "placement_percentage": "91.5%",
            "top_recruiters": ["Morgan Stanley", "Google", "Amazon", "Qualcomm", "Texas Instruments", "Intel", "Samsung R&D"]
        },
        "campus_facilities": [
            "800-acre residential campus with Siemens Centre of Excellence in Manufacturing",
            "Octagon Computer Centre with high-speed supercomputing servers",
            "24x7 Modern Library & Innovation Incubation Centre",
            "Pragyan — international techno-managerial fest"
        ],
        "pros": ["Ranked #1 NIT in India consistently", "50% Home State Quota specifically for Tamil Nadu students", "Exceptional core engineering and software placement records"],
        "cons": ["Trichy climate can be hot during summer months", "Far from Chennai metropolitan airport"]
    },
    {
        "id": "mit_anna_univ",
        "name": "Madras Institute of Technology (MIT Campus), Anna University",
        "category": "engineering",
        "logo_emoji": "✈️",
        "location": "Chromepet, Chennai, Tamil Nadu",
        "nirf_ranking": "Constituent Campus of Anna University (NIRF Rank #13) | Dr. APJ Abdul Kalam Alma Mater",
        "accreditation": "NBA Accredited & NAAC A++",
        "flagship_courses": ["B.Tech Aeronautical Engineering", "B.Tech Artificial Intelligence & Data Science", "B.Tech Automobile Engineering", "B.Tech Information Technology"],
        "eligibility_criteria": "Direct After 12th: 12th Standard Pass with PCM. High TNEA Cutoff out of 200 (~193-198 for Aero & IT).",
        "entrance_exams": ["TNEA (Tamil Nadu Engineering Admissions)"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "No Entrance Exam (Merit Cutoff based on 12th Marks)",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "TNEA Online Single Window Counselling via tneaonline.org. 7.5% Govt School reservation applies with 100% Free Tuition, Hostel & Mess.",
        "tuition_fees_per_year": "₹31,000 / year (Govt Subsidized — ₹0 for First Graduate & 7.5% Quota)",
        "hostel_mess_fees_per_year": "₹32,000 / year",
        "scholarships_available": [
            "7.5% TN Govt School Free Higher Education Scheme",
            "First Generation Graduate Concession (₹25,000/yr)",
            "Pudhumai Penn & Tamil Puthalvan (₹1,000/mo)"
        ],
        "placement_stats": {
            "highest_package": "₹38.5 LPA",
            "average_package": "₹9.8 LPA",
            "median_package": "₹7.8 LPA",
            "placement_percentage": "92.4%",
            "top_recruiters": ["Boeing", "Airbus", "Zoho", "TCS Digital", "Hyundai Motors", "Robert Bosch", "Cognizant"]
        },
        "campus_facilities": [
            "Pioneer Aerospace Hangar with real aircrafts and flight simulators",
            "Dr. APJ Abdul Kalam Innovation Centre",
            "Automotive Dynamics Test Track and EV testing lab"
        ],
        "pros": ["Legendary aerospace and automobile engineering heritage", "Alma mater of Bharat Ratna Dr. APJ Abdul Kalam", "Low government fee structure"],
        "cons": ["Campus is located in busy Chromepet suburban area"]
    },
    {
        "id": "psg_tech",
        "name": "PSG College of Technology (Autonomous), Coimbatore",
        "category": "engineering",
        "logo_emoji": "⚙️",
        "location": "Avinashi Road, Peelamedu, Coimbatore, Tamil Nadu",
        "nirf_ranking": "NIRF Rank #63 (Engineering) | Premier Govt-Aided Autonomous Institution",
        "accreditation": "NBA & NAAC A++ Accredited",
        "flagship_courses": ["B.E Robotics & Automation", "B.E Computer Science & Engineering", "B.E Mechanical Engineering (Sandwich 5-Yr)", "B.Tech Information Technology"],
        "eligibility_criteria": "Direct After 12th: 12th Standard Pass with PCM. High TNEA Cutoff for Govt-Aided seats (~192-198/200).",
        "entrance_exams": ["TNEA (Tamil Nadu Engineering Admissions)"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "No Entrance Exam (Merit Cutoff based on 12th Marks)",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "Single window online counselling via TNEA for Govt-Aided and Self-Supporting seats. Merit management quota available directly.",
        "tuition_fees_per_year": "₹45,000 / year (Govt-Aided Seats) | ₹1,20,000 / year (Self-Supporting)",
        "hostel_mess_fees_per_year": "₹55,000 / year",
        "scholarships_available": [
            "Tamil Nadu 7.5% Govt School Free Education",
            "First Generation Graduate Concession",
            "PSG Industrial Institute Merit Endowment"
        ],
        "placement_stats": {
            "highest_package": "₹42.0 LPA",
            "average_package": "₹11.2 LPA",
            "median_package": "₹9.0 LPA",
            "placement_percentage": "93.6%",
            "top_recruiters": ["Microsoft", "Qualcomm", "Robert Bosch", "Caterpillar", "Cognizant", "L&T", "Amazon"]
        },
        "campus_facilities": [
            "PSG Industrial Institute on-campus manufacturing units",
            "Centre of Excellence in Robotics, AI and Industrial IoT",
            "Sandwich engineering programmes with integrated industry apprenticeships"
        ],
        "pros": ["Industry-integrated Sandwich courses with live manufacturing experience", "Unbeatable core engineering reputation in South India", "High campus placement conversion"],
        "cons": ["Rigorous attendance and disciplinary rules"]
    },
    {
        "id": "ssn_chennai",
        "name": "SSN College of Engineering (Autonomous), Chennai",
        "category": "engineering",
        "logo_emoji": "🌟",
        "location": "Rajiv Gandhi Salai (OMR), Kalavakkam, Chennai, Tamil Nadu",
        "nirf_ranking": "NIRF Rank #45 (Engineering) | Founded by Shiv Nadar (HCL Technologies)",
        "accreditation": "NBA & NAAC A++ (Autonomous, Affiliated to Anna University)",
        "flagship_courses": ["B.E Computer Science & Engineering", "B.Tech AI & Data Science", "B.E Electronics & Communication", "B.E Biomedical Engineering"],
        "eligibility_criteria": "Direct After 12th: 12th Pass with PCM. High TNEA Cutoff (65% Single Window Seats) or SSN Merit Admission (35% Management Seats).",
        "entrance_exams": ["TNEA (Tamil Nadu Engineering Admissions)"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "No Entrance Exam (Merit Cutoff based on 12th Marks)",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "65% seats via TNEA single-window counselling; 35% management quota via merit walk-in based on 12th marks and aptitude.",
        "tuition_fees_per_year": "₹1,50,000 / year (Fixed by Tamil Nadu Govt Fee Committee)",
        "hostel_mess_fees_per_year": "₹65,000 / year",
        "scholarships_available": [
            "Shiv Nadar Foundation Merit Scholarships (₹4+ Crores disbursed annually)",
            "100% Tuition Fee Waiver for State Board Toppers",
            "Rural Talents Scholarship for Govt School students"
        ],
        "placement_stats": {
            "highest_package": "₹64.0 LPA",
            "average_package": "₹10.5 LPA",
            "median_package": "₹8.0 LPA",
            "placement_percentage": "95.1%",
            "top_recruiters": ["Amazon", "Atlassian", "Cisco", "HCLTech", "Barclays", "Goldman Sachs", "Infosys"]
        },
        "campus_facilities": [
            "250-acre Wi-Fi enabled modern green campus on OMR IT Corridor",
            "State-of-the-art Research Centres with internal funding grants up to ₹3 Lakhs/student project",
            "Air-conditioned auditorium, sports stadiums and gymnasium"
        ],
        "pros": ["Generous scholarship schemes disbursing ₹4+ Crores per year", "Prime location on OMR Chennai IT Highway", "Consistently high placement rate over 95%"],
        "cons": ["Distance from Central Chennai (approx 35 km)"]
    },

    # ---------------- 2. MEDICAL (TAMIL NADU — DIRECT AFTER 12TH PCB) ----------------
    {
        "id": "madras_medical_college",
        "name": "Madras Medical College (MMC), Chennai",
        "category": "medical",
        "logo_emoji": "🩺",
        "location": "EVR Periyar Salai, Park Town, Chennai, Tamil Nadu",
        "nirf_ranking": "NIRF Rank #11 (Medical) | Est. 1835 (3rd Oldest Medical Institution in Asia)",
        "accreditation": "National Medical Commission (NMC) & TN Dr. M.G.R. Medical University",
        "flagship_courses": ["MBBS (250 Seats)", "B.Pharm (Bachelor of Pharmacy)", "B.Sc Nursing (4-Year)", "BPT (Bachelor of Physiotherapy)"],
        "eligibility_criteria": "Direct After 12th: 12th Pass with PCB with min 50% + High NEET-UG score for MBBS; 12th PCB marks for Nursing/B.Pharm.",
        "entrance_exams": ["NEET-UG (National Eligibility cum Entrance Test)"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "Upcoming",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "1. Write NEET-UG. 2. Register for Tamil Nadu State Quota (85%) conducted by Selection Committee DME Kilpauk at tnmedicalselection.net. 3. Online choice filling and seat allotment. 4. Crucial: 7.5% Horizontal Reservation for TN Govt School students with 100% Free Tuition, Hostel & Mess.",
        "tuition_fees_per_year": "₹13,610 / year (Govt Medical College regulated - 100% Free under 7.5% quota)",
        "hostel_mess_fees_per_year": "₹28,000 / year",
        "scholarships_available": [
            "Tamil Nadu 7.5% Govt School Horizontal Reservation (100% Free Tuition, Hostel, Mess)",
            "Pudhumai Penn Scheme (₹1,000/month for female TN Govt school students)",
            "Tamil Puthalvan Scheme (₹1,000/month for male students)",
            "Post-Matric Scholarship for SC/SCA/ST students"
        ],
        "placement_stats": {
            "highest_package": "₹22.0 LPA | CRRI Internship Stipend: ₹25,000/month",
            "average_package": "₹11.5 LPA",
            "median_package": "₹9.6 LPA",
            "placement_percentage": "100%",
            "top_recruiters": ["Rajiv Gandhi Govt General Hospital (RGGGH)", "Tamil Nadu MRB", "Apollo Hospitals", "Fortis"]
        },
        "campus_facilities": [
            "Associated with Rajiv Gandhi Govt General Hospital (3,000+ beds, 10,000+ daily OPD patients)",
            "Historic red-brick heritage anatomy & pathology museum",
            "Asia's foremost tertiary referral clinical training exposure"
        ],
        "pros": ["Highest clinical patient volume in South India providing unmatched hands-on doctor training", "Extremely low government fee of ₹13,610/year", "Massive alumni presence across top UK NHS and US hospitals"],
        "cons": ["Very high NEET cutoff required to secure a seat", "Intense clinical duty hours during internship"]
    },
    {
        "id": "stanley_medical_college",
        "name": "Stanley Medical College (SMC), Chennai",
        "category": "medical",
        "logo_emoji": "🏥",
        "location": "Old Jail Road, Royapuram, Chennai, Tamil Nadu",
        "nirf_ranking": "Top 25 Medical in India | World-Renowned for Hand & Reconstructive Surgery",
        "accreditation": "National Medical Commission (NMC) & TN Dr. M.G.R. Medical University",
        "flagship_courses": ["MBBS (250 Seats)", "B.Sc Nursing", "B.Pharm"],
        "eligibility_criteria": "Direct After 12th: 12th Pass with PCB + Qualifying NEET-UG score for TN State Quota.",
        "entrance_exams": ["NEET-UG"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "Upcoming",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "Selection Committee DME Tamil Nadu conducts online centralized counselling via tnmedicalselection.net based on NEET-UG rank. 7.5% Govt School reservation applies.",
        "tuition_fees_per_year": "₹13,610 / year (Govt Medical College)",
        "hostel_mess_fees_per_year": "₹28,000 / year",
        "scholarships_available": [
            "Tamil Nadu 7.5% Govt School Free Education Scheme",
            "Pudhumai Penn & Tamil Puthalvan (₹1,000/mo)",
            "Post-Matric Scholarship for SC/ST"
        ],
        "placement_stats": {
            "highest_package": "₹20.0 LPA | CRRI Stipend: ₹25,000/month",
            "average_package": "₹11.0 LPA",
            "median_package": "₹9.2 LPA",
            "placement_percentage": "100%",
            "top_recruiters": ["Govt Stanley Hospital", "Tamil Nadu MRB", "Apollo Hospitals"]
        },
        "campus_facilities": [
            "Institute for Research and Rehabilitation of Hand and Plastic Surgery",
            "1,800-bed Govt Stanley Hospital with super-specialty surgical blocks",
            "Extensive trauma care and cadaveric dissection labs"
        ],
        "pros": ["Pioneer in hand transplantation and plastic surgery worldwide", "Government fees of only ₹13,610/year", "100% internship placement with ₹25,000/mo stipend"],
        "cons": ["Located in dense North Chennai old city area"]
    },
    {
        "id": "cmc_vellore",
        "name": "Christian Medical College (CMC), Vellore",
        "category": "medical",
        "logo_emoji": "🩺",
        "location": "Ida Scudder Road, Vellore, Tamil Nadu",
        "nirf_ranking": "NIRF Rank #3 (Medical) in India | Founded in 1900 by Dr. Ida Scudder",
        "accreditation": "National Medical Commission (NMC) & NABH Accredited",
        "flagship_courses": ["MBBS (100 Seats)", "B.Sc Nursing", "Allied Health Sciences (B.Sc MLT, Radiography)"],
        "eligibility_criteria": "Direct After 12th: 12th Pass with PCB (min 60%) + Qualified in NEET-UG.",
        "entrance_exams": ["NEET-UG"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "Upcoming",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "Admissions through Selection Committee, Directorate of Medical Education (DME) Tamil Nadu based on NEET-UG scores under State Govt and institutional merit categories.",
        "tuition_fees_per_year": "₹52,000 / year (Heavily subsidised through endowment funds)",
        "hostel_mess_fees_per_year": "₹45,000 / year",
        "scholarships_available": [
            "CMC Vellore Need-Based Full Tuition and Living Waivers",
            "Endowment Bursaries for economically disadvantaged students"
        ],
        "placement_stats": {
            "highest_package": "₹24.0 LPA",
            "average_package": "₹12.5 LPA",
            "median_package": "₹10.0 LPA",
            "placement_percentage": "100%",
            "top_recruiters": ["CMC Hospital Network", "AIIMS", "WHO", "Global Research Fellowships"]
        },
        "campus_facilities": [
            "Ranipet New Campus with 1,500-bed modern multi-specialty trauma hospital",
            "Town Campus with historic hospital and comprehensive clinical departments",
            "Wellcome Trust Research Laboratory & Stem Cell Research Centre"
        ],
        "pros": ["Consistently ranked #3 Medical College in India", "Deep ethos of community healthcare and empathy", "Subsidised fees compared to private medical colleges"],
        "cons": ["Strict service obligation bond to serve in rural mission hospitals"]
    },

    # ---------------- 3. ARTS & SCIENCE (TAMIL NADU — DIRECT AFTER 12TH) ----------------
    {
        "id": "loyola_chennai",
        "name": "Loyola College (Autonomous), Chennai",
        "category": "arts_science",
        "logo_emoji": "📚",
        "location": "Sterling Road, Nungambakkam, Chennai, Tamil Nadu",
        "nirf_ranking": "NIRF Rank #8 (Colleges in India) | NAAC A++ (CGPA 3.59)",
        "accreditation": "UGC College of Excellence (Autonomous, Affiliated to University of Madras)",
        "flagship_courses": ["B.Sc Computer Science & Data Science", "B.Com (General / Accounting & Finance)", "B.A Economics", "B.Sc Visual Communication (VisCom)"],
        "eligibility_criteria": "Direct After 12th: 12th Pass from TN State Board / CBSE with relevant subjects. High cutoffs (typically 90-97% for Shift-1 Day stream).",
        "entrance_exams": ["Merit-Based on 12th Marks + Loyola Online Application & Personal Interview"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "No Entrance Exam (Merit Cutoff based on 12th Marks)",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "Direct online application on loyolacollege.edu -> Category and marks-based shortlisting -> Personal interview -> Document verification and admission.",
        "tuition_fees_per_year": "₹42,000 / year (Aided Shift 1) | ₹85,000 / year (Self-Financed Shift 2)",
        "hostel_mess_fees_per_year": "₹55,000 / year",
        "scholarships_available": [
            "Loyola Management Scholarships for Economically Poor Students",
            "Post-Matric Govt Scholarships for SC/ST/BC/MBC",
            "Jesuit Alumni Bursaries"
        ],
        "placement_stats": {
            "highest_package": "₹21.0 LPA",
            "average_package": "₹6.8 LPA",
            "median_package": "₹5.5 LPA",
            "placement_percentage": "91.2%",
            "top_recruiters": ["Deloitte", "EY", "KPMG", "PwC", "Goldman Sachs", "McKinsey", "Google", "Zoho"]
        },
        "campus_facilities": [
            "99-acre historic tree-shaded campus in central Nungambakkam",
            "Pioneering Visual Communication media studio and editing labs",
            "World-class sports stadium that produced tennis grand slam legends"
        ],
        "pros": ["Prestigious alumni network including former President, Union Ministers & top CEOs", "Premier Big-4 accounting firm placements for B.Com", "Pioneering media studies VisCom course"],
        "cons": ["Very high cutoff for Day stream Shift-1", "Shift 1 is men only; Shift 2 is co-educational"]
    },
    {
        "id": "presidency_chennai",
        "name": "Presidency College (Autonomous), Chennai",
        "category": "arts_science",
        "logo_emoji": "🏛️",
        "location": "Kamarajar Salai (Marina Beach Road), Triplicane, Chennai, Tamil Nadu",
        "nirf_ranking": "NIRF Rank #3 (Colleges in India) | Est. 1840 | 'Mother of University of Madras'",
        "accreditation": "UGC Autonomous, NAAC A+ Grade (Tamil Nadu Government College)",
        "flagship_courses": ["B.Sc Physics", "B.Sc Mathematics", "B.A Economics", "B.Com", "B.Sc Statistics"],
        "eligibility_criteria": "Direct After 12th: 12th Standard Pass from TN State Board / CBSE with high subject aggregate.",
        "entrance_exams": ["TNGASA (Tamil Nadu Government Arts & Science Colleges Admissions)"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "No Entrance Exam (Merit Cutoff based on 12th Marks)",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "Apply via TNGASA portal (tngasa.in). 100% Free under Pudhumai Penn (for girls) and Tamil Puthalvan (for boys) with priority for Tamil Nadu Government school students.",
        "tuition_fees_per_year": "₹2,400 / year (Virtually Free Education — ₹0 for girls and SC/ST)",
        "hostel_mess_fees_per_year": "₹22,000 / year",
        "scholarships_available": [
            "Pudhumai Penn Scheme (₹1,000/month for female students)",
            "Tamil Puthalvan Scheme (₹1,000/month for male students)",
            "Full tuition fee waiver for SC/ST/PwD"
        ],
        "placement_stats": {
            "highest_package": "₹12.0 LPA",
            "average_package": "₹4.5 LPA",
            "median_package": "₹3.8 LPA",
            "placement_percentage": "84.5%",
            "top_recruiters": ["Wipro", "Cognizant", "TNPSC Aspirants", "TCS", "Ford India"]
        },
        "campus_facilities": [
            "Historic Victorian gothic campus facing Marina Beach",
            "Heritage science laboratories where Nobel Laureates Sir C.V. Raman & S. Chandrasekhar studied",
            "Extensive botanical garden and herbarium"
        ],
        "pros": ["Ranked #3 College in all of India by NIRF", "Tuition fee of only ₹2,400/year", "Alma mater of two Nobel Laureates in Physics"],
        "cons": ["Government administrative procedures can take time"]
    },
    {
        "id": "psg_cas_coimbatore",
        "name": "PSG College of Arts & Science (Autonomous), Coimbatore",
        "category": "arts_science",
        "logo_emoji": "🎓",
        "location": "Civil Aerodrome Post, Peelamedu, Coimbatore, Tamil Nadu",
        "nirf_ranking": "NIRF Rank #11 (Colleges) | Star College Scheme by DBT Govt of India",
        "accreditation": "NAAC A++ Grade (CGPA 3.61)",
        "flagship_courses": ["B.Com Professional Accounting", "B.Sc Computer Science", "B.Sc Biotechnology", "B.Sc Electronics"],
        "eligibility_criteria": "Direct After 12th: 12th Standard Pass with high cutoff.",
        "entrance_exams": ["Merit-based on 12th Marks via Online Application"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "No Entrance Exam (Merit Cutoff based on 12th Marks)",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "Online application at psgcas.ac.in -> Merit ranking based on 12th marks -> Online counselling and seat confirmation.",
        "tuition_fees_per_year": "₹35,000 / year (Aided) | ₹80,000 / year (Unaided)",
        "hostel_mess_fees_per_year": "₹48,000 / year",
        "scholarships_available": [
            "Pudhumai Penn & Tamil Puthalvan (₹1,000/mo)",
            "PSG Trust Merit Endowment Scholarships"
        ],
        "placement_stats": {
            "highest_package": "₹15.0 LPA",
            "average_package": "₹5.5 LPA",
            "median_package": "₹4.5 LPA",
            "placement_percentage": "89.2%",
            "top_recruiters": ["Goldman Sachs", "Amazon", "Deloitte", "Federal Bank", "Cognizant", "TCS"]
        },
        "campus_facilities": [
            "50-acre green campus in Peelamedu, Coimbatore",
            "DBT Star College supported high-end science labs",
            "Integrated coaching for CA / CMA professional exams"
        ],
        "pros": ["Premier Arts & Science institution in Western Tamil Nadu", "Excellent CA Foundation and Big-4 placement record", "NAAC A++ accreditation with highest CGPA"],
        "cons": ["High cutoff for B.Com Professional Accounting"]
    },

    # ---------------- 4. POLYTECHNIC & DIPLOMA (TAMIL NADU — AFTER 10TH & 12TH LATERAL) ----------------
    {
        "id": "cpt_chennai",
        "name": "Central Polytechnic College (CPT), Chennai",
        "category": "polytechnic_diploma",
        "logo_emoji": "🔧",
        "location": "CIT Campus, Taramani, Chennai, Tamil Nadu",
        "nirf_ranking": "Premier Government Polytechnic of Tamil Nadu | Est. 1916 (110+ Years Heritage)",
        "accreditation": "Directorate of Technical Education (DOTE), Government of Tamil Nadu & AICTE",
        "flagship_courses": [
            "Diploma in Mechanical Engineering",
            "Diploma in Computer Engineering",
            "Diploma in Electrical & Electronics Engineering (EEE)",
            "Diploma in Civil Engineering",
            "Direct 2nd-Year Lateral Entry Diploma (for 12th PCM / ITI)"
        ],
        "eligibility_criteria": "Regular 3-Year Diploma: Direct After 10th (SSLC Pass). Direct 2nd Year Lateral Entry: Direct After 12th PCM / Vocational / 2-Year ITI Pass with 60%+.",
        "entrance_exams": ["DOTE Tamil Nadu Centralized Polytechnic Admissions (No Entrance Exam Required)"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "No Entrance Exam (Direct 10th SSLC Merit Admission)",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "1. Apply online via DOTE portal (tnpoly.in). 2. Submit marks of 10th SSLC (for regular 3-year) or 12th/ITI (for lateral entry). 3. Single-window centralized merit counselling. 4. Crucial: 7.5% Horizontal Reservation for TN Govt School students with 100% Free Education, Hostel & Mess funded by TN Govt.",
        "tuition_fees_per_year": "₹2,482 / year (Govt Regulated — Virtually Free Education)",
        "hostel_mess_fees_per_year": "₹20,000 / year",
        "scholarships_available": [
            "Tamil Nadu 7.5% Govt School Horizontal Reservation (100% Free Tuition, Hostel, Mess)",
            "Pudhumai Penn Scheme (₹1,000/month for female TN Govt school students)",
            "Tamil Puthalvan Scheme (₹1,000/month for male students)",
            "Free Laptop Scheme for Govt Polytechnic Students",
            "AICTE Pragati Scholarship for Girls (₹50,000/year)"
        ],
        "placement_stats": {
            "highest_package": "₹7.5 LPA",
            "average_package": "₹3.8 LPA",
            "median_package": "₹3.2 LPA",
            "placement_percentage": "94.6%",
            "top_recruiters": ["Hyundai Motor India", "L&T Construction", "Ashok Leyland", "Royal Enfield", "MRF Tyres", "TVS Lucas", "Renault-Nissan"]
        },
        "campus_facilities": [
            "Extensive 40-acre campus inside Central Institutes of Technology (CIT) Taramani",
            "Industrial CNC Machining, Foundry, Heat Engines & Heavy Material Testing Labs",
            "Direct proximity to Tidel Park & OMR Tech Corridor"
        ],
        "pros": ["Virtually free tuition fee of ₹2,482/year", "Direct lateral entry into 2nd year B.E at Anna University CEG/MIT via TNEA", "100% placement pipeline into Chennai's automotive corridor"],
        "cons": ["Campus infrastructure is government-run and utilitarian"]
    },
    {
        "id": "psg_polytechnic",
        "name": "PSG Polytechnic College (Autonomous), Coimbatore",
        "category": "polytechnic_diploma",
        "logo_emoji": "⚙️",
        "location": "Avinashi Road, Peelamedu, Coimbatore, Tamil Nadu",
        "nirf_ranking": "India's Leading Govt-Aided Autonomous Polytechnic | Est. 1939",
        "accreditation": "AICTE Approved & NBA Accredited (Autonomous)",
        "flagship_courses": [
            "Diploma in Mechanical (Sandwich with Industry Internship)",
            "Diploma in Computer Engineering",
            "Diploma in Mechatronics Engineering",
            "Diploma in Automobile Engineering"
        ],
        "eligibility_criteria": "Regular: Direct After 10th Standard Pass. Lateral Entry: Direct After 12th PCM / ITI.",
        "entrance_exams": ["DOTE Tamil Nadu Polytechnic Admissions"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "No Entrance Exam (Direct 10th SSLC Merit Admission)",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "Single window DOTE admission (tnpoly.in) for Govt-Aided seats and PSG Merit Selection for Self-Supporting courses.",
        "tuition_fees_per_year": "₹12,000 / year (Govt-Aided Seats) | ₹45,000 / year (Self-Supporting)",
        "hostel_mess_fees_per_year": "₹45,000 / year",
        "scholarships_available": [
            "Tamil Nadu 7.5% Govt School Free Education Scheme",
            "Pudhumai Penn & Tamil Puthalvan (₹1,000/mo)",
            "PSG Industrial Institute Merit Bursaries"
        ],
        "placement_stats": {
            "highest_package": "₹8.2 LPA",
            "average_package": "₹4.2 LPA",
            "median_package": "₹3.6 LPA",
            "placement_percentage": "97.2%",
            "top_recruiters": ["Siemens", "Robert Bosch", "Caterpillar", "Titan Industries", "Schneider Electric", "Roots Industries"]
        },
        "campus_facilities": [
            "Integrated industry apprenticeship with PSG Industrial Institute on-campus",
            "Mechatronics and Robotics Automation Training Centre",
            "Modern CAD/CAM and CNC programming labs"
        ],
        "pros": ["Highest diploma placement percentage in India (97.2%)", "Unique Sandwich diploma integrating live factory shifts", "Smooth transition into PSG Tech B.E via lateral entry"],
        "cons": ["Demands rigorous punctuality and professional workshop discipline"]
    },
    {
        "id": "murugappa_poly",
        "name": "Murugappa Polytechnic College (Autonomous), Avadi, Chennai",
        "category": "polytechnic_diploma",
        "logo_emoji": "🏭",
        "location": "Sathyamurthy Nagar, Avadi, Chennai, Tamil Nadu",
        "nirf_ranking": "Premier Govt-Aided Autonomous Polytechnic | Murugappa Group Heritage",
        "accreditation": "AICTE Approved & NBA Accredited",
        "flagship_courses": [
            "Diploma in Mechanical Engineering",
            "Diploma in Electrical & Electronics Engineering",
            "Diploma in Tool & Die Making",
            "Diploma in Computer Engineering"
        ],
        "eligibility_criteria": "Regular: Direct After 10th Pass. Lateral Entry: Direct After 12th PCM / Vocational / ITI.",
        "entrance_exams": ["DOTE Tamil Nadu Single Window Counselling"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "No Entrance Exam (Direct 10th SSLC Merit Admission)",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "Admissions through DOTE tnpoly.in portal and institutional merit counselling. 7.5% Govt school reservation applies.",
        "tuition_fees_per_year": "₹10,500 / year (Govt Aided)",
        "hostel_mess_fees_per_year": "₹38,000 / year",
        "scholarships_available": [
            "Murugappa Group Merit Scholarship",
            "Pudhumai Penn & Tamil Puthalvan (₹1,000/mo)",
            "7.5% Govt School Free Seats"
        ],
        "placement_stats": {
            "highest_package": "₹7.0 LPA",
            "average_package": "₹3.6 LPA",
            "median_package": "₹3.2 LPA",
            "placement_percentage": "93.8%",
            "top_recruiters": ["TI Cycles", "Tube Investments of India", "Carborundum Universal", "Ashok Leyland", "Brakes India"]
        },
        "campus_facilities": [
            "Advanced Tool & Die making precision workshop",
            "Electrical machines testing lab and power electronics wing",
            "Automotive manufacturing hands-on workstations"
        ],
        "pros": ["Direct corporate linkage with Murugappa Group industrial conglomerates", "Specialized Tool & Die making program with 100% hiring demand", "Affordable aided fees"],
        "cons": ["Located in Avadi industrial sector outside central Chennai"]
    },

    # ---------------- 5. LAW (TAMIL NADU — 5-YEAR INTEGRATED DIRECT AFTER 12TH) ----------------
    {
        "id": "soel_tndalu",
        "name": "School of Excellence in Law (SOEL) — TNDALU, Chennai",
        "category": "law",
        "logo_emoji": "⚖️",
        "location": "MGR Salai, Perungudi, Chennai, Tamil Nadu",
        "nirf_ranking": "Pioneer State Law University of Tamil Nadu | Est. by Government of Tamil Nadu",
        "accreditation": "Bar Council of India (BCI) & UGC Approved",
        "flagship_courses": [
            "5-Year Integrated B.A. LL.B (Hons)",
            "5-Year Integrated B.B.A. LL.B (Hons)",
            "5-Year Integrated B.Com. LL.B (Hons)",
            "5-Year Integrated B.C.A. LL.B (Hons — Cyber Law Specialization)"
        ],
        "eligibility_criteria": "Direct After 12th: 12th Standard Pass from recognized board with min 70% aggregate (60% for SC/ST). No CLAT score required!",
        "entrance_exams": ["TNDALU Law Admissions (Purely Merit-Based on 12th Marks)"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "No Entrance Exam (Merit Cutoff based on 12th Marks)",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "1. Apply online at tndalu.ac.in. 2. Merit rank list generated based on 12th standard percentage. 3. Online Single-Window Counselling. 4. Crucial: 7.5% Horizontal Reservation for TN Govt School students with 100% Free Tuition, Hostel & Mess fees funded by TN Govt.",
        "tuition_fees_per_year": "₹85,000 / year (Honours Law Program — 100% Free under 7.5% Govt School Quota)",
        "hostel_mess_fees_per_year": "₹42,000 / year",
        "scholarships_available": [
            "Tamil Nadu 7.5% Govt School Horizontal Reservation (100% Free Tuition, Hostel, Mess)",
            "Pudhumai Penn Scheme (₹1,000/month for female TN Govt school students)",
            "Tamil Puthalvan Scheme (₹1,000/month for male students)",
            "Post-Matric Scholarship for SC/ST/SCA students"
        ],
        "placement_stats": {
            "highest_package": "₹16.0 LPA",
            "average_package": "₹6.5 LPA",
            "median_package": "₹5.2 LPA",
            "placement_percentage": "86.4%",
            "top_recruiters": ["Cyril Amarchand Mangaldas", "Shardul Amarchand Mangaldas", "Fox Mandal", "Madras High Court Chambers", "L&T Legal"]
        },
        "campus_facilities": [
            "Ultra-modern Perungudi campus on OMR IT Expressway",
            "High-tech Air-Conditioned Moot Court Halls replicating High Court benches",
            "Extensive Law Library with access to SCC Online, Manupatra & Westlaw"
        ],
        "pros": ["No CLAT required — admission strictly on 12th standard marks", "Offers unique B.C.A. LL.B (Hons) for Cyber Law and Tech Privacy", "Strong placement into corporate law firms and judicial services"],
        "cons": ["High cutoff percentage in 12th marks required for Honours"]
    },
    {
        "id": "tnnlu_trichy",
        "name": "Tamil Nadu National Law University (TNNLU), Tiruchirappalli",
        "category": "law",
        "logo_emoji": "🏛️",
        "location": "Dindigul Main Road, Navalurkuttappattu, Tiruchirappalli, Tamil Nadu",
        "nirf_ranking": "NIRF Rank #25 (Law) | Premier National Law University in Tamil Nadu",
        "accreditation": "Bar Council of India (BCI) & UGC Approved",
        "flagship_courses": ["5-Year Integrated B.A. LL.B (Hons)", "5-Year Integrated B.Com. LL.B (Hons)"],
        "eligibility_criteria": "Direct After 12th: 12th Standard Pass with min 45% + Valid score in CLAT (Common Law Admission Test). 50% Home State Quota reserved for Tamil Nadu students.",
        "entrance_exams": ["CLAT (Common Law Admission Test)"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "Upcoming",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "Appear for CLAT exam in December -> Register on Consortium of NLUs portal -> 50% seats allocated to Tamil Nadu domicile students -> Online document verification and seat confirmation.",
        "tuition_fees_per_year": "₹1,85,000 / year (Residential NLU Campus)",
        "hostel_mess_fees_per_year": "₹55,000 / year",
        "scholarships_available": [
            "Tamil Nadu Domicile Fee Subsidies",
            "Merit-cum-Means Scholarships from TNNLU Corpus"
        ],
        "placement_stats": {
            "highest_package": "₹18.0 LPA",
            "average_package": "₹8.5 LPA",
            "median_package": "₹7.0 LPA",
            "placement_percentage": "89.0%",
            "top_recruiters": ["Trilegal", "Khaitan & Co", "AZB & Partners", "Supreme Court Advocates on Record", "ICICI Bank Legal"]
        },
        "campus_facilities": [
            "25-acre modern residential campus in Trichy",
            "State-of-the-art Moot Court Hall and Legal Research Centres",
            "Digital law library with 24x7 database subscriptions"
        ],
        "pros": ["National Law University tag with 50% Home State Tamil Nadu Quota", "Top Tier-1 corporate law firm campus recruitments", "High success rate in Judicial Magistrate examinations"],
        "cons": ["Requires preparation for CLAT entrance examination"]
    },

    # ---------------- 6. AGRICULTURE & VETERINARY (TAMIL NADU — DIRECT AFTER 12TH PCB) ----------------
    {
        "id": "tnau_coimbatore",
        "name": "Tamil Nadu Agricultural University (TNAU), Coimbatore",
        "category": "agriculture",
        "logo_emoji": "🌾",
        "location": "Marudhamalai Road, Coimbatore, Tamil Nadu",
        "nirf_ranking": "NIRF Rank #5 (Agriculture & Allied) in India | Established in 1906",
        "accreditation": "Indian Council of Agricultural Research (ICAR) & State Agricultural University",
        "flagship_courses": [
            "B.Sc (Hons) Agriculture",
            "B.Sc (Hons) Horticulture",
            "B.Tech Agricultural Engineering",
            "B.Tech Food Technology",
            "B.Tech Biotechnology"
        ],
        "eligibility_criteria": "Direct After 12th: 12th Pass with Physics, Chemistry, Biology & Maths (or Botany & Zoology). TNAU Cutoff out of 200.",
        "entrance_exams": ["TNAU Undergraduate Single Window Counselling (No Entrance Exam Required)"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "No Entrance Exam (Merit Cutoff based on 12th Marks)",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "1. Apply online at tnau.ac.in. 2. Rank list published based on 12th marks. 3. Online Single-Window Counselling for 14 constituent campuses and 28 affiliated colleges across Tamil Nadu. 4. Crucial: 7.5% Horizontal Reservation for TN Govt School students with 100% Free Tuition, Hostel & Mess fees funded by TN Govt.",
        "tuition_fees_per_year": "₹48,000 / year (Govt constituent campus — 100% Free under 7.5% reservation)",
        "hostel_mess_fees_per_year": "₹35,000 / year",
        "scholarships_available": [
            "Tamil Nadu 7.5% Govt School Horizontal Reservation (100% Free Tuition, Hostel, Mess)",
            "Pudhumai Penn & Tamil Puthalvan Schemes (₹1,000/month stipend)",
            "ICAR National Talent Scholarship (NTS)"
        ],
        "placement_stats": {
            "highest_package": "₹12.0 LPA",
            "average_package": "₹5.6 LPA",
            "median_package": "₹4.8 LPA",
            "placement_percentage": "91.5%",
            "top_recruiters": ["ITC Agri Business", "Godrej Agrovet", "Syngenta", "NABARD", "State Bank of India (AFO)", "IFFCO"]
        },
        "campus_facilities": [
            "300-acre historic Coimbatore research campus with botanical garden & insect museum",
            "Centre for Plant Molecular Biology & Biotechnology (CPMB)",
            "Automated Smart Greenhouses"
        ],
        "pros": ["Ranked #5 Agricultural University in India", "Direct eligibility for Agricultural Officer (AO) via TNPSC", "100% Free fees for 7.5% TN Govt school students"],
        "cons": ["Requires high 12th cutoff (190+ out of 200 for B.Sc Agriculture)"]
    },
    {
        "id": "tanuvas_mvc_chennai",
        "name": "Madras Veterinary College (TANUVAS), Chennai",
        "category": "agriculture",
        "logo_emoji": "🐾",
        "location": "Vepery High Road, Vepery, Chennai, Tamil Nadu",
        "nirf_ranking": "Premier Veterinary Institution of Asia | Est. 1876 | TANUVAS",
        "accreditation": "Veterinary Council of India (VCI) & ICAR Approved",
        "flagship_courses": [
            "B.V.Sc & A.H (Bachelor of Veterinary Science & Animal Husbandry — 5.5 Years)",
            "B.Tech Food Technology",
            "B.Tech Poultry Technology"
        ],
        "eligibility_criteria": "Direct After 12th: 12th Pass with Biology (or Botany & Zoology), Physics, Chemistry. High 12th PCB Cutoff out of 200 (~190-197 for BVSc).",
        "entrance_exams": ["TANUVAS Single Window Counselling (Merit-Based on 12th Marks)"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "No Entrance Exam (Merit Cutoff based on 12th Marks)",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "Register at tanuvas.ac.in -> Rank list based on 12th PCB marks -> Single-window online counselling. 7.5% Govt School reservation applies with 100% free fees.",
        "tuition_fees_per_year": "₹18,500 / year (Govt Constituent College — 100% Free under 7.5% quota)",
        "hostel_mess_fees_per_year": "₹32,000 / year",
        "scholarships_available": [
            "Tamil Nadu 7.5% Govt School Free Education Scheme",
            "Pudhumai Penn & Tamil Puthalvan (₹1,000/mo)",
            "ICAR National Talent Scholarship"
        ],
        "placement_stats": {
            "highest_package": "₹15.0 LPA (Govt VAS: ₹65,000 - ₹90,000/month)",
            "average_package": "₹7.2 LPA",
            "median_package": "₹6.5 LPA",
            "placement_percentage": "100%",
            "top_recruiters": ["Tamil Nadu Animal Husbandry Dept (TNPSC)", "Aavin", "Hatsun Agro", "Suguna Foods", "Vandalur Zoo"]
        },
        "campus_facilities": [
            "150-year-old historic Vepery clinical hospital handling 500+ animal patients daily",
            "Small Animal Intensive Care Unit & Advanced Orthopaedic Surgery Wing",
            "Avian Disease Diagnosis Lab & Cattle Breeding Stations"
        ],
        "pros": ["100% career absorption as Veterinary Assistant Surgeon (VAS)", "Prestigious heritage as Asia's oldest veterinary college", "Low annual fee of ₹18,500/year"],
        "cons": ["Demands working with large animals and rural field postings"]
    },

    # ---------------- 7. ARCHITECTURE (TAMIL NADU — DIRECT AFTER 12TH PCM) ----------------
    {
        "id": "sap_anna_univ",
        "name": "School of Architecture and Planning (SAP), Anna University",
        "category": "architecture",
        "logo_emoji": "📐",
        "location": "Sardar Patel Road, Guindy, Chennai, Tamil Nadu",
        "nirf_ranking": "NIRF Rank #1 in Tamil Nadu & Top 10 in India for Architecture | Est. 1957",
        "accreditation": "Council of Architecture (CoA) & NAAC A++ (Anna University)",
        "flagship_courses": ["B.Arch (5-Year Bachelor of Architecture)", "B.Plan (4-Year Bachelor of Planning)"],
        "eligibility_criteria": "Direct After 12th: 12th Pass with PCM (min 50%) + Valid score in NATA (National Aptitude Test in Architecture). Merit calculated out of 400 (200 from 12th PCM + 200 from NATA).",
        "entrance_exams": ["NATA (National Aptitude Test in Architecture) + Anna University B.Arch Counselling"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "Upcoming",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "1. Write NATA exam. 2. Register for Anna University B.Arch single-window counselling (annauniv.edu). 3. Merit rank out of 400 generated. 4. Online seat selection. 5. 7.5% Govt School reservation applies with 100% Free Tuition & Hostel.",
        "tuition_fees_per_year": "₹42,000 / year (Govt Subsidized — ₹0 for 7.5% Quota & First Graduate)",
        "hostel_mess_fees_per_year": "₹32,000 / year",
        "scholarships_available": [
            "Tamil Nadu 7.5% Govt School Horizontal Reservation",
            "First Generation Graduate Concession",
            "Pudhumai Penn & Tamil Puthalvan (₹1,000/mo)"
        ],
        "placement_stats": {
            "highest_package": "₹15.0 LPA",
            "average_package": "₹6.2 LPA",
            "median_package": "₹5.0 LPA",
            "placement_percentage": "92.0%",
            "top_recruiters": ["Morphogenesis", "RSP Architects", "L&T Realty", "CRN Architects Chennai", "CMDA Chennai"]
        },
        "campus_facilities": [
            "Iconic architectural design studios with daylighting architecture",
            "Woodworking, Model Making, CNC Laser Cutting & 3D Printing Labs",
            "Climatology & Acoustic Simulation Testing Laboratories"
        ],
        "pros": ["#1 Architecture school in Tamil Nadu with highest prestige", "Subsidised government fee of ₹42,000/year", "Direct recruitment by top Chennai and international architectural firms"],
        "cons": ["Rigorous studio hours with intensive late-night design juries"]
    },
    {
        "id": "measi_architecture",
        "name": "MEASI Academy of Architecture (Autonomous), Chennai",
        "category": "architecture",
        "logo_emoji": "🏛️",
        "location": "Association Gardens, Peter's Road, Royapettah, Chennai, Tamil Nadu",
        "nirf_ranking": "Premier Autonomous Architecture Academy in Tamil Nadu | Affiliated to Anna University",
        "accreditation": "Council of Architecture (CoA) & NAAC Accredited",
        "flagship_courses": ["B.Arch (5-Year Bachelor of Architecture)"],
        "eligibility_criteria": "Direct After 12th: 12th PCM + Valid NATA Score.",
        "entrance_exams": ["NATA + Anna University Single Window / Management Merit"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "Upcoming",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "Admissions through Anna University B.Arch counselling and MEASI merit selection based on combined 12th + NATA score.",
        "tuition_fees_per_year": "₹1,25,000 / year",
        "hostel_mess_fees_per_year": "₹50,000 / year",
        "scholarships_available": [
            "MEASI Trust Merit Scholarships",
            "Post-Matric Government Scholarships"
        ],
        "placement_stats": {
            "highest_package": "₹12.0 LPA",
            "average_package": "₹5.5 LPA",
            "median_package": "₹4.5 LPA",
            "placement_percentage": "90.5%",
            "top_recruiters": ["Oscar & Ponni Architects", "Nataraj & Venkat Architects", "Gensler", "RSP Design"]
        },
        "campus_facilities": [
            "Design studios located in central Chennai heritage campus",
            "Digital Fabrication and BIM modeling suites",
            "Material testing museum and construction technology yard"
        ],
        "pros": ["Specialized exclusively in architecture with 100% institutional focus", "Prime Royapettah location in heart of Chennai", "Strong practitioner-faculty network"],
        "cons": ["Private college fee structure compared to SAP Anna University"]
    },

    # ---------------- 8. DESIGN (TAMIL NADU — DIRECT AFTER 12TH) ----------------
    {
        "id": "nift_chennai",
        "name": "National Institute of Fashion Technology (NIFT), Chennai",
        "category": "design",
        "logo_emoji": "🎨",
        "location": "Rajiv Gandhi Salai, Taramani, Chennai, Tamil Nadu",
        "nirf_ranking": "NIRF Rank #3 in Design & Fashion | Ministry of Textiles, Govt of India",
        "accreditation": "Statutory Institute under NIFT Act (Government of India)",
        "flagship_courses": [
            "B.Des Fashion Design",
            "B.Des Textile Design",
            "B.Des Leather Design",
            "B.Des Accessory Design",
            "B.F.Tech Apparel Production"
        ],
        "eligibility_criteria": "Direct After 12th: 12th Standard Pass in any stream (for B.Des) or 12th PCM (for B.F.Tech). NIFT Entrance Exam score.",
        "entrance_exams": ["NIFT Entrance Exam (CAT + GAT + Situation Test)"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "Upcoming",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "1. Apply online at nift.ac.in. 2. Clear Creative Ability Test (CAT) & General Ability Test (GAT). 3. Situation Test in April. 4. Centralized Seat Allocation with State Domicile quota for Tamil Nadu students.",
        "tuition_fees_per_year": "₹1,90,000 / year",
        "hostel_mess_fees_per_year": "₹55,000 / year",
        "scholarships_available": [
            "SARTHAK Financial Assistance Scheme (Up to 100% Tuition Fee Subsidy)",
            "National Scholarship Portal Schemes"
        ],
        "placement_stats": {
            "highest_package": "₹18.0 LPA",
            "average_package": "₹7.2 LPA",
            "median_package": "₹5.8 LPA",
            "placement_percentage": "94.0%",
            "top_recruiters": ["Arvind Fashions", "Titan", "Madura Fashion", "Raymond", "FabIndia", "H&M", "Shoppers Stop"]
        },
        "campus_facilities": [
            "Modern campus on OMR IT Corridor with specialized leather and garment technology centers",
            "Computer Aided Design (CAD) textile printing & weaving studios",
            "Leather testing laboratories and shoe prototyping workshops"
        ],
        "pros": ["National Institute of Fashion Technology brand recognition", "Tamil Nadu State Domicile reservation quota", "Proximity to South India's textile & leather manufacturing hubs"],
        "cons": ["High competition in CAT visual creativity tests"]
    },
    {
        "id": "dj_academy_design",
        "name": "DJ Academy of Design, Coimbatore",
        "category": "design",
        "logo_emoji": "✏️",
        "location": "Othakkalmandapam, Coimbatore, Tamil Nadu",
        "nirf_ranking": "Renowned Industrial & Product Design Institution in Western Tamil Nadu",
        "accreditation": "Founded by G.K. Sundaram (Lakshmi Mills)",
        "flagship_courses": ["B.Des Industrial Product Design", "B.Des Communication Design"],
        "eligibility_criteria": "Direct After 12th: 12th Standard Pass in any stream + DJAD Design Aptitude Test (DAT) & Portfolio Review.",
        "entrance_exams": ["DJAD Design Aptitude Test (DAT)"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "Upcoming",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "Admissions through DJAD Design Aptitude Test (DAT), personal interview and creative portfolio presentation.",
        "tuition_fees_per_year": "₹2,10,000 / year",
        "hostel_mess_fees_per_year": "₹60,000 / year",
        "scholarships_available": [
            "G.K. Sundaram Merit Scholarships for Creative Talents"
        ],
        "placement_stats": {
            "highest_package": "₹14.0 LPA",
            "average_package": "₹6.5 LPA",
            "median_package": "₹5.2 LPA",
            "placement_percentage": "91.0%",
            "top_recruiters": ["Tata Motors Design Studio", "TVS Design", "Titan", "Cognizant Interactive"]
        },
        "campus_facilities": [
            "Sprawling design workshop with wood, metal, plastic & digital prototyping labs",
            "Communication design animation and typography studios"
        ],
        "pros": ["Focus on tangible industrial product design and manufacturing ergonomics", "Small batch sizes with personalized master-apprentice mentorship", "High placement in automotive design studios"],
        "cons": ["Located in Coimbatore outskirts"]
    },

    # ---------------- 9. VOCATIONAL & ITI (TAMIL NADU — DIRECT AFTER 10TH) ----------------
    {
        "id": "govt_iti_guindy",
        "name": "Government Industrial Training Institute (ITI), Guindy, Chennai",
        "category": "vocational_iti",
        "logo_emoji": "🛠️",
        "location": "Alandur Road, Guindy Industrial Estate, Chennai, Tamil Nadu",
        "nirf_ranking": "Premier ITI in Tamil Nadu | Directorate of Employment & Training (DET)",
        "accreditation": "NCVT & Directorate of Employment and Training, Govt of Tamil Nadu",
        "flagship_courses": [
            "Electrician (2-Year Trade)",
            "Fitter (2-Year Trade)",
            "Machinist & CNC Operator (2-Year Trade)",
            "Mechanic Motor Vehicle (2-Year Trade)",
            "Welder & Sheet Metal Worker (1-Year Trade)"
        ],
        "eligibility_criteria": "Direct After 10th: 10th Standard (SSLC) Pass with Science & Maths. Age: Minimum 14 years.",
        "entrance_exams": ["DET Tamil Nadu ITI Online Merit Admissions (skilltraining.tn.gov.in)"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "No Entrance Exam (Direct 10th SSLC Merit Admission)",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "Apply online at skilltraining.tn.gov.in -> Selection on 10th marks -> Seat allotment. 100% Free Training + Free Uniforms, Free Bus Pass, Free Bicycle and ₹750/month Government stipend.",
        "tuition_fees_per_year": "100% FREE (Zero tuition fee + ₹750/month training allowance)",
        "hostel_mess_fees_per_year": "FREE",
        "scholarships_available": [
            "Tamil Nadu Govt Monthly Stipend: ₹750 / month",
            "National Apprenticeship Promotion Scheme (NAPS) stipend (₹8,000 - ₹12,000/mo)"
        ],
        "placement_stats": {
            "highest_package": "₹5.5 LPA",
            "average_package": "₹3.2 LPA",
            "median_package": "₹2.8 LPA",
            "placement_percentage": "96.0%",
            "top_recruiters": ["Hyundai Motor India", "Ashok Leyland", "TVS Motor", "Brakes India", "TANGEDCO", "Southern Railway"]
        },
        "campus_facilities": [
            "Located inside Guindy Industrial Estate with direct factory apprenticeships",
            "Modern CNC Machining Centre & Industrial Automation Labs",
            "Automotive Servicing Garage and electrical wiring bays"
        ],
        "pros": ["100% free education right after 10th with ₹750/mo govt stipend", "Direct lateral entry into 2nd year Polytechnic Diploma", "Immediate employment in Chennai's industrial corridors"],
        "cons": ["Manual workshop labor required"]
    },
    {
        "id": "govt_iti_coimbatore",
        "name": "Government Industrial Training Institute (ITI), Coimbatore",
        "category": "vocational_iti",
        "logo_emoji": "⚙️",
        "location": "G.N. Mills Post, Mettupalayam Road, Coimbatore, Tamil Nadu",
        "nirf_ranking": "Leading Vocational Institute in Western Tamil Nadu | DET",
        "accreditation": "NCVT & Directorate of Employment and Training, Govt of Tamil Nadu",
        "flagship_courses": [
            "Electrician",
            "Fitter & Tool Maker",
            "Turner & Machinist",
            "Refrigeration & Air Conditioning Mechanic (RAC)"
        ],
        "eligibility_criteria": "Direct After 10th: 10th Standard (SSLC) Pass from recognized board.",
        "entrance_exams": ["DET Tamil Nadu Single Window Counselling"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "No Entrance Exam (Direct 10th SSLC Merit Admission)",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "Admissions based on 10th marks via skilltraining.tn.gov.in. 100% Free with government welfare schemes.",
        "tuition_fees_per_year": "100% FREE",
        "hostel_mess_fees_per_year": "FREE",
        "scholarships_available": [
            "TN Govt Monthly Allowance ₹750/month",
            "Free Bicycle & Free Bus Pass"
        ],
        "placement_stats": {
            "highest_package": "₹5.0 LPA",
            "average_package": "₹3.0 LPA",
            "median_package": "₹2.6 LPA",
            "placement_percentage": "94.5%",
            "top_recruiters": ["Lakshmi Machine Works (LMW)", "ELGI Equipments", "Pricol", "Roots Industries", "TVS"]
        },
        "campus_facilities": [
            "Precision Tool and Die manufacturing workshop",
            "Air Conditioning & Refrigeration test chambers",
            "Textile machinery maintenance unit"
        ],
        "pros": ["Direct absorption into Coimbatore's motor and pump industries", "Zero tuition expense", "Gateway to lateral polytechnic diploma"],
        "cons": ["Strict workshop safety and discipline"]
    },

    # ---------------- 10. DEFENCE & DIRECT GOVT RECRUITMENT (DIRECT AFTER 10TH / 12TH) ----------------
    {
        "id": "nda_naval_cadet_academy",
        "name": "National Defence Academy (NDA) & Indian Navy 10+2 B.Tech Cadet Scheme",
        "category": "defence_govt",
        "logo_emoji": "🎖️",
        "location": "Tamil Nadu Candidate Screening Hub (Chennai / Coimbatore / Trichy)",
        "nirf_ranking": "Premier Military Officer Commissioning for 12th Passed Students | UPSC",
        "accreditation": "Ministry of Defence, Government of India & JNU / AICTE Degree",
        "flagship_courses": [
            "B.Tech / B.Sc / B.A Military Degree (3 Years NDA + 1 Year IMA / AFA / INA)",
            "Direct 4-Year B.Tech Degree at Indian Naval Academy (INA Ezhimala) via 10+2 Cadet Scheme"
        ],
        "eligibility_criteria": "Direct After 12th: 12th Pass with PCM (for Air Force, Navy & Naval Academy) or any stream (for Army). Age: 16.5 - 19.5 Years. Unmarried Indian citizens.",
        "entrance_exams": ["UPSC NDA & NA Exam (I & II)", "Indian Navy 10+2 B.Tech Cadet Scheme (via JEE Main Rank)"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "Upcoming",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "1. Clear UPSC NDA Written Exam (Maths 300 + GAT 600) or qualify JEE Main for Navy Cadet. 2. 5-Day SSB Interview at Selection Centre South. 3. Special Military Medical Examination. 4. All India Merit List. 100% Free Education with monthly cadet stipend!",
        "tuition_fees_per_year": "100% FREE (Zero tuition, free boarding, uniform, mess, medical & books provided by Govt of India)",
        "hostel_mess_fees_per_year": "FREE",
        "scholarships_available": [
            "Cadet Training Stipend: ₹56,100 / month during final year training",
            "Tamil Nadu Government Cash Award for inducted defence officers"
        ],
        "placement_stats": {
            "highest_package": "₹19.0 LPA (Starting Basic Pay ₹56,100 + MSP ₹15,500 + DA + Free Officer Quarters)",
            "average_package": "₹15.5 LPA",
            "median_package": "₹14.5 LPA",
            "placement_percentage": "100%",
            "top_recruiters": ["Indian Army, Indian Navy, Indian Air Force (Commissioned as Lieutenant / Sub-Lieutenant / Flying Officer)"]
        },
        "campus_facilities": [
            "Olympic-standard sports complexes, equestrian riding arenas, firing ranges",
            "Flight simulators and naval navigation bridge simulators",
            "Fully residential cadet squadrons with modern amenities"
        ],
        "pros": ["100% Free military degree right after 12th with monthly stipend", "Commissioned as Lieutenant / Flying Officer with immense national prestige", "Unmatched leadership responsibility and lifetime medical/pension benefits"],
        "cons": ["Requires exceptional physical stamina and clearing 5-day SSB interview"]
    },
    {
        "id": "tnpsc_training_institute",
        "name": "Tamil Nadu Public Service Commission (TNPSC Group 4 & VAO Direct Entry)",
        "category": "defence_govt",
        "logo_emoji": "🏛️",
        "location": "Frazer Bridge Road, VOC Nagar, Park Town, Chennai, Tamil Nadu",
        "nirf_ranking": "Apex Recruitment Commission of the Government of Tamil Nadu",
        "accreditation": "Constitutional Body under Article 315 (Government of Tamil Nadu)",
        "flagship_courses": [
            "Village Administrative Officer (VAO — Revenue Department)",
            "Junior Assistant (JA in Collectorates, Registration, Treasuries, Courts)",
            "Typist & Steno-Typist in Govt Departments",
            "Bill Collector Grade I"
        ],
        "eligibility_criteria": "Direct After 10th: Minimum 10th Standard (SSLC) Pass with eligibility for higher secondary admission. Knowledge of Tamil is mandatory. Age: 21 - 32 years (Relaxed to 42 for BC/MBC/SC/ST).",
        "entrance_exams": ["TNPSC Group 4 & VAO Examination (Single-Stage Written Test)"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "Upcoming",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "1. One-Time Registration (OTR) on tnpsc.gov.in. 2. Single-Stage Written Exam (200 Questions, 300 Marks: Part A General Tamil 100 Qs + Part B General Studies 75 Qs & Aptitude 25 Qs). 3. Certificate verification and Phase-wise counselling at TNPSC Office in Park Town, Chennai. 4. Same-day department and district allotment order!",
        "tuition_fees_per_year": "₹100 Application Fee (100% Free for SC/ST/PwD/Destitute Widows and 3 Free Chances for BC/MBC)",
        "hostel_mess_fees_per_year": "FREE (Free foundation training at Bhavanisagar Civil Services Institute)",
        "scholarships_available": [
            "Free TNPSC Coaching at all 38 District Employment Exchanges in Tamil Nadu",
            "Naan Mudhalvan competitive exam monthly allowance"
        ],
        "placement_stats": {
            "highest_package": "₹6.5 LPA (Junior Assistant / VAO: ₹24,000 - ₹38,000/month)",
            "average_package": "₹4.2 LPA",
            "median_package": "₹3.8 LPA",
            "placement_percentage": "100%",
            "top_recruiters": ["Tamil Nadu Revenue Dept", "Registration Dept", "Tamil Nadu Secretariat", "High Court Judicial Service"]
        },
        "campus_facilities": [
            "Civil Services Training Institute at Bhavanisagar (Erode district)",
            "District Collectorate revenue and administrative field attachments",
            "E-Governance computer labs and digital land records training center"
        ],
        "pros": ["Direct recruitment right after 10th Standard SSLC pass", "Permanent state government employment with zero risk of layoff", "Direct path to becoming Tahsildar / Deputy Collector through departmental promotions"],
        "cons": ["High number of applicants requiring rigorous preparation in General Tamil and General Studies"]
    },
    {
        "id": "tnusrb_constable_academy",
        "name": "TNUSRB Grade II Police Constable & Fireman Hub (Direct 10th Pass)",
        "category": "defence_govt",
        "logo_emoji": "👮",
        "location": "Oonamanchery, Vandalur, Chennai, Tamil Nadu",
        "nirf_ranking": "Tamil Nadu Uniformed Services Recruitment Board (TNUSRB)",
        "accreditation": "Home Department, Government of Tamil Nadu",
        "flagship_courses": [
            "Grade II Police Constable (Armed Reserve & Tamil Nadu Special Police)",
            "Jail Warder (Prison Department)",
            "Fireman (Tamil Nadu Fire and Rescue Services)"
        ],
        "eligibility_criteria": "Direct After 10th: 10th Standard (SSLC) Pass with Tamil as a subject. Age: 18 - 26 Years (Relaxed for BC/MBC/SC/ST). Height & Physical Endurance required.",
        "entrance_exams": ["TNUSRB Police Constable Written Exam + Physical Efficiency Test (PET)"],
        "exam_schedule": {
            "application_start": "Upcoming",
            "last_date": "Upcoming",
            "exam_date": "Upcoming",
            "result_date": "Upcoming"
        },
        "admission_counselling_process": "1. Online application on tnusrb.tn.gov.in. 2. Written Examination (Tamil Eligibility Test 80 Qs + Main Exam 70 Qs). 3. Physical Measurement & Endurance Tests (1,500m run, long jump, rope climbing). 4. Certificate Verification and appointment into Tamil Nadu Police Force.",
        "tuition_fees_per_year": "100% FREE (Govt sponsored training + Monthly training stipend)",
        "hostel_mess_fees_per_year": "FREE",
        "scholarships_available": [
            "Monthly Training Stipend during police academy training",
            "Free government accommodation, uniform allowance & medical benefits"
        ],
        "placement_stats": {
            "highest_package": "₹5.5 LPA (Constable: ₹24,000 - ₹38,000/month with Govt Quarters)",
            "average_package": "₹4.5 LPA",
            "median_package": "₹4.0 LPA",
            "placement_percentage": "100%",
            "top_recruiters": ["Tamil Nadu Police Department (Permanent Govt Service with promotion to Head Constable & SI)"]
        },
        "campus_facilities": [
            "130-acre training academy at Vandalur with tactical mock drill towns",
            "Indoor and outdoor computerized firing ranges",
            "State-of-the-art gymnasium, obstacle courses and parade grounds"
        ],
        "pros": ["Direct permanent Tamil Nadu government job right after 10th SSLC", "Clear promotion ladder to Head Constable, Special Sub-Inspector and SI", "Complete family medical insurance and government quarters"],
        "cons": ["Demanding emergency duty hours and 24x7 public service responsibilities"]
    }
]


# =====================================================================
# COURSE COMPARISON REPOSITORY (TAMIL NADU DIRECT NEXT-STEPS)
# =====================================================================

COURSE_COMPARISON_REPOSITORY: List[Dict[str, Any]] = [
    {
        "id": "hsc_bio_maths",
        "course_name": "11th & 12th Bio-Maths Stream (Group 1 - Tamil Nadu Board)",
        "category": "arts_science",
        "duration": "2 Years (Higher Secondary)",
        "eligibility": "Direct After 10th Standard (SSLC) Pass with good marks in Science & Maths.",
        "entrance_exams": ["School Merit Admissions (tnschools.gov.in)"],
        "avg_starting_salary": "Foundation for Professional Degrees (Engineering, MBBS, Agri)",
        "top_roles": ["Pre-Engineering", "Pre-Medicine", "Agricultural Sciences", "Biotechnology"],
        "future_scopes": ["Eligible for 100% of University Degree programs in India (B.Tech, MBBS, BDS, B.Sc Agri, B.Arch, Law, B.Sc, B.Com)"],
        "why_choose": "The most versatile 11th standard stream in Tamil Nadu: keeps both Engineering (TNEA) and Medical (NEET) pathways fully open."
    },
    {
        "id": "diploma_computer_engg",
        "course_name": "Polytechnic Diploma in Computer Engineering (DOTE Tamil Nadu)",
        "category": "polytechnic_diploma",
        "duration": "3 Years (Direct After 10th) OR 2 Years (Lateral Entry After 12th)",
        "eligibility": "10th Standard (SSLC) Pass from Tamil Nadu State Board or equivalent.",
        "entrance_exams": ["DOTE TN Polytechnic Admissions (tnpoly.in)"],
        "avg_starting_salary": "₹3.2 LPA - ₹6.5 LPA",
        "top_roles": ["Network Technician", "Web Developer", "Junior IT Support Engineer", "System Administrator"],
        "future_scopes": ["Direct 2nd Year Lateral Entry into B.E Computer Science at Anna University CEG / MIT via TNEA Counselling"],
        "why_choose": "Fastest and most affordable technical qualification right after 10th (₹2,482/yr) with guaranteed lateral entry into B.E."
    },
    {
        "id": "diploma_mechanical_engg",
        "course_name": "Polytechnic Diploma in Mechanical / Automobile (DOTE Tamil Nadu)",
        "category": "polytechnic_diploma",
        "duration": "3 Years (Regular) / 2 Years (Direct Lateral Entry)",
        "eligibility": "10th Standard (SSLC) Pass or 12th PCM / ITI.",
        "entrance_exams": ["DOTE TN Polytechnic Admissions (tnpoly.in)"],
        "avg_starting_salary": "₹3.5 LPA - ₹7.0 LPA",
        "top_roles": ["Junior Engineer (Southern Railway)", "CNC Machinist", "EV Assembly Technician", "Production Supervisor"],
        "future_scopes": ["Lateral Entry B.E Mechanical at PSG Tech / GCT / CEG Anna University", "AMIE Certification"],
        "why_choose": "Direct recruitment into Chennai's automotive corridor (Detroit of Asia: Hyundai, Ashok Leyland, Royal Enfield, TVS)."
    },
    {
        "id": "iti_electrician_fitter",
        "course_name": "2-Year ITI Electrician / Fitter Trade (DET Tamil Nadu)",
        "category": "vocational_iti",
        "duration": "2 Years (Practical Vocational Training)",
        "eligibility": "Direct After 10th Standard (SSLC) Pass. Minimum age 14.",
        "entrance_exams": ["DET Tamil Nadu ITI Admissions (skilltraining.tn.gov.in)"],
        "avg_starting_salary": "₹2.8 LPA - ₹5.5 LPA (100% Free Training + ₹750/mo Stipend)",
        "top_roles": ["Licensed Wireman", "Industrial Fitter", "Southern Railway Technician", "TANGEDCO Lineman"],
        "future_scopes": ["Direct 2nd Year Lateral Entry into Polytechnic Diploma", "National Apprenticeship Certificate (NAC)"],
        "why_choose": "100% free hands-on trade training with government stipend, free bicycle, and immediate employment in factory manufacturing."
    },
    {
        "id": "tnpsc_group4_vao",
        "course_name": "TNPSC Group 4 & VAO (Village Administrative Officer & Junior Assistant)",
        "category": "defence_govt",
        "duration": "Direct Recruitment into Tamil Nadu State Government Service",
        "eligibility": "Direct After 10th: 10th Standard (SSLC) Pass with Tamil language. Age: 21-32 years (up to 42 for BC/MBC/SC/ST).",
        "entrance_exams": ["TNPSC Group 4 & VAO Single-Stage Written Examination (300 Marks)"],
        "avg_starting_salary": "₹3.2 LPA - ₹5.0 LPA (Monthly: ₹24,000 - ₹38,000 + Govt Quarters & Pension)",
        "top_roles": ["Village Administrative Officer (VAO)", "Junior Assistant (JA)", "Typist", "Bill Collector"],
        "future_scopes": ["Departmental Promotion to Revenue Inspector (RI), Tahsildar, Revenue Divisional Officer (RDO)"],
        "why_choose": "Direct permanent state government job right after 10th standard pass with 100% job security and zero debt burden."
    },
    {
        "id": "btech_cse",
        "course_name": "B.E / B.Tech Computer Science & Engineering (TNEA & Anna Univ)",
        "category": "engineering",
        "duration": "4 Years (8 Semesters)",
        "eligibility": "Direct After 12th: 12th Pass with PCM. High TNEA Cutoff out of 200 (~190-199/200).",
        "entrance_exams": ["TNEA (Tamil Nadu Engineering Admissions)", "JEE Main (IITM / NITT)"],
        "avg_starting_salary": "₹6.5 LPA - ₹42.0 LPA",
        "top_roles": ["Full Stack Developer", "Cloud Solutions Architect", "AI/ML Engineer", "Product Specialist"],
        "future_scopes": ["M.Tech at Anna University CEG / IIT Madras", "MS in USA / Germany", "GATE for ISRO"],
        "why_choose": "Direct pipeline into Tamil Nadu's thriving IT corridors (OMR Chennai, Coimbatore, Trichy) with starting salaries up to ₹40+ LPA."
    },
    {
        "id": "btech_ece",
        "course_name": "B.E Electronics & Communication Engineering (ECE / VLSI)",
        "category": "engineering",
        "duration": "4 Years (8 Semesters)",
        "eligibility": "Direct After 12th: 12th Pass with PCM. TNEA Cutoff out of 200.",
        "entrance_exams": ["TNEA", "JEE Main"],
        "avg_starting_salary": "₹5.5 LPA - ₹32.0 LPA",
        "top_roles": ["VLSI Design Engineer", "Embedded Firmware Developer", "5G Telecom Specialist", "Automotive Systems Engineer"],
        "future_scopes": ["M.Tech VLSI at Anna University / IITM", "GATE for ISRO / DRDO", "Semiconductor R&D"],
        "why_choose": "High demand in Tamil Nadu's automotive and electronics hardware corridors (Foxconn, Pegatron, Bosch, Qualcomm Chennai)."
    },
    {
        "id": "mbbs_course",
        "course_name": "MBBS — Bachelor of Medicine & Surgery (Tamil Nadu DME Selection)",
        "category": "medical",
        "duration": "5.5 Years (4.5 Years Academics + 1 Year CRRI Internship)",
        "eligibility": "Direct After 12th: 12th Pass with Physics, Chemistry, Biology + Qualified in NEET-UG.",
        "entrance_exams": ["NEET-UG (Selection Committee DME Kilpauk 85% State Quota)"],
        "avg_starting_salary": "₹9.0 LPA - ₹18.0 LPA (Internship Stipend: ₹25,000/month)",
        "top_roles": ["Medical Officer (Tamil Nadu MRB)", "Resident Doctor", "Clinical Researcher", "Hospital Administrator"],
        "future_scopes": ["MD / MS via NEET-PG", "DM / M.Ch Super-Specialty", "MRCP / USMLE"],
        "why_choose": "Supreme societal respect, lifelong medical calling, 7.5% TN Govt School 100% Free Quota, and highly subsidised ₹13,610/yr fee."
    },
    {
        "id": "b_pharm_course",
        "course_name": "B.Pharm — Bachelor of Pharmacy (Tamil Nadu Paramedical Counselling)",
        "category": "medical",
        "duration": "4 Years (8 Semesters)",
        "eligibility": "Direct After 12th: 12th Pass with PCB or PCM. Cutoff based on 12th marks.",
        "entrance_exams": ["Tamil Nadu Paramedical / B.Pharm Single Window Counselling"],
        "avg_starting_salary": "₹4.0 LPA - ₹9.5 LPA",
        "top_roles": ["Drug Inspector (Tamil Nadu Drugs Control)", "Quality Control Chemist", "Formulation Scientist", "Hospital Pharmacist"],
        "future_scopes": ["M.Pharm via GPAT", "Pharm.D Post-Baccalaureate", "Drug Regulatory Affairs"],
        "why_choose": "Vital healthcare profession with high demand in Tamil Nadu pharmaceutical manufacturing zones and clinical research CROs."
    },
    {
        "id": "bsc_nursing_course",
        "course_name": "B.Sc Nursing (Tamil Nadu Paramedical Counselling)",
        "category": "medical",
        "duration": "4 Years (8 Semesters)",
        "eligibility": "Direct After 12th: 12th Pass with PCB with min 45%.",
        "entrance_exams": ["Tamil Nadu Paramedical / Nursing Counselling"],
        "avg_starting_salary": "₹3.8 LPA - ₹9.0 LPA (Overseas: ₹28 LPA - ₹48 LPA)",
        "top_roles": ["Staff Nurse (TN MRB)", "ICU / Trauma Specialist Nurse", "Nurse Educator", "International Clinical Nurse"],
        "future_scopes": ["M.Sc Nursing", "Critical Care Nurse Practitioner (NPCC)", "Hospital Administration (MHA)"],
        "why_choose": "Universal global employment demand (UK NHS, Germany, USA NCLEX-RN, Gulf) with lifelong job security."
    },
    {
        "id": "ba_llb_law",
        "course_name": "5-Year Integrated B.A. LL.B (Hons) / B.Com. LL.B (SOEL Chennai & TNDALU)",
        "category": "law",
        "duration": "5 Years (10 Semesters)",
        "eligibility": "Direct After 12th: 12th Pass with min 70% for SOEL (60% for SC/ST) or CLAT for TNNLU.",
        "entrance_exams": ["TNDALU Law Counselling (12th Marks)", "CLAT (TNNLU Trichy)"],
        "avg_starting_salary": "₹5.5 LPA - ₹18.0 LPA",
        "top_roles": ["High Court Advocate", "Civil Judge / Magistrate (TN Judicial Service)", "Corporate Legal Counsel", "Public Prosecutor"],
        "future_scopes": ["LL.M via TNDALU / CLAT PG", "Judicial Magistrate Exam", "Civil Services TNPSC Group 1"],
        "why_choose": "No CLAT required for SOEL Chennai (strictly on 12th marks); direct corporate advisory and judicial careers."
    },
    {
        "id": "bsc_agri_course",
        "course_name": "B.Sc (Hons) Agriculture / Horticulture (TNAU Coimbatore)",
        "category": "agriculture",
        "duration": "4 Years (8 Semesters)",
        "eligibility": "Direct After 12th: 12th Pass with PCB / Botany & Zoology. TNAU Cutoff out of 200.",
        "entrance_exams": ["TNAU Undergraduate Single Window Counselling (tnau.ac.in)"],
        "avg_starting_salary": "₹5.0 LPA - ₹12.0 LPA",
        "top_roles": ["Agricultural Officer (AO via TNPSC)", "Bank Agricultural Field Officer (IBPS AFO)", "Agribusiness Manager", "Agronomist"],
        "future_scopes": ["M.Sc (Agri) at TNAU / IARI", "Agribusiness MBA at IIM Ahmedabad / TNAU"],
        "why_choose": "Direct entry into prestigious Tamil Nadu Government Agricultural Department (AO/HO) and agribusiness corporate sector."
    },
    {
        "id": "barch_course",
        "course_name": "B.Arch — Bachelor of Architecture (Anna University SAP)",
        "category": "architecture",
        "duration": "5 Years (10 Semesters)",
        "eligibility": "Direct After 12th: 12th Pass with PCM (min 50%) + Valid score in NATA. Merit out of 400.",
        "entrance_exams": ["NATA (National Aptitude Test in Architecture) + Anna University Counselling"],
        "avg_starting_salary": "₹4.8 LPA - ₹15.0 LPA",
        "top_roles": ["Licensed Architect (COA)", "Urban Designer (CMDA Chennai)", "BIM Specialist", "Interior & Heritage Consultant"],
        "future_scopes": ["M.Arch at SAP Anna University", "Master of Urban Planning (M.Plan)"],
        "why_choose": "Blend of creative artistic vision and structural engineering with high infrastructure growth in Chennai and Tamil Nadu."
    },
    {
        "id": "nda_military",
        "course_name": "NDA Commissioned Officer / Navy 10+2 B.Tech Cadet Scheme",
        "category": "defence_govt",
        "duration": "3 to 4 Years Military B.Tech Degree (100% Free with Stipend)",
        "eligibility": "Direct After 12th: 12th Pass with PCM / relevant stream. Age: 16.5 - 19.5 Years.",
        "entrance_exams": ["UPSC NDA Exam", "Indian Navy 10+2 Cadet Scheme (JEE Main)"],
        "avg_starting_salary": "₹14.5 LPA - ₹19.0 LPA (100% Free Education + Monthly Stipend)",
        "top_roles": ["Lieutenant (Indian Army)", "Flying Officer (Indian Air Force)", "Sub-Lieutenant (Indian Navy)"],
        "future_scopes": ["Defence Services Staff College (DSSC), Wellington, Nilgiris, Tamil Nadu"],
        "why_choose": "Supreme national pride, prestigious military leadership, 100% free education with stipend, and lifelong officer benefits."
    }
]


def list_top_colleges(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """Returns top colleges directory (100% Tamil Nadu next-steps), optionally filtered by category."""
    if category and category != "all":
        return [c for c in TOP_COLLEGES_DATABASE if c["category"] == category]
    return TOP_COLLEGES_DATABASE


def get_top_college(college_id: str) -> Optional[Dict[str, Any]]:
    """Returns single college profile."""
    return next((c for c in TOP_COLLEGES_DATABASE if c["id"] == college_id), None)


def compare_top_colleges(college_ids: List[str]) -> List[Dict[str, Any]]:
    """Returns up to 3 colleges for side-by-side comparison."""
    c_map = {c["id"]: c for c in TOP_COLLEGES_DATABASE}
    return [c_map[cid] for cid in college_ids[:3] if cid in c_map]


def list_comparable_courses() -> List[Dict[str, Any]]:
    """Returns course comparison repository for Tamil Nadu next-steps."""
    return COURSE_COMPARISON_REPOSITORY


def compare_courses(course_ids: List[str]) -> List[Dict[str, Any]]:
    """Returns up to 3 courses for side-by-side comparison."""
    c_map = {c["id"]: c for c in COURSE_COMPARISON_REPOSITORY}
    return [c_map[cid] for cid in course_ids[:3] if cid in c_map]


# =====================================================================
# CAREER POSITIONS & RELEVANT ENTRANCE EXAMS DIRECTORY (TAMIL NADU FOCUS)
# =====================================================================

CAREER_POSITIONS_DATABASE: List[Dict[str, Any]] = [   {   'future_career_growth': [   'Junior Software Engineer -> SDE II -> Senior Software Engineer -> Technical Lead '
                                    '-> Engineering Manager / Solutions Architect'],
        'government_perks_quotas': 'Eligible for Tamil Nadu 7.5% Govt School 100% Free Tuition & Hostel Quota; Naan '
                                   'Mudhalvan free coding kits and certifications.',
        'id': 'pos_software_engineer',
        'position_description': 'Designs, develops, tests, and deploys high-scale software applications, full-stack '
                                'web platforms, mobile apps, and machine learning models for top technology companies '
                                'and global delivery centres.',
        'position_title': 'Software Engineer / Cloud & AI Developer',
        'qualification_badge': '12th PCM / Diploma Lateral',
        'qualification_stage': 'after_12th',
        'recruiting_organizations': [   'Zoho',
                                        'TCS',
                                        'Infosys',
                                        'Cognizant',
                                        'Amazon',
                                        'Freshworks',
                                        'Kaar Technologies',
                                        'Anna University Campus Placement'],
        'relevant_entrance_exams': [   {   'conducting_body': 'Directorate of Technical Education (DoTE), Chennai',
                                           'exam_category': 'State Single-Window Cutoff Counselling',
                                           'exam_date': 'No Entrance Exam (Cutoff Merit)',
                                           'exam_name': 'TNEA (Tamil Nadu Engineering Admissions)',
                                           'exam_pattern': 'Cutoff formula: Mathematics (100) + Physics (50) + '
                                                           'Chemistry (50) = 200 Marks',
                                           'how_to_prepare': 'Score 95%+ in TN State Board or CBSE 12th Mathematics, '
                                                             'Physics, and Chemistry.',
                                           'official_portal': 'https://www.tneaonline.org',
                                           'registration_window': 'May - June 2027',
                                           'selection_stages': '12th Board PCM Cutoff Marks (out of 200) -> 4 Rounds '
                                                               'of Online Single Window Seat Allotment (Anna Univ, PSG '
                                                               'Tech, SSN, CIT)'},
                                       {   'conducting_body': 'National Testing Agency (NTA)',
                                           'exam_category': 'National Entrance Exam',
                                           'exam_date': 'Session 1: January | Session 2: April',
                                           'exam_name': 'JEE Main (Joint Entrance Examination)',
                                           'exam_pattern': '300 Marks (Physics 100, Chemistry 100, Mathematics 100). '
                                                           '75 MCQs + Numerical.',
                                           'how_to_prepare': 'NCERT concepts + previous 5-year JEE Main papers with '
                                                             'timed mock tests.',
                                           'official_portal': 'https://jeemain.nta.nic.in',
                                           'registration_window': 'Session 1: Nov-Dec | Session 2: Feb-Mar',
                                           'selection_stages': 'Computer Based Test (CBT) -> JoSAA Counselling for NIT '
                                                               'Trichy & IIIT Kancheepuram'},
                                       {   'conducting_body': 'Tata Consultancy Services (TCS iON)',
                                           'exam_category': 'Corporate Recruitment Assessment',
                                           'exam_date': 'Quarterly Testing Windows',
                                           'exam_name': 'TCS NQT / National Qualifier Test',
                                           'exam_pattern': 'Numerical Ability, Verbal Ability, Reasoning Ability, and '
                                                           'Hands-on Coding (Python/Java/C++)',
                                           'how_to_prepare': 'Data structures, algorithms, aptitude problems, and OOP '
                                                             'concepts.',
                                           'official_portal': 'https://www.tcs.com/careers',
                                           'registration_window': 'Conducted 4 times a year',
                                           'selection_stages': 'Online Cognitive + Coding Test -> Technical Interview '
                                                               '-> HR Interview'}],
        'salary_range': '₹4.5 - ₹18 LPA (Fresher) -> ₹25 - ₹50+ LPA (Lead / Architect)',
        'sector': 'Engineering & Technology'},
    {   'future_career_growth': [   'Graduate Engineer Trainee -> Design Engineer -> R&D Specialist -> Plant Manager / '
                                    'Vice President of Manufacturing'],
        'government_perks_quotas': 'Direct employment in TN SIPCOT industrial clusters; subsidized industrial training '
                                   'subsidies under Naan Mudhalvan.',
        'id': 'pos_mechanical_engineer',
        'position_description': 'Engineers and manufactures automotive systems, EV drivetrains, robotics, thermal '
                                'machinery, and precision components across Chennai-Hosur automotive corridors.',
        'position_title': 'Mechanical & Automobile Design Engineer',
        'qualification_badge': '12th PCM / 10th Polytechnic Lateral',
        'qualification_stage': 'after_12th',
        'recruiting_organizations': [   'Hyundai Motor India',
                                        'Ashok Leyland',
                                        'TVS Motor',
                                        'Renault Nissan',
                                        'L&T Heavy Engineering',
                                        'Royal Enfield',
                                        'Tata Motors'],
        'relevant_entrance_exams': [   {   'conducting_body': 'DoTE Tamil Nadu / Anna University',
                                           'exam_category': 'State Single-Window Cutoff Counselling',
                                           'exam_date': 'No Entrance Exam (Cutoff Merit)',
                                           'exam_name': 'TNEA (Tamil Nadu Engineering Admissions)',
                                           'exam_pattern': 'PCM Cutoff out of 200 marks',
                                           'how_to_prepare': 'Strengthen mechanics, calculus, thermodynamics in 12th '
                                                             'standard.',
                                           'official_portal': 'https://www.tneaonline.org',
                                           'registration_window': 'May - June 2027',
                                           'selection_stages': '12th PCM Cutoff -> Single Window Choice Filling for '
                                                               'CEG, MIT, PSG Tech, CIT Coimbatore'},
                                       {   'conducting_body': 'IITs / IISc',
                                           'exam_category': 'National PSU & Higher Study Exam',
                                           'exam_date': 'February',
                                           'exam_name': 'GATE (Graduate Aptitude Test in Engineering - Mechanical)',
                                           'exam_pattern': '65 Questions / 100 Marks (Engineering Mathematics, General '
                                                           'Aptitude, Core Mechanical Subjects)',
                                           'how_to_prepare': 'Master strength of materials, fluid mechanics, '
                                                             'thermodynamics, and manufacturing technology.',
                                           'official_portal': 'https://gate2025.iitr.ac.in',
                                           'registration_window': 'August - September',
                                           'selection_stages': 'Online Computer-Based Test (100 Marks) -> Direct '
                                                               'recruitment by ONGC, BHEL Trichy, IOCL, ISRO, DRDO'}],
        'salary_range': '₹3.8 - ₹9.5 LPA (Fresher) -> ₹15 - ₹28 LPA (Senior Specialist)',
        'sector': 'Engineering & Technology'},
    {   'future_career_growth': [   'Silicon Design Engineer -> Senior Hardware Architect -> Director of Semiconductor '
                                    'Engineering'],
        'government_perks_quotas': 'Covered under Tamil Nadu Semiconductor & Advanced Electronics Policy 2024 with '
                                   'special state R&D grants.',
        'id': 'pos_ece_vlsi_engineer',
        'position_description': 'Designs microchips, embedded IoT controllers, 5G RF hardware, and semiconductor '
                                'circuitry for consumer electronics, telecom, and aerospace systems.',
        'position_title': 'Electronics & Communications (ECE) / VLSI Chip Designer',
        'qualification_badge': '12th PCM',
        'qualification_stage': 'after_12th',
        'recruiting_organizations': [   'Qualcomm',
                                        'Texas Instruments',
                                        'Intel',
                                        'ISRO',
                                        'Bharat Electronics (BEL)',
                                        'Foxconn Chennai',
                                        'Samsung R&D'],
        'relevant_entrance_exams': [   {   'conducting_body': 'DoTE Tamil Nadu',
                                           'exam_category': 'State Single-Window Cutoff Counselling',
                                           'exam_date': 'No Entrance Exam (Cutoff Merit)',
                                           'exam_name': 'TNEA (Tamil Nadu Engineering Admissions)',
                                           'exam_pattern': 'PCM Cutoff out of 200 marks',
                                           'how_to_prepare': 'Focus on 12th physics (electromagnetism, semiconductor '
                                                             'physics) and mathematics.',
                                           'official_portal': 'https://www.tneaonline.org',
                                           'registration_window': 'May - June',
                                           'selection_stages': '12th PCM Cutoff -> Anna Univ CEG, MIT Campus, SSN, PSG '
                                                               'Tech ECE branches'},
                                       {   'conducting_body': 'ISRO / Department of Space',
                                           'exam_category': 'Central PSU Scientific Scientist/Engineer Exam',
                                           'exam_date': 'Scheduled post-notification',
                                           'exam_name': 'ISRO Centralised Recruitment Board (ICRB)',
                                           'exam_pattern': '80 Core Electronics Questions (Signals, Digital Circuits, '
                                                           'Microprocessors, Communication Systems)',
                                           'how_to_prepare': 'Master digital electronics, signal processing, and '
                                                             'antenna wave propagation.',
                                           'official_portal': 'https://www.isro.gov.in',
                                           'registration_window': 'Announced as per vacancy',
                                           'selection_stages': 'Written Examination (80 MCQs) -> Technical Interview '
                                                               "-> Scientist/Engineer 'SC' Appointment"}],
        'salary_range': '₹5.5 - ₹16 LPA (Fresher) -> ₹25 - ₹60 LPA (Semiconductor Lead)',
        'sector': 'Engineering & Technology'},
    {   'future_career_growth': [   'Assistant Engineer (AE) -> Assistant Executive Engineer (AEE) -> Executive '
                                    'Engineer (EE) -> Superintending Engineer (SE) -> Chief Engineer'],
        'government_perks_quotas': 'Official vehicle, govt quarters, medical insurance, pension benefits, and 7.5% '
                                   'Govt School reservation.',
        'id': 'pos_civil_pwd_engineer',
        'position_description': 'Supervises structural construction, highway expressways, bridges, water supply '
                                'systems, and public infrastructure projects across Tamil Nadu.',
        'position_title': 'Civil Engineer / PWD Assistant Engineer (AE)',
        'qualification_badge': '12th PCM',
        'qualification_stage': 'after_12th',
        'recruiting_organizations': [   'Tamil Nadu PWD',
                                        'Highways Department',
                                        'TWAD Board',
                                        'L&T Construction',
                                        'Chennai Metro Rail (CMRL)',
                                        'Afcons Infrastructure'],
        'relevant_entrance_exams': [   {   'conducting_body': 'DoTE Tamil Nadu',
                                           'exam_category': 'State Single-Window Cutoff Counselling',
                                           'exam_date': 'No Entrance Exam (Cutoff Merit)',
                                           'exam_name': 'TNEA (Tamil Nadu Engineering Admissions)',
                                           'exam_pattern': 'PCM Cutoff out of 200 marks',
                                           'how_to_prepare': 'Score high in 12th Maths, Physics, and Chemistry.',
                                           'official_portal': 'https://www.tneaonline.org',
                                           'registration_window': 'May - June',
                                           'selection_stages': '12th Board PCM Cutoff -> Anna University CEG Guindy & '
                                                               'Govt Engineering Colleges'},
                                       {   'conducting_body': 'Tamil Nadu Public Service Commission (TNPSC)',
                                           'exam_category': 'Tamil Nadu State Gazetted Technical Exam',
                                           'exam_date': 'Scheduled post-notification',
                                           'exam_name': 'TNPSC Combined Engineering Services Examination (CESE)',
                                           'exam_pattern': 'Paper 1 Civil Engg (300 Marks, 200 Qs) + Paper 2 General '
                                                           'Studies & Tamil (200 Marks)',
                                           'how_to_prepare': 'Standard civil engineering textbooks (Surveying, '
                                                             'Building Materials, RCC Design, Soil Mechanics).',
                                           'official_portal': 'https://www.tnpsc.gov.in',
                                           'registration_window': 'Annual Notification (as per TNPSC Planner)',
                                           'selection_stages': 'Written Exam (Paper 1 Subject + Paper 2 Tamil '
                                                               'Eligibility & GS) -> Certificate Verification -> '
                                                               'Direct Appointment as Assistant Engineer'}],
        'salary_range': '₹36,700 - ₹1,16,200 / month (Level 16 TN Govt Pay Scale) or ₹4.5 - ₹12 LPA (L&T)',
        'sector': 'Engineering & Technology'},
    {   'future_career_growth': [   'Junior Engineer -> Senior Section Engineer (SSE) -> Direct Lateral Entry into 2nd '
                                    'Year B.E -> Assistant Engineer'],
        'government_perks_quotas': '100% Free Tuition, Hostel & Mess in Govt Polytechnics under 7.5% TN Govt School '
                                   'Quota; Pudhumai Penn & Tamil Puthalvan ₹1,000/month.',
        'id': 'pos_junior_engineer_diploma',
        'position_description': 'Oversees day-to-day shopfloor manufacturing, field maintenance, CAD drafting, machine '
                                'diagnostics, and technical quality inspection right after 3-year polytechnic diploma.',
        'position_title': 'Junior Engineer (JE) / Technical Supervisor (Diploma)',
        'qualification_badge': 'Direct 10th (SSLC Pass)',
        'qualification_stage': 'after_10th',
        'recruiting_organizations': [   'TANGEDCO',
                                        'Chennai Metro',
                                        'Indian Railways (RRB JE)',
                                        'BHEL Trichy',
                                        'Ashok Leyland',
                                        'Murugappa Group'],
        'relevant_entrance_exams': [   {   'conducting_body': 'Directorate of Technical Education (DoTE), Tamil Nadu',
                                           'exam_category': 'State Single-Window Cutoff Counselling',
                                           'exam_date': 'No Entrance Exam (10th SSLC Merit Admission)',
                                           'exam_name': 'DOTE Tamil Nadu Centralized Polytechnic Admissions',
                                           'exam_pattern': 'Total 10th Marks out of 500 (Tamil, English, Maths, '
                                                           'Science, Social)',
                                           'how_to_prepare': 'Score high in 10th Science and Mathematics.',
                                           'official_portal': 'https://www.tnpoly.in',
                                           'registration_window': 'May - June (Immediately after 10th results)',
                                           'selection_stages': '10th SSLC Total Marks (out of 500) -> Merit rank list '
                                                               '-> Single-window seat allotment across CPT Chennai, '
                                                               'PSG Poly, Murugappa Poly, Coimbatore Govt Poly'},
                                       {   'conducting_body': 'Railway Recruitment Control Board (RRB)',
                                           'exam_category': 'Central Government Technical Recruitment',
                                           'exam_date': 'Scheduled via RRB Calendar',
                                           'exam_name': 'RRB Junior Engineer (Railway Recruitment Board)',
                                           'exam_pattern': 'Stage 1: 100 Qs / 90 Mins | Stage 2: 150 Qs / 120 Mins '
                                                           '(100 Technical Domain)',
                                           'how_to_prepare': 'Revise 3-year polytechnic curriculum and practice basic '
                                                             'quantitative aptitude.',
                                           'official_portal': 'https://www.rrbchennai.gov.in',
                                           'registration_window': 'Periodic Central Notification',
                                           'selection_stages': 'CBT Stage 1 (Maths, Reasoning, General Science) -> CBT '
                                                               'Stage 2 (Technical Domain) -> Medical Fitness'}],
        'salary_range': '₹18,000 - ₹35,000 / month (Fresher) -> ₹45,000 - ₹80,000 / month (Senior JE)',
        'sector': 'Engineering & Technology'},
    {   'future_career_growth': [   'Apprentice -> Certified Technician -> Maintenance Supervisor -> Direct 2nd Year '
                                    'Lateral Entry to Polytechnic Diploma'],
        'government_perks_quotas': '100% Free Training, Free Govt Laptop, Free Bicycle, Free Bus Pass, Free Uniforms, '
                                   'and ₹750/month Govt Stipend.',
        'id': 'pos_iti_skilled_technician',
        'position_description': 'Executes high-precision electrical wiring, CNC milling, welding, motor winding, '
                                'refrigeration, and automotive servicing across modern factories.',
        'position_title': 'Skilled Industrial Technician & Electrician / CNC Machinist',
        'qualification_badge': 'Direct 10th (SSLC Pass)',
        'qualification_stage': 'after_10th',
        'recruiting_organizations': [   'TNSTC (Tamil Nadu State Transport)',
                                        'TANGEDCO',
                                        'Integral Coach Factory (ICF Chennai)',
                                        'L&T Valves',
                                        'TVS Lucas',
                                        'Brakes India'],
        'relevant_entrance_exams': [   {   'conducting_body': 'Directorate of Employment and Training (DET), Tamil '
                                                              'Nadu',
                                           'exam_category': 'Direct State Merit Online Admissions',
                                           'exam_date': 'No Entrance Exam (Direct 10th SSLC Merit Admission)',
                                           'exam_name': 'Tamil Nadu DET ITI Admissions',
                                           'exam_pattern': 'Merit rank based on 10th standard SSLC marks',
                                           'how_to_prepare': 'Pass 10th standard board exam from recognized board.',
                                           'official_portal': 'https://skilltraining.tn.gov.in',
                                           'registration_window': 'May - June',
                                           'selection_stages': 'Online registration based on 10th marks -> '
                                                               'District-wise counselling -> Direct admission into '
                                                               '100+ Govt ITIs with zero fees'},
                                       {   'conducting_body': 'Ministry of Skill Development & DET Tamil Nadu',
                                           'exam_category': 'Industry Paid Practical Certification',
                                           'exam_date': 'Annual AITT Exam',
                                           'exam_name': 'Apprenticeship Training Scheme (NATS / NAPS)',
                                           'exam_pattern': 'Practical trade skill assessment + theory paper',
                                           'how_to_prepare': 'Hands-on workshop practice during ITI course.',
                                           'official_portal': 'https://www.apprenticeshipindia.gov.in',
                                           'registration_window': 'Year-round portal registration',
                                           'selection_stages': '1-Year on-the-job industrial apprenticeship with '
                                                               'monthly stipend -> All India Trade Test (AITT) -> '
                                                               'National Apprenticeship Certificate (NAC)'}],
        'salary_range': '₹15,000 - ₹28,000 / month + ₹750/mo govt stipend during training',
        'sector': 'Engineering & Technology'},
    {   'future_career_growth': [   'MBBS (5.5 Years) -> CRMI Internship -> NEET-PG (MD / MS in Cardiology, Neurology, '
                                    'Ortho, Paediatrics) -> Super Speciality (DM / M.Ch)'],
        'government_perks_quotas': '7.5% Horizontal Reservation for TN Govt School Students with 100% Free Tuition, '
                                   'Books & Hostel funded entirely by TN Govt.',
        'id': 'pos_medical_doctor_mbbs',
        'position_description': 'Diagnoses illnesses, performs medical surgeries, prescribes therapies, and '
                                'administers critical healthcare in government hospitals and private multispeciality '
                                'medical institutions.',
        'position_title': 'Medical Doctor / General Physician & Surgeon (MBBS)',
        'qualification_badge': '12th PCB (Physics, Chemistry, Biology)',
        'qualification_stage': 'after_12th',
        'recruiting_organizations': [   'Tamil Nadu Medical Services Corporation (TNMSC)',
                                        'Directorate of Medical Services (DMS)',
                                        'Apollo Hospitals',
                                        'Kauvery Hospital',
                                        'MIOT',
                                        'Christian Medical College Vellore'],
        'relevant_entrance_exams': [   {   'conducting_body': 'National Testing Agency (NTA)',
                                           'exam_category': 'National Mandatory Medical Entrance Exam',
                                           'exam_date': 'First Sunday of May',
                                           'exam_name': 'NEET-UG (National Eligibility cum Entrance Test)',
                                           'exam_pattern': '720 Marks: Biology (Botany 180 + Zoology 180 = 360), '
                                                           'Physics (180), Chemistry (180). 180 MCQs to answer from '
                                                           '200.',
                                           'how_to_prepare': 'Thorough NCERT 11th & 12th Biology line-by-line mastery '
                                                             '+ regular physics problem solving.',
                                           'official_portal': 'https://neet.nta.nic.in',
                                           'registration_window': 'February - March',
                                           'selection_stages': 'National Pen-and-Paper Written Test (720 Marks) -> TN '
                                                               'State Merit Rank List -> Selection Committee DME '
                                                               'Counselling for 36 Govt Medical Colleges'},
                                       {   'conducting_body': 'Directorate of Medical Education (DME), Kilpauk, '
                                                              'Chennai',
                                           'exam_category': 'State Single-Window Medical Seat Allotment',
                                           'exam_date': 'Online Counselling Sessions (July - August)',
                                           'exam_name': 'Selection Committee DME Tamil Nadu 85% State Quota '
                                                        'Counselling',
                                           'exam_pattern': 'Merit rank derived exclusively from NEET-UG score',
                                           'how_to_prepare': 'Keep community certificate, nativity certificate, and '
                                                             'NEET scorecard ready.',
                                           'official_portal': 'https://www.tnmedicalselection.net',
                                           'registration_window': 'June - July (Post-NEET Results)',
                                           'selection_stages': 'Registration on tnmedicalselection.net -> Release of '
                                                               'TN State Merit Rank List -> 4 Rounds of Online Seat '
                                                               'Allotment (MMC, Stanley, Kilpauk, Madurai MC)'}],
        'salary_range': '₹55,000 - ₹95,000 / month (Intern / Medical Officer) -> ₹1.5 - ₹5+ Lakhs / month '
                        '(Postgraduate MD/MS Specialist)',
        'sector': 'Medical & Healthcare'},
    {   'future_career_growth': [   'BDS (5 Years) -> NEET-MDS (Master of Dental Surgery) -> Specialised Practice / '
                                    'Maxillofacial Surgery'],
        'government_perks_quotas': 'Covered under 7.5% Govt School Free Quota; Pudhumai Penn & Tamil Puthalvan '
                                   'assistance.',
        'id': 'pos_dental_surgeon_bds',
        'position_description': 'Treats dental disorders, performs oral surgeries, orthodontics, root canals, and '
                                'cosmetic dentofacial reconstruction.',
        'position_title': 'Dental Surgeon / Oral & Maxillofacial Specialist (BDS)',
        'qualification_badge': '12th PCB',
        'qualification_stage': 'after_12th',
        'recruiting_organizations': [   'Tamil Nadu Govt Dental College Chennai',
                                        'Private Dental Clinics',
                                        'Clove Dental',
                                        'Armed Forces Dental Corps',
                                        'Research Institutes'],
        'relevant_entrance_exams': [   {   'conducting_body': 'National Testing Agency (NTA)',
                                           'exam_category': 'National Medical & Dental Entrance Exam',
                                           'exam_date': 'First Sunday of May',
                                           'exam_name': 'NEET-UG',
                                           'exam_pattern': '720 Marks: Biology 360, Physics 180, Chemistry 180',
                                           'how_to_prepare': 'Strong fundamentals in NCERT Human Physiology and '
                                                             'Genetics.',
                                           'official_portal': 'https://neet.nta.nic.in',
                                           'registration_window': 'February - March',
                                           'selection_stages': 'Written Examination (720 Marks) -> DME Counselling for '
                                                               'Government Dental College Chennai & 20+ Self-Financing '
                                                               'Dental Colleges'},
                                       {   'conducting_body': 'Directorate of Medical Education, Chennai',
                                           'exam_category': 'State Single-Window Dental Admissions',
                                           'exam_date': 'Counselling in July - August',
                                           'exam_name': 'Tamil Nadu DME Dental Counselling',
                                           'exam_pattern': 'State NEET Rank Cutoff',
                                           'how_to_prepare': 'Apply on tnmedicalselection.net immediately after NEET '
                                                             'results.',
                                           'official_portal': 'https://www.tnmedicalselection.net',
                                           'registration_window': 'July (Post-NEET Results)',
                                           'selection_stages': 'NEET State Rank -> Online Choice Filling -> Seat '
                                                               'Allotment -> Certificate Verification'}],
        'salary_range': '₹35,000 - ₹75,000 / month (Govt/Clinic) -> ₹1 - ₹3 Lakhs / month (Private Practice)',
        'sector': 'Medical & Healthcare'},
    {   'future_career_growth': [   'Staff Nurse -> Nursing Sister -> Assistant Nursing Superintendent -> Chief '
                                    'Nursing Officer (CNO) / Global Nursing Specialist'],
        'government_perks_quotas': 'High international mobility; permanent state government pension & health insurance '
                                   'under TN MRB.',
        'id': 'pos_registered_nurse',
        'position_description': 'Provides clinical nursing care, ICU patient monitoring, post-operative '
                                'rehabilitation, and medication delivery in premier hospitals in India and abroad (UK, '
                                'Germany, Middle East).',
        'position_title': 'Registered Staff Nurse / Nursing Officer (B.Sc Nursing)',
        'qualification_badge': '12th PCB / Science',
        'qualification_stage': 'after_12th',
        'recruiting_organizations': [   'TN MRB (Medical Services Recruitment Board)',
                                        'Govt General Hospitals (GH)',
                                        'AIIMS',
                                        'Apollo Hospitals',
                                        'NHS UK',
                                        'Fortis Healthcare'],
        'relevant_entrance_exams': [   {   'conducting_body': 'Selection Committee, DME Tamil Nadu',
                                           'exam_category': 'State Single-Window Merit Admissions',
                                           'exam_date': 'No Entrance Exam (Merit Cutoff based on 12th Marks)',
                                           'exam_name': 'Tamil Nadu Paramedical / B.Sc Nursing Single-Window '
                                                        'Counselling',
                                           'exam_pattern': 'Cutoff calculated from Biology (100) + Physics (50) + '
                                                           'Chemistry (50) = 200 Marks',
                                           'how_to_prepare': 'Aim for 170+ / 200 in 12th PCB cutoff.',
                                           'official_portal': 'https://www.tnmedicalselection.net',
                                           'registration_window': 'May - June (Post-12th Results)',
                                           'selection_stages': 'Online application based on 12th PCB marks -> Merit '
                                                               'Cutoff (out of 200) -> Counselling for Madras Medical '
                                                               'College, Stanley, MMC Vellore'},
                                       {   'conducting_body': 'Medical Services Recruitment Board (MRB) Tamil Nadu',
                                           'exam_category': 'Tamil Nadu State Govt Permanent Job Exam',
                                           'exam_date': 'Scheduled via MRB Calendar',
                                           'exam_name': 'TN MRB Staff Nurse Recruitment Examination',
                                           'exam_pattern': '100 Objective Questions on Nursing Foundations, Anatomy, '
                                                           'Pharmacology, Community Health',
                                           'how_to_prepare': 'Revise 4-year B.Sc Nursing degree syllabus.',
                                           'official_portal': 'https://www.mrb.tn.gov.in',
                                           'registration_window': 'As per MRB notification',
                                           'selection_stages': 'Computer Based Test (100 Marks) -> Document '
                                                               'Verification -> Appointment as Staff Nurse in TN '
                                                               'Public Health Department'}],
        'salary_range': '₹25,000 - ₹55,000 / month (India) -> ₹2.5 - ₹4.5 Lakhs / month (NHS UK / Germany / Gulf)',
        'sector': 'Medical & Healthcare'},
    {   'future_career_growth': [   'Pharmacist -> Drug Inspector -> Senior Drug Inspector -> Assistant Drugs '
                                    'Controller -> Director of Drugs Control'],
        'government_perks_quotas': 'Enormous private industrial pharma sector in Chennai & Puducherry; regulatory '
                                   'authority and gazetted status as Drug Inspector.',
        'id': 'pos_pharmacist_drug_inspector',
        'position_description': 'Formulates medicines, inspects pharmaceutical manufacturing units, dispenses clinical '
                                'therapies, and regulates drug quality standards across the healthcare supply chain.',
        'position_title': 'Clinical Pharmacist / Drug Inspector (B.Pharm)',
        'qualification_badge': '12th PCB / PCM',
        'qualification_stage': 'after_12th',
        'recruiting_organizations': [   'Tamil Nadu Drugs Control Administration',
                                        'TN MRB',
                                        'Sun Pharma',
                                        "Dr. Reddy's",
                                        'Cipla',
                                        'Apex Laboratories Chennai'],
        'relevant_entrance_exams': [   {   'conducting_body': 'Selection Committee, DME Tamil Nadu',
                                           'exam_category': 'State Single-Window Merit Admissions',
                                           'exam_date': 'No Entrance Exam (12th Board Merit Cutoff)',
                                           'exam_name': 'Tamil Nadu Paramedical B.Pharm Single-Window Counselling',
                                           'exam_pattern': 'Marks in Physics, Chemistry, and Biology/Maths',
                                           'how_to_prepare': 'Score high in 12th science board subjects.',
                                           'official_portal': 'https://www.tnmedicalselection.net',
                                           'registration_window': 'May - June',
                                           'selection_stages': '12th PCB/PCM Marks -> DME Cutoff Rank List -> Choice '
                                                               'filling for Madras Medical College & Madurai Medical '
                                                               'College Pharmacy departments'},
                                       {   'conducting_body': 'TNPSC / Medical Services Recruitment Board',
                                           'exam_category': 'Tamil Nadu State Gazetted Regulatory Exam',
                                           'exam_date': 'Scheduled via planner',
                                           'exam_name': 'TNPSC / TN MRB Drug Inspector Examination',
                                           'exam_pattern': 'Paper 1 (Pharmacy 200 Qs / 300 Marks) + Paper 2 (General '
                                                           'Studies & Tamil 100 Qs / 150 Marks)',
                                           'how_to_prepare': 'Master pharmacology, pharmaceutics, drug jurisprudence, '
                                                             'and pharmacognosy.',
                                           'official_portal': 'https://www.tnpsc.gov.in',
                                           'registration_window': 'Periodic State Gazetted Notification',
                                           'selection_stages': 'Written Examination (Paper 1 Pharmacy Subject + Paper '
                                                               '2 General Studies) -> Oral Interview -> Appointment as '
                                                               'Drug Inspector'}],
        'salary_range': '₹30,000 - ₹65,000 / month (or ₹37,700 - ₹1,19,500 Level 18 for Drug Inspector)',
        'sector': 'Medical & Healthcare'},
    {   'future_career_growth': [   'Veterinary Assistant Surgeon (VAS) -> Assistant Director of Animal Husbandry -> '
                                    'Joint Director -> Director of Animal Husbandry'],
        'government_perks_quotas': 'Gazetted Officer Grade, 7.5% Govt School Free Quota, official quarters, NPA '
                                   'allowance, and prestigious status.',
        'id': 'pos_veterinary_surgeon',
        'position_description': 'Provides clinical medical treatment, surgery, disease prevention, and reproductive '
                                'management for livestock, pets, poultry, and wildlife reserves.',
        'position_title': 'Veterinary Surgeon / Animal Husbandry Officer (B.V.Sc & AH)',
        'qualification_badge': '12th PCB (Cutoff out of 200)',
        'qualification_stage': 'after_12th',
        'recruiting_organizations': [   'Tamil Nadu Animal Husbandry Department',
                                        'Aavin (Tamil Nadu Co-operative Milk)',
                                        'TANUVAS Research Centres',
                                        'Wildlife Sanctuaries (Mudumalai, Anamalai)',
                                        'Pet Care Multispecialities'],
        'relevant_entrance_exams': [   {   'conducting_body': 'Tamil Nadu Veterinary and Animal Sciences University '
                                                              '(TANUVAS), Chennai',
                                           'exam_category': 'State Single-Window Merit Admissions',
                                           'exam_date': 'No Entrance Exam (Cutoff Merit out of 200)',
                                           'exam_name': 'TANUVAS Undergraduate Single-Window Admissions',
                                           'exam_pattern': 'Cutoff formula: Biology (100) + Physics (50) + Chemistry '
                                                           '(50) = 200 Marks',
                                           'how_to_prepare': 'Aim for 195+ / 200 in 12th PCB cutoff.',
                                           'official_portal': 'https://tanuvas.ac.in',
                                           'registration_window': 'June - July',
                                           'selection_stages': '12th Board PCB Cutoff (out of 200) -> Merit rank list '
                                                               '-> Single-window counselling for Madras Veterinary '
                                                               'College (MVC), VC&RI Namakkal, Tirunelveli, '
                                                               'Orathanadu, Salem'},
                                       {   'conducting_body': 'Tamil Nadu Public Service Commission (TNPSC)',
                                           'exam_category': 'Tamil Nadu State Gazetted Technical Exam',
                                           'exam_date': 'Scheduled via planner',
                                           'exam_name': 'TNPSC Veterinary Assistant Surgeon (VAS) Examination',
                                           'exam_pattern': 'Paper 1 (Veterinary Science 200 Qs / 300 Marks) + Paper 2 '
                                                           '(General Studies 100 Qs / 150 Marks)',
                                           'how_to_prepare': 'Revise 5.5-year B.V.Sc curriculum.',
                                           'official_portal': 'https://www.tnpsc.gov.in',
                                           'registration_window': 'As per TNPSC annual planner',
                                           'selection_stages': 'Written Examination (Paper 1 Veterinary Science + '
                                                               'Paper 2 Tamil Eligibility & GS) -> Oral Test '
                                                               '(Interview) -> Gazetted Appointment'}],
        'salary_range': '₹56,100 - ₹1,77,500 / month (Level 22 Gazetted Officer) + Non-Practicing Allowance (NPA)',
        'sector': 'Agriculture & Veterinary'},
    {   'future_career_growth': [   'Agricultural Officer (AO) -> Assistant Director of Agriculture (ADA) -> Joint '
                                    'Director of Agriculture (JDA) -> Director of Agriculture'],
        'government_perks_quotas': 'Direct village administration influence; 7.5% Govt School reservation with 100% '
                                   'Free Tuition; high demand in banking as Agri Field Officer (AFO).',
        'id': 'pos_agricultural_officer',
        'position_description': 'Guides rural farmers on crop yield maximization, sustainable organic farming, soil '
                                'diagnostics, fertilizer technologies, and executes state welfare schemes across Tamil '
                                'Nadu blocks.',
        'position_title': 'Agricultural Officer (AO) / Farm Scientist (B.Sc Agri)',
        'qualification_badge': '12th PCB / PCM (Cutoff out of 200)',
        'qualification_stage': 'after_12th',
        'recruiting_organizations': [   'Tamil Nadu Department of Agriculture',
                                        'TNAU Research Stations',
                                        'National Seeds Corporation',
                                        'NABARD',
                                        'ITC Agri Business',
                                        'Bayer Crop Science'],
        'relevant_entrance_exams': [   {   'conducting_body': 'Tamil Nadu Agricultural University (TNAU), Coimbatore',
                                           'exam_category': 'State Single-Window Merit Admissions',
                                           'exam_date': 'No Entrance Exam (Cutoff Merit out of 200)',
                                           'exam_name': 'TNAU Undergraduate Single-Window Admissions',
                                           'exam_pattern': 'Cutoff derived from Physics, Chemistry, Biology / Maths',
                                           'how_to_prepare': 'Maintain high marks in 12th standard science stream.',
                                           'official_portal': 'https://tnau.ac.in',
                                           'registration_window': 'May - June (Post-12th Results)',
                                           'selection_stages': '12th Marks Online Application -> TNAU Merit Cutoff '
                                                               'Rank -> Online Choice Filling for Coimbatore Main, '
                                                               'Madurai, Trichy, Killikulam constituent colleges'},
                                       {   'conducting_body': 'Tamil Nadu Public Service Commission (TNPSC)',
                                           'exam_category': 'Tamil Nadu State Gazetted Technical Exam',
                                           'exam_date': 'Scheduled via planner',
                                           'exam_name': 'TNPSC Agricultural Officer (AO) Examination',
                                           'exam_pattern': 'Paper 1 (Agriculture Degree Level 200 Qs / 300 Marks) + '
                                                           'Paper 2 (General Studies 100 Qs / 150 Marks)',
                                           'how_to_prepare': 'Master agronomy, genetics, plant pathology, agricultural '
                                                             'economics, and soil science.',
                                           'official_portal': 'https://www.tnpsc.gov.in',
                                           'registration_window': 'As per TNPSC Annual Calendar',
                                           'selection_stages': 'Written Examination (Paper 1 Agriculture + Paper 2 '
                                                               'Tamil & GS) -> Certificate Verification -> Direct '
                                                               'Appointment as Agricultural Officer'}],
        'salary_range': '₹37,700 - ₹1,19,500 / month (Level 18 TN Govt) or ₹4.5 - ₹10 LPA (Agri-tech / Seeds)',
        'sector': 'Agriculture & Veterinary'},
    {   'future_career_growth': [   'Village Administrative Officer (VAO) -> Revenue Inspector (RI - after 6 years) -> '
                                    'Deputy Tahsildar -> Tahsildar (Taluk Magistrate) -> Revenue Divisional Officer '
                                    '(RDO) -> District Revenue Officer (DRO)'],
        'government_perks_quotas': 'Direct permanent Tamil Nadu government job immediately after 10th standard; '
                                   'permanent pension scheme, medical benefits, and enormous social respect.',
        'id': 'pos_village_administrative_officer',
        'position_description': 'Administrative head of the revenue village in Tamil Nadu. Issues community, income, '
                                'and nativity certificates; maintains land patta records; supervises local peace and '
                                'revenue collection.',
        'position_title': 'Village Administrative Officer (VAO)',
        'qualification_badge': 'Direct 10th (SSLC Pass)',
        'qualification_stage': 'after_10th',
        'recruiting_organizations': [   'Tamil Nadu Revenue & Disaster Management Department (Direct Government '
                                        'Posting in Home District)'],
        'relevant_entrance_exams': [   {   'conducting_body': 'Tamil Nadu Public Service Commission (TNPSC), Chennai',
                                           'exam_category': 'State Competitive Written Examination',
                                           'exam_date': 'June 2027',
                                           'exam_name': 'TNPSC Group 4 & VAO Examination',
                                           'exam_pattern': 'Part A: General Tamil (SSLC Standard - 100 Qs / 150 Marks) '
                                                           '+ Part B: General Studies (75 Qs) & Aptitude/Mental '
                                                           'Ability (25 Qs) = 150 Marks. Total 300 Marks. Duration: 3 '
                                                           'Hours.',
                                           'how_to_prepare': 'Master Tamil Nadu Samacheer Kalvi 6th to 10th standard '
                                                             'Tamil textbooks, Science, Social Science, and basic '
                                                             'school mathematics.',
                                           'official_portal': 'https://www.tnpsc.gov.in',
                                           'registration_window': 'January - February 2027',
                                           'selection_stages': 'Single-Stage Written Examination (300 Marks, 200 '
                                                               'Questions) -> State Merit & Communal Rank List -> '
                                                               'District-wise Certificate Verification -> Permanent '
                                                               'Govt Appointment'}],
        'salary_range': '₹19,500 - ₹62,000 / month (Level 8 TN Govt Pay Scale) + DA, HRA, Medical & Travel Perks',
        'sector': 'Tamil Nadu Government & Administration'},
    {   'future_career_growth': [   'Junior Assistant -> Assistant -> Superintendent -> Section Officer -> Under '
                                    'Secretary to Government (Secretariat)'],
        'government_perks_quotas': 'Job security till age 60; fixed 5-day week in Secretariat/offices; compassionate '
                                   'appointment privileges.',
        'id': 'pos_junior_assistant_typist',
        'position_description': 'Executes clerical, administrative documentation, official correspondence, and public '
                                'welfare program records across Tamil Nadu Secretariat, Collectorates, Municipalities, '
                                'and Courts.',
        'position_title': 'Junior Assistant / Typist / Bill Collector (TN Govt)',
        'qualification_badge': 'Direct 10th (SSLC Pass)',
        'qualification_stage': 'after_10th',
        'recruiting_organizations': [   'Tamil Nadu Secretariat',
                                        'District Collectorates (All 38 Districts)',
                                        'Judicial Courts',
                                        'Commercial Taxes Department',
                                        'Registration Department'],
        'relevant_entrance_exams': [   {   'conducting_body': 'Tamil Nadu Public Service Commission (TNPSC)',
                                           'exam_category': 'State Competitive Written Examination',
                                           'exam_date': 'June',
                                           'exam_name': 'TNPSC Group 4 Examination',
                                           'exam_pattern': 'General Tamil (100 Qs) + General Studies & Mental Ability '
                                                           '(100 Qs). No Interview.',
                                           'how_to_prepare': 'Practice TN Samacheer Kalvi school textbooks and '
                                                             'previous 10 years TNPSC question papers.',
                                           'official_portal': 'https://www.tnpsc.gov.in',
                                           'registration_window': 'January - February',
                                           'selection_stages': 'Single Written Exam (200 Questions / 300 Marks). For '
                                                               'typists: Technical qualification in Tamil & English '
                                                               'Typewriting.'}],
        'salary_range': '₹19,500 - ₹62,000 / month (Level 8 TN Govt Pay Matrix)',
        'sector': 'Tamil Nadu Government & Administration'},
    {   'future_career_growth': [   'Sub-Registrar Grade II -> Sub-Registrar Grade I -> District Registrar -> Deputy '
                                    'Inspector General of Registration (DIG)'],
        'government_perks_quotas': 'Executive authority, official government seals, gazetted promotion avenues, and '
                                   'housing loan privileges.',
        'id': 'pos_sub_registrar_revenue_inspector',
        'position_description': 'Executes land and property registrations, conducts revenue inquiries, oversees '
                                'municipal civic administration, and enforces commercial taxation across towns and '
                                'districts.',
        'position_title': 'Sub-Registrar / Revenue Inspector / Municipal Commissioner',
        'qualification_badge': "Any Bachelor's Degree (Direct After 12th Graduation)",
        'qualification_stage': 'diploma_graduate',
        'recruiting_organizations': [   'Registration Department',
                                        'Revenue Administration',
                                        'Municipal Administration',
                                        'Commercial Taxes',
                                        'Labour Department'],
        'relevant_entrance_exams': [   {   'conducting_body': 'Tamil Nadu Public Service Commission (TNPSC)',
                                           'exam_category': 'State Multi-Stage Civil Services Exam',
                                           'exam_date': 'Scheduled via TNPSC Calendar',
                                           'exam_name': 'TNPSC Group 2 & 2A Combined Civil Services Examination',
                                           'exam_pattern': 'Prelims: General Tamil (100 Qs) + General Studies (75 Qs) '
                                                           '+ Aptitude (25 Qs). Mains: Descriptive paper on TN '
                                                           'socio-economic development, administration, and '
                                                           'science/technology.',
                                           'how_to_prepare': 'In-depth study of Tamil Nadu history, administrative '
                                                             'machinery, economy, and descriptive writing practice.',
                                           'official_portal': 'https://www.tnpsc.gov.in',
                                           'registration_window': 'As per TNPSC Planner',
                                           'selection_stages': 'Prelims Exam (Objective 300 Marks) -> Mains Written '
                                                               'Exam (Descriptive 300 Marks) -> Interview (for Group 2 '
                                                               'Interview Posts) / Merit Counselling (for Group 2A '
                                                               'Non-Interview)'}],
        'salary_range': '₹36,900 - ₹1,16,600 / month (Level 18/16 TN Govt Pay Matrix)',
        'sector': 'Tamil Nadu Government & Administration'},
    {   'future_career_growth': [   'Deputy Collector -> District Revenue Officer (DRO) -> Conferred IAS (District '
                                    'Collector -> Principal Secretary to Govt)'],
        'government_perks_quotas': 'Executive bungalow, official vehicle with beacon, armed security, VIP protocol, '
                                   'and gateway to IAS.',
        'id': 'pos_deputy_collector_dsp',
        'position_description': 'Highest state civil service position. Heads revenue divisions, maintains district law '
                                'and order, coordinates disaster relief, and eligible for promotion to Indian '
                                'Administrative Service (IAS) and Indian Police Service (IPS).',
        'position_title': 'Deputy Collector / DSP (District Superintendent of Police)',
        'qualification_badge': "Any Bachelor's Degree",
        'qualification_stage': 'diploma_graduate',
        'recruiting_organizations': ['Government of Tamil Nadu (Revenue, Police, Commercial Taxes, Rural Development)'],
        'relevant_entrance_exams': [   {   'conducting_body': 'Tamil Nadu Public Service Commission (TNPSC)',
                                           'exam_category': 'Premier State Civil Services Examination',
                                           'exam_date': 'Prelims in July | Mains in December',
                                           'exam_name': 'TNPSC Group 1 Examination',
                                           'exam_pattern': 'Prelims: 200 Questions (General Studies 175 + Aptitude '
                                                           '25). Mains: Paper 1 (Modern India & TN Culture), Paper 2 '
                                                           '(Indian Polity & Emerging Social Issues), Paper 3 '
                                                           '(Economy, Geography, Environment).',
                                           'how_to_prepare': 'Extensive reading of Indian Constitution, Tamil society '
                                                             'and literature, current affairs, and answer writing.',
                                           'official_portal': 'https://www.tnpsc.gov.in',
                                           'registration_window': 'Annual Notification',
                                           'selection_stages': 'Stage 1: Preliminary Exam (300 Marks) -> Stage 2: Main '
                                                               'Written Exam (3 Descriptive Papers = 750 Marks) -> '
                                                               'Stage 3: Oral Interview (100 Marks)'}],
        'salary_range': '₹56,100 - ₹1,77,500 / month (Level 22 Premier Gazetted Pay Scale) + Executive Perks',
        'sector': 'Tamil Nadu Government & Administration'},
    {   'future_career_growth': [   'Grade II Police Constable -> Grade I Constable (after 5 yrs) -> Head Constable -> '
                                    'Sub-Inspector of Police (via departmental exam)'],
        'government_perks_quotas': 'Free uniform, subsidized police canteen, family health insurance, quarters in '
                                   'police colony, and 20% departmental quota for Sub-Inspector.',
        'id': 'pos_police_constable_fireman',
        'position_description': 'Maintains public safety, conducts foot and vehicle patrols, law and order '
                                'enforcement, crime investigation assistance, and firefighting rescue across Tamil '
                                'Nadu.',
        'position_title': 'Grade II Police Constable / Jail Warder / Fireman',
        'qualification_badge': 'Direct 10th (SSLC Pass)',
        'qualification_stage': 'after_10th',
        'recruiting_organizations': [   'Tamil Nadu Police Department (Armed Reserve, Taluk, Tamil Nadu Special '
                                        'Police)',
                                        'Prison Department',
                                        'Fire and Rescue Services'],
        'relevant_entrance_exams': [   {   'conducting_body': 'Tamil Nadu Uniformed Services Recruitment Board '
                                                              '(TNUSRB), Chennai',
                                           'exam_category': 'State Uniformed Services Examination',
                                           'exam_date': 'December 2027',
                                           'exam_name': 'TNUSRB Common Recruitment (Grade II PC & Fireman)',
                                           'exam_pattern': 'Written Exam: 70 Marks (General Knowledge 45 Marks + '
                                                           'Psychology / Reasoning 25 Marks). Qualifying Tamil Test: '
                                                           '80 Marks (Min 40% required). Physical Test: 24 Marks.',
                                           'how_to_prepare': 'Master 6th to 10th Samacheer Kalvi GK, mental ability '
                                                             'puzzles, and daily physical fitness running.',
                                           'official_portal': 'https://www.tnusrb.tn.gov.in',
                                           'registration_window': 'August - September 2027',
                                           'selection_stages': 'Stage 1: Written Examination (Part 1 Tamil Eligibility '
                                                               '80 Marks + Part 2 Main Exam 70 Marks) -> Stage 2: '
                                                               'Physical Measurement Test (PMT) & Endurance Test (ET) '
                                                               '-> Stage 3: Physical Efficiency Test (PET - Running, '
                                                               'Rope Climbing, Long Jump) -> Medical & Police '
                                                               'Verification'}],
        'salary_range': '₹18,200 - ₹57,900 / month (Level 7 TN Govt Pay Scale) + Ration Allowance, Uniform & Risk '
                        'Allowances',
        'sector': 'Police & Defence Services'},
    {   'future_career_growth': [   'Sub-Inspector (SI) -> Inspector of Police (after 8-10 yrs) -> Deputy '
                                    'Superintendent of Police (DSP) -> Additional SP -> Superintendent of Police '
                                    '(IPS)'],
        'government_perks_quotas': 'Authorised service weapon, official jeep/motorcycle, station commander authority, '
                                   'and rapid departmental promotions.',
        'id': 'pos_sub_inspector_police',
        'position_description': 'Station House Officer (SHO) commanding a police station jurisdiction. Investigates '
                                'IPC crimes, registers FIRs, leads tactical operations, and maintains law and order.',
        'position_title': 'Sub-Inspector of Police (Taluk, Armed Reserve, TSP)',
        'qualification_badge': "Any Bachelor's Degree",
        'qualification_stage': 'diploma_graduate',
        'recruiting_organizations': ['Tamil Nadu Police Department (Law & Order, Crime, Traffic, CBCID, Cyber Crime)'],
        'relevant_entrance_exams': [   {   'conducting_body': 'Tamil Nadu Uniformed Services Recruitment Board '
                                                              '(TNUSRB)',
                                           'exam_category': 'State Uniformed Officer Recruitment',
                                           'exam_date': 'Scheduled via TNUSRB Calendar',
                                           'exam_name': 'TNUSRB Police Sub-Inspector (SI) Examination',
                                           'exam_pattern': 'General Knowledge (40 Marks) + Logical Analysis, Numerical '
                                                           '& Communication Skills (30 Marks)',
                                           'how_to_prepare': 'Master Indian Penal Code basics, current events, mental '
                                                             'reasoning, and maintain 1500m/400m running times.',
                                           'official_portal': 'https://www.tnusrb.tn.gov.in',
                                           'registration_window': 'Periodic Notification',
                                           'selection_stages': 'Part 1 Tamil Eligibility Test -> Part 2 Written '
                                                               'Examination (70 Marks Open / 85 Marks Dept) -> PMT & '
                                                               'ET -> PET (15 Marks) -> Viva-Voce Interview (10 '
                                                               'Marks)'}],
        'salary_range': '₹36,900 - ₹1,16,600 / month (Level 18 TN Govt Pay Matrix)',
        'sector': 'Police & Defence Services'},
    {   'future_career_growth': [   'Lieutenant / Flying Officer -> Captain / Flight Lieutenant -> Major / Squadron '
                                    'Leader -> Lt Colonel / Wing Commander -> Colonel -> Brigadier -> Major General -> '
                                    'General'],
        'government_perks_quotas': "Direct President's Commission, free military housing, defense health coverage "
                                   '(ECHS), CSD canteen, sports facilities, and pension.',
        'id': 'pos_defence_commissioned_officer',
        'position_description': 'Commands military platoons, fighter jets, naval warships, and special forces units in '
                                'defence of the nation. Direct entry as Commissioned Lieutenant / Flying Officer / '
                                'Sub-Lieutenant.',
        'position_title': 'Defence Commissioned Officer (Army, Navy, Air Force Lieutenant)',
        'qualification_badge': '12th Any (Army) / 12th PCM (Navy & Air Force)',
        'qualification_stage': 'after_12th',
        'recruiting_organizations': ['Indian Army', 'Indian Navy', 'Indian Air Force'],
        'relevant_entrance_exams': [   {   'conducting_body': 'Union Public Service Commission (UPSC)',
                                           'exam_category': 'National Defence Commissioned Officer Exam',
                                           'exam_date': 'NDA I: April | NDA II: September',
                                           'exam_name': 'UPSC NDA & NA Examination',
                                           'exam_pattern': 'Paper 1: Mathematics (300 Marks, 120 Qs, 2.5 Hrs) + Paper '
                                                           '2: General Ability Test (600 Marks: English 200 + GK 400, '
                                                           '150 Qs, 2.5 Hrs).',
                                           'how_to_prepare': 'Thorough command over 11th & 12th algebra, trigonometry, '
                                                             'calculus, English grammar, and daily newspapers for '
                                                             'current defence affairs.',
                                           'official_portal': 'https://www.upsc.gov.in',
                                           'registration_window': 'NDA I: Dec - Jan | NDA II: May - June',
                                           'selection_stages': 'Written Examination (900 Marks) -> 5-Day Services '
                                                               'Selection Board (SSB) Interview (Psychology, GTO, '
                                                               'Personal Interview - 900 Marks) -> Special Medical '
                                                               'Board -> 3-Year Tri-Services Cadet Training at NDA '
                                                               'Khadakwasla, Pune'}],
        'salary_range': '₹56,100 - ₹1,77,500 / month (Level 10 Defence Pay Scale) + Military Service Pay (MSP ₹15,500) '
                        '+ Flying/High Altitude Allowances',
        'sector': 'Police & Defence Services'},
    {   'future_career_growth': [   'Sub-Lieutenant -> Lieutenant -> Lieutenant Commander -> Commander -> Captain -> '
                                    'Commodore -> Rear Admiral -> Vice Admiral'],
        'government_perks_quotas': 'World travel, 100% free B.Tech education from Jawaharlal Nehru University (JNU), '
                                   'and officer lifestyle.',
        'id': 'pos_naval_executive_btech',
        'position_description': 'Executes surface combat operations, naval engineering propulsion, weapons systems, '
                                'and navigation on destroyers, frigates, and aircraft carriers.',
        'position_title': 'Naval Executive / Technical Officer (10+2 B.Tech Entry)',
        'qualification_badge': '12th PCM with min 70% aggregate',
        'qualification_stage': 'after_12th',
        'recruiting_organizations': ['Indian Navy (Permanent Commission / Short Service Commission)'],
        'relevant_entrance_exams': [   {   'conducting_body': 'Indian Navy (joinindiannavy.gov.in)',
                                           'exam_category': 'Direct SSB Shortlisting via JEE Main',
                                           'exam_date': 'No separate written exam (Directly based on JEE Main Rank)',
                                           'exam_name': 'Indian Navy 10+2 B.Tech Cadet Entry Scheme',
                                           'exam_pattern': 'Valid JEE Main NTA Score in Paper 1',
                                           'how_to_prepare': 'Prepare for JEE Main and cultivate officer-like '
                                                             'qualities (OLQs) for SSB.',
                                           'official_portal': 'https://www.joinindiannavy.gov.in',
                                           'registration_window': 'Twice a year (June & December)',
                                           'selection_stages': 'Shortlisting based on All India Common Rank List (CRL) '
                                                               'in JEE Main -> 5-Day SSB Interview (Bangalore / Bhopal '
                                                               '/ Visakhapatnam) -> Medical Board -> 4-Year B.Tech '
                                                               'Degree at Indian Naval Academy (INA) Ezhimala (100% '
                                                               'Free funded by Govt)'}],
        'salary_range': '₹56,100 - ₹1,77,500 / month + MSP + Sea Duty Allowances',
        'sector': 'Police & Defence Services'},
    {   'future_career_growth': [   'Advocate -> Senior Advocate (High Court) -> Legal Advisor -> Corporate Partner / '
                                    'Elevation as High Court Judge'],
        'government_perks_quotas': 'Enormous societal authority; eligible for direct recruitment as Assistant Public '
                                   'Prosecutor (APP) and Civil Judge.',
        'id': 'pos_advocate_legal_advisor',
        'position_description': 'Argues cases before Madras High Court, District Courts, and Supreme Court; drafts '
                                'commercial contracts, patent filings, and defends human rights.',
        'position_title': 'Advocate / Corporate Legal Counsel / High Court Practitioner',
        'qualification_badge': '12th Any Stream (Min 70% for SOEL)',
        'qualification_stage': 'after_12th',
        'recruiting_organizations': [   'Madras High Court Bar',
                                        'Top Corporate Law Firms (Shardul Amarchand, AZB & Partners, Trilegal)',
                                        'Banks',
                                        'Multinational Corporations'],
        'relevant_entrance_exams': [   {   'conducting_body': 'The Tamil Nadu Dr. Ambedkar Law University (TNDALU), '
                                                              'Chennai',
                                           'exam_category': 'State Single-Window Merit Admissions',
                                           'exam_date': 'No Entrance Exam (Cutoff Merit based on 12th Aggregate)',
                                           'exam_name': 'TNDALU 5-Year Integrated Honours Law Admissions',
                                           'exam_pattern': 'Merit calculated from 12th standard four major subjects '
                                                           '(excluding languages)',
                                           'how_to_prepare': 'Score 85%+ in 12th standard board exams. 7.5% Govt '
                                                             'School reservation applies.',
                                           'official_portal': 'https://www.tndalu.ac.in',
                                           'registration_window': 'May - June (Post-12th Results)',
                                           'selection_stages': 'Online application based on 12th aggregate marks -> '
                                                               'Merit Cutoff Rank -> Counselling for School of '
                                                               'Excellence in Law (SOEL, Perungudi, Chennai) & 14 Govt '
                                                               'Law Colleges'},
                                       {   'conducting_body': 'Consortium of National Law Universities (NLUs)',
                                           'exam_category': 'National Law Entrance Exam',
                                           'exam_date': 'First Sunday of December',
                                           'exam_name': 'CLAT (Common Law Admission Test)',
                                           'exam_pattern': '120 MCQs / 120 Marks: Reading Comprehension (English), '
                                                           'Current Affairs & GK, Legal Reasoning, Logical Reasoning, '
                                                           'and Quantitative Techniques.',
                                           'how_to_prepare': 'Daily editorial reading (The Hindu), legal principles, '
                                                             'and critical reasoning drills.',
                                           'official_portal': 'https://consortiumofnlus.ac.in',
                                           'registration_window': 'July - November',
                                           'selection_stages': 'Pen-and-paper Written Examination (120 Questions) -> '
                                                               'National Centralized Seat Allotment for Tamil Nadu '
                                                               'National Law University (TNNLU Trichy - 50% TN Home '
                                                               'State Quota)'}],
        'salary_range': '₹35,000 - ₹90,000 / month (Junior Counsel) -> ₹8 - ₹25+ LPA (Corporate Law Firm Associate)',
        'sector': 'Law & Judiciary'},
    {   'future_career_growth': [   'Civil Judge / Judicial Magistrate -> Senior Civil Judge / Chief Judicial '
                                    'Magistrate (CJM) -> District & Sessions Judge -> Elevation to High Court Judge'],
        'government_perks_quotas': 'Constitutional judicial status, official court staff, security, car, bungalow, and '
                                   'supreme independence.',
        'id': 'pos_civil_judge_magistrate',
        'position_description': 'Presides over court trials, adjudicates civil and criminal disputes, delivers '
                                'judicial judgments, and exercises state magistracy powers.',
        'position_title': 'Civil Judge / Judicial Magistrate (TN State Judicial Service)',
        'qualification_badge': 'LL.B Degree + Bar Council Enrollment',
        'qualification_stage': 'diploma_graduate',
        'recruiting_organizations': ['Madras High Court Registry & Tamil Nadu Judicial Service'],
        'relevant_entrance_exams': [   {   'conducting_body': 'Tamil Nadu Public Service Commission & Madras High '
                                                              'Court',
                                           'exam_category': 'State Judicial Service Examination',
                                           'exam_date': 'Scheduled via planner',
                                           'exam_name': 'TNPSC Civil Judge Examination',
                                           'exam_pattern': 'Law Paper I (Civil Law), Law Paper II (Criminal Law), Law '
                                                           'Paper III (Judgement Writing), Translation Paper',
                                           'how_to_prepare': 'Master Code of Civil Procedure (CPC), Code of Criminal '
                                                             'Procedure (CrPC), Indian Evidence Act, and case laws.',
                                           'official_portal': 'https://www.tnpsc.gov.in',
                                           'registration_window': 'As per High Court / TNPSC notification',
                                           'selection_stages': 'Preliminary Examination (Objective 100 Marks) -> Main '
                                                               'Written Examination (4 Papers: Translation, Law I, Law '
                                                               'II, Law III - 400 Marks) -> Viva-Voce Interview (60 '
                                                               'Marks)'}],
        'salary_range': '₹77,840 - ₹1,36,520 / month (Junior Civil Judge) + Judicial Perks',
        'sector': 'Law & Judiciary'},
    {   'future_career_growth': [   'Chartered Accountant -> Audit Manager -> VP of Finance -> Chief Financial Officer '
                                    '(CFO) / Managing Partner'],
        'government_perks_quotas': 'Exclusive legal statutory authority to sign balance sheets and audit reports under '
                                   'Companies Act 2013.',
        'id': 'pos_chartered_accountant',
        'position_description': 'Statutory auditor, financial strategist, corporate taxation advisor, and CFO '
                                'controlling balance sheets, corporate mergers, and tax compliance.',
        'position_title': 'Chartered Accountant (CA) / Audit & Taxation Specialist',
        'qualification_badge': '12th Commerce / Any Stream',
        'qualification_stage': 'after_12th',
        'recruiting_organizations': [   'The Big 4 (Deloitte, PwC, EY, KPMG)',
                                        'BDO',
                                        'Grant Thornton',
                                        'Indian & Global Banks',
                                        'Self-Owned CA Firm'],
        'relevant_entrance_exams': [   {   'conducting_body': 'The Institute of Chartered Accountants of India (ICAI)',
                                           'exam_category': 'National Professional Qualification Entry',
                                           'exam_date': 'January, May, September',
                                           'exam_name': 'ICAI CA Foundation Examination',
                                           'exam_pattern': '4 Papers (400 Marks): Paper 1 Accounting (100), Paper 2 '
                                                           'Business Laws (100), Paper 3 Quantitative Aptitude '
                                                           '(Maths/Stats/LR - 100), Paper 4 Business Economics (100).',
                                           'how_to_prepare': 'Master 11th & 12th Accountancy, Business Studies, and '
                                                             'practice quantitative aptitude problems.',
                                           'official_portal': 'https://www.icai.org',
                                           'registration_window': 'Open year-round (Exams thrice a year in Jan, '
                                                                  'May/June, Sept)',
                                           'selection_stages': 'Registration post-10th/12th -> CA Foundation Written '
                                                               'Exam -> CA Intermediate (8 Papers) -> 2-Year '
                                                               'Articleship -> CA Final Examination -> Chartered '
                                                               'Accountant Membership'}],
        'salary_range': '₹8 - ₹24 LPA (Fresher CA) -> ₹40 - ₹80+ LPA (Partner / Director)',
        'sector': 'Banking, Finance & Commerce'},
    {   'future_career_growth': [   'Probationary Officer (Scale I) -> Branch Manager (Scale II) -> Chief Manager '
                                    '(Scale IV) -> Deputy General Manager (DGM) -> Executive Director -> Chairman / '
                                    'MD'],
        'government_perks_quotas': 'High job security, low-interest home & vehicle loans, LTC travel concessions, and '
                                   'guaranteed bi-partite wage revisions.',
        'id': 'pos_bank_probationary_officer',
        'position_description': 'Manages branch credit disbursement, corporate loans, foreign exchange, treasury '
                                'operations, and digital customer banking services.',
        'position_title': 'Bank Probationary Officer (PO) & Specialist Officer',
        'qualification_badge': "Any Bachelor's Degree",
        'qualification_stage': 'diploma_graduate',
        'recruiting_organizations': [   'State Bank of India (SBI)',
                                        'Canara Bank',
                                        'Indian Bank',
                                        'Indian Overseas Bank (IOB)',
                                        'Punjab National Bank',
                                        'Bank of Baroda'],
        'relevant_entrance_exams': [   {   'conducting_body': 'Institute of Banking Personnel Selection (IBPS) & SBI',
                                           'exam_category': 'National Public Sector Bank Officer Exam',
                                           'exam_date': 'Prelims: October | Mains: November',
                                           'exam_name': 'IBPS PO / SBI PO Examination',
                                           'exam_pattern': 'Speed and accuracy in Data Interpretation, Reasoning '
                                                           'Puzzles, Financial Awareness, and English comprehension.',
                                           'how_to_prepare': 'Daily speed math, reasoning mocks, and banking '
                                                             'awareness.',
                                           'official_portal': 'https://www.ibps.in',
                                           'registration_window': 'August - September',
                                           'selection_stages': 'Stage 1: Preliminary Exam (100 Marks: English 30, '
                                                               'Quant 35, Reasoning 35) -> Stage 2: Main Examination '
                                                               '(200 Marks Objective + 25 Marks Descriptive Essay) -> '
                                                               'Stage 3: Psychometric Test, Group Exercise & Personal '
                                                               'Interview'}],
        'salary_range': '₹52,000 - ₹75,000 / month (Grade 1 Officer) + Leased Accommodation & Concessional Loans',
        'sector': 'Banking, Finance & Commerce'},
    {   'future_career_growth': [   'Junior Architect -> Project Architect -> Associate Partner -> Principal Architect '
                                    '/ Urban Planner'],
        'government_perks_quotas': 'Council of Architecture (CoA) licensed professional status; direct eligibility for '
                                   'CMDA and government town planning consultancies.',
        'id': 'pos_architect_urban_planner',
        'position_description': 'Conceives architectural layouts, residential skyscrapers, sustainable green campuses, '
                                'airport terminals, and heritage restoration projects across urban centres.',
        'position_title': 'Architect / Urban Design Consultant (B.Arch)',
        'qualification_badge': '12th PCM with min 50% marks',
        'qualification_stage': 'after_12th',
        'recruiting_organizations': [   'School of Architecture and Planning (SAP Anna University)',
                                        'L&T Architecture',
                                        'Morphogenesis',
                                        'HOK',
                                        'CMDA (Chennai Metropolitan Development Authority)'],
        'relevant_entrance_exams': [   {   'conducting_body': 'Council of Architecture (CoA)',
                                           'exam_category': 'National Mandatory Architecture Aptitude Exam',
                                           'exam_date': 'Multiple dates from April to July',
                                           'exam_name': 'NATA (National Aptitude Test in Architecture)',
                                           'exam_pattern': '200 Marks: Visual Reasoning, Aesthetic Sensitivity, '
                                                           'Architectural Awareness, Mathematics, and Freehand 2D/3D '
                                                           'Drawing.',
                                           'how_to_prepare': 'Practice 2D/3D sketch rendering, perspective drawing, '
                                                             'light & shadow, and architectural history.',
                                           'official_portal': 'https://www.nata.in',
                                           'registration_window': 'March - July (Conducted across multiple weekend '
                                                                  'cycles)',
                                           'selection_stages': 'Computer Based + Drawing Aptitude Test (200 Marks) -> '
                                                               'Anna University B.Arch Single-Window Counselling'},
                                       {   'conducting_body': 'Anna University, Chennai',
                                           'exam_category': 'State Single-Window Architecture Seat Allotment',
                                           'exam_date': 'No separate exam (Rank based on 12th + NATA composite cutoff)',
                                           'exam_name': 'Anna University B.Arch Single-Window Counselling',
                                           'exam_pattern': 'Cutoff formula: (12th Board Marks / 2) + (NATA Score / 2) '
                                                           '= Out of 200',
                                           'how_to_prepare': 'Aim for 140+ in NATA and 90%+ in 12th PCM.',
                                           'official_portal': 'https://www.annauniv.edu',
                                           'registration_window': 'June - July',
                                           'selection_stages': 'Cutoff calculated: 50% weightage for 12th Board PCM + '
                                                               '50% weightage for NATA Score = Total 200 Marks -> '
                                                               'Counselling for SAP Guindy & Measi Academy of '
                                                               'Architecture'}],
        'salary_range': '₹4.5 - ₹12 LPA (Fresher) -> ₹20 - ₹50+ LPA (Consultant / Principal Architect)',
        'sector': 'Design & Architecture'},
    {   'future_career_growth': [   'Apparel Designer -> Senior Stylist -> Design Head -> Creative Director / '
                                    'Independent Fashion Label Owner'],
        'government_perks_quotas': "Direct linkage with Tamil Nadu's ₹40,000+ Crore textile & apparel export corridor; "
                                   'National Institute of Design (NID) & NIFT prestige.',
        'id': 'pos_fashion_designer_apparel',
        'position_description': 'Creates garment collections, luxury fashion lines, textile weaves, apparel graphics, '
                                'and coordinates retail styling for international fashion houses and Tiruppur knitwear '
                                'export clusters.',
        'position_title': 'Fashion & Apparel Designer / Textile Merchandiser (B.Des)',
        'qualification_badge': '12th Any Stream',
        'qualification_stage': 'after_12th',
        'recruiting_organizations': [   'NIFT Chennai',
                                        'Aditya Birla Fashion',
                                        'Raymond',
                                        'Myntra',
                                        'Zudio',
                                        'Tiruppur Export Consortium',
                                        'Celebrity Styling Studios'],
        'relevant_entrance_exams': [   {   'conducting_body': 'National Institute of Fashion Technology (NIFT) & NTA',
                                           'exam_category': 'National Premier Design Institute Exam',
                                           'exam_date': 'First week of February',
                                           'exam_name': 'NIFT Entrance Examination',
                                           'exam_pattern': 'CAT (Drawing & Visual Concepts 50%) + GAT (English, '
                                                           'Quantitative, GK 30%) + Situation Test (20%)',
                                           'how_to_prepare': 'Practice concept sketching, innovative design ideation, '
                                                             'and material crafting.',
                                           'official_portal': 'https://www.nift.ac.in',
                                           'registration_window': 'November - December',
                                           'selection_stages': 'Stage 1: Written Test (Creative Ability Test - CAT & '
                                                               'General Ability Test - GAT) -> Stage 2: Situation Test '
                                                               '(Hands-on Material Crafting) -> National Seat '
                                                               'Allotment for NIFT Chennai & 18 campuses'}],
        'salary_range': '₹4.2 - ₹10 LPA (Fresher) -> ₹18 - ₹45 LPA (Creative Director)',
        'sector': 'Design & Architecture'},
    {   'future_career_growth': [   'Junior First Officer -> Senior First Officer -> Captain (Commander) -> Designated '
                                    'Examiner (DE) / Chief Pilot'],
        'government_perks_quotas': 'High international prestige, global tax and travel privileges, and rapid captaincy '
                                   'transitions.',
        'id': 'pos_commercial_pilot',
        'position_description': 'Operates commercial passenger aircraft (Airbus A320, Boeing 737), executes flight '
                                'navigation, weather radar analysis, and cross-border aviation protocols.',
        'position_title': 'Commercial Airline Pilot / First Officer',
        'qualification_badge': '12th PCM with min 50% marks',
        'qualification_stage': 'after_12th',
        'recruiting_organizations': [   'IndiGo Airlines',
                                        'Air India',
                                        'Air India Express',
                                        'Akasa Air',
                                        'SpiceJet',
                                        'Global Cargo Fleets'],
        'relevant_entrance_exams': [   {   'conducting_body': 'Directorate General of Civil Aviation (DGCA), India',
                                           'exam_category': 'National Aviation Licensing Examinations',
                                           'exam_date': 'Quarterly Testing Cycles',
                                           'exam_name': 'DGCA Pilot Ground Examinations (CPL)',
                                           'exam_pattern': 'Computer Based Test with 70% passing criteria in each '
                                                           'subject',
                                           'how_to_prepare': 'Master 12th Physics (optics, mechanics, electronics), '
                                                             '12th Maths, and DGCA RK Bali aviation navigation '
                                                             'manuals.',
                                           'official_portal': 'https://pariksha.dgca.gov.in',
                                           'registration_window': 'Conducted 4 times a year (Quarterly)',
                                           'selection_stages': 'Written Exams (Air Navigation, Aviation Meteorology, '
                                                               'Air Regulation, Technical General, Technical Specific) '
                                                               '-> 200 Flying Hours Training -> Commercial Pilot '
                                                               'License (CPL) Issuance'},
                                       {   'conducting_body': 'Indira Gandhi Rashtriya Uran Akademi (IGRUA) & Airline '
                                                              'Cadet Programs (IndiGo/Air India)',
                                           'exam_category': 'National Flight Academy Entrance Test',
                                           'exam_date': 'June',
                                           'exam_name': 'IGRUA Entrance Examination & Airline Cadet Programs',
                                           'exam_pattern': '100 MCQs (General English, Maths, Physics, Reasoning)',
                                           'how_to_prepare': 'High mental arithmetic speed, spatial awareness, and '
                                                             'cockpit multitasking.',
                                           'official_portal': 'https://igrua.gov.in',
                                           'registration_window': 'March - May',
                                           'selection_stages': 'Stage 1: Online Written Test (Maths, Physics, English, '
                                                               'General Reasoning) -> Stage 2: Pilot Aptitude Test '
                                                               '(WOMBAT / COMPASS) -> Stage 3: Personal Interview'}],
        'salary_range': '₹1.8 - ₹3.5 Lakhs / month (Junior First Officer) -> ₹6.5 - ₹12+ Lakhs / month (Captain)',
        'sector': 'Design & Architecture'},
    {   'future_career_growth': [   'Assistant Professor (Stage 1) -> Assistant Professor (Stage 2) -> Associate '
                                    'Professor -> Professor -> Dean / Vice-Chancellor'],
        'government_perks_quotas': 'UGC 7th Pay Commission scales, paid academic sabbaticals, research grants, and '
                                   'high social dignity.',
        'id': 'pos_research_scientist_professor',
        'position_description': 'Delivers collegiate university lectures, mentors undergraduate students, spearheads '
                                'funded scientific research, and publishes high-impact journals.',
        'position_title': 'College Assistant Professor / Research Scientist (CS / Arts / Science)',
        'qualification_badge': "Master's Degree (M.Sc / M.A / M.E / M.Tech / Ph.D)",
        'qualification_stage': 'diploma_graduate',
        'recruiting_organizations': [   'Anna University',
                                        'University of Madras',
                                        'Presidency College',
                                        'Loyola College Chennai',
                                        'PSG Tech',
                                        'Govt Arts & Science Colleges'],
        'relevant_entrance_exams': [   {   'conducting_body': 'Teachers Recruitment Board (TRB), Government of Tamil '
                                                              'Nadu',
                                           'exam_category': 'State Collegiate Recruitment Examination',
                                           'exam_date': 'Scheduled via TRB Calendar',
                                           'exam_name': 'Tamil Nadu Teachers Recruitment Board (TN TRB) Assistant '
                                                        'Professor Exam',
                                           'exam_pattern': 'Subject Paper (200 Marks) + General Knowledge & Teaching '
                                                           'Aptitude',
                                           'how_to_prepare': 'Deep mastery of Post-Graduate core subject papers.',
                                           'official_portal': 'https://trb.tn.gov.in',
                                           'registration_window': 'As per TRB Annual Planner',
                                           'selection_stages': 'Written Competitive Exam -> Certificate Verification '
                                                               '-> Direct Appointment across 164+ TN Govt Arts & '
                                                               'Science Colleges and Govt Engineering Colleges'},
                                       {   'conducting_body': "National Testing Agency (NTA) & Mother Teresa Women's "
                                                              'University (TNSET)',
                                           'exam_category': 'National & State Eligibility Test for Assistant '
                                                            'Professorship & JRF',
                                           'exam_date': 'June and December',
                                           'exam_name': 'UGC-NET / CSIR-NET / TNSET',
                                           'exam_pattern': 'Paper 1: 50 Questions (100 Marks) | Paper 2: 100 Questions '
                                                           '(200 Marks)',
                                           'how_to_prepare': 'Research methodology, comprehension, and PG subject '
                                                             'literature.',
                                           'official_portal': 'https://ugcnet.nta.ac.in',
                                           'registration_window': 'Twice a year (June & December cycles)',
                                           'selection_stages': 'Paper 1 (Teaching & Research Aptitude) + Paper 2 '
                                                               '(Chosen Subject Domain) -> Qualify for Assistant '
                                                               'Professorship & Junior Research Fellowship (JRF - '
                                                               '₹37,000/mo stipend)'}],
        'salary_range': '₹57,700 - ₹1,82,400 / month (UGC Academic Level 10) + Academic Allowances',
        'sector': 'Engineering & Technology'}]


def get_all_career_positions(
    sector: Optional[str] = None,
    stage: Optional[str] = None,
    search: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Returns all career positions filtered by sector, stage, or search term."""
    results = list(CAREER_POSITIONS_DATABASE)
    if sector and sector.lower() != "all":
        results = [p for p in results if p.get("sector", "").lower() == sector.lower()]
    if stage and stage.lower() != "all":
        if stage == "after_10th":
            results = [p for p in results if p.get("qualification_stage") in ["after_10th", "after_10th_12th"]]
        elif stage == "after_12th":
            results = [p for p in results if p.get("qualification_stage") in ["after_12th", "after_10th_12th"]]
        elif stage == "diploma_graduate":
            results = [p for p in results if p.get("qualification_stage") in ["diploma_graduate"]]
        else:
            results = [p for p in results if p.get("qualification_stage") == stage]
    if search:
        s = search.lower().strip()
        filtered = []
        for p in results:
            pos_text = f"{p.get('position_title', '')} {p.get('sector', '')} {p.get('position_description', '')} {p.get('qualification_badge', '')}".lower()
            exam_text = " ".join([f"{e.get('exam_name', '')} {e.get('conducting_body', '')} {e.get('exam_category', '')}" for e in p.get("relevant_entrance_exams", [])]).lower()
            orgs_text = " ".join(p.get("recruiting_organizations", [])).lower()
            if s in pos_text or s in exam_text or s in orgs_text:
                filtered.append(p)
        results = filtered
    return results


def get_career_position_detail(position_id: str) -> Optional[Dict[str, Any]]:
    """Returns full detail of a specific career position including exams, salary, and perks."""
    for p in CAREER_POSITIONS_DATABASE:
        if p["id"] == position_id:
            return dict(p)
    return None
