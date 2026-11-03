/**
 * portfolio-view.js — Advanced Public Portfolio Viewer Controller.
 * Features:
 * - Dynamic Glassmorphic Navigation Dock with smooth section anchoring
 * - Reading scroll progress indicator (0% -> 100%)
 * - Live Dark / Light mode toggle
 * - Interactive Project Quick-View modal with full architecture & tech stack
 * - Interactive "Hire Me / Get in Touch" modal with 1-click email/phone copying
 * - Floating action dock with Back-to-Top and Link Share toast
 * - Executive Print / PDF export
 */

document.addEventListener("DOMContentLoaded", async () => {
  const loadingEl = document.getElementById("portfolio-loading-container");
  const errorEl = document.getElementById("portfolio-error-container");
  const errorMsgEl = document.getElementById("portfolio-error-message");
  const stageEl = document.getElementById("portfolio-public-stage");
  const topNavEl = document.getElementById("portfolio-top-navbar");
  const floatingBar = document.getElementById("public-floating-bar");
  const btnFloatingCopy = document.getElementById("btn-floating-copy");
  const btnFloatingTop = document.getElementById("btn-floating-top");
  const btnFloatingHire = document.getElementById("btn-floating-hire");
  const btnNavHireMe = document.getElementById("btn-nav-hire-me");
  const btnToggleTheme = document.getElementById("btn-toggle-portfolio-theme");
  const btnPrintPortfolio = document.getElementById("btn-print-portfolio");
  const progressBar = document.getElementById("portfolio-scroll-progress");

  // Global helper for smooth section scrolling
  window.scrollToPortfolioSection = function (sectionId) {
    const el = document.getElementById(sectionId);
    if (el) {
      const navHeight = topNavEl ? topNavEl.offsetHeight : 0;
      const elementPosition = el.getBoundingClientRect().top + window.pageYOffset;
      const offsetPosition = elementPosition - navHeight - 16;
      window.scrollTo({
        top: offsetPosition,
        behavior: "smooth"
      });
    }
  };

  // Toast notification trigger
  function showPortfolioToast(msg, icon = "✓") {
    const toast = document.getElementById("portfolio-toast");
    const toastMsg = document.getElementById("portfolio-toast-msg");
    const toastIcon = document.getElementById("portfolio-toast-icon");
    if (!toast) return;

    if (toastMsg) toastMsg.textContent = msg;
    if (toastIcon) toastIcon.textContent = icon;

    toast.style.opacity = "1";
    toast.style.transform = "translateY(0)";

    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transform = "translateY(100px)";
    }, 2800);
  }

  // Extract slug from URL pathname or query parameter
  function extractSlug() {
    const urlParams = new URLSearchParams(window.location.search);
    const querySlug = urlParams.get("slug");
    if (querySlug) return querySlug.trim();

    // Check pathname: /portfolio/username or /portfolio/username/
    const pathParts = window.location.pathname.split("/").filter(Boolean);
    const pIdx = pathParts.indexOf("portfolio");
    if (pIdx !== -1 && pathParts.length > pIdx + 1) {
      const part = pathParts[pIdx + 1];
      if (part && !part.endsWith(".html")) {
        return part.trim();
      }
    }
    return null;
  }

  const slug = extractSlug();

  if (!slug) {
    loadingEl.classList.add("d-none");
    errorEl.classList.remove("d-none");
    errorMsgEl.textContent = "No portfolio slug specified in URL.";
    return;
  }

  try {
    let data = null;
    const client = (typeof window !== "undefined" && window.portfolioAPI) || (typeof portfolioAPI !== "undefined" ? portfolioAPI : null);
    if (client && typeof client.getPublicPortfolio === "function") {
      const response = await client.getPublicPortfolio(slug);
      data = response?.data;
    } else {
      const res = await fetch(`/api/v1/portfolio/public/${encodeURIComponent(slug)}`);
      const payload = await res.json();
      data = payload?.data;
    }

    if (!data || !data.is_published) {
      throw new Error("Portfolio is private or unpublished.");
    }

    const candidateName = data.candidate_name || "Professional Portfolio";
    const professionalHeadline = data.professional_headline || data.candidate?.current_role || "Full Stack Technologist";

    // Set page title
    document.title = `${candidateName} — ${professionalHeadline}`;

    // Reveal UI stages
    loadingEl.classList.add("d-none");
    stageEl.classList.remove("d-none");
    if (topNavEl) topNavEl.classList.remove("d-none");
    if (floatingBar) floatingBar.classList.remove("d-none");

    // Theme initialization
    let isDarkMode = Boolean(data.dark_mode || data.theme_id === "dark" || data.theme_id === "developer" || data.theme_id === "ai_tech");
    function applyColorMode(dark) {
      isDarkMode = dark;
      document.body.setAttribute("data-bs-theme", isDarkMode ? "dark" : "light");
      document.body.style.backgroundColor = isDarkMode ? "#090d16" : "#f8fafc";
      document.body.style.color = isDarkMode ? "#f8fafc" : "#0f172a";

      const themeIcon = document.getElementById("theme-toggle-icon");
      const themeText = document.getElementById("theme-toggle-text");
      if (themeIcon) themeIcon.textContent = isDarkMode ? "☀️" : "🌙";
      if (themeText) themeText.textContent = isDarkMode ? "Light" : "Dark";
    }
    applyColorMode(isDarkMode);

    if (btnToggleTheme) {
      btnToggleTheme.addEventListener("click", () => {
        applyColorMode(!isDarkMode);
        showPortfolioToast(`Switched to ${isDarkMode ? 'Dark' : 'Light'} Mode`, isDarkMode ? '🌙' : '☀️');
      });
    }

    // Render using the theme engine
    PortfolioThemesEngine.render(stageEl, data);

    // Populate Top Navigation Bar Brand Details
    const navName = document.getElementById("nav-candidate-name");
    const navHeadline = document.getElementById("nav-candidate-headline");
    const navAvatar = document.getElementById("nav-brand-avatar");

    if (navName) navName.textContent = candidateName;
    if (navHeadline) navHeadline.textContent = professionalHeadline;
    if (navAvatar) {
      const initials = candidateName
        .split(" ")
        .filter(Boolean)
        .map(n => n[0].toUpperCase())
        .slice(0, 2)
        .join("") || "CV";
      navAvatar.textContent = initials;
    }

    // Hide navigation anchors if corresponding sections were disabled or empty
    const checkSection = (id, linkId) => {
      const sec = document.getElementById(id);
      const link = document.getElementById(linkId);
      if (link) {
        if (!sec) link.classList.add("d-none");
        else link.classList.remove("d-none");
      }
    };
    checkSection("section-about", "nav-link-about");
    checkSection("section-skills", "nav-link-skills");
    checkSection("section-experience", "nav-link-experience");
    checkSection("section-projects", "nav-link-projects");
    checkSection("section-education", "nav-link-education");
    checkSection("section-contact", "nav-link-contact");

    // Scroll reading progress & Back to Top logic
    window.addEventListener("scroll", () => {
      const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
      if (totalHeight > 0) {
        const progress = Math.min(100, Math.max(0, (window.scrollY / totalHeight) * 100));
        if (progressBar) progressBar.style.width = `${progress}%`;
      }

      if (btnFloatingTop) {
        if (window.scrollY > 280) {
          btnFloatingTop.classList.remove("d-none");
        } else {
          btnFloatingTop.classList.add("d-none");
        }
      }
    });

    if (btnFloatingTop) {
      btnFloatingTop.addEventListener("click", () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
      });
    }

    // Print / PDF Export
    if (btnPrintPortfolio) {
      btnPrintPortfolio.addEventListener("click", () => {
        window.print();
      });
    }

    // Hire Me / Get in Touch Modal Setup
    const contactEmail = data.social_links?.email || data.candidate?.resume_email || data.candidate?.user?.email || "";
    const contactPhone = data.social_links?.phone || data.candidate?.phone || "";
    const contactLocation = data.social_links?.location || data.candidate?.location || "Remote / Worldwide";

    function setupHireMeModal() {
      const emailEl = document.getElementById("hire-email-text");
      const phoneEl = document.getElementById("hire-phone-text");
      const locEl = document.getElementById("hire-location-text");
      const phoneCard = document.getElementById("hire-phone-card");
      const linkEmail = document.getElementById("link-direct-email");
      const linkPhone = document.getElementById("link-direct-phone");

      if (emailEl) emailEl.textContent = contactEmail || "Available on inquiry";
      if (linkEmail) linkEmail.href = contactEmail ? `mailto:${contactEmail}?subject=Interview%20Inquiry%20from%20Portfolio` : "#";

      if (contactPhone) {
        if (phoneEl) phoneEl.textContent = contactPhone;
        if (linkPhone) linkPhone.href = `tel:${contactPhone.replace(/\s+/g, '')}`;
        if (phoneCard) phoneCard.classList.remove("d-none");
      } else if (phoneCard) {
        phoneCard.classList.add("d-none");
      }

      if (locEl) locEl.textContent = contactLocation;

      // Copy email button
      const btnCopyEmail = document.getElementById("btn-copy-hire-email");
      if (btnCopyEmail && contactEmail) {
        btnCopyEmail.addEventListener("click", () => {
          navigator.clipboard.writeText(contactEmail).then(() => {
            showPortfolioToast("Email Copied to Clipboard!");
          });
        });
      }

      // Copy phone button
      const btnCopyPhone = document.getElementById("btn-copy-hire-phone");
      if (btnCopyPhone && contactPhone) {
        btnCopyPhone.addEventListener("click", () => {
          navigator.clipboard.writeText(contactPhone).then(() => {
            showPortfolioToast("Phone Number Copied to Clipboard!");
          });
        });
      }

      // Note composer trigger
      const btnSendNote = document.getElementById("btn-send-recruiter-note");
      if (btnSendNote && contactEmail) {
        btnSendNote.addEventListener("click", () => {
          const subj = document.getElementById("hire-note-subject")?.value?.trim() || "Opportunity Inquiry";
          const body = document.getElementById("hire-note-body")?.value?.trim() || "Hi, I viewed your portfolio and would like to connect!";
          window.location.href = `mailto:${encodeURIComponent(contactEmail)}?subject=${encodeURIComponent(subj)}&body=${encodeURIComponent(body)}`;
        });
      }
    }
    setupHireMeModal();

    function openHireModal() {
      const modalEl = document.getElementById("hireMeModal");
      if (window.bootstrap && modalEl) {
        const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
        modal.show();
      }
    }

    if (btnNavHireMe) btnNavHireMe.addEventListener("click", openHireModal);
    if (btnFloatingHire) btnFloatingHire.addEventListener("click", openHireModal);

    // Interactive Project Detail Modal Binding
    function setupProjectModalBinding() {
      const projects = Array.isArray(data.projects) ? data.projects : [];
      if (!projects.length) return;

      const projectCards = stageEl.querySelectorAll(".project-card-item, .portfolio-project-card, [data-project-idx]");
      projectCards.forEach((card, idx) => {
        card.style.cursor = "pointer";
        card.setAttribute("title", "Click to explore project architecture & details");
        
        card.addEventListener("click", (e) => {
          // Do not hijack direct outgoing links if clicked directly
          if (e.target.tagName === "A" && e.target.getAttribute("href") && !e.target.getAttribute("href").startsWith("#")) {
            return;
          }

          const proj = projects[idx] || projects[0];
          if (!proj) return;

          const titleEl = document.getElementById("proj-modal-title");
          const descEl = document.getElementById("proj-modal-desc");
          const techList = document.getElementById("proj-modal-tech-list");
          const highlightsList = document.getElementById("proj-modal-highlights");
          const demoLink = document.getElementById("proj-modal-demo-link");
          const codeLink = document.getElementById("proj-modal-code-link");

          if (titleEl) titleEl.textContent = proj.title || "Featured Project";
          if (descEl) descEl.textContent = proj.description || "Production-grade project demonstrating core competencies, modular design, and robust implementation.";

          // Tech badges
          if (techList) {
            const techs = Array.isArray(proj.technologies) ? proj.technologies : (typeof proj.technologies === "string" ? proj.technologies.split(",") : []);
            if (techs.length > 0) {
              techList.innerHTML = techs.map(t => `<span class="badge bg-primary-subtle text-primary border rounded-pill px-2.5 py-1 small">${t.trim()}</span>`).join("");
            } else {
              techList.innerHTML = `<span class="badge bg-light text-secondary border rounded-pill px-2.5 py-1 small">Modern Full-Stack</span>`;
            }
          }

          // Highlights
          if (highlightsList) {
            const hls = Array.isArray(proj.highlights) ? proj.highlights : (proj.description ? [proj.description.slice(0, 120)] : []);
            if (hls.length > 0) {
              highlightsList.innerHTML = hls.map(h => `<li class="mb-1">${h}</li>`).join("");
            } else {
              highlightsList.innerHTML = `
                <li>Clean, modular, and maintainable architecture.</li>
                <li>Designed for scalable performance and seamless user experience.</li>
              `;
            }
          }

          // Links
          if (demoLink) {
            if (proj.link && proj.link !== "#") {
              demoLink.href = proj.link;
              demoLink.classList.remove("d-none");
            } else {
              demoLink.classList.add("d-none");
            }
          }

          if (codeLink) {
            if (proj.github_url && proj.github_url !== "#") {
              codeLink.href = proj.github_url;
              codeLink.classList.remove("d-none");
            } else {
              codeLink.classList.add("d-none");
            }
          }

          const modalEl = document.getElementById("projectDetailModal");
          if (window.bootstrap && modalEl) {
            const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
            modal.show();
          }
        });
      });
    }
    setupProjectModalBinding();

    // Floating Copy & Share Link
    if (btnFloatingCopy) {
      btnFloatingCopy.addEventListener("click", () => {
        navigator.clipboard.writeText(window.location.href).then(() => {
          showPortfolioToast("Portfolio Link Copied to Clipboard!");
        });
      });
    }

  } catch (err) {
    console.error("Failed loading public portfolio:", err);
    loadingEl.classList.add("d-none");
    errorEl.classList.remove("d-none");
    errorMsgEl.textContent = err.message || "This portfolio is currently private or does not exist.";
  }
});
