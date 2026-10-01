/**
 * mobile-nav.js — Universal Responsive Mobile Navigation & Sidebar Handler
 * Enhances all candidate and recruiter dashboard, portal, search, assessment,
 * and messages pages with smooth mobile sidebar drawer toggling, touch-scroll support,
 * and responsive layout adjustments.
 */
document.addEventListener("DOMContentLoaded", () => {
  initMobileSidebar();
  initResponsiveHeader();
  initResponsiveTables();
  initResponsiveMessages();
  initResponsiveModals();
  handleResize();
  window.addEventListener("resize", handleResize);
});

/**
 * Handle window resize — reset sidebar state when transitioning to desktop
 */
function handleResize() {
  if (window.innerWidth >= 768) {
    const sidebar = document.querySelector("nav.d-none.d-md-flex, nav#unified-messages-sidebar, nav[class*='sidebar']");
    const backdrop = document.querySelector(".mobile-sidebar-backdrop");
    if (sidebar) sidebar.classList.remove("mobile-sidebar-open");
    if (backdrop) backdrop.classList.remove("show");
    document.body.classList.remove("mobile-sidebar-active");
  }
}

/**
 * Initialize mobile sidebar drawer with backdrop, close button, and toggle
 */
function initMobileSidebar() {
  const sidebar = document.querySelector("nav.d-none.d-md-flex, nav#unified-messages-sidebar, nav[class*='sidebar']");
  if (!sidebar) return;

  // Create mobile backdrop if not existing
  let backdrop = document.querySelector(".mobile-sidebar-backdrop");
  if (!backdrop) {
    backdrop = document.createElement("div");
    backdrop.className = "mobile-sidebar-backdrop d-md-none";
    document.body.appendChild(backdrop);
  }

  // Add a close button inside the sidebar if missing
  if (!sidebar.querySelector(".mobile-sidebar-close")) {
    const closeBtn = document.createElement("button");
    closeBtn.type = "button";
    closeBtn.className = "btn-close d-md-none mobile-sidebar-close";
    closeBtn.setAttribute("aria-label", "Close navigation drawer");

    // Find existing brand element in sidebar
    const brand = sidebar.querySelector(".navbar-brand");
    if (brand) {
      // Make the brand row a flex container with close button
      brand.classList.add("d-flex", "align-items-center", "justify-content-between", "w-100");
      brand.style.position = "relative";
      closeBtn.style.marginLeft = "auto";
      brand.appendChild(closeBtn);
    } else {
      // Standalone drawer header
      const topHeader = document.createElement("div");
      topHeader.className = "d-flex align-items-center justify-content-between mb-3 pb-2 border-bottom d-md-none w-100";
      const menuLabel = document.createElement("span");
      menuLabel.className = "fw-bold fs-6 text-dark";
      menuLabel.textContent = "Navigation Menu";
      topHeader.appendChild(menuLabel);
      topHeader.appendChild(closeBtn);
      sidebar.insertBefore(topHeader, sidebar.firstChild);
    }

    closeBtn.addEventListener("click", closeMobileSidebar);
  }

  // Close sidebar when backdrop is clicked
  backdrop.addEventListener("click", closeMobileSidebar);

  // Close sidebar when any nav link inside sidebar is clicked on mobile
  sidebar.querySelectorAll(".nav-link, a[href]").forEach(link => {
    link.addEventListener("click", () => {
      if (window.innerWidth < 768) {
        setTimeout(closeMobileSidebar, 100);
      }
    });
  });

  // Close on Escape key
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && sidebar.classList.contains("mobile-sidebar-open")) {
      closeMobileSidebar();
    }
  });

  function closeMobileSidebar() {
    sidebar.classList.remove("mobile-sidebar-open");
    if (backdrop) backdrop.classList.remove("show");
    document.body.classList.remove("mobile-sidebar-active");
  }
}

/**
 * Add mobile hamburger menu toggle button to the header
 * Kept on ONE clean row with page title and action buttons
 */
