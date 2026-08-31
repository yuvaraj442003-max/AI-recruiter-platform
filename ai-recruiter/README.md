# AI Recruiter — AI-Powered Recruitment & Interview Platform

**Status: Phase 1 — authentication foundation.** Resume parsing, AI matching, ranking,
interviews, and analytics are built in later phases on top of this base.

## 1. Project Overview

AI Recruiter helps recruiters analyze resumes, match candidates to jobs, rank candidates,
generate interview questions, run AI-assisted interviews, and produce evaluation reports.
Candidates can register, upload resumes, find recommended jobs, apply, and take AI interviews.

**Status: All 7 phases complete.** Auth, resume upload/parsing/NLP, job matching, LLM
service + AI summaries/analysis/questions, the full AI interview flow, analytics
dashboards, and the admin panel + production hardening below.

## 2. Features

### Phase 1 — Foundation
- Recruiter and candidate registration with role selection
- Secure login with hashed passwords (bcrypt) and JWT access/refresh tokens
- Protected `/auth/me` endpoint and role-based access control (`require_role`)
- Consistent `{success, message, data}` / `{success, message, error_code}` API responses
- Global FastAPI exception handling
- Plain HTML/CSS/JS frontend (no build tooling): Login/Register pages, a shared
  `fetch()`-based API layer with JWT handling, role-guarded dashboards
- Dockerized: FastAPI backend (PostgreSQL) + nginx-served static frontend via `docker-compose`


### Phase 2 — Resume AI
- Resume upload (PDF/DOCX, 10MB limit) with extension/size/secure-filename validation
- Text extraction: PyMuPDF (primary) with a pdfplumber fallback for PDFs, python-docx for DOCX
- NLP pipeline (spaCy for tokenization/lemmatization/NER, NLTK for sentence splitting):
  cleans text, extracts name/email/phone/education/experience-years/summary, runs NER for
  organizations and locations
- Alias-based skill extraction against a 60+ skill knowledge base (`app/nlp/skills_data.py`)
  with normalization (e.g. "Postgres"/"Postgre SQL" → "PostgreSQL")
- `CandidateProfile`, `Skill`, `CandidateSkill` tables; skills auto-seed on startup
- A transparent profile-completeness score (0–100) — not a candidate quality judgment
- Upload Resume page in the frontend with drag-and-drop, live parsed-profile preview,
  and skill badges

### Phase 3 — Job Matching
- Job CRUD (recruiter, owner-only edit/delete), with required/preferred skills either
  given explicitly or auto-extracted from the description via the Phase 2 NLP pipeline
- `Job`, `JobSkill`, `Application` tables (match score + full JSON explanation stored
  per application)
- TF-IDF + cosine similarity matching (`app/ml/tfidf_matcher.py`, scikit-learn)
- Semantic matching (`app/ml/semantic_matcher.py`) with a **3-tier fallback**:
  Sentence-Transformers (`all-MiniLM-L6-v2`) → spaCy `en_core_web_md` word vectors
  (network-free) → TF-IDF, so it never hard-fails even without internet access to
  huggingface.co
- Explainable final match score (`app/ml/ranking.py`): skill match 40%, experience
  match 20%, TF-IDF 15%, semantic 20%, preferred skills 5% — always returned with
  matched/missing skills, never as a bare number
- Apply to jobs (blocks duplicate applications and applying without a resume),
  recruiter-only ranked applicant view, application status updates (shortlist/reject/etc.),
  ad-hoc match-score preview, and job recommendations for candidates
- Frontend: job browsing + apply with live recommendations (`jobs.html`), job posting
  (`post-job.html`), a recruiter's job list (`my-jobs.html`), a ranked-applicant view with
  score breakdowns (`job-applicants.html`), and a candidate's application history
  (`my-applications.html`)

### Phase 4 — LLM Service
- Provider-agnostic LLM service layer (`app/ai/llm_service.py`): configurable via
  `LLM_PROVIDER` (`openai` or `huggingface`), auto-detected from whichever API key is
  set if unspecified. Every call gracefully returns `None` on failure — no LLM
  provider is ever able to break an unrelated request
