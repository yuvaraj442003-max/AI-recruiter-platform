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

  const loaded = { users: false, "recruiter-approvals": false, companies: false, fraud: false, skills: false, jobs: false, audit: false };

  function loadTab(tab) {
    if (tab === "users" && !loaded.users) loadUsers();
    if (tab === "recruiter-approvals" && !loaded["recruiter-approvals"]) loadPendingRecruiters();
    if (tab === "companies" && !loaded.companies) loadCompanies();
    if (tab === "fraud" && !loaded.fraud) loadFraudJobs();
    if (tab === "skills" && !loaded.skills) loadSkills();
    if (tab === "jobs" && !loaded.jobs) loadJobs();
    if (tab === "audit" && !loaded.audit) loadAuditLog();
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

  document.addEventListener("ar:auth-ready", () => {
    loadStats();
    loadUsers();
  });
})();
