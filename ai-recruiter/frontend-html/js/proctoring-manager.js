/**
 * proctoring-manager.js — Unified Client-Side Proctoring & Integrity Orchestrator.
 * Works seamlessly across Technical Coding Assessments and AI Video Interviews.
 *
 * Capabilities:
 *  1. Candidate Permission & Pre-Check modal (Camera, Mic, Face & Audio detection with live preview).
 *  2. Real-time camera monitoring with 5s debounced face-loss & multiple faces warning toasts.
 *  3. Browser tab switching & focus monitoring (TAB_SWITCH, TAB_RETURN, WINDOW_BLUR, WINDOW_FOCUS) with max 3 warnings.
 *  4. Copy / Paste / Cut monitoring (COPY_ATTEMPT, PASTE_ATTEMPT, CUT_ATTEMPT).
 *  5. Audio level & spike monitoring (HIGH_AUDIO_SPIKE, MIC_MUTED_OR_DISCONNECTED).
 *  6. Real-time floating proctoring HUD status badge with live connection & warning counters.
 *  7. Speech-to-Text streaming for AI live interview dialogue turns.
 *  8. Resilient offline event queue with automatic retries.
 */

class ProctoringManager {
  constructor(config = {}) {
    this.mode = config.mode || "assessment"; // "assessment" | "interview"
    this.attemptId = config.attemptId || null;
    this.interviewId = config.interviewId || null;
    this.assessmentId = config.assessmentId || null;
    this.videoElement = config.videoElement || null;
    this.maxTabWarnings = config.maxTabWarnings || 3;
    this.onEventLogged = config.onEventLogged || (() => {});

    this.stream = null;
    this.cameraDetector = null;
    this.audioDetector = null;
    this.speechToText = null;

    this.eventQueue = [];
    this.isFlushingQueue = false;
    this.flushInterval = null;

    this.tabSwitchCount = 0;
    this.copyPasteCount = 0;
    this.isTabHidden = false;
    this.tabHiddenStartTime = null;

    this.hudElement = null;
    this.preCheckModalEl = null;
    this.identitySnapshot = null;
    this.isActive = false;

    // Bind event handlers
    this.handleVisibilityChange = this.handleVisibilityChange.bind(this);
    this.handleWindowBlur = this.handleWindowBlur.bind(this);
    this.handleWindowFocus = this.handleWindowFocus.bind(this);
    this.handleCopy = this.handleCopy.bind(this);
    this.handlePaste = this.handlePaste.bind(this);
    this.handleCut = this.handleCut.bind(this);
  }