- **AI resume summary** (`POST /resumes/summary`): a 3-4 sentence professional summary
  generated from the parsed resume, stored separately from the raw NLP-extracted
  `summary` field as `ai_summary`
- **AI job description analysis** (`POST /jobs/analyze`): extracts title, required/preferred
  skills, and experience range from a pasted job description, to pre-fill the "Post a
  Job" form
- **AI interview question generation** (`POST /jobs/{id}/generate-questions`): technical
  (skill-based), behavioral, and problem-solving questions across easy/medium/hard
  difficulty — preview only; persisting into an actual interview happens in Phase 5
- Every one of the above has a **deterministic template fallback** (built from the
  Phase 2/3 NLP data, or a hand-written question bank) used automatically when no LLM
  is configured or the call fails, so the whole platform works immediately without an
  API key and never hard-fails because of an LLM outage
- Frontend: "Generate with AI" on the resume page, "Analyze with AI" on the job-posting
  form, and "Generate Questions" on the applicant-ranking page

### Phase 5 — AI Interview
- `Interview`, `InterviewQuestion`, `InterviewAnswer`, `InterviewEvaluation` tables
- Recruiter starts an interview for an applicant in one action (`POST /interviews`) —
  validated against an existing `Application`, auto-generates and persists questions via
  the Phase 4 question generator
- Candidate answers one question at a time (text, or voice transcribed via `/speech/transcribe`
  and reviewed before submitting); each answer is auto-evaluated on submission
  (`app/ai/interview_evaluator.py`) with a genuine LLM path and a keyword-overlap template
  fallback, explicitly labeled low-fidelity rather than presented as equivalent
- The interview **auto-completes** once every question is answered, immediately rolling
  per-answer scores into a holistic `InterviewEvaluation` (category scores are always a
  straightforward average — never LLM-guessed — only the strengths/weaknesses/recommendation
  text is optionally LLM-generated)
- Full interview report (`GET /interviews/{id}/report`) with per-question breakdown,
  category scores, strengths/weaknesses, and an explicit **"Human Review Required"** notice
  — the AI evaluation is decision support, never an automated hiring decision
- Whisper-based speech-to-text (`app/ai/whisper_service.py`) has **no fake fallback** —
  unlike summaries/matching, a wrong transcription would be actively misleading, so with
  no provider configured it returns a clear `503 TRANSCRIPTION_UNAVAILABLE` asking the
  candidate to type instead, rather than guessing
- Audio is transcribed in memory and never written to disk, per the platform's privacy
  principles (Phase 2)
- Frontend: `interview.html` (progress bar, one question at a time, text answers plus
  optional browser mic recording via `MediaRecorder`), `interview-report.html` (shared
  view for both roles), and "Start Interview" wired into the recruiter's applicant list

