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
    const token = this.getAccessToken();
    const user = this.getUser();
    if (!token || !user) return false;
    if (user.is_email_verified === false) return false;
    return true;
  },
};

window.Session = Session;
window.API_BASE_URL = API_BASE_URL;




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

async function request(path, { method = "GET", body, auth = true, _isRetry = false } = {}) {
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
    if (response.status === 401 && path !== "/auth/login" && path !== "/auth/google" && path !== "/auth/refresh") {
      const refreshToken = safeStorage.getItem(TOKEN_KEYS.refresh);
      if (refreshToken && !_isRetry) {
        try {
          const refreshRes = await fetch(`${API_BASE_URL}/auth/refresh`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refresh_token: refreshToken }),
          });
          if (refreshRes.ok) {
            const refreshPayload = await refreshRes.json();
            if (refreshPayload?.data) {
              Session.save(refreshPayload.data);
              return request(path, { method, body, auth, _isRetry: true });
            }
          }
        } catch (e) {
          // Token refresh failed, fall through to logout
        }
      }

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

function buildQueryString(params = {}) {
  const cleanParams = {};
  for (const [key, value] of Object.entries(params || {})) {
    if (value !== undefined && value !== null && value !== "") {
      cleanParams[key] = value;
    }
  }
  const query = new URLSearchParams(cleanParams).toString();
  return query ? `?${query}` : "";
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
  checkEmail: (email) => api.get(`/auth/check-email?email=${encodeURIComponent(email)}`, { auth: false }),
  register: (payload) => api.post("/auth/register", payload, { auth: false }),
  login: (payload) => api.post("/auth/login", payload, { auth: false }),
  google: (credential, role = "candidate") => api.post("/auth/google", { credential, role }, { auth: false }),
  forgotPassword: (email) => api.post("/auth/forgot-password", { email }, { auth: false }),
  resetPassword: (payload) => api.post("/auth/reset-password", payload, { auth: false }),
  verifyEmail: (token) => api.get(`/auth/verify-email?token=${encodeURIComponent(token)}`, { auth: false }),
  verifyOTP: (email, otp) => api.post("/auth/verify-otp", { email, otp }, { auth: false }),
  resendVerification: (email) => api.post("/auth/resend-verification", { email }, { auth: false }),
  resendOTP: (email) => api.post("/auth/resend-otp", { email }, { auth: false }),
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
  list: (params = {}) => api.get(`/jobs${buildQueryString(params)}`),
  get: (jobId) => {
    if (!jobId || jobId === "undefined") return Promise.reject(new ApiError("Invalid Job ID", "INVALID_PARAM", 400));
    return api.get(`/jobs/${jobId}`);
  },
  update: (jobId, payload) => {
    if (!jobId || jobId === "undefined") return Promise.reject(new ApiError("Invalid Job ID", "INVALID_PARAM", 400));
    return api.put(`/jobs/${jobId}`, payload);
  },
  remove: (jobId) => {
    if (!jobId || jobId === "undefined") return Promise.reject(new ApiError("Invalid Job ID", "INVALID_PARAM", 400));
    return api.delete(`/jobs/${jobId}`);
  },
  apply: (jobId) => {
    if (!jobId || jobId === "undefined") return Promise.reject(new ApiError("Invalid Job ID", "INVALID_PARAM", 400));
    return api.post(`/jobs/${jobId}/apply`, {});
  },
  ranking: (jobId) => api.get(`/jobs/${jobId}/ranking`),
  applications: (jobId, params = {}) => api.get(`/jobs/${jobId}/applications${buildQueryString(params)}`),
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
  sendAudio: async (audioBlobOrFile, receiverId, applicationId = null) => {
    const token = Session.getAccessToken();
    const formData = new FormData();
    formData.append("file", audioBlobOrFile, audioBlobOrFile.name || "voice-message.webm");
    formData.append("receiver_id", receiverId);
    if (applicationId) formData.append("application_id", applicationId);

    const response = await fetch(`${API_BASE_URL}/messages/send-audio`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
    });

    const payload = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new ApiError(payload?.message || "Failed to send audio message", payload?.error_code, response.status);
    }
    return payload;
  },
  getThread: (otherUserId) => api.get(`/messages/thread/${otherUserId}`),
  getConversations: () => api.get("/messages/conversations"),
  getContacts: () => api.get("/messages/contacts"),
  getUnreadCount: () => api.get("/messages/unread-count"),
  delete: (messageId) => api.delete(`/messages/${messageId}`),
  update: (messageId, content) => api.put(`/messages/${messageId}`, { content }),
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
      alert("Access Denied: This area is restricted to Candidate accounts. Redirecting to your Recruiter Portal...");
      window.location.href = dashboardUrlForRole(userRole);
    } else if (reqRole === "recruiter" && (userRole === "recruiter" || userRole === "company_admin")) {
      const currentFile = window.location.pathname.split("/").pop();
      if (user?.is_profile_complete === false && currentFile !== "recruiter-profile.html") {
        window.location.href = "recruiter-profile.html?onboarding=required";
      }
    } else if (reqRole === "recruiter" && userRole !== "recruiter" && userRole !== "company_admin") {
      alert("Access Denied: This area is restricted to Recruiter accounts. Redirecting to your Candidate Portal...");
      window.location.href = dashboardUrlForRole(userRole);
    } else if (reqRole === "admin" && userRole !== "admin" && userRole !== "superadmin") {
      alert("Access Denied: This area is restricted to Administrators only. Redirecting to your Portal...");
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
window.API_BASE_URL = API_BASE_URL;
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
const codingAPI = {
  createQuestion: (payload) => api.post("/coding/questions", payload),
  listQuestions: (params = {}) => api.get("/coding/questions", params),
  getQuestion: (id) => api.get(`/coding/questions/${id}`),
  createAssessment: (payload) => api.post("/coding/assessments", payload),
  listAssessments: (jobId) => api.get("/coding/assessments", jobId ? { job_id: jobId } : {}),
  getAssessment: (id) => api.get(`/coding/assessments/${id}`),
  getCandidateAssessments: () => api.get("/coding/candidate/assessments"),
  startAssessment: (id) => api.post(`/coding/candidate/assessments/${id}/start`),
  runCode: (attemptId, payload) => api.post(`/coding/candidate/attempts/${attemptId}/run`, payload),
  submitAssessment: (attemptId, submissions) => api.post(`/coding/candidate/attempts/${attemptId}/submit`, submissions),
  getAttemptResult: (attemptId) => api.get(`/coding/candidate/attempts/${attemptId}/result`),
};

window.codingAPI = codingAPI;

const calendarAPI = {
  getGoogleAuthUrl: () => api.get("/calendar/connect/google"),
  getOutlookAuthUrl: () => api.get("/calendar/connect/outlook"),
  disconnect: (provider = "google") => api.post(`/calendar/disconnect?provider=${provider}`),
  getStatus: () => api.get("/calendar/status"),
};

const emailSettingsAPI = {
  getSettings: () => api.get("/notifications/email-settings"),
  updateSettings: (payload) => api.put("/notifications/email-settings", payload),
  getLogs: () => api.get("/notifications/logs"),
};

const scheduledInterviewsAPI = {
  schedule: (payload) => api.post("/interviews/schedule", payload),
  reschedule: (interviewId, payload) => api.put(`/interviews/${interviewId}/reschedule`, payload),
  cancel: (interviewId) => api.post(`/interviews/${interviewId}/cancel`),
  sendReminder: (interviewId) => api.post(`/interviews/${interviewId}/reminder`),
  getUpcoming: () => api.get("/interviews/upcoming"),
};

window.calendarAPI = calendarAPI;
window.emailSettingsAPI = emailSettingsAPI;
window.scheduledInterviewsAPI = scheduledInterviewsAPI;
window.dashboardUrlForRole = dashboardUrlForRole;

const candidateSearchAPI = {
  smartSearch: (payload) => api.post("/candidates/smart-search", payload),
  searchGet: (params = {}) => api.get("/candidates/search", params),
  parseQuery: (query) => api.post("/candidates/parse-query", { query }),
  getResumeUrl: (candidateId) => `${API_BASE_URL}/candidates/${candidateId}/resume`,
  getAtsReport: (candidateId, jobId = null) => api.get(`/candidates/${candidateId}/ats-report`, jobId ? { job_id: jobId } : {}),
  getSavedSearches: () => api.get("/candidates/saved-searches"),
  saveSearch: (payload) => api.post("/candidates/saved-searches", payload),
  deleteSavedSearch: (searchId) => api.delete(`/candidates/saved-searches/${searchId}`),
  getRecentSearches: () => api.get("/candidates/recent-searches"),
  clearRecentSearches: () => api.delete("/candidates/recent-searches"),
  shortlist: (payload) => api.post("/candidates/shortlist", payload),
  bulkShortlist: (payload) => api.post("/candidates/bulk-shortlist", payload),
  invite: (payload) => api.post("/candidates/invite", payload),
  bulkInvite: (payload) => api.post("/candidates/bulk-invite", payload),
};

const screeningAPI = {
  start: (applicationId) => api.post(`/screening/applications/${applicationId}/start`),
  getByApplication: (applicationId) => api.get(`/screening/applications/${applicationId}`),
  getSession: (screeningId) => api.get(`/screening/${screeningId}`),
  submitAnswer: (screeningId, answer) => api.post(`/screening/${screeningId}/answer`, { answer }),
  cancel: (screeningId) => api.post(`/screening/${screeningId}/cancel`),
  resume: (screeningId) => api.post(`/screening/${screeningId}/resume`),
  getResult: (screeningId) => api.get(`/screening/${screeningId}/result`),
  override: (screeningId, formData) => api.post(`/screening/${screeningId}/override`, formData),
  getConsent: () => api.get("/screening/consent/me"),
  updateConsent: (payload) => api.post("/screening/consent", payload),
};

const proctoringAPI = {
  submitConsent: (attemptId, payload) => api.post(`/proctoring/attempts/${attemptId}/consent`, payload),
  recordEvent: (attemptId, payload) => api.post(`/proctoring/attempts/${attemptId}/events`, payload),
  getEvents: (attemptId) => api.get(`/proctoring/attempts/${attemptId}/events`),
  getIntegrity: (attemptId) => api.get(`/proctoring/attempts/${attemptId}/integrity`),
  analyzeSimilarity: (attemptId, submissionId) => api.post(`/proctoring/attempts/${attemptId}/code-similarity?submission_id=${submissionId}`),
  saveDecision: (attemptId, payload) => api.post(`/proctoring/attempts/${attemptId}/recruiter-decision`, payload),
};

const interviewScorecardAPI = {
  getScorecard: (interviewId) => api.get(`/interviews/${interviewId}/scorecard`),
  regenerateScorecard: (interviewId) => api.post(`/interviews/${interviewId}/scorecard/regenerate`, {}),
  saveDecision: (scorecardId, payload) => api.post(`/scorecards/${scorecardId}/recruiter-decision`, payload),
};

const talentRediscoveryAPI = {
  triggerRediscovery: (jobId) => api.post(`/jobs/${jobId}/rediscover`, {}),
  getStatus: (jobId) => api.get(`/jobs/${jobId}/rediscovery/status`),
  getSummary: (jobId) => api.get(`/jobs/${jobId}/rediscovery`),
  getCandidates: (jobId, params = {}) => api.get(`/jobs/${jobId}/rediscovery/candidates${buildQueryString(params)}`),
  getCandidateDetail: (jobId, candidateId) => api.get(`/jobs/${jobId}/rediscovery/${candidateId}`),
  shortlistCandidate: (jobId, candidateId) => api.post(`/jobs/${jobId}/rediscovery/${candidateId}/shortlist`, {}),
  contactCandidate: (jobId, candidateId) => api.post(`/jobs/${jobId}/rediscovery/${candidateId}/contact`, {}),
  smartSearch: (query, minScore = 50, silverOnly = false) =>
    api.post("/talent-rediscovery/smart-search", { query, min_score: minScore, silver_medalist_only: silverOnly }),
  getAnalytics: () => api.get("/talent-rediscovery/analytics"),
};

const feedbackAPI = {
  get: (applicationId) => api.get(`/applications/${applicationId}/feedback`),
  generate: (applicationId, feedbackLevel = "personalized", customDirection = null) =>
    api.post(`/applications/${applicationId}/feedback/generate?feedback_level=${feedbackLevel}${customDirection ? `&custom_direction=${encodeURIComponent(customDirection)}` : ""}`, {}),
  approve: (applicationId, finalContentOverride = null) =>
    api.post(`/applications/${applicationId}/feedback/approve`, finalContentOverride ? { final_content_override: finalContentOverride } : {}),
  regenerate: (applicationId, customDirection = "more encouraging") =>
    api.post(`/applications/${applicationId}/feedback/regenerate?custom_direction=${encodeURIComponent(customDirection)}`, {}),
  bulkGenerate: (applicationIds, autoApprove = false, prompt = null) =>
    api.post("/recruiter/feedback/bulk-generate", { application_ids: applicationIds, auto_approve: autoApprove, regeneration_prompt: prompt }),
};

window.candidateSearchAPI = candidateSearchAPI;
window.screeningAPI = screeningAPI;
window.proctoringAPI = proctoringAPI;
window.interviewScorecardAPI = interviewScorecardAPI;
window.talentRediscoveryAPI = talentRediscoveryAPI;
window.feedbackAPI = feedbackAPI;

// Attach sub-namespaces directly to api object so API.interviews, API.jobs, etc. work seamlessly
Object.assign(api, {
  auth: authAPI,
  ats: atsAPI,
  comparison: comparisonAPI,
  resumeImprovement: resumeImprovementAPI,
  resume: resumeAPI,
  resumes: resumeAPI,
  jobs: jobsAPI,
  applications: applicationsAPI,
  matching: matchingAPI,
  recommendations: recommendationsAPI,
  interviews: interviewsAPI,
  speech: speechAPI,
  analytics: analyticsAPI,
  admin: adminAPI,
  recruiterProfile: recruiterProfileAPI,
  notifications: notificationsAPI,
  messages: messagesAPI,
  coding: codingAPI,
  calendar: calendarAPI,
  emailSettings: emailSettingsAPI,
  scheduledInterviews: scheduledInterviewsAPI,
  candidateSearch: candidateSearchAPI,
  screening: screeningAPI,
  proctoring: proctoringAPI,
  interviewScorecard: interviewScorecardAPI,
  talentRediscovery: talentRediscoveryAPI,
  feedback: feedbackAPI,
});