  // ==========================================
  // 1. PRE-CHECK SYSTEM & PERMISSION MODAL
  // ==========================================
  showPreCheckModal(options = {}) {
    return new Promise((resolve, reject) => {
      // Create modal container
      const modalId = "proctoring-precheck-modal";
      const existing = document.getElementById(modalId);
      if (existing) existing.remove();

      const modalWrapper = document.createElement("div");
      modalWrapper.id = modalId;
      modalWrapper.style.cssText = `
        position: fixed; inset: 0; z-index: 10000;
        background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(8px);
        display: flex; align-items: center; justify-content: center;
        padding: 1rem; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      `;

      const title = this.mode === "interview" ? "AI Video Interview Proctoring Pre-Check" : "Technical Assessment System & Proctoring Check";
      const desc = this.mode === "interview"
        ? "Before beginning your AI Video Interview, please verify your camera and microphone setup. Live proctoring and dialogue recording will remain active throughout the session."
        : "To maintain test integrity, your assessment session is monitored. Please verify your camera, microphone, and browser permissions below.";

      modalWrapper.innerHTML = `
        <div style="background: #ffffff; color: #1e293b; border-radius: 16px; max-width: 620px; width: 100%; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.35); overflow: hidden; border: 1px solid #e2e8f0; animation: modalFadeIn 0.3s ease;">
          <div style="background: linear-gradient(135deg, #2563eb, #1d4ed8); color: #fff; padding: 1.25rem 1.5rem; display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
              <div style="width: 36px; height: 36px; border-radius: 10px; background: rgba(255,255,255,0.2); display: flex; align-items: center; justify-content: center; font-size: 1.2rem;">🛡️</div>
              <div>
                <h3 style="margin: 0; font-size: 1.15rem; font-weight: 700; color: #fff;">${title}</h3>
                <span style="font-size: 0.8rem; opacity: 0.9;">Secure AI Proctoring Environment</span>
              </div>
            </div>
          </div>

          <div style="padding: 1.5rem; max-height: calc(85vh - 120px); overflow-y: auto;">
            <p style="margin: 0 0 1rem 0; font-size: 0.9rem; color: #64748b; line-height: 1.5;">${desc}</p>

            <!-- Video Preview Box -->
            <div style="position: relative; width: 100%; height: 220px; background: #0f172a; border-radius: 12px; overflow: hidden; margin-bottom: 1.25rem; display: flex; align-items: center; justify-content: center;">
              <video id="precheck-preview-video" autoplay playsinline muted style="width: 100%; height: 100%; object-fit: cover; transform: scaleX(-1);"></video>
              <div id="precheck-preview-overlay" style="position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; background: rgba(15,23,42,0.7); color: #fff;">
                <div class="spinner-border text-primary mb-2" role="status" style="width: 2rem; height: 2rem;"></div>
                <span style="font-size: 0.85rem;">Requesting device access...</span>
              </div>
              <div id="precheck-face-badge" style="position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.6); backdrop-filter: blur(4px); color: #fff; padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; display: none;">
                Face: Detecting...
              </div>
            </div>

            <!-- Check Items Grid -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-bottom: 1.25rem;">
              <div id="chk-camera" style="display: flex; align-items: center; gap: 0.6rem; padding: 0.75rem 1rem; border: 1px solid #e2e8f0; border-radius: 10px; background: #f8fafc;">
                <span id="chk-camera-icon" style="font-size: 1.2rem;">⏳</span>
                <div>
                  <div style="font-size: 0.85rem; font-weight: 600;">Camera</div>
                  <div id="chk-camera-status" style="font-size: 0.75rem; color: #64748b;">Connecting...</div>
                </div>
              </div>

              <div id="chk-mic" style="display: flex; align-items: center; gap: 0.6rem; padding: 0.75rem 1rem; border: 1px solid #e2e8f0; border-radius: 10px; background: #f8fafc;">
                <span id="chk-mic-icon" style="font-size: 1.2rem;">⏳</span>
                <div>
                  <div style="font-size: 0.85rem; font-weight: 600;">Microphone</div>
                  <div id="chk-mic-status" style="font-size: 0.75rem; color: #64748b;">Connecting...</div>
                </div>
              </div>

              <div id="chk-face" style="display: flex; align-items: center; gap: 0.6rem; padding: 0.75rem 1rem; border: 1px solid #e2e8f0; border-radius: 10px; background: #f8fafc;">
                <span id="chk-face-icon" style="font-size: 1.2rem;">⏳</span>
                <div>
                  <div style="font-size: 0.85rem; font-weight: 600;">Face Detected</div>
                  <div id="chk-face-status" style="font-size: 0.75rem; color: #64748b;">Analyzing view...</div>
                </div>
              </div>

              <div id="chk-audio" style="display: flex; align-items: center; gap: 0.6rem; padding: 0.75rem 1rem; border: 1px solid #e2e8f0; border-radius: 10px; background: #f8fafc;">
                <span id="chk-audio-icon" style="font-size: 1.2rem;">⏳</span>
                <div>
                  <div style="font-size: 0.85rem; font-weight: 600;">Audio Level</div>
                  <div id="chk-audio-status" style="font-size: 0.75rem; color: #64748b;">Listening...</div>
                </div>
              </div>
            </div>

            <!-- Monitoring Notice Box -->
            <div style="background: #eff6ff; border-left: 4px solid #3b82f6; padding: 0.75rem 1rem; border-radius: 6px; font-size: 0.8rem; color: #1e40af; margin-bottom: 1.25rem;">
              <strong>Proctoring Notice:</strong> Camera presence, window/tab switching, and audio integrity events are recorded and included in your submission summary for recruiter audit.
            </div>

            <div id="precheck-error-msg" style="display: none; padding: 0.75rem; background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; color: #dc2626; font-size: 0.85rem; margin-bottom: 1rem;"></div>
          </div>

          <div style="background: #f8fafc; border-top: 1px solid #e2e8f0; padding: 1rem 1.5rem; display: flex; align-items: center; justify-content: flex-end; gap: 0.75rem;">
            <button id="precheck-retry-btn" style="padding: 0.6rem 1.2rem; border-radius: 8px; border: 1px solid #cbd5e1; background: #fff; color: #475569; font-weight: 600; font-size: 0.85rem; cursor: pointer; display: none;">Retry Permissions</button>
            <button id="precheck-start-btn" disabled style="padding: 0.6rem 1.4rem; border-radius: 8px; border: none; background: #2563eb; color: #fff; font-weight: 600; font-size: 0.9rem; cursor: not-allowed; opacity: 0.5; transition: all 0.2s;">
              Confirm & Start Session
            </button>
          </div>
        </div>
      `;

      document.body.appendChild(modalWrapper);
      this.preCheckModalEl = modalWrapper;

      const videoEl = modalWrapper.querySelector("#precheck-preview-video");
      const overlayEl = modalWrapper.querySelector("#precheck-preview-overlay");
      const faceBadge = modalWrapper.querySelector("#precheck-face-badge");
      const startBtn = modalWrapper.querySelector("#precheck-start-btn");
      const retryBtn = modalWrapper.querySelector("#precheck-retry-btn");
      const errorMsg = modalWrapper.querySelector("#precheck-error-msg");

      let hasCamera = false;
      let hasMic = false;
      let faceDetected = false;
      let audioLevelDetected = false;

      const updateStartButton = () => {
        if (hasCamera && hasMic) {
          startBtn.disabled = false;
          startBtn.style.opacity = "1";
          startBtn.style.cursor = "pointer";
          startBtn.style.background = "#10b981";
          startBtn.textContent = "✓ Confirm & Start Session";
        }
      };

      const startMediaCheck = async () => {
        errorMsg.style.display = "none";
        retryBtn.style.display = "none";
        overlayEl.style.display = "flex";

        try {
          const stream = await navigator.mediaDevices.getUserMedia({
            video: { width: { ideal: 640 }, height: { ideal: 480 }, facingMode: "user" },
            audio: true,
          });

          this.stream = stream;
          videoEl.srcObject = stream;
          overlayEl.style.display = "none";

          // Camera Check Passed
          hasCamera = stream.getVideoTracks().length > 0;
          const camIcon = modalWrapper.querySelector("#chk-camera-icon");
          const camStatus = modalWrapper.querySelector("#chk-camera-status");
          if (hasCamera) {
            camIcon.textContent = "✅";
            camStatus.textContent = "Connected ✓";
            camStatus.style.color = "#16a34a";
          }

          // Microphone Check Passed
          hasMic = stream.getAudioTracks().length > 0;
          const micIcon = modalWrapper.querySelector("#chk-mic-icon");
          const micStatus = modalWrapper.querySelector("#chk-mic-status");
          if (hasMic) {
            micIcon.textContent = "✅";
            micStatus.textContent = "Connected ✓";
            micStatus.style.color = "#16a34a";
          }

          // Initialize Face Detector for Pre-Check Preview
          faceBadge.style.display = "block";
          const preCheckFaceDetector = new ProctorCameraDetector(videoEl, {
            intervalMs: 600,
            onFaceUpdate: (f) => {
              const faceIcon = modalWrapper.querySelector("#chk-face-icon");
              const faceStatus = modalWrapper.querySelector("#chk-face-status");
              if (f.count >= 1) {
                faceDetected = true;
                faceIcon.textContent = "✅";
                faceStatus.textContent = "Face visible ✓";
                faceStatus.style.color = "#16a34a";
                faceBadge.textContent = "✓ Face Detected";
                faceBadge.style.background = "rgba(16, 185, 129, 0.8)";
              } else {
                faceIcon.textContent = "⚠️";
                faceStatus.textContent = "Face not detected";
                faceStatus.style.color = "#ea580c";
                faceBadge.textContent = "⚠️ Position Face";
                faceBadge.style.background = "rgba(234, 88, 12, 0.8)";
              }
              updateStartButton();
            },
          });
          preCheckFaceDetector.start();

          // Initialize Audio Detector for Pre-Check Preview
          const preCheckAudioDetector = new ProctorAudioDetector({
            onAudioStateChange: (a) => {
              const audIcon = modalWrapper.querySelector("#chk-audio-icon");
              const audStatus = modalWrapper.querySelector("#chk-audio-status");
              if (a.decibels > -90) {
                audioLevelDetected = true;
                audIcon.textContent = "✅";
                audStatus.textContent = `Active (${a.decibels} dB) ✓`;
                audStatus.style.color = "#16a34a";
              }
              updateStartButton();
            },
          });
          preCheckAudioDetector.start(stream);

          updateStartButton();

          // Action on Start Click
          startBtn.onclick = async () => {
            // Capture reference snapshot
            this.identitySnapshot = preCheckFaceDetector.captureSnapshot();

            // Stop precheck preview timers
            preCheckFaceDetector.stop();
            preCheckAudioDetector.stop();

            // Send explicit consent to backend
            try {
              if (window.proctoringAPI && window.proctoringAPI.submitUnifiedConsent) {
                await window.proctoringAPI.submitUnifiedConsent({
                  attempt_id: this.attemptId,
                  interview_id: this.interviewId,
                  assessment_id: this.assessmentId,
                  camera_consent: true,
                  microphone_consent: true,
                  browser_consent: true,
                  clipboard_consent: true,
                  identity_reference_image: this.identitySnapshot,
                });
              }
            } catch (err) {
              console.warn("Consent recording note:", err);
            }

            modalWrapper.remove();
            this.preCheckModalEl = null;

            // Start full proctoring monitors
            this.startMonitors(this.stream);
            resolve({ stream: this.stream, snapshot: this.identitySnapshot });
          };
        } catch (err) {
          overlayEl.style.display = "none";
          retryBtn.style.display = "block";
          errorMsg.style.display = "block";
          errorMsg.innerHTML = `<strong>Permission Denied:</strong> ${err.message || "Please allow camera and microphone permissions in your browser settings to proceed."}`;

          const camIcon = modalWrapper.querySelector("#chk-camera-icon");
          const camStatus = modalWrapper.querySelector("#chk-camera-status");
          camIcon.textContent = "❌";
          camStatus.textContent = "Permission Blocked";
          camStatus.style.color = "#dc2626";

          const micIcon = modalWrapper.querySelector("#chk-mic-icon");
          const micStatus = modalWrapper.querySelector("#chk-mic-status");
          micIcon.textContent = "❌";
          micStatus.textContent = "Permission Blocked";
          micStatus.style.color = "#dc2626";
        }
      };

      retryBtn.onclick = () => startMediaCheck();
      startMediaCheck();
    });
  }

