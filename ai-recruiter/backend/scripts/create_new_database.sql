-- ====================================================================
-- AI RECRUITER PLATFORM - COMPLETE POSTGRESQL SCHEMA INITIALIZATION
-- Run this script in pgAdmin Query Tool or psql to create a fresh DB
-- ====================================================================

-- Step 1: Create Database (Run this line separately if in psql)
-- CREATE DATABASE ai_recruiter;
-- \c ai_recruiter;

-- Enable UUID extension for auto-generating UUID keys
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop existing tables if re-initializing (Order matters for Foreign Keys)
DROP TABLE IF EXISTS chat_messages CASCADE;
DROP TABLE IF EXISTS notifications CASCADE;
DROP TABLE IF EXISTS audit_logs CASCADE;
DROP TABLE IF EXISTS interview_evaluations CASCADE;
DROP TABLE IF EXISTS interview_answers CASCADE;
DROP TABLE IF EXISTS interview_questions CASCADE;
DROP TABLE IF EXISTS interviews CASCADE;
DROP TABLE IF EXISTS application_status_history CASCADE;
DROP TABLE IF EXISTS applications CASCADE;
DROP TABLE IF EXISTS job_skills CASCADE;
DROP TABLE IF EXISTS jobs CASCADE;
DROP TABLE IF EXISTS candidate_skills CASCADE;
DROP TABLE IF EXISTS skills CASCADE;
DROP TABLE IF EXISTS candidate_profiles CASCADE;
DROP TABLE IF EXISTS companies CASCADE;
DROP TABLE IF EXISTS recruiter_profiles CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- --------------------------------------------------------------------
-- 1. USERS TABLE
-- --------------------------------------------------------------------
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'candidate', -- 'candidate', 'recruiter', 'admin', 'superadmin'
    is_active BOOLEAN DEFAULT TRUE,
    verification_status VARCHAR(50) DEFAULT 'approved',
    verification_reasons TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------------------
-- 2. RECRUITER PROFILES TABLE
-- --------------------------------------------------------------------
CREATE TABLE recruiter_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    company_name VARCHAR(255),
    phone VARCHAR(50),
    recruiter_linkedin_url VARCHAR(255),
    company_linkedin_url VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------------------
-- 3. COMPANIES TABLE
-- --------------------------------------------------------------------
CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    domain VARCHAR(255),
    verification_status VARCHAR(50) DEFAULT 'unverified',
    verification_details TEXT,
    ssl_details TEXT,
    verification_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------------------
-- 4. CANDIDATE PROFILES TABLE
-- --------------------------------------------------------------------
CREATE TABLE candidate_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    phone VARCHAR(50),
    location VARCHAR(255),
    experience_years FLOAT DEFAULT 0.0,
    parsed_resume_json TEXT,
    profile_photo VARCHAR(500),
    headline VARCHAR(255),
    "current_role" VARCHAR(255),
    certifications TEXT,
    portfolio_url VARCHAR(255),
    linkedin_url VARCHAR(255),
    github_url VARCHAR(255),
    other_links TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------------------
-- 5. SKILLS TAXONOMY TABLE
-- --------------------------------------------------------------------
CREATE TABLE skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    skill_name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------------------
-- 6. CANDIDATE SKILLS (JOIN TABLE)
-- --------------------------------------------------------------------
CREATE TABLE candidate_skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id UUID NOT NULL REFERENCES candidate_profiles(id) ON DELETE CASCADE,
    skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    proficiency_level VARCHAR(50) DEFAULT 'intermediate',
    years_experience FLOAT DEFAULT 0.0,
    CONSTRAINT uq_candidate_skill UNIQUE (candidate_id, skill_id)
);

-- --------------------------------------------------------------------
-- 7. JOBS TABLE
-- --------------------------------------------------------------------
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recruiter_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(255),
    employment_type VARCHAR(50) NOT NULL DEFAULT 'full_time',
    experience_required FLOAT DEFAULT 0.0,
    salary_range VARCHAR(100),
    status VARCHAR(50) NOT NULL DEFAULT 'published',
    fraud_risk_score FLOAT DEFAULT 0.0,
    fraud_risk_level VARCHAR(20) DEFAULT 'LOW',
    fraud_reasons TEXT,
    company_name VARCHAR(255),
    company_logo VARCHAR(500),
    company_description TEXT,
    company_website VARCHAR(255),
    company_location VARCHAR(255),
    industry VARCHAR(150),
    company_size VARCHAR(100),
    linkedin_profile VARCHAR(255),
    github_profile VARCHAR(255),
    other_links TEXT,
    min_ats_score FLOAT DEFAULT 60.0,
    min_job_match_score FLOAT DEFAULT 60.0,
    min_experience FLOAT DEFAULT 0.0,
    auto_screening BOOLEAN DEFAULT TRUE,
    auto_shortlist BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------------------
