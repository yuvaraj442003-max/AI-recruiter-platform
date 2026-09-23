/**
 * proctoring-detector.js — Real-Time Camera & Audio Proctoring Monitor.
 * Provides client-side face count detection (multiple persons, face absence with 5s debounce, face return),
 * audio level/spike detection, and Speech-to-Text streaming for live interview transcription.
 */

class ProctorCameraDetector {
  constructor(videoElement, options = {}) {
    this.videoEl = videoElement;
    this.intervalMs = options.intervalMs || 1000;
    this.noFaceDebounceMs = options.noFaceDebounceMs || 5000; // 5-second debounce before flagging NO_FACE
    this.onFaceUpdate = options.onFaceUpdate || (() => {});
    this.onNoFaceFlagged = options.onNoFaceFlagged || (() => {});
    this.onFaceReturned = options.onFaceReturned || (() => {});
    this.onMultipleFaces = options.onMultipleFaces || (() => {});

    this.timer = null;
    this.faceDetector = null;
    this.canvas = document.createElement("canvas");
    this.ctx = this.canvas.getContext("2d", { willReadFrequently: true });

    this.currentFaceCount = 1;
    this.noFaceStartTime = null;
    this.noFaceFlagged = false;
    this.multipleFacesFlagged = false;
    this.consecutiveMultiCount = 0;

    // Check Native FaceDetector API support
    if (typeof window !== "undefined" && "FaceDetector" in window) {
      try {
        this.faceDetector = new window.FaceDetector({ fastMode: true, maxDetectedFaces: 10 });
      } catch (e) {
        this.faceDetector = null;
      }
    }
  }

  start() {
    if (this.timer) return;
    this.timer = setInterval(() => this.analyzeFrame(), this.intervalMs);
  }

  stop() {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
  }

  captureSnapshot() {
    try {
      if (!this.videoEl || !this.videoEl.videoWidth) return null;
      const snapCanvas = document.createElement("canvas");
      snapCanvas.width = this.videoEl.videoWidth || 320;
      snapCanvas.height = this.videoEl.videoHeight || 240;
      const sCtx = snapCanvas.getContext("2d");
      sCtx.drawImage(this.videoEl, 0, 0, snapCanvas.width, snapCanvas.height);
      return snapCanvas.toDataURL("image/jpeg", 0.75);
    } catch (e) {
      console.warn("Failed to capture snapshot:", e);
      return null;
    }
  }

  async analyzeFrame() {
    if (!this.videoEl || this.videoEl.paused || this.videoEl.ended || !this.videoEl.videoWidth) {
      return;
    }

    let detectedCount = 1;

    if (this.faceDetector) {
      try {
        const faces = await this.faceDetector.detect(this.videoEl);
        detectedCount = faces.length;
      } catch (err) {
        detectedCount = this.canvasFallbackDetect();
      }
    } else {
      detectedCount = this.canvasFallbackDetect();
    }

    const now = Date.now();

    // 1. Multiple Faces Handling (requires 5 consecutive seconds of 2+ separate faces)
    if (detectedCount > 1) {
      this.consecutiveMultiCount++;
      if (this.consecutiveMultiCount >= 5 && !this.multipleFacesFlagged) {
        this.multipleFacesFlagged = true;
        this.onMultipleFaces({
          count: detectedCount,
          event_type: "MULTIPLE_FACES_DETECTED",
          severity: "high",
          message: `⚠️ Multiple faces (${detectedCount}) detected. Please ensure only you are in camera view.`,
        });
      }
    } else {
      this.consecutiveMultiCount = Math.max(0, this.consecutiveMultiCount - 1);
      if (this.consecutiveMultiCount === 0) {
        this.multipleFacesFlagged = false;
      }
    }

    // 2. No Face Handling (Debounced 5 seconds)
    if (detectedCount === 0) {
      if (!this.noFaceStartTime) {
        this.noFaceStartTime = now;
      } else {
        const elapsed = now - this.noFaceStartTime;
        if (elapsed >= this.noFaceDebounceMs && !this.noFaceFlagged) {
          this.noFaceFlagged = true;
          this.onNoFaceFlagged({
            event_type: "NO_FACE_DETECTED",
            severity: "medium",
            duration_seconds: Math.round(elapsed / 1000),
            message: "⚠️ Face absence detected: Candidate not visible in camera frame.",
          });
        }
      }
    } else {
      // Face is visible
      if (this.noFaceFlagged) {
        const absenceDuration = this.noFaceStartTime ? Math.round((now - this.noFaceStartTime) / 1000) : 5;
        this.noFaceFlagged = false;
        this.onFaceReturned({
          event_type: "FACE_DETECTED_AGAIN",
          severity: "info",
          duration_seconds: absenceDuration,
          message: "✓ Candidate face visible again in camera view.",
        });
      }
      this.noFaceStartTime = null;
    }

    this.currentFaceCount = detectedCount;

    let state = "FACE_DETECTED";
    if (this.multipleFacesFlagged) {
      state = "MULTIPLE_FACES";
    } else if (this.noFaceFlagged) {
      state = "NO_FACE";
    }

    this.onFaceUpdate({
      count: detectedCount,
      state: state,
      noFaceFlagged: this.noFaceFlagged,
      multipleFaces: this.multipleFacesFlagged,
      message: this.multipleFacesFlagged
        ? `Multiple faces (${detectedCount}) detected in camera view!`
        : (this.noFaceFlagged ? "Face not detected" : "Camera Active ✓")
    });
  }

