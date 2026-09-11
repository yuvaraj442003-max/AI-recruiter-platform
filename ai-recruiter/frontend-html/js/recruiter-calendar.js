(function () {
  let allJobs = [];

  async function loadUpcomingInterviews() {
    const container = document.getElementById("upcoming-interviews-container");
    if (!container || !window.scheduledInterviewsAPI) return;

    try {
      const res = await scheduledInterviewsAPI.getUpcoming();
      if (res.success && res.data.length > 0) {
        container.innerHTML = `
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="bg-light text-secondary small">
                <tr>
                  <th>Candidate</th>
                  <th>Job Title</th>
                  <th>Date &amp; Time</th>
                  <th>Calendar Sync</th>
                  <th>Status</th>
                  <th class="text-end">Actions</th>
                </tr>
              </thead>
              <tbody>
                ${res.data.map(item => {
                  const dt = new Date(item.start_time_utc);
                  const dateStr = dt.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
                  const timeStr = dt.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' });
                  return `
                    <tr>
                      <td class="fw-semibold text-dark">${item.candidate_name}</td>
                      <td>${item.job_title}</td>
                      <td>
                        <div class="fw-medium">${dateStr}</div>
                        <div class="small text-muted">${timeStr} (${item.timezone || 'UTC'})</div>
                      </td>
                      <td>
                        <span class="badge bg-${item.calendar_sync_status === 'synced' ? 'success' : 'secondary'}">
                          ${item.calendar_sync_status}
                        </span>
                      </td>
                      <td>
                        <span class="badge bg-${item.status === 'SCHEDULED' ? 'primary' : item.status === 'RESCHEDULED' ? 'info' : 'danger'}">
                          ${item.status}
                        </span>
                      </td>
                      <td class="text-end">
                        <div class="btn-group btn-group-sm">
                          <a href="${item.join_link}" class="btn btn-outline-primary fw-semibold" target="_blank">Join Room</a>
                          <button class="btn btn-outline-info btn-reschedule-btn" data-id="${item.interview_id || item.id}">Reschedule</button>
                          <button class="btn btn-outline-secondary btn-reminder-btn" data-id="${item.interview_id || item.id}">Reminder</button>
                          <button class="btn btn-outline-danger btn-cancel-btn" data-id="${item.interview_id || item.id}">Cancel</button>
                        </div>
                      </td>
                    </tr>
                  `;
                }).join('')}
              </tbody>
            </table>
          </div>
        `;

        // Attach event listeners
        container.querySelectorAll(".btn-reminder-btn").forEach(btn => {
          btn.addEventListener("click", async () => {
            const id = btn.dataset.id;
            btn.disabled = true;
            try {
              await scheduledInterviewsAPI.sendReminder(id);
              alert("Reminder sent to candidate!");
            } catch (e) {
              alert(e.message);
            } finally {
              btn.disabled = false;
            }
          });
        });

        container.querySelectorAll(".btn-reschedule-btn").forEach(btn => {
          btn.addEventListener("click", () => {
            const id = btn.dataset.id;
            document.getElementById("resched-interview-id").value = id;
            const tomorrow = new Date();
            tomorrow.setDate(tomorrow.getDate() + 1);
            tomorrow.setHours(11, 0, 0, 0);
            document.getElementById("resched-datetime").value = tomorrow.toISOString().slice(0, 16);
            const modalEl = document.getElementById("rescheduleModal");
            if (window.bootstrap && modalEl) {
              const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
              modal.show();
            }
          });
        });

        container.querySelectorAll(".btn-cancel-btn").forEach(btn => {
          btn.addEventListener("click", () => {
            const id = btn.dataset.id;
            document.getElementById("cancel-interview-id").value = id;
            const modalEl = document.getElementById("cancelModal");
            if (window.bootstrap && modalEl) {
              const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
              modal.show();
            }
          });
        });
      } else {
        container.innerHTML = '<div class="text-muted small text-center py-4">No upcoming interviews scheduled yet. Click "+ Schedule New Interview" to create one.</div>';
      }
    } catch (err) {
      container.innerHTML = `<div class="text-danger small text-center py-3">${err.message}</div>`;
    }
  }

  async function loadJobsDropdown() {
    try {
      const res = await jobsAPI.list();
      allJobs = res.data || [];
      const select = document.getElementById("sched-job-select");
      if (select) {
        select.innerHTML = '<option value="">Select Job Position...</option>' +
          allJobs.map(j => `<option value="${j.id}">${j.title} (${j.location || 'Remote'})</option>`).join('');
        
        select.addEventListener("change", () => loadApplicantsDropdown());
      }

      const urlParams = new URLSearchParams(window.location.search);
      const paramJobId = urlParams.get("job_id");
      const paramCandId = urlParams.get("candidate_id");

      if (paramJobId && select) {
        select.value = paramJobId;
        await loadApplicantsDropdown(paramCandId);
      }
      if ((paramJobId || paramCandId) && window.bootstrap) {
        const modalEl = document.getElementById("scheduleInterviewModal");
        if (modalEl) {
          const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
          modal.show();
        }
      }
    } catch (e) {
      console.warn("Error loading jobs for calendar:", e);
    }
  }

  async function loadApplicantsDropdown(preselectCandId = null) {
    const jobId = document.getElementById("sched-job-select").value;
    const candSelect = document.getElementById("sched-candidate-select");
    if (!jobId || !candSelect) return;

    candSelect.innerHTML = '<option value="">Loading applicants...</option>';
    try {
      const res = await jobsAPI.applications(jobId);
      const apps = res.data || [];
      if (apps.length > 0) {
        candSelect.innerHTML = '<option value="">Select Candidate...</option>' +
          apps.map(a => `<option value="${a.candidate_id}">${a.candidate_name || 'Candidate'} (${a.status})</option>`).join('');
        if (preselectCandId) {
          candSelect.value = preselectCandId;
        }
      } else {
        candSelect.innerHTML = '<option value="">No applicants found for this job position.</option>';
      }
    } catch (e) {
      candSelect.innerHTML = `<option value="">Error: ${e.message}</option>`;
    }
  }

  async function loadCalendarStatusQuick() {
    const el = document.getElementById("quick-calendar-status");
    if (!el || !window.calendarAPI) return;
    try {
      const res = await calendarAPI.getStatus();
      if (res.data) {
        const g = res.data.google;
        const o = res.data.outlook;
        let html = '';
        html += `<div>Google: ${g.connected ? '🟢 Connected' : '⚪ Not Connected'}</div>`;
        html += `<div>Outlook: ${o.connected ? '🟢 Connected' : '⚪ Not Connected'}</div>`;
        el.innerHTML = html;
      }
    } catch (e) {
      el.textContent = "Status unavailable";
    }
  }

  const form = document.getElementById("form-schedule-interview");
  if (form) {
    // Default to tomorrow 10:00 AM in datetime-local picker
    const dtPicker = document.getElementById("sched-datetime");
    if (dtPicker) {
      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);
      tomorrow.setHours(10, 0, 0, 0);
      dtPicker.value = tomorrow.toISOString().slice(0, 16);
    }

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = document.getElementById("btn-submit-schedule");
      btn.disabled = true;
      btn.textContent = "Scheduling...";

      const dtVal = document.getElementById("sched-datetime").value;
      const isoStr = new Date(dtVal).toISOString();

      const payload = {
        job_id: document.getElementById("sched-job-select").value,
        candidate_id: document.getElementById("sched-candidate-select").value,
        start_time_iso: isoStr,
        duration_minutes: parseInt(document.getElementById("sched-duration").value) || 30,
        timezone_name: document.getElementById("sched-timezone").value || "Asia/Kolkata",
        interview_type: "AI Technical Interview",
        send_email: document.getElementById("chk-sched-email").checked,
        sync_calendar: document.getElementById("chk-sched-cal").checked,
      };

      try {
        await scheduledInterviewsAPI.schedule(payload);
        alert("Interview scheduled successfully!");
        const modalEl = document.getElementById("scheduleInterviewModal");
        if (window.bootstrap && modalEl) {
          const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
          modal.hide();
        }
        loadUpcomingInterviews();
      } catch (err) {
        alert(err.message);
      } finally {
        btn.disabled = false;
        btn.textContent = "Schedule Interview";
      }
    });
  }

  const reschedForm = document.getElementById("form-reschedule-interview");
  if (reschedForm) {
    reschedForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const interviewId = document.getElementById("resched-interview-id").value;
      const btn = document.getElementById("btn-submit-reschedule");
      btn.disabled = true;
      btn.textContent = "Rescheduling...";

      const dtVal = document.getElementById("resched-datetime").value;
      const isoStr = new Date(dtVal).toISOString();

      const payload = {
        new_start_time_iso: isoStr,
        duration_minutes: parseInt(document.getElementById("resched-duration").value) || 30,
        timezone_name: document.getElementById("resched-timezone").value || "Asia/Kolkata",
        reason: document.getElementById("resched-reason").value || "Recruiter rescheduled",
        send_email: true,
      };

      try {
        await scheduledInterviewsAPI.reschedule(interviewId, payload);
        alert("Interview rescheduled successfully!");
        const modalEl = document.getElementById("rescheduleModal");
        if (window.bootstrap && modalEl) {
          const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
          modal.hide();
        }
        loadUpcomingInterviews();
      } catch (err) {
        alert(err.message);
      } finally {
        btn.disabled = false;
        btn.textContent = "Confirm Reschedule";
      }
    });
  }

  const cancelForm = document.getElementById("form-cancel-interview");
  if (cancelForm) {
    cancelForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const interviewId = document.getElementById("cancel-interview-id").value;
      const btn = document.getElementById("btn-submit-cancel");
      btn.disabled = true;
      btn.textContent = "Cancelling...";

      const reason = document.getElementById("cancel-reason-select").value || "Cancelled by recruiter";

      try {
        await scheduledInterviewsAPI.cancel(interviewId, { reason });
        alert("Interview cancelled.");
        const modalEl = document.getElementById("cancelModal");
        if (window.bootstrap && modalEl) {
          const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
          modal.hide();
        }
        loadUpcomingInterviews();
      } catch (err) {
        alert(err.message);
      } finally {
        btn.disabled = false;
        btn.textContent = "Confirm Cancel";
      }
    });
  }

  loadUpcomingInterviews();
  loadJobsDropdown();
  loadCalendarStatusQuick();
})();