function initResponsiveHeader() {
  const header = document.querySelector("main header, .flex-grow-1 > header, .interview-header, .top-header");
  const sidebar = document.querySelector("nav.d-none.d-md-flex, nav#unified-messages-sidebar, nav[class*='sidebar']");
  if (!header) return;

  // Add mobile layout class
  header.classList.add("mobile-header-bar");

  // Create mobile sidebar toggle button if missing
  if (sidebar && !header.querySelector(".mobile-sidebar-toggler")) {
    const toggleBtn = document.createElement("button");
    toggleBtn.type = "button";
    toggleBtn.className = "btn btn-sm btn-outline-secondary d-md-none mobile-sidebar-toggler d-inline-flex align-items-center gap-1 shadow-sm";
    toggleBtn.innerHTML = `<span style="font-size: 1.1rem; line-height: 1;">☰</span> <span class="fw-semibold d-none d-sm-inline">Menu</span>`;
    toggleBtn.setAttribute("aria-label", "Toggle navigation menu");
    toggleBtn.style.cssText = "border-radius: 8px; border-color: #cbd5e1; color: #334155; padding: 0.3rem 0.55rem; font-size: 0.8rem; flex-shrink: 0; background: #f8fafc;";

    // Check if header has a standalone heading or a left div container
    const firstDiv = header.querySelector(":scope > div");
    const heading = header.querySelector(":scope > h1, :scope > h2, :scope > h3, :scope > h4, :scope > h5");

    if (heading && (!firstDiv || heading.compareDocumentPosition(firstDiv) & Node.DOCUMENT_POSITION_FOLLOWING)) {
      // Heading is direct child before any div: wrap in a left container
      const leftContainer = document.createElement("div");
      leftContainer.className = "d-flex align-items-center gap-2 mobile-header-left";
      header.insertBefore(leftContainer, heading);
      leftContainer.appendChild(toggleBtn);
      leftContainer.appendChild(heading);
    } else if (firstDiv) {
      firstDiv.insertBefore(toggleBtn, firstDiv.firstChild);
      firstDiv.classList.add("mobile-header-left");
    } else {
      header.insertBefore(toggleBtn, header.firstChild);
    }

    // Mark the last div as right container
    const divs = header.querySelectorAll(":scope > div");
    if (divs.length > 1) {
      divs[divs.length - 1].classList.add("mobile-header-right");
    }

    toggleBtn.addEventListener("click", () => {
      const backdrop = document.querySelector(".mobile-sidebar-backdrop");
      sidebar.classList.toggle("mobile-sidebar-open");
      if (backdrop) backdrop.classList.toggle("show");
      document.body.classList.toggle("mobile-sidebar-active");
    });
  }
}

/**
 * Ensure all data tables are wrapped in .table-responsive for horizontal touch-scroll on mobile
 */
function initResponsiveTables() {
  document.querySelectorAll("table").forEach(table => {
    if (!table.parentElement.classList.contains("table-responsive")) {
      const wrapper = document.createElement("div");
      wrapper.className = "table-responsive w-100 mb-3";
      table.parentNode.insertBefore(wrapper, table);
      wrapper.appendChild(table);
    }
  });
}

/**
 * Responsive Messages Layout Switcher (Mobile Contacts vs Chat Pane)
 */
function initResponsiveMessages() {
  const sidebar = document.getElementById("messages-sidebar");
  const mainPane = document.getElementById("messages-main-pane");
  const backBtn = document.getElementById("back-to-sidebar-btn");

  if (!sidebar || !mainPane) return;

  function updateMessagesMobileView() {
    if (window.innerWidth < 768) {
      if (mainPane.classList.contains("active-chat")) {
        sidebar.style.display = "none";
        mainPane.style.display = "flex";
      } else {
        sidebar.style.display = "flex";
        mainPane.style.display = "none";
      }
    } else {
      sidebar.style.display = "";
      mainPane.style.display = "";
    }
  }

  if (backBtn) {
    backBtn.addEventListener("click", () => {
      mainPane.classList.remove("active-chat");
      updateMessagesMobileView();
    });
  }

  document.addEventListener("click", (e) => {
    if (e.target.closest(".partner-item, .contact-item, [data-partner-id]")) {
      mainPane.classList.add("active-chat");
      updateMessagesMobileView();
    }
  });

  window.addEventListener("resize", updateMessagesMobileView);
  updateMessagesMobileView();
}

/**
 * Ensure Bootstrap Modals auto-adjust max width on mobile screens
 */
function initResponsiveModals() {
  document.querySelectorAll(".modal-dialog").forEach(dialog => {
    dialog.classList.add("modal-dialog-centered");
  });
}