  canvasFallbackDetect() {
    const width = 160;
    const height = 120;
    this.canvas.width = width;
    this.canvas.height = height;

    try {
      this.ctx.drawImage(this.videoEl, 0, 0, width, height);
      const imgData = this.ctx.getImageData(0, 0, width, height);
      const data = imgData.data;

      // 32 columns x 24 rows grid
      const gridCols = 32;
      const gridRows = 24;
      const cellW = width / gridCols;
      const cellH = height / gridRows;
      const skinGrid = Array.from({ length: gridRows }, () => Array(gridCols).fill(0));
      let totalSkinCells = 0;

      for (let r = 0; r < gridRows; r++) {
        for (let c = 0; c < gridCols; c++) {
          const startX = Math.floor(c * cellW);
          const startY = Math.floor(r * cellH);
          let skinPixels = 0;
          const totalSamples = 16;

          for (let sy = 0; sy < 4; sy++) {
            for (let sx = 0; sx < 4; sx++) {
              const px = Math.min(width - 1, startX + sx);
              const py = Math.min(height - 1, startY + sy);
              const idx = (py * width + px) * 4;
              const red = data[idx];
              const green = data[idx + 1];
              const blue = data[idx + 2];

              // Robust human skin color detector across varied skin tones
              const isSkin =
                red > 70 &&
                green > 40 &&
                blue > 25 &&
                red > green &&
                red > blue &&
                (red - green) >= 12 &&
                Math.abs(red - green) <= 130 &&
                (Math.max(red, green, blue) - Math.min(red, green, blue)) >= 15;

              if (isSkin) skinPixels++;
            }
          }

          if (skinPixels >= 5) {
            skinGrid[r][c] = 1;
            totalSkinCells++;
          }
        }
      }

      // If virtually no skin detected anywhere in frame
      if (totalSkinCells < 15) {
        return 0;
      }

      // 2D Connected Component Analysis (BFS flood-fill)
      const visited = Array.from({ length: gridRows }, () => Array(gridCols).fill(false));
      const blobs = [];

      for (let r = 0; r < gridRows; r++) {
        for (let c = 0; c < gridCols; c++) {
          if (skinGrid[r][c] === 1 && !visited[r][c]) {
            let cells = 0;
            let minC = c, maxC = c, minR = r, maxR = r;
            const queue = [[r, c]];
            visited[r][c] = true;

            while (queue.length > 0) {
              const [currR, currC] = queue.shift();
              cells++;
              if (currC < minC) minC = currC;
              if (currC > maxC) maxC = currC;
              if (currR < minR) minR = currR;
              if (currR > maxR) maxR = currR;

              const neighbors = [
                [currR - 1, currC],
                [currR + 1, currC],
                [currR, currC - 1],
                [currR, currC + 1],
              ];

              for (const [nr, nc] of neighbors) {
                if (nr >= 0 && nr < gridRows && nc >= 0 && nc < gridCols && !visited[nr][nc] && skinGrid[nr][nc] === 1) {
                  visited[nr][nc] = true;
                  queue.push([nr, nc]);
                }
              }
            }

            const blobWidth = maxC - minC + 1;
            const blobHeight = maxR - minR + 1;
            const aspectRatio = blobHeight / Math.max(1, blobWidth);

            // Keep blobs that have substantial size and head-like aspect ratio
            if (cells >= 20 && aspectRatio >= 0.6 && aspectRatio <= 2.8) {
              blobs.push({
                cells,
                minC, maxC, minR, maxR,
                width: blobWidth,
                height: blobHeight,
                centerC: (minC + maxC) / 2,
                centerR: (minR + maxR) / 2,
              });
            }
          }
        }
      }

      // If no well-formed blob was extracted, but skin cells exist, treat as 1 face (candidate)
      if (blobs.length === 0) {
        return totalSkinCells >= 20 ? 1 : 0;
      }

      // If only 1 major blob, candidate is alone
      if (blobs.length === 1) {
        return 1;
      }

      // Sort by size descending
      blobs.sort((a, b) => b.cells - a.cells);
      const b1 = blobs[0];
      const b2 = blobs[1];

      // To qualify as MULTIPLE FACES:
      // Both blobs must be large, distinct heads separated horizontally by at least 32% of screen width
      const centerDistC = Math.abs(b1.centerC - b2.centerC);
      const minRequiredSeparation = gridCols * 0.32; // ~10 grid columns
      const bothAreLarge = b1.cells >= 28 && b2.cells >= 28;

      if (bothAreLarge && centerDistC >= minRequiredSeparation) {
        return 2;
      }

      return 1;
    } catch (e) {
      return 1;
    }
  }
}


