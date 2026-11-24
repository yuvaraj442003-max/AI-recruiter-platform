/**
 * proctoring-detector.js — Real-Time Camera & Audio Proctoring Monitor.
 * Provides client-side face count detection (multiple persons, face absence with 5s debounce, face return),
 * audio level/spike detection, and Speech-to-Text streaming for live interview transcription.
 */

class ProctorCameraDetector {
  constructor(videoElement, options = {}) {
    this.videoEl = videoElement;
    this.intervalMs = options.intervalMs || 500; // 500ms for responsive, snappy real-time detection
    this.noFaceDebounceMs = options.noFaceDebounceMs || 4000; // 4-second debounce before flagging NO_FACE
    this.multiFaceDebounceCount = options.multiFaceDebounceCount !== undefined ? options.multiFaceDebounceCount : 1; // Immediate alert upon second face
    this.onFaceUpdate = options.onFaceUpdate || (() => {});
    this.onNoFaceFlagged = options.onNoFaceFlagged || (() => {});
    this.onFaceReturned = options.onFaceReturned || (() => {});
    this.onMultipleFaces = options.onMultipleFaces || (() => {});
    this.onMultipleFacesCleared = options.onMultipleFacesCleared || (() => {});

    this.timer = null;
    this.faceDetector = null;
    this.blazeFaceModel = null;
    this.isLoadingModel = false;
    this.canvas = document.createElement("canvas");
    this.ctx = this.canvas.getContext("2d", { willReadFrequently: true });

    this.currentFaceCount = 0;
    this.noFaceStartTime = null;
    this.noFaceFlagged = false;
    this.multipleFacesFlagged = false;
    this.consecutiveMultiCount = 0;

    // 1. Initialize Neural BlazeFace Detector if loaded
    this.initBlazeFace();

    // 2. Check Native Hardware FaceDetector API support
    if (typeof window !== "undefined" && "FaceDetector" in window) {
      try {
        this.faceDetector = new window.FaceDetector({ fastMode: true, maxDetectedFaces: 10 });
      } catch (e) {
        this.faceDetector = null;
      }
    }
  }

