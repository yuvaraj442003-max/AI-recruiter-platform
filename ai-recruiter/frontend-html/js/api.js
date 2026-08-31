/**
 * api.js — thin fetch() wrapper for the AI Recruiter backend.
 * Handles the base URL, attaching the JWT, and normalizing errors
 * so every page can call `await api.post(...)` the same way.
 */
const API_BASE_URL = "http://localhost:8000/api/v1";

const TOKEN_KEYS = {
  access: "ar_access_token",
  refresh: "ar_refresh_token",
  user: "ar_user",
};

const memoryStore = {};

const safeStorage = {
  getItem(key) {
    try {
      return localStorage.getItem(key) || memoryStore[key] || null;
    } catch {
      return memoryStore[key] || null;
    }
  },
  setItem(key, val) {
    memoryStore[key] = val;
    try {
      localStorage.setItem(key, val);
    } catch (e) {
      // localStorage blocked by browser tracking prevention or file:// restriction — falling back to memoryStore
    }
  },
  removeItem(key) {
    delete memoryStore[key];
    try {
      localStorage.removeItem(key);
    } catch (e) { }
  }
};

const Session = {
  getAccessToken() {
    return safeStorage.getItem(TOKEN_KEYS.access);
  },
  getUser() {
    const raw = safeStorage.getItem(TOKEN_KEYS.user);
    if (!raw) return null;
    try {
      return typeof raw === "object" ? raw : JSON.parse(raw);
    } catch {
      return null;
    }
  },
  save(data) {
    if (!data) return;
    const { access_token, refresh_token, user } = data;
    if (access_token) safeStorage.setItem(TOKEN_KEYS.access, access_token);
    if (refresh_token) safeStorage.setItem(TOKEN_KEYS.refresh, refresh_token);
    if (user) safeStorage.setItem(TOKEN_KEYS.user, typeof user === "string" ? user : JSON.stringify(user));
  },
  clear() {
    safeStorage.removeItem(TOKEN_KEYS.access);
    safeStorage.removeItem(TOKEN_KEYS.refresh);
    safeStorage.removeItem(TOKEN_KEYS.user);
  },
  isLoggedIn() {
    return Boolean(this.getAccessToken());
  },
};




/**
 * ApiError carries the backend's message/error_code so callers
 * can show a useful message instead of a generic failure.
 */
class ApiError extends Error {
  constructor(message, errorCode, status) {
    super(message);
    this.errorCode = errorCode;
    this.status = status;
  }
}

async function request(path, { method = "GET", body, auth = true } = {}) {
  const headers = { "Content-Type": "application/json" };

  if (auth) {
    const token = Session.getAccessToken();
    if (token) headers.Authorization = `Bearer ${token}`;
  }

  let response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined,
    });
  } catch (networkErr) {
    throw new ApiError("Could not reach the server. Is the backend running?", "NETWORK_ERROR", 0);
  }

  let payload = null;
  try {
    payload = await response.json();
  } catch {
    // Empty or non-JSON body — leave payload as null.
  }

  if (!response.ok) {
    if (response.status === 401 && path !== "/auth/login" && path !== "/auth/google") {
      Session.clear();
      const currentPath = window.location.pathname.split("/").pop();
      if (currentPath && !["login.html", "register.html", "index.html"].includes(currentPath)) {
        window.location.href = "login.html?expired=1";
      }
    }

    let message = payload?.message;
    const errorDetails = payload?.details || payload?.detail;
    if (errorDetails) {
      if (Array.isArray(errorDetails)) {
        const detailMsgs = errorDetails.map((d) => {
          if (typeof d === "string") return d;
          const locStr = d.loc ? d.loc.filter((l) => l !== "body").join(".") : "";
          const msgStr = d.msg || d.message || "";
          return locStr ? `${locStr}: ${msgStr}` : msgStr;
        }).filter(Boolean).join("; ");
        if (detailMsgs) {
          message = message && message !== "Invalid request data" ? `${message} (${detailMsgs})` : detailMsgs;
        }
      } else if (typeof errorDetails === "string") {
        message = errorDetails;
      }
    }
    if (!message) message = "Something went wrong. Please try again.";

    const errorCode = payload?.error_code || "UNKNOWN_ERROR";
    throw new ApiError(message, errorCode, response.status);
  }


  return payload;
}

