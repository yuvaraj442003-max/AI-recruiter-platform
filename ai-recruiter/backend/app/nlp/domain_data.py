"""
domain_data.py — Knowledge base of industry technology domains and job roles.

Maps standard job roles to their strict required skills, preferred skills,
and domain-specific key terms used for strict ATS domain evaluation.
"""

DOMAINS_KB: dict[str, dict] = {
    "Software Developer": {
        "title": "Software Developer",
        "description": "Software architecture, coding, system design, algorithm development, and application building.",
        "required_skills": ["SQL", "Git"],
        "core_languages": ["Python", "Java", "JavaScript", "C++", "C#", "TypeScript", "Go"],
        "preferred_skills": ["REST API", "Docker", "Unit Testing", "System Design", "Agile", "PostgreSQL", "Linux"],
        "keywords": ["software", "developer", "code", "programming", "algorithm", "architecture", "debugging", "repository", "git", "framework"],
        "certifications": ["AWS Certified Developer - Associate", "Oracle Certified Professional Developer", "Microsoft Certified: Azure Developer Associate"],
        "experience_guidance": [
            "Highlight core programming languages, software design patterns, and application scalability.",
            "Include quantifiable impact metrics: 'Developed core features serving 100k+ active users', 'Optimized code execution efficiency by 30%'."
        ],
    },
    "Backend Developer": {
        "title": "Backend Developer",
        "description": "Server-side logic, API development, databases, and microservices architecture.",
        "required_skills": ["REST API", "SQL"],
        "core_languages": ["Python", "Java", "Node.js", "Go", "C#", "FastAPI", "Django", "Spring Boot", "Express.js"],
        "preferred_skills": ["PostgreSQL", "MySQL", "MongoDB", "Redis", "Docker", "Microservices", "GraphQL", "gRPC", "Kafka", "Unit Testing", "System Design"],
        "keywords": ["api", "backend", "database", "orm", "queries", "server", "microservice", "endpoint", "architecture", "scalability", "restful"],
        "certifications": ["AWS Certified Developer - Associate", "Oracle Certified Professional: Java SE Developer", "Meta Backend Developer Professional Certificate"],
        "experience_guidance": [
            "Detail your experience designing scalable RESTful APIs, microservices, or database schemas.",
            "Include quantifiable metrics: API response time reductions (e.g., 'Reduced query execution time by 40%'), database query optimizations, or request throughput (RPS)."
        ],
    },
    "Frontend Developer": {
        "title": "Frontend Developer",
        "description": "User interface development, web components, state management, and responsive design.",
        "required_skills": ["JavaScript", "HTML", "CSS"],
        "core_languages": ["React", "Vue.js", "Angular", "TypeScript"],
        "preferred_skills": ["Next.js", "Tailwind CSS", "Bootstrap", "Redux", "SASS", "UI/UX", "Webpack", "Vite", "Jest"],
        "keywords": ["frontend", "ui", "ux", "component", "state management", "responsive", "browser", "dom", "web", "layout"],
        "certifications": ["Meta Frontend Developer Professional Certificate", "W3C Front-End Web Developer Certificate", "AWS Certified Developer"],
        "experience_guidance": [
            "Highlight modern frontend frameworks (React, Vue, Angular) and component-driven architecture.",
            "Add impact metrics such as 'Improved web page load speed by 35% using lazy loading & bundle optimization' or 'Increased mobile user conversion by 20% through responsive UI redesign'."
        ],
    },
    "Full Stack Developer": {
        "title": "Full Stack Developer",
        "description": "End-to-end application development spanning frontend interfaces and backend APIs.",
        "required_skills": ["JavaScript", "HTML", "CSS", "SQL", "REST API"],
        "core_languages": ["React", "Node.js", "Python", "TypeScript"],
        "preferred_skills": ["Next.js", "PostgreSQL", "MongoDB", "Docker", "Git", "CI/CD", "AWS", "Tailwind CSS", "GraphQL"],
        "keywords": ["fullstack", "full stack", "frontend", "backend", "database", "api", "client", "server", "deployment"],
        "certifications": ["IBM Full Stack Software Developer Professional Certificate", "AWS Certified Solutions Architect - Associate", "Meta Full Stack Developer Certificate"],
        "experience_guidance": [
            "Demonstrate end-to-end feature ownership from database design to UI implementation.",
            "Quantify product delivery impact (e.g., 'Built and deployed end-to-end portal serving 50k+ active users')."
        ],
    },
    "Data Analyst": {
        "title": "Data Analyst",
        "description": "Data collection, statistical analysis, SQL querying, business intelligence dashboards, and reporting.",
        "required_skills": ["SQL", "Excel", "Data Analysis"],
        "core_languages": ["Python", "Pandas", "NumPy", "Data Visualization"],
        "preferred_skills": ["Tableau", "Power BI", "PostgreSQL", "Statistics", "Google Analytics", "KPI Analysis"],
        "keywords": ["data analyst", "analytics", "sql", "excel", "dashboard", "reporting", "insights", "metrics", "kpi", "trends", "visualization"],
        "certifications": ["Google Data Analytics Professional Certificate", "Microsoft Certified: Power BI Data Analyst Associate", "IBM Data Analyst Professional Certificate"],
        "experience_guidance": [
            "Detail data modeling, SQL queries written, and BI dashboards generated for executive stakeholders.",
            "Quantify insights value: 'Generated data reports identifying \$200k in cost savings', 'Automated weekly executive dashboard saving 10 hours/week'."
        ],
    },
    "Data Scientist / AI Engineer": {
        "title": "Data Scientist / AI Engineer",
        "description": "Machine learning modeling, natural language processing, data analytics, and AI algorithms.",
        "required_skills": ["Python", "Machine Learning"],
        "core_languages": ["Pandas", "NumPy", "scikit-learn", "PyTorch", "TensorFlow"],
        "preferred_skills": ["Deep Learning", "Natural Language Processing", "LLM", "RAG", "spaCy", "Computer Vision", "SQL", "Data Analysis"],
        "keywords": ["data science", "machine learning", "ai", "model", "algorithm", "training", "nlp", "analytics", "statistics", "dataset"],
        "certifications": ["TensorFlow Developer Certificate", "AWS Certified Machine Learning - Specialty", "Google Cloud Professional Data Engineer"],
        "experience_guidance": [
            "Specify ML models, datasets, accuracy metrics (F1-score, Precision, Recall, RMSE) and training pipelines.",
            "Quantify business value (e.g., 'Trained NLP classification model achieving 92% accuracy, automating 80% of customer ticket routing')."
        ],
    },
    "DevOps / Cloud Engineer": {
        "title": "DevOps / Cloud Engineer",
        "description": "Infrastructure automation, CI/CD pipelines, container orchestration, and cloud architecture.",
        "required_skills": ["Docker", "CI/CD", "Linux"],
        "core_languages": ["AWS", "Kubernetes", "Git", "Terraform"],
        "preferred_skills": ["Azure", "Google Cloud Platform", "Jenkins", "GitHub Actions", "Prometheus", "Grafana", "Ansible", "Nginx", "Serverless"],
        "keywords": ["devops", "cloud", "infrastructure", "pipeline", "container", "automation", "deployment", "monitoring", "serverless"],
        "certifications": ["Certified Kubernetes Administrator (CKA)", "AWS Certified DevOps Engineer - Professional", "Docker Certified Associate (DCA)"],
        "experience_guidance": [
            "Detail CI/CD pipeline automation, infrastructure-as-code (Terraform), and containerization (Docker/K8s).",
            "Quantify reliability gains (e.g., 'Reduced deployment downtime to 0s with blue-green deployments and cut build times by 50%')."
        ],
    },
    "QA / Automation Test Engineer": {
        "title": "QA / Automation Test Engineer",
        "description": "Software quality assurance, automated test scripts, unit testing, and API verification.",
        "required_skills": ["Unit Testing"],
        "core_languages": ["pytest", "Selenium", "Jest", "Cypress", "Playwright"],
        "preferred_skills": ["JUnit", "Test-Driven Development", "Postman", "CI/CD", "JavaScript", "Python"],
        "keywords": ["qa", "testing", "test automation", "test cases", "bug", "quality assurance", "integration testing", "e2e"],
        "certifications": ["ISTQB Certified Tester Foundation Level (CTFL)", "Selenium Automation Test Engineer Certification"],
        "experience_guidance": [
            "Detail test automation frameworks built, regression test suite size, and CI pipeline test integration.",
            "Quantify quality improvements (e.g., 'Achieved 85%+ automated test coverage, reducing post-release bugs by 60%')."
        ],
    },
    "UI/UX Designer": {
        "title": "UI/UX Designer",
        "description": "User interface design, user experience research, wireframing, and interactive prototyping.",
        "required_skills": ["UI/UX"],
        "core_languages": ["Figma", "UI Components"],
        "preferred_skills": ["User Research", "Wireframing", "Prototyping", "Design System", "HTML", "CSS", "Tailwind CSS", "Bootstrap"],
        "keywords": ["design", "ui", "ux", "user interface", "user experience", "figma", "prototype", "wireframe", "usability"],
        "certifications": ["Google UX Design Professional Certificate", "Nielsen Norman Group UX Certification", "Figma Design System Certification"],
        "experience_guidance": [
            "Showcase user research methodologies, wireframes, interactive Figma prototypes, and design systems built.",
            "Quantify UX impact (e.g., 'Redesigned checkout workflow in Figma, reducing user drop-off rate by 25%')."
        ],
    },
    "Human Resources (HR) / Recruiter": {
        "title": "Human Resources (HR) / Recruiter",
        "description": "Talent acquisition, candidate interviewing, employee engagement, HR compliance, and payroll.",
        "required_skills": ["Recruitment", "Communication"],
        "core_languages": ["Talent Acquisition", "Employee Relations", "Onboarding"],
        "preferred_skills": ["HRIS", "HR Policies", "Workforce Planning", "Payroll", "Labor Laws", "Performance Management"],
        "keywords": ["hr", "human resources", "recruitment", "recruiter", "sourcing", "talent acquisition", "onboarding", "employee relations", "interviews", "hiring", "compliance"],
        "certifications": ["SHRM Certified Professional (SHRM-CP)", "PHR (Professional in Human Resources)", "AIHR HR Generalist Certificate"],
        "experience_guidance": [
            "Highlight end-to-end recruitment lifecycle, sourcing channels, candidate experience, and HR policy implementation.",
            "Quantify HR metrics: 'Hired 45+ technical candidates in 6 months', 'Reduced average time-to-hire by 25 days', 'Improved retention rate by 18%'."
        ],
    },
    "Accountant / Financial Analyst": {
        "title": "Accountant / Financial Analyst",
        "description": "Financial reporting, general ledger, auditing, tax compliance, budgeting, and financial modeling.",
        "required_skills": ["Financial Accounting", "Excel"],
        "core_languages": ["Financial Reporting", "Financial Analysis"],
        "preferred_skills": ["Auditing", "Taxation", "Bookkeeping", "Budgeting", "QuickBooks", "Tally", "Accounts Payable", "Accounts Receivable"],
        "keywords": ["accounting", "accountant", "financial", "finance", "audit", "tax", "ledger", "balance sheet", "p&l", "reconciliation", "budget", "compliance"],
        "certifications": ["CPA (Certified Public Accountant)", "CFA (Chartered Financial Analyst)", "ACCA Certification", "Certified Management Accountant (CMA)"],
        "experience_guidance": [
            "Detail financial statement preparation, month-end closing, tax compliance, and budget forecasting.",
            "Quantify financial impact: 'Managed \$5M annual budget with zero variance', 'Streamlined invoice reconciliation process saving 15 hours/month'."
        ],
    },
    "Digital Marketing Specialist": {
        "title": "Digital Marketing Specialist",
        "description": "Digital marketing campaigns, SEO optimization, social media strategy, content creation, and analytics.",
        "required_skills": ["Digital Marketing", "SEO"],
        "core_languages": ["Content Marketing", "Social Media Marketing"],
        "preferred_skills": ["Google Analytics", "PPC", "Email Marketing", "Brand Strategy", "Market Research", "Copywriting"],
        "keywords": ["marketing", "digital marketing", "seo", "sem", "content", "social media", "campaign", "traffic", "conversion", "google analytics", "brand", "copywriting"],
        "certifications": ["Google Digital Marketing & E-commerce Professional Certificate", "HubSpot Digital Marketing Certification", "Meta Certified Digital Marketing Associate"],
        "experience_guidance": [
            "Highlight SEO organic growth, PPC ad performance, social media campaign ROI, and content engagement.",
            "Quantify marketing impact: 'Increased organic website traffic by 140% in 90 days', 'Generated \$120k in revenue through targeted Google & Meta ad campaigns'."
        ],
    },
    "Sales & Business Development": {
        "title": "Sales & Business Development",
        "description": "B2B client acquisition, lead generation, sales pipeline management, contract negotiation, and CRM.",
        "required_skills": ["Sales Strategy", "Communication"],
        "core_languages": ["Lead Generation", "B2B Sales"],
        "preferred_skills": ["CRM", "Salesforce", "HubSpot", "Negotiation", "Account Management", "Cold Calling"],
        "keywords": ["sales", "business development", "b2b", "leads", "prospecting", "pipeline", "quota", "revenue", "crm", "salesforce", "closing", "deals"],
        "certifications": ["HubSpot Inbound Sales Certification", "Salesforce Certified Sales Cloud Consultant", "Certified Professional Sales Person (CPSP)"],
        "experience_guidance": [
            "Detail consultative sales process, client relationship building, and revenue quota achievements.",
            "Quantify sales results: 'Exceeded annual sales quota by 135% generating \$1.2M in new ARR', 'Closed 30+ enterprise client contracts'."
        ],
    },
    "Project / Product Manager": {
        "title": "Project / Product Manager",
        "description": "Project planning, Agile delivery, cross-functional leadership, product roadmap execution, and stakeholder management.",
        "required_skills": ["Project Management", "Agile"],
        "core_languages": ["Scrum", "Product Strategy"],
        "preferred_skills": ["Jira", "Roadmapping", "Stakeholder Management", "Risk Management", "Team Leadership", "Budgeting"],
        "keywords": ["project manager", "product manager", "agile", "scrum", "jira", "roadmap", "stakeholder", "sprint", "milestones", "delivery", "leadership"],
        "certifications": ["PMP (Project Management Professional)", "Certified ScrumMaster (CSM)", "PMI-ACP", "Certified Product Manager (AIPMM)"],
        "experience_guidance": [
            "Highlight end-to-end project lifecycle management, sprint planning, risk mitigation, and cross-functional team coordination.",
            "Quantify delivery success: 'Led 12-person cross-functional team to deliver flagship product on time and 15% under budget'."
        ],
    },
    "Business Operations Manager": {
        "title": "Business Operations Manager",
        "description": "Process optimization, business strategy execution, operational efficiency, vendor management, and supply chain.",
        "required_skills": ["Business Operations", "Problem Solving"],
        "core_languages": ["Process Optimization", "Vendor Management"],
        "preferred_skills": ["Supply Chain", "Budgeting", "Project Management", "Risk Management", "Data Analysis", "Team Leadership"],
        "keywords": ["operations", "process", "workflow", "efficiency", "vendor", "supply chain", "logistics", "optimization", "strategy", "management"],
        "certifications": ["Six Sigma Green / Black Belt", "Certified Supply Chain Professional (CSCP)", "Certified Operations Management Professional"],
        "experience_guidance": [
            "Detail operational workflow redesigns, cost reduction initiatives, and cross-departmental coordination.",
            "Quantify operational metrics: 'Streamlined operational processes, reducing operational overhead by 22% and improving turnaround time by 40%'."
        ],
    },
    "Customer Success / Support Specialist": {
        "title": "Customer Success / Support Specialist",
        "description": "Customer onboarding, issue resolution, client retention, helpdesk support, and account relationship management.",
        "required_skills": ["Customer Support", "Communication"],
        "core_languages": ["Customer Success", "Troubleshooting"],
        "preferred_skills": ["Zendesk", "Freshdesk", "CRM", "Stakeholder Management", "Account Management"],
        "keywords": ["customer support", "customer success", "client support", "helpdesk", "tickets", "zendesk", "retention", "onboarding", "satisfaction", "csat"],
        "certifications": ["Certified Customer Success Manager (CCSM)", "HubSpot Service Hub Certification", "ITIL Foundation Certificate"],
        "experience_guidance": [
            "Highlight resolution times, customer satisfaction (CSAT) scores, and proactive client retention efforts.",
            "Quantify support metrics: 'Maintained 98%+ CSAT rating across 5,000+ support tickets while reducing average resolution time to under 15 mins'."
        ],
    },
    "Cyber Security Specialist": {
        "title": "Cyber Security Specialist",
        "description": "Information security, network defense, threat analysis, vulnerability assessments, and security compliance.",
        "required_skills": ["Security", "Linux"],
        "core_languages": ["Network Security", "Vulnerability Assessment"],
        "preferred_skills": ["AWS", "Docker", "OWASP", "Penetration Testing", "SIEM", "Firewall", "Risk Management"],
        "keywords": ["security", "cybersecurity", "network", "firewall", "vulnerability", "penetration testing", "siem", "compliance", "threat", "incident response"],
        "certifications": ["CompTIA Security+", "CISSP (Certified Information Systems Security Professional)", "CEH (Certified Ethical Hacker)"],
        "experience_guidance": [
            "Detail security audits conducted, incident response protocols, and vulnerability remediations.",
            "Quantify security impact: 'Identified and patched 120+ critical vulnerabilities across corporate infrastructure, achieving 100% SOC2 compliance'."
        ],
    },
}


def get_available_domains() -> list[dict]:
    """Returns list of domain options for dropdown selection."""
    return [
        {"key": key, "title": meta["title"], "description": meta["description"]}
        for key, meta in DOMAINS_KB.items()
    ]
