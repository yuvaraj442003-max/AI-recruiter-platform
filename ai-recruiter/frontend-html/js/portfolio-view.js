/**
 * portfolio-view.js — Public Portfolio Viewer Controller.
 * Fetches published portfolio data by slug and renders with PortfolioThemesEngine.
 */

document.addEventListener("DOMContentLoaded", async () => {
  const loadingEl = document.getElementById("portfolio-loading-container");
  const errorEl = document.getElementById("portfolio-error-container");
  const errorMsgEl = document.getElementById("portfolio-error-message");
  const stageEl = document.getElementById("portfolio-public-stage");
  const floatingBar = document.getElementById("public-floating-bar");
  const btnCopy = document.getElementById("btn-floating-copy");

  // Determine slug from URL pathname or query param
  function extractSlug() {
    const urlParams = new URLSearchParams(window.location.search);
    const querySlug = urlParams.get("slug");
    if (querySlug) return querySlug.trim();

    // Check pathname: /portfolio/yuvaraj or /portfolio/yuvaraj/
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

    // Set page title
    document.title = `${data.candidate_name} — ${data.professional_headline || 'Professional Portfolio'}`;

    // Render using dynamic theme engine
    loadingEl.classList.add("d-none");
    stageEl.classList.remove("d-none");
    floatingBar.classList.remove("d-none");

    const isDark = Boolean(data.dark_mode || data.theme_id === "dark" || data.theme_id === "developer" || data.theme_id === "ai_tech");
    document.body.style.backgroundColor = isDark ? "#090d16" : "#f8fafc";
    document.body.setAttribute("data-bs-theme", isDark ? "dark" : "light");

    PortfolioThemesEngine.render(stageEl, data);

    // Floating copy link
    btnCopy.addEventListener("click", () => {
      navigator.clipboard.writeText(window.location.href).then(() => {
        btnCopy.innerHTML = "<span>✓ Link Copied!</span>";
        setTimeout(() => {
          btnCopy.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg><span>Share Portfolio</span>`;
        }, 2500);
      });
    });

  } catch (err) {
    console.error("Failed loading public portfolio:", err);
    loadingEl.classList.add("d-none");
    errorEl.classList.remove("d-none");
    errorMsgEl.textContent = err.message || "This portfolio is currently private or does not exist.";
  }
});