const api = {
  get: (path, opts) => request(path, { ...opts, method: "GET" }),
  post: (path, body, opts) => request(path, { ...opts, method: "POST", body }),
  put: (path, body, opts) => request(path, { ...opts, method: "PUT", body }),
  patch: (path, body, opts) => request(path, { ...opts, method: "PATCH", body }),
  delete: (path, opts) => request(path, { ...opts, method: "DELETE" }),
};

let _authConfigPromise = null;

const authAPI = {
  register: (payload) => api.post("/auth/register", payload, { auth: false }),
  login: (payload) => api.post("/auth/login", payload, { auth: false }),
  google: (credential, role = "candidate") => api.post("/auth/google", { credential, role }, { auth: false }),
  getConfig() {
    if (!_authConfigPromise) {
      _authConfigPromise = api.get("/auth/config", { auth: false });
    }
    return _authConfigPromise;
  },
  me: () => api.get("/auth/me"),
  logout() {
    Session.clear();
  },
};

const atsAPI = {
  getAnalysis: (candidateId, jobId) => api.get(`/ats/candidate/${candidateId}/job/${jobId}`),
  getMatchingJobs: (candidateId) => api.get(`/ats/candidate/${candidateId}/matching-jobs`),
};

const comparisonAPI = {
  compare: (jobId, candidateIds) => api.post("/candidates/compare", { job_id: jobId, candidate_ids: candidateIds }),
  recommend: (jobId, candidateIds) => api.post("/candidates/recommend", { job_id: jobId, candidate_ids: candidateIds }),
  getMatchingCandidates: (jobId) => api.get(`/jobs/${jobId}/matching-candidates`),
};

const resumeImprovementAPI = {
  improve: (candidateId, jobId) => api.post("/resumes/improve", { candidate_id: candidateId, job_id: jobId }),
  acceptImprovement: (candidateId, originalText, improvedText, section = "experience") =>
    api.post("/resumes/accept-improvement", {
      candidate_id: candidateId,
      original_text: originalText,
      improved_text: improvedText,
      section: section,
    }),
};

const candidateSearchAPI = {
  smartSearch: (payload) => api.post("/candidates/smart-search", payload),
  parseQuery: (query) => api.post("/candidates/parse-query", { query: query }),
};




