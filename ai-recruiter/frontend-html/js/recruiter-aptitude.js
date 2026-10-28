/**
 * recruiter-aptitude.js — Frontend controller for AI Aptitude Question Generator & Studio.
 * Handles:
 * - Dynamic topic selection (chips, custom inputs)
 * - AI test generation with real-time spinner & status alerts
 * - Interactive Question Studio (Review, Edit, Regenerate, Delete)
 * - Test Publishing
 * - Assessment Library & Candidate Attempts/Results modal
 */

let selectedTopics = ["Percentages", "Profit and Loss", "Logical Reasoning"];
let currentTest = null;
let editModalInstance = null;
let resultsModalInstance = null;

document.addEventListener("DOMContentLoaded", () => {
  // Check auth
  const user = Session.getUser();
  if (user) {
    const greetingEl = document.getElementById("user-greeting");
    if (greetingEl) greetingEl.textContent = `👋 ${user.name || user.email}`;
  }

  // Initialize Bootstrap modals
  const editModalEl = document.getElementById("editQuestionModal");
  if (editModalEl) editModalInstance = new bootstrap.Modal(editModalEl);

  const resultsModalEl = document.getElementById("resultsModal");
  if (resultsModalEl) resultsModalInstance = new bootstrap.Modal(resultsModalEl);

  // Bind topic chip clicks
  document.querySelectorAll(".topic-chip").forEach((chip) => {
    const topic = chip.dataset.topic;
    if (selectedTopics.includes(topic)) {
      chip.classList.add("active");
    }
    chip.addEventListener("click", () => {
      toggleTopic(topic, chip);
    });
  });

  // Bind custom topic addition
  const addTopicBtn = document.getElementById("btn-add-topic");
  const customInput = document.getElementById("custom-topic-input");
  if (addTopicBtn && customInput) {
    addTopicBtn.addEventListener("click", () => {
      addCustomTopic(customInput.value);
      customInput.value = "";
    });
    customInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        addCustomTopic(customInput.value);
        customInput.value = "";
      }
    });
  }

  // Library button
  const libBtn = document.getElementById("btn-show-library");
  if (libBtn) {
    libBtn.addEventListener("click", () => {
      switchView("library-view");
      loadRecruiterTests();
    });
  }

  // Logout button
  const logoutBtn = document.getElementById("logout-btn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      safeStorage.removeItem(TOKEN_KEYS.access);
      safeStorage.removeItem(TOKEN_KEYS.refresh);
      safeStorage.removeItem(TOKEN_KEYS.user);
      window.location.href = "login.html";
    });
  }
  const logoutMobileBtn = document.getElementById("logout-btn-mobile");
  if (logoutMobileBtn) {
    logoutMobileBtn.addEventListener("click", () => {
      safeStorage.removeItem(TOKEN_KEYS.access);
      safeStorage.removeItem(TOKEN_KEYS.refresh);
      safeStorage.removeItem(TOKEN_KEYS.user);
      window.location.href = "login.html";
    });
  }

  renderSelectedTopics();
});

// ==============================================================================
// TOPIC MANAGEMENT
// ==============================================================================

function toggleTopic(topic, chipEl) {
  const index = selectedTopics.indexOf(topic);
  if (index > -1) {
    selectedTopics.splice(index, 1);
    if (chipEl) chipEl.classList.remove("active");
  } else {
    selectedTopics.push(topic);
    if (chipEl) chipEl.classList.add("active");
  }
  renderSelectedTopics();
}

function addCustomTopic(topicStr) {
  const cleaned = (topicStr || "").trim();
  if (!cleaned) return;
  if (!selectedTopics.includes(cleaned)) {
    selectedTopics.push(cleaned);
    renderSelectedTopics();
  }
}

function removeTopic(topic) {
  const index = selectedTopics.indexOf(topic);
  if (index > -1) {
    selectedTopics.splice(index, 1);
    // Unhighlight corresponding chip if exists
    document.querySelectorAll(".topic-chip").forEach((chip) => {
      if (chip.dataset.topic === topic) {
        chip.classList.remove("active");
      }
    });
    renderSelectedTopics();
  }
}

