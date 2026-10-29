/**
 * portfolio-builder.js — Gemini AI Prompt-Driven Portfolio Studio Controller.
 * Fully rebuilt from scratch for natural language prompt portfolio creation.
 */

document.addEventListener("DOMContentLoaded", async () => {
  let currentPortfolio = null;

  // DOM Elements - Alerts & Header
  const alertEl = document.getElementById("builder-alert");
  const statusPill = document.getElementById("portfolio-status-pill");
  const publicLinkGroup = document.getElementById("portfolio-public-link-group");
  const btnCopyLink = document.getElementById("btn-copy-portfolio-link");
  const btnOpenLink = document.getElementById("btn-open-portfolio-link");
  const btnTogglePublish = document.getElementById("btn-toggle-publish");
  const btnSavePortfolio = document.getElementById("btn-save-portfolio");
  const btnSavePortfolioBottom = document.getElementById("btn-save-portfolio-bottom");
  const btnExportHtml = document.getElementById("btn-export-portfolio-html");
  const btnPrintCv = document.getElementById("btn-print-portfolio-cv");
  const btnToggleEditMode = document.getElementById("btn-toggle-edit-mode");
  const btnBannerEdit = document.getElementById("btn-banner-edit");
  const btnQuickEditPreview = document.getElementById("btn-quick-edit-preview");
  const portfolioReadyBanner = document.getElementById("portfolio-ready-banner");
  const tabBtnContent = document.getElementById("tab-btn-content");
  const studioInspectorCard = document.getElementById("studio-inspector-card");
  const btnDeletePortfolio = document.getElementById("btn-delete-portfolio");
  const btnDeletePortfolioTab = document.getElementById("btn-delete-portfolio-tab");
  const btnConfirmDeletePortfolio = document.getElementById("btn-confirm-delete-portfolio");
  const deletePortfolioModalEl = document.getElementById("deletePortfolioModal");
  const modalDeleteSlug = document.getElementById("modal-delete-slug");
  const deleteBtnSpinner = document.getElementById("delete-btn-spinner");

  // DOM Elements - Prompt Center
  const inputAiPrompt = document.getElementById("input-ai-prompt");
  const checkIncludeResume = document.getElementById("check-include-resume");
  const btnGenerateGemini = document.getElementById("btn-generate-with-gemini");
  const btnGenerateIcon = document.getElementById("btn-generate-icon");
  const btnGenerateText = document.getElementById("btn-generate-text");
  const promptStarters = document.querySelectorAll(".prompt-starter-chip");

  // DOM Elements - Conversational Refine Bar
  const inputRefinePrompt = document.getElementById("input-refine-prompt");
  const btnSubmitRefine = document.getElementById("btn-submit-refine");
  const refineChips = document.querySelectorAll(".refine-chip");

  // DOM Elements - Preview & Simulator
  const previewStage = document.getElementById("portfolio-preview-stage");
  const previewThemeIndicator = document.getElementById("preview-theme-indicator");
  const previewFrameContainer = document.getElementById("preview-frame-container");
  const chromeSlugDisplay = document.getElementById("chrome-slug-display");
  const deviceButtons = document.querySelectorAll(".device-switcher-btn");
  const btnToggleExpand = document.getElementById("btn-toggle-expand");
  const controlsColumn = document.getElementById("builder-controls-column");
  const previewColumn = document.getElementById("builder-preview-column");
  const aiLoadingOverlay = document.getElementById("ai-loading-overlay");
  const aiLoadingTitle = document.getElementById("ai-loading-title");
  const aiLoadingStep = document.getElementById("ai-loading-step");

  // DOM Elements - Style Tokens
  const selectLayoutArchitecture = document.getElementById("select-layout-architecture");
  const selectThemeId = document.getElementById("select-theme-id");
  const inputPrimaryColor = document.getElementById("input-primary-color");
  const inputPrimaryColorText = document.getElementById("input-primary-color-text");
  const inputSecondaryColor = document.getElementById("input-secondary-color");
  const inputSecondaryColorText = document.getElementById("input-secondary-color-text");
  const selectFontFamily = document.getElementById("select-font-family");
  const selectBgStyle = document.getElementById("select-bg-style");
  const selectCardStyle = document.getElementById("select-card-style");
  const selectButtonStyle = document.getElementById("select-button-style");
  const switchDarkMode = document.getElementById("switch-dark-mode");
  const paletteButtons = document.querySelectorAll(".palette-btn");
  const bgPresetButtons = document.querySelectorAll(".bg-preset-card");
  const inputBgImageUrl = document.getElementById("input-bg-image-url");
  const btnApplyBgImage = document.getElementById("btn-apply-bg-image");
  const btnClearBgImage = document.getElementById("btn-clear-bg-image");
  const maskShapeButtons = document.querySelectorAll(".mask-shape-btn");

  // DOM Elements - Content Editor
  const inputCandidateName = document.getElementById("input-candidate-name");
  const inputHeadline = document.getElementById("input-headline");
  const textareaAbout = document.getElementById("textarea-about");
  const btnRewriteHeadline = document.getElementById("btn-quick-rewrite-headline");
  const btnRewriteAbout = document.getElementById("btn-quick-rewrite-about");
  const metricsContainer = document.getElementById("metrics-editor-container");
  const btnAddMetric = document.getElementById("btn-add-metric");
  const skillsContainer = document.getElementById("skills-editor-container");
  const inputAddSkill = document.getElementById("input-add-skill-text");
  const btnAddSkill = document.getElementById("btn-add-skill-item");
  const btnReorganizeSkills = document.getElementById("btn-ai-reorganize-skills");
  const projectsContainer = document.getElementById("projects-editor-container");
  const btnAddProject = document.getElementById("btn-add-project-item");
  const experienceContainer = document.getElementById("experience-editor-container");
  const btnAddExperience = document.getElementById("btn-add-experience-item");
  const educationContainer = document.getElementById("education-editor-container");
  const btnAddEducation = document.getElementById("btn-add-education-item");
  const certificationsContainer = document.getElementById("certifications-editor-container");
  const btnAddCertification = document.getElementById("btn-add-certification-item");
  const servicesContainer = document.getElementById("services-editor-container");
  const btnAddService = document.getElementById("btn-add-service-item");

  // DOM Elements - Contact & Social
  const inputSocialEmail = document.getElementById("input-social-email");
  const inputSocialPhone = document.getElementById("input-social-phone");
  const inputSocialLocation = document.getElementById("input-social-location");
  const inputSocialWebsite = document.getElementById("input-social-website");
  const inputSocialLinkedin = document.getElementById("input-social-linkedin");
  const inputSocialGithub = document.getElementById("input-social-github");

  // DOM Elements - URL Slug
  const inputSlug = document.getElementById("input-portfolio-slug");
  const btnCheckSlug = document.getElementById("btn-check-slug");
  const slugMsg = document.getElementById("slug-availability-msg");

  // Helpers
  function showAlert(msg, type = "success") {
    alertEl.className = `alert alert-${type} py-2 px-3 mb-4 rounded-3 d-block shadow-sm`;
    alertEl.textContent = msg;
    setTimeout(() => {
      alertEl.className = "alert d-none";
    }, 6000);
  }

  function safeParse(val, fallback) {
    if (val === null || val === undefined) return fallback;
    if (typeof val === "object") return val;
    if (typeof val === "string") {
      try {
        const parsed = JSON.parse(val);
        return parsed !== null && parsed !== undefined ? parsed : fallback;
      } catch {
        return fallback;
      }
    }
    return fallback;
  }

  function setAiLoading(show, title = "Gemini AI Generating Portfolio...", step = "Analyzing prompt and persona...") {
    if (show) {
      aiLoadingTitle.textContent = title;
      aiLoadingStep.textContent = step;
      aiLoadingOverlay.classList.remove("d-none");
      btnGenerateGemini.disabled = true;
      btnGenerateIcon.textContent = "⏳";
      btnGenerateText.textContent = "Thinking...";
    } else {
      aiLoadingOverlay.classList.add("d-none");
      btnGenerateGemini.disabled = false;
      btnGenerateIcon.textContent = "✨";
      btnGenerateText.textContent = "Generate with Gemini AI";
    }
  }

  /**
   * Main Initialize Flow
   */
  async function init() {
    bindPromptStarters();
    bindDeviceSwitcher();
    bindExpandToggle();
    bindStyleTokenControls();
    bindContentControls();
    bindPublishAndExportControls();
    bindEditModeControls();
    bindDeleteControls();

    // Check user authentication
    const user = Session.getUser();
    if (!user) {
      window.location.href = "login.html";
      return;
    }

    // Load initial candidate portfolio
    try {
      const res = await portfolioAPI.getMyPortfolio();
      if (res && res.data) {
        currentPortfolio = res.data;
        syncDataToUI();
        renderLivePreview();
        if (portfolioReadyBanner) portfolioReadyBanner.classList.remove("d-none");
      } else {
        // Attempt to auto-generate portfolio from existing resume/profile
        try {
          const genRes = await portfolioAPI.generatePortfolio({ theme_id: "auto" });
          if (genRes && genRes.data) {
            currentPortfolio = genRes.data;
            syncDataToUI();
            renderLivePreview();
            if (portfolioReadyBanner) portfolioReadyBanner.classList.remove("d-none");
            return;
          }
        } catch (genErr) {
          console.warn("Auto portfolio generation failed, falling back to starter:", genErr);
        }
        setupInitialDefaultPortfolio(user);
      }
    } catch (err) {
      console.warn("Could not load candidate portfolio:", err);
      setupInitialDefaultPortfolio(user);
    }
  }

  function setupInitialDefaultPortfolio(user) {
    currentPortfolio = {
      candidate_name: user?.name || "Candidate",
      professional_headline: "Senior Software Engineer | High-Scale Distributed Systems",
      headline_options: [
        "Senior Software Engineer | High-Scale Distributed Systems",
        "Full Stack Architect | Cloud & AI Solutions",
      ],
      about: `Hi, I'm ${user?.name || "Candidate"}. I design and engineer scalable web applications, distributed systems, and intuitive user experiences. Enter a prompt above to let Gemini AI build a custom bespoke portfolio tailored to your unique career goals!`,
      theme_id: "modern",
      primary_color: "#4f46e5",
      secondary_color: "#06b6d4",
      font: "Plus Jakarta Sans",
      background_style: "mesh",
      card_style: "glass",
      button_style: "rounded",
      dark_mode: false,
      layout: "modern",
      achievements: [
        { value: "99.9%", label: "System Reliability", icon: "⚡" },
        { value: "10M+", label: "Monthly API Requests", icon: "🚀" },
        { value: "35%", label: "Query Latency Reduction", icon: "📉" },
        { value: "5+", label: "Years Experience", icon: "🏆" },
      ],
      skills: {
        "Core Languages": ["Python", "TypeScript", "JavaScript", "SQL"],
        "Frameworks & Web": ["React", "Next.js", "FastAPI", "Node.js"],
        "Cloud & DevOps": ["Docker", "Kubernetes", "AWS", "CI/CD"],
        "Databases & Tools": ["PostgreSQL", "Redis", "Git"],
      },
      services: [
        { title: "Full-Stack Architecture", description: "Designing end-to-end cloud platforms with resilient microservices.", icon: "🏗️" },
        { title: "API & Data Engineering", description: "Sub-100ms API endpoints and automated ETL data streaming.", icon: "⚡" },
        { title: "Performance Auditing", description: "Optimizing render times, bundle size, and database query throughput.", icon: "🎯" },
      ],
      projects: [
        {
          name: "Cloud Telemetry Engine",
          description: "Distributed monitoring platform processing high-throughput application metrics in real time.",
          key_features: ["Engineered streaming event pipeline with Kafka", "Built interactive dashboard with sub-50ms refresh"],
          technologies: ["Python", "FastAPI", "React", "Docker"],
          live_demo_url: "",
          github_url: "",
        },
        {
          name: "AI Recruiting Automation Hub",
          description: "Intelligent ATS matching system with semantic resume parsing and interview assessment.",
          key_features: ["Implemented NLP skill extraction engine", "Engineered role-based evaluation workflows"],
          technologies: ["TypeScript", "FastAPI", "PostgreSQL", "Gemini AI"],
          live_demo_url: "",
          github_url: "",
        },
      ],
      experience: [
        {
          title: "Senior Software Engineer",
          company: "Enterprise Cloud Tech",
          location: "San Francisco, CA",
          start_date: "2022",
          end_date: "Present",
          is_current: true,
          description: "Leading core platform services and engineering scalability initiatives.",
          highlights: [
            "Reduced cloud infrastructure costs by 30% through container orchestration tuning.",
            "Mentored 4 junior engineers and standardized API documentation across teams.",
          ],
          technologies: ["Python", "React", "AWS", "Docker"],
        },
      ],
      education: [
        { degree: "B.S. in Computer Science", institution: "University of Technology", end_year: "2021", grade: "First Class" },
      ],
      social_links: {
        email: user?.email || "candidate@example.com",
        location: "San Francisco, CA",
        github: "https://github.com",
        linkedin: "https://linkedin.com",
      },
      slug: (user?.name || "candidate").toLowerCase().replace(/[^a-z0-9]+/g, "-"),
      is_published: false,
    };

    syncDataToUI();
    renderLivePreview();
  }

  /**
   * Synchronizes currentPortfolio state into all form inputs
   */
  function syncDataToUI() {
    if (!currentPortfolio) return;

    // Candidate Name
    if (inputCandidateName) {
      inputCandidateName.value = currentPortfolio.candidate_name || "";
    }

    // Headline & About
    inputHeadline.value = currentPortfolio.professional_headline || "";
    textareaAbout.value = currentPortfolio.about || "";

    // Layout Architecture
    if (selectLayoutArchitecture) {
      selectLayoutArchitecture.value = currentPortfolio.layout || "nova";
    }

    // Style Tokens
    selectThemeId.value = currentPortfolio.theme_id || "modern";
    inputPrimaryColor.value = currentPortfolio.primary_color || "#4f46e5";
    inputPrimaryColorText.value = currentPortfolio.primary_color || "#4f46e5";
    inputSecondaryColor.value = currentPortfolio.secondary_color || "#06b6d4";
    inputSecondaryColorText.value = currentPortfolio.secondary_color || "#06b6d4";
    selectFontFamily.value = currentPortfolio.font || "Plus Jakarta Sans";
    selectBgStyle.value = currentPortfolio.background_style || "mesh";
    if (selectCardStyle) selectCardStyle.value = currentPortfolio.card_style || "glass";
    if (selectButtonStyle) selectButtonStyle.value = currentPortfolio.button_style || "rounded";
    switchDarkMode.checked = Boolean(currentPortfolio.dark_mode);

    // Background Image
    const currentBgUrl = currentPortfolio.background_image || "";
    if (inputBgImageUrl) {
      inputBgImageUrl.value = (currentBgUrl && currentBgUrl !== "none") ? currentBgUrl : "";
    }
    bgPresetButtons.forEach(btn => {
      const pUrl = btn.getAttribute("data-bg-url");
      if (pUrl === "none" && (currentBgUrl === "none" || currentBgUrl === "")) {
        btn.classList.add("active");
      } else if (pUrl && pUrl !== "none" && currentBgUrl === pUrl) {
        btn.classList.add("active");
      } else {
        btn.classList.remove("active");
      }
    });

    // Sculpted Portrait Mask Shape
    let currentMask = currentPortfolio.portrait_mask;
    if (!currentMask && currentPortfolio.custom_css) {
      try {
        const parsedCss = typeof currentPortfolio.custom_css === "string" ? JSON.parse(currentPortfolio.custom_css) : currentPortfolio.custom_css;
        if (parsedCss && parsedCss.portrait_mask) currentMask = parsedCss.portrait_mask;
      } catch (e) {}
    }
    if (!currentMask) currentMask = "mask-pebble";
    currentPortfolio.portrait_mask = currentMask;

    maskShapeButtons.forEach(btn => {
      if (btn.getAttribute("data-mask") === currentMask) {
        btn.classList.add("active");
      } else {
        btn.classList.remove("active");
      }
    });

    // Slug & Status
    inputSlug.value = currentPortfolio.slug || "";
    chromeSlugDisplay.textContent = currentPortfolio.slug || "candidate";

    updatePublishStatusBadge();

    // Render Sub-Sections in UI
    renderMetricsEditor();
    renderSkillsEditor();
    renderProjectsEditor();
    renderExperienceEditor();
    renderEducationEditor();
    renderCertificationsEditor();
    renderServicesEditor();
    renderSocialLinksEditor();
  }

  function updatePublishStatusBadge() {
    const isPub = Boolean(currentPortfolio?.is_published);
    if (isPub) {
      statusPill.className = "badge bg-success text-white px-3 py-2 rounded-pill fw-semibold shadow-sm";
      statusPill.textContent = "Status: Live Public Site";
      btnTogglePublish.className = "btn btn-sm btn-outline-danger fw-bold px-3 py-2 shadow-sm d-flex align-items-center gap-1";
      btnTogglePublish.innerHTML = "<span>🛑</span> Unpublish";
      publicLinkGroup.classList.remove("d-none");
      btnOpenLink.href = `/portfolio/${currentPortfolio.slug}`;
    } else {
      statusPill.className = "badge bg-secondary-subtle text-secondary px-3 py-2 rounded-pill fw-semibold";
      statusPill.textContent = "Status: Draft (Private)";
      btnTogglePublish.className = "btn btn-sm btn-success fw-bold px-3 py-2 shadow-sm d-flex align-items-center gap-1";
      btnTogglePublish.innerHTML = "<span>🚀</span> Publish Portfolio";
      publicLinkGroup.classList.add("d-none");
    }
  }

  /**
   * Renders the portfolio live into preview stage using PortfolioThemesEngine
   */
  function renderLivePreview() {
    if (!currentPortfolio || !previewStage) return;

    // Update indicator
    const themeName = selectThemeId.options[selectThemeId.selectedIndex]?.text || currentPortfolio.theme_id;
    const layoutName = selectLayoutArchitecture?.options[selectLayoutArchitecture.selectedIndex]?.text || currentPortfolio.layout;
    previewThemeIndicator.textContent = `${themeName} • ${layoutName ? layoutName.split('(')[0].trim() : 'NOVA'}`;
    chromeSlugDisplay.textContent = currentPortfolio.slug || "candidate";

    try {
      PortfolioThemesEngine.render(previewStage, currentPortfolio);
    } catch (err) {
      console.error("Rendering error in PortfolioThemesEngine:", err);
    }
  }

  /**
   * Binds Prompt Starters & Gemini Generation
   */
  function bindPromptStarters() {
    promptStarters.forEach(chip => {
      chip.addEventListener("click", () => {
        const text = chip.getAttribute("data-prompt");
        if (text) {
          inputAiPrompt.value = text;
          inputAiPrompt.focus();
          btnGenerateGemini.classList.add("pulse-glow");
          setTimeout(() => btnGenerateGemini.classList.remove("pulse-glow"), 1000);
        }
      });
    });

    btnGenerateGemini.addEventListener("click", async () => {
      const promptText = (inputAiPrompt.value || "").trim();
      if (!promptText) {
        showAlert("Please enter a prompt describing your desired portfolio or click one of the ideas above!", "warning");
        inputAiPrompt.focus();
        return;
      }

      setAiLoading(true, "Triple-Gemini Pipeline Active...", "Model 1: Analyzing authentic resume credentials, projects & career facts...");

      // Multi-model step progression
      const t1 = setTimeout(() => {
        aiLoadingStep.textContent = "Model 2: Analyzing prompt intent for layout, colors, background & UI styling...";
      }, 1400);
      const t2 = setTimeout(() => {
        aiLoadingStep.textContent = "Model 3: Synthesizing bespoke portfolio specification and creative copy...";
      }, 3200);

      try {
        const res = await portfolioAPI.generateFromPrompt(promptText, {
          include_resume: checkIncludeResume.checked,
          refinement: false,
        });

        clearTimeout(t1);
        clearTimeout(t2);

        if (res && res.data) {
          currentPortfolio = res.data;
          syncDataToUI();
          renderLivePreview();
          if (portfolioReadyBanner) portfolioReadyBanner.classList.remove("d-none");
          openEditMode();
          showAlert("✨ Portfolio generated successfully! Review below and customize any details or correct any information.", "success");
        } else {
          throw new Error(res?.message || "Generation did not return portfolio data");
        }
      } catch (err) {
        clearTimeout(t1);
        clearTimeout(t2);
        console.error("Generation error:", err);
        showAlert(err.message || "Could not generate portfolio with Gemini AI. Please check your network or try again.", "danger");
      } finally {
        setAiLoading(false);
      }
    });

    // Keyboard shortcut (Ctrl+Enter / Cmd+Enter to generate)
    inputAiPrompt.addEventListener("keydown", (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        e.preventDefault();
        btnGenerateGemini.click();
      }
    });

    // Conversational Refine Bar
    btnSubmitRefine.addEventListener("click", () => {
      const refineText = (inputRefinePrompt.value || "").trim();
      if (refineText) {
        executePromptRefinement(refineText);
      }
    });

    inputRefinePrompt.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        const refineText = (inputRefinePrompt.value || "").trim();
        if (refineText) {
          executePromptRefinement(refineText);
        }
      }
    });

    refineChips.forEach(chip => {
      chip.addEventListener("click", () => {
        const text = chip.getAttribute("data-refine");
        if (text) {
          inputRefinePrompt.value = text;
          executePromptRefinement(text);
        }
      });
    });
  }

  async function executePromptRefinement(instruction) {
    setAiLoading(true, "Gemini AI Refining Portfolio...", `Applying refinement: "${instruction}"...`);
    try {
      const res = await portfolioAPI.generateFromPrompt(instruction, {
        include_resume: true,
        refinement: true,
      });

      if (res && res.data) {
        currentPortfolio = res.data;
        syncDataToUI();
        renderLivePreview();
        inputRefinePrompt.value = "";
        showAlert("✨ Gemini AI successfully refined your portfolio!", "success");
      } else {
        throw new Error(res?.message || "Refinement failed");
      }
    } catch (err) {
      console.error("Refinement error:", err);
      showAlert(err.message || "Failed to refine portfolio.", "danger");
    } finally {
      setAiLoading(false);
    }
  }

  /**
   * Device Simulator Switcher & Fullscreen Expand
   */
  function bindDeviceSwitcher() {
    deviceButtons.forEach(btn => {
      btn.addEventListener("click", () => {
        deviceButtons.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        const mode = btn.getAttribute("data-mode");
        previewFrameContainer.className = `preview-frame-container preview-mode-${mode}`;
      });
    });
  }

  function bindExpandToggle() {
    let isExpanded = false;
    btnToggleExpand.addEventListener("click", () => {
      isExpanded = !isExpanded;
      if (isExpanded) {
        controlsColumn.classList.add("d-none");
        previewColumn.className = "col-12";
        btnToggleExpand.innerHTML = "🗗 Collapse";
      } else {
        controlsColumn.classList.remove("d-none");
        previewColumn.className = "col-xl-7 col-lg-6";
        btnToggleExpand.innerHTML = "⛶ Expand";
      }
    });
  }

  /**
   * Style Tokens & Design Controls
   */
  function bindStyleTokenControls() {
    // Layout Architecture
    if (selectLayoutArchitecture) {
      selectLayoutArchitecture.addEventListener("change", () => {
        if (!currentPortfolio) return;
        currentPortfolio.layout = selectLayoutArchitecture.value;
        renderLivePreview();
      });
    }

    // Active Theme Style
    selectThemeId.addEventListener("change", () => {
      if (!currentPortfolio) return;
      currentPortfolio.theme_id = selectThemeId.value;
      renderLivePreview();
    });

    // Primary Color
    inputPrimaryColor.addEventListener("input", () => {
      inputPrimaryColorText.value = inputPrimaryColor.value;
      if (currentPortfolio) {
        currentPortfolio.primary_color = inputPrimaryColor.value;
        renderLivePreview();
      }
    });

    inputPrimaryColorText.addEventListener("change", () => {
      inputPrimaryColor.value = inputPrimaryColorText.value;
      if (currentPortfolio) {
        currentPortfolio.primary_color = inputPrimaryColorText.value;
        renderLivePreview();
      }
    });

    // Secondary Color
    inputSecondaryColor.addEventListener("input", () => {
      inputSecondaryColorText.value = inputSecondaryColor.value;
      if (currentPortfolio) {
        currentPortfolio.secondary_color = inputSecondaryColor.value;
        renderLivePreview();
      }
    });

    inputSecondaryColorText.addEventListener("change", () => {
      inputSecondaryColor.value = inputSecondaryColorText.value;
      if (currentPortfolio) {
        currentPortfolio.secondary_color = inputSecondaryColorText.value;
        renderLivePreview();
      }
    });

    // Background Image Presets Gallery
    bgPresetButtons.forEach(btn => {
      btn.addEventListener("click", () => {
        bgPresetButtons.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        const pUrl = btn.getAttribute("data-bg-url");
        if (pUrl === "none" || !pUrl) {
          if (inputBgImageUrl) inputBgImageUrl.value = "";
          if (currentPortfolio) currentPortfolio.background_image = "none";
        } else {
          if (inputBgImageUrl) inputBgImageUrl.value = pUrl;
          if (currentPortfolio) currentPortfolio.background_image = pUrl;
        }
        renderLivePreview();
      });
    });

    // Custom Background Image URL Apply & Clear
    if (btnApplyBgImage) {
      btnApplyBgImage.addEventListener("click", () => {
        const customUrl = (inputBgImageUrl?.value || "").trim();
        if (customUrl && currentPortfolio) {
          currentPortfolio.background_image = customUrl;
          bgPresetButtons.forEach(b => b.classList.remove("active"));
          renderLivePreview();
          showAlert("Custom background image applied!", "info");
        }
      });
    }

    if (btnClearBgImage) {
      btnClearBgImage.addEventListener("click", () => {
        if (inputBgImageUrl) inputBgImageUrl.value = "";
        if (currentPortfolio) currentPortfolio.background_image = "none";
        bgPresetButtons.forEach(b => {
          if (b.getAttribute("data-bg-url") === "none") b.classList.add("active");
          else b.classList.remove("active");
        });
        renderLivePreview();
        showAlert("Background image cleared (clean solid ambient mode active).", "info");
      });
    }

    // Sculpted Portrait Mask Shape Buttons
    maskShapeButtons.forEach(btn => {
      btn.addEventListener("click", () => {
        const mask = btn.getAttribute("data-mask") || "mask-pebble";
        maskShapeButtons.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        if (currentPortfolio) {
          currentPortfolio.portrait_mask = mask;
          currentPortfolio.custom_css = JSON.stringify({ portrait_mask: mask });
          renderLivePreview();
        }
      });
    });

    // Typography Font Family
    selectFontFamily.addEventListener("change", () => {
      if (!currentPortfolio) return;
      currentPortfolio.font = selectFontFamily.value;
      renderLivePreview();
    });

    // Ambient Pattern
    selectBgStyle.addEventListener("change", () => {
      if (!currentPortfolio) return;
      currentPortfolio.background_style = selectBgStyle.value;
      renderLivePreview();
    });

    // Card Style
    if (selectCardStyle) {
      selectCardStyle.addEventListener("change", () => {
        if (!currentPortfolio) return;
        currentPortfolio.card_style = selectCardStyle.value;
        renderLivePreview();
      });
    }

    // Button Style
    if (selectButtonStyle) {
      selectButtonStyle.addEventListener("change", () => {
        if (!currentPortfolio) return;
        currentPortfolio.button_style = selectButtonStyle.value;
        renderLivePreview();
      });
    }

    // Dark Mode Toggle
    switchDarkMode.addEventListener("change", () => {
      if (!currentPortfolio) return;
      currentPortfolio.dark_mode = switchDarkMode.checked;
      renderLivePreview();
    });

    // Palettes
    paletteButtons.forEach(btn => {
      btn.addEventListener("click", () => {
        const pri = btn.getAttribute("data-primary");
        const sec = btn.getAttribute("data-secondary");
        if (pri && sec && currentPortfolio) {
          inputPrimaryColor.value = pri;
          inputPrimaryColorText.value = pri;
          inputSecondaryColor.value = sec;
          inputSecondaryColorText.value = sec;
          currentPortfolio.primary_color = pri;
          currentPortfolio.secondary_color = sec;
          renderLivePreview();
        }
      });
    });
  }

  /**
   * Content Editing & Real-time Live Sync
   */
  function bindContentControls() {
    inputHeadline.addEventListener("input", () => {
      if (!currentPortfolio) return;
      currentPortfolio.professional_headline = inputHeadline.value;
      renderLivePreview();
    });

    textareaAbout.addEventListener("input", () => {
      if (!currentPortfolio) return;
      currentPortfolio.about = textareaAbout.value;
      renderLivePreview();
    });

    btnRewriteHeadline.addEventListener("click", async () => {
      setAiLoading(true, "Gemini AI Polishing Headline...", "Refining professional headline with impactful phrasing...");
      try {
        const res = await portfolioAPI.refineSection("headline", "Make it punchier, authoritative, and role-tailored");
        if (res && res.data) {
          currentPortfolio = res.data;
          syncDataToUI();
          renderLivePreview();
          showAlert("✨ Headline polished successfully with Gemini AI!", "success");
        }
      } catch (err) {
        showAlert("Failed to polish headline.", "danger");
      } finally {
        setAiLoading(false);
      }
    });

    btnRewriteAbout.addEventListener("click", async () => {
      setAiLoading(true, "Gemini AI Polishing Bio...", "Polishing About Me narrative with active verbs and executive vision...");
      try {
        const res = await portfolioAPI.refineSection("about", "Polish narrative with strong impact verbs and clear professional vision");
        if (res && res.data) {
          currentPortfolio = res.data;
          syncDataToUI();
          renderLivePreview();
          showAlert("✨ About Me bio polished successfully with Gemini AI!", "success");
        }
      } catch (err) {
        showAlert("Failed to polish bio.", "danger");
      } finally {
        setAiLoading(false);
      }
    });

    btnAddMetric.addEventListener("click", () => {
      if (!currentPortfolio) return;
      let metrics = safeParse(currentPortfolio.achievements, []);
      metrics.push({ value: "100%", label: "New KPI Impact", icon: "⚡" });
      currentPortfolio.achievements = metrics;
      renderMetricsEditor();
      renderLivePreview();
    });

    btnAddSkill.addEventListener("click", () => {
      const val = (inputAddSkill.value || "").trim();
      if (!val || !currentPortfolio) return;
      let skills = safeParse(currentPortfolio.skills, {});
      if (Array.isArray(skills)) {
        skills.push(val);
      } else {
        const firstKey = Object.keys(skills)[0] || "Core Technologies";
        if (!skills[firstKey]) skills[firstKey] = [];
        skills[firstKey].push(val);
      }
      currentPortfolio.skills = skills;
      inputAddSkill.value = "";
      renderSkillsEditor();
      renderLivePreview();
    });

    btnReorganizeSkills.addEventListener("click", async () => {
      setAiLoading(true, "Gemini AI Categorizing Skills...", "Organizing skills into clean industry-standard categories...");
      try {
        const res = await portfolioAPI.refineSection("skills", "Categorize skills cleanly into 3-4 standard engineering groups");
        if (res && res.data) {
          currentPortfolio = res.data;
          syncDataToUI();
          renderLivePreview();
          showAlert("✨ Skills organized cleanly into categories!", "success");
        }
      } catch (err) {
        showAlert("Failed to organize skills.", "danger");
      } finally {
        setAiLoading(false);
      }
    });

    btnAddProject.addEventListener("click", () => {
      if (!currentPortfolio) return;
      let projects = safeParse(currentPortfolio.projects, []);
      projects.push({
        name: "New Flagship Project",
        description: "Engineered scalable features delivering high performance and seamless user experience.",
        key_features: ["Implemented resilient architecture", "Optimized sub-100ms response time"],
        technologies: ["TypeScript", "React", "PostgreSQL"],
        live_demo_url: "",
        github_url: "",
      });
      currentPortfolio.projects = projects;
      renderProjectsEditor();
      renderLivePreview();
    });

    btnAddExperience.addEventListener("click", () => {
      if (!currentPortfolio) return;
      let exp = safeParse(currentPortfolio.experience, []);
      exp.push({
        title: "Senior Engineer",
        company: "Tech Enterprise",
        location: "Remote",
        start_date: "2023",
        end_date: "Present",
        is_current: true,
        description: "Leading core systems and product features.",
        highlights: ["Delivered major engineering milestones on schedule."],
        technologies: ["Python", "Docker"],
      });
      currentPortfolio.experience = exp;
      renderExperienceEditor();
      renderLivePreview();
    });

    if (inputCandidateName) {
      inputCandidateName.addEventListener("input", () => {
        if (!currentPortfolio) return;
        currentPortfolio.candidate_name = inputCandidateName.value;
        renderLivePreview();
      });
    }

    if (btnAddEducation) {
      btnAddEducation.addEventListener("click", () => {
        if (!currentPortfolio) return;
        let edu = safeParse(currentPortfolio.education, []);
        edu.push({
          degree: "B.S. in Computer Science",
          institution: "University of Technology",
          end_year: "2023",
          grade: "Honors",
        });
        currentPortfolio.education = edu;
        renderEducationEditor();
        renderLivePreview();
      });
    }

    if (btnAddCertification) {
      btnAddCertification.addEventListener("click", () => {
        if (!currentPortfolio) return;
        let certs = safeParse(currentPortfolio.certifications, []);
        certs.push({
          name: "AWS Certified Solutions Architect",
          organization: "Amazon Web Services",
          year: "2024",
          credential_url: "",
        });
        currentPortfolio.certifications = certs;
        renderCertificationsEditor();
        renderLivePreview();
      });
    }

    if (btnAddService) {
      btnAddService.addEventListener("click", () => {
        if (!currentPortfolio) return;
        let servs = safeParse(currentPortfolio.services, []);
        servs.push({
          title: "Full-Stack System Engineering",
          description: "Designing end-to-end resilient microservices with sub-100ms API latency.",
          icon: "⚡",
        });
        currentPortfolio.services = servs;
        renderServicesEditor();
        renderLivePreview();
      });
    }
  }

  function renderMetricsEditor() {
    metricsContainer.innerHTML = "";
    if (!currentPortfolio) return;
    const metrics = safeParse(currentPortfolio.achievements, []);
    metrics.forEach((m, idx) => {
      const row = document.createElement("div");
      row.className = "d-flex align-items-center gap-2 p-2 bg-white rounded border";
      row.innerHTML = `
        <span class="fs-6">${m.icon || "⚡"}</span>
        <input type="text" class="form-control form-control-sm fw-bold text-primary metric-val" value="${m.value || ''}" style="width: 80px;" placeholder="e.g. 99.9%" />
        <input type="text" class="form-control form-control-sm metric-lbl" value="${m.label || ''}" placeholder="Label..." />
        <button type="button" class="btn btn-sm btn-outline-danger py-0 px-2 btn-del-metric">×</button>
      `;

      row.querySelector(".metric-val").addEventListener("input", (e) => {
        metrics[idx].value = e.target.value;
        currentPortfolio.achievements = metrics;
        renderLivePreview();
      });
      row.querySelector(".metric-lbl").addEventListener("input", (e) => {
        metrics[idx].label = e.target.value;
        currentPortfolio.achievements = metrics;
        renderLivePreview();
      });
      row.querySelector(".btn-del-metric").addEventListener("click", () => {
        metrics.splice(idx, 1);
        currentPortfolio.achievements = metrics;
        renderMetricsEditor();
        renderLivePreview();
      });

      metricsContainer.appendChild(row);
    });
  }

  function renderSkillsEditor() {
    skillsContainer.innerHTML = "";
    if (!currentPortfolio) return;
    const skills = safeParse(currentPortfolio.skills, {});

    if (Array.isArray(skills)) {
      const chipContainer = document.createElement("div");
      chipContainer.className = "d-flex flex-wrap gap-1";
      skills.forEach((s, idx) => {
        const badge = document.createElement("span");
        badge.className = "badge bg-white text-dark border px-2 py-1 d-inline-flex align-items-center gap-1";
        badge.innerHTML = `<span>${s}</span><span class="cursor-pointer text-danger" style="font-size: 11px;">×</span>`;
        badge.querySelector(".text-danger").addEventListener("click", () => {
          skills.splice(idx, 1);
          currentPortfolio.skills = skills;
          renderSkillsEditor();
          renderLivePreview();
        });
        chipContainer.appendChild(badge);
      });
      skillsContainer.appendChild(chipContainer);
    } else {
      Object.entries(skills).forEach(([cat, list]) => {
        const sec = document.createElement("div");
        sec.className = "mb-2";
        sec.innerHTML = `<small class="fw-bold text-muted d-block mb-1">${cat}</small>`;
        const chipContainer = document.createElement("div");
        chipContainer.className = "d-flex flex-wrap gap-1";
        if (Array.isArray(list)) {
          list.forEach((s, idx) => {
            const badge = document.createElement("span");
            badge.className = "badge bg-white text-dark border px-2 py-1 d-inline-flex align-items-center gap-1";
            badge.innerHTML = `<span>${s}</span><span class="cursor-pointer text-danger" style="font-size: 11px;">×</span>`;
            badge.querySelector(".text-danger").addEventListener("click", () => {
              list.splice(idx, 1);
              currentPortfolio.skills = skills;
              renderSkillsEditor();
              renderLivePreview();
            });
            chipContainer.appendChild(badge);
          });
        }
        sec.appendChild(chipContainer);
        skillsContainer.appendChild(sec);
      });
    }
  }

  function renderProjectsEditor() {
    projectsContainer.innerHTML = "";
    if (!currentPortfolio) return;
    const projects = safeParse(currentPortfolio.projects, []);

    if (projects.length === 0) {
      projectsContainer.innerHTML = `<div class="text-muted small p-2 text-center bg-white rounded border">No projects yet. Click <strong>+ Add Project</strong> to showcase your work.</div>`;
      return;
    }

    projects.forEach((p, idx) => {
      const card = document.createElement("div");
      card.className = "p-2 bg-white rounded border";
      card.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-1">
          <input type="text" class="form-control form-control-sm fw-bold proj-name" value="${p.name || ''}" placeholder="Project Name" />
          <button type="button" class="btn btn-sm text-danger ms-2 btn-del-proj" title="Delete Project">×</button>
        </div>
        <textarea rows="2" class="form-control form-control-sm proj-desc mb-1" placeholder="Description">${p.description || ''}</textarea>
        <div class="row g-1 mb-1">
          <div class="col-12">
            <input type="text" class="form-control form-control-sm proj-techs" value="${(p.technologies || []).join(', ')}" placeholder="Technologies (comma separated, e.g. React, Python)" />
          </div>
          <div class="col-6">
            <input type="url" class="form-control form-control-sm proj-live" value="${p.live_demo_url || ''}" placeholder="Live Demo URL (optional)" />
          </div>
          <div class="col-6">
            <input type="url" class="form-control form-control-sm proj-gh" value="${p.github_url || ''}" placeholder="GitHub URL (optional)" />
          </div>
        </div>
      `;

      card.querySelector(".proj-name").addEventListener("input", (e) => {
        projects[idx].name = e.target.value;
        currentPortfolio.projects = projects;
        renderLivePreview();
      });
      card.querySelector(".proj-desc").addEventListener("input", (e) => {
        projects[idx].description = e.target.value;
        currentPortfolio.projects = projects;
        renderLivePreview();
      });
      card.querySelector(".proj-techs").addEventListener("change", (e) => {
        projects[idx].technologies = e.target.value.split(",").map(t => t.trim()).filter(Boolean);
        currentPortfolio.projects = projects;
        renderLivePreview();
      });
      card.querySelector(".proj-live").addEventListener("input", (e) => {
        projects[idx].live_demo_url = e.target.value.trim();
        currentPortfolio.projects = projects;
        renderLivePreview();
      });
      card.querySelector(".proj-gh").addEventListener("input", (e) => {
        projects[idx].github_url = e.target.value.trim();
        currentPortfolio.projects = projects;
        renderLivePreview();
      });
      card.querySelector(".btn-del-proj").addEventListener("click", () => {
        projects.splice(idx, 1);
        currentPortfolio.projects = projects;
        renderProjectsEditor();
        renderLivePreview();
      });

      projectsContainer.appendChild(card);
    });
  }

  function renderExperienceEditor() {
    experienceContainer.innerHTML = "";
    if (!currentPortfolio) return;
    const exp = safeParse(currentPortfolio.experience, []);

    if (exp.length === 0) {
      experienceContainer.innerHTML = `<div class="text-muted small p-2 text-center bg-white rounded border">No experience added yet. Click <strong>+ Add Experience</strong> to list career history.</div>`;
      return;
    }

    exp.forEach((eItem, idx) => {
      const card = document.createElement("div");
      card.className = "p-2 bg-white rounded border";
      card.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-1">
          <input type="text" class="form-control form-control-sm fw-bold exp-title" value="${eItem.title || ''}" placeholder="Role Title (e.g. Lead Engineer)" />
          <button type="button" class="btn btn-sm text-danger ms-2 btn-del-exp" title="Delete Experience">×</button>
        </div>
        <div class="row g-1 mb-1">
          <div class="col-4">
            <input type="text" class="form-control form-control-sm exp-comp" value="${eItem.company || ''}" placeholder="Company" />
          </div>
          <div class="col-4">
            <input type="text" class="form-control form-control-sm exp-loc" value="${eItem.location || ''}" placeholder="Location" />
          </div>
          <div class="col-4">
            <input type="text" class="form-control form-control-sm exp-dates" value="${eItem.start_date || ''}${eItem.end_date ? ' - ' + eItem.end_date : ''}" placeholder="Dates (e.g. 2022 - Present)" />
          </div>
        </div>
        <textarea rows="2" class="form-control form-control-sm exp-desc mb-1" placeholder="Description & achievements">${eItem.description || ''}</textarea>
        <input type="text" class="form-control form-control-sm exp-techs" value="${(eItem.technologies || []).join(', ')}" placeholder="Technologies used (optional)" />
      `;

      card.querySelector(".exp-title").addEventListener("input", (e) => {
        exp[idx].title = e.target.value;
        currentPortfolio.experience = exp;
        renderLivePreview();
      });
      card.querySelector(".exp-comp").addEventListener("input", (e) => {
        exp[idx].company = e.target.value;
        currentPortfolio.experience = exp;
        renderLivePreview();
      });
      card.querySelector(".exp-loc").addEventListener("input", (e) => {
        exp[idx].location = e.target.value;
        currentPortfolio.experience = exp;
        renderLivePreview();
      });
      card.querySelector(".exp-dates").addEventListener("change", (e) => {
        const parts = e.target.value.split("-").map(p => p.trim());
        exp[idx].start_date = parts[0] || "";
        exp[idx].end_date = parts[1] || "";
        currentPortfolio.experience = exp;
        renderLivePreview();
      });
      card.querySelector(".exp-desc").addEventListener("input", (e) => {
        exp[idx].description = e.target.value;
        currentPortfolio.experience = exp;
        renderLivePreview();
      });
      card.querySelector(".exp-techs").addEventListener("change", (e) => {
        exp[idx].technologies = e.target.value.split(",").map(t => t.trim()).filter(Boolean);
        currentPortfolio.experience = exp;
        renderLivePreview();
      });
      card.querySelector(".btn-del-exp").addEventListener("click", () => {
        exp.splice(idx, 1);
        currentPortfolio.experience = exp;
        renderExperienceEditor();
        renderLivePreview();
      });

      experienceContainer.appendChild(card);
    });
  }

  function renderEducationEditor() {
    if (!educationContainer) return;
    educationContainer.innerHTML = "";
    if (!currentPortfolio) return;
    const eduList = safeParse(currentPortfolio.education, []);

    if (eduList.length === 0) {
      educationContainer.innerHTML = `<div class="text-muted small p-2 text-center bg-white rounded border">No education items yet. Click <strong>+ Add Education</strong> to add your degree.</div>`;
      return;
    }

    eduList.forEach((edu, idx) => {
      const card = document.createElement("div");
      card.className = "p-2 bg-white rounded border";
      card.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-1">
          <input type="text" class="form-control form-control-sm fw-bold edu-deg" value="${edu.degree || ''}" placeholder="Degree (e.g. B.S. in Computer Science)" />
          <button type="button" class="btn btn-sm text-danger ms-2 btn-del-edu" title="Delete">×</button>
        </div>
        <div class="row g-2 mb-1">
          <div class="col-6">
            <input type="text" class="form-control form-control-sm edu-inst" value="${edu.institution || ''}" placeholder="University / College" />
          </div>
          <div class="col-3">
            <input type="text" class="form-control form-control-sm edu-year" value="${edu.end_year || edu.year || ''}" placeholder="Year (e.g. 2022)" />
          </div>
          <div class="col-3">
            <input type="text" class="form-control form-control-sm edu-grade" value="${edu.grade || ''}" placeholder="Grade / GPA" />
          </div>
        </div>
      `;

      card.querySelector(".edu-deg").addEventListener("input", (e) => {
        eduList[idx].degree = e.target.value;
        currentPortfolio.education = eduList;
        renderLivePreview();
      });
      card.querySelector(".edu-inst").addEventListener("input", (e) => {
        eduList[idx].institution = e.target.value;
        currentPortfolio.education = eduList;
        renderLivePreview();
      });
      card.querySelector(".edu-year").addEventListener("input", (e) => {
        eduList[idx].end_year = e.target.value;
        currentPortfolio.education = eduList;
        renderLivePreview();
      });
      card.querySelector(".edu-grade").addEventListener("input", (e) => {
        eduList[idx].grade = e.target.value;
        currentPortfolio.education = eduList;
        renderLivePreview();
      });
      card.querySelector(".btn-del-edu").addEventListener("click", () => {
        eduList.splice(idx, 1);
        currentPortfolio.education = eduList;
        renderEducationEditor();
        renderLivePreview();
      });

      educationContainer.appendChild(card);
    });
  }

  function renderCertificationsEditor() {
    if (!certificationsContainer) return;
    certificationsContainer.innerHTML = "";
    if (!currentPortfolio) return;
    const certList = safeParse(currentPortfolio.certifications, []);

    if (certList.length === 0) {
      certificationsContainer.innerHTML = `<div class="text-muted small p-2 text-center bg-white rounded border">No certifications yet. Click <strong>+ Add Certification</strong> to add one.</div>`;
      return;
    }

    certList.forEach((cert, idx) => {
      const card = document.createElement("div");
      card.className = "p-2 bg-white rounded border";
      card.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-1">
          <input type="text" class="form-control form-control-sm fw-bold cert-name" value="${cert.name || ''}" placeholder="Certification Name (e.g. AWS Solutions Architect)" />
          <button type="button" class="btn btn-sm text-danger ms-2 btn-del-cert" title="Delete">×</button>
        </div>
        <div class="row g-2 mb-1">
          <div class="col-6">
            <input type="text" class="form-control form-control-sm cert-org" value="${cert.organization || ''}" placeholder="Issuing Organization" />
          </div>
          <div class="col-6">
            <input type="text" class="form-control form-control-sm cert-year" value="${cert.year || ''}" placeholder="Year / Date" />
          </div>
          <div class="col-12">
            <input type="url" class="form-control form-control-sm cert-url" value="${cert.credential_url || cert.url || ''}" placeholder="Credential URL or ID" />
          </div>
        </div>
      `;

      card.querySelector(".cert-name").addEventListener("input", (e) => {
        certList[idx].name = e.target.value;
        currentPortfolio.certifications = certList;
        renderLivePreview();
      });
      card.querySelector(".cert-org").addEventListener("input", (e) => {
        certList[idx].organization = e.target.value;
        currentPortfolio.certifications = certList;
        renderLivePreview();
      });
      card.querySelector(".cert-year").addEventListener("input", (e) => {
        certList[idx].year = e.target.value;
        currentPortfolio.certifications = certList;
        renderLivePreview();
      });
      card.querySelector(".cert-url").addEventListener("input", (e) => {
        certList[idx].credential_url = e.target.value;
        currentPortfolio.certifications = certList;
        renderLivePreview();
      });
      card.querySelector(".btn-del-cert").addEventListener("click", () => {
        certList.splice(idx, 1);
        currentPortfolio.certifications = certList;
        renderCertificationsEditor();
        renderLivePreview();
      });

      certificationsContainer.appendChild(card);
    });
  }

  function renderServicesEditor() {
    if (!servicesContainer) return;
    servicesContainer.innerHTML = "";
    if (!currentPortfolio) return;
    const servList = safeParse(currentPortfolio.services, []);

    if (servList.length === 0) {
      servicesContainer.innerHTML = `<div class="text-muted small p-2 text-center bg-white rounded border">No services yet. Click <strong>+ Add Service</strong> to highlight offerings.</div>`;
      return;
    }

    servList.forEach((serv, idx) => {
      const card = document.createElement("div");
      card.className = "p-2 bg-white rounded border";
      card.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-1">
          <div class="d-flex align-items-center gap-1 flex-grow-1">
            <input type="text" class="form-control form-control-sm serv-icon" value="${serv.icon || '⚡'}" style="width: 45px;" placeholder="Icon" />
            <input type="text" class="form-control form-control-sm fw-bold serv-title" value="${serv.title || ''}" placeholder="Service Title (e.g. Cloud Architecture)" />
          </div>
          <button type="button" class="btn btn-sm text-danger ms-2 btn-del-serv" title="Delete">×</button>
        </div>
        <textarea rows="2" class="form-control form-control-sm serv-desc" placeholder="Brief service description">${serv.description || ''}</textarea>
      `;

      card.querySelector(".serv-icon").addEventListener("input", (e) => {
        servList[idx].icon = e.target.value;
        currentPortfolio.services = servList;
        renderLivePreview();
      });
      card.querySelector(".serv-title").addEventListener("input", (e) => {
        servList[idx].title = e.target.value;
        currentPortfolio.services = servList;
        renderLivePreview();
      });
      card.querySelector(".serv-desc").addEventListener("input", (e) => {
        servList[idx].description = e.target.value;
        currentPortfolio.services = servList;
        renderLivePreview();
      });
      card.querySelector(".btn-del-serv").addEventListener("click", () => {
        servList.splice(idx, 1);
        currentPortfolio.services = servList;
        renderServicesEditor();
        renderLivePreview();
      });

      servicesContainer.appendChild(card);
    });
  }

  function renderSocialLinksEditor() {
    if (!currentPortfolio) return;
    const s = safeParse(currentPortfolio.social_links, {});
    inputSocialEmail.value = s.email || "";
    if (inputSocialPhone) inputSocialPhone.value = s.phone || "";
    inputSocialLocation.value = s.location || "";
    if (inputSocialWebsite) inputSocialWebsite.value = s.website || s.portfolio || "";
    inputSocialLinkedin.value = s.linkedin || "";
    inputSocialGithub.value = s.github || "";

    const syncSocial = () => {
      currentPortfolio.social_links = {
        email: inputSocialEmail.value.trim(),
        phone: inputSocialPhone ? inputSocialPhone.value.trim() : (s.phone || ""),
        location: inputSocialLocation.value.trim(),
        website: inputSocialWebsite ? inputSocialWebsite.value.trim() : (s.website || ""),
        portfolio: inputSocialWebsite ? inputSocialWebsite.value.trim() : (s.portfolio || ""),
        linkedin: inputSocialLinkedin.value.trim(),
        github: inputSocialGithub.value.trim(),
      };
      renderLivePreview();
    };

    inputSocialEmail.oninput = syncSocial;
    if (inputSocialPhone) inputSocialPhone.oninput = syncSocial;
    inputSocialLocation.oninput = syncSocial;
    if (inputSocialWebsite) inputSocialWebsite.oninput = syncSocial;
    inputSocialLinkedin.oninput = syncSocial;
    inputSocialGithub.oninput = syncSocial;
  }

  function openEditMode(sectionId = null) {
    if (tabBtnContent && window.bootstrap && bootstrap.Tab) {
      const bsTab = bootstrap.Tab.getOrCreateInstance(tabBtnContent);
      bsTab.show();
    }
    if (controlsColumn && controlsColumn.classList.contains("d-none")) {
      controlsColumn.classList.remove("d-none");
      if (previewColumn) previewColumn.className = "col-xl-7 col-lg-6";
      if (btnToggleExpand) btnToggleExpand.innerHTML = "⛶ Expand";
    }
    const target = sectionId ? document.getElementById(sectionId) : (document.getElementById("studio-inspector-card") || document.getElementById("tab-content"));
    if (target) {
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    }
    if (inputCandidateName && !sectionId) {
      setTimeout(() => inputCandidateName.focus(), 350);
    }
  }

  function bindEditModeControls() {
    if (btnToggleEditMode) btnToggleEditMode.addEventListener("click", () => openEditMode());
    if (btnBannerEdit) btnBannerEdit.addEventListener("click", () => openEditMode());
    if (btnQuickEditPreview) btnQuickEditPreview.addEventListener("click", () => openEditMode());
    if (btnSavePortfolioBottom) btnSavePortfolioBottom.addEventListener("click", () => btnSavePortfolio.click());
  }

  /**
   * Save, Publish, Check Slug & Export Flows
   */
  function bindPublishAndExportControls() {
    btnSavePortfolio.addEventListener("click", async () => {
      if (!currentPortfolio) return;
      btnSavePortfolio.disabled = true;
      btnSavePortfolio.textContent = "Saving...";

      try {
        const customCssValue = currentPortfolio.custom_css || (currentPortfolio.portrait_mask ? JSON.stringify({ portrait_mask: currentPortfolio.portrait_mask }) : undefined);
        const payload = {
          theme_id: currentPortfolio.theme_id,
          candidate_name: (inputCandidateName?.value || currentPortfolio.candidate_name || "").trim(),
          primary_color: currentPortfolio.primary_color,
          secondary_color: currentPortfolio.secondary_color,
          font: currentPortfolio.font,
          background_style: currentPortfolio.background_style,
          background_image: currentPortfolio.background_image,
          layout: currentPortfolio.layout,
          card_style: currentPortfolio.card_style,
          button_style: currentPortfolio.button_style,
          custom_css: customCssValue,
          dark_mode: currentPortfolio.dark_mode,
          professional_headline: currentPortfolio.professional_headline,
          about: currentPortfolio.about,
          skills: currentPortfolio.skills,
          projects: currentPortfolio.projects,
          experience: currentPortfolio.experience,
          education: currentPortfolio.education,
          certifications: currentPortfolio.certifications,
          achievements: currentPortfolio.achievements,
          services: currentPortfolio.services,
          social_links: currentPortfolio.social_links,
          slug: inputSlug.value.trim() || currentPortfolio.slug,
        };

        const res = await portfolioAPI.updateMyPortfolio(payload);
        if (res && res.data) {
          currentPortfolio = res.data;
          syncDataToUI();
          renderLivePreview();
          showAlert("💾 Portfolio changes saved successfully!", "success");
        }
      } catch (err) {
        console.error("Save error:", err);
        showAlert(err.message || "Failed to save portfolio changes.", "danger");
      } finally {
        btnSavePortfolio.disabled = false;
        btnSavePortfolio.innerHTML = "<span>💾</span> Save Changes";
      }
    });

    btnTogglePublish.addEventListener("click", async () => {
      if (!currentPortfolio) return;
      const isPub = Boolean(currentPortfolio.is_published);
      btnTogglePublish.disabled = true;

      try {
        let res;
        if (isPub) {
          res = await portfolioAPI.unpublish();
          showAlert("Portfolio unpublished. Public link is now private.", "info");
        } else {
          res = await portfolioAPI.publish();
          showAlert("🚀 Portfolio published live! Your public site is accessible.", "success");
        }

        if (res && res.data) {
          currentPortfolio = res.data;
          updatePublishStatusBadge();
          renderLivePreview();
        }
      } catch (err) {
        console.error("Publish error:", err);
        showAlert(err.message || "Could not toggle publish state.", "danger");
      } finally {
        btnTogglePublish.disabled = false;
      }
    });

    btnCheckSlug.addEventListener("click", async () => {
      const val = (inputSlug.value || "").trim();
      if (!val) {
        slugMsg.textContent = "Please enter a slug to check.";
        slugMsg.className = "small text-warning";
        return;
      }

      slugMsg.textContent = "Checking availability...";
      slugMsg.className = "small text-muted";

      try {
        const res = await portfolioAPI.checkSlug(val);
        if (res && res.data && res.data.is_available) {
          slugMsg.textContent = `✓ Slug '${res.data.slug}' is available!`;
          slugMsg.className = "small text-success fw-bold";
          if (currentPortfolio) {
            currentPortfolio.slug = res.data.slug;
            chromeSlugDisplay.textContent = res.data.slug;
          }
        } else {
          slugMsg.textContent = `✕ Slug '${val}' is already taken. Please try another.`;
          slugMsg.className = "small text-danger fw-bold";
        }
      } catch (err) {
        slugMsg.textContent = "Error checking slug.";
        slugMsg.className = "small text-danger";
      }
    });

    btnCopyLink.addEventListener("click", () => {
      const fullUrl = `${window.location.origin}/portfolio/${currentPortfolio.slug}`;
      navigator.clipboard.writeText(fullUrl).then(() => {
        btnCopyLink.innerHTML = "<span>✓</span> Copied!";
        setTimeout(() => {
          btnCopyLink.innerHTML = "<span>📋</span> Copy Link";
        }, 2000);
      });
    });

    // Standalone Self-Contained HTML Website Export
    btnExportHtml.addEventListener("click", () => {
      if (!currentPortfolio) return;
      const htmlContent = generateStandalonePortfolioHtml(currentPortfolio);
      const blob = new Blob([htmlContent], { type: "text/html" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${currentPortfolio.slug || "portfolio"}.html`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      showAlert("💾 Standalone HTML website file downloaded successfully!", "success");
    });

    btnPrintCv.addEventListener("click", () => {
      window.print();
    });

    // Logout
    const logoutBtn = document.getElementById("logout-btn");
    if (logoutBtn) {
      logoutBtn.addEventListener("click", () => {
        Session.clear();
        window.location.href = "login.html";
      });
    }
  }

  /**
   * Delete Portfolio Controls & Confirmation Modal
   */
  function bindDeleteControls() {
    const getModal = () => {
      if (!deletePortfolioModalEl) return null;
      if (typeof bootstrap !== "undefined" && bootstrap.Modal) {
        return bootstrap.Modal.getOrCreateInstance(deletePortfolioModalEl);
      }
      return null;
    };

    const showDeleteConfirmation = () => {
      if (!currentPortfolio || !currentPortfolio.id) {
        showAlert("No saved portfolio found to delete.", "info");
        return;
      }
      if (modalDeleteSlug) {
        modalDeleteSlug.textContent = currentPortfolio.slug ? `/portfolio/${currentPortfolio.slug}` : "Draft Portfolio";
      }
      const modal = getModal();
      if (modal) {
        modal.show();
      } else {
        if (confirm("Are you sure you want to permanently delete your portfolio? This action cannot be undone.")) {
          executeDeletePortfolio();
        }
      }
    };

    if (btnDeletePortfolio) {
      btnDeletePortfolio.addEventListener("click", showDeleteConfirmation);
    }
    if (btnDeletePortfolioTab) {
      btnDeletePortfolioTab.addEventListener("click", showDeleteConfirmation);
    }

    if (btnConfirmDeletePortfolio) {
      btnConfirmDeletePortfolio.addEventListener("click", executeDeletePortfolio);
    }

    async function executeDeletePortfolio() {
      if (!currentPortfolio) return;
      if (deleteBtnSpinner) deleteBtnSpinner.classList.remove("d-none");
      if (btnConfirmDeletePortfolio) btnConfirmDeletePortfolio.disabled = true;

      try {
        const res = await portfolioAPI.deleteMyPortfolio();
        if (res && res.success !== false) {
          const modal = getModal();
          if (modal) modal.hide();

          // Reset internal state
          currentPortfolio = null;

          // Reset UI Status Badges and Buttons
          if (statusPill) {
            statusPill.textContent = "Status: Not Created";
            statusPill.className = "badge bg-secondary-subtle text-secondary px-3 py-2 rounded-pill fw-semibold";
          }
          if (publicLinkGroup) publicLinkGroup.classList.add("d-none");
          if (portfolioReadyBanner) portfolioReadyBanner.classList.add("d-none");
          if (previewThemeIndicator) previewThemeIndicator.textContent = "Theme: None";
          if (chromeSlugDisplay) chromeSlugDisplay.textContent = "none";
          if (inputSlug) inputSlug.value = "";
          if (btnTogglePublish) {
            btnTogglePublish.innerHTML = "<span>🚀</span> Publish Portfolio";
            btnTogglePublish.className = "btn btn-sm btn-success fw-bold px-3 py-2 shadow-sm d-flex align-items-center gap-1";
          }

          // Reset Form Input Fields
          if (inputHeadline) inputHeadline.value = "";
          if (textareaAbout) textareaAbout.value = "";
          if (metricsContainer) metricsContainer.innerHTML = "";
          if (skillsContainer) skillsContainer.innerHTML = "";
          if (projectsContainer) projectsContainer.innerHTML = "";
          if (experienceContainer) experienceContainer.innerHTML = "";
          if (educationContainer) educationContainer.innerHTML = "";
          if (certificationsContainer) certificationsContainer.innerHTML = "";
          if (servicesContainer) servicesContainer.innerHTML = "";

          // Render Clean Empty-State Preview Stage
          if (previewStage) {
            previewStage.innerHTML = `
              <div class="d-flex flex-column align-items-center justify-content-center py-5 text-center px-4" style="min-height: 520px;">
                <div class="p-4 rounded-circle bg-light mb-3 shadow-sm" style="font-size: 3rem;">🌐</div>
                <h4 class="fw-bold text-dark mb-2">Portfolio Deleted</h4>
                <p class="text-muted small mb-4" style="max-width: 480px;">
                  Your generated portfolio has been deleted. Enter a prompt above or re-upload your resume anytime to generate a brand new portfolio!
                </p>
                <button type="button" class="btn btn-primary fw-bold px-4 py-2 rounded-3 shadow-sm d-inline-flex align-items-center gap-2" onclick="document.getElementById('input-ai-prompt').focus()">
                  <span>✨</span> Generate New Portfolio
                </button>
              </div>
            `;
          }

          showAlert("🗑️ Portfolio permanently deleted successfully.", "success");
        } else {
          throw new Error(res?.message || "Failed to delete portfolio");
        }
      } catch (err) {
        console.error("Delete portfolio error:", err);
        showAlert(err.message || "Failed to delete portfolio.", "danger");
      } finally {
        if (deleteBtnSpinner) deleteBtnSpinner.classList.add("d-none");
        if (btnConfirmDeletePortfolio) btnConfirmDeletePortfolio.disabled = false;
      }
    }
  }

  /**
   * Generates a self-contained offline HTML website for download
   */
  function generateStandalonePortfolioHtml(portfolio) {
    const renderedHtml = previewStage.innerHTML;
    const title = `${portfolio.candidate_name || 'Candidate'} — ${portfolio.professional_headline || 'Portfolio'}`;
    const font = portfolio.font || "Plus Jakarta Sans";

    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Inter:wght@400;500;600;700&family=Outfit:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;1,600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: '${font}', system-ui, -apple-system, sans-serif;
      margin: 0;
      padding: 0;
      background-color: ${portfolio.dark_mode ? '#090d16' : '#f8fafc'};
      color: ${portfolio.dark_mode ? '#f8fafc' : '#0f172a'};
    }
  </style>
</head>
<body data-bs-theme="${portfolio.dark_mode ? 'dark' : 'light'}">
  <div id="portfolio-root">
    ${renderedHtml}
  </div>
</body>
</html>`;
  }

  // Start initialization
  init();
});