class ProctorAudioDetector {
  constructor(options = {}) {
    this.noiseThresholdDb = options.noiseThresholdDb || 32; // Set high enough so speech and typing do not trigger alerts
    this.onNoiseDetected = options.onNoiseDetected || (() => {});
    this.onAudioStateChange = options.onAudioStateChange || (() => {});
    this.onMicDisconnected = options.onMicDisconnected || (() => {});

    this.audioCtx = null;
    this.analyser = null;
    this.source = null;
    this.timer = null;
    this.stream = null;

    this.baselineDb = -50;
    this.calibrated = false;
    this.calibrationSamples = [];
    this.consecutiveNoiseSpikes = 0;
    this.continuousVoiceCount = 0;
  }

  start(stream) {
    if (!stream || !stream.getAudioTracks().length) return;
    this.stream = stream;

    // Track disconnection/mute
    const audioTrack = stream.getAudioTracks()[0];
    if (audioTrack) {
      audioTrack.onmute = () => {
        this.onMicDisconnected({
          event_type: "MIC_MUTED_OR_DISCONNECTED",
          severity: "medium",
          message: "⚠️ Microphone muted or disconnected!",
        });
      };
      audioTrack.onended = () => {
        this.onMicDisconnected({
          event_type: "MIC_MUTED_OR_DISCONNECTED",
          severity: "high",
          message: "⚠️ Microphone track ended or hardware unplugged!",
        });
      };
    }

    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return;

      this.audioCtx = new AudioCtx();
      this.analyser = this.audioCtx.createAnalyser();
      this.analyser.fftSize = 512;
      this.analyser.smoothingTimeConstant = 0.8;

      this.source = this.audioCtx.createMediaStreamSource(stream);
      this.source.connect(this.analyser);

      this.timer = setInterval(() => this.analyzeAudio(), 500);
    } catch (err) {
      console.warn("ProctorAudioDetector initialization skipped:", err);
    }
  }

  stop() {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
    if (this.audioCtx) {
      this.audioCtx.close().catch(() => {});
      this.audioCtx = null;
    }
  }

  analyzeAudio() {
    if (!this.analyser) return;

    const dataArray = new Uint8Array(this.analyser.frequencyBinCount);
    this.analyser.getByteFrequencyData(dataArray);

    let sumSq = 0;
    for (let i = 0; i < dataArray.length; i++) {
      const normalized = dataArray[i] / 255;
      sumSq += normalized * normalized;
    }
    const rms = Math.sqrt(sumSq / dataArray.length);
    const db = rms > 0 ? 20 * Math.log10(rms) : -100;

    // Calibration Phase (~2.5 seconds)
    if (!this.calibrated) {
      this.calibrationSamples.push(db);
      if (this.calibrationSamples.length >= 5) {
        const sum = this.calibrationSamples.reduce((a, b) => a + b, 0);
        this.baselineDb = sum / this.calibrationSamples.length;
        this.calibrated = true;
      }
      return;
    }

    const deltaDb = db - this.baselineDb;

    this.onAudioStateChange({
      decibels: Math.round(db),
      baseline: Math.round(this.baselineDb),
      delta: Math.round(deltaDb),
      rms: rms.toFixed(3),
      speaking: deltaDb >= 15 && db > -38,
    });

    // Detect sustained loud ambient noise spike (+32 dB over baseline AND above -22 dB)
    if (deltaDb >= this.noiseThresholdDb && db > -22) {
      this.consecutiveNoiseSpikes++;
      if (this.consecutiveNoiseSpikes === 4) { // Sustained for 2 seconds
        this.onNoiseDetected({
          event_type: "AUDIO_ACTIVITY",
          severity: "low",
          decibels: Math.round(db),
          delta: Math.round(deltaDb),
          message: `Ambient audio activity (+${Math.round(deltaDb)} dB over baseline).`,
        });
      }
    } else {
      this.consecutiveNoiseSpikes = Math.max(0, this.consecutiveNoiseSpikes - 1);
    }
  }
}