const resumeAPI = {
  /** Uploads a resume file (multipart/form-data — bypasses the JSON request() helper). */
  async upload(file) {
    const token = Session.getAccessToken();
    const formData = new FormData();
    formData.append("file", file);

    let response;
    try {
      response = await fetch(`${API_BASE_URL}/resumes/upload`, {
        method: "POST",
        headers: token ? { Authorization: `Bearer ${token}` } : {},
        body: formData,
      });
    } catch {
      throw new ApiError("Could not reach the server. Is the backend running?", "NETWORK_ERROR", 0);
    }

    const payload = await response.json().catch(() => null);
    if (!response.ok) {
      throw new ApiError(payload?.message || "Upload failed.", payload?.error_code || "UNKNOWN_ERROR", response.status);
    }
    return payload;
  },

  me: () => api.get("/resumes/me"),
  generateSummary: () => api.post("/resumes/summary", {}),
  update: (payload) => api.put("/resumes/me", payload),
  delete: () => api.delete("/resumes/me"),
  getDomains: () => api.get("/resumes/domains"),
  analyzeDomain: (targetDomain) =>
    api.post(`/resumes/analyze-domain?target_domain=${encodeURIComponent(targetDomain)}`),
  getBestRole: () => api.get("/resumes/best-role"),
  completeRegistration: async (formData) => {
    const token = Session.getAccessToken();
    let response;
    try {
      response = await fetch(`${API_BASE_URL}/resumes/complete-registration`, {
        method: "POST",
        headers: token ? { Authorization: `Bearer ${token}` } : {},
        body: formData,
      });
    } catch {
      throw new ApiError("Could not reach the server. Is the backend running?", "NETWORK_ERROR", 0);
    }
    const payload = await response.json().catch(() => null);
    if (!response.ok) {
      throw new ApiError(payload?.message || "Registration submission failed.", payload?.error_code || "UNKNOWN_ERROR", response.status);
    }
    return payload;
  },
  async exportDetails(candidateId, format = "pdf", applicationId = null) {
    const token = Session.getAccessToken();
    let url = `${API_BASE_URL}/resumes/${candidateId}/export?format=${encodeURIComponent(format)}`;
    if (applicationId) {
      url += `&application_id=${encodeURIComponent(applicationId)}`;
    }
    let response;
    try {
      response = await fetch(url, {
        method: "GET",
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
    } catch {
      throw new ApiError("Could not reach the server. Is the backend running?", "NETWORK_ERROR", 0);
    }
    if (!response.ok) {
      const payload = await response.json().catch(() => null);
      throw new ApiError(payload?.message || "Export failed.", payload?.error_code || "UNKNOWN_ERROR", response.status);
    }
    if (format === "json") {
      return await response.json();
    }
    const blob = await response.blob();
    let filename = format === "pdf" ? "Candidate_Profile.pdf" : (format === "zip" ? "Candidate_Full_Details.zip" : "Candidate_Profile.html");
    const disposition = response.headers.get("Content-Disposition");
    if (disposition && disposition.includes("filename=")) {
      const match = disposition.match(/filename="?([^";]+)"?/);
      if (match && match[1]) filename = match[1];
    }
    const blobUrl = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = blobUrl;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(blobUrl);
  },
  download(candidateId, format = "pdf", applicationId = null) {
    return this.exportDetails(candidateId, format, applicationId);
  },
};
const resumesAPI = resumeAPI;

const jobsAPI = {
  create: (payload) => api.post("/jobs", payload),
  list: (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return api.get(`/jobs${query ? `?${query}` : ""}`);
  },
  get: (jobId) => api.get(`/jobs/${jobId}`),
  update: (jobId, payload) => api.put(`/jobs/${jobId}`, payload),
  remove: (jobId) => api.delete(`/jobs/${jobId}`),
  apply: (jobId) => api.post(`/jobs/${jobId}/apply`, {}),
  ranking: (jobId) => api.get(`/jobs/${jobId}/ranking`),
  applications: (jobId, params = {}) => {
    const query = new URLSearchParams(params).toString();
    return api.get(`/jobs/${jobId}/applications${query ? `?${query}` : ""}`);
  },
  eligibleApplications: (jobId) => api.get(`/jobs/${jobId}/applications/eligible`),
  screeningStats: (jobId) => api.get(`/jobs/${jobId}/screening-statistics`),
  updateScreeningSettings: (jobId, payload) => api.patch(`/jobs/${jobId}/screening-settings`, payload),
  analyze: (description) => api.post("/jobs/analyze", { description }),
  generateQuestions: (jobId, numQuestions = 6) =>
    api.post(`/jobs/${jobId}/generate-questions?num_questions=${numQuestions}`, {}),
};

const applicationsAPI = {
  mine: () => api.get("/applications"),
  get: (applicationId) => api.get(`/applications/${applicationId}`),
  screen: (applicationId) => api.post(`/applications/${applicationId}/screen`, {}),
  getATSReport: (applicationId) => api.get(`/applications/${applicationId}/ats-report`),
  updateStatus: (applicationId, status, overrideReason = null) =>
    api.patch(`/applications/${applicationId}/status`, { status, override_reason: overrideReason }),
};

const recommendationsAPI = {
  jobs: (limit = 10) => api.get(`/recommendations/jobs?limit=${limit}`),
};

const interviewsAPI = {
  start: (candidateId, jobId, interviewType = "mixed", numQuestions = 6) =>
    api.post("/interviews", {
      candidate_id: candidateId,
      job_id: jobId,
      interview_type: interviewType,
      num_questions: numQuestions,
    }),
  list: () => api.get("/interviews"),
  get: (interviewId) => api.get(`/interviews/${interviewId}`),
  answer: (interviewId, questionId, answerText) =>
    api.post(`/interviews/${interviewId}/answers`, { question_id: questionId, answer_text: answerText }),
  report: (interviewId) => api.get(`/interviews/${interviewId}/report`),
  evaluate: (interviewId) => api.post(`/interviews/${interviewId}/evaluate`, {}),
};

const speechAPI = {
  async transcribe(audioBlob, filename = "answer.webm") {
    const token = Session.getAccessToken();
    const formData = new FormData();
    formData.append("file", audioBlob, filename);

    let response;
    try {
      response = await fetch(`${API_BASE_URL}/speech/transcribe`, {
        method: "POST",
        headers: token ? { Authorization: `Bearer ${token}` } : {},
        body: formData,
      });
    } catch {
      throw new ApiError("Could not reach the server. Is the backend running?", "NETWORK_ERROR", 0);
    }

    const payload = await response.json().catch(() => null);
    if (!response.ok) {
      throw new ApiError(payload?.message || "Transcription failed.", payload?.error_code || "UNKNOWN_ERROR", response.status);
    }
    return payload;
  },
};

const analyticsAPI = {
  recruiter: (params = {}) => {
    const cleanParams = {};
    for (const [k, v] of Object.entries(params)) {
      if (v !== null && v !== undefined && v !== "") {
        cleanParams[k] = v;
      }
    }
    const query = new URLSearchParams(cleanParams).toString();
    return api.get(`/analytics/recruiter${query ? `?${query}` : ""}`);
  },
  candidate: () => api.get("/analytics/candidate"),
  compareCandidates: (jobId, candidateIds) =>
    api.post("/recruiter/candidates/compare", { job_id: jobId, candidate_ids: candidateIds }),
};

const notificationsAPI = {
  get: () => api.get("/notifications"),
  markRead: (id) => api.patch(`/notifications/${id}/read`, {}),
  markAllRead: () => api.post("/notifications/read-all", {}),
};

const recruiterProfileAPI = {
  get: () => api.get("/recruiter-profile"),
  update: (payload) => api.put("/recruiter-profile", payload),
  verifyDomain: () => api.post("/recruiter-profile/verify-domain", {}),
  verifyWebsite: () => api.post("/recruiter-profile/verify-website", {}),
  submitCompanyVerification: (payload) =>
    api.post(
      `/recruiter-profile/submit-company-verification?cin_gstin=${encodeURIComponent(
        payload.cin_gstin || ""
      )}&registration_number=${encodeURIComponent(
        payload.registration_number || ""
      )}&country=${encodeURIComponent(payload.country || "")}&address=${encodeURIComponent(
        payload.address || ""
      )}`,
      {}
    ),
};

const adminAPI = {
  stats: () => api.get("/admin/stats"),
  users: (role) => api.get(`/admin/users${role ? `?role=${role}` : ""}`),
  toggleUserActive: (userId) => api.patch(`/admin/users/${userId}/toggle-active`, {}),
  deleteUser: (userId) => api.delete(`/admin/users/${userId}`),
  pendingRecruiters: () => api.get("/admin/pending-recruiters"),
  approveRecruiter: (userId) => api.patch(`/admin/recruiters/${userId}/approve`, {}),
  rejectRecruiter: (userId) => api.patch(`/admin/recruiters/${userId}/reject`, {}),
  companies: () => api.get("/admin/companies"),
  verifyCompany: (companyId, status, notes) =>
    api.patch(`/admin/companies/${companyId}/verification?status=${status}&notes=${encodeURIComponent(notes || "")}`, {}),
  suspiciousJobs: () => api.get("/admin/suspicious-jobs"),
  moderateJob: (jobId, status) => api.patch(`/admin/jobs/${jobId}/moderate?status=${status}`, {}),
  skills: () => api.get("/admin/skills"),
  createSkill: (skillName, category) => api.post("/admin/skills", { skill_name: skillName, category }),
  deleteSkill: (skillId) => api.delete(`/admin/skills/${skillId}`),
  jobs: () => api.get("/admin/jobs"),
  auditLogs: (limit = 50) => api.get(`/admin/audit-logs?limit=${limit}`),
};

const messagesAPI = {
  send: (payload) => api.post("/messages/send", payload),
  getThread: (otherUserId) => api.get(`/messages/thread/${otherUserId}`),
  getConversations: () => api.get("/messages/conversations"),
  getContacts: () => api.get("/messages/contacts"),
  getUnreadCount: () => api.get("/messages/unread-count"),
};
api.messages = messagesAPI;

function dashboardUrlForRole(role) {
  const user = Session.getUser();
  if (role === "admin" || role === "superadmin") return "admin.html";
  if (role === "recruiter" || role === "company_admin") {
    if (user && user.is_profile_complete === false) {
      return "recruiter-profile.html?onboarding=required";
    }
    return "recruiter-portal.html";
  }
  if (role === "candidate") {
    if (user && user.is_profile_complete === false) {
      return "complete-registration.html?onboarding=required";
    }
    return "candidate-portal.html";
  }
  return "candidate-portal.html";
}


/** Automatic Role Enforcement Guard across all HTML pages */
(function checkRoleGuard() {
  function enforce() {
    const reqRole = document.body?.dataset?.requiredRole;
    if (!reqRole) return;

    if (!Session.isLoggedIn()) {
      window.location.href = "login.html";
      return;
    }

    const user = Session.getUser();
    const userRole = user?.role || "candidate";

    if (reqRole === "candidate" && userRole === "candidate") {
      const currentFile = window.location.pathname.split("/").pop();
      if (user?.is_profile_complete === false && currentFile !== "complete-registration.html") {
        window.location.href = "complete-registration.html?onboarding=required";
      }
    } else if (reqRole === "candidate" && userRole !== "candidate") {
      window.location.href = dashboardUrlForRole(userRole);
    } else if (reqRole === "recruiter" && (userRole === "recruiter" || userRole === "company_admin")) {
      const currentFile = window.location.pathname.split("/").pop();
      if (user?.is_profile_complete === false && currentFile !== "recruiter-profile.html") {
        window.location.href = "recruiter-profile.html?onboarding=required";
      }
    } else if (reqRole === "recruiter" && userRole !== "recruiter") {
      window.location.href = dashboardUrlForRole(userRole);
    } else if (reqRole === "admin" && userRole !== "admin") {
      window.location.href = dashboardUrlForRole(userRole);
    }
  }


  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", enforce);
  } else {
    enforce();
  }
})();

