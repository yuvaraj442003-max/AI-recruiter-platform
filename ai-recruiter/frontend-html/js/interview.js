/**
 * interview.js — drives the candidate's interview-taking flow:
 * question rendering, TTS speech synthesis, text/voice answers.
 */
(function () {
  const params = new URLSearchParams(window.location.search);
  const interviewId = params.get("interview_id");

  const alertBox = document.getElementById("interview-alert");
  const subtitleEl = document.getElementById("interview-subtitle");
  const progressWrapper = document.getElementById("progress-wrapper");
  const progressLabel = document.getElementById("progress-label");
  const progressBar = document.getElementById("progress-bar");
  const questionCard = document.getElementById("question-card");
  const completedCard = document.getElementById("completed-card");

  const questionTypeBadge = document.getElementById("question-type-badge");
  const questionDifficultyBadge = document.getElementById("question-difficulty-badge");
  const questionText = document.getElementById("question-text");
  const answerText = document.getElementById("answer-text");
  const submitBtn = document.getElementById("submit-answer-btn");
  const submitBtnText = document.getElementById("submit-answer-text");
  const submitSpinner = document.getElementById("submit-answer-spinner");

  const recordBtn = document.getElementById("record-btn");
  const recordingStatus = document.getElementById("recording-status");
  const ttsBtn = document.getElementById("tts-btn");
  const ttsBtnText = document.getElementById("tts-btn-text");

  let mediaRecorder = null;
  let audioChunks = [];
  let currentQuestion = null;
  let isSpeaking = false;

  function showAlert(message, variant) {
    if (!alertBox) return;
    alertBox.textContent = message;
    alertBox.className = `alert alert-${variant} py-2`;
  }

  function difficultyClass(difficulty) {
    const map = { easy: "text-bg-success", medium: "text-bg-warning", hard: "text-bg-danger" };
    return map[difficulty] || "text-bg-secondary";
  }

  function stopSpeech() {
    if ("speechSynthesis" in window) {
      window.speechSynthesis.cancel();
    }
    isSpeaking = false;
    if (ttsBtnText) ttsBtnText.textContent = "Read Question Aloud";
    if (ttsBtn) ttsBtn.className = "btn btn-sm btn-outline-primary fw-semibold d-flex align-items-center gap-1";
    if (questionCard) questionCard.classList.remove("border", "border-primary", "shadow");
  }

  function playSpeech(text) {
    if (!("speechSynthesis" in window)) {
      showAlert("Text-to-Speech is not supported in your browser.", "warning");
      return;
    }

    stopSpeech(); // Cancel any ongoing speech

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;

    utterance.onstart = () => {
      isSpeaking = true;
      if (ttsBtnText) ttsBtnText.textContent = "Stop Reading";
      if (ttsBtn) ttsBtn.className = "btn btn-sm btn-danger fw-semibold d-flex align-items-center gap-1";
      if (questionCard) questionCard.classList.add("border", "border-primary", "shadow");
    };

    utterance.onend = stopSpeech;
    utterance.onerror = stopSpeech;

    window.speechSynthesis.speak(utterance);
  }

  if (ttsBtn) {
    ttsBtn.addEventListener("click", () => {
      if (isSpeaking) {
        stopSpeech();
      } else if (currentQuestion && currentQuestion.question) {
        playSpeech(currentQuestion.question);
      }
    });
  }

  function renderQuestion(interview) {
    stopSpeech();
    const unanswered = interview.questions.find((q) => !q.answered);

    if (!unanswered) {
      questionCard.classList.add("d-none");
      progressWrapper.classList.add("d-none");
      completedCard.classList.remove("d-none");
      document.getElementById("view-report-link").href = `interview-report.html?interview_id=${interview.id}`;
      subtitleEl.textContent = `${interview.job_title} · Completed`;
      return;
    }

    currentQuestion = unanswered;
    const answeredCount = interview.questions.filter((q) => q.answered).length;
    const total = interview.questions.length;

    subtitleEl.textContent = `${interview.job_title} · Question ${answeredCount + 1} of ${total}`;
    progressLabel.textContent = `Question ${answeredCount + 1} of ${total}`;
    progressBar.style.width = `${(answeredCount / total) * 100}%`;
    progressWrapper.classList.remove("d-none");

    questionTypeBadge.textContent = unanswered.question_type.replace("_", " ");
    questionDifficultyBadge.textContent = unanswered.difficulty;
    questionDifficultyBadge.className = `badge ${difficultyClass(unanswered.difficulty)}`;
    questionText.textContent = unanswered.question;
    answerText.value = "";
    questionCard.classList.remove("d-none");
    completedCard.classList.add("d-none");
  }

  async function loadInterview() {
    if (!interviewId) {
      showAlert("No interview specified.", "danger");
      return;
    }
    try {
      const res = await API.interviews.get(interviewId);
      renderQuestion(res.data);
    } catch (err) {
      showAlert(err.message, "danger");
    }
  }

  submitBtn.addEventListener("click", async () => {
    stopSpeech();
    if (!currentQuestion) return;
    const text = answerText.value.trim();
    if (!text) {
      showAlert("Write or record an answer before submitting.", "warning");
      return;
    }

    submitBtn.disabled = true;
    submitSpinner.classList.remove("d-none");
    submitBtnText.textContent = "Submitting...";

    try {
      await API.interviews.answer(interviewId, currentQuestion.id, text);
      const res = await API.interviews.get(interviewId);
      renderQuestion(res.data);
    } catch (err) {
      showAlert(err.message, "danger");
    } finally {
      submitBtn.disabled = false;
      submitSpinner.classList.add("d-none");
      submitBtnText.textContent = "Submit Answer";
    }
  });

  // --- Voice recording (optional; falls back gracefully) ---
  recordBtn.addEventListener("click", async () => {
    stopSpeech();
    if (mediaRecorder && mediaRecorder.state === "recording") {
      mediaRecorder.stop();
      return;
    }

    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      recordingStatus.textContent = "Voice recording isn't supported in this browser — please type your answer.";
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioChunks = [];
      mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data);
      mediaRecorder.onstop = async () => {
        stream.getTracks().forEach((track) => track.stop());
        recordBtn.textContent = "🎤 Start Recording";
        recordingStatus.textContent = "Transcribing...";

        const blob = new Blob(audioChunks, { type: "audio/webm" });
        try {
          const res = await speechAPI.transcribe(blob, "answer.webm");
          answerText.value = res.data.text;
          recordingStatus.textContent = "Transcribed — review your answer below before submitting.";
        } catch (err) {
          recordingStatus.textContent = err.message;
        }
      };

      mediaRecorder.start();
      recordBtn.textContent = "⏹ Stop Recording";
      recordingStatus.textContent = "Recording...";
    } catch {
      recordingStatus.textContent = "Microphone access was denied — please type your answer instead.";
    }
  });

  document.addEventListener("ar:auth-ready", loadInterview);
})();
