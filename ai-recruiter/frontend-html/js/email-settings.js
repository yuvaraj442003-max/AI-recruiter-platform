(function () {
  async function loadCalendarStatus() {
    try {
      const res = await calendarAPI.getStatus();
      if (res.success && res.data) {
        const g = res.data.google;
        const o = res.data.outlook;

        // Google UI
        const gText = document.getElementById("google-status-text");
        const gBtn = document.getElementById("google-btn-container");
        if (g.connected) {
          gText.innerHTML = `<span class="badge bg-success">Connected ✓</span> <small class="text-muted ms-1">${g.account_email || ''}</small>`;
          gBtn.innerHTML = `<button class="btn btn-sm btn-outline-danger" id="btn-disc-google">Disconnect</button>`;
          document.getElementById("btn-disc-google")?.addEventListener("click", () => disconnect("google"));
        } else {
          gText.textContent = "Not connected";
          gBtn.innerHTML = `<button class="btn btn-sm btn-primary fw-bold" id="btn-conn-google">Connect Google</button>`;
          document.getElementById("btn-conn-google")?.addEventListener("click", connectGoogle);
        }

        // Outlook UI
        const oText = document.getElementById("outlook-status-text");
        const oBtn = document.getElementById("outlook-btn-container");
        if (o.connected) {
          oText.innerHTML = `<span class="badge bg-success">Connected ✓</span> <small class="text-muted ms-1">${o.account_email || ''}</small>`;
          oBtn.innerHTML = `<button class="btn btn-sm btn-outline-danger" id="btn-disc-outlook">Disconnect</button>`;
          document.getElementById("btn-disc-outlook")?.addEventListener("click", () => disconnect("outlook"));
        } else {
          oText.textContent = "Not connected";
          oBtn.innerHTML = `<button class="btn btn-sm btn-outline-primary fw-bold" id="btn-conn-outlook">Connect Outlook</button>`;
          document.getElementById("btn-conn-outlook")?.addEventListener("click", connectOutlook);
        }
      }
    } catch (e) {
      console.warn("Calendar status error:", e);
    }
  }

  async function connectGoogle() {
    try {
      const res = await calendarAPI.getGoogleAuthUrl();
      if (res.data?.auth_url) {
        window.location.href = res.data.auth_url;
      }
    } catch (e) {
      alert(e.message);
    }
  }

  async function connectOutlook() {
    try {
      const res = await calendarAPI.getOutlookAuthUrl();
      if (res.data?.auth_url) {
        window.location.href = res.data.auth_url;
      }
    } catch (e) {
      alert(e.message);
    }
  }

  async function disconnect(provider) {
    if (!confirm(`Are you sure you want to disconnect ${provider}?`)) return;
    try {
      await calendarAPI.disconnect(provider);
      loadCalendarStatus();
    } catch (e) {
      alert(e.message);
    }
  }

  async function loadEmailSettings() {
    try {
      const res = await emailSettingsAPI.getSettings();
      if (res.success && res.data) {
        const d = res.data;
        document.getElementById("chk-app-received").checked = d.app_received;
        document.getElementById("chk-shortlisted").checked = d.candidate_shortlisted;
        document.getElementById("chk-interview-invited").checked = d.interview_invited;
        document.getElementById("chk-interview-reminder").checked = d.interview_reminder;
        document.getElementById("chk-interview-rescheduled").checked = d.interview_rescheduled;
        document.getElementById("chk-interview-cancelled").checked = d.interview_cancelled;
        document.getElementById("chk-candidate-rejected").checked = d.candidate_rejected;
      }
    } catch (e) {
      console.warn("Email settings error:", e);
    }
  }

  const form = document.getElementById("email-settings-form");
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const saveBtn = document.getElementById("btn-save-settings");
      saveBtn.disabled = true;
      saveBtn.textContent = "Saving...";

      const payload = {
        app_received: document.getElementById("chk-app-received").checked,
        candidate_shortlisted: document.getElementById("chk-shortlisted").checked,
        interview_invited: document.getElementById("chk-interview-invited").checked,
        interview_reminder: document.getElementById("chk-interview-reminder").checked,
        interview_rescheduled: document.getElementById("chk-interview-rescheduled").checked,
        interview_cancelled: document.getElementById("chk-interview-cancelled").checked,
        candidate_rejected: document.getElementById("chk-candidate-rejected").checked,
      };

      try {
        await emailSettingsAPI.updateSettings(payload);
        alert("Email notification preferences saved!");
      } catch (err) {
        alert(err.message);
      } finally {
        saveBtn.disabled = false;
        saveBtn.textContent = "Save Preferences";
      }
    });
  }

  loadCalendarStatus();
  loadEmailSettings();
})();