/**
 * ProctorSpeechToText — Browser Web Speech API wrapper for real-time AI interview dialogue transcription.
 */
class ProctorSpeechToText {
  constructor(options = {}) {
    this.onTurn = options.onTurn || (() => {});
    this.onError = options.onError || (() => {});
    this.recognition = null;
    this.isListening = false;
    this.accumulatedText = "";

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      this.recognition = new SpeechRecognition();
      this.recognition.continuous = true;
      this.recognition.interimResults = false;
      this.recognition.lang = options.lang || "en-US";

      this.recognition.onresult = (event) => {
        let finalTranscript = "";
        for (let i = event.resultIndex; i < event.results.length; ++i) {
          if (event.results[i].isFinal) {
            finalTranscript += event.results[i][0].transcript + " ";
          }
        }
        finalTranscript = finalTranscript.trim();
        if (finalTranscript) {
          this.accumulatedText += (this.accumulatedText ? " " : "") + finalTranscript;
          this.onTurn({
            speaker: options.speaker || "Candidate",
            text: finalTranscript,
            timestamp: new Date().toTimeString().split(" ")[0],
          });
        }
      };

      this.recognition.onerror = (event) => {
        if (event.error !== "no-speech") {
          console.warn("SpeechRecognition error:", event.error);
          this.onError(event.error);
        }
      };

      this.recognition.onend = () => {
        if (this.isListening) {
          try {
            this.recognition.start();
          } catch (e) {}
        }
      };
    }
  }

  start() {
    if (!this.recognition || this.isListening) return;
    try {
      this.isListening = true;
      this.recognition.start();
    } catch (e) {
      console.warn("Could not start SpeechRecognition:", e);
    }
  }

  stop() {
    if (!this.recognition || !this.isListening) return;
    this.isListening = false;
    try {
      this.recognition.stop();
    } catch (e) {}
  }
}

// Export for browser environment
if (typeof window !== "undefined") {
  window.ProctorCameraDetector = ProctorCameraDetector;
  window.ProctorAudioDetector = ProctorAudioDetector;
  window.ProctorSpeechToText = ProctorSpeechToText;
}