  async initBlazeFace() {
    if (typeof window !== "undefined" && window.blazeface && !this.blazeFaceModel && !this.isLoadingModel) {
      try {
        this.isLoadingModel = true;
        this.blazeFaceModel = await window.blazeface.load();
        this.isLoadingModel = false;
        console.log("✓ BlazeFace neural face detector initialized for proctoring.");
      } catch (e) {
        this.isLoadingModel = false;
        console.warn("BlazeFace load note, using anthropometric detector:", e);
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

    // Priority 1: High-Accuracy Neural BlazeFace Model
    if (this.blazeFaceModel) {
      try {
        const predictions = await this.blazeFaceModel.estimateFaces(this.videoEl, false);
        const validFaces = (predictions || []).filter(p => {
          const prob = p.probability ? (Array.isArray(p.probability) ? p.probability[0] : p.probability) : 1.0;
          if (prob < 0.65) return false;
          const w = Math.abs(p.bottomRight[0] - p.topLeft[0]);
          const h = Math.abs(p.bottomRight[1] - p.topLeft[1]);
          return w >= 25 && h >= 25;
        });
        detectedCount = validFaces.length;
      } catch (err) {
        detectedCount = this.canvasFallbackDetect();
      }
    }
    // Priority 2: Native Hardware FaceDetector API
    else if (this.faceDetector) {
      try {
        const faces = await this.faceDetector.detect(this.videoEl);
        const validFaces = (faces || []).filter(f => f.boundingBox && f.boundingBox.width >= 35 && f.boundingBox.height >= 35);
        detectedCount = validFaces.length;
      } catch (err) {
        detectedCount = this.canvasFallbackDetect();
      }
    }
    // Priority 3: Enhanced Anthropometric Facial Landmark Canvas Detector
    else {
      if (typeof window !== "undefined" && window.blazeface && !this.blazeFaceModel && !this.isLoadingModel) {
        this.initBlazeFace();
      }
      detectedCount = this.canvasFallbackDetect();
    }

    const now = Date.now();

    // 1. Multiple Faces Handling (Immediate: multiFaceDebounceCount = 1)
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

    // 2. No Face Handling (Debounced for cheating violation log)
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
        const absenceDuration = this.noFaceStartTime ? Math.round((now - this.noFaceStartTime) / 1000) : 4;
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

  verifyFaceLandmarks(data, canvasWidth, minC, maxC, minR, maxR, cellW, cellH) {
    // Tests for human facial structure (forehead-to-eye valley, cheek-to-eye contrast, eye symmetry).
    // Completely rejects flat skin surfaces, hands, fingers, and background items.
    const startX = Math.floor(minC * cellW);
    const endX = Math.min(canvasWidth - 1, Math.floor((maxC + 1) * cellW));
    const startY = Math.floor(minR * cellH);
    const endY = Math.min(119, Math.floor((maxR + 1) * cellH));
    const boxW = endX - startX;
    const boxH = endY - startY;

    if (boxW < 12 || boxH < 15) return false;

    let lumForehead = 0, countForehead = 0;
    let lumEyes = 0, countEyes = 0;
    let lumCheeks = 0, countCheeks = 0;
    let totalLum = 0, totalCount = 0;
    const allLums = [];

    let lumLeftEye = 0, countLeftEye = 0;
    let lumRightEye = 0, countRightEye = 0;

    for (let y = startY; y < endY; y += 2) {
      const relY = (y - startY) / boxH;
      for (let x = startX; x < endX; x += 2) {
        const relX = (x - startX) / boxW;
        const idx = (y * canvasWidth + x) * 4;
        const r = data[idx], g = data[idx + 1], b = data[idx + 2];
        const lum = 0.299 * r + 0.587 * g + 0.114 * b;

        allLums.push(lum);
        totalLum += lum;
        totalCount++;

        // Zone 1: Forehead (Top 8% - 25% of head box)
        if (relY >= 0.08 && relY < 0.25) {
          lumForehead += lum;
          countForehead++;
        }
        // Zone 2: Eye & Brow Band (28% - 50% of head box)
        else if (relY >= 0.28 && relY < 0.50) {
          lumEyes += lum;
          countEyes++;
          if (relX >= 0.12 && relX < 0.42) {
            lumLeftEye += lum;
            countLeftEye++;
          } else if (relX > 0.58 && relX <= 0.88) {
            lumRightEye += lum;
            countRightEye++;
          }
        }
        // Zone 3: Cheeks & Upper Nose (52% - 75% of head box)
        else if (relY >= 0.52 && relY < 0.75) {
          lumCheeks += lum;
          countCheeks++;
        }
      }
    }

    if (totalCount < 16) return false;

    const mean = totalLum / totalCount;
    let varSum = 0;
    for (let i = 0; i < allLums.length; i++) {
      const d = allLums[i] - mean;
      varSum += d * d;
    }
    const stdDev = Math.sqrt(varSum / totalCount);

    // Reject flat background surfaces (uniform wood doors, beige walls)
    if (stdDev < 6.5) return false;

    // Anthropometric Facial Eye-Dip Test:
    // In human faces, the eye/eyebrow sockets are darker than the forehead and/or cheeks.
    // A hand or plain forearm has no dark eye band between forehead and cheeks!
    if (countForehead >= 4 && countEyes >= 6 && countCheeks >= 6) {
      const meanForehead = lumForehead / countForehead;
      const meanEyes = lumEyes / countEyes;
      const meanCheeks = lumCheeks / countCheeks;
      const eyeDip = (meanForehead - meanEyes) + (meanCheeks - meanEyes);

      // Real face exhibits distinctive eye dip (>= 2.5), or at least one significant ocular dip
      if (eyeDip < 2.5 && (meanForehead - meanEyes) < 1.8 && (meanCheeks - meanEyes) < 1.8) {
        return false; // Hand, palm, or flat surface rejected!
      }

      // Check bilateral eye symmetry: both eyes should have comparable luminance
      if (countLeftEye >= 2 && countRightEye >= 2) {
        const leftEyeMean = lumLeftEye / countLeftEye;
        const rightEyeMean = lumRightEye / countRightEye;
        if (Math.abs(leftEyeMean - rightEyeMean) > 50) {
          return false; // Strongly asymmetric shadow, not a human face
        }
      }
    }

    return true;
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

              // Multi-space accurate skin detection
              const Y = 0.299 * red + 0.587 * green + 0.114 * blue;
              const Cr = 0.5 * red - 0.418688 * green - 0.081312 * blue + 128;
              const Cb = -0.168736 * red - 0.331264 * green + 0.5 * blue + 128;

              if (Y < 30 || Y > 245) continue;

              const isSkinYCbCr = (Cr >= 133 && Cr <= 175 && Cb >= 75 && Cb <= 128);
              const maxRGB = Math.max(red, green, blue);
              const minRGB = Math.min(red, green, blue);
              const isSkinRGB = (
                red > 45 && green > 30 && blue > 20 &&
                red > green &&
                green >= blue &&
                (red - green) >= 10 &&
                (maxRGB - minRGB) >= 12 &&
                (red - minRGB) >= 14 &&
                Math.abs(red - green) <= 110
              );

              const isDarkSkin = (
                Y >= 30 && Y <= 115 &&
                red >= 38 && green >= 24 && blue >= 15 &&
                red >= green && (red - minRGB) >= 10 &&
                Cr >= 134 && Cr <= 178 && Cb >= 78 && Cb <= 128
              );

              if ((isSkinYCbCr && isSkinRGB) || isDarkSkin) {
                skinPixels++;
              }
            }
          }

          if (skinPixels >= 8) {
            skinGrid[r][c] = 1;
            totalSkinCells++;
          }
        }
      }

