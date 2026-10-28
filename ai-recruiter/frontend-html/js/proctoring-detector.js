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
    this.multiFaceDebounceCount = options.multiFaceDebounceCount || 2; // 2 consecutive detections (~2s)
    this.onFaceUpdate = options.onFaceUpdate || (() => {});
    this.onNoFaceFlagged = options.onNoFaceFlagged || (() => {});
    this.onFaceReturned = options.onFaceReturned || (() => {});
    this.onMultipleFaces = options.onMultipleFaces || (() => {});
    this.onMultipleFacesCleared = options.onMultipleFacesCleared || (() => {});

    this.timer = null;
    this.faceDetector = null;
    this.canvas = document.createElement("canvas");
    this.ctx = this.canvas.getContext("2d", { willReadFrequently: true });

    this.currentFaceCount = 0;
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

    let detectedCount = 0;

    if (this.faceDetector) {
      try {
        const faces = await this.faceDetector.detect(this.videoEl);
        // Exclude tiny artifacts (must be at least 35x35 pixels)
        const validFaces = (faces || []).filter(f => f.boundingBox && f.boundingBox.width >= 35 && f.boundingBox.height >= 35);
        detectedCount = validFaces.length;
      } catch (err) {
        detectedCount = this.canvasFallbackDetect();
      }
    } else {
      detectedCount = this.canvasFallbackDetect();
    }

    const now = Date.now();

    // 1. Multiple Faces Handling (Debounced: requires multiFaceDebounceCount consecutive positive detections)
    if (detectedCount > 1) {
      this.consecutiveMultiCount = Math.min(this.multiFaceDebounceCount, this.consecutiveMultiCount + 1);
      if (this.consecutiveMultiCount >= this.multiFaceDebounceCount && !this.multipleFacesFlagged) {
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
      if (this.consecutiveMultiCount === 0 && this.multipleFacesFlagged) {
        this.multipleFacesFlagged = false;
        this.onMultipleFacesCleared({
          count: detectedCount,
          event_type: "MULTIPLE_FACES_CLEARED",
          severity: "info",
          message: "✓ Multiple faces resolved: Only single candidate detected.",
        });
      }
    }

    // 2. No Face Handling (Debounced 5 seconds for cheating violation log)
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
    if (this.multipleFacesFlagged || (detectedCount > 1 && this.consecutiveMultiCount >= this.multiFaceDebounceCount)) {
      state = "MULTIPLE_FACES";
    } else if (detectedCount === 0) {
      state = "NO_FACE";
    }

    this.onFaceUpdate({
      count: detectedCount,
      state: state,
      noFaceFlagged: this.noFaceFlagged,
      multipleFaces: state === "MULTIPLE_FACES",
      message: state === "MULTIPLE_FACES"
        ? `Multiple faces (${detectedCount}) detected in camera view!`
        : (state === "NO_FACE" ? "Face not detected" : "Camera Active ✓")
    });
  }

  verifyBlobTexture(data, canvasWidth, minC, maxC, minR, maxR, cellW, cellH) {
    // Verifies whether a candidate blob has facial luminance variance (eyes, brows, nose, lips).
    // Flat background objects (plain wood doors, beige walls, fabric) have near-zero variance.
    let totalLum = 0;
    let pixelCount = 0;
    const lums = [];

    const startX = Math.floor(minC * cellW);
    const endX = Math.min(canvasWidth - 1, Math.floor((maxC + 1) * cellW));
    const startY = Math.floor(minR * cellH);
    const endY = Math.min(119, Math.floor((maxR + 1) * cellH));

    for (let y = startY; y < endY; y += 2) {
      for (let x = startX; x < endX; x += 2) {
        const idx = (y * canvasWidth + x) * 4;
        const r = data[idx];
        const g = data[idx + 1];
        const b = data[idx + 2];
        const lum = 0.299 * r + 0.587 * g + 0.114 * b;
        lums.push(lum);
        totalLum += lum;
        pixelCount++;
      }
    }

    if (pixelCount < 16) return false;

    const mean = totalLum / pixelCount;
    let varianceSum = 0;
    for (let i = 0; i < pixelCount; i++) {
      const diff = lums[i] - mean;
      varianceSum += diff * diff;
    }
    const stdDev = Math.sqrt(varianceSum / pixelCount);
    // Real face with facial contrast has stdDev >= 8.0
    return stdDev >= 8.0;
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

      // 40 columns x 30 rows grid (each cell is 4x4 px = 16 px)
      const gridCols = 40;
      const gridRows = 30;
      const cellW = width / gridCols;
      const cellH = height / gridRows;
      const skinGrid = Array.from({ length: gridRows }, () => Array(gridCols).fill(0));
      let totalSkinCells = 0;

      for (let r = 0; r < gridRows; r++) {
        for (let c = 0; c < gridCols; c++) {
          const startX = Math.floor(c * cellW);
          const startY = Math.floor(r * cellH);
          let skinPixels = 0;

          for (let sy = 0; sy < 4; sy++) {
            for (let sx = 0; sx < 4; sx++) {
              const px = Math.min(width - 1, startX + sx);
              const py = Math.min(height - 1, startY + sy);
              const idx = (py * width + px) * 4;
              const red = data[idx];
              const green = data[idx + 1];
              const blue = data[idx + 2];

              // Multi-space accurate skin detection:
              // 1. Standard YCbCr chromaticity
              const Y = 0.299 * red + 0.587 * green + 0.114 * blue;
              const Cr = 0.5 * red - 0.418688 * green - 0.081312 * blue + 128;
              const Cb = -0.168736 * red - 0.331264 * green + 0.5 * blue + 128;

              // Reject extreme overexposure / total darkness
              if (Y < 32 || Y > 240) continue;

              // Human skin chrominance cluster: Cr in [133, 173], Cb in [77, 127]
              const isSkinYCbCr = (Cr >= 133 && Cr <= 173 && Cb >= 77 && Cb <= 127);

              // 2. Strict RGB checks to reject plain wood/cardboard/tan walls:
              // Wood & beige walls often have high red & high green with almost no blue,
              // or red and green too close together (yellow), or flat neutral tone.
              const maxRGB = Math.max(red, green, blue);
              const minRGB = Math.min(red, green, blue);
              const isSkinRGB = (
                red > 45 && green > 32 && blue > 20 &&
                red > green &&
                green >= blue &&
                (red - green) >= 12 &&
                (maxRGB - minRGB) >= 14 &&
                (red - minRGB) >= 16 &&
                Math.abs(red - green) <= 110
              );

              // Darker skin tones under indoor lighting
              const isDarkSkin = (
                Y >= 32 && Y <= 110 &&
                red >= 40 && green >= 25 && blue >= 15 &&
                red >= green && (red - minRGB) >= 10 &&
                Cr >= 134 && Cr <= 176 && Cb >= 80 && Cb <= 126
              );

              if ((isSkinYCbCr && isSkinRGB) || isDarkSkin) {
                skinPixels++;
              }
            }
          }

          // Require at least 8 out of 16 pixels (50%) to be skin to count cell as skin
          if (skinPixels >= 8) {
            skinGrid[r][c] = 1;
            totalSkinCells++;
          }
        }
      }

      // If less than 35 skin cells across the entire 1200-cell frame,
      // no human face can possibly be present in camera view.
      if (totalSkinCells < 35) {
        return 0;
      }

      // 2D Connected Component Analysis (BFS flood-fill)
      const visited = Array.from({ length: gridRows }, () => Array(gridCols).fill(false));
      const rawBlobs = [];

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

            // Filter out small noise blobs (< 20 cells).
            // A human head in front of a laptop webcam is at least 30-150 cells.
            if (cells >= 20 && blobWidth >= 3 && blobHeight >= 4) {
              // Verify facial internal luminance texture (rejects flat uniform wood/walls)
              const hasFaceTexture = this.verifyBlobTexture(data, width, minC, maxC, minR, maxR, cellW, cellH);

              rawBlobs.push({
                cells,
                minC, maxC, minR, maxR,
                width: blobWidth,
                height: blobHeight,
                aspectRatio,
                centerC: (minC + maxC) / 2,
                centerR: (minR + maxR) / 2,
                hasFaceTexture,
              });
            }
          }
        }
      }

      if (rawBlobs.length === 0) {
        return 0;
      }

      // Sort candidate blobs by size descending
      rawBlobs.sort((a, b) => b.cells - a.cells);

      // STEP 1: Find the PRIMARY candidate face
      // Must be substantial (cells >= 30), proper aspect ratio, located in upper/middle frame,
      // and have facial variance/texture (not a flat wooden door or beige wall).
      const primaryFace = rawBlobs.find(b =>
        b.cells >= 30 &&
        b.width >= 4 &&
        b.height >= 5 &&
        b.aspectRatio >= 0.70 && b.aspectRatio <= 2.1 &&
        b.centerR <= 22 &&
        b.hasFaceTexture
      );

      // CRITICAL RULE: If no valid primary candidate face exists, NO ONE is in front of the camera!
      // This completely prevents empty rooms with background objects from registering 4 or 5 faces.
      if (!primaryFace) {
        return 0;
      }

      // STEP 2: Detect any SECONDARY persons (real multiple faces)
      const distinctHeads = [primaryFace];

      for (const blob of rawBlobs) {
        if (blob === primaryFace) continue;

        // Exclude bottom edge strips (hands resting on keyboard / desk)
        if (blob.minR >= 22 && blob.aspectRatio < 0.75) {
          continue;
        }

        // Exclude body parts directly below the primary head (neck, shoulders, chest)
        const colDiff = Math.abs(blob.centerC - primaryFace.centerC);
        const isBelowPrimary = blob.centerR > primaryFace.centerR && colDiff <= Math.max(primaryFace.width, blob.width) * 0.7;
        const eDistFromPrimary = Math.hypot(blob.centerC - primaryFace.centerC, blob.centerR - primaryFace.centerR);
        if (isBelowPrimary || eDistFromPrimary < 6.0) {
          continue;
        }

        // To qualify as a genuine SECOND face:
        // Must be a substantial head (cells >= 25, width >= 4, height >= 5),
        // within human head proportions (aspectRatio 0.7 to 1.9),
        // with face texture, and clear spatial separation from all other heads.
        if (
          blob.cells >= 25 &&
          blob.width >= 4 &&
          blob.height >= 5 &&
          blob.aspectRatio >= 0.70 && blob.aspectRatio <= 1.9 &&
          blob.centerR <= 22 &&
          blob.hasFaceTexture
        ) {
          let separated = true;
          for (const head of distinctHeads) {
            const dist = Math.hypot(blob.centerC - head.centerC, blob.centerR - head.centerR);
            if (dist < 6.0) {
              separated = false;
              break;
            }
          }
          if (separated) {
            distinctHeads.push(blob);
          }
        }
      }

      // Cap at reasonable maximum for single proctored camera view
      return Math.min(distinctHeads.length, 3);
    } catch (e) {
      console.warn("Face detection error:", e);
      return 0;
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