-- 8. JOB SKILLS (JOIN TABLE)
-- --------------------------------------------------------------------
CREATE TABLE job_skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    required BOOLEAN DEFAULT TRUE,
    weight FLOAT DEFAULT 1.0,
    CONSTRAINT uq_job_skill UNIQUE (job_id, skill_id)
);

-- --------------------------------------------------------------------
-- 9. APPLICATIONS TABLE
-- --------------------------------------------------------------------
CREATE TABLE applications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id UUID NOT NULL REFERENCES candidate_profiles(id) ON DELETE CASCADE,
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL DEFAULT 'applied',
    match_score FLOAT,
    match_breakdown TEXT,
    ats_score FLOAT,
    job_match_score FLOAT,
    skills_match_score FLOAT,
    experience_match_score FLOAT,
    education_match_score FLOAT,
    location_match_score FLOAT,
    keyword_match_score FLOAT,
    responsibility_match_score FLOAT,
    matched_skills TEXT,
    missing_skills TEXT,
    matched_keywords TEXT,
    missing_keywords TEXT,
    recommendation VARCHAR(100),
    screening_status VARCHAR(100),
    is_eligible BOOLEAN DEFAULT FALSE,
    is_shortlisted BOOLEAN DEFAULT FALSE,
    screened_at TIMESTAMP WITH TIME ZONE,
    screening_version VARCHAR(50) DEFAULT 'v1.0',
    recruiter_override BOOLEAN DEFAULT FALSE,
    override_reason TEXT,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_candidate_job_application UNIQUE (candidate_id, job_id)
);

-- --------------------------------------------------------------------
-- 10. APPLICATION STATUS HISTORY TABLE
-- --------------------------------------------------------------------
CREATE TABLE application_status_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    application_id UUID NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
    old_status VARCHAR(50),
    new_status VARCHAR(50) NOT NULL,
    changed_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------------------
-- 11. INTERVIEWS TABLE
-- --------------------------------------------------------------------
CREATE TABLE interviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id UUID NOT NULL REFERENCES candidate_profiles(id) ON DELETE CASCADE,
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    application_id UUID REFERENCES applications(id) ON DELETE CASCADE,
    interview_type VARCHAR(50) NOT NULL DEFAULT 'technical',
    status VARCHAR(50) NOT NULL DEFAULT 'scheduled',
    overall_score FLOAT,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------------------
-- 12. INTERVIEW QUESTIONS TABLE
-- --------------------------------------------------------------------
CREATE TABLE interview_questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    interview_id UUID NOT NULL REFERENCES interviews(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    question_type TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    expected_topics TEXT,
    order_number INT NOT NULL
);

-- --------------------------------------------------------------------
-- 13. INTERVIEW ANSWERS TABLE
-- --------------------------------------------------------------------
CREATE TABLE interview_answers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_id UUID UNIQUE NOT NULL REFERENCES interview_questions(id) ON DELETE CASCADE,
    candidate_id UUID NOT NULL REFERENCES candidate_profiles(id) ON DELETE CASCADE,
    answer_text TEXT NOT NULL,
    answer_source TEXT NOT NULL DEFAULT 'text',
    answer_score FLOAT,
    feedback TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------------------
-- 14. INTERVIEW EVALUATIONS TABLE
-- --------------------------------------------------------------------
CREATE TABLE interview_evaluations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    interview_id UUID UNIQUE NOT NULL REFERENCES interviews(id) ON DELETE CASCADE,
    overall_score FLOAT NOT NULL,
    technical_score FLOAT,
    relevance_score FLOAT,
    communication_score FLOAT,
    problem_solving_score FLOAT,
    strengths TEXT,
    weaknesses TEXT,
    recommendation TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------------------
-- 15. AUDIT LOGS TABLE
-- --------------------------------------------------------------------
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    details TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------------------
-- 16. NOTIFICATIONS TABLE
-- --------------------------------------------------------------------
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------------------
-- 17. CHAT MESSAGES TABLE
-- --------------------------------------------------------------------
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sender_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    receiver_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ====================================================================
-- SEED INITIAL SKILLS TAXONOMY
-- ====================================================================
INSERT INTO skills (skill_name, category) VALUES
    ('Python', 'Programming'),
    ('FastAPI', 'Backend'),
    ('PostgreSQL', 'Database'),
    ('Docker', 'DevOps'),
    ('React', 'Frontend'),
    ('TypeScript', 'Programming'),
    ('Machine Learning', 'AI/ML'),
    ('PyTorch', 'AI/ML'),
    ('SQL', 'Database'),
    ('REST API', 'Backend'),
    ('AWS', 'Cloud'),
    ('Git', 'DevOps')
ON CONFLICT (skill_name) DO NOTHING;

-- ====================================================================
-- SUCCESS VERIFICATION QUERY
-- ====================================================================
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;