  // ==========================================
  // 2. REAL-TIME MONITORS (CAM, AUDIO, TAB, CLIPBOARD)
  // ==========================================
  startMonitors(stream) {
    if (this.isActive) return;
    this.isActive = true;
    this.stream = stream || this.stream;

    // Attach stream to active video element if specified
    if (this.videoElement && this.stream) {
      this.videoElement.srcObject = this.stream;
      this.videoElement.play().catch(() => {});
    }

    // 1. Camera Monitoring
    const activeVid = this.videoElement || document.querySelector("video");
    if (activeVid) {
      this.cameraDetector = new ProctorCameraDetector(activeVid, {
        intervalMs: 1000,
        noFaceDebounceMs: 5000,
        onFaceUpdate: (f) => this.updateHudFaceStatus(f),
        onNoFaceFlagged: (ev) => {
          this.logEvent("NO_FACE_DETECTED", "medium", { duration_seconds: ev.duration_seconds });
          this.showToast("⚠️ Face Absence Alert", "Candidate face is not detected in the camera frame.", "warning");
        },
        onFaceReturned: (ev) => {
          this.logEvent("FACE_DETECTED_AGAIN", "info", { duration_seconds: ev.duration_seconds });
          this.showToast("✓ Face Detected", "Candidate face has returned to view.", "info");
        },
        onMultipleFaces: (ev) => {
          this.logEvent("MULTIPLE_FACES_DETECTED", "high", { face_count: ev.count });
          this.showToast("⚠️ Multiple Faces Detected", "Multiple faces detected. Please ensure that only you are visible in the camera.", "warning");
        },
      });
      this.cameraDetector.start();
    }

    // 2. Audio Monitoring
    if (this.stream) {
      this.audioDetector = new ProctorAudioDetector({
        noiseThresholdDb: 32,
        onAudioStateChange: (a) => this.updateHudAudioMeter(a),
        onNoiseDetected: (ev) => {
          this.logEvent("AUDIO_ACTIVITY", "low", { decibels: ev.decibels, delta: ev.delta });
        },
        onMicDisconnected: (ev) => {
          this.logEvent("MIC_MUTED_OR_DISCONNECTED", "high");
          this.showToast("⚠️ Microphone Issue", "Microphone stream disconnected or muted.", "warning");
        },
      });
      this.audioDetector.start(this.stream);
    }

    // 3. Tab Switching & Window Focus Monitoring
    document.addEventListener("visibilitychange", this.handleVisibilityChange);
    window.addEventListener("blur", this.handleWindowBlur);
    window.addEventListener("focus", this.handleWindowFocus);

    // 4. Clipboard Monitoring
    document.addEventListener("copy", this.handleCopy);
    document.addEventListener("paste", this.handlePaste);
    document.addEventListener("cut", this.handleCut);

    // 5. Speech-to-Text for Interview Mode
    if (this.mode === "interview" && window.ProctorSpeechToText) {
      this.speechToText = new ProctorSpeechToText({
        speaker: "Candidate",
        onTurn: (turn) => this.handleSpeechTurn(turn),
      });
      this.speechToText.start();
    }

    // 6. Floating Status HUD
    this.createFloatingHud();

    // 7. Flush Offline Queue Periodically
    this.flushInterval = setInterval(() => this.flushQueue(), 6000);
    window.addEventListener("online", () => this.flushQueue());
  }

