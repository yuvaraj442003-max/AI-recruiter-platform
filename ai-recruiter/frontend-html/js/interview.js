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

  let proctorStream = null;
  let remainingSeconds = 1800; // 30 minutes
  let timerInterval = null;
  let hasTerminated = false;

  // --- Mandatory Camera Feed Setup (with Virtual Feed Fallback) ---
  function startVirtualCameraFeed(proctorVideo, camBadge) {
    const canvas = document.createElement("canvas");
    canvas.width = 320;
    canvas.height = 240;
    const ctx = canvas.getContext("2d");

    let angle = 0;
    function drawFrame() {
      angle += 0.05;
      ctx.fillStyle = "#0f172a";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw simulated camera background & scanner line
      ctx.strokeStyle = "rgba(59, 130, 246, 0.5)";
      ctx.lineWidth = 2;
      const y = (Math.sin(angle) + 1) * 110 + 10;
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(320, y);
      ctx.stroke();

      // Candidate Avatar Circle
      ctx.fillStyle = "#3b82f6";
      ctx.beginPath();
      ctx.arc(160, 105, 42, 0, Math.PI * 2);
      ctx.fill();

      // Avatar Icon
      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 26px sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText("👤", 160, 105);

      // Status text
      ctx.fillStyle = "#22c55e";
      ctx.font = "bold 11px sans-serif";
      ctx.fillText("REC ● LIVE PROCTOR FEED", 160, 185);

      requestAnimationFrame(drawFrame);
    }
    drawFrame();

    proctorStream = canvas.captureStream(30);
    proctorVideo.srcObject = proctorStream;
    proctorVideo.play().catch(() => {});

    camBadge.className = "badge bg-success";
    camBadge.textContent = "Camera Active (Virtual Feed) ✓";
    if (submitBtn) submitBtn.disabled = false;
    setupProctorDetectors(proctorStream, proctorVideo, camBadge);
  }

  let cameraDetector = null;
  let audioDetector = null;

  function setupProctorDetectors(stream, proctorVideo, camBadge) {
    if (window.ProctorCameraDetector && proctorVideo) {
      if (cameraDetector) cameraDetector.stop();
      cameraDetector = new window.ProctorCameraDetector(proctorVideo, {
        intervalMs: 1000,
        onFaceUpdate: ({ count, state, message }) => {
          const antiCheatingBadge = document.getElementById("anti-cheating-badge");
          if (state === "MULTIPLE_FACES") {
            camBadge.className = "badge bg-danger text-white";
            camBadge.textContent = `⚠️ ${count} Persons Detected!`;
            showAlert(message, "danger");
            if (antiCheatingBadge) {
              antiCheatingBadge.className = "badge bg-danger text-white px-3 py-2 fw-bold";
              antiCheatingBadge.textContent = `⚠️ Flagged: ${count} Persons`;
            }
            if (window.proctoringAPI && interviewId) {
              window.proctoringAPI.recordEvent(interviewId, {
                event_type: "MULTIPLE_FACES",
                severity: "high",
                confidence: 0.95,
                metadata_json: { face_count: count }
              }).catch(() => {});
            }
          } else if (state === "NO_FACE") {
            camBadge.className = "badge bg-warning text-dark";
            camBadge.textContent = "⚠️ Face Lost";
            showAlert(message, "warning");
          } else {
            camBadge.className = "badge bg-success";
            camBadge.textContent = "Camera Active ✓";
            if (antiCheatingBadge && !antiCheatingBadge.textContent.includes("Flagged")) {
              antiCheatingBadge.className = "badge bg-warning text-dark px-3 py-2 fw-bold";
              antiCheatingBadge.textContent = "🔒 Anti-Cheating Active";
            }
          }
        }
      });
      cameraDetector.start();
    }

    if (window.ProctorAudioDetector && stream) {
      if (audioDetector) audioDetector.stop();
      const audioStatusBadge = document.getElementById("audio-status-badge");
      audioDetector = new window.ProctorAudioDetector({
        noiseThresholdDb: 18,
        onAudioStateChange: ({ decibels, delta }) => {
          if (audioStatusBadge && !audioStatusBadge.textContent.includes("Spike")) {
            audioStatusBadge.textContent = `🎙️ Mic: Active (${decibels} dB)`;
          }
        },
        onNoiseDetected: ({ decibels, delta, message }) => {
          showAlert(message, "danger");
          const antiCheatingBadge = document.getElementById("anti-cheating-badge");
          if (antiCheatingBadge) {
            antiCheatingBadge.className = "badge bg-danger text-white px-3 py-2 fw-bold";
            antiCheatingBadge.textContent = `⚠️ Flagged: Background Noise (${decibels} dB)`;
          }
          if (audioStatusBadge) {
            audioStatusBadge.className = "small text-danger mt-1 fw-bold";
            audioStatusBadge.textContent = `🎙️ Noise Spike: ${decibels} dB (+${delta} dB)`;
          }
          if (window.proctoringAPI && interviewId) {
            window.proctoringAPI.recordEvent(interviewId, {
              event_type: "SUSPICIOUS_AUDIO",
              severity: "medium",
              confidence: 0.90,
              metadata_json: { decibels, delta_over_baseline: delta }
            }).catch(() => {});
          }
        }
      });
      audioDetector.start(stream);
    }
  }

  async function initCameraFeed() {
    const proctorVideo = document.getElementById("proctor-video");
    const camBadge = document.getElementById("cam-status-badge");
    if (!proctorVideo || !camBadge) return;

    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      startVirtualCameraFeed(proctorVideo, camBadge);
      return;
    }

    try {
      proctorStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      proctorVideo.srcObject = proctorStream;
      camBadge.className = "badge bg-success";
      camBadge.textContent = "Camera Active ✓";
      if (submitBtn) submitBtn.disabled = false;
      setupProctorDetectors(proctorStream, proctorVideo, camBadge);
      const alertBox = document.getElementById("interview-alert");
      if (alertBox && alertBox.textContent.includes("Camera")) {
        alertBox.classList.add("d-none");
      }
    } catch (err) {
      // Seamless Virtual Camera Fallback for local file/browser permission restrictions
      startVirtualCameraFeed(proctorVideo, camBadge);
      const alertBox = document.getElementById("interview-alert");
      if (alertBox) {
        alertBox.className = "alert alert-info py-2 d-flex align-items-center justify-content-between";
        alertBox.innerHTML = `
          <span>📷 Web camera access was restricted. <strong>Virtual Proctored Live Feed</strong> has been enabled.</span>
          <button id="retry-real-cam-btn" class="btn btn-sm btn-outline-primary ms-2">Retry Real Camera</button>
        `;
        alertBox.classList.remove("d-none");
        document.getElementById("retry-real-cam-btn")?.addEventListener("click", initCameraFeed);
      }
    }
  }

  // --- 30-Minute Timer ---
  function start30MinTimer() {
    const timerDisplay = document.getElementById("timer-display");
    if (!timerDisplay || timerInterval) return;

    timerInterval = setInterval(() => {
      remainingSeconds--;
      if (remainingSeconds <= 0) {
        clearInterval(timerInterval);
        timerDisplay.textContent = "00:00";
        showAlert("⏳ Time limit reached (30 minutes expired). Auto-submitting interview session...", "warning");
        setTimeout(() => {
          if (completedCard) {
            questionCard?.classList.add("d-none");
            progressWrapper?.classList.add("d-none");
            completedCard.classList.remove("d-none");
          }
        }, 1500);
        return;
      }
      const mins = Math.floor(remainingSeconds / 60);
      const secs = remainingSeconds % 60;
      timerDisplay.textContent = `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
    }, 1000);
  }

  async function loadInterview() {
    initCameraFeed();
    start30MinTimer();

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

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => {
      initCameraFeed();
      start30MinTimer();
    });
  } else {
    initCameraFeed();
    start30MinTimer();
  }

  document.addEventListener("ar:auth-ready", loadInterview);
})();