function renderSelectedTopics() {
  const container = document.getElementById("selected-topics-container");
  if (!container) return;

  if (selectedTopics.length === 0) {
    container.innerHTML = `<span class="text-muted small fst-italic" id="no-topics-placeholder">No topics selected yet. Click any chip above or type a topic.</span>`;
    return;
  }

  container.innerHTML = selectedTopics
    .map(
      (t) => `
    <span class="selected-topic-tag">
      <span>${escapeHtml(t)}</span>
      <button type="button" class="btn-remove" onclick="removeTopic('${escapeJs(t)}')">&times;</button>
    </span>
  `
    )
    .join("");
}

// ==============================================================================
// VIEW SWITCHER
// ==============================================================================

function switchView(viewId) {
  const views = ["creator-view", "studio-view", "library-view"];
  views.forEach((v) => {
    const el = document.getElementById(v);
    if (el) {
      if (v === viewId) {
        el.classList.remove("d-none");
      } else {
        el.classList.add("d-none");
      }
    }
  });
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// ==============================================================================
// 1. GENERATE APTITUDE TEST
// ==============================================================================

async function handleGenerateQuestions() {
  const title = (document.getElementById("test-title").value || "").trim();
  if (!title) {
    showAlert("Please enter a test title.", "warning");
    return;
  }

  if (selectedTopics.length === 0) {
    showAlert("Please select at least one topic for question generation.", "warning");
    return;
  }

  const numQuestions = parseInt(document.getElementById("num-questions").value, 10) || 10;
  const difficulty = document.getElementById("difficulty-level").value || "mixed";
  const duration = parseInt(document.getElementById("test-duration").value, 10) || 15;
  const marksPerQ = parseFloat(document.getElementById("marks-per-question").value) || 1.0;

  const btn = document.getElementById("btn-generate");
  const originalHtml = btn.innerHTML;
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status"></span> Generating ${numQuestions} Aptitude Questions with AI...`;

  showAlert(`Synthesizing ${numQuestions} verified questions across ${selectedTopics.length} topics. Please wait a moment...`, "info");

  try {
    const payload = {
      title: title,
      topics: selectedTopics,
      num_questions: numQuestions,
      difficulty: difficulty,
      duration_minutes: duration,
      marks_per_question: marksPerQ,
    };

    const res = await api.post("/aptitude/generate", payload);
    if (res.success && res.data) {
      currentTest = res.data;
      showAlert("Questions successfully generated! Review them in the studio below.", "success");
      renderQuestionStudio(currentTest);
      switchView("studio-view");
    } else {
      showAlert(res.message || "Failed to generate questions. Please try again.", "danger");
    }
  } catch (err) {
    console.error("AI Generation error:", err);
    showAlert(err.message || "An error occurred while communicating with the AI service.", "danger");
  } finally {
    btn.disabled = false;
    btn.innerHTML = originalHtml;
  }
}

// ==============================================================================
// 2. QUESTION STUDIO RENDERING
// ==============================================================================

function renderQuestionStudio(test) {
  if (!test) return;

  // Set test metadata
  document.getElementById("studio-test-title").textContent = test.title;
  document.getElementById("studio-total-q").textContent = test.total_questions;
  document.getElementById("studio-total-marks").textContent = test.total_marks.toFixed(1);
  document.getElementById("studio-duration").textContent = `${test.duration_minutes}m`;

  const statusBadge = document.getElementById("studio-status-badge");
  if (test.status === "published") {
    statusBadge.className = "badge bg-success text-white px-3 py-1 rounded-pill fw-bold";
    statusBadge.textContent = "✓ Published — Live for Candidates";
    document.getElementById("btn-publish-test").classList.add("d-none");
  } else {
    statusBadge.className = "badge bg-warning text-dark px-3 py-1 rounded-pill fw-bold";
    statusBadge.textContent = "Draft — Review & Approval Required";
    document.getElementById("btn-publish-test").classList.remove("d-none");
  }

  // Topics pills
  const topicsContainer = document.getElementById("studio-topics-list");
  if (topicsContainer) {
    const topics = test.topics || [];
    topicsContainer.innerHTML = topics
      .map((t) => `<span class="badge bg-light text-dark border rounded-pill">${escapeHtml(t)}</span>`)
      .join(" ");
  }

  // Render questions
  const qContainer = document.getElementById("studio-questions-container");
  if (!qContainer) return;

  if (!test.questions || test.questions.length === 0) {
    qContainer.innerHTML = `<div class="col-12 text-center py-5 text-muted">No questions in this test. Click "➕ New Test" to generate.</div>`;
    return;
  }

  qContainer.innerHTML = test.questions
    .map((q, idx) => {
      const qNum = idx + 1;
      const optionsHtml = (q.options || [])
        .map((opt) => {
          const isCorrect = opt.is_correct || opt.order_index === q.correct_option_index;
          return `
          <div class="col-md-6">
            <div class="option-box ${isCorrect ? "is-correct shadow-sm" : ""}">
              <div class="d-flex justify-content-between align-items-center">
                <span><strong>${escapeHtml(opt.option_letter)}.</strong> ${escapeHtml(opt.option_text)}</span>
                ${isCorrect ? `<span class="badge bg-success text-white rounded-pill px-2 py-1">✓ Correct Answer</span>` : ""}
              </div>
            </div>
          </div>
        `;
        })
        .join("");

      return `
      <div class="col-12" id="q-card-${q.id}">
        <div class="question-card p-4">
          <!-- Card Header -->
          <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-3 pb-2 border-bottom">
            <div class="d-flex align-items-center gap-2">
              <span class="badge bg-dark text-white rounded-pill px-3 py-1 fw-bold fs-6">Q${qNum}</span>
              <span class="badge bg-primary-subtle text-primary rounded-pill px-2.5 py-1 fw-semibold">${escapeHtml(q.topic_name || q.subtopic || "General")}</span>
              <span class="badge bg-secondary-subtle text-secondary rounded-pill px-2.5 py-1 text-capitalize">${escapeHtml(q.difficulty || "medium")}</span>
              <span class="badge bg-light text-dark border rounded-pill px-2.5 py-1">${q.marks} Mark${q.marks > 1 ? "s" : ""}</span>
            </div>

            <!-- Card Actions -->
            <div class="d-flex align-items-center gap-2">
              <button class="btn btn-sm btn-outline-primary rounded-pill px-3 fw-semibold" onclick="openEditModal('${q.id}')">
                ✏️ Edit
              </button>
              <button class="btn btn-sm btn-outline-info rounded-pill px-3 fw-semibold" onclick="handleRegenerateQuestion('${q.id}', this)">
                🔄 Regenerate
              </button>
              <button class="btn btn-sm btn-outline-danger rounded-pill px-3 fw-semibold" onclick="handleDeleteQuestion('${q.id}')">
                🗑️ Delete
              </button>
            </div>
          </div>

          <!-- Question Statement -->
          <p class="fs-5 fw-medium text-dark mb-4" style="line-height: 1.6;">
            ${escapeHtml(q.question)}
          </p>

          <!-- 4 Options Grid -->
          <div class="row g-2 mb-3">
            ${optionsHtml}
          </div>

          <!-- Explanation Accordion -->
          <div class="explanation-callout mt-3">
            <div class="d-flex align-items-start gap-2">
              <span class="fs-5">💡</span>
              <div>
                <strong class="text-success d-block mb-1">Step-by-Step Mathematical Explanation:</strong>
                <span class="text-secondary small" style="white-space: pre-line; line-height: 1.5;">${escapeHtml(q.explanation || "No explanation provided.")}</span>
              </div>
            </div>
          </div>

        </div>
      </div>
    `;
    })
    .join("");
}

// ==============================================================================
// 3. EDIT QUESTION
// ==============================================================================

function openEditModal(questionId) {
  if (!currentTest || !currentTest.questions) return;
  const q = currentTest.questions.find((item) => item.id === questionId);
  if (!q) return;

  document.getElementById("edit-q-id").value = q.id;
  document.getElementById("edit-q-text").value = q.question;
  document.getElementById("edit-q-topic").value = q.topic_name || q.subtopic || "";
  document.getElementById("edit-q-diff").value = q.difficulty || "medium";
  document.getElementById("edit-q-marks").value = q.marks || 1.0;
  document.getElementById("edit-q-explanation").value = q.explanation || "";

  // Set options & correct radio
  const corrIdx = q.correct_option_index || 0;
  for (let i = 0; i < 4; i++) {
    const optVal = q.options && q.options[i] ? q.options[i].option_text : "";
    document.getElementById(`edit-opt-${i}`).value = optVal;
    const radio = document.getElementById(`opt-radio-${i}`);
    if (radio) radio.checked = i === corrIdx;
  }

  if (editModalInstance) editModalInstance.show();
}

async function handleSaveQuestionEdit() {
  const qId = document.getElementById("edit-q-id").value;
  const qText = (document.getElementById("edit-q-text").value || "").trim();
  const qTopic = (document.getElementById("edit-q-topic").value || "").trim();
  const qDiff = document.getElementById("edit-q-diff").value;
  const qMarks = parseFloat(document.getElementById("edit-q-marks").value) || 1.0;
  const qExplanation = (document.getElementById("edit-q-explanation").value || "").trim();

  const options = [];
  for (let i = 0; i < 4; i++) {
    const val = (document.getElementById(`edit-opt-${i}`).value || "").trim();
    if (!val) {
      alert(`Option ${String.fromCharCode(65 + i)} cannot be empty.`);
      return;
    }
    options.push(val);
  }

  let correctIdx = 0;
  const radios = document.getElementsByName("edit-correct-opt");
  for (let r of radios) {
    if (r.checked) {
      correctIdx = parseInt(r.value, 10);
      break;
    }
  }

  const payload = {
    question: qText,
    topic_name: qTopic,
    difficulty: qDiff,
    marks: qMarks,
    options: options,
    correct_option_index: correctIdx,
    explanation: qExplanation,
  };

  try {
    const res = await api.put(`/aptitude/questions/${qId}`, payload);
    if (res.success && res.data) {
      if (editModalInstance) editModalInstance.hide();
      showAlert("Question updated successfully!", "success");

      // Update in memory
      if (currentTest && currentTest.questions) {
        const idx = currentTest.questions.findIndex((x) => x.id === qId);
        if (idx > -1) {
          currentTest.questions[idx] = res.data;
          // Recalculate total marks
          currentTest.total_marks = currentTest.questions.reduce((sum, q) => sum + (q.marks || 1.0), 0);
          renderQuestionStudio(currentTest);
        }
      }
    } else {
      alert(res.message || "Failed to update question.");
    }
  } catch (err) {
    console.error("Save question error:", err);
    alert(err.message || "Failed to save question.");
  }
}

// ==============================================================================
// 4. REGENERATE SINGLE QUESTION
// ==============================================================================

async function handleRegenerateQuestion(questionId, btnEl) {
  if (!confirm("Regenerate this question with a fresh problem statement and options using AI?")) {
    return;
  }

  const originalHtml = btnEl.innerHTML;
  btnEl.disabled = true;
  btnEl.innerHTML = `<span class="spinner-border spinner-border-sm" role="status"></span>`;

  try {
    const res = await api.post(`/aptitude/questions/${questionId}/regenerate`, {});
    if (res.success && res.data) {
      showAlert("Question regenerated successfully!", "success");
      if (currentTest && currentTest.questions) {
        const idx = currentTest.questions.findIndex((x) => x.id === questionId);
        if (idx > -1) {
          currentTest.questions[idx] = res.data;
          renderQuestionStudio(currentTest);
        }
      }
    } else {
      showAlert(res.message || "Failed to regenerate question.", "danger");
    }
  } catch (err) {
    console.error("Regenerate question error:", err);
    showAlert(err.message || "Failed to regenerate question.", "danger");
  } finally {
    btnEl.disabled = false;
    btnEl.innerHTML = originalHtml;
  }
}

// ==============================================================================
// 5. DELETE QUESTION
// ==============================================================================

async function handleDeleteQuestion(questionId) {
  if (!confirm("Are you sure you want to delete this question? Total marks will be updated.")) {
    return;
  }

  try {
    const res = await api.delete(`/aptitude/questions/${questionId}`);
    if (res.success) {
      showAlert("Question deleted.", "info");
      if (currentTest && currentTest.questions) {
        currentTest.questions = currentTest.questions.filter((x) => x.id !== questionId);
        currentTest.total_questions = currentTest.questions.length;
        currentTest.total_marks = currentTest.questions.reduce((sum, q) => sum + (q.marks || 1.0), 0);
        renderQuestionStudio(currentTest);
      }
    } else {
      showAlert(res.message || "Failed to delete question.", "danger");
    }
  } catch (err) {
    console.error("Delete question error:", err);
    showAlert(err.message || "Failed to delete question.", "danger");
  }
}

// ==============================================================================
// 6. PUBLISH CURRENT TEST
// ==============================================================================

async function handlePublishCurrentTest() {
  if (!currentTest || !currentTest.id) return;

  if (!confirm(`Are you ready to approve and publish "${currentTest.title}"? Candidates will immediately be able to take this assessment.`)) {
    return;
  }

  const btn = document.getElementById("btn-publish-test");
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status"></span> Publishing...`;

  try {
    const res = await api.post(`/aptitude/tests/${currentTest.id}/publish`, {});
    if (res.success && res.data) {
      currentTest = res.data;
      showAlert("🎉 Test published successfully! It is now live for all candidates.", "success");
      renderQuestionStudio(currentTest);
    } else {
      showAlert(res.message || "Failed to publish test.", "danger");
      btn.disabled = false;
      btn.innerHTML = "🚀 Approve & Publish Test &rarr;";
    }
  } catch (err) {
    console.error("Publish test error:", err);
    showAlert(err.message || "Failed to publish test.", "danger");
    btn.disabled = false;
    btn.innerHTML = "🚀 Approve & Publish Test &rarr;";
  }
}

// ==============================================================================
// 7. LOAD RECRUITER TESTS LIBRARY
// ==============================================================================

async function loadRecruiterTests() {
  const tbody = document.getElementById("tests-table-body");
  if (!tbody) return;
  tbody.innerHTML = `<tr><td colspan="8" class="text-center py-4 text-muted"><span class="spinner-border spinner-border-sm me-2"></span> Loading your tests...</td></tr>`;

  try {
    const res = await api.get("/aptitude/tests?status=all");
    if (res.success && res.data) {
      if (res.data.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" class="text-center py-4 text-muted">No tests created yet. Click "Create New Test" above to generate your first test!</td></tr>`;
        return;
      }

      tbody.innerHTML = res.data
        .map((t) => {
          const isPub = t.status === "published";
          const topicsBadges = (t.topics || [])
            .map((top) => `<span class="badge bg-light text-dark border me-1">${escapeHtml(top)}</span>`)
            .join("");

          return `
          <tr>
            <td>
              <div class="fw-bold text-dark">${escapeHtml(t.title)}</div>
              <div class="mt-1">${topicsBadges || '<span class="text-muted small">General Aptitude</span>'}</div>
            </td>
            <td><strong>${t.total_questions}</strong></td>
            <td><strong>${t.total_marks.toFixed(1)}</strong></td>
            <td>${t.duration_minutes}m</td>
            <td class="text-capitalize">${escapeHtml(t.difficulty || "mixed")}</td>
            <td>
              ${
                isPub
                  ? `<span class="badge bg-success text-white px-2 py-1 rounded-pill">✓ Published</span>`
                  : `<span class="badge bg-warning text-dark px-2 py-1 rounded-pill">Draft</span>`
              }
            </td>
            <td>
              <span class="badge bg-info-subtle text-info-emphasis rounded-pill px-2.5 py-1">
                ${t.attempts_count || 0} candidate${t.attempts_count === 1 ? "" : "s"}
              </span>
            </td>
            <td class="text-end text-nowrap">
              <button class="btn btn-sm btn-outline-primary rounded-pill px-3 me-1" onclick="openTestInStudio('${t.id}')">
                🔍 Studio
              </button>
              <button class="btn btn-sm btn-outline-secondary rounded-pill px-2.5" onclick="viewCandidateResults('${t.id}', '${escapeJs(t.title)}')">
                📊 Results
              </button>
            </td>
          </tr>
        `;
        })
        .join("");
    } else {
      tbody.innerHTML = `<tr><td colspan="8" class="text-center py-4 text-danger">Failed to load tests.</td></tr>`;
    }
  } catch (err) {
    console.error("Load tests error:", err);
    tbody.innerHTML = `<tr><td colspan="8" class="text-center py-4 text-danger">${escapeHtml(err.message || "Failed to load tests")}</td></tr>`;
  }
}

async function openTestInStudio(testId) {
  showAlert("Loading test into studio...", "info");
  try {
    const res = await api.get(`/aptitude/tests/${testId}`);
    if (res.success && res.data) {
      currentTest = res.data;
      renderQuestionStudio(currentTest);
      switchView("studio-view");
      hideAlert();
    } else {
      showAlert(res.message || "Could not load test details.", "danger");
    }
  } catch (err) {
    console.error("Open test in studio error:", err);
    showAlert(err.message || "Could not load test details.", "danger");
  }
}

// ==============================================================================
// 8. VIEW CANDIDATE RESULTS
// ==============================================================================

async function viewCandidateResults(testId, testTitle) {
  const modalTitle = document.getElementById("results-modal-title");
  if (modalTitle) modalTitle.textContent = `📊 Candidate Results: ${testTitle}`;

  const tbody = document.getElementById("results-table-body");
  if (tbody) {
    tbody.innerHTML = `<tr><td colspan="8" class="text-center py-4 text-muted"><span class="spinner-border spinner-border-sm me-2"></span> Loading candidate submissions...</td></tr>`;
  }

  if (resultsModalInstance) resultsModalInstance.show();

  try {
    const res = await api.get(`/aptitude/tests/${testId}/results`);
    if (res.success && res.data) {
      if (res.data.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" class="text-center py-4 text-muted">No candidates have taken this assessment yet.</td></tr>`;
        return;
      }

      tbody.innerHTML = res.data
        .map((att) => {
          const passBadge = att.passed
            ? `<span class="badge bg-success text-white rounded-pill px-2.5 py-1">Passed</span>`
            : `<span class="badge bg-danger text-white rounded-pill px-2.5 py-1">Failed</span>`;

          const submittedStr = att.submitted_at ? new Date(att.submitted_at).toLocaleString() : "—";
          const timeMins = att.time_taken_seconds ? `${Math.round(att.time_taken_seconds / 60)} mins` : "—";

          return `
          <tr>
            <td class="fw-bold">${escapeHtml(att.candidate_name)}</td>
            <td class="text-muted small">${escapeHtml(att.candidate_email)}</td>
            <td><span class="badge bg-light text-dark border">${escapeHtml(att.status)}</span></td>
            <td><strong>${att.score !== null ? att.score.toFixed(1) : "—"} / ${att.total_marks || "—"}</strong></td>
            <td><strong>${att.percentage !== null ? att.percentage.toFixed(1) + "%" : "—"}</strong></td>
            <td>${passBadge}</td>
            <td>${timeMins}</td>
            <td class="text-muted small">${submittedStr}</td>
          </tr>
        `;
        })
        .join("");
    } else {
      tbody.innerHTML = `<tr><td colspan="8" class="text-center py-4 text-danger">Failed to load candidate results.</td></tr>`;
    }
  } catch (err) {
    console.error("View candidate results error:", err);
    tbody.innerHTML = `<tr><td colspan="8" class="text-center py-4 text-danger">${escapeHtml(err.message || "Failed to load results")}</td></tr>`;
  }
}

// ==============================================================================
// UTILITIES
// ==============================================================================

function showAlert(message, type = "info") {
  const alertEl = document.getElementById("status-alert");
  if (!alertEl) return;
  alertEl.className = `alert alert-${type} py-3 shadow-sm rounded-3 d-flex align-items-center justify-content-between`;
  alertEl.innerHTML = `
    <div>${message}</div>
    <button type="button" class="btn-close" onclick="hideAlert()" aria-label="Close"></button>
  `;
  alertEl.classList.remove("d-none");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function hideAlert() {
  const alertEl = document.getElementById("status-alert");
  if (alertEl) alertEl.classList.add("d-none");
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function escapeJs(str) {
  if (!str) return "";
  return String(str).replace(/'/g, "\\'").replace(/"/g, '\\"');
}