  stopMonitors() {
    this.isActive = false;

    if (this.cameraDetector) {
      this.cameraDetector.stop();
      this.cameraDetector = null;
    }
    if (this.audioDetector) {
      this.audioDetector.stop();
      this.audioDetector = null;
    }
    if (this.speechToText) {
      this.speechToText.stop();
      this.speechToText = null;
    }

    document.removeEventListener("visibilitychange", this.handleVisibilityChange);
    window.removeEventListener("blur", this.handleWindowBlur);
    window.removeEventListener("focus", this.handleWindowFocus);

    document.removeEventListener("copy", this.handleCopy);
    document.removeEventListener("paste", this.handlePaste);
    document.removeEventListener("cut", this.handleCut);

    if (this.flushInterval) {
      clearInterval(this.flushInterval);
      this.flushInterval = null;
    }

    // Final queue flush
    this.flushQueue();

    if (this.hudElement) {
      this.hudElement.remove();
      this.hudElement = null;
    }
  }

  // ==========================================
  // 3. EVENT HANDLERS & TRACKING
  // ==========================================
  handleVisibilityChange() {
    if (document.hidden) {
      this.isTabHidden = true;
      this.tabHiddenStartTime = Date.now();
      this.tabSwitchCount++;

      this.logEvent("TAB_SWITCH", "medium", {
        switch_count: this.tabSwitchCount,
        max_warnings: this.maxTabWarnings,
      });

      this.updateHudCounters();

      // Show warning toast if within warning threshold
      const warnMsg = this.tabSwitchCount <= this.maxTabWarnings
        ? `Tab switch detected (Warning ${this.tabSwitchCount}/${this.maxTabWarnings}). Please stay on this tab to maintain assessment integrity.`
        : `Tab switch #${this.tabSwitchCount} recorded and flagged in your session integrity report.`;

      this.showToast("⚠️ Tab Switch Warning", warnMsg, this.tabSwitchCount <= this.maxTabWarnings ? "warning" : "danger");
    } else {
      if (this.isTabHidden) {
        const awaySeconds = this.tabHiddenStartTime ? Math.round((Date.now() - this.tabHiddenStartTime) / 1000) : 0;
        this.isTabHidden = false;
        this.tabHiddenStartTime = null;

        this.logEvent("TAB_RETURN", "info", {
          away_seconds: awaySeconds,
        });
      }
    }
  }

