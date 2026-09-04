/**
 * messages.js — Standalone Messaging & Chat Interface Script
 */
(function () {
  if (!Session.isLoggedIn()) return;

  const currentUser = Session.getUser();
  if (!currentUser) return;

  let activeTab = "conversations"; // 'conversations' or 'contacts'
  let activePartnerId = null;
  let activePartnerInfo = null;
  let conversationsCache = [];
  let contactsCache = [];
  let pollInterval = null;

  // DOM Elements
  const sidebarListContainer = document.getElementById("sidebar-list-container");
  const chatThreadContainer = document.getElementById("chat-thread-container");
  const chatTextInput = document.getElementById("chat-text-input");
  const chatSendBtn = document.getElementById("chat-send-submit-btn");
  const chatMessageForm = document.getElementById("chat-message-form");
  const searchInput = document.getElementById("contact-search-input");
  const tabConvosBtn = document.getElementById("tab-btn-conversations");
  const tabContactsBtn = document.getElementById("tab-btn-contacts");
  const activeAvatar = document.getElementById("active-partner-avatar");
  const activeName = document.getElementById("active-partner-name");
  const activeSub = document.getElementById("active-partner-sub");
  const totalUnreadBadge = document.getElementById("total-unread-counter");
  const navUnreadBadge = document.getElementById("nav-unread-badge");
  const userDisplayName = document.getElementById("user-display-name");
  const logoutBtn = document.getElementById("logout-btn");
  const navDashLink = document.getElementById("nav-dashboard-link");
  const navProfileLink = document.getElementById("nav-profile-link");

  document.addEventListener("DOMContentLoaded", () => {
    initNavigation();
    bindEvents();
    loadUnreadCount();

    // Check URL parameters for direct partner target e.g. ?user_id=...
    const urlParams = new URLSearchParams(window.location.search);
    const targetUserId = urlParams.get("user_id");

    loadSidebarData().then(() => {
      if (targetUserId) {
        selectPartner(targetUserId);
      }
    });

    // Start auto polling for current conversation & unread count
    pollInterval = setInterval(() => {
      loadUnreadCount();
      if (activePartnerId) {
        loadThread(activePartnerId, false);
      }
      refreshSidebarQuietly();
    }, 3000);
  });

  function initNavigation() {
    if (userDisplayName) userDisplayName.textContent = currentUser.name || currentUser.email;

    const role = (currentUser.role || "candidate").toLowerCase();
    const isRecruiterRole = ["recruiter", "admin", "superadmin", "company_admin"].includes(role);

    const portalHome = document.getElementById("nav-portal-home");
    const portalDash = document.getElementById("nav-portal-dash");

    if (portalHome) {
      portalHome.href = isRecruiterRole ? "recruiter-portal.html" : "candidate-portal.html";
    }
    if (portalDash) {
      portalDash.href = isRecruiterRole ? "recruiter-dashboard.html" : "candidate-dashboard.html";
    }

    const handleLogout = () => {
      Session.clear();
      window.location.href = "login.html";
    };

    if (logoutBtn) logoutBtn.addEventListener("click", handleLogout);
  }

  function showChatError(msg) {
    const alertBox = document.getElementById("chat-alert-container");
    const alertText = document.getElementById("chat-alert-text");
    if (alertBox && alertText) {
      alertText.textContent = msg || "Error sending message. Please try again.";
      alertBox.classList.remove("d-none");
    }
  }

  function hideChatError() {
    const alertBox = document.getElementById("chat-alert-container");
    if (alertBox) {
      alertBox.classList.add("d-none");
    }
  }

  function bindEvents() {
    if (tabConvosBtn) {
      tabConvosBtn.addEventListener("click", () => {
        activeTab = "conversations";
        tabConvosBtn.className = "btn btn-sm btn-primary fw-semibold active";
        tabContactsBtn.className = "btn btn-sm btn-outline-secondary fw-semibold";
        renderSidebar();
      });
    }

    if (tabContactsBtn) {
      tabContactsBtn.addEventListener("click", () => {
        activeTab = "contacts";
        tabContactsBtn.className = "btn btn-sm btn-primary fw-semibold active";
        tabConvosBtn.className = "btn btn-sm btn-outline-secondary fw-semibold";
        renderSidebar();
      });
    }

    if (searchInput) {
      searchInput.addEventListener("input", () => {
        renderSidebar();
      });
    }

    if (chatMessageForm) {
      chatMessageForm.addEventListener("submit", (e) => {
        if (e) {
          e.preventDefault();
          if (typeof e.stopPropagation === "function") e.stopPropagation();
        }
        sendMessage();
        return false;
      });
    }

    const backBtn = document.getElementById("back-to-sidebar-btn");
    if (backBtn) {
      backBtn.addEventListener("click", () => {
        const sidebar = document.getElementById("messages-sidebar");
        const mainPane = document.getElementById("messages-main-pane");
        if (sidebar && mainPane) {
          sidebar.classList.remove("d-none");
          mainPane.classList.add("d-none", "d-md-flex");
        }
      });
    }
  }

  async function loadUnreadCount() {
    try {
      const res = await API.messages.getUnreadCount();
      if (res.success && res.data) {
        const count = res.data.unread_count || 0;
        if (navUnreadBadge) {
          navUnreadBadge.textContent = count;
          navUnreadBadge.classList.toggle("d-none", count === 0);
        }
        if (totalUnreadBadge) {
          totalUnreadBadge.textContent = `${count} unread`;
          totalUnreadBadge.classList.toggle("d-none", count === 0);
        }
      }
    } catch (e) {
      console.warn("Unread count fetch error:", e);
    }
  }

  async function loadSidebarData() {
    try {
      const [convosRes, contactsRes] = await Promise.all([
        API.messages.getConversations().catch(() => ({ success: false, data: [] })),
        API.messages.getContacts().catch(() => ({ success: false, data: [] }))
      ]);

      if (convosRes.success && Array.isArray(convosRes.data)) {
        conversationsCache = convosRes.data;
      }
      if (contactsRes.success && Array.isArray(contactsRes.data)) {
        contactsCache = contactsRes.data;
      }

      // Auto-select top conversation or contact if no partner selected yet
      if (!activePartnerId) {
        if (conversationsCache.length > 0) {
          selectPartner(conversationsCache[0].other_user_id);
        } else if (contactsCache.length > 0) {
          activeTab = "contacts";
          if (tabContactsBtn) tabContactsBtn.className = "btn btn-sm btn-primary fw-semibold active";
          if (tabConvosBtn) tabConvosBtn.className = "btn btn-sm btn-outline-secondary fw-semibold";
          selectPartner(contactsCache[0].user_id);
        } else {
          if (chatTextInput) {
            chatTextInput.disabled = true;
            chatTextInput.placeholder = "Select a contact or candidate from the sidebar...";
          }
          if (chatSendBtn) chatSendBtn.disabled = true;
        }
      }

      renderSidebar();
    } catch (err) {
      console.error("Error loading sidebar data:", err);
      if (err?.status === 401 || !Session.isLoggedIn()) {
        Session.clear();
        window.location.href = "login.html?expired=1";
        return;
      }
      sidebarListContainer.innerHTML = `
        <div class="p-3 text-center small">
          <div class="text-danger mb-2">Failed to load contacts: ${escapeHtml(err.message)}</div>
          <button id="retry-messages-sidebar-btn" class="btn btn-sm btn-outline-primary fw-semibold">🔄 Retry Connection</button>
        </div>`;
      document.getElementById("retry-messages-sidebar-btn")?.addEventListener("click", () => {
        sidebarListContainer.innerHTML = `<div class="text-center text-muted p-4 small"><div class="spinner-border spinner-border-sm text-primary mb-2"></div><div>Connecting...</div></div>`;
        loadSidebarData();
      });
    }
  }

  async function refreshSidebarQuietly() {
    try {
      const [convosRes, contactsRes] = await Promise.all([
        API.messages.getConversations().catch(() => null),
        API.messages.getContacts().catch(() => null)
      ]);
      if (convosRes && convosRes.success && Array.isArray(convosRes.data)) {
        conversationsCache = convosRes.data;
      }
      if (contactsRes && contactsRes.success && Array.isArray(contactsRes.data)) {
        contactsCache = contactsRes.data;
      }
      renderSidebar();
    } catch (e) {}
  }

  function renderSidebar() {
    if (!sidebarListContainer) return;
    const term = (searchInput?.value || "").toLowerCase().trim();

    if (activeTab === "conversations") {
      let list = conversationsCache.filter(c =>
        (c.other_user_name || "").toLowerCase().includes(term) ||
        (c.company_or_headline || "").toLowerCase().includes(term) ||
        (c.last_message || "").toLowerCase().includes(term)
      );

      if (list.length === 0) {
        sidebarListContainer.innerHTML = `
          <div class="text-center text-muted p-4 small">
            <div>No active conversations found.</div>
            <button id="switch-to-contacts-link" class="btn btn-link btn-sm text-decoration-none mt-1">Browse all contacts</button>
          </div>`;
        document.getElementById("switch-to-contacts-link")?.addEventListener("click", () => {
          tabContactsBtn?.click();
        });
        return;
      }

      sidebarListContainer.innerHTML = list.map(c => {
        const isSelected = activePartnerId === c.other_user_id;
        const initial = (c.other_user_name || "U")[0].toUpperCase();
        const unreadBadge = c.unread_count > 0 ? `<span class="badge bg-danger rounded-pill">${c.unread_count}</span>` : "";

        return `
          <div class="card border-0 mb-1 rounded-3 sidebar-contact-item cursor-pointer ${isSelected ? "bg-primary-subtle text-primary border-start border-4 border-primary" : "bg-body hover-bg-light"}"
               data-user-id="${c.other_user_id}">
            <div class="card-body p-2.5 d-flex align-items-center gap-2">
              <div class="rounded-circle bg-secondary text-white fw-bold d-flex align-items-center justify-content-center flex-shrink-0" style="width: 40px; height: 40px;">
                ${initial}
              </div>
              <div class="flex-grow-1 min-w-0">
                <div class="d-flex align-items-center justify-content-between">
                  <h6 class="mb-0 text-truncate fw-semibold ${isSelected ? "text-primary" : "text-body"}" style="font-size: 0.92rem;">${escapeHtml(c.other_user_name)}</h6>
                  <small class="text-muted opacity-75" style="font-size: 0.75rem;">${formatTimeShort(c.last_message_at)}</small>
                </div>
                <div class="d-flex align-items-center justify-content-between mt-1">
                  <p class="mb-0 small text-muted text-truncate" style="max-width: 170px;">${escapeHtml(c.last_message || "")}</p>
                  ${unreadBadge}
                </div>
              </div>
            </div>
          </div>
        `;
      }).join("");
    } else {
      // Contacts tab
      let list = contactsCache.filter(c =>
        (c.name || "").toLowerCase().includes(term) ||
        (c.company_or_headline || "").toLowerCase().includes(term) ||
        (c.job_title || "").toLowerCase().includes(term)
      );

      if (list.length === 0) {
        sidebarListContainer.innerHTML = `<div class="text-center text-muted p-4 small">No contacts found matching search.</div>`;
        return;
      }

      sidebarListContainer.innerHTML = list.map(c => {
        const isSelected = activePartnerId === c.user_id;
        const initial = (c.name || "U")[0].toUpperCase();
        const subtitle = c.job_title ? `${c.job_title} • ${c.company_or_headline}` : (c.company_or_headline || c.role);

        return `
          <div class="card border-0 mb-1 rounded-3 sidebar-contact-item cursor-pointer ${isSelected ? "bg-primary-subtle border-start border-4 border-primary" : "bg-body hover-bg-light"}"
               data-user-id="${c.user_id}">
            <div class="card-body p-2.5 d-flex align-items-center gap-2">
              <div class="rounded-circle bg-primary text-white fw-bold d-flex align-items-center justify-content-center flex-shrink-0" style="width: 40px; height: 40px;">
                ${initial}
              </div>
              <div class="flex-grow-1 min-w-0">
                <h6 class="mb-0 text-truncate fw-semibold text-body" style="font-size: 0.92rem;">${escapeHtml(c.name)}</h6>
                <small class="text-muted text-truncate d-block" style="font-size: 0.78rem;">${escapeHtml(subtitle)}</small>
              </div>
            </div>
          </div>
        `;
      }).join("");
    }

    // Attach click listeners to sidebar cards
    sidebarListContainer.querySelectorAll(".sidebar-contact-item").forEach(item => {
      item.addEventListener("click", () => {
        const userId = item.getAttribute("data-user-id");
        selectPartner(userId);
      });
    });
  }

  async function selectPartner(partnerId) {
    if (!partnerId) return;
    activePartnerId = partnerId;
    hideChatError();

    // Responsive toggle for mobile view
    const sidebar = document.getElementById("messages-sidebar");
    const mainPane = document.getElementById("messages-main-pane");
    if (window.innerWidth < 768 && sidebar && mainPane) {
      sidebar.classList.add("d-none");
      mainPane.classList.remove("d-none");
      mainPane.classList.add("d-flex");
    }

    // Update active partner info header
    let partnerObj = conversationsCache.find(c => c.other_user_id === partnerId) ||
                     contactsCache.find(c => c.user_id === partnerId);

    activePartnerInfo = partnerObj || { name: "User", company_or_headline: "" };

    const nameStr = activePartnerInfo.other_user_name || activePartnerInfo.name || "User";
    const subStr = activePartnerInfo.company_or_headline || activePartnerInfo.job_title || (activePartnerInfo.other_user_role === "candidate" ? "Candidate" : "Recruiter");

    if (activeAvatar) activeAvatar.textContent = (nameStr[0] || "U").toUpperCase();
    if (activeName) activeName.textContent = nameStr;
    if (activeSub) activeSub.textContent = subStr;

    if (chatTextInput) {
      chatTextInput.disabled = false;
      chatTextInput.placeholder = "Type your message...";
    }
    if (chatSendBtn) chatSendBtn.disabled = false;

    renderSidebar();
    await loadThread(partnerId, true);
  }

  async function loadThread(partnerId, scrollToBottom = false) {
    try {
      const res = await API.messages.getThread(partnerId);
      if (!res.success || !Array.isArray(res.data)) return;

      const messages = res.data;
      if (messages.length === 0) {
        chatThreadContainer.innerHTML = `
          <div class="h-100 d-flex align-items-center justify-content-center text-muted flex-column gap-2 my-auto">
            <span class="fs-1">👋</span>
            <h6 class="fw-bold mb-0">Start the conversation!</h6>
            <p class="small text-muted mb-0">Send a greeting message to start chatting.</p>
          </div>`;
        return;
      }

      const isScrolledToBottom = chatThreadContainer.scrollHeight - chatThreadContainer.scrollTop <= chatThreadContainer.clientHeight + 100;

      chatThreadContainer.innerHTML = messages.map(msg => {
        const isSelf = msg.sender_id === currentUser.id;
        return `
          <div class="d-flex flex-column ${isSelf ? "align-items-end" : "align-items-start"} mb-2">
            <div class="p-3 shadow-sm rounded-4 ${isSelf ? "bg-primary text-white me-2" : "bg-body border text-body ms-2"}"
                 style="max-width: 75%; font-size: 0.95rem; border-bottom-${isSelf ? "right" : "left"}-radius: 4px !important;">
              <div class="text-break">${escapeHtml(msg.content)}</div>
            </div>
            <small class="text-muted opacity-75 px-3 mt-1" style="font-size: 0.72rem;">
              ${formatTimeFull(msg.created_at)}
            </small>
          </div>
        `;
      }).join("");

      if (scrollToBottom || isScrolledToBottom) {
        requestAnimationFrame(() => {
          chatThreadContainer.scrollTop = chatThreadContainer.scrollHeight;
        });
      }
    } catch (err) {
      console.error("Error loading chat thread:", err);
    }
  }

  async function sendMessage() {
    if (!activePartnerId || !chatTextInput) return;
    const text = chatTextInput.value.trim();
    if (!text) return;

    hideChatError();

    // Disable input while sending
    chatTextInput.disabled = true;
    if (chatSendBtn) chatSendBtn.disabled = true;

    try {
      const res = await messagesAPI.send({
        receiver_id: activePartnerId,
        content: text,
        application_id: activePartnerInfo?.application_id || null
      });

      if (res && res.success) {
        // Clear input ONLY on success!
        chatTextInput.value = "";
        await loadThread(activePartnerId, true);
        await refreshSidebarQuietly();
        loadUnreadCount();
      } else {
        showChatError(res?.message || "Failed to send message");
      }
    } catch (err) {
      console.error("Failed to send message:", err);
      showChatError(err?.message || "Error sending message. Please try again.");
    } finally {
      if (chatTextInput) {
        chatTextInput.disabled = false;
        chatTextInput.focus();
      }
      if (chatSendBtn) {
        chatSendBtn.disabled = false;
      }
    }
  }

  function escapeHtml(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function formatTimeShort(dateStr) {
    if (!dateStr) return "";
    const d = new Date(dateStr);
    const now = new Date();
    if (d.toDateString() === now.toDateString()) {
      return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    return d.toLocaleDateString([], { month: 'short', day: 'numeric' });
  }

  function formatTimeFull(dateStr) {
    if (!dateStr) return "";
    const d = new Date(dateStr);
    return `${d.toLocaleDateString([], { month: 'short', day: 'numeric' })} at ${d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
  }
})();