/** ThemeManager — Dark / Light Mode Toggle */
const ThemeManager = {
  getTheme() {
    return safeStorage.getItem("ar_theme") || "light";
  },
  setTheme(theme) {
    safeStorage.setItem("ar_theme", theme);
    document.documentElement.setAttribute("data-bs-theme", theme);
    document.documentElement.setAttribute("data-theme", theme);
    this.updateToggleButtons(theme);
  },
  toggle() {
    const next = this.getTheme() === "dark" ? "light" : "dark";
    this.setTheme(next);
  },
  updateToggleButtons(theme) {
    const btns = document.querySelectorAll("#theme-toggle-btn, .theme-toggle");
    btns.forEach(btn => {
      btn.textContent = theme === "dark" ? "☀️" : "🌙";
    });
  },
  init() {
    const current = this.getTheme();
    document.documentElement.setAttribute("data-bs-theme", current);
    document.documentElement.setAttribute("data-theme", current);

    const setup = () => {
      this.updateToggleButtons(current);
      const btns = document.querySelectorAll("#theme-toggle-btn, .theme-toggle");
      btns.forEach(btn => {
        btn.onclick = (e) => {
          e.preventDefault();
          this.toggle();
        };
      });
    };

    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", setup);
    } else {
      setup();
    }
  }
};
ThemeManager.init();