  handleWindowBlur() {
    this.logEvent("WINDOW_BLUR", "low", {});
  }

  handleWindowFocus() {
    this.logEvent("WINDOW_FOCUS", "info", {});
  }

  handleCopy(e) {
    this.copyPasteCount++;
    this.updateHudCounters();
    const len = window.getSelection() ? window.getSelection().toString().length : 0;
    this.logEvent("COPY_ATTEMPT", "low", { length: len });
  }

  handlePaste(e) {
    this.copyPasteCount++;
    this.updateHudCounters();
    let text = "";
    if (e.clipboardData) {
      text = e.clipboardData.getData("text") || "";
    }
    this.logEvent("PASTE_ATTEMPT", "medium", { length: text.length });
    this.showToast("ℹ️ Clipboard Logged", "Clipboard paste action recorded in proctoring audit.", "info");
  }

  handleCut(e) {
    this.copyPasteCount++;
    this.updateHudCounters();
    this.logEvent("CUT_ATTEMPT", "low", {});
  }

  handleSpeechTurn(turn) {
    if (!this.interviewId) return;
    if (window.proctoringAPI && window.proctoringAPI.appendTranscript) {
      window.proctoringAPI.appendTranscript(this.interviewId, turn).catch((err) => {
        console.debug("Transcript append queued/skipped:", err);
      });
    }
  }

