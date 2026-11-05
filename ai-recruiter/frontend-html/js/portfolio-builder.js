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

  // DOM Elements - Prompt Center & Editor
  const inputAiPrompt = document.getElementById("input-ai-prompt");
  const btnAutoDraftPrompt = document.getElementById("btn-auto-draft-prompt");
  const btnCopyPrompt = document.getElementById("btn-copy-prompt");
  const btnClearPrompt = document.getElementById("btn-clear-prompt");
  const promptCharCount = document.getElementById("prompt-char-count");
  const promptEditBadge = document.getElementById("prompt-edit-badge");
  const promptModPills = document.querySelectorAll(".prompt-mod-pill");
  const checkIncludeResume = document.getElementById("check-include-resume");
  const btnGenerateGemini = document.getElementById("btn-generate-with-gemini");
  const btnGenerateIcon = document.getElementById("btn-generate-icon");
  const btnGenerateText = document.getElementById("btn-generate-text");
  const promptStarters = document.querySelectorAll(".prompt-starter-chip");
  const btnResetTemplate = document.getElementById("btn-reset-template");
  const templateCategoryPills = document.querySelectorAll(".template-cat-pill");
  const templateCards = document.querySelectorAll(".prompt-template-card");
  const dimModPills = document.querySelectorAll(".dim-mod-pill");

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

  // DOM Elements - Profile Image / Portrait
  const inputProfileImageFile = document.getElementById("input-profile-image-file");
  const btnUploadProfileImage = document.getElementById("btn-upload-profile-image");
  const btnRemoveProfileImage = document.getElementById("btn-remove-profile-image");
  const inputProfileImageUrl = document.getElementById("input-profile-image-url");
  const btnApplyImageUrl = document.getElementById("btn-apply-image-url");
  const builderPhotoPreviewWrap = document.getElementById("builder-photo-preview-wrap");
  const btnQuickPhotoClick = document.getElementById("btn-quick-photo-click");
  const badgePhotoStatus = document.getElementById("badge-photo-status");
  const btnHeroChangePhoto = document.getElementById("btn-hero-change-photo");
  const heroPhotoBtnText = document.getElementById("hero-photo-btn-text");

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

  // DOM Elements - Audit & Strength Meter
  const auditScoreBadge = document.getElementById("audit-score-badge");
  const auditProgressBar = document.getElementById("audit-progress-bar");
  const auditCheckBio = document.getElementById("audit-check-bio");
  const auditCheckMetrics = document.getElementById("audit-check-metrics");
  const auditCheckProjects = document.getElementById("audit-check-projects");
  const auditCheckServices = document.getElementById("audit-check-services");
  const btnAuditFixBio = document.getElementById("btn-audit-fix-bio");
  const btnAuditFixMetrics = document.getElementById("btn-audit-fix-metrics");
  const btnAuditFixProjects = document.getElementById("btn-audit-fix-projects");
  const btnAuditFixServices = document.getElementById("btn-audit-fix-services");

  // DOM Elements - AI Quick Generator Buttons
  const btnAiGenerateMetrics = document.getElementById("btn-ai-generate-metrics");
  const btnAiGenerateServices = document.getElementById("btn-ai-generate-services");

  // DOM Elements - Preview Controls
  const btnPreviewDarkToggle = document.getElementById("btn-preview-dark-toggle");
  const secVisChecks = document.querySelectorAll(".sec-vis-check");

  // DOM Elements - Recruiter Pitch & Share Suite
  const btnRecruiterPitchModal = document.getElementById("btn-recruiter-pitch-modal");
  const recruiterPitchModalEl = document.getElementById("recruiterPitchModal");
  const textPitchLinkedin = document.getElementById("text-pitch-linkedin");
  const textPitchEmail = document.getElementById("text-pitch-email");
  const textPitchQuick = document.getElementById("text-pitch-quick");
  const qrCodeImg = document.getElementById("qr-code-img");
  const btnCopyPitches = document.querySelectorAll(".btn-copy-pitch");

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
    bindProfileImageControls();
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
          const genRes = await portfolioAPI.generate({ theme_id: "auto" });
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

    // Check for incoming custom prompt from website/homepage launcher or URL parameter
    const urlParams = new URLSearchParams(window.location.search);
    const incomingPrompt = urlParams.get("prompt") || sessionStorage.getItem("pending_portfolio_prompt");
    const autoGenRequested = urlParams.get("autoGenerate") === "true" || !!sessionStorage.getItem("pending_portfolio_prompt");

    if (incomingPrompt && incomingPrompt.trim()) {
      sessionStorage.removeItem("pending_portfolio_prompt");
      if (inputAiPrompt) {
        inputAiPrompt.value = incomingPrompt.trim();
        adjustPromptHeight();
        updatePromptCharCount();
        if (promptEditBadge) {
          promptEditBadge.innerHTML = `<span>✨</span> Custom Prompt Loaded`;
          promptEditBadge.className = "badge bg-indigo-subtle text-light small d-flex align-items-center gap-1";
        }
      }
      if (autoGenRequested && btnGenerateGemini) {
        setTimeout(() => {
          btnGenerateGemini.click();
        }, 350);
      }
    }
  }

  function setupInitialDefaultPortfolio(user) {
    currentPortfolio = {
      candidate_name: user?.name || "Candidate",
      generation_prompt: "",
      profile_image: user?.profile_photo || "",
      portrait_mask: "mask-pebble",
      professional_headline: "",
      headline_options: [],
      about: "",
      theme_id: "modern",
      primary_color: "#4f46e5",
      secondary_color: "#06b6d4",
      font: "Plus Jakarta Sans",
      background_style: "mesh",
      card_style: "glass",
      button_style: "rounded",
      dark_mode: false,
      layout: "modern",
      achievements: [],
      skills: {},
      services: [],
      projects: [],
      experience: [],
      education: [],
      certifications: [],
      social_links: {
        email: user?.email || "",
        location: "",
        github: "",
        linkedin: "",
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

    // Prompt Center Sync: Pre-fill existing prompt or smart candidate draft so it's always editable
    if (inputAiPrompt) {
      if (currentPortfolio.generation_prompt && currentPortfolio.generation_prompt.trim()) {
        inputAiPrompt.value = currentPortfolio.generation_prompt.trim();
      } else if (!inputAiPrompt.value || !inputAiPrompt.value.trim()) {
        inputAiPrompt.value = buildSmartCandidatePrompt(currentPortfolio, Session.getUser());
      }
      adjustPromptHeight();
      updatePromptCharCount();
    }

    // Render Sub-Sections in UI
    renderProfileImageEditor();
    renderMetricsEditor();
    renderSkillsEditor();
    renderProjectsEditor();
    renderExperienceEditor();
    renderEducationEditor();
    renderCertificationsEditor();
    renderServicesEditor();
    renderSocialLinksEditor();

    // Sync Section Visibility Checkboxes
    const currentVis = safeParse(currentPortfolio.section_visibility, {});
    secVisChecks.forEach(chk => {
      const sec = chk.getAttribute("data-section");
      if (sec in currentVis) {
        chk.checked = currentVis[sec] !== false;
      }
    });

    // Update Live Recruiter Readiness Audit Score
    updateAuditScore();
  }

  /**
   * Evaluates portfolio completeness and assigns a 0-100% Recruiter Readiness score.
   */
  function updateAuditScore() {
    if (!currentPortfolio || !auditScoreBadge || !auditProgressBar) return;
    let score = 0;

    // 1. Headline & Bio (25 pts)
    const hl = (currentPortfolio.professional_headline || "").trim();
    const ab = (currentPortfolio.about || "").trim();
    const bioPass = hl.length > 8 && ab.length > 40;
    if (hl.length > 8) score += 10;
    if (ab.length > 40) score += 15;
    if (auditCheckBio) {
      auditCheckBio.innerHTML = bioPass 
        ? '<span class="text-success fw-bold">✓</span>' 
        : '<span class="text-warning fw-bold">!</span>';
    }

    // 2. Metrics & KPIs (25 pts)
    const metrics = safeParse(currentPortfolio.achievements, []);
    const metricsPass = metrics.length >= 3;
    score += Math.min(25, metrics.length * 7);
    if (auditCheckMetrics) {
      auditCheckMetrics.innerHTML = metricsPass 
        ? '<span class="text-success fw-bold">✓</span>' 
        : '<span class="text-warning fw-bold">!</span>';
    }

    // 3. Projects & Case Studies (25 pts)
    const projects = safeParse(currentPortfolio.projects, []);
    let projPts = 0;
    if (projects.length >= 1) projPts += 10;
    if (projects.length >= 2) projPts += 10;
    const hasDetailedProj = projects.some(p => (p.key_features && p.key_features.length > 0) || (p.technologies && p.technologies.length > 1));
    if (hasDetailedProj) projPts += 5;
    score += projPts;
    const projectsPass = projects.length >= 2;
    if (auditCheckProjects) {
      auditCheckProjects.innerHTML = projectsPass 
        ? '<span class="text-success fw-bold">✓</span>' 
        : '<span class="text-warning fw-bold">!</span>';
    }

    // 4. Value Pillars / Services (15 pts)
    const services = safeParse(currentPortfolio.services, []);
    const servicesPass = services.length >= 2;
    score += Math.min(15, services.length * 5);
    if (auditCheckServices) {
      auditCheckServices.innerHTML = servicesPass 
        ? '<span class="text-success fw-bold">✓</span>' 
        : '<span class="text-warning fw-bold">!</span>';
    }

    // 5. Contact & Social Channels (10 pts)
    const soc = safeParse(currentPortfolio.social_links, {});
    let socPts = 0;
    if (soc.email) socPts += 4;
    if (soc.location) socPts += 3;
    if (soc.github || soc.linkedin) socPts += 3;
    score += socPts;

    // Bound score 0-100
    score = Math.min(100, Math.max(10, score));

    // Update UI
    auditProgressBar.style.width = `${score}%`;
    if (score >= 90) {
      auditScoreBadge.className = "badge bg-success-subtle text-success border px-2.5 py-1 fw-bold";
      auditScoreBadge.textContent = `Score: ${score}% (Recruiter Ready 🌟)`;
      auditProgressBar.className = "progress-bar bg-success";
    } else if (score >= 70) {
      auditScoreBadge.className = "badge bg-primary-subtle text-primary border px-2.5 py-1 fw-bold";
      auditScoreBadge.textContent = `Score: ${score}% (Solid Impact 🚀)`;
      auditProgressBar.className = "progress-bar bg-primary";
    } else {
      auditScoreBadge.className = "badge bg-warning-subtle text-dark border px-2.5 py-1 fw-bold";
      auditScoreBadge.textContent = `Score: ${score}% (Needs Details ⚠️)`;
      auditProgressBar.className = "progress-bar bg-warning";
    }
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

      // Make rendered avatar/portrait clickable to quickly replace image
      const previewAvatars = previewStage.querySelectorAll(
        ".nova-portrait-frame, .portfolio-avatar-wrap, .portfolio-avatar-monogram, .bento-avatar-card, .notion-avatar-wrap, img.nova-portrait-img"
      );
      previewAvatars.forEach(el => {
        el.style.cursor = "pointer";
        el.setAttribute("title", "Click to change or replace profile image");
        el.addEventListener("click", (e) => {
          e.preventDefault();
          e.stopPropagation();
          if (inputProfileImageFile) {
            inputProfileImageFile.click();
          }
        });
      });
    } catch (err) {
      console.error("Rendering error in PortfolioThemesEngine:", err);
    }
  }

  /**
   * Automatically resizes the prompt textarea based on content length
   */
  function adjustPromptHeight() {
    if (!inputAiPrompt) return;
    inputAiPrompt.style.height = "auto";
    const newH = Math.max(105, Math.min(inputAiPrompt.scrollHeight, 320));
    inputAiPrompt.style.height = `${newH}px`;
  }

  /**
   * Updates live character count and editor status badge
   */
  function updatePromptCharCount() {
    if (!inputAiPrompt) return;
    const count = (inputAiPrompt.value || "").length;
    if (promptCharCount) {
      promptCharCount.textContent = `${count} characters`;
    }
    if (promptEditBadge) {
      if (count > 0) {
        promptEditBadge.innerHTML = `<span>✏️</span> Customizing Prompt`;
        promptEditBadge.className = "badge bg-indigo-subtle text-light small d-flex align-items-center gap-1";
      } else {
        promptEditBadge.innerHTML = `<span>💡</span> Ready for Prompt`;
        promptEditBadge.className = "badge bg-secondary-subtle text-white-50 small d-flex align-items-center gap-1";
      }
    }
  }

  /**
   * Synthesizes an intelligent, personalized candidate prompt based on verified profile facts
   */
  function buildSmartCandidatePrompt(portfolio, user) {
    const name = (portfolio?.candidate_name || user?.name || "Candidate").trim();
    const headline = (portfolio?.professional_headline || "Software Engineer").trim();
    const layout = portfolio?.layout || "modern";
    const theme = portfolio?.theme_id || "modern";
    const skillsObj = portfolio?.skills || {};
    let skillList = [];
    if (Array.isArray(skillsObj)) {
      skillList = skillsObj;
    } else if (typeof skillsObj === "object" && skillsObj !== null) {
      skillList = Object.values(skillsObj).flat();
    }
    const topSkills = skillList.filter(s => typeof s === "string" && s.trim()).slice(0, 6).join(", ");

    let p = `Create a high-impact, modern portfolio website for ${name}, ${headline}`;
    if (topSkills) {
      p += ` with verified expertise in ${topSkills}`;
    }
    p += `. Highlight scalable architecture, clean responsive design, and quantified achievements using a ${layout} layout in ${theme} theme.`;
    return p;
  }

  const PORTFOLIO_PROMPT_TEMPLATES = [
    {
      id: "bento-modular",
      category: "bento",
      name: "Ultra-Modern Bento",
      badge: "Modular Grid • Kinetic Glass",
      icon: "🍱",
      layout: "modern",
      theme_id: "modern",
      primary_color: "#4f46e5",
      secondary_color: "#10b981",
      ambient_color: "#0f172a",
      dark_mode: true,
      animation: "✨ 3D Tilt Cards & Glass Glow",
      prompt: "Create an award-winning portfolio with a modern Bento modular grid layout for an innovative engineer. Use a deep midnight slate theme with electric indigo (#4f46e5) and vibrant emerald (#10b981) accents. Feature frosted glassmorphic cards, 3D perspective tilt physics on hover, interactive metric counters, and showcase high-impact projects with live demo links."
    },
    {
      id: "cyber-hud",
      category: "ai",
      name: "Cyberpunk Neural HUD",
      badge: "AI Telemetry • Holographic",
      icon: "🤖",
      layout: "ai_tech",
      theme_id: "ai_tech",
      primary_color: "#00e5ff",
      secondary_color: "#a855f7",
      ambient_color: "#090d16",
      dark_mode: true,
      animation: "⚡ Glowing Pulse & Radar Telemetry",
      prompt: "Design a futuristic Cyberpunk Neural HUD portfolio for an advanced AI & Systems Specialist. Use an ultra-dark OLED obsidian palette with glowing neon cyan (#00e5ff) and hyper-violet (#a855f7) accents. Incorporate telemetry radar stats, neural network architecture flowcharts, sub-100ms inference benchmarks, and animated terminal command line widgets."
    },
    {
      id: "terminal-ide",
      category: "developer",
      name: "Developer Terminal IDE",
      badge: "Terminal Workstation • Monospace",
      icon: "💻",
      layout: "developer",
      theme_id: "developer",
      primary_color: "#22c55e",
      secondary_color: "#38bdf8",
      ambient_color: "#0a0e14",
      dark_mode: true,
      animation: "⌨️ Terminal Cursor Typing & Git Graph",
      prompt: "Create an authentic Developer Terminal IDE portfolio with a dark workstation code aesthetic. Use a Matrix carbon black background (#0a0e14) with phosphor emerald green (#22c55e) and sky blue (#38bdf8) syntax highlights. Include an interactive typewriter terminal headline, collapsible code file trees, git commit activity graph, and live system status pills."
    },
    {
      id: "swiss-minimal",
      category: "minimalist",
      name: "Minimalist Swiss Editorial",
      badge: "Monograph • Clean Typography",
      icon: "📐",
      layout: "minimal",
      theme_id: "minimal",
      primary_color: "#18181b",
      secondary_color: "#e11d48",
      ambient_color: "#f8fafc",
      dark_mode: false,
      animation: "📐 Hairline Dividers & Smooth Fade",
      prompt: "Build an ultra-clean, minimalist Swiss editorial monograph portfolio for a Principal Architect. Use an asymmetrical high-contrast grid with ivory light or obsidian charcoal tones, crisp hairline borders, and striking crimson carmine (#e11d48) accents. Focus on bold typography, executive impact summaries, and refined, distraction-free case studies."
    },
    {
      id: "creative-studio",
      category: "creative",
      name: "Creative Neo-Studio",
      badge: "Neo-Display • Fluid Gradients",
      icon: "🎨",
      layout: "creative",
      theme_id: "creative",
      primary_color: "#f97316",
      secondary_color: "#8b5cf6",
      ambient_color: "#1e1b4b",
      dark_mode: true,
      animation: "💫 Magnetic Fluid Hover & Dynamic Mesh",
      prompt: "Design an expressive, creative neo-studio portfolio for a Senior UI/UX & Frontend Creative Technologist. Use warm sunset terracotta (#f97316) and amethyst violet (#8b5cf6) gradients over deep slate. Feature floating organic project vignettes, magnetic fluid hover physics, bold typography badges, and an interactive project sandbox."
    },
    {
      id: "executive-dossier",
      category: "executive",
      name: "Executive Leadership Dossier",
      badge: "2-Column • Strategic Impact",
      icon: "💼",
      layout: "corporate",
      theme_id: "corporate",
      primary_color: "#0f172a",
      secondary_color: "#2563eb",
      ambient_color: "#f59e0b",
      dark_mode: false,
      animation: "📊 Kinetic KPI Counters & Subtle Lift",
      prompt: "Construct a prestigious Executive Briefing Dossier portfolio for an Engineering Director & Technology Leader. Use an authoritative 2-column layout with deep royal navy (#0f172a), cobalt blue (#2563eb), and champagne gold (#f59e0b) accents. Highlight team scaling metrics (30+ engineers), multi-million cloud cost optimization, and board-level strategic roadmaps."
    },
    {
      id: "data-science-lab",
      category: "ai",
      name: "Algorithmic Data Science Lab",
      badge: "Scientific Bento • Benchmarks",
      icon: "🔬",
      layout: "ai_tech",
      theme_id: "dashboard",
      primary_color: "#0d9488",
      secondary_color: "#f59e0b",
      ambient_color: "#0b192c",
      dark_mode: true,
      animation: "📈 Animated Model Curves & Pipeline Flow",
      prompt: "Build a high-precision Scientific Bento Dashboard portfolio for a Senior Data Scientist & Quantitative Researcher. Use dark oceanic navy (#0b192c) with precision teal (#0d9488) and amber (#f59e0b) accents. Showcase interactive machine learning model accuracy curves, data pipeline diagrams, distributed training throughput stats, and published research benchmarks."
    },
    {
      id: "split-screen-showcase",
      category: "split",
      name: "Interactive Split-Screen 3D",
      badge: "50/50 Dual Panel • Parallax",
      icon: "🪞",
      layout: "split_screen",
      theme_id: "split_screen",
      primary_color: "#f43f5e",
      secondary_color: "#7c3aed",
      ambient_color: "#111827",
      dark_mode: true,
      animation: "🌊 Parallax Dual-Scroll & Frosted Glass",
      prompt: "Create a modern 50/50 Split-Screen portfolio for a Full-Stack Product Builder. Feature a sticky personal brand hero on the left with glowing social links and dynamic availability badge, and an immersive scrollable project showcase on the right with frosted glass refraction, live demo popovers, and smooth parallax depth scrolling."
    }
  ];

  let activePromptTemplateId = "bento-modular";

  /**
   * Binds Prompt Starters, Creative Templates, Dimension Modifiers, Live Editing, and Gemini Generation
   */
  function bindPromptStarters() {
    // 1. Textarea auto-resize and live character count
    if (inputAiPrompt) {
      inputAiPrompt.addEventListener("input", () => {
        adjustPromptHeight();
        updatePromptCharCount();
        if (promptEditBadge) {
          promptEditBadge.innerHTML = `<span>✏️</span> Custom Edited`;
          promptEditBadge.className = "badge bg-warning-subtle text-light small d-flex align-items-center gap-1";
        }
      });
    }

    // 2. Creative Template Category Filters
    const catPills = document.querySelectorAll(".template-cat-pill");
    const cards = document.querySelectorAll(".prompt-template-card");
    catPills.forEach(pill => {
      pill.addEventListener("click", () => {
        catPills.forEach(p => p.classList.remove("active"));
        pill.classList.add("active");
        const category = pill.getAttribute("data-category");

        cards.forEach(card => {
          const cardCat = card.getAttribute("data-category");
          if (category === "all" || cardCat === category) {
            card.style.display = "flex";
          } else {
            card.style.display = "none";
          }
        });
      });
    });

    // 3. Creative Template Cards Click & Selection
    cards.forEach(card => {
      card.addEventListener("click", () => {
        const tId = card.getAttribute("data-template-id");
        const tmpl = PORTFOLIO_PROMPT_TEMPLATES.find(t => t.id === tId);
        if (!tmpl) return;

        activePromptTemplateId = tId;
        cards.forEach(c => c.classList.remove("active"));
        card.classList.add("active");

        // Load prompt template into textarea
        if (inputAiPrompt) {
          inputAiPrompt.value = tmpl.prompt;
          adjustPromptHeight();
          updatePromptCharCount();
          inputAiPrompt.focus();
        }

        // Update toolbar badge
        if (promptEditBadge) {
          promptEditBadge.innerHTML = `<span>${tmpl.icon}</span> Template: ${tmpl.name}`;
          promptEditBadge.className = "badge bg-indigo-subtle text-light small d-flex align-items-center gap-1";
        }

        // Pulse prompt editor card to highlight active customization
        const editorCard = document.getElementById("prompt-editor-card");
        if (editorCard) {
          editorCard.style.boxShadow = "0 0 0 3px rgba(129, 140, 248, 0.4), 0 10px 30px rgba(0,0,0,0.5)";
          setTimeout(() => {
            editorCard.style.boxShadow = "";
          }, 800);
        }

        showAlert(`✨ Loaded "${tmpl.name}" prompt template! You can freely edit, refine, or customize every sentence below.`, "info");
      });
    });

    // 4. Reset to Template Default Button
    if (btnResetTemplate) {
      btnResetTemplate.addEventListener("click", () => {
        const tmpl = PORTFOLIO_PROMPT_TEMPLATES.find(t => t.id === activePromptTemplateId) || PORTFOLIO_PROMPT_TEMPLATES[0];
        if (tmpl && inputAiPrompt) {
          inputAiPrompt.value = tmpl.prompt;
          adjustPromptHeight();
          updatePromptCharCount();
          if (promptEditBadge) {
            promptEditBadge.innerHTML = `<span>${tmpl.icon}</span> Template: ${tmpl.name}`;
            promptEditBadge.className = "badge bg-indigo-subtle text-light small d-flex align-items-center gap-1";
          }
          showAlert(`↺ Reset prompt to default "${tmpl.name}" template text.`, "info");
        }
      });
    }

    // 5. Auto-Draft from Profile button
    if (btnAutoDraftPrompt) {
      btnAutoDraftPrompt.addEventListener("click", () => {
        const user = Session.getUser();
        const smartPrompt = buildSmartCandidatePrompt(currentPortfolio, user);
        inputAiPrompt.value = smartPrompt;
        adjustPromptHeight();
        updatePromptCharCount();
        inputAiPrompt.focus();
        if (promptEditBadge) {
          promptEditBadge.innerHTML = `<span>🪄</span> Auto-Drafted Profile`;
          promptEditBadge.className = "badge bg-primary-subtle text-light small d-flex align-items-center gap-1";
        }
        showAlert("✨ Prompt drafted from your profile facts! You can now freely edit, customize, or tweak every word.", "info");
      });
    }

    // 6. Copy Prompt button
    if (btnCopyPrompt) {
      btnCopyPrompt.addEventListener("click", () => {
        const val = (inputAiPrompt.value || "").trim();
        if (!val) {
          showAlert("Prompt is empty, nothing to copy.", "warning");
          return;
        }
        navigator.clipboard.writeText(val);
        const orig = btnCopyPrompt.innerHTML;
        btnCopyPrompt.innerHTML = `<span>✓</span> Copied!`;
        btnCopyPrompt.classList.replace("btn-outline-light", "btn-success");
        setTimeout(() => {
          btnCopyPrompt.innerHTML = orig;
          btnCopyPrompt.classList.replace("btn-success", "btn-outline-light");
        }, 2000);
      });
    }

    // 7. Clear Prompt button
    if (btnClearPrompt) {
      btnClearPrompt.addEventListener("click", () => {
        inputAiPrompt.value = "";
        adjustPromptHeight();
        updatePromptCharCount();
        inputAiPrompt.focus();
        if (promptEditBadge) {
          promptEditBadge.innerHTML = `<span>✏️</span> Blank Prompt`;
          promptEditBadge.className = "badge bg-secondary-subtle text-light small d-flex align-items-center gap-1";
        }
        showAlert("Prompt cleared. Type a custom prompt or click any template/modifier above.", "info");
      });
    }

    // 8. Dimension Fine-Tuning Studio Modifiers (Layout, Colors, Animations, Tone)
    const dimPills = document.querySelectorAll(".dim-mod-pill");
    dimPills.forEach(pill => {
      pill.addEventListener("click", () => {
        const dimValue = pill.getAttribute("data-value");
        const dimType = pill.getAttribute("data-dimension");
        if (!dimValue) return;

        let currentVal = (inputAiPrompt.value || "").trim();
        if (!currentVal) {
          const user = Session.getUser();
          currentVal = `Create an exceptional portfolio for ${currentPortfolio?.candidate_name || user?.name || "Candidate"}`;
        }

        // Avoid exact duplicate injection
        if (!currentVal.toLowerCase().includes(dimValue.toLowerCase())) {
          if (/[.!?]$/.test(currentVal)) {
            currentVal += ` Also design it ${dimValue}.`;
          } else if (/,$/.test(currentVal)) {
            currentVal += ` ${dimValue}`;
          } else {
            currentVal += `, ${dimValue}`;
          }
        }

        inputAiPrompt.value = currentVal;
        adjustPromptHeight();
        updatePromptCharCount();
        inputAiPrompt.focus();

        if (promptEditBadge) {
          promptEditBadge.innerHTML = `<span>⚡</span> Customized Directives`;
          promptEditBadge.className = "badge bg-indigo-subtle text-light small d-flex align-items-center gap-1";
        }

        // Pill visual feedback
        pill.classList.add("active");
        setTimeout(() => pill.classList.remove("active"), 1200);

        const dimLabel = dimType ? dimType.charAt(0).toUpperCase() + dimType.slice(1) : "Preference";
        showAlert(`⚡ ${dimLabel} directive added to prompt! You can continue customizing your prompt text above.`, "info");
      });
    });

    // Legacy prompt starter chips support if present
    promptStarters.forEach(chip => {
      chip.addEventListener("click", () => {
        const text = chip.getAttribute("data-prompt");
        if (text) {
          inputAiPrompt.value = text;
          adjustPromptHeight();
          updatePromptCharCount();
          inputAiPrompt.focus();
        }
      });
    });

    // 7. Generate button click
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
          currentPortfolio.generation_prompt = promptText;
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
          renderProfileImageEditor();
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
      metrics.push({ value: "", label: "", icon: "⚡" });
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
        name: "",
        description: "",
        key_features: [],
        technologies: [],
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
        title: "",
        company: "",
        location: "",
        start_date: "",
        end_date: "",
        is_current: false,
        description: "",
        highlights: [],
        technologies: [],
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
          degree: "",
          institution: "",
          end_year: "",
          grade: "",
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
          name: "",
          organization: "",
          year: "",
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
          title: "",
          description: "",
          icon: "⚡",
        });
        currentPortfolio.services = servs;
        renderServicesEditor();
        renderLivePreview();
        updateAuditScore();
      });
    }

    // AI Quick Generate 4 KPIs
    if (btnAiGenerateMetrics) {
      btnAiGenerateMetrics.addEventListener("click", async () => {
        if (!currentPortfolio) return;
        btnAiGenerateMetrics.disabled = true;
        btnAiGenerateMetrics.innerHTML = `<span class="spinner-border spinner-border-sm" role="status"></span>`;
        try {
          const skillsObj = safeParse(currentPortfolio.skills, {});
          const flatSkills = Array.isArray(skillsObj) ? skillsObj : Object.values(skillsObj).flat();
          const res = await portfolioAPI.generateMetrics({
            role: currentPortfolio.professional_headline,
            skills: flatSkills,
          });
          if (res && res.data && res.data.metrics) {
            currentPortfolio.achievements = res.data.metrics;
            renderMetricsEditor();
            renderLivePreview();
            updateAuditScore();
            showAlert("⚡ 4 Grounded impact KPIs generated successfully!", "success");
          }
        } catch (err) {
          showAlert("Could not auto-generate metrics.", "warning");
        } finally {
          btnAiGenerateMetrics.disabled = false;
          btnAiGenerateMetrics.innerHTML = "✨ AI 4 KPIs";
        }
      });
    }

    // AI Quick Generate Value Pillars
    if (btnAiGenerateServices) {
      btnAiGenerateServices.addEventListener("click", async () => {
        if (!currentPortfolio) return;
        btnAiGenerateServices.disabled = true;
        btnAiGenerateServices.innerHTML = `<span class="spinner-border spinner-border-sm" role="status"></span>`;
        try {
          const skillsObj = safeParse(currentPortfolio.skills, {});
          const flatSkills = Array.isArray(skillsObj) ? skillsObj : Object.values(skillsObj).flat();
          const res = await portfolioAPI.generateServices({
            role: currentPortfolio.professional_headline,
            skills: flatSkills,
          });
          if (res && res.data && res.data.services) {
            currentPortfolio.services = res.data.services;
            renderServicesEditor();
            renderLivePreview();
            updateAuditScore();
            showAlert("🎯 Core value proposition pillars generated successfully!", "success");
          }
        } catch (err) {
          showAlert("Could not auto-generate services.", "warning");
        } finally {
          btnAiGenerateServices.disabled = false;
          btnAiGenerateServices.innerHTML = "✨ AI Pillars";
        }
      });
    }

    // Audit Widget 1-Click AI Fix Actions
    if (btnAuditFixBio) {
      btnAuditFixBio.addEventListener("click", () => {
        if (tabBtnContent) tabBtnContent.click();
        if (btnRewriteAbout) btnRewriteAbout.click();
      });
    }
    if (btnAuditFixMetrics) {
      btnAuditFixMetrics.addEventListener("click", () => {
        if (tabBtnContent) tabBtnContent.click();
        if (btnAiGenerateMetrics) btnAiGenerateMetrics.click();
      });
    }
    if (btnAuditFixProjects) {
      btnAuditFixProjects.addEventListener("click", () => {
        if (tabBtnContent) tabBtnContent.click();
        const projs = safeParse(currentPortfolio.projects, []);
        if (projs.length === 0) {
          if (btnAddProject) btnAddProject.click();
        } else {
          const firstEnrich = document.querySelector(".btn-enrich-case-study");
          if (firstEnrich) firstEnrich.click();
        }
      });
    }
    if (btnAuditFixServices) {
      btnAuditFixServices.addEventListener("click", () => {
        if (tabBtnContent) tabBtnContent.click();
        if (btnAiGenerateServices) btnAiGenerateServices.click();
      });
    }

    // Section Visibility Checkboxes
    secVisChecks.forEach(chk => {
      chk.addEventListener("change", (e) => {
        if (!currentPortfolio) return;
        const sec = e.target.getAttribute("data-section");
        let vis = safeParse(currentPortfolio.section_visibility, {});
        vis[sec] = e.target.checked;
        currentPortfolio.section_visibility = vis;
        renderLivePreview();
        updateAuditScore();
        showAlert(`Toggled ${sec} visibility in preview.`);
      });
    });

    // Live Dark/Light Mode Toggle in Preview Chrome
    if (btnPreviewDarkToggle) {
      btnPreviewDarkToggle.addEventListener("click", () => {
        if (!currentPortfolio) return;
        currentPortfolio.dark_mode = !currentPortfolio.dark_mode;
        if (switchDarkMode) switchDarkMode.checked = currentPortfolio.dark_mode;
        btnPreviewDarkToggle.textContent = currentPortfolio.dark_mode ? "☀️" : "🌙";
        renderLivePreview();
        showAlert(`Switched to ${currentPortfolio.dark_mode ? 'Dark Mode' : 'Light Mode'}`);
      });
    }

    // Recruiter Outreach & Share Suite Modal
    if (btnRecruiterPitchModal) {
      btnRecruiterPitchModal.addEventListener("click", () => {
        if (!currentPortfolio) return;
        const slug = currentPortfolio.slug || "candidate";
        const origin = window.location.origin;
        const publicUrl = `${origin}/portfolio/${slug}`;
        const name = currentPortfolio.full_name || "Candidate";
        const headline = currentPortfolio.professional_headline || "Software Engineer";
        const skillsObj = safeParse(currentPortfolio.skills, {});
        const flatSkills = Array.isArray(skillsObj) ? skillsObj : Object.values(skillsObj).flat();
        const topSkills = flatSkills.slice(0, 5).join(", ") || "Modern Full-Stack Technologies";
        const projects = safeParse(currentPortfolio.projects, []);
        const topProjects = projects.slice(0, 3).map(p => p.name).filter(Boolean).join(", ") || "Production Systems";

        if (textPitchLinkedin) {
          textPitchLinkedin.value = `Hi [Hiring Manager / Recruiter Name],\n\nI came across your team's open engineering roles and wanted to share my interactive portfolio:\n👉 ${publicUrl}\n\nIt features my core system architectures (${topProjects}), verified technical competencies in ${topSkills}, and quantified impact metrics.\n\nI'd welcome the chance to connect and discuss how my background aligns with your engineering initiatives.\n\nBest regards,\n${name}`;
        }

        if (textPitchEmail) {
          textPitchEmail.value = `Subject: ${headline} Portfolio — ${name}\n\nDear Hiring Team,\n\nI am reaching out regarding technical opportunities at your organization. Please find my verified interactive portfolio here:\n${publicUrl}\n\nPortfolio Overview:\n• Role Focus: ${headline}\n• Core Competencies: ${topSkills}\n• Key Flagship Projects: ${topProjects}\n\nI look forward to discussing how I can deliver value to your team.\n\nSincerely,\n${name}`;
        }

        if (textPitchQuick) {
          textPitchQuick.value = `Hey! Here is my updated interactive engineering portfolio with live case studies and verified impact metrics: ${publicUrl}`;
        }

        if (qrCodeImg) {
          qrCodeImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=${encodeURIComponent(publicUrl)}`;
        }

        if (typeof bootstrap !== "undefined" && recruiterPitchModalEl) {
          const modal = bootstrap.Modal.getOrCreateInstance(recruiterPitchModalEl);
          modal.show();
        }
      });
    }

    btnCopyPitches.forEach(btn => {
      btn.addEventListener("click", () => {
        const targetId = btn.getAttribute("data-target");
        const textarea = document.getElementById(targetId);
        if (textarea && textarea.value) {
          navigator.clipboard.writeText(textarea.value);
          const originalText = btn.innerHTML;
          btn.innerHTML = `<span>✓</span> Copied to Clipboard!`;
          btn.classList.replace("btn-primary", "btn-success");
          setTimeout(() => {
            btn.innerHTML = originalText;
            btn.classList.replace("btn-success", "btn-primary");
          }, 2200);
        }
      });
    });
  }

  /**
   * Renders and updates the Profile Image / Portrait preview in the Studio Builder
   */
  function renderProfileImageEditor() {
    if (!currentPortfolio || !builderPhotoPreviewWrap) return;
    const imgUrl = (currentPortfolio.profile_image || "").trim();
    const hasPhoto = Boolean(imgUrl && !imgUrl.includes("ui-avatars.com"));
    const mask = currentPortfolio.portrait_mask || "mask-pebble";
    const name = currentPortfolio.candidate_name || "Candidate";
    const initials = name.split(/\s+/).map(p => p[0]).filter(Boolean).slice(0, 2).join("").toUpperCase() || "CP";
    const primary = currentPortfolio.primary_color || "#4f46e5";
    const secondary = currentPortfolio.secondary_color || "#06b6d4";

    if (hasPhoto) {
      builderPhotoPreviewWrap.innerHTML = `
        <img src="${escapeHtml(imgUrl)}" alt="${escapeHtml(name)}" class="w-100 h-100 object-fit-cover ${mask}" style="border-radius: 12px; transition: transform 0.25s ease;" />
      `;
      if (badgePhotoStatus) {
        badgePhotoStatus.className = "badge bg-success-subtle text-success small";
        badgePhotoStatus.textContent = "Custom Photo Active";
      }
      if (heroPhotoBtnText) {
        heroPhotoBtnText.textContent = "Change Photo ✓";
      }
      if (inputProfileImageUrl && !imgUrl.startsWith("data:")) {
        inputProfileImageUrl.value = imgUrl;
      }
    } else {
      builderPhotoPreviewWrap.innerHTML = `
        <div class="w-100 h-100 d-flex align-items-center justify-content-center fw-bold text-white shadow-sm" style="background: linear-gradient(135deg, ${primary} 0%, ${secondary} 100%); font-size: 1.25rem; letter-spacing: -0.02em; border-radius: 12px;">
          ${initials}
        </div>
      `;
      if (badgePhotoStatus) {
        badgePhotoStatus.className = "badge bg-secondary-subtle text-secondary small";
        badgePhotoStatus.textContent = "Initials Monogram";
      }
      if (heroPhotoBtnText) {
        heroPhotoBtnText.textContent = "Add Photo";
      }
      if (inputProfileImageUrl) {
        inputProfileImageUrl.value = "";
      }
    }
  }

  /**
   * Binds photo file upload, URL apply, removal, and real-time synchronization
   */
  function bindProfileImageControls() {
    const triggerUpload = () => {
      if (inputProfileImageFile) inputProfileImageFile.click();
    };

    if (btnUploadProfileImage) btnUploadProfileImage.addEventListener("click", triggerUpload);
    if (btnQuickPhotoClick) btnQuickPhotoClick.addEventListener("click", triggerUpload);
    if (btnHeroChangePhoto) btnHeroChangePhoto.addEventListener("click", triggerUpload);

    if (inputProfileImageFile) {
      inputProfileImageFile.addEventListener("change", async (e) => {
        const file = e.target.files && e.target.files[0];
        if (!file) return;

        // Instant local preview via FileReader
        const reader = new FileReader();
        reader.onload = (loadEvt) => {
          const localDataUrl = loadEvt.target.result;
          if (localDataUrl && currentPortfolio) {
            currentPortfolio.profile_image = localDataUrl;
            renderProfileImageEditor();
            renderLivePreview();
          }
        };
        reader.readAsDataURL(file);

        // Upload to backend API
        try {
          if (btnUploadProfileImage) {
            btnUploadProfileImage.disabled = true;
            btnUploadProfileImage.innerHTML = `<span>⏳</span> Uploading...`;
          }
          if (window.portfolioAPI && typeof window.portfolioAPI.uploadProfileImage === "function") {
            const res = await window.portfolioAPI.uploadProfileImage(file);
            if (res && res.data && res.data.profile_image) {
              currentPortfolio.profile_image = res.data.profile_image;
              renderProfileImageEditor();
              renderLivePreview();
              showAlert("Profile image uploaded and updated successfully!", "success");
            }
          } else {
            await portfolioAPI.updateMyPortfolio({ profile_image: currentPortfolio.profile_image });
            showAlert("Profile image updated!", "success");
          }
        } catch (err) {
          console.warn("Upload API warning (retaining instant local preview):", err);
          showAlert("Profile image applied to preview!", "info");
        } finally {
          if (btnUploadProfileImage) {
            btnUploadProfileImage.disabled = false;
            btnUploadProfileImage.innerHTML = `<span>⬆️</span> Upload Image`;
          }
          inputProfileImageFile.value = "";
        }
      });
    }

    if (btnRemoveProfileImage) {
      btnRemoveProfileImage.addEventListener("click", async () => {
        if (!currentPortfolio) return;
        currentPortfolio.profile_image = "";
        renderProfileImageEditor();
        renderLivePreview();
        try {
          await portfolioAPI.updateMyPortfolio({ profile_image: "" });
          showAlert("Profile photo removed. Initial monogram is now active.", "info");
        } catch (err) {
          console.error("Failed to reset profile image:", err);
        }
      });
    }

    if (btnApplyImageUrl && inputProfileImageUrl) {
      btnApplyImageUrl.addEventListener("click", async () => {
        const url = (inputProfileImageUrl.value || "").trim();
        if (!url) {
          showAlert("Please enter a valid image URL", "warning");
          return;
        }
        if (currentPortfolio) {
          currentPortfolio.profile_image = url;
          renderProfileImageEditor();
          renderLivePreview();
          try {
            await portfolioAPI.updateMyPortfolio({ profile_image: url });
            showAlert("Profile image URL applied successfully!", "success");
          } catch (err) {
            console.error("Failed to save image URL:", err);
          }
        }
      });
    }
  }

  function renderMetricsEditor() {
    metricsContainer.innerHTML = "";
    if (!currentPortfolio) return;
    const metrics = safeParse(currentPortfolio.achievements, []);

    if (metrics.length === 0) {
      metricsContainer.innerHTML = `<div class="text-muted small p-2 text-center bg-white rounded border">No impact metrics yet. Click <strong>✨ AI 4 KPIs</strong> above to auto-generate verified KPIs.</div>`;
      return;
    }

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
        updateAuditScore();
      });
      row.querySelector(".metric-lbl").addEventListener("input", (e) => {
        metrics[idx].label = e.target.value;
        currentPortfolio.achievements = metrics;
        renderLivePreview();
        updateAuditScore();
      });
      row.querySelector(".btn-del-metric").addEventListener("click", () => {
        metrics.splice(idx, 1);
        currentPortfolio.achievements = metrics;
        renderMetricsEditor();
        renderLivePreview();
        updateAuditScore();
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
      projectsContainer.innerHTML = `
        <div class="text-muted small p-3 text-center bg-white rounded-3 border">
          <div class="mb-2">No projects added yet. Click below to add your first flagship project.</div>
          <button type="button" class="btn btn-sm btn-primary fw-semibold" id="btn-empty-add-project">+ Add Project</button>
        </div>
      `;
      const emptyAdd = document.getElementById("btn-empty-add-project");
      if (emptyAdd) {
        emptyAdd.addEventListener("click", () => {
          projects.push({
            name: "",
            description: "",
            key_features: [],
            technologies: [],
            live_demo_url: "",
            github_url: ""
          });
          currentPortfolio.projects = projects;
          renderProjectsEditor();
          renderLivePreview();
          updateAuditScore();
        });
      }
      return;
    }

    projects.forEach((p, idx) => {
      const card = document.createElement("div");
      card.className = "p-3 bg-white rounded-3 border shadow-sm mb-2";
      const kfText = Array.isArray(p.key_features) ? p.key_features.join("\n") : (p.key_features || "");
      card.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-2">
          <div class="d-flex align-items-center gap-1 flex-grow-1">
            <span class="badge bg-light text-dark border fw-bold" style="font-size: 0.72rem;">#${idx + 1}</span>
            <input type="text" class="form-control form-control-sm fw-bold proj-name" value="${p.name || ''}" placeholder="Project Title" />
          </div>
          <div class="d-flex align-items-center gap-1 ms-2">
            ${idx > 0 ? `<button type="button" class="btn btn-sm btn-outline-secondary py-0 px-1 btn-move-up" title="Move Up">▲</button>` : ''}
            ${idx < projects.length - 1 ? `<button type="button" class="btn btn-sm btn-outline-secondary py-0 px-1 btn-move-down" title="Move Down">▼</button>` : ''}
            <button type="button" class="btn btn-sm btn-outline-primary py-0 px-2 fw-semibold btn-enrich-case-study" title="Enrich to high-impact STAR case study with key features" style="font-size: 0.72rem;">
              ✨ AI Polish
            </button>
            <button type="button" class="btn btn-sm text-danger py-0 px-1 btn-del-proj" title="Delete Project">×</button>
          </div>
        </div>

        <div class="mb-2">
          <label class="form-label text-muted small mb-1" style="font-size: 0.72rem;">Architectural &amp; Problem Overview</label>
          <textarea rows="2" class="form-control form-control-sm proj-desc" placeholder="Describe the problem, architectural design, and impact...">${p.description || ''}</textarea>
        </div>

        <div class="mb-2">
          <label class="form-label text-muted small mb-1" style="font-size: 0.72rem;">Key Deliverables &amp; Engineering Highlights (one per line)</label>
          <textarea rows="2" class="form-control form-control-sm proj-kf" placeholder="• Architected modular REST endpoints&#10;• Reduced latency by 45% with Redis caching">${kfText}</textarea>
        </div>

        <div class="row g-2 mb-1">
          <div class="col-12">
            <input type="text" class="form-control form-control-sm proj-techs" value="${(p.technologies || []).join(', ')}" placeholder="Technologies (e.g. React, FastAPI, Docker, PostgreSQL)" />
          </div>
          <div class="col-6">
            <div class="input-group input-group-sm">
              <input type="url" class="form-control proj-live" value="${p.live_demo_url || ''}" placeholder="Live Demo URL" />
              ${p.live_demo_url ? `<a href="${p.live_demo_url}" target="_blank" class="btn btn-outline-secondary py-0 px-2 d-flex align-items-center" title="Test Live Link">↗</a>` : ''}
            </div>
          </div>
          <div class="col-6">
            <div class="input-group input-group-sm">
              <input type="url" class="form-control proj-gh" value="${p.github_url || ''}" placeholder="GitHub URL" />
              ${p.github_url ? `<a href="${p.github_url}" target="_blank" class="btn btn-outline-secondary py-0 px-2 d-flex align-items-center" title="Test GitHub Link">↗</a>` : ''}
            </div>
          </div>
        </div>
      `;

      card.querySelector(".proj-name").addEventListener("input", (e) => {
        projects[idx].name = e.target.value;
        currentPortfolio.projects = projects;
        renderLivePreview();
        updateAuditScore();
      });
      card.querySelector(".proj-desc").addEventListener("input", (e) => {
        projects[idx].description = e.target.value;
        currentPortfolio.projects = projects;
        renderLivePreview();
        updateAuditScore();
      });
      card.querySelector(".proj-kf").addEventListener("input", (e) => {
        projects[idx].key_features = e.target.value.split("\n").map(l => l.replace(/^[•\-\*]\s*/, '').trim()).filter(Boolean);
        currentPortfolio.projects = projects;
        renderLivePreview();
        updateAuditScore();
      });
      card.querySelector(".proj-techs").addEventListener("change", (e) => {
        projects[idx].technologies = e.target.value.split(",").map(t => t.trim()).filter(Boolean);
        currentPortfolio.projects = projects;
        renderLivePreview();
        updateAuditScore();
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

      // Move Up
      const btnUp = card.querySelector(".btn-move-up");
      if (btnUp) {
        btnUp.addEventListener("click", () => {
          const temp = projects[idx];
          projects[idx] = projects[idx - 1];
          projects[idx - 1] = temp;
          currentPortfolio.projects = projects;
          renderProjectsEditor();
          renderLivePreview();
        });
      }

      // Move Down
      const btnDown = card.querySelector(".btn-move-down");
      if (btnDown) {
        btnDown.addEventListener("click", () => {
          const temp = projects[idx];
          projects[idx] = projects[idx + 1];
          projects[idx + 1] = temp;
          currentPortfolio.projects = projects;
          renderProjectsEditor();
          renderLivePreview();
        });
      }

      // AI Case Study Polish
      const btnEnrich = card.querySelector(".btn-enrich-case-study");
      if (btnEnrich) {
        btnEnrich.addEventListener("click", async () => {
          btnEnrich.disabled = true;
          btnEnrich.innerHTML = `<span class="spinner-border spinner-border-sm" role="status"></span>`;
          try {
            const res = await portfolioAPI.improveProject(projects[idx]);
            if (res && res.data && res.data.improved_project) {
              const imp = res.data.improved_project;
              projects[idx].description = imp.description || projects[idx].description;
              if (imp.key_features) projects[idx].key_features = imp.key_features;
              currentPortfolio.projects = projects;
              renderProjectsEditor();
              renderLivePreview();
              updateAuditScore();
              showAlert("✨ Project case study polished with architectural highlights!", "success");
            }
          } catch (err) {
            showAlert("Could not enrich project.", "warning");
          } finally {
            btnEnrich.disabled = false;
            btnEnrich.innerHTML = "✨ AI Polish";
          }
        });
      }

      card.querySelector(".btn-del-proj").addEventListener("click", () => {
        projects.splice(idx, 1);
        currentPortfolio.projects = projects;
        renderProjectsEditor();
        renderLivePreview();
        updateAuditScore();
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
      servicesContainer.innerHTML = `<div class="text-muted small p-2 text-center bg-white rounded border">No value pillars yet. Click <strong>✨ AI Pillars</strong> above to highlight capability offerings.</div>`;
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
        updateAuditScore();
      });
      card.querySelector(".serv-title").addEventListener("input", (e) => {
        servList[idx].title = e.target.value;
        currentPortfolio.services = servList;
        renderLivePreview();
        updateAuditScore();
      });
      card.querySelector(".serv-desc").addEventListener("input", (e) => {
        servList[idx].description = e.target.value;
        currentPortfolio.services = servList;
        renderLivePreview();
        updateAuditScore();
      });
      card.querySelector(".btn-del-serv").addEventListener("click", () => {
        servList.splice(idx, 1);
        currentPortfolio.services = servList;
        renderServicesEditor();
        renderLivePreview();
        updateAuditScore();
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
          generation_prompt: (inputAiPrompt?.value || currentPortfolio.generation_prompt || "").trim(),
          profile_image: currentPortfolio.profile_image,
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