// Attach all API objects to global window object
window.Session = Session;
window.ThemeManager = ThemeManager;
window.api = typeof api !== "undefined" ? api : undefined;
window.API = typeof api !== "undefined" ? api : undefined;
window.authAPI = typeof authAPI !== "undefined" ? authAPI : undefined;
window.resumeAPI = typeof resumeAPI !== "undefined" ? resumeAPI : undefined;
window.resumesAPI = typeof resumeAPI !== "undefined" ? resumeAPI : undefined;
window.jobsAPI = typeof jobsAPI !== "undefined" ? jobsAPI : undefined;
window.applicationsAPI = typeof applicationsAPI !== "undefined" ? applicationsAPI : undefined;
window.matchingAPI = typeof matchingAPI !== "undefined" ? matchingAPI : undefined;
window.recommendationsAPI = typeof recommendationsAPI !== "undefined" ? recommendationsAPI : undefined;
window.interviewsAPI = typeof interviewsAPI !== "undefined" ? interviewsAPI : undefined;
window.speechAPI = typeof speechAPI !== "undefined" ? speechAPI : undefined;
window.analyticsAPI = typeof analyticsAPI !== "undefined" ? analyticsAPI : undefined;
window.adminAPI = typeof adminAPI !== "undefined" ? adminAPI : undefined;
window.recruiterProfileAPI = typeof recruiterProfileAPI !== "undefined" ? recruiterProfileAPI : undefined;
window.notificationsAPI = typeof notificationsAPI !== "undefined" ? notificationsAPI : undefined;
window.messagesAPI = typeof messagesAPI !== "undefined" ? messagesAPI : undefined;
window.dashboardUrlForRole = dashboardUrlForRole;