  // ==========================================
  // 4. EVENT QUEUE & DISPATCHER
  // ==========================================
  logEvent(eventType, severity = "low", metadata = {}) {
    const payload = {
      event_type: eventType,
      severity: severity,
      confidence: 1.0,
      duration_seconds: metadata.duration_seconds || null,
      attempt_id: this.attemptId,
      interview_id: this.interviewId,
      assessment_id: this.assessmentId,
      metadata_json: metadata,
      occurred_at: new Date().toISOString(),
    };

    this.eventQueue.push(payload);
    this.onEventLogged(payload);

    // Attempt immediate dispatch
    this.flushQueue();
  }

  async flushQueue() {
    if (this.isFlushingQueue || !this.eventQueue.length) return;
    this.isFlushingQueue = true;

    const toSend = [...this.eventQueue];
    try {
      if (window.proctoringAPI && window.proctoringAPI.recordBatchEvents) {
        await window.proctoringAPI.recordBatchEvents({
          events: toSend,
          attempt_id: this.attemptId,
          interview_id: this.interviewId,
          assessment_id: this.assessmentId,
        });
        // Remove successfully sent items
        this.eventQueue.splice(0, toSend.length);
      } else if (window.proctoringAPI && window.proctoringAPI.recordEvent) {
        for (let i = 0; i < toSend.length; i++) {
          await window.proctoringAPI.recordEvent(toSend[i]);
          this.eventQueue.shift();
        }
      }
    } catch (err) {
      console.warn("Proctoring events buffered locally (network retry active):", err.message);
    } finally {
      this.isFlushingQueue = false;
    }
  }

