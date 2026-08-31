"""
Skills knowledge base used for skill extraction and normalization.

Each entry maps a canonical skill name to its category and a list of
aliases/variants that should all normalize to that canonical name
(e.g. "Postgres", "PostgreSQL", "Postgre SQL" -> "PostgreSQL").

This is intentionally a plain Python data structure (not a DB table)
so it's fast to extend; `seed_skills()` in resume_service.py syncs it
into the `skills` table so jobs/candidates can reference it relationally.
"""

SKILLS_KB: dict[str, dict] = {
    "Python": {"category": "Programming", "aliases": ["py", "python3", "python 3", "python programming"]},
    "Java": {"category": "Programming", "aliases": ["java programming", "core java"]},
    "JavaScript": {"category": "Programming", "aliases": ["js", "java script", "es6", "es6+", "ecmascript", "vanilla js", "vanilla javascript"]},
    "TypeScript": {"category": "Programming", "aliases": ["ts"]},
    "C++": {"category": "Programming", "aliases": ["cpp", "c plus plus"]},
    "C#": {"category": "Programming", "aliases": ["csharp", "c sharp"]},
    "Go": {"category": "Programming", "aliases": ["golang"]},
    "Ruby": {"category": "Programming", "aliases": []},
    "PHP": {"category": "Programming", "aliases": []},
    "SQL": {"category": "Database", "aliases": ["structured query language"]},

    "React": {"category": "Frontend", "aliases": ["react", "react.js", "react-js", "reactjs", "react js", "react 18", "react 17"]},
    "Next.js": {"category": "Frontend", "aliases": ["next.js", "nextjs", "next js", "next"]},
    "Redux": {"category": "Frontend", "aliases": ["redux toolkit", "redux-toolkit", "react-redux"]},
    "React Native": {"category": "Mobile", "aliases": ["react-native", "reactnative"]},
    "Vue.js": {"category": "Frontend", "aliases": ["vue", "vuejs", "vue js"]},
    "Angular": {"category": "Frontend", "aliases": ["angularjs", "angular.js"]},
    "HTML": {"category": "Frontend", "aliases": ["html5"]},
    "CSS": {"category": "Frontend", "aliases": ["css3", "css styling"]},
    "Bootstrap": {"category": "Frontend", "aliases": ["bootstrap5", "bootstrap 5"]},
    "Tailwind CSS": {"category": "Frontend", "aliases": ["tailwind", "tailwindcss"]},
    "Expo": {"category": "Mobile", "aliases": ["expo go"]},
    "Flutter": {"category": "Mobile", "aliases": []},
    "Swift": {"category": "Mobile", "aliases": []},
    "Kotlin": {"category": "Mobile", "aliases": []},
    "Android Studio": {"category": "Tools", "aliases": ["android-studio"]},
    "Xcode": {"category": "Tools", "aliases": []},

    "Django": {"category": "Backend", "aliases": []},
    "FastAPI": {"category": "Backend", "aliases": ["fast api"]},
    "Flask": {"category": "Backend", "aliases": []},
    "Node.js": {"category": "Backend", "aliases": ["nodejs", "node js", "node"]},
    "Express.js": {"category": "Backend", "aliases": ["express", "expressjs", "express js"]},
    "Spring Boot": {"category": "Backend", "aliases": ["springboot", "spring"]},
    "REST API": {"category": "Backend", "aliases": ["rest apis", "restful api", "restful apis", "rest", "api integration", "api integrations"]},
    "GraphQL": {"category": "Backend", "aliases": []},
    "Firebase": {"category": "Backend", "aliases": ["firebase realtime", "cloud firestore", "firestore"]},

    "PostgreSQL": {"category": "Database", "aliases": ["postgres", "postgre sql", "postgressql"]},
    "MySQL": {"category": "Database", "aliases": ["my sql"]},
    "MongoDB": {"category": "Database", "aliases": ["mongo db", "mongo"]},
    "Redis": {"category": "Database", "aliases": []},
    "SQLite": {"category": "Database", "aliases": ["sqlite3"]},
    "Oracle Database": {"category": "Database", "aliases": ["oracle db", "oracle"]},

    "AWS": {"category": "Cloud", "aliases": ["amazon web services"]},
    "Azure": {"category": "Cloud", "aliases": ["microsoft azure"]},
    "Google Cloud Platform": {"category": "Cloud", "aliases": ["gcp", "google cloud"]},

    "Docker": {"category": "DevOps", "aliases": ["dockerized", "containerization"]},
    "Kubernetes": {"category": "DevOps", "aliases": ["k8s"]},
    "CI/CD": {"category": "DevOps", "aliases": ["ci cd", "continuous integration", "continuous deployment"]},
    "Jenkins": {"category": "DevOps", "aliases": []},
    "Git": {"category": "DevOps", "aliases": ["github", "gitlab", "version control", "git hub", "git lab"]},
    "GitHub Actions": {"category": "DevOps", "aliases": ["github actions"]},
    "Terraform": {"category": "DevOps", "aliases": []},
    "Linux": {"category": "DevOps", "aliases": ["unix", "bash"]},
    "VS Code": {"category": "Tools", "aliases": ["vscode", "visual studio code", "vs code"]},
    "Postman": {"category": "Tools", "aliases": ["postman api"]},
    "Figma": {"category": "Tools", "aliases": ["figma design"]},

    "Machine Learning": {"category": "AI", "aliases": ["ml"]},
    "Deep Learning": {"category": "AI", "aliases": ["dl"]},
    "Natural Language Processing": {"category": "AI", "aliases": ["nlp"]},
    "Computer Vision": {"category": "AI", "aliases": ["cv"]},
    "TensorFlow": {"category": "Machine Learning", "aliases": []},
    "PyTorch": {"category": "Machine Learning", "aliases": []},
    "scikit-learn": {"category": "Machine Learning", "aliases": ["sklearn", "scikit learn"]},
    "Keras": {"category": "Machine Learning", "aliases": []},
    "spaCy": {"category": "Machine Learning", "aliases": []},
    "Pandas": {"category": "Data Science", "aliases": []},
    "NumPy": {"category": "Data Science", "aliases": []},
    "Data Analysis": {"category": "Data Science", "aliases": ["data analytics"]},
    "Data Visualization": {"category": "Data Science", "aliases": []},

    "pytest": {"category": "Testing", "aliases": ["py.test"]},
    "Unit Testing": {"category": "Testing", "aliases": ["unit tests"]},
    "Selenium": {"category": "Testing", "aliases": []},

    "Project Management": {"category": "Management", "aliases": []},
    "Agile": {"category": "Management", "aliases": ["scrum", "agile methodology"]},
    "Team Leadership": {"category": "Management", "aliases": ["leadership", "team lead"]},
    "Team Collaboration": {"category": "Soft Skills", "aliases": ["team collaboration", "collaborative", "collaboration", "teamwork", "team player"]},
    "Communication": {"category": "Soft Skills", "aliases": ["communication skills"]},
    "Problem Solving": {"category": "Soft Skills", "aliases": ["problem-solving", "problem solving skills"]},
    "Debugging": {"category": "Soft Skills", "aliases": ["debugging skills", "debug"]},
    "Data Optimization": {"category": "Data Science", "aliases": ["data optimization", "query optimization", "sql optimization"]},
    "UI/UX": {"category": "Frontend", "aliases": ["ui ux", "ui/ux design", "user interface", "user experience"]},
    "UI Components": {"category": "Frontend", "aliases": ["ui components", "component design"]},
    "Next.js": {"category": "Frontend", "aliases": ["nextjs", "next js"]},
    "Nuxt.js": {"category": "Frontend", "aliases": ["nuxtjs", "nuxt js", "nuxt"]},
    "SASS": {"category": "Frontend", "aliases": ["scss", "sass/scss"]},
    "Webpack": {"category": "Frontend", "aliases": []},
    "Vite": {"category": "Frontend", "aliases": ["vitejs"]},
    "Redux": {"category": "Frontend", "aliases": ["redux toolkit", "rtk"]},
    "RxJS": {"category": "Frontend", "aliases": []},

    "gRPC": {"category": "Backend", "aliases": ["grpc api"]},
    "WebSockets": {"category": "Backend", "aliases": ["websocket", "socket.io"]},
    "OAuth": {"category": "Backend", "aliases": ["oauth2", "oauth 2.0", "sso", "single sign-on"]},
    "JWT": {"category": "Backend", "aliases": ["json web token"]},
    "Microservices": {"category": "Backend", "aliases": ["microservice architecture", "micro-services"]},
    "Event-Driven Architecture": {"category": "Backend", "aliases": ["event driven", "event-driven"]},
    "NestJS": {"category": "Backend", "aliases": ["nest.js", "nestjs"]},
    "Elixir": {"category": "Programming", "aliases": ["phoenix framework"]},
    "Rust": {"category": "Programming", "aliases": ["rustlang"]},

    "DynamoDB": {"category": "Database", "aliases": ["aws dynamodb"]},
    "Cassandra": {"category": "Database", "aliases": ["apache cassandra"]},
    "Elasticsearch": {"category": "Database", "aliases": ["opensearch", "elastic search"]},
    "Kafka": {"category": "DevOps", "aliases": ["apache kafka", "kafka messaging"]},
    "RabbitMQ": {"category": "DevOps", "aliases": ["rabbitmq queue"]},
    "Celery": {"category": "Backend", "aliases": ["celery task worker"]},
    "Supabase": {"category": "Backend", "aliases": []},
    "Neo4j": {"category": "Database", "aliases": ["graph database", "graph db"]},

    "Ansible": {"category": "DevOps", "aliases": []},
    "CloudFormation": {"category": "Cloud", "aliases": ["aws cloudformation"]},
    "Serverless": {"category": "Cloud", "aliases": ["serverless framework", "aws lambda"]},
    "Prometheus": {"category": "DevOps", "aliases": ["prometheus monitoring"]},
    "Grafana": {"category": "DevOps", "aliases": ["grafana dashboards"]},
    "Nginx": {"category": "DevOps", "aliases": ["nginx reverse proxy"]},
    "Apache": {"category": "DevOps", "aliases": ["apache web server"]},

    "LLM": {"category": "AI", "aliases": ["large language model", "large language models", "gpt-4", "chatgpt", "claude", "gemini"]},
    "RAG": {"category": "AI", "aliases": ["retrieval augmented generation", "retrieval-augmented generation"]},
    "LangChain": {"category": "AI", "aliases": ["langchain framework"]},
    "LlamaIndex": {"category": "AI", "aliases": ["llamaindex"]},
    "Transformers": {"category": "AI", "aliases": ["huggingface", "hugging face", "huggingface transformers"]},
    "Vector Database": {"category": "AI", "aliases": ["vector db", "chromadb", "pinecone", "milvus", "qdrant", "weaviate"]},
    "MLflow": {"category": "AI", "aliases": ["mlops"]},
    "Apache Spark": {"category": "Data Science", "aliases": ["spark", "pyspark"]},
    "Airflow": {"category": "Data Science", "aliases": ["apache airflow"]},

    "Jest": {"category": "Testing", "aliases": ["jest testing"]},
    "Cypress": {"category": "Testing", "aliases": ["cypress.io"]},
    "Playwright": {"category": "Testing", "aliases": []},
    "JUnit": {"category": "Testing", "aliases": ["junit5"]},
    "Test-Driven Development": {"category": "Testing", "aliases": ["tdd"]},

    "System Design": {"category": "Engineering", "aliases": ["system architecture", "software architecture"]},
    "Scalability": {"category": "Engineering", "aliases": ["scalable systems", "high availability", "load balancing"]},
    "Performance Optimization": {"category": "Engineering", "aliases": ["performance tuning", "code optimization", "memory optimization"]},
    "Code Review": {"category": "Engineering", "aliases": ["code reviews", "pull requests"]},
    "Security": {"category": "Engineering", "aliases": ["cybersecurity", "application security", "owasp"]},

    # HR & Talent Acquisition
    "Recruitment": {"category": "Human Resources", "aliases": ["recruiting", "talent sourcing", "sourcing"]},
    "Talent Acquisition": {"category": "Human Resources", "aliases": ["talent acquisition", "headhunting"]},
    "Employee Relations": {"category": "Human Resources", "aliases": ["employee engagement", "staff relations"]},
    "Performance Management": {"category": "Human Resources", "aliases": ["performance appraisal", "kpi management"]},
    "Onboarding": {"category": "Human Resources", "aliases": ["employee onboarding", "induction"]},
    "HR Policies": {"category": "Human Resources", "aliases": ["hr compliance", "company policies"]},
    "Payroll": {"category": "Human Resources", "aliases": ["payroll processing", "salary administration"]},
    "Workforce Planning": {"category": "Human Resources", "aliases": ["resource planning", "staffing"]},
    "HRIS": {"category": "Human Resources", "aliases": ["workday", "bambooHR", "peoplesoft", "personio"]},
    "Labor Laws": {"category": "Human Resources", "aliases": ["employment law", "labor compliance"]},

    # Accounting & Finance
    "Financial Accounting": {"category": "Finance", "aliases": ["accounting", "general ledger"]},
    "Auditing": {"category": "Finance", "aliases": ["internal audit", "financial audit", "audit"]},
    "Taxation": {"category": "Finance", "aliases": ["tax compliance", "income tax", "gst", "vat"]},
    "Bookkeeping": {"category": "Finance", "aliases": ["journal entries", "bank reconciliation"]},
    "Financial Analysis": {"category": "Finance", "aliases": ["financial modeling", "fp&a", "variance analysis"]},
    "Budgeting": {"category": "Finance", "aliases": ["budget forecasting", "cost control"]},
    "Financial Reporting": {"category": "Finance", "aliases": ["balance sheet", "p&l statement", "cash flow"]},
    "QuickBooks": {"category": "Finance Tools", "aliases": ["quickbooks online"]},
    "Tally": {"category": "Finance Tools", "aliases": ["tally prime", "tally erp"]},
    "Excel": {"category": "Tools", "aliases": ["ms excel", "microsoft excel", "vlookup", "pivot tables", "advanced excel"]},
    "Accounts Payable": {"category": "Finance", "aliases": ["ap accounting"]},
    "Accounts Receivable": {"category": "Finance", "aliases": ["ar accounting", "billing"]},

    # Marketing & Content
    "Digital Marketing": {"category": "Marketing", "aliases": ["online marketing", "internet marketing"]},
    "SEO": {"category": "Marketing", "aliases": ["search engine optimization", "on-page seo", "off-page seo"]},
    "Content Marketing": {"category": "Marketing", "aliases": ["content creation", "content strategy", "copywriting"]},
    "Social Media Marketing": {"category": "Marketing", "aliases": ["smm", "social media management", "facebook ads", "linkedin ads"]},
    "Google Analytics": {"category": "Marketing Tools", "aliases": ["ga4", "web analytics"]},
    "Email Marketing": {"category": "Marketing", "aliases": ["mailchimp", "email campaigns", "newsletter"]},
    "PPC": {"category": "Marketing", "aliases": ["pay per click", "google ads", "sem"]},
    "Market Research": {"category": "Marketing", "aliases": ["competitor analysis", "market analysis"]},
    "Brand Strategy": {"category": "Marketing", "aliases": ["brand management", "branding"]},

    # Sales & Business Development
    "Sales Strategy": {"category": "Sales", "aliases": ["sales management", "sales planning"]},
    "Lead Generation": {"category": "Sales", "aliases": ["prospecting", "lead nurturing", "cold calling"]},
    "B2B Sales": {"category": "Sales", "aliases": ["business to business", "enterprise sales"]},
    "CRM": {"category": "Sales Tools", "aliases": ["customer relationship management"]},
    "Salesforce": {"category": "Sales Tools", "aliases": ["salesforce crm"]},
    "HubSpot": {"category": "Sales Tools", "aliases": ["hubspot crm"]},
    "Negotiation": {"category": "Sales", "aliases": ["deal closing", "contract negotiation"]},
    "Account Management": {"category": "Sales", "aliases": ["key account management", "client relationship"]},

    # Project / Product Management & Operations
    "Scrum": {"category": "Management", "aliases": ["scrum master", "scrum framework"]},
    "Jira": {"category": "Tools", "aliases": ["atlassian jira", "confluence"]},
    "Product Strategy": {"category": "Product", "aliases": ["product vision", "product management"]},
    "Roadmapping": {"category": "Product", "aliases": ["product roadmap", "feature prioritization"]},
    "Stakeholder Management": {"category": "Management", "aliases": ["client communication", "stakeholder engagement"]},
    "Risk Management": {"category": "Management", "aliases": ["risk assessment", "mitigation"]},
    "Business Operations": {"category": "Operations", "aliases": ["operations management", "process optimization"]},
    "Vendor Management": {"category": "Operations", "aliases": ["supplier management", "procurement"]},
    "Supply Chain": {"category": "Operations", "aliases": ["logistics", "inventory management"]},
    "Customer Support": {"category": "Customer Success", "aliases": ["customer service", "helpdesk", "zendesk", "freshdesk"]},
    "Customer Success": {"category": "Customer Success", "aliases": ["client onboarding", "retention"]},
}


def build_alias_index() -> dict[str, str]:
    """Flatten SKILLS_KB into {lowercased alias/name -> canonical name}."""
    index: dict[str, str] = {}
    for canonical, meta in SKILLS_KB.items():
        index[canonical.lower()] = canonical
        for alias in meta.get("aliases", []):
            index[alias.lower()] = canonical
    return index


ALIAS_INDEX = build_alias_index()


def get_all_skill_variants(skill_name: str) -> set[str]:
    """Returns a set of all lowercased string representations (canonical name, raw name, and aliases) for a skill."""
    if not skill_name:
        return set()
    raw = skill_name.strip()
    raw_lower = raw.lower()
    variants = {raw_lower}

    canonical = ALIAS_INDEX.get(raw_lower, raw)
    canonical_lower = canonical.lower()
    variants.add(canonical_lower)

    if canonical in SKILLS_KB:
        for al in SKILLS_KB[canonical].get("aliases", []):
            variants.add(al.lower())

    for alias_key, canon_val in ALIAS_INDEX.items():
        if canon_val.lower() == canonical_lower:
            variants.add(alias_key.lower())

    return variants

