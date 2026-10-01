/**
 * mobile-nav.js — Universal Responsive Mobile Navigation & Sidebar Handler
 * Enhances all dashboard, portal, search, assessment, and messages pages
 * with smooth mobile sidebar drawer toggling, touch-scroll support,
 * and responsive layout adjustments.
 */
document.addEventListener("DOMContentLoaded", () => {
  initMobileSidebar();
  initResponsiveTables();
  initResponsiveMessages();
  initResponsiveModals();
});

function initMobileSidebar() {
  const sidebar = document.querySelector("nav.d-none.d-md-flex, nav#unified-messages-sidebar, nav[class*='sidebar']");
  if (!sidebar) return;

  // Find header to inject mobile toggle if not already present
  const header = document.querySelector("main header, .flex-grow-1 > header, .interview-header, .top-header");
  
  // Create mobile backdrop if not existing
  let backdrop = document.querySelector(".mobile-sidebar-backdrop");
  if (!backdrop) {
    backdrop = document.createElement("div");
    backdrop.className = "mobile-sidebar-backdrop d-md-none";
    document.body.appendChild(backdrop);
  }

  // Create mobile sidebar toggle button if header exists and button missing
  if (header && !header.querySelector(".mobile-sidebar-toggler")) {
    const toggleBtn = document.createElement("button");
    toggleBtn.type = "button";
    toggleBtn.className = "btn btn-sm btn-outline-secondary d-md-none me-2 mobile-sidebar-toggler d-inline-flex align-items-center gap-1";
    toggleBtn.innerHTML = `<span>☰</span> <span class="fw-semibold">Menu</span>`;
    toggleBtn.setAttribute("aria-label", "Toggle navigation menu");

    // Insert toggle button at start of header's first flex child or header itself
    const targetContainer = header.querySelector(".d-flex") || header;
    targetContainer.insertBefore(toggleBtn, targetContainer.firstChild);

    toggleBtn.addEventListener("click", () => {
      sidebar.classList.toggle("mobile-sidebar-open");
      backdrop.classList.toggle("show");
      document.body.classList.toggle("mobile-sidebar-active");
    });
  }

  // Close sidebar when backdrop is clicked
  backdrop.addEventListener("click", closeMobileSidebar);

  // Close sidebar when any nav link inside sidebar is clicked on mobile
  sidebar.querySelectorAll(".nav-link, a").forEach(link => {
    link.addEventListener("click", () => {
      if (window.innerWidth < 768) {
        closeMobileSidebar();
      }
    });
  });

  function closeMobileSidebar() {
    sidebar.classList.remove("mobile-sidebar-open");
    backdrop.classList.remove("show");
    document.body.classList.remove("mobile-sidebar-active");
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

  // Delegate partner item click to switch to chat pane on mobile
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