  // ==========================================
  // 5. FLOATING HUD & TOAST NOTIFICATIONS
  // ==========================================
  createFloatingHud() {
    if (this.hudElement) return;

    const hud = document.createElement("div");
    hud.id = "proctoring-floating-hud";
    hud.style.cssText = `
      position: fixed; top: 16px; right: 16px; z-index: 9999;
      background: rgba(15, 23, 42, 0.92); backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 12px;
      padding: 8px 14px; color: #fff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      box-shadow: 0 10px 25px -5px rgba(0,0,0,0.4); display: flex; align-items: center; gap: 12px;
      user-select: none; font-size: 0.8rem; transition: all 0.3s ease;
    `;

    hud.innerHTML = `
      <div style="display: flex; align-items: center; gap: 6px;">
        <span style="width: 8px; height: 8px; border-radius: 50%; background: #10b981; box-shadow: 0 0 8px #10b981; animation: hudPulse 2s infinite;"></span>
        <span style="font-weight: 700; letter-spacing: 0.5px; color: #e2e8f0;">PROCTORING</span>
      </div>

      <div style="width: 1px; height: 16px; background: rgba(255,255,255,0.2);"></div>

      <!-- Face Status -->
      <div id="hud-face-indicator" style="display: flex; align-items: center; gap: 4px; color: #10b981;">
        <span id="hud-face-icon">👤</span>
        <span id="hud-face-text" style="font-weight: 600;">Active</span>
      </div>

      <div style="width: 1px; height: 16px; background: rgba(255,255,255,0.2);"></div>

      <!-- Audio Level Meter -->
      <div title="Audio Activity" style="display: flex; align-items: center; gap: 4px;">
        <span>🎙️</span>
        <div style="width: 28px; height: 6px; background: rgba(255,255,255,0.2); border-radius: 3px; overflow: hidden;">
          <div id="hud-audio-bar" style="width: 20%; height: 100%; background: #10b981; transition: width 0.15s ease;"></div>
        </div>
      </div>

      <div style="width: 1px; height: 16px; background: rgba(255,255,255,0.2);"></div>

      <!-- Tab Switch Counter Badge -->
      <div id="hud-tab-badge" title="Tab Switches" style="background: rgba(255,255,255,0.1); padding: 2px 7px; border-radius: 6px; font-weight: 600;">
        📑 <span id="hud-tab-count">0</span>/${this.maxTabWarnings}
      </div>

      <!-- Copy/Paste Counter Badge -->
      <div id="hud-copy-badge" title="Clipboard Actions" style="background: rgba(255,255,255,0.1); padding: 2px 7px; border-radius: 6px; font-weight: 600;">
        📋 <span id="hud-copy-count">0</span>
      </div>
    `;

    document.body.appendChild(hud);
    this.hudElement = hud;

    // Append CSS animations
    if (!document.getElementById("proctoring-styles")) {
      const style = document.createElement("style");
      style.id = "proctoring-styles";
      style.textContent = `
        @keyframes hudPulse {
          0%, 100% { opacity: 1; transform: scale(1); }
          50% { opacity: 0.4; transform: scale(1.1); }
        }
        @keyframes modalFadeIn {
          from { opacity: 0; transform: scale(0.96); }
          to { opacity: 1; transform: scale(1); }
        }
        .proctoring-toast {
          position: fixed; bottom: 24px; right: 24px; z-index: 10001;
          min-width: 300px; max-width: 420px; padding: 12px 16px;
          border-radius: 10px; color: #fff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
          box-shadow: 0 15px 30px rgba(0,0,0,0.3); animation: modalFadeIn 0.3s ease;
          display: flex; align-items: flex-start; gap: 10px; font-size: 0.85rem;
        }
      `;
      document.head.appendChild(style);
    }
  }

