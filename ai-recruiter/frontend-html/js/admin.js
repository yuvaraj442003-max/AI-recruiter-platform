/**
 * admin.js — tabs for Users / Skills / Jobs / Audit Log, plus the
 * system-wide stat cards. Each tab loads its data lazily the first
 * time it's opened.
 */
(function () {
  const alertBox = document.getElementById("admin-alert");

  function showAlert(message, variant) {
    alertBox.textContent = message;
    alertBox.className = `alert alert-${variant} py-2`;
  }

  // --- Tabs ---
  document.querySelectorAll("[data-tab]").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll("[data-tab]").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      document.querySelectorAll(".tab-pane").forEach((p) => p.classList.add("d-none"));
      const pane = document.getElementById(`tab-${btn.dataset.tab}`);
      pane.classList.remove("d-none");
      loadTab(btn.dataset.tab);
    });
  });

  const loaded = { users: false, "weekly-questions": false, "recruiter-approvals": false, companies: false, fraud: false, skills: false, jobs: false, audit: false, "vector-db": false };

  function loadTab(tab) {
    if (tab === "users" && !loaded.users) loadUsers();
    if (tab === "weekly-questions" && !loaded["weekly-questions"]) loadWeeklyQuestions();
    if (tab === "recruiter-approvals" && !loaded["recruiter-approvals"]) loadPendingRecruiters();
    if (tab === "companies" && !loaded.companies) loadCompanies();
    if (tab === "fraud" && !loaded.fraud) loadFraudJobs();
    if (tab === "skills" && !loaded.skills) loadSkills();
    if (tab === "jobs" && !loaded.jobs) loadJobs();
    if (tab === "audit" && !loaded.audit) loadAuditLog();
    if (tab === "vector-db") loadVectorDB();
  }


  // --- Stats ---
  async function loadStats() {
    try {
      const res = await adminAPI.stats();
      const data = res.data;
      document.getElementById("stat-total-users").textContent = data.total_users;
      document.getElementById("stat-recruiters").textContent = data.total_recruiters;
      document.getElementById("stat-candidates").textContent = data.total_candidates;
      document.getElementById("stat-jobs").textContent = data.total_jobs;
      document.getElementById("stat-applications").textContent = data.total_applications;
      document.getElementById("stat-interview-completion").textContent =
        data.interview_completion_rate != null ? `${Math.round(data.interview_completion_rate)}%` : "—";
    } catch (err) {
      showAlert(err.message, "danger");
    }
  }

  // --- Pending Recruiter Approvals ---
  async function loadPendingRecruiters() {
    const wrapper = document.getElementById("recruiter-approvals-table");
    try {
      const res = await adminAPI.pendingRecruiters();
      const recruiters = res.data;
      loaded["recruiter-approvals"] = true;

      if (!recruiters.length) {
        wrapper.innerHTML = '<div class="text-success small p-3">No recruiter security verification approvals pending. All registered recruiters are verified.</div>';
        return;
      }

      const rows = recruiters
        .map(
          (r) => {
            let reasons = [];
            try { reasons = JSON.parse(r.verification_reasons || "[]"); } catch (e) {}
            return `
        <tr>
          <td>
            <div class="fw-bold text-dark">${r.name}</div>
            <div class="small text-muted">${r.email}</div>
            <div class="small text-muted">${r.job_title || ''} ${r.phone ? '• ' + r.phone : ''}</div>
          </td>
          <td>
            <div class="fw-bold text-primary">${r.company_name || 'Unspecified'}</div>
            <a href="${r.website || '#'}" target="_blank" class="small text-decoration-none">${r.website || 'No website'}</a>
            <div class="small text-muted">${r.company_location || ''} ${r.industry ? '• ' + r.industry : ''}</div>
          </td>
          <td>
            <span class="badge bg-warning text-dark mb-1">PENDING REVIEW</span>
            <div class="small text-secondary" style="max-width: 250px;">${reasons.join("<br/>") || 'Awaiting email/domain match check'}</div>
          </td>
          <td class="text-end text-nowrap">
            <button class="btn btn-sm btn-success approve-recruiter-btn me-1" data-user-id="${r.id}">Approve Account</button>
            <button class="btn btn-sm btn-outline-danger reject-recruiter-btn" data-user-id="${r.id}">Reject</button>
          </td>
        </tr>
      `;
          }
        )
        .join("");

      wrapper.innerHTML = `
        <div class="table-responsive">
          <table class="table table-sm table-hover mb-0">
            <thead><tr><th>Recruiter Details</th><th>Company Profile</th><th>Security Evaluation</th><th>Moderation</th></tr></thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      `;

      wrapper.querySelectorAll(".approve-recruiter-btn").forEach((btn) => {
        btn.addEventListener("click", async () => {
          try {
            await adminAPI.approveRecruiter(btn.dataset.userId);
            showAlert("Recruiter account approved successfully!", "success");
            loaded["recruiter-approvals"] = false;
            loadPendingRecruiters();
            loadStats();
          } catch (e) {
            showAlert(e.message, "danger");
          }
        });
      });

      wrapper.querySelectorAll(".reject-recruiter-btn").forEach((btn) => {
        btn.addEventListener("click", async () => {
          if (!confirm("Reject this recruiter registration request?")) return;
          try {
            await adminAPI.rejectRecruiter(btn.dataset.userId);
            showAlert("Recruiter account registration rejected.", "warning");
            loaded["recruiter-approvals"] = false;
            loadPendingRecruiters();
            loadStats();
          } catch (e) {
            showAlert(e.message, "danger");
          }
        });
      });
    } catch (err) {
      wrapper.innerHTML = `<div class="text-danger small">${err.message}</div>`;
    }
  }

  // --- Companies Verification ---
  async function loadCompanies() {
    const wrapper = document.getElementById("companies-table");
    try {
      const res = await adminAPI.companies();
      const companies = res.data;
      loaded.companies = true;

      if (!companies.length) {
        wrapper.innerHTML = '<div class="text-muted-custom small">No registered companies found.</div>';
        return;
      }

      const rows = companies
        .map(
          (c) => `
        <tr>
          <td class="fw-bold">${c.name}</td>
          <td>${c.cin_gstin || c.registration_number || '—'}</td>
          <td><a href="${c.website || '#'}" target="_blank" class="small text-decoration-none">${c.website || '—'}</a></td>
          <td>
            <span class="badge ${c.verification_status === 'government_verified' ? 'bg-success' : c.verification_status === 'domain_verified' ? 'bg-info' : 'bg-secondary'}">
              ${c.verification_status.replace('_', ' ').toUpperCase()}
            </span>
          </td>
          <td>${c.ssl_verified ? '🔒 Secure' : '⚠️ Unverified'}</td>
          <td class="text-end">
            <button class="btn btn-sm btn-outline-success verify-gov-btn me-1" data-company-id="${c.id}">Approve Gov Verification</button>
          </td>
        </tr>
      `
        )
        .join("");

      wrapper.innerHTML = `
        <div class="table-responsive">
          <table class="table table-sm table-hover mb-0">
            <thead><tr><th>Company</th><th>CIN / Registration</th><th>Website</th><th>Verification Status</th><th>SSL</th><th>Actions</th></tr></thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      `;

      wrapper.querySelectorAll(".verify-gov-btn").forEach((btn) => {
        btn.addEventListener("click", async () => {
          try {
            await adminAPI.verifyCompany(btn.dataset.companyId, "government_verified", "Verified by Super Admin");
            showAlert("Company verified as Government Verified!", "success");
            loaded.companies = false;
            loadCompanies();
            loadStats();
          } catch (e) {
            showAlert(e.message, "danger");
          }
        });
      });
    } catch (err) {
      wrapper.innerHTML = `<div class="text-danger small">${err.message}</div>`;
    }
  }

  // --- Fraud Alerts / Suspicious Jobs ---
  async function loadFraudJobs() {
    const wrapper = document.getElementById("fraud-table");
    try {
      const res = await adminAPI.suspiciousJobs();
      const jobs = res.data;
      loaded.fraud = true;

      if (!jobs.length) {
        wrapper.innerHTML = '<div class="text-success small">No high risk suspicious job postings detected. Platform is clean.</div>';
        return;
      }

      const rows = jobs
        .map(
          (j) => `
        <tr>
          <td class="fw-bold">${j.title}</td>
          <td>${j.company_name} <br/><span class="small text-muted">${j.recruiter_email || ''}</span></td>
          <td><span class="badge ${j.fraud_risk_level === 'HIGH' ? 'bg-danger' : 'bg-warning text-dark'}">${j.fraud_risk_score}/100 (${j.fraud_risk_level})</span></td>
          <td><span class="badge text-bg-light border">${j.status}</span></td>
          <td class="text-end">
            <button class="btn btn-sm btn-success approve-job-btn me-1" data-job-id="${j.id}">Approve (Publish)</button>
            <button class="btn btn-sm btn-danger flag-job-btn" data-job-id="${j.id}">Flag / Block</button>
          </td>
        </tr>
      `
        )
        .join("");

      wrapper.innerHTML = `
        <div class="table-responsive">
          <table class="table table-sm table-hover mb-0">
            <thead><tr><th>Job Title</th><th>Employer</th><th>Fraud Risk</th><th>Status</th><th>Moderation</th></tr></thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      `;

      wrapper.querySelectorAll(".approve-job-btn").forEach((btn) => {
        btn.addEventListener("click", async () => {
          try {
            await adminAPI.moderateJob(btn.dataset.jobId, "published");
            showAlert("Job approved and published successfully!", "success");
            loaded.fraud = false;
            loadFraudJobs();
            loadStats();
          } catch (e) {
            showAlert(e.message, "danger");
          }
        });
      });

      wrapper.querySelectorAll(".flag-job-btn").forEach((btn) => {
        btn.addEventListener("click", async () => {
          try {
            await adminAPI.moderateJob(btn.dataset.jobId, "flagged");
            showAlert("Job flagged and blocked from public view.", "warning");
            loaded.fraud = false;
            loadFraudJobs();
            loadStats();
          } catch (e) {
            showAlert(e.message, "danger");
          }
        });
      });
    } catch (err) {
      wrapper.innerHTML = `<div class="text-danger small">${err.message}</div>`;
    }
  }

  // --- Users ---
  async function loadUsers() {
    const wrapper = document.getElementById("users-table");
    const role = document.getElementById("user-role-filter").value;
    try {
      const res = await adminAPI.users(role || undefined);
      const users = res.data;
      loaded.users = true;

      if (!users.length) {
        wrapper.innerHTML = '<div class="text-muted-custom small">No users found.</div>';
        return;
      }

      const rows = users
        .map(
          (u) => `
        <tr>
          <td class="fw-medium">${u.name}</td>
          <td>${u.email}</td>
          <td><span class="badge text-bg-light border">${u.role}</span></td>
          <td>
            <span class="badge ${u.is_active !== false ? 'bg-success' : 'bg-danger'}">
              ${u.is_active !== false ? 'Active' : 'Suspended'}
            </span>
          </td>
          <td>${new Date(u.created_at).toLocaleDateString()}</td>
          <td class="text-end">
            <button class="btn btn-sm btn-outline-warning toggle-user-btn me-1" data-user-id="${u.id}">
              ${u.is_active !== false ? 'Suspend' : 'Activate'}
            </button>
            <button class="btn btn-sm btn-outline-danger delete-user-btn" data-user-id="${u.id}">Delete</button>
          </td>
        </tr>
      `
        )
        .join("");

      wrapper.innerHTML = `
        <div class="table-responsive">
          <table class="table table-sm table-hover mb-0">
            <thead><tr><th>Name</th><th>Email</th><th>Role</th><th>Status</th><th>Joined</th><th>Actions</th></tr></thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      `;

      wrapper.querySelectorAll(".toggle-user-btn").forEach((btn) => {
        btn.addEventListener("click", async () => {
          try {
            await adminAPI.toggleUserActive(btn.dataset.userId);
            loaded.users = false;
            loadUsers();
          } catch (err) {
            showAlert(err.message, "danger");
          }
        });
      });

      wrapper.querySelectorAll(".delete-user-btn").forEach((btn) => {
        btn.addEventListener("click", async () => {
          if (!confirm("Delete this user? This cannot be undone.")) return;
          try {
            await adminAPI.deleteUser(btn.dataset.userId);
            loaded.users = false;
            loadUsers();
            loadStats();
          } catch (err) {
            showAlert(err.message, "danger");
          }
        });
      });
    } catch (err) {
      wrapper.innerHTML = `<div class="text-danger small">${err.message}</div>`;
    }
  }
  document.getElementById("user-role-filter").addEventListener("change", () => {
    loaded.users = false;
    loadUsers();
  });

  // --- Skills ---
  async function loadSkills() {
    const wrapper = document.getElementById("skills-table");
    try {
      const res = await adminAPI.skills();
      const skills = res.data;
      loaded.skills = true;

      if (!skills.length) {
        wrapper.innerHTML = '<div class="text-muted-custom small">No skills yet.</div>';
        return;
      }

      const rows = skills
        .map(
          (s) => `
        <tr>
          <td class="fw-medium">${s.skill_name}</td>
          <td>${s.category || "—"}</td>
          <td class="text-end">
            <button class="btn btn-sm btn-outline-danger delete-skill-btn" data-skill-id="${s.id}">Delete</button>
          </td>
        </tr>
      `
        )
        .join("");

      wrapper.innerHTML = `
        <div class="table-responsive">
          <table class="table table-sm table-hover mb-0">
            <thead><tr><th>Skill</th><th>Category</th><th></th></tr></thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      `;

      wrapper.querySelectorAll(".delete-skill-btn").forEach((btn) => {
        btn.addEventListener("click", async () => {
          try {
            await adminAPI.deleteSkill(btn.dataset.skillId);
            loaded.skills = false;
            loadSkills();
          } catch (err) {
            showAlert(err.message, "danger");
          }
        });
      });
    } catch (err) {
      wrapper.innerHTML = `<div class="text-danger small">${err.message}</div>`;
    }
  }

  document.getElementById("skill-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = document.getElementById("skill-name-input").value.trim();
    const category = document.getElementById("skill-category-input").value.trim() || null;
    if (!name) return;

    try {
      await adminAPI.createSkill(name, category);
      document.getElementById("skill-name-input").value = "";
      document.getElementById("skill-category-input").value = "";
      loaded.skills = false;
      loadSkills();
    } catch (err) {
      showAlert(err.message, "danger");
    }
  });

  // --- Jobs ---
  async function loadJobs() {
    const wrapper = document.getElementById("jobs-table");
    try {
      const res = await adminAPI.jobs();
      const jobs = res.data;
      loaded.jobs = true;

      if (!jobs.length) {
        wrapper.innerHTML = '<div class="text-muted-custom small">No jobs posted yet.</div>';
        return;
      }

      const rows = jobs
        .map(
          (j) => `
        <tr>
          <td class="fw-medium">${j.title}</td>
          <td>${j.recruiter_name || "—"}</td>
          <td><span class="badge text-bg-light border">${j.status}</span></td>
          <td>${j.applications_count}</td>
          <td>${new Date(j.created_at).toLocaleDateString()}</td>
        </tr>
      `
        )
        .join("");

      wrapper.innerHTML = `
        <div class="table-responsive">
          <table class="table table-sm table-hover mb-0">
            <thead><tr><th>Job</th><th>Recruiter</th><th>Status</th><th>Applications</th><th>Posted</th></tr></thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      `;
    } catch (err) {
      wrapper.innerHTML = `<div class="text-danger small">${err.message}</div>`;
    }
  }

  // --- Audit log ---
  async function loadAuditLog() {
    const wrapper = document.getElementById("audit-table");
    try {
      const res = await adminAPI.auditLogs(100);
      const logs = res.data;
      loaded.audit = true;

      if (!logs.length) {
        wrapper.innerHTML = '<div class="text-muted-custom small">No audit log entries yet.</div>';
        return;
      }

      const rows = logs
        .map(
          (l) => `
        <tr>
          <td class="text-nowrap small">${new Date(l.created_at).toLocaleString()}</td>
          <td><span class="badge text-bg-light border">${l.action}</span></td>
          <td class="small text-muted-custom">${l.details || "—"}</td>
          <td class="small text-muted-custom">${l.ip_address || "—"}</td>
        </tr>
      `
        )
        .join("");

      wrapper.innerHTML = `
        <div class="table-responsive">
          <table class="table table-sm table-hover mb-0">
            <thead><tr><th>Time</th><th>Action</th><th>Details</th><th>IP</th></tr></thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      `;
    } catch (err) {
      wrapper.innerHTML = `<div class="text-danger small">${err.message}</div>`;
    }
  }

  async function loadSystemStatus() {
    const redisBadge = document.getElementById("redis-live-badge");
    const dbBadge = document.getElementById("db-live-badge");
    if (!redisBadge && !dbBadge) return;

    try {
      const res = await systemAPI.getStatus();
      const info = res?.data || {};

      if (redisBadge && info.redis_cache) {
        const rc = info.redis_cache;
        if (rc.is_live || rc.backend_type === "redis_live") {
          redisBadge.className = "badge bg-success-subtle text-success border border-success-subtle px-2 py-1";
          redisBadge.innerHTML = `🟢 Redis Live: ${rc.host}:${rc.port} (${rc.keys_cached || 0} keys)`;
        } else if (rc.backend_type === "fakeredis_fallback") {
          redisBadge.className = "badge bg-warning-subtle text-dark border border-warning-subtle px-2 py-1";
          redisBadge.innerHTML = `🟡 Redis: Fallback (In-Memory)`;
        } else {
          redisBadge.className = "badge bg-secondary-subtle text-muted border px-2 py-1";
          redisBadge.innerHTML = `Redis: ${rc.backend_type || "Disabled"}`;
        }
      }

      if (dbBadge && info.databases) {
        const db = info.databases;
        const engineName = (db.active_engine || "unknown").toUpperCase();
        if (db.connected) {
          dbBadge.className = "badge bg-primary-subtle text-primary border border-primary-subtle px-2 py-1";
          dbBadge.innerHTML = `🗄️ DB: ${engineName} (Connected)`;
        } else {
          dbBadge.className = "badge bg-danger-subtle text-danger border border-danger-subtle px-2 py-1";
          dbBadge.innerHTML = `⚠️ DB: ${engineName} (Disconnected)`;
        }
      }
    } catch (err) {
      if (redisBadge) {
        redisBadge.className = "badge bg-secondary-subtle text-secondary border px-2 py-1";
        redisBadge.textContent = "Redis: Status Unavailable";
      }
    }
  }

  function escapeHtml(str) {
    if (str == null) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // --- Weekly Placement Questions & Rotations ---
  async function loadWeeklyQuestions() {
    const wrapper = document.getElementById("weekly-questions-table");
    if (!wrapper) return;
    wrapper.innerHTML = '<div class="text-muted-custom small p-2">⏳ Loading question bank…</div>';

    const qType = document.getElementById("weekly-filter-type")?.value || "aptitude";
    const qDiff = document.getElementById("weekly-filter-difficulty")?.value || "";
    const qStat = document.getElementById("weekly-filter-status")?.value || "";

    try {
      const params = { type: qType };
      if (qDiff) params.difficulty = qDiff;
      if (qStat) params.status = qStat;

      const res = await api.weekly.adminListQuestions(params);
      loaded["weekly-questions"] = true;
      updatePdfRagStatus();

      const questions = res?.data?.questions || [];
      if (!questions.length) {
        wrapper.innerHTML = `<div class="text-muted small p-3 text-center">No ${escapeHtml(qType)} questions found matching your filter criteria.</div>`;
        return;
      }

      const rows = questions.map(q => {
        const isApt = (q.type === "aptitude");
        const titleText = isApt ? q.question : q.title;
        const subtopicText = isApt ? q.subtopic : (q.category || "Algorithms");
        const diffBadge = q.difficulty?.toLowerCase() === "easy"
          ? 'bg-success'
          : (q.difficulty?.toLowerCase() === "hard" ? 'bg-danger' : 'bg-warning text-dark');
        const statusBadge = q.status === "approved"
          ? '<span class="badge bg-success">Approved</span>'
          : '<span class="badge bg-warning text-dark">Pending Review</span>';
        const weekTag = q.week_assigned
          ? `<span class="badge bg-primary">${escapeHtml(q.week_assigned)}</span>`
          : '<span class="badge bg-secondary">Unassigned</span>';

        return `
          <tr>
            <td>
              <span class="badge ${isApt ? 'bg-info text-dark' : 'bg-primary'} mb-1">${isApt ? 'Aptitude MCQ' : 'Coding Challenge'}</span>
              <div class="small fw-semibold text-dark">${escapeHtml(subtopicText)}</div>
              ${q.company_tag ? `<div class="small text-muted">🏷️ ${escapeHtml(q.company_tag)}</div>` : ''}
            </td>
            <td style="max-width: 320px;">
              <div class="small fw-bold text-dark text-truncate mb-1" title="${escapeHtml(titleText)}">${escapeHtml(titleText)}</div>
              ${isApt && q.explanation ? `<div class="small text-muted text-truncate" title="${escapeHtml(q.explanation)}">💡 ${escapeHtml(q.explanation)}</div>` : ''}
              ${!isApt && q.description ? `<div class="small text-muted text-truncate" title="${escapeHtml(q.description)}">${escapeHtml(q.description)}</div>` : ''}
            </td>
            <td>
              <span class="badge ${diffBadge} text-capitalize">${escapeHtml(q.difficulty || 'medium')}</span>
            </td>
            <td>${statusBadge}</td>
            <td>${weekTag}</td>
            <td class="text-end text-nowrap">
              ${isApt && q.status !== 'approved' ? `<button class="btn btn-sm btn-outline-success approve-weekly-q-btn me-1" data-id="${q.id}" data-type="aptitude">Approve</button>` : ''}
              <button class="btn btn-sm btn-outline-danger delete-weekly-q-btn" data-id="${q.id}" data-type="${isApt ? 'aptitude' : 'coding'}">Delete</button>
            </td>
          </tr>
        `;
      }).join("");

      wrapper.innerHTML = `
        <div class="table-responsive">
          <table class="table table-sm table-hover align-middle mb-0">
            <thead>
              <tr>
                <th>Type &amp; Domain</th>
                <th>Statement / Title</th>
                <th>Difficulty</th>
                <th>Status</th>
                <th>Week Assigned</th>
                <th class="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      `;

      wrapper.querySelectorAll(".approve-weekly-q-btn").forEach(btn => {
        btn.addEventListener("click", async () => {
          try {
            await api.weekly.adminApproveAptitude(btn.dataset.id);
            showAlert("Question approved for weekly challenge pool!", "success");
            loadWeeklyQuestions();
          } catch (e) {
            showAlert("Approval failed: " + e.message, "danger");
          }
        });
      });

      wrapper.querySelectorAll(".delete-weekly-q-btn").forEach(btn => {
        btn.addEventListener("click", async () => {
          if (!confirm("Are you sure you want to permanently delete this question?")) return;
          try {
            if (btn.dataset.type === "aptitude") {
              await api.weekly.adminDeleteAptitude(btn.dataset.id);
            } else {
              await api.weekly.adminDeleteCoding(btn.dataset.id);
            }
            showAlert("Question deleted successfully.", "warning");
            loadWeeklyQuestions();
          } catch (e) {
            showAlert("Deletion failed: " + e.message, "danger");
          }
        });
      });
    } catch (err) {
      wrapper.innerHTML = `<div class="text-danger small p-2">Error loading questions: ${escapeHtml(err.message)}</div>`;
    }
  }

  // Hook filters & admin actions
  const filterWeeklyBtn = document.getElementById("btn-filter-weekly");
  if (filterWeeklyBtn) {
    filterWeeklyBtn.addEventListener("click", () => {
      loadWeeklyQuestions();
    });
  }

  async function updatePdfRagStatus() {
    const badge = document.getElementById("pdf-rag-status-badge");
    const text = document.getElementById("pdf-rag-status-text");
    if (!badge || !text) return;

    try {
      const res = await api.weekly.adminGetPdfRagStatus();
      const d = res?.data || {};
      if (d.pdf_found) {
        badge.className = "badge bg-success ms-1";
        badge.textContent = `PDF Ready (${d.qdrant_points_count || 0} chunks in Qdrant)`;
        text.textContent = `Focus: ${d.focus_topic} (${d.chapters} • ${d.current_week_code})`;
      } else {
        badge.className = "badge bg-warning text-dark ms-1";
        badge.textContent = "PDF Not Found";
        text.textContent = "Ensure RS Aggarwal Reasoning PDF is placed in dataset folder.";
      }
    } catch (e) {
      badge.className = "badge bg-secondary ms-1";
      badge.textContent = "Offline / Disabled";
    }
  }

  const forceRotateBtn = document.getElementById("btn-force-rotate");
  if (forceRotateBtn) {
    forceRotateBtn.addEventListener("click", async () => {
      if (!confirm("Trigger immediate weekly question rotation? This will select new aptitude and coding sets for candidates for the current week.")) return;
      try {
        const res = await api.weekly.adminRotateNow();
        showAlert(`✅ Weekly rotation successful! New challenges active for ${res.data.week_code}.`, "success");
        loadWeeklyQuestions();
        updatePdfRagStatus();
      } catch (e) {
        showAlert("Rotation error: " + e.message, "danger");
      }
    });
  }

  const btnIndexPdf = document.getElementById("btn-index-pdf-qdrant");
  if (btnIndexPdf) {
    btnIndexPdf.addEventListener("click", async () => {
      btnIndexPdf.disabled = true;
      btnIndexPdf.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span> Indexing PDF...';
      try {
        const res = await api.weekly.adminIndexPdf({ max_pages: 180, force: true });
        showAlert(`✅ ${res.message || "Reasoning PDF indexed into Qdrant!"} (${res.data?.points_count || 0} chunks)`, "success");
        updatePdfRagStatus();
      } catch (err) {
        showAlert("Failed to index PDF: " + err.message, "danger");
      } finally {
        btnIndexPdf.disabled = false;
        btnIndexPdf.innerHTML = '📥 Index PDF to Qdrant';
      }
    });
  }

  const btnRotateFromPdf = document.getElementById("btn-rotate-from-pdf");
  if (btnRotateFromPdf) {
    btnRotateFromPdf.addEventListener("click", async () => {
      btnRotateFromPdf.disabled = true;
      btnRotateFromPdf.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span> Generating from PDF...';
      try {
        const res = await api.weekly.adminRotateFromPdf();
        showAlert(`⚡ ${res.message || "Weekly challenge updated from PDF via Qdrant!"} Focus: ${res.data?.focus_topic}`, "success");
        updatePdfRagStatus();
        loadWeeklyQuestions();
      } catch (err) {
        showAlert("Failed to update weekly from PDF: " + err.message, "danger");
      } finally {
        btnRotateFromPdf.disabled = false;
        btnRotateFromPdf.innerHTML = '⚡ Update Weekly from PDF';
      }
    });
  }

  const formAddAptitude = document.getElementById("form-add-aptitude");
  if (formAddAptitude) {
    formAddAptitude.addEventListener("submit", async (e) => {
      e.preventDefault();
      try {
        const payload = {
          topic_slug: document.getElementById("apt-topic-slug").value,
          subtopic: document.getElementById("apt-subtopic").value,
          difficulty: document.getElementById("apt-difficulty").value,
          company_tag: document.getElementById("apt-company-tag").value || "General",
          status: document.getElementById("apt-status").value,
          question: document.getElementById("apt-question").value,
          options: [
            document.getElementById("apt-opt-0").value,
            document.getElementById("apt-opt-1").value,
            document.getElementById("apt-opt-2").value,
            document.getElementById("apt-opt-3").value,
          ],
          correct_option_index: parseInt(document.getElementById("apt-correct-idx").value, 10),
          explanation: document.getElementById("apt-explanation").value,
        };
        await api.weekly.adminCreateAptitude(payload);
        showAlert("Aptitude MCQ added successfully!", "success");
        formAddAptitude.reset();
        const modalEl = document.getElementById("modal-add-aptitude");
        const modalInstance = bootstrap.Modal.getInstance(modalEl);
        if (modalInstance) modalInstance.hide();
        loadWeeklyQuestions();
      } catch (err) {
        showAlert("Failed to save question: " + err.message, "danger");
      }
    });
  }

  // --- Aptitude Semantic Duplicate Checker ---
  const btnCheckDup = document.getElementById("btn-check-apt-duplicate");
  if (btnCheckDup) {
    btnCheckDup.addEventListener("click", async () => {
      const qText = (document.getElementById("apt-question").value || "").trim();
      const feedback = document.getElementById("apt-dup-feedback");
      if (!qText) {
        feedback.className = "alert alert-warning py-1 px-2 mt-1 small";
        feedback.textContent = "Please enter the question statement first.";
        feedback.classList.remove("d-none");
        return;
      }
      btnCheckDup.disabled = true;
      btnCheckDup.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Checking…';
      try {
        const res = await window.vectorAPI.checkDuplicate({
          text: qText,
          threshold: 0.85,
          collection: "aptitude_questions",
        });
        feedback.classList.remove("d-none");
        if (res.data && res.data.is_duplicate) {
          feedback.className = "alert alert-danger py-1 px-2 mt-1 small";
          feedback.innerHTML = `⚠️ Near duplicate detected (${(res.data.highest_similarity * 100).toFixed(1)}% match): <em>${escapeHtml(res.data.duplicate_document.text_snippet || '')}</em>`;
        } else {
          feedback.className = "alert alert-success py-1 px-2 mt-1 small";
          feedback.textContent = "✅ Original question! No semantic duplicates detected in vector DB.";
        }
      } catch (e) {
        feedback.className = "alert alert-danger py-1 px-2 mt-1 small";
        feedback.textContent = "Duplicate check error: " + e.message;
        feedback.classList.remove("d-none");
      } finally {
        btnCheckDup.disabled = false;
        btnCheckDup.innerHTML = '🔍 Check Semantic Duplicates';
      }
    });
  }

  // --- Quick Vector Sync for Aptitude ---
  const btnQuickSyncApt = document.getElementById("btn-quick-sync-aptitude");
  if (btnQuickSyncApt) {
    btnQuickSyncApt.addEventListener("click", async () => {
      btnQuickSyncApt.disabled = true;
      btnQuickSyncApt.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Syncing…';
      try {
        const res = await (window.aptitudeAPI ? window.aptitudeAPI.syncVectors() : api.post("/aptitude/sync-vectors", {}));
        showAlert(`✅ Aptitude vector database synchronized! Total questions indexed: ${res.data.vectors_indexed}`, "success");
        if (loaded["vector-db"]) loadVectorDB();
      } catch (e) {
        showAlert("Vector sync error: " + e.message, "danger");
      } finally {
        btnQuickSyncApt.disabled = false;
        btnQuickSyncApt.innerHTML = '⚡ Sync Vectors';
      }
    });
  }

  // --- Aptitude Topic Management ---
  async function loadTopicsList() {
    const tbody = document.getElementById("topics-list-tbody");
    if (!tbody) return;
    try {
      const res = await (window.aptitudeAPI ? window.aptitudeAPI.getTopics() : api.get("/aptitude/topics"));
      const topics = res.data || [];
      if (topics.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted small py-3">No topics configured yet.</td></tr>';
        return;
      }
      tbody.innerHTML = topics.map(t => `
        <tr>
          <td class="fs-5">${escapeHtml(t.icon || '📊')}</td>
          <td><strong>${escapeHtml(t.name)}</strong><br><small class="text-muted">${escapeHtml(t.description || '')}</small></td>
          <td><code>${escapeHtml(t.slug)}</code></td>
          <td><span class="badge bg-primary-subtle text-primary border">${t.question_count || 0} questions</span></td>
          <td class="text-end">
            <button class="btn btn-xs btn-outline-primary me-1" onclick="editTopic('${t.id}', '${escapeJs(t.name)}', '${escapeJs(t.slug)}', '${escapeJs(t.description || '')}', '${escapeJs(t.icon || '📊')}', ${t.order_index || 0})">✏️ Edit</button>
            <button class="btn btn-xs btn-outline-danger" onclick="deleteTopic('${t.id}', '${escapeJs(t.name)}')">🗑️</button>
          </td>
        </tr>
      `).join("");

      // Also refresh topic select dropdown in add question modal
      const aptTopicSelect = document.getElementById("apt-topic-slug");
      if (aptTopicSelect) {
        aptTopicSelect.innerHTML = topics.map(t => `<option value="${escapeHtml(t.slug)}">${escapeHtml(t.icon || '')} ${escapeHtml(t.name)}</option>`).join("");
      }
    } catch (err) {
      tbody.innerHTML = `<tr><td colspan="5" class="text-danger small py-3">Failed to load topics: ${escapeHtml(err.message)}</td></tr>`;
    }
  }

  window.editTopic = function(id, name, slug, desc, icon, order) {
    document.getElementById("topic-edit-id").value = id;
    document.getElementById("topic-name").value = name;
    document.getElementById("topic-desc").value = desc;
    document.getElementById("topic-icon").value = icon;
    document.getElementById("topic-order").value = order;
    document.getElementById("topic-form-heading").textContent = "✏️ Edit Topic: " + name;
    const cancelBtn = document.getElementById("btn-cancel-topic-edit");
    if (cancelBtn) cancelBtn.classList.remove("d-none");
    document.getElementById("btn-save-topic").textContent = "Update Topic";
  };

  window.deleteTopic = async function(id, name) {
    if (!confirm(`Are you sure you want to delete topic "${name}"?`)) return;
    try {
      if (window.aptitudeAPI) await window.aptitudeAPI.deleteTopic(id);
      else await api.delete(`/aptitude/topics/${id}`);
      showAlert(`Topic "${name}" deleted successfully.`, "success");
      loadTopicsList();
    } catch (err) {
      showAlert("Failed to delete topic: " + err.message, "danger");
    }
  };

  const btnCancelTopicEdit = document.getElementById("btn-cancel-topic-edit");
  if (btnCancelTopicEdit) {
    btnCancelTopicEdit.addEventListener("click", () => {
      document.getElementById("form-manage-topic").reset();
      document.getElementById("topic-edit-id").value = "";
      document.getElementById("topic-form-heading").textContent = "➕ Add New Aptitude Topic";
      document.getElementById("btn-save-topic").textContent = "Save Topic";
      btnCancelTopicEdit.classList.add("d-none");
    });
  }

  const formManageTopic = document.getElementById("form-manage-topic");
  if (formManageTopic) {
    formManageTopic.addEventListener("submit", async (e) => {
      e.preventDefault();
      const topicId = document.getElementById("topic-edit-id").value;
      const payload = {
        name: document.getElementById("topic-name").value.trim(),
        description: document.getElementById("topic-desc").value.trim(),
        icon: document.getElementById("topic-icon").value.trim() || "📊",
        order_index: parseInt(document.getElementById("topic-order").value, 10) || 0,
      };

      try {
        if (topicId) {
          if (window.aptitudeAPI) await window.aptitudeAPI.updateTopic(topicId, payload);
          else await api.put(`/aptitude/topics/${topicId}`, payload);
          showAlert("Topic updated successfully!", "success");
        } else {
          if (window.aptitudeAPI) await window.aptitudeAPI.createTopic(payload);
          else await api.post("/aptitude/topics", payload);
          showAlert("Topic created successfully!", "success");
        }
        formManageTopic.reset();
        document.getElementById("topic-edit-id").value = "";
        document.getElementById("topic-form-heading").textContent = "➕ Add New Aptitude Topic";
        document.getElementById("btn-save-topic").textContent = "Save Topic";
        if (btnCancelTopicEdit) btnCancelTopicEdit.classList.add("d-none");
        loadTopicsList();
      } catch (err) {
        showAlert("Failed to save topic: " + err.message, "danger");
      }
    });
  }

  const modalManageTopics = document.getElementById("modal-manage-topics");
  if (modalManageTopics) {
    modalManageTopics.addEventListener("show.bs.modal", () => {
      loadTopicsList();
    });
  }

  const formAddCoding = document.getElementById("form-add-coding");
  if (formAddCoding) {
    formAddCoding.addEventListener("submit", async (e) => {
      e.preventDefault();
      try {
        let publicTcs = [];
        let hiddenTcs = [];
        try {
          publicTcs = JSON.parse(document.getElementById("code-public-tcs").value);
        } catch {
          throw new Error("Public test cases must be a valid JSON array.");
        }
        try {
          hiddenTcs = JSON.parse(document.getElementById("code-hidden-tcs").value);
        } catch {
          throw new Error("Hidden test cases must be a valid JSON array.");
        }

        const payload = {
          title: document.getElementById("code-title").value,
          category: document.getElementById("code-category").value,
          difficulty: document.getElementById("code-difficulty").value,
          status: document.getElementById("code-status").value,
          description: document.getElementById("code-description").value,
          constraints: document.getElementById("code-constraints").value,
          programming_languages: ["python", "javascript", "java", "cpp"],
          starter_code: {
            python: document.getElementById("code-starter").value || "def solution():\n    pass\n"
          },
          public_test_cases: publicTcs,
          hidden_test_cases: hiddenTcs,
        };

        await api.weekly.adminCreateCoding(payload);
        showAlert("Coding Challenge added successfully!", "success");
        formAddCoding.reset();
        const modalEl = document.getElementById("modal-add-coding");
        const modalInstance = bootstrap.Modal.getInstance(modalEl);
        if (modalInstance) modalInstance.hide();
        loadWeeklyQuestions();
      } catch (err) {
        showAlert("Failed to save coding question: " + err.message, "danger");
      }
    });
  }

  const btnTriggerAiGen = document.getElementById("btn-trigger-ai-gen");
  if (btnTriggerAiGen) {
    btnTriggerAiGen.addEventListener("click", async () => {
      const resBox = document.getElementById("ai-gen-result");
      const topic = document.getElementById("ai-topic-slug").value;
      const difficulty = document.getElementById("ai-difficulty").value;
      resBox.className = "alert alert-warning small py-2 font-monospace";
      resBox.textContent = "⏳ Generating placement question with automated validation checks...";
      resBox.classList.remove("d-none");
      btnTriggerAiGen.disabled = true;

      try {
        const res = await api.weekly.adminGenerateAIQuestion({ topic_slug: topic, difficulty: difficulty });
        if (res.success) {
          resBox.className = "alert alert-success small py-2";
          resBox.innerHTML = `<strong>✅ Generated &amp; Validated:</strong><br/>"${escapeHtml(res.data.question)}"<br/><small class="text-muted">Subtopic: ${escapeHtml(res.data.subtopic)} | Difficulty: ${escapeHtml(res.data.difficulty)}</small>`;
          showAlert("AI question generated and added to question bank!", "success");
          loadWeeklyQuestions();
        } else {
          resBox.className = "alert alert-danger small py-2";
          resBox.textContent = "Failed: " + res.message;
        }
      } catch (err) {
        resBox.className = "alert alert-danger small py-2";
        resBox.textContent = "Generation error: " + err.message;
      } finally {
        btnTriggerAiGen.disabled = false;
      }
    });
  }

  // --- Vector Database (Qdrant) ---
  const collectionDescriptions = {
    resumes: "Candidate Resumes & Extracted Skills",
    jobs: "Published & Active Job Postings",
    aptitude_questions: "Psychometric & Aptitude Question Bank",
    coding_problems: "Algorithmic Challenges & Problems",
    interview_questions: "AI Mock & Technical Interview Question Bank",
    learning_resources: "Campus Roadmaps & Placement Guides",
  };

  async function loadVectorDB() {
    const statusBadge = document.getElementById("vec-status-badge");
    const modeEl = document.getElementById("vec-mode");
    const modelEl = document.getElementById("vec-model");
    const dimEl = document.getElementById("vec-dim");
    const tbody = document.getElementById("vector-collections-tbody");

    if (!statusBadge || !tbody) return;

    try {
      const res = await window.vectorAPI.health();
      const d = res.data;
      if (d.available) {
        statusBadge.innerHTML = '<span class="badge bg-success">Operational</span>';
      } else {
        statusBadge.innerHTML = '<span class="badge bg-warning text-dark">Unavailable / Fallback</span>';
      }
      modeEl.textContent = (d.mode || "unknown").replace("_", " ").toUpperCase();
      modelEl.textContent = d.embedding_model || "all-MiniLM-L6-v2";
      dimEl.textContent = d.vector_dimension || 384;

      const colls = d.collections || {};
      const keys = Object.keys(colls);
      if (keys.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted py-3">No collections initialized. Click "Synchronize Relational DB" to index.</td></tr>';
        return;
      }

      tbody.innerHTML = keys
        .map((k) => {
          const info = colls[k];
          const desc = collectionDescriptions[k] || "Domain Entities";
          const count = info.points_count != null ? info.points_count.toLocaleString() : "0";
          const status = info.exists
            ? '<span class="badge bg-success-subtle text-success border border-success-subtle">Ready</span>'
            : '<span class="badge bg-secondary">Not Created</span>';
          return `
            <tr>
              <td class="fw-semibold font-monospace">${escapeHtml(k)}</td>
              <td class="small text-muted">${escapeHtml(desc)}</td>
              <td class="small font-monospace">Cosine (384-dim)</td>
              <td class="fw-bold">${count}</td>
              <td>${status}</td>
            </tr>
          `;
        })
        .join("");

      loaded["vector-db"] = true;
    } catch (err) {
      statusBadge.innerHTML = '<span class="badge bg-danger">Error</span>';
      tbody.innerHTML = `<tr><td colspan="5" class="text-danger py-3">Failed to load Vector DB status: ${escapeHtml(err.message)}</td></tr>`;
    }
  }

  const btnSyncVec = document.getElementById("btn-sync-vector-db");
  if (btnSyncVec) {
    btnSyncVec.addEventListener("click", async () => {
      const feedback = document.getElementById("vec-sync-feedback");
      btnSyncVec.disabled = true;
      btnSyncVec.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span> Synchronizing…';
      feedback.className = "alert alert-info py-2 small mb-3";
      feedback.textContent = "Syncing relational database records to Qdrant vector database…";
      feedback.classList.remove("d-none");

      try {
        const res = await window.vectorAPI.sync(false);
        feedback.className = "alert alert-success py-2 small mb-3";
        const c = (res.data && res.data.counts) || {};
        feedback.textContent = `Sync completed! Indexed: ${c.jobs || 0} jobs, ${c.resumes || 0} resumes, ${c.aptitude_questions || 0} aptitude questions, ${c.coding_problems || 0} coding challenges, ${c.interview_questions || 0} interview questions, ${c.learning_resources || 0} study materials.`;
        loadVectorDB();
      } catch (err) {
        feedback.className = "alert alert-danger py-2 small mb-3";
        feedback.textContent = "Vector synchronization failed: " + err.message;
      } finally {
        btnSyncVec.disabled = false;
        btnSyncVec.textContent = "⚡ Synchronize Relational DB";
      }
    });
  }

  const btnRefreshVec = document.getElementById("btn-refresh-vector-health");
  if (btnRefreshVec) {
    btnRefreshVec.addEventListener("click", () => {
      loadVectorDB();
    });
  }

  const formVecSearch = document.getElementById("form-vector-search");
  if (formVecSearch) {
    formVecSearch.addEventListener("submit", async (e) => {
      e.preventDefault();
      const coll = document.getElementById("vec-search-collection").value;
      const query = document.getElementById("vec-search-query").value.trim();
      const resultsContainer = document.getElementById("vector-search-results");
      const tbody = document.getElementById("vector-search-results-tbody");
      const btnSearch = document.getElementById("btn-vector-search-run");

      if (!query) return;

      btnSearch.disabled = true;
      btnSearch.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>';

      try {
        const res = await window.vectorAPI.search({
          collection: coll,
          query: query,
          limit: 5,
        });

        resultsContainer.classList.remove("d-none");
        const list = (res.data && res.data.results) || [];
        if (list.length === 0) {
          tbody.innerHTML = '<tr><td colspan="3" class="text-center text-muted py-3">No matching documents found above similarity threshold.</td></tr>';
        } else {
          tbody.innerHTML = list
            .map((item) => {
              const pct = item.similarity_pct || 0;
              const badgeClass = pct >= 80 ? "bg-success" : pct >= 60 ? "bg-primary" : "bg-secondary";
              const snippet = item.payload.text_snippet || JSON.stringify(item.payload);
              return `
                <tr>
                  <td><span class="badge ${badgeClass}">${pct}% Match</span></td>
                  <td class="font-monospace small">${item.score}</td>
                  <td>
                    <div class="small fw-semibold mb-1">${escapeHtml(item.payload.title || item.payload.topic_name || item.payload.headline || item.id)}</div>
                    <div class="text-muted small font-monospace text-truncate" style="max-width: 500px;">${escapeHtml(snippet)}</div>
                  </td>
                </tr>
              `;
            })
            .join("");
        }
      } catch (err) {
        resultsContainer.classList.remove("d-none");
        tbody.innerHTML = `<tr><td colspan="3" class="text-danger py-2">Search failed: ${escapeHtml(err.message)}</td></tr>`;
      } finally {
        btnSearch.disabled = false;
        btnSearch.textContent = "🔍 Search";
      }
    });
  }

  document.addEventListener("ar:auth-ready", () => {
    loadSystemStatus();
    loadStats();
    loadUsers();
  });
})();
