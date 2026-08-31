/**
 * chat.js — Recruiter <-> Candidate Real-Time Messaging & Chat System
 */
(function () {
  if (!Session.isLoggedIn()) return;

  const currentUser = Session.getUser();
  if (!currentUser) return;

  let activePartnerId = null;
  let activePartnerInfo = null;
  let chatPollInterval = null;
  let unreadPollInterval = null;
  let conversationsCache = [];

  // Inject Chat Modal HTML into body if not present
  function injectChatUI() {
    if (document.getElementById("ar-chat-modal")) return;

    const modalHTML = `
      <!-- AI Recruiter Chat Modal -->
      <div class="modal fade" id="ar-chat-modal" tabindex="-1" aria-labelledby="arChatModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-xl modal-dialog-centered" style="max-width: 1000px;">
          <div class="modal-content border-0 shadow-lg" style="border-radius: 16px; overflow: hidden; height: 650px;">
            <div class="modal-header bg-dark text-white p-3 border-0">
              <div class="d-flex align-items-center gap-2">
                <span class="fs-4">💬</span>
                <div>
                  <h5 class="modal-title fw-bold mb-0" id="arChatModalLabel">Messages &amp; Chat</h5>
                  <span class="small opacity-75">Communicate directly between Candidates &amp; Recruiters</span>
                </div>
              </div>
              <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>

            <div class="modal-body p-0 d-flex h-100 overflow-hidden">
              <!-- Left Sidebar: Conversations & Contacts -->
              <div class="border-end bg-light d-flex flex-column" style="width: 320px; min-width: 320px;">
                <div class="p-3 border-bottom bg-white">
                  <div class="input-group input-group-sm mb-2">
                    <span class="input-group-text bg-light border-end-0">🔍</span>
                    <input type="text" id="chat-search-input" class="form-control bg-light border-start-0" placeholder="Search contacts or candidates..." />
                  </div>
                  <div class="btn-group w-100" role="group">
                    <button id="chat-tab-convos" class="btn btn-sm btn-outline-primary active fw-semibold">Conversations</button>
                    <button id="chat-tab-contacts" class="btn btn-sm btn-outline-secondary fw-semibold">Contacts</button>
                  </div>
                </div>

                <div id="chat-sidebar-list" class="flex-grow-1 overflow-auto p-2">
                  <div class="text-center text-muted p-4 small">Loading conversations...</div>
                </div>
              </div>

              <!-- Main Chat Window -->
              <div class="flex-grow-1 d-flex flex-column bg-white">
                <!-- Chat Window Header -->
                <div id="chat-header" class="p-3 border-bottom d-flex align-items-center justify-content-between bg-light">
                  <div class="d-flex align-items-center gap-3">
                    <div id="chat-header-avatar" class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center fw-bold" style="width: 42px; height: 42px;">?</div>
                    <div>
                      <h6 id="chat-header-name" class="fw-bold mb-0 text-dark">Select a Conversation</h6>
                      <div id="chat-header-sub" class="small text-muted">Choose a candidate or recruiter from the list</div>
                    </div>
                  </div>
                </div>

                <!-- Messages Thread Area -->
                <div id="chat-messages-container" class="flex-grow-1 p-3 overflow-auto bg-white" style="background-color: #f8fafc !important;">
                  <div class="h-100 d-flex align-items-center justify-content-center text-muted flex-column gap-2">
                    <span class="fs-1">💬</span>
                    <p class="mb-0 fw-medium">No conversation selected</p>
                    <span class="small text-muted">Select a candidate or recruiter to start messaging.</span>
                  </div>
                </div>

                <!-- Inline Chat Alert Container -->
                <div id="modal-chat-alert" class="px-3 pt-2 d-none">
                  <div class="alert alert-danger mb-0 py-2 small" id="modal-chat-alert-text"></div>
                </div>

                <!-- Message Input Footer -->
                <div class="p-3 border-top bg-white">
                  <form id="chat-send-form" class="d-flex gap-2" action="javascript:void(0);" onsubmit="event.preventDefault(); return false;">
                    <input type="text" id="chat-input-text" class="form-control" placeholder="Type your message here..." disabled autocomplete="off" />
                    <button type="submit" id="chat-send-btn" class="btn btn-primary fw-semibold px-4" disabled>Send</button>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Floating Floating Chat Trigger Button -->
      <button id="ar-floating-chat-btn" class="btn btn-primary shadow-lg rounded-circle d-flex align-items-center justify-content-center position-fixed" style="bottom: 24px; right: 24px; width: 56px; height: 56px; z-index: 1050; border: 2px solid #fff;" title="Open Messages">
        <span class="fs-4">💬</span>
        <span id="ar-chat-unread-badge" class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger d-none">0</span>
      </button>
    `;

    document.body.insertAdjacentHTML("beforeend", modalHTML);
  }

  // Load conversations list into sidebar
  async function loadConversations() {
    if (!Session.isLoggedIn()) return;
    const sidebar = document.getElementById("chat-sidebar-list");
    if (!sidebar) return;

    try {
      const res = await messagesAPI.getConversations();
      conversationsCache = res.data || [];
      if (!conversationsCache || conversationsCache.length === 0) {
        const tabContacts = document.getElementById("chat-tab-contacts");
        if (tabContacts && !activePartnerId) {
          tabContacts.click();
          return;
        }
      } else if (!activePartnerId && conversationsCache.length > 0) {
        const first = conversationsCache[0];
        window.openChatWithUser(first.other_user_id, first.other_user_name, first.other_user_role, first.company_or_headline);
        return;
      }
      renderSidebarConversations(conversationsCache);
    } catch (err) {
      if (err?.status === 401 || !Session.isLoggedIn()) {
        Session.clear();
        window.location.href = "login.html?expired=1";
        return;
      }
      sidebar.innerHTML = `
        <div class="text-center p-3 small">
          <div class="text-danger mb-2">Failed to load conversations: ${escapeHtml(err.message)}</div>
          <button id="retry-chat-convos-btn" class="btn btn-sm btn-outline-primary fw-semibold">🔄 Retry Connection</button>
        </div>`;
      document.getElementById("retry-chat-convos-btn")?.addEventListener("click", () => {
        sidebar.innerHTML = `<div class="text-center text-muted p-4 small"><div class="spinner-border spinner-border-sm text-primary mb-2"></div><div>Connecting...</div></div>`;
        loadConversations();
      });
    }
  }

  function renderSidebarConversations(list) {
    const sidebar = document.getElementById("chat-sidebar-list");
    if (!sidebar) return;

    if (!list || list.length === 0) {
      sidebar.innerHTML = `<div class="text-center text-muted p-4 small">No conversations yet.<br/>Switch to <strong>Contacts</strong> to start a chat!</div>`;
      return;
    }

    let html = "";
    list.forEach((c) => {
      const isSelected = activePartnerId === c.other_user_id;
      const dateStr = new Date(c.last_message_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
      const badgeHtml = c.unread_count > 0 ? `<span class="badge bg-danger rounded-pill">${c.unread_count}</span>` : "";
      const roleBadge = c.other_user_role === "candidate" ? `<span class="badge text-bg-info small">Candidate</span>` : `<span class="badge text-bg-primary small">Recruiter</span>`;

      html += `
        <div class="card mb-2 cursor-pointer border-0 shadow-sm ${isSelected ? "border-start border-primary border-4 bg-white shadow" : "bg-white"}" onclick="window.openChatWithUser('${c.other_user_id}', '${escapeHtml(c.other_user_name)}', '${c.other_user_role}', '${escapeHtml(c.company_or_headline || "")}')">
          <div class="card-body p-2.5">
            <div class="d-flex justify-content-between align-items-start mb-1">
              <div class="fw-bold text-dark text-truncate small me-1" style="max-width: 140px;">${escapeHtml(c.other_user_name)}</div>
              <span class="text-muted" style="font-size: 0.7rem;">${dateStr}</span>
            </div>
            <div class="d-flex justify-content-between align-items-center">
              <span class="text-muted text-truncate small" style="max-width: 170px;">${escapeHtml(c.last_message)}</span>
              ${badgeHtml}
            </div>
            <div class="mt-1 d-flex align-items-center justify-content-between">
              ${roleBadge}
              <span class="text-muted" style="font-size: 0.7rem;">${escapeHtml(c.company_or_headline || "")}</span>
            </div>
          </div>
        </div>
      `;
    });
    sidebar.innerHTML = html;
  }

  // Load contacts list into sidebar
  async function loadContacts() {
    if (!Session.isLoggedIn()) return;
    const sidebar = document.getElementById("chat-sidebar-list");
    if (!sidebar) return;

    sidebar.innerHTML = `<div class="text-center text-muted p-4 small">Loading contacts...</div>`;
    try {
      const res = await messagesAPI.getContacts();
      const contacts = res.data || [];
      if (contacts.length === 0) {
        sidebar.innerHTML = `<div class="text-center text-muted p-4 small">No available contacts found.</div>`;
        return;
      }

      if (!activePartnerId && contacts.length > 0) {
        const first = contacts[0];
        window.openChatWithUser(first.user_id, first.name, first.role, first.company_or_headline || first.email);
        return;
      }

      let html = "";
      contacts.forEach((c) => {
        const roleBadge = c.role === "candidate" ? `<span class="badge text-bg-info small">Candidate</span>` : `<span class="badge text-bg-primary small">Recruiter</span>`;
        const jobTag = c.job_title ? `<div class="text-primary small fw-semibold">For: ${escapeHtml(c.job_title)}</div>` : "";

        html += `
          <div class="card mb-2 cursor-pointer border-0 shadow-sm bg-white" onclick="window.openChatWithUser('${c.user_id}', '${escapeHtml(c.name)}', '${c.role}', '${escapeHtml(c.company_or_headline || "")}')">
            <div class="card-body p-2.5">
              <div class="d-flex justify-content-between align-items-center mb-1">
                <div class="fw-bold text-dark small">${escapeHtml(c.name)}</div>
                ${roleBadge}
              </div>
              ${jobTag}
              <div class="text-muted small">${escapeHtml(c.company_or_headline || c.email)}</div>
            </div>
          </div>
        `;
      });
      sidebar.innerHTML = html;
    } catch (err) {
      if (err?.status === 401 || !Session.isLoggedIn()) {
        Session.clear();
        window.location.href = "login.html?expired=1";
        return;
      }
      sidebar.innerHTML = `
        <div class="text-center p-3 small">
          <div class="text-danger mb-2">Failed to load contacts: ${escapeHtml(err.message)}</div>
          <button id="retry-chat-contacts-btn" class="btn btn-sm btn-outline-primary fw-semibold">🔄 Retry Connection</button>
        </div>`;
      document.getElementById("retry-chat-contacts-btn")?.addEventListener("click", () => {
        sidebar.innerHTML = `<div class="text-center text-muted p-4 small"><div class="spinner-border spinner-border-sm text-primary mb-2"></div><div>Connecting...</div></div>`;
        loadContacts();
      });
    }
  }

  function isValidUserId(id) {
    return id && id !== "undefined" && id !== "null" && String(id).trim() !== "";
  }

  // Load thread history for active user
  async function loadActiveThread() {
    if (!isValidUserId(activePartnerId)) return;

    const container = document.getElementById("chat-messages-container");
    if (!container) return;

    try {
      const res = await messagesAPI.getThread(activePartnerId);
      const messages = res.data || [];

      if (messages.length === 0) {
        container.innerHTML = `
          <div class="h-100 d-flex align-items-center justify-content-center text-muted flex-column gap-2">
            <span class="fs-1">👋</span>
            <p class="mb-0 fw-medium">No messages yet with ${escapeHtml(activePartnerInfo?.name || "this user")}</p>
            <span class="small text-muted">Send a message below to start the conversation!</span>
          </div>
        `;
        return;
      }

      let html = '<div class="d-flex flex-column gap-2">';
      messages.forEach((m) => {
        const isMine = m.sender_id === currentUser.id;
        const timeStr = new Date(m.created_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

        html += `
          <div class="d-flex ${isMine ? "justify-content-end" : "justify-content-start"}">
            <div class="p-3 shadow-sm ${isMine ? "bg-primary text-white rounded-3 rounded-bottom-0" : "bg-white text-dark border rounded-3 rounded-bottom-0"}" style="max-width: 75%; font-size: 0.92rem; border-radius: 16px;">
              <div class="mb-1">${escapeHtml(m.content)}</div>
              <div class="text-end opacity-75" style="font-size: 0.7rem;">${timeStr} ${isMine ? (m.is_read ? "✓✓" : "✓") : ""}</div>
            </div>
          </div>
        `;
      });
      html += "</div>";
      container.innerHTML = html;
      container.scrollTop = container.scrollHeight;
    } catch (err) {
      console.error("Load thread error:", err);
    }
  }

  // Global helper to open chat with specific recipient on full dedicated messages page
  window.openChatWithUser = function (userId, name, role, companyOrHeadline = "") {
    if (isValidUserId(userId)) {
      window.location.href = `messages.html?user_id=${encodeURIComponent(userId)}`;
    } else {
      window.location.href = "messages.html";
    }
  };

  // Poll for total unread messages count
  async function updateUnreadBadge() {
    if (!Session.isLoggedIn()) {
      if (unreadPollInterval) clearInterval(unreadPollInterval);
      return;
    }
    try {
      const res = await messagesAPI.getUnreadCount();
      const count = res.data?.unread_count || 0;
      const badge = document.getElementById("ar-chat-unread-badge");
      if (badge) {
        if (count > 0) {
          badge.textContent = count;
          badge.classList.remove("d-none");
        } else {
          badge.classList.add("d-none");
        }
      }
    } catch (e) {
      if (e?.status === 401 || !Session.isLoggedIn()) {
        if (unreadPollInterval) clearInterval(unreadPollInterval);
      }
    }
  }

  function escapeHtml(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // Initialize event listeners after DOM load
  function initChatEvents() {
    if (!Session.isLoggedIn()) return;
    injectChatUI();
    updateUnreadBadge();

    // Poll unread badge every 10s
    unreadPollInterval = setInterval(updateUnreadBadge, 10000);

    const floatBtn = document.getElementById("ar-floating-chat-btn");
    if (floatBtn) {
      floatBtn.addEventListener("click", () => {
        window.location.href = "messages.html";
      });
    }

    const tabConvos = document.getElementById("chat-tab-convos");
    const tabContacts = document.getElementById("chat-tab-contacts");
    if (tabConvos && tabContacts) {
      tabConvos.addEventListener("click", () => {
        tabConvos.classList.add("active", "btn-outline-primary");
        tabConvos.classList.remove("btn-outline-secondary");
        tabContacts.classList.remove("active", "btn-outline-primary");
        tabContacts.classList.add("btn-outline-secondary");
        loadConversations();
      });
      tabContacts.addEventListener("click", () => {
        tabContacts.classList.add("active", "btn-outline-primary");
        tabContacts.classList.remove("btn-outline-secondary");
        tabConvos.classList.remove("active", "btn-outline-primary");
        tabConvos.classList.add("btn-outline-secondary");
        loadContacts();
      });
    }

    // Sidebar search filter
    const searchInput = document.getElementById("chat-search-input");
    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        const q = e.target.value.toLowerCase().trim();
        if (!q) {
          renderSidebarConversations(conversationsCache);
          return;
        }
        const filtered = conversationsCache.filter(
          (c) =>
            c.other_user_name.toLowerCase().includes(q) ||
            (c.company_or_headline && c.company_or_headline.toLowerCase().includes(q)) ||
            (c.last_message && c.last_message.toLowerCase().includes(q))
        );
        renderSidebarConversations(filtered);
      });
    }

    function showModalChatError(msg) {
      const alertBox = document.getElementById("modal-chat-alert");
      const alertText = document.getElementById("modal-chat-alert-text");
      if (alertBox && alertText) {
        alertText.textContent = msg || "Failed to send message.";
        alertBox.classList.remove("d-none");
      }
    }

    function hideModalChatError() {
      const alertBox = document.getElementById("modal-chat-alert");
      if (alertBox) {
        alertBox.classList.add("d-none");
      }
    }

    // Form submit & send button handlers
    async function doSendMessage(e) {
      if (e) {
        e.preventDefault();
        if (typeof e.stopPropagation === "function") e.stopPropagation();
      }

      hideModalChatError();

      const inputText = document.getElementById("chat-input-text");
      const sendBtn = document.getElementById("chat-send-btn");
      const content = inputText ? inputText.value.trim() : "";

      if (!content || !isValidUserId(activePartnerId)) return false;

      if (inputText) inputText.disabled = true;
      if (sendBtn) sendBtn.disabled = true;

      try {
        const res = await messagesAPI.send({
          receiver_id: activePartnerId,
          content: content,
          application_id: activePartnerInfo?.application_id || null
        });
        if (res && res.success) {
          // Clear input ONLY on success!
          if (inputText) inputText.value = "";
          await loadActiveThread();
          await loadConversations();
        } else {
          showModalChatError(res?.message || "Failed to send message.");
        }
      } catch (err) {
        console.error("Modal send message error:", err);
        showModalChatError(err?.message || "Error sending message. Please try again.");
      } finally {
        if (isValidUserId(activePartnerId)) {
          if (inputText) {
            inputText.disabled = false;
            inputText.focus();
          }
          if (sendBtn) sendBtn.disabled = false;
        } else {
          if (inputText) inputText.disabled = true;
          if (sendBtn) sendBtn.disabled = true;
        }
      }
      return false;
    }

    const sendForm = document.getElementById("chat-send-form");
    if (sendForm) {
      sendForm.addEventListener("submit", doSendMessage);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initChatEvents);
  } else {
    initChatEvents();
  }
})();