  updateHudFaceStatus(face) {
    if (!this.hudElement) return;
    const faceText = this.hudElement.querySelector("#hud-face-text");
    const faceIndicator = this.hudElement.querySelector("#hud-face-indicator");

    if (face.noFaceFlagged) {
      faceIndicator.style.color = "#f97316";
      faceText.textContent = "No Face";
    } else if (face.multipleFaces) {
      faceIndicator.style.color = "#ef4444";
      faceText.textContent = `Multiple (${face.count})`;
    } else {
      faceIndicator.style.color = "#10b981";
      faceText.textContent = "Active";
    }
  }

  updateHudAudioMeter(audio) {
    if (!this.hudElement) return;
    const bar = this.hudElement.querySelector("#hud-audio-bar");
    if (!bar) return;

    const pct = Math.min(100, Math.max(10, Math.round(((audio.decibels + 70) / 70) * 100)));
    bar.style.width = `${pct}%`;
    bar.style.background = audio.speaking ? "#3b82f6" : (pct > 75 ? "#f97316" : "#10b981");
  }

  updateHudCounters() {
    if (!this.hudElement) return;
    const tabEl = this.hudElement.querySelector("#hud-tab-count");
    const copyEl = this.hudElement.querySelector("#hud-copy-count");
    const tabBadge = this.hudElement.querySelector("#hud-tab-badge");

    if (tabEl) tabEl.textContent = this.tabSwitchCount;
    if (copyEl) copyEl.textContent = this.copyPasteCount;

    if (tabBadge) {
      if (this.tabSwitchCount >= this.maxTabWarnings) {
        tabBadge.style.background = "rgba(239, 68, 68, 0.4)";
        tabBadge.style.color = "#fca5a5";
      } else if (this.tabSwitchCount > 0) {
        tabBadge.style.background = "rgba(245, 158, 11, 0.3)";
        tabBadge.style.color = "#fde68a";
      }
    }
  }

  showToast(title, message, type = "info") {
    const toast = document.createElement("div");
    toast.className = "proctoring-toast";

    const bgMap = {
      info: "linear-gradient(135deg, #1e293b, #334155)",
      warning: "linear-gradient(135deg, #b45309, #d97706)",
      danger: "linear-gradient(135deg, #991b1b, #dc2626)",
    };
    toast.style.background = bgMap[type] || bgMap.info;

    toast.innerHTML = `
      <div style="font-size: 1.2rem;">${type === "danger" ? "🚨" : type === "warning" ? "⚠️" : "ℹ️"}</div>
      <div style="flex: 1;">
        <div style="font-weight: 700; margin-bottom: 2px;">${title}</div>
        <div style="opacity: 0.9; line-height: 1.4;">${message}</div>
      </div>
      <button style="background: none; border: none; color: #fff; font-size: 1.1rem; cursor: pointer; opacity: 0.7; padding: 0 0 0 4px;" onclick="this.parentElement.remove()">×</button>
    `;

    document.body.appendChild(toast);
    setTimeout(() => {
      if (toast.parentElement) toast.remove();
    }, 5000);
  }
}

// Attach to window
if (typeof window !== "undefined") {
  window.ProctoringManager = ProctoringManager;
}