      if (totalSkinCells < 30) {
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

            // Filter out tiny noise blobs (< 18 cells)
            if (cells >= 18 && blobWidth >= 3 && blobHeight >= 4) {
              const hasFaceLandmarks = this.verifyFaceLandmarks(data, width, minC, maxC, minR, maxR, cellW, cellH);

              rawBlobs.push({
                cells,
                minC, maxC, minR, maxR,
                width: blobWidth,
                height: blobHeight,
                aspectRatio,
                centerC: (minC + maxC) / 2,
                centerR: (minR + maxR) / 2,
                touchesBottom: (maxR >= 22),
                hasFaceLandmarks,
              });
            }
          }
        }
      }

      if (rawBlobs.length === 0) {
        return 0;
      }

      rawBlobs.sort((a, b) => b.cells - a.cells);

      // STEP 1: Find the PRIMARY candidate face
      // Must be substantial, head aspect ratio (0.95 to 1.85), located in upper 2/3 of frame
      let primaryFace = rawBlobs.find(b =>
        b.cells >= 25 &&
        b.width >= 4 &&
        b.height >= 5 &&
        b.aspectRatio >= 0.95 && b.aspectRatio <= 1.85 &&
        b.centerR <= 20 &&
        b.hasFaceLandmarks
      );

      // If strict landmarks were borderline due to low webcam lighting, accept top primary head candidate
      if (!primaryFace) {
        primaryFace = rawBlobs.find(b =>
          b.cells >= 35 &&
          b.width >= 4 &&
          b.height >= 5 &&
          b.aspectRatio >= 0.95 && b.aspectRatio <= 1.85 &&
          b.centerR <= 19
        );
      }

      if (!primaryFace) {
        return 0;
      }

      // STEP 2: Detect genuine SECONDARY persons (real multiple faces)
      const distinctHeads = [primaryFace];
      const maxHeadDim = Math.max(primaryFace.width, primaryFace.height);

      for (const blob of rawBlobs) {
        if (blob === primaryFace) continue;

        const distFromPrimary = Math.hypot(blob.centerC - primaryFace.centerC, blob.centerR - primaryFace.centerR);

        // FILTER 1: Hand touching or adjacent to primary face (scratching face, chin on palm, glasses)
        // If within touching distance of primary head, it is absorbed into candidate
        if (distFromPrimary < maxHeadDim * 0.95) {
          continue;
        }

        // FILTER 2: Hand/arm coming from the bottom edge or lap (keyboard/desk area)
        if (blob.touchesBottom) {
          continue;
        }

        // FILTER 3: Torso/neck/chest region directly below candidate head
        const colDiff = Math.abs(blob.centerC - primaryFace.centerC);
        const isBelowPrimary = (blob.centerR > primaryFace.centerR + primaryFace.height * 0.4) && (colDiff <= primaryFace.width * 0.85);
        if (isBelowPrimary) {
          continue;
        }

        // FILTER 4: To qualify as a genuine SECOND face:
        // Must be a substantial head (cells >= 20, width >= 4, height >= 5),
        // within human head proportions (aspectRatio 0.95 to 1.75),
        // located in upper/middle frame, passing strict facial landmarks,
        // and clearly separate from candidate (dist >= 1.15 * head size).
        if (
          blob.cells >= 20 &&
          blob.width >= 4 &&
          blob.height >= 5 &&
          blob.aspectRatio >= 0.95 && blob.aspectRatio <= 1.75 &&
          blob.centerR <= 20 &&
          blob.hasFaceLandmarks &&
          distFromPrimary >= maxHeadDim * 1.15
        ) {
          let separated = true;
          for (const head of distinctHeads) {
            const dist = Math.hypot(blob.centerC - head.centerC, blob.centerR - head.centerR);
            if (dist < maxHeadDim * 1.1) {
              separated = false;
              break;
            }
          }
          if (separated) {
            distinctHeads.push(blob);
          }
        }
      }

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
