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

  // Audio recording state
  let mediaRecorder = null;
  let audioChunks = [];
  let recordingTimerInterval = null;
  let recordingSeconds = 0;

  // DOM Elements
  const sidebarListContainer = document.getElementById("sidebar-list-container");
  const chatThreadContainer = document.getElementById("chat-thread-container");
  const chatTextInput = document.getElementById("chat-text-input");
  const chatSendBtn = document.getElementById("chat-send-submit-btn");
  const chatMessageForm = document.getElementById("chat-message-form");
  const micRecordBtn = document.getElementById("mic-record-btn");
  const audioRecordingBar = document.getElementById("audio-recording-bar");
  const recordingTimer = document.getElementById("recording-timer");
  const cancelRecordingBtn = document.getElementById("cancel-recording-btn");
  const sendAudioRecordingBtn = document.getElementById("send-audio-recording-btn");
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

    if (micRecordBtn) {
      micRecordBtn.addEventListener("click", startAudioRecording);
    }

    if (cancelRecordingBtn) {
      cancelRecordingBtn.addEventListener("click", cancelAudioRecording);
    }

    if (sendAudioRecordingBtn) {
      sendAudioRecordingBtn.addEventListener("click", sendAudioRecording);
    }

    const saveEditBtn = document.getElementById("save-edit-message-btn");
    if (saveEditBtn) {
      saveEditBtn.addEventListener("click", async () => {
        const msgId = document.getElementById("edit-message-id")?.value;
        const newText = document.getElementById("edit-message-text")?.value;
        if (!msgId) return;

        saveEditBtn.disabled = true;
        try {
          const res = await API.messages.update(msgId, newText);
          if (res && res.success) {
            const modalEl = document.getElementById("editMessageModal");
            const modalInst = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
            if (modalInst) modalInst.hide();
            await loadThread(activePartnerId, true);
            await refreshSidebarQuietly();
          } else {
            showChatError(res?.message || "Failed to update message");
          }
        } catch (err) {
          showChatError(err?.message || "Failed to update message");
        } finally {
          saveEditBtn.disabled = false;
        }
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

  function openEditModal(msgId, currentText) {
    const modalEl = document.getElementById("editMessageModal");
    const editMsgIdInput = document.getElementById("edit-message-id");
    const editMsgTextInput = document.getElementById("edit-message-text");

    if (!modalEl || !editMsgIdInput || !editMsgTextInput) return;
    editMsgIdInput.value = msgId;
    editMsgTextInput.value = currentText;

    const bsModal = new bootstrap.Modal(modalEl);
    bsModal.show();
  }

  async function startAudioRecording() {
    if (!activePartnerId) return;
    hideChatError();

    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      showChatError("Microphone recording is not supported in your browser.");
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioChunks = [];

      let options = {};
      if (typeof MediaRecorder.isTypeSupported === "function") {
        if (MediaRecorder.isTypeSupported("audio/webm;codecs=opus")) {
          options = { mimeType: "audio/webm;codecs=opus" };
        } else if (MediaRecorder.isTypeSupported("audio/webm")) {
          options = { mimeType: "audio/webm" };
        }
      }

      mediaRecorder = new MediaRecorder(stream, options);

      mediaRecorder.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) {
          audioChunks.push(e.data);
        }
      };

      // Collect audio data chunks every 250ms continuously to capture 100% of speech stream
      mediaRecorder.start(250);

      if (chatMessageForm) chatMessageForm.classList.add("d-none");
      if (audioRecordingBar) {
        audioRecordingBar.classList.remove("d-none");
        audioRecordingBar.classList.add("d-flex");
      }

      recordingSeconds = 0;
      updateTimerDisplay();
      clearInterval(recordingTimerInterval);
      recordingTimerInterval = setInterval(() => {
        recordingSeconds++;
        updateTimerDisplay();
      }, 1000);
    } catch (err) {
      console.error("Microphone access error:", err);
      showChatError("Microphone access denied or unavailable.");
    }
  }

  function updateTimerDisplay() {
    if (!recordingTimer) return;
    const mins = String(Math.floor(recordingSeconds / 60)).padStart(2, "0");
    const secs = String(recordingSeconds % 60).padStart(2, "0");
    recordingTimer.textContent = `${mins}:${secs}`;
  }

  function cancelAudioRecording() {
    clearInterval(recordingTimerInterval);
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
      mediaRecorder.onstop = () => {
        audioChunks = [];
      };
      mediaRecorder.stop();
      if (mediaRecorder.stream) {
        mediaRecorder.stream.getTracks().forEach(t => t.stop());
      }
    }
    if (audioRecordingBar) {
      audioRecordingBar.classList.add("d-none");
      audioRecordingBar.classList.remove("d-flex");
    }
    if (chatMessageForm) chatMessageForm.classList.remove("d-none");
  }

  async function sendAudioRecording() {
    clearInterval(recordingTimerInterval);
    if (!mediaRecorder || mediaRecorder.state === "inactive") return;

    if (sendAudioRecordingBtn) sendAudioRecordingBtn.disabled = true;

    mediaRecorder.onstop = async () => {
      try {
        if (mediaRecorder.stream) {
          mediaRecorder.stream.getTracks().forEach(t => t.stop());
        }

        const mimeType = mediaRecorder.mimeType || "audio/webm";
        const audioBlob = new Blob(audioChunks, { type: mimeType });
        if (audioBlob.size < 100) {
          showChatError("Audio recording was too short.");
          return;
        }

        const res = await API.messages.sendAudio(
          audioBlob,
          activePartnerId,
          activePartnerInfo?.application_id || null
        );

        if (res && res.success) {
          await loadThread(activePartnerId, true);
          await refreshSidebarQuietly();
          loadUnreadCount();
        } else {
          showChatError(res?.message || "Failed to send voice message");
        }
      } catch (err) {
        console.error("Audio upload error:", err);
        showChatError(err?.message || "Error uploading voice message. Please try again.");
      } finally {
        if (sendAudioRecordingBtn) sendAudioRecordingBtn.disabled = false;
        if (audioRecordingBar) {
          audioRecordingBar.classList.add("d-none");
          audioRecordingBar.classList.remove("d-flex");
        }
        if (chatMessageForm) chatMessageForm.classList.remove("d-none");
      }
    };

    if (mediaRecorder.state === "recording") {
      try {
        mediaRecorder.requestData();
      } catch (e) {}
      mediaRecorder.stop();
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
          if (micRecordBtn) micRecordBtn.disabled = true;
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
        const previewMsg = c.last_message_is_audio ? "🎙️ Voice Message" : (c.last_message || "");

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
                  <p class="mb-0 small text-muted text-truncate" style="max-width: 170px;">${escapeHtml(previewMsg)}</p>
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
      chatTextInput.placeholder = "Type a message or click 🎙️ to record audio...";
    }
    if (chatSendBtn) chatSendBtn.disabled = false;
    if (micRecordBtn) micRecordBtn.disabled = false;

    renderSidebar();
    await loadThread(partnerId, true);
  }

  let currentThreadSignature = "";

  async function loadThread(partnerId, scrollToBottom = false) {
    try {
      const res = await API.messages.getThread(partnerId);
      if (!res.success || !Array.isArray(res.data)) return;

      const messages = res.data;

      // Compute unique signature of current message thread state
      const newSignature = `${partnerId}:${messages.length}:${messages.map(m => m.id).join(",")}`;

      // Check if any audio element in the thread is currently playing or being listened to
      const isAudioActive = Array.from(chatThreadContainer.querySelectorAll("audio")).some(a => !a.paused || a.currentTime > 0);

      // If this is background polling and thread content hasn't changed or audio is playing, skip DOM re-render!
      if (!scrollToBottom && newSignature === currentThreadSignature) {
        return;
      }
      if (!scrollToBottom && isAudioActive) {
        return;
      }

      currentThreadSignature = newSignature;

      if (messages.length === 0) {
        chatThreadContainer.innerHTML = `
          <div class="h-100 d-flex align-items-center justify-content-center text-muted flex-column gap-2 my-auto">
            <span class="fs-1">👋</span>
            <h6 class="fw-bold mb-0">Start the conversation!</h6>
            <p class="small text-muted mb-0">Send a text or voice message to start chatting.</p>
          </div>`;
        return;
      }

      const isScrolledToBottom = chatThreadContainer.scrollHeight - chatThreadContainer.scrollTop <= chatThreadContainer.clientHeight + 100;

      chatThreadContainer.innerHTML = messages.map(msg => {
        const isSelf = msg.sender_id === currentUser.id;
        const isAudio = msg.is_audio || !!msg.audio_url;

        const bodyHtml = isAudio
          ? `
            <div class="d-flex align-items-center gap-2 mb-1 fw-semibold" style="font-size: 0.9rem;">
              <span>🎙️</span> Voice Message
            </div>
            <audio controls src="${escapeHtml(formatAudioUrl(msg.audio_url))}" preload="auto" class="w-100 mt-1 voice-audio-player" style="max-width: 270px; height: 38px; border-radius: 20px; outline: none;"></audio>
            ${msg.content && msg.content !== "🎙️ Voice Message" && msg.content !== "🎙️ Audio Message" ? `<div class="small mt-1 opacity-75 text-break">${escapeHtml(msg.content)}</div>` : ""}
          `
          : `<div class="text-break">${escapeHtml(msg.content)}</div>`;

        return `
          <div class="d-flex flex-column ${isSelf ? "align-items-end" : "align-items-start"} mb-2 msg-bubble-wrapper">
            <div class="p-3 shadow-sm rounded-4 position-relative ${isSelf ? "bg-primary text-white me-2" : "bg-body border text-body ms-2"}"
                 style="max-width: 78%; font-size: 0.95rem; border-bottom-${isSelf ? "right" : "left"}-radius: 4px !important;">
              ${bodyHtml}
              ${isSelf ? `
                <div class="d-flex align-items-center justify-content-end gap-2 mt-2 pt-1 border-top border-white-50" style="font-size: 0.76rem;">
                  ${!isAudio ? `
                    <button type="button" class="btn btn-link btn-sm p-0 text-white-50 hover-text-white text-decoration-none edit-msg-btn" data-msg-id="${msg.id}" data-msg-content="${escapeHtml(msg.content || '')}">✏️ Edit</button>
                    <span class="opacity-50">•</span>
                  ` : ''}
                  <button type="button" class="btn btn-link btn-sm p-0 text-white-50 hover-text-white text-decoration-none delete-msg-btn" data-msg-id="${msg.id}">🗑️ Delete</button>
                </div>
              ` : ''}
            </div>
            <small class="text-muted opacity-75 px-3 mt-1" style="font-size: 0.72rem;">
              ${formatTimeFull(msg.created_at)}
            </small>
          </div>
        `;
      }).join("");

      // Apply WebM duration fix to all rendered voice audio players
      chatThreadContainer.querySelectorAll(".voice-audio-player").forEach(audioEl => {
        fixWebmAudioDuration(audioEl);
      });

      // Attach Edit button listeners
      chatThreadContainer.querySelectorAll(".edit-msg-btn").forEach(btn => {
        btn.addEventListener("click", (e) => {
          e.stopPropagation();
          const msgId = btn.getAttribute("data-msg-id");
          const content = btn.getAttribute("data-msg-content") || "";
          openEditModal(msgId, content);
        });
      });

      // Attach Delete button listeners
      chatThreadContainer.querySelectorAll(".delete-msg-btn").forEach(btn => {
        btn.addEventListener("click", async (e) => {
          e.stopPropagation();
          const msgId = btn.getAttribute("data-msg-id");
          if (confirm("Are you sure you want to delete this message?")) {
            try {
              const res = await API.messages.delete(msgId);
              if (res && res.success) {
                await loadThread(activePartnerId, true);
                await refreshSidebarQuietly();
                loadUnreadCount();
              } else {
                showChatError(res?.message || "Failed to delete message");
              }
            } catch (err) {
              showChatError(err?.message || "Error deleting message");
            }
          }
        });
      });

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

  function formatAudioUrl(url) {
    if (!url) return "";
    if (url.startsWith("http://") || url.startsWith("https://") || url.startsWith("blob:")) {
      return url;
    }
    const origin = (typeof API_BASE_URL !== "undefined" ? API_BASE_URL : "http://localhost:8000/api/v1").replace(/\/api\/v1\/?$/, "");
    const cleanPath = url.startsWith("/") ? url : "/" + url;
    return origin + cleanPath;
  }

  function fixWebmAudioDuration(audioEl) {
    if (!audioEl) return;

    const applyFix = () => {
      try {
        if (audioEl.duration === Infinity || isNaN(audioEl.duration) || audioEl.duration <= 5) {
          audioEl.currentTime = 1e101;
          audioEl.ontimeupdate = function () {
            audioEl.ontimeupdate = null;
            audioEl.currentTime = 0;
          };
        }
      } catch (e) {}
    };

    if (audioEl.readyState >= 1) {
      applyFix();
    } else {
      audioEl.addEventListener("loadedmetadata", applyFix, { once: true });
    }
  }

  function formatTimeFull(dateStr) {
    if (!dateStr) return "";
    const d = new Date(dateStr);
    return `${d.toLocaleDateString([], { month: 'short', day: 'numeric' })} at ${d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
  }
})();