### Phase 6 — Professional Dashboard
- `app/services/analytics_service.py` aggregates existing data on request (no new tables,
  no caching layer — dashboard traffic doesn't need it) into two endpoints:
  `GET /analytics/recruiter` and `GET /analytics/candidate`
- **Recruiter dashboard**: real stat cards (total jobs, candidates, applications,
  shortlisted, interviews, selected) and four Chart.js charts — applications by job,
  hiring funnel (by application status), top candidate skills across applicants, and
  interview scores — plus a per-job performance table (applications, avg match score,
  interviews completed)
- **Candidate dashboard**: real stat cards (profile completion, resume status,
  applications, interview status), a profile-completion donut chart, an
  applications-by-status chart, the latest completed interview score, a job-recommendation
  count (jobs scoring 60%+), and extracted skill badges
- Every number is computed from real jobs/applications/interviews/skills data — verified
  live end-to-end with a recruiter running two jobs, a candidate applying, being
  shortlisted, and completing an interview, then confirming both dashboards reflect it
  correctly (shortlisted count, hiring funnel, per-job performance, profile completion,
  interview score, and skill aggregation all checked against the real values)

### Phase 7 — Production
- **Security fix**: public registration can no longer create an admin account —
  `UserRegister` validates `role` against `{candidate, recruiter}` only, enforced
  server-side (not just hidden from the frontend). The only way to get an admin
  account is `scripts/create_admin.py`, run with server access
- **Admin panel** (`app/routers/admin.py`, admin-only): list/filter/view/delete users
  (can't delete yourself), create/delete skills, view every job across all recruiters
  with applicant counts, system-wide statistics (users by role, jobs, applications by
  status, avg match/interview scores, interview completion rate, most-requested skills,
  most common candidate skills), and a searchable audit log
- **Audit logging** (`AuditLog` table, `app/utils/audit.py`): records logins,
  registrations, failed logins, and admin actions (user deletion, skill create/delete)
  with a short JSON detail blob and IP address — never passwords, tokens, resume text,
  or interview answers. Failures here are logged and swallowed, never break the request
  they're describing
- **Rate limiting** (`app/core/rate_limit.py`): a per-IP sliding-window limiter on
  registration, and — more importantly — a failed-login lockout by email on `/auth/login`
  (5 failures in 15 minutes locks out even the correct password until the window
  expires), the standard defense against credential stuffing
- **Security headers middleware**: `X-Content-Type-Options`, `X-Frame-Options`,
  `Referrer-Policy`, and a locked-down `Content-Security-Policy` (this is a JSON API,
  so `default-src 'none'`) on every response
- **Found and fixed a real bug** while building this: the global validation-error
  handler crashed with a `TypeError` when a `field_validator` raised a plain
  `ValueError` (Pydantic v2 embeds the raw exception in `ctx.error`, which isn't
  JSON-serializable) — now sanitized before encoding
- **Docker hardening**: backend runs as a non-root user, `HEALTHCHECK` on both the
  Dockerfile and docker-compose, frontend waits on backend health not just backend
  start, a commented `gunicorn` multi-worker `CMD` for production
- **CI**: `.github/workflows/backend-tests.yml` runs the full pytest suite (with the
  spaCy models and NLTK data) plus a frontend JS syntax check on every push/PR
- Frontend: `admin.html` — tabbed panel (Users/Skills/Jobs/Audit Log) with the same
  system stat cards, wired into login/register's role-based redirect

## 3. Architecture

```
HTML/CSS/JS  →  REST API (/api/v1)  →  FastAPI  →  SQLite
```

## 4. Technology Stack

**Frontend:** Plain HTML5, CSS3, JavaScript (no build step), Bootstrap 5 via CDN
**Backend:** FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2, python-jose (JWT), passlib/bcrypt
**Database:** SQLite by default (single file, zero setup) — swap `DATABASE_URL` to a
PostgreSQL connection string if you'd rather; every model/migration uses a
dialect-agnostic UUID type (`app/core/db_types.py`), so nothing else needs to change
**Infra:** Docker, docker-compose (frontend served by nginx)

## 5. Project Structure

```
ai-recruiter/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI app entrypoint
│   │   ├── core/               # config, database, security, deps, exceptions
│   │   ├── models/              # SQLAlchemy models (User in Phase 1)
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   ├── routers/             # API route modules (auth in Phase 1)
│   │   ├── services/            # business logic (later phases)
│   │   ├── ai/ nlp/ ml/         # AI/NLP/ML modules (later phases)
│   │   ├── utils/ middleware/   # helpers (later phases)
│   ├── alembic/                 # DB migrations
│   ├── uploads/                 # resume storage (later phases)
│   ├── tests/                   # pytest suite
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
├── frontend-html/
│   ├── index.html                 # landing page
│   ├── login.html
│   ├── register.html
│   ├── recruiter-dashboard.html
│   ├── candidate-dashboard.html
│   ├── css/style.css              # custom styles on top of Bootstrap 5 CDN
│   ├── js/
│   │   ├── api.js                 # fetch wrapper + JWT storage (shared)
│   │   ├── auth-guard.js          # protects dashboard pages
│   │   ├── login.js
│   │   ├── register.js
│   │   └── dashboard.js
│   ├── assets/                    # images/icons
│   └── Dockerfile                 # nginx static file server
├── docker-compose.yml
└── README.md
```

## 6. Installation & Setup

### Prerequisites
- Python 3.12+
- Node.js 20+ (only if you want to serve the frontend via something other than plain `python3 -m http.server`)
- Docker + Docker Compose (optional but recommended)

No database server to install — SQLite ships with Python.

### Option A — Run everything with Docker (recommended)

```bash
cd ai-recruiter
cp backend/.env.example backend/.env      # edit JWT_SECRET before real use
docker compose up --build
```

- Backend: http://localhost:8000 (Swagger docs at http://localhost:8000/docs)
- Frontend: http://localhost:8080
- The SQLite database file lives in a named Docker volume (`ai_recruiter_data`), so it
  persists across container restarts and rebuilds.

Run migrations once the containers are up:

```bash
docker compose exec backend alembic upgrade head
```

### Option B — Run backend and frontend locally

#### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # DATABASE_URL already defaults to SQLite; edit JWT_SECRET
```

Then install the spaCy English model (not on PyPI proper):

```bash
python -m spacy download en_core_web_sm
```

If that 403s behind a restrictive network/proxy, install the wheel directly instead:

```bash
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
```

#### Database Setup

Nothing to create — SQLite is just a file, created automatically. Run migrations:

```bash
alembic upgrade head
```

This creates `backend/ai_recruiter.db`. Start the API:

```bash
uvicorn app.main:app --reload
```

API is now live at http://localhost:8000, Swagger UI at http://localhost:8000/docs.

#### Frontend Setup

No install or build step — it's plain HTML/CSS/JS. Just serve the folder statically:

```bash
cd frontend-html
python3 -m http.server 8080
```

Frontend is now live at http://localhost:8080. If your backend isn't at
`http://localhost:8000`, update the one constant at the top of `js/api.js`:

```javascript
const API_BASE_URL = "http://localhost:8000/api/v1";
```

## 7. Environment Variables

See `backend/.env.example` and `frontend/.env.example`. Never commit real `.env` files.

Key backend variables:

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | SQLAlchemy connection string |
| `JWT_SECRET` | Secret used to sign access/refresh tokens — set a strong random value |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token lifetime |
| `CORS_ORIGINS` | Comma-separated list of allowed frontend origins |
| `LLM_PROVIDER` | `openai` or `huggingface` — auto-detected from the keys below if unset |
| `OPENAI_API_KEY`, `OPENAI_MODEL`, `OPENAI_BASE_URL` | OpenAI (or OpenAI-compatible) provider config |
| `HF_API_KEY`, `HF_MODEL` | Hugging Face Inference API provider config |

Everything LLM-related is optional — with nothing set, AI summary/analysis/question
endpoints automatically use their template fallback (see section 15).

## 8. Running Locally — Quick Test

1. Start the backend and frontend (Docker or manual, above).
2. Open http://localhost:8000/docs and try `POST /api/v1/auth/register`:
   ```json
   {
     "name": "Jane Doe",
     "email": "jane@example.com",
     "password": "SecurePass123",
     "role": "candidate"
   }
   ```
3. Copy the returned `access_token` and call `GET /api/v1/auth/me` with header
   `Authorization: Bearer <token>` — should return the same user.
4. Open http://localhost:8080/register.html in the browser and create an account through
   the UI; you should land on the role-appropriate dashboard.

## 9. API Documentation

FastAPI auto-generates interactive docs:

- Swagger UI: `/docs`
- ReDoc: `/redoc`
- Raw OpenAPI schema: `/openapi.json`

### Phase 1, 2 & 3 Endpoints

```
POST /api/v1/auth/register   → create account, returns tokens + user
POST /api/v1/auth/login      → returns tokens + user
POST /api/v1/auth/refresh    → exchange refresh token for a new pair
GET  /api/v1/auth/me         → current user (requires Bearer token)

POST /api/v1/resumes/upload      → upload + parse a resume (candidate only)
GET  /api/v1/resumes/me          → the current candidate's parsed profile
GET  /api/v1/resumes/{id}        → any candidate's profile (recruiter/admin only)

POST   /api/v1/jobs                    → create a job (recruiter only)
GET    /api/v1/jobs                    → search/list jobs (?title=&location=&employment_type=)
GET    /api/v1/jobs/{id}               → job detail
PUT    /api/v1/jobs/{id}               → update a job (owner only)
DELETE /api/v1/jobs/{id}               → delete a job (owner only)
POST   /api/v1/jobs/{id}/apply         → apply to a job (candidate only)
GET    /api/v1/jobs/{id}/ranking       → ranked applicants with score breakdown (owner only)
GET    /api/v1/jobs/{id}/applications  → applications with candidate info (owner only)

GET   /api/v1/applications             → the current candidate's own applications
GET   /api/v1/applications/{id}        → application detail (owning candidate or recruiter)
PATCH /api/v1/applications/{id}/status → update application status (owning recruiter)

GET /api/v1/matching/{candidate_id}/{job_id}  → ad-hoc match score preview
GET /api/v1/recommendations/jobs              → jobs recommended for the current candidate

POST /api/v1/resumes/summary                  → generate/refresh the candidate's AI summary
POST /api/v1/jobs/analyze                     → analyze a job description (no job created)
POST /api/v1/jobs/{id}/generate-questions     → generate interview questions for a job

POST /api/v1/interviews                            → start an interview for candidate+job (recruiter)
GET  /api/v1/interviews                            → list your own interviews
GET  /api/v1/interviews/{id}                        → interview detail (owning candidate/recruiter)
POST /api/v1/interviews/{id}/generate-questions     → regenerate questions (recruiter, owner)
POST /api/v1/interviews/{id}/answers                → submit an answer (candidate, owner)
POST /api/v1/interviews/{id}/evaluate               → force re-evaluation (recruiter, owner)
GET  /api/v1/interviews/{id}/report                 → full report (owning candidate/recruiter)
POST /api/v1/speech/transcribe                      → transcribe a voice answer (candidate)

GET /api/v1/analytics/recruiter    → recruiter's dashboard stats + chart data
GET /api/v1/analytics/candidate    → candidate's dashboard stats + chart data

GET    /api/v1/admin/users              → list/filter users by role (admin)
GET    /api/v1/admin/users/{id}         → user detail (admin)
DELETE /api/v1/admin/users/{id}         → delete a user, not yourself (admin)
GET    /api/v1/admin/skills             → list all skills (admin)
POST   /api/v1/admin/skills             → create a skill (admin)
DELETE /api/v1/admin/skills/{id}        → delete a skill (admin)
GET    /api/v1/admin/jobs               → all jobs across all recruiters (admin)
GET    /api/v1/admin/stats              → system-wide statistics (admin)
GET    /api/v1/admin/audit-logs         → recent audit log entries (admin)
```

## 10. Testing

```bash
cd backend
pytest tests/ -v
```

The test suite uses an isolated SQLite database (shared across test files via
`tests/conftest.py`, so it never touches your real development database. 58 tests cover
registration, login, `/me`, the full resume pipeline (PDF/DOCX upload, skill/field
extraction, role enforcement, profile retrieval), job matching (CRUD, ownership
enforcement, applying, duplicate-application prevention, ranking order, ad-hoc match
scoring, recommendations), the LLM service layer (provider selection, graceful failure
handling with a real network call against a fake key, template-fallback paths), and the
full AI interview flow (starting an interview requires an existing application,
duplicate-interview prevention, per-answer evaluation, auto-completion after the last
question, the final report, forced re-evaluation, ownership enforcement on every
endpoint, and speech-to-text's honest `503` when unconfigured), analytics
(both dashboards' stats computed correctly against real activity, and scoped to only
the requesting recruiter's own jobs), and Phase 7 (the admin-role registration block,
admin panel CRUD and stats, audit log writes, login lockout via a real 5-attempt
sequence, an IP rate limit trip via a temporarily-lowered threshold with proper
cleanup so it doesn't affect other tests, and security headers) — using
in-memory-generated PDF/DOCX fixtures, no external test files or API keys needed.

## 11. Docker Setup

`docker-compose.yml` at the repo root brings up two services: `backend` (FastAPI on
:8000, SQLite database file persisted in the `ai_recruiter_data` named volume) and
`frontend` (the static HTML/CSS/JS site served by nginx on :8080). Uploaded resumes
persist to `backend/uploads` via a bind mount.

## 12. Deployment

For production:

- Set a strong, unique `JWT_SECRET` and restrict `CORS_ORIGINS` to your real frontend domain.
- Run the backend behind a proper ASGI process manager (e.g. `uvicorn` with `gunicorn` workers
  — see the commented `CMD` in `backend/Dockerfile`) or a managed container platform.
- SQLite is genuinely fine for small-to-medium deployments (single writer process, file
  on persistent storage/volume). If you outgrow it — multiple backend replicas, heavy
  concurrent write load — switch `DATABASE_URL` to a managed PostgreSQL instance; every
  model and migration already uses the dialect-agnostic `GUID` type (`app/core/db_types.py`),
  so no code changes are needed, just uncomment `psycopg2-binary` in `requirements.txt`
  and run `alembic upgrade head` against the new URL as part of your deploy step.
- Serve the frontend via a static host or CDN, or the provided nginx Dockerfile.
- Never bake secrets into images; inject them via environment variables / secret manager.

## 13. Project Structure Rules Followed

- Frontend and backend are fully separated, communicating only over REST.
- All secrets are environment-driven — nothing is hard-coded.
- API responses follow a consistent `{success, message, data}` / `{..., error_code}` shape.
- Passwords are hashed with bcrypt; JWTs are signed with a configurable secret and algorithm.
- Role-based access control is enforced via a reusable `require_role()` dependency.

## 14. Creating an Admin Account

Admin accounts can't be created through public registration (by design — see Phase 7
below). Create one via the bootstrap script, run with server/container access:

```bash
cd backend
python -m scripts.create_admin --name "Jane Admin" --email admin@example.com --password "SomeStrongPassword123"
```

Or interactively (omit flags to be prompted, with the password entered securely):

```bash
python -m scripts.create_admin
```

In Docker:

```bash
docker compose exec backend python -m scripts.create_admin --name "Jane Admin" --email admin@example.com --password "SomeStrongPassword123"
```

## 15. Next Phases

All 7 phases from the original plan are complete. Natural next steps beyond the spec:
a proper Redis-backed rate limiter for multi-instance deployments, refresh-token
rotation, and a frontend admin experience beyond the current tabbed panel (bulk actions,
pagination for large user/job lists).

## 16. Notes on the Semantic Matcher

`app/ml/semantic_matcher.py` tries three tiers, in order, and logs which one is active:

1. **Sentence-Transformers** (`all-MiniLM-L6-v2`) — best quality. Downloads from
   `huggingface.co` the first time it's used; needs normal internet access.
2. **spaCy `en_core_web_md`** word vectors — good quality, no network call at request
   time (just needs the model installed). Used automatically if tier 1 can't reach
   huggingface.co (e.g. a locked-down network).
3. **TF-IDF** cosine similarity — last resort, so a score is always returned.

If you have normal internet access, tier 1 will just work — no action needed. If you're
deploying somewhere that blocks huggingface.co, install `en_core_web_md` (see the
requirements.txt comment) to get tier 2's better fallback instead of tier 3.

## 17. Future Improvements

- Redis-backed rate limiting for multi-instance deployments (current limiter is in-memory,
  correct for a single process)
- Refresh-token rotation and revocation list
- Email verification and password reset flow
- Pagination for large user/job/audit-log lists in the admin panel
- CI pipeline already runs backend tests + frontend JS syntax checks on every PR
  (`.github/workflows/backend-tests.yml`) — extend with frontend E2E tests
