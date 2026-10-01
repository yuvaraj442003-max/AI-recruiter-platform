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
});

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

  // Ensure sidebar has a mobile close button inside if missing
  if (!sidebar.querySelector(".mobile-sidebar-close")) {
    const closeBtn = document.createElement("button");
    closeBtn.type = "button";
    closeBtn.className = "btn-close d-md-none mobile-sidebar-close p-2 border rounded-circle bg-light ms-auto";
    closeBtn.setAttribute("aria-label", "Close navigation drawer");
    
    // Insert at top of sidebar
    const firstChild = sidebar.firstElementChild;
    if (firstChild) {
      if (firstChild.classList.contains("navbar-brand") || firstChild.classList.contains("d-flex")) {
        firstChild.classList.add("justify-content-between");
        firstChild.appendChild(closeBtn);
      } else {
        const topHeader = document.createElement("div");
        topHeader.className = "d-flex align-items-center justify-content-between mb-3 pb-2 border-bottom d-md-none";
        topHeader.innerHTML = `<span class="fw-bold fs-6 text-dark">Menu Navigation</span>`;
        topHeader.appendChild(closeBtn);
        sidebar.insertBefore(topHeader, firstChild);
      }
    }
    
    closeBtn.addEventListener("click", closeMobileSidebar);
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
    if (backdrop) backdrop.classList.remove("show");
    document.body.classList.remove("mobile-sidebar-active");
  }
}

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
    toggleBtn.className = "btn btn-sm btn-outline-secondary d-md-none mobile-sidebar-toggler me-2 flex-shrink-0 d-inline-flex align-items-center gap-1 shadow-sm";
    toggleBtn.innerHTML = `<span>☰</span> <span class="fw-semibold">Menu</span>`;
    toggleBtn.setAttribute("aria-label", "Toggle navigation menu");

    // Insert toggle button at top left of header
    header.insertBefore(toggleBtn, header.firstChild);

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
