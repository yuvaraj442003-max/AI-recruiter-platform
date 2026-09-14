/**
 * proctoring-detector.js — Real-Time Camera & Audio Proctoring Monitor.
 * Provides client-side face count detection (detecting multiple persons or face loss)
 * and real-time audio noise/external sound monitoring.
 */

class ProctorCameraDetector {
  constructor(videoElement, options = {}) {
    this.videoEl = videoElement;
    this.intervalMs = options.intervalMs || 1000;
    this.onFaceUpdate = options.onFaceUpdate || (() => {});
    this.timer = null;
    this.faceDetector = null;
    this.canvas = document.createElement("canvas");
    this.ctx = this.canvas.getContext("2d", { willReadFrequently: true });
    this.currentFaceCount = 1;
    this.consecutiveMultiCount = 0;
    this.consecutiveNoFaceCount = 0;

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

  async analyzeFrame() {
    if (!this.videoEl || this.videoEl.paused || this.videoEl.ended || !this.videoEl.videoWidth) {
      return;
    }

    let detectedCount = 1; // default neutral assumption

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

    // Debounce state transitions to prevent false positives from brief lighting/shadow glitches
    if (detectedCount > 1) {
      this.consecutiveMultiCount++;
      this.consecutiveNoFaceCount = 0;
    } else if (detectedCount === 0) {
      this.consecutiveNoFaceCount++;
      this.consecutiveMultiCount = 0;
    } else {
      this.consecutiveMultiCount = 0;
      this.consecutiveNoFaceCount = 0;
    }

    let finalState = "NORMAL";
    let reportedCount = 1;

    if (this.consecutiveMultiCount >= 1) {
      finalState = "MULTIPLE_FACES";
      reportedCount = Math.max(2, detectedCount);
    } else if (this.consecutiveNoFaceCount >= 2) {
      finalState = "NO_FACE";
      reportedCount = 0;
    }

    this.currentFaceCount = reportedCount;
    this.onFaceUpdate({
      count: reportedCount,
      state: finalState,
      message:
        finalState === "MULTIPLE_FACES"
          ? `⚠️ Anti-Cheating Alert: Multiple persons (${reportedCount}) detected in camera frame!`
          : finalState === "NO_FACE"
          ? "⚠️ Anti-Cheating Alert: Candidate face lost from camera frame!"
          : "Camera monitoring active — single person confirmed ✓",
    });
  }

  /**
   * Canvas-based skin-tone & face contour blob detection algorithm.
   * Runs locally on canvas pixel buffers when native FaceDetector is unavailable.
   */
  canvasFallbackDetect() {
    const width = 160;
    const height = 120;
    this.canvas.width = width;
    this.canvas.height = height;

    try {
      this.ctx.drawImage(this.videoEl, 0, 0, width, height);
      const imgData = this.ctx.getImageData(0, 0, width, height);
      const data = imgData.data;

      // Map skin pixels into grid cells to detect distinct face regions
      const gridCols = 8;
      const gridRows = 6;
      const cellW = Math.floor(width / gridCols);
      const cellH = Math.floor(height / gridRows);
      const grid = Array.from({ length: gridRows }, () => Array(gridCols).fill(0));

      for (let y = 0; y < height; y += 2) {
        for (let x = 0; x < width; x += 2) {
          const idx = (y * width + x) * 4;
          const r = data[idx];
          const g = data[idx + 1];
          const b = data[idx + 2];

          // Standard Normalized Skin Color Threshold (YCbCr / RGB skin color rule)
          const isSkin =
            r > 60 &&
            g > 35 &&
            b > 20 &&
            r > g &&
            r > b &&
            Math.max(r, g, b) - Math.min(r, g, b) > 15 &&
            Math.abs(r - g) > 15;

          if (isSkin) {
            const col = Math.min(gridCols - 1, Math.floor(x / cellW));
            const row = Math.min(gridRows - 1, Math.floor(y / cellH));
            grid[row][col]++;
          }
        }
      }

      // Count active skin region clusters separated by non-skin columns
      let activeClusters = 0;
      let inCluster = false;
      let clusterDensity = 0;

      for (let col = 0; col < gridCols; col++) {
        let colSkinCount = 0;
        for (let row = 0; row < gridRows; row++) {
          colSkinCount += grid[row][col];
        }

        const isDenseCol = colSkinCount > (cellW * cellH * 0.12);
        if (isDenseCol) {
          if (!inCluster) {
            inCluster = true;
            activeClusters++;
          }
          clusterDensity += colSkinCount;
        } else {
          inCluster = false;
        }
      }

      if (activeClusters >= 2 && clusterDensity > (width * height * 0.18)) {
        return 2; // Multiple face regions detected
      }
      if (clusterDensity < (cellW * cellH * 1.5)) {
        return 0; // Face lost / no skin detected
      }
      return 1; // Single candidate face
    } catch (e) {
      return 1;
    }
  }
}


class ProctorAudioDetector {
  constructor(options = {}) {
    this.noiseThresholdDb = options.noiseThresholdDb || 18; // dB above calibrated baseline
    this.onNoiseDetected = options.onNoiseDetected || (() => {});
    this.onAudioStateChange = options.onAudioStateChange || (() => {});

    this.audioCtx = null;
    this.analyser = null;
    this.source = null;
    this.timer = null;

    this.baselineDb = -50;
    this.calibrated = false;
    this.calibrationSamples = [];
    this.consecutiveNoiseSpikes = 0;
  }

  start(stream) {
    if (!stream || !stream.getAudioTracks().length) return;

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

    // Calculate Root Mean Square (RMS) energy
    let sumSq = 0;
    for (let i = 0; i < dataArray.length; i++) {
      const normalized = dataArray[i] / 255;
      sumSq += normalized * normalized;
    }
    const rms = Math.sqrt(sumSq / dataArray.length);
    const db = rms > 0 ? 20 * Math.log10(rms) : -100;

    // Phase 1: Calibrate ambient baseline sound (first 5 samples = ~2.5 seconds)
    if (!this.calibrated) {
      this.calibrationSamples.push(db);
      if (this.calibrationSamples.length >= 5) {
        const sum = this.calibrationSamples.reduce((a, b) => a + b, 0);
        this.baselineDb = sum / this.calibrationSamples.length;
        this.calibrated = true;
      }
      return;
    }

    // Phase 2: Monitor real-time audio volume vs baseline
    const deltaDb = db - this.baselineDb;

    this.onAudioStateChange({
      decibels: Math.round(db),
      baseline: Math.round(this.baselineDb),
      delta: Math.round(deltaDb),
      rms: rms.toFixed(3),
    });

    // Detect background noise spike or sustained external noise (delta > threshold)
    if (deltaDb >= this.noiseThresholdDb && db > -35) {
      this.consecutiveNoiseSpikes++;

      if (this.consecutiveNoiseSpikes >= 2) {
        this.onNoiseDetected({
          event_type: "SUSPICIOUS_AUDIO",
          decibels: Math.round(db),
          baseline: Math.round(this.baselineDb),
          delta: Math.round(deltaDb),
          message: `⚠️ Anti-Cheating Alert: High background noise or external sound detected (${Math.round(db)} dB, +${Math.round(deltaDb)} dB over baseline)!`,
        });
      }
    } else {
      this.consecutiveNoiseSpikes = Math.max(0, this.consecutiveNoiseSpikes - 1);
    }
  }
}

// Export for browser environment
if (typeof window !== "undefined") {
  window.ProctorCameraDetector = ProctorCameraDetector;
  window.ProctorAudioDetector = ProctorAudioDetector;
}
