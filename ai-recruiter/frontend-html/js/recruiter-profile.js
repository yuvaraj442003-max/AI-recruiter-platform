/**
 * recruiter-profile.js — loads and manages recruiter & company profile.
 */
(function () {
  const profileAlert = document.getElementById("profile-alert");
  const editForm = document.getElementById("edit-profile-form");
  const modalEl = document.getElementById("editProfileModal");
  let modalInstance = null;

  function showAlert(msg, type = "success") {
    profileAlert.textContent = msg;
    profileAlert.className = `alert alert-${type} py-2 mb-4`;
    profileAlert.classList.remove("d-none");
    setTimeout(() => profileAlert.classList.add("d-none"), 4000);
  }

  async function loadProfile() {
    try {
      const res = await API.get("/recruiter-profile");
      const p = res.data;
      if (!p) return;

      const isComplete = Boolean(p.company_name && p.company_name.trim());

      const user = Session.getUser();
      if (user) {
        user.is_profile_complete = isComplete;
        if (typeof safeStorage !== "undefined") {
          safeStorage.setItem("ar_user", JSON.stringify(user));
        } else {
          try { localStorage.setItem("ar_user", JSON.stringify(user)); } catch (e) {}
        }
      }

      const urlParams = new URLSearchParams(window.location.search);
      const headerAlert = document.getElementById("profile-alert");
      if (headerAlert) {
        if (!isComplete || urlParams.get("onboarding") === "required") {
          headerAlert.className = "alert alert-warning py-3 mb-4 shadow-sm border-warning";
          headerAlert.innerHTML = `
            <h6 class="fw-bold mb-1">⚠️ Mandatory Company &amp; Recruiter Onboarding</h6>
            <p class="small mb-0">Please fill out and save your official company name, website, and recruiter details below. Access to the Recruiter Dashboard and Job Posting will be unlocked once completed and verified.</p>
          `;
          headerAlert.classList.remove("d-none");
        } else {
          headerAlert.classList.add("d-none");
        }
      }

      document.getElementById("recruiter-name-display").textContent = p.recruiter_name || "Recruiter";
      document.getElementById("job-title-display").textContent = p.job_title || "Recruiter / Talent Acquisition";
      document.getElementById("company-name-badge").textContent = p.company_name ? `🏢 ${p.company_name}` : "🏢 Company Name Not Set";

      document.getElementById("location-display").textContent = p.location ? `📍 ${p.location}` : "📍 Location Not Set";
      document.getElementById("company-description-display").textContent = p.company_description || "No company description provided yet. Click 'Edit Profile' to add information about your organization.";
      
      document.getElementById("industry-display").textContent = p.industry || "—";
      document.getElementById("company-size-display").textContent = p.company_size || "—";
      document.getElementById("company-location-display").textContent = p.location || "—";
      
      const webEl = document.getElementById("website-display");
      if (p.website) {
        webEl.innerHTML = `<a href="${p.website}" target="_blank" class="text-success text-decoration-none">${p.website}</a>`;
      } else {
        webEl.textContent = "—";
      }

      if (p.profile_photo) {
        document.getElementById("profile-photo-img").src = p.profile_photo;
      } else {
        const name = encodeURIComponent(p.recruiter_name || "Recruiter");
        document.getElementById("profile-photo-img").src = `https://ui-avatars.com/api/?name=${name}&background=11998e&color=fff&size=128`;
      }

      // Social Links
      const btnLinkedin = document.getElementById("btn-linkedin");
      if (p.linkedin_url) {
        btnLinkedin.href = p.linkedin_url;
        btnLinkedin.classList.remove("d-none");
      } else {
        btnLinkedin.classList.add("d-none");
      }

      const btnGithub = document.getElementById("btn-github");
      if (p.github_url) {
        btnGithub.href = p.github_url;
        btnGithub.classList.remove("d-none");
      } else {
        btnGithub.classList.add("d-none");
      }

      const btnWeb = document.getElementById("btn-website");
      if (p.website) {
        btnWeb.href = p.website;
        btnWeb.classList.remove("d-none");
      } else {
        btnWeb.classList.add("d-none");
      }

      // Populate Edit Form Inputs
      document.getElementById("edit-job-title").value = p.job_title || "";
      document.getElementById("edit-profile-photo").value = p.profile_photo || "";
      document.getElementById("edit-company-name").value = p.company_name || "";
      document.getElementById("edit-company-logo").value = p.company_logo || "";
      document.getElementById("edit-company-desc").value = p.company_description || "";
      document.getElementById("edit-industry").value = p.industry || "";
      document.getElementById("edit-company-size").value = p.company_size || "";
      document.getElementById("edit-location").value = p.location || "";
      document.getElementById("edit-website").value = p.website || "";
      document.getElementById("edit-linkedin").value = p.linkedin_url || "";
      document.getElementById("edit-github").value = p.github_url || "";
      document.getElementById("edit-other-links").value = p.other_links || "";

      loadActiveJobs(p.user_id);
    } catch (e) {
      showAlert(e.message, "danger");
    }
  }

  async function loadActiveJobs(userId) {
    const container = document.getElementById("active-jobs-container");
    try {
      const res = await jobsAPI.list();
      const userJobs = res.data.filter(j => j.recruiter_id === userId);
      if (!userJobs.length) {
        container.innerHTML = `<div class="p-3 bg-light rounded text-muted small">No active job postings yet. <a href="post-job.html" class="text-success">Post a job</a></div>`;
        return;
      }

      container.innerHTML = userJobs.map(j => `
        <div class="card p-3 border-0 shadow-sm mb-2" style="border-radius: 12px; background: #f8fafc;">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h6 class="fw-bold mb-1 text-dark">${j.title}</h6>
              <div class="text-muted small">📍 ${j.location || 'Remote'} • ${j.employment_type.replace('_', ' ')}</div>
            </div>
            <div>
              <a href="job-applicants.html?job_id=${j.id}" class="btn btn-sm btn-outline-success fw-semibold">View Applicants &rarr;</a>
            </div>
          </div>
        </div>
      `).join("");
    } catch (err) {
      container.innerHTML = `<div class="text-danger small">${err.message}</div>`;
    }
  }

  editForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const saveBtn = document.getElementById("save-profile-btn");
    saveBtn.disabled = true;
    saveBtn.textContent = "Saving...";

    const payload = {
      job_title: document.getElementById("edit-job-title").value.trim() || null,
      profile_photo: document.getElementById("edit-profile-photo").value.trim() || null,
      company_name: document.getElementById("edit-company-name").value.trim() || null,
      company_logo: document.getElementById("edit-company-logo").value.trim() || null,
      company_description: document.getElementById("edit-company-desc").value.trim() || null,
      industry: document.getElementById("edit-industry").value.trim() || null,
      company_size: document.getElementById("edit-company-size").value || null,
      location: document.getElementById("edit-location").value.trim() || null,
      website: document.getElementById("edit-website").value.trim() || null,
      linkedin_url: document.getElementById("edit-linkedin").value.trim() || null,
      github_url: document.getElementById("edit-github").value.trim() || null,
      other_links: document.getElementById("edit-other-links").value.trim() || null,
    };

    try {
      await API.put("/recruiter-profile", payload);
      const user = Session.getUser();
      if (user && payload.company_name && payload.company_name.trim()) {

        user.is_profile_complete = true;
        if (typeof safeStorage !== "undefined") {
          safeStorage.setItem("ar_user", JSON.stringify(user));
        } else {
          try { localStorage.setItem("ar_user", JSON.stringify(user)); } catch (e) {}
        }
      }
      showAlert("Recruiter & Company profile updated successfully!", "success");
      if (window.bootstrap && modalEl) {
        const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
        modal.hide();
      }
      loadProfile();
    } catch (err) {
      alert(err.message);
    }
 finally {
      saveBtn.disabled = false;
      saveBtn.textContent = "Save Changes";
    }
  });

  // Company Verification Handlers
  document.getElementById("btn-verify-domain")?.addEventListener("click", async () => {
    const btn = document.getElementById("btn-verify-domain");
    btn.disabled = true;
    btn.textContent = "Verifying...";
    try {
      const res = await recruiterProfileAPI.verifyDomain();
      document.getElementById("domain-verification-msg").textContent = res.message;
      if (res.data.verification_status === "domain_verified") {
        document.getElementById("domain-verification-badge").className = "badge bg-success";
        document.getElementById("domain-verification-badge").textContent = "Domain Verified ✓";
      } else {
        document.getElementById("domain-verification-badge").className = "badge bg-warning text-dark";
        document.getElementById("domain-verification-badge").textContent = "Domain Unverified";
      }
      showAlert(res.message, res.data.verification_status === "domain_verified" ? "success" : "warning");
    } catch (e) {
      alert(e.message);
    } finally {
      btn.disabled = false;
      btn.textContent = "Verify Domain";
    }
  });

  document.getElementById("btn-verify-ssl")?.addEventListener("click", async () => {
    const btn = document.getElementById("btn-verify-ssl");
    btn.disabled = true;
    btn.textContent = "Checking...";
    try {
      const res = await recruiterProfileAPI.verifyWebsite();
      document.getElementById("ssl-verification-msg").textContent = res.data.ssl_details;
      if (res.data.ssl_verified) {
        document.getElementById("ssl-verification-badge").className = "badge bg-success";
        document.getElementById("ssl-verification-badge").textContent = "SSL Secure ✓";
      } else {
        document.getElementById("ssl-verification-badge").className = "badge bg-danger";
        document.getElementById("ssl-verification-badge").textContent = "SSL Failed";
      }
      showAlert(res.message, res.data.ssl_verified ? "success" : "danger");
    } catch (e) {
      alert(e.message);
    } finally {
      btn.disabled = false;
      btn.textContent = "Check SSL";
    }
  });

  document.getElementById("btn-submit-gov-verification")?.addEventListener("click", async () => {
    const input = document.getElementById("input-cin-gstin");
    const val = input.value.trim();
    if (!val) {
      alert("Please enter a valid CIN or GSTIN number.");
      return;
    }
    const btn = document.getElementById("btn-submit-gov-verification");
    btn.disabled = true;
    btn.textContent = "Submitting...";
    try {
      const res = await recruiterProfileAPI.submitCompanyVerification({ cin_gstin: val });
      document.getElementById("gov-verification-status-msg").textContent = res.data.notes;
      showAlert(res.message, res.data.verification_status === "government_verified" ? "success" : "info");
    } catch (e) {
      alert(e.message);
    } finally {
      btn.disabled = false;
      btn.textContent = "Submit";
    }
  });

  document.addEventListener("ar:auth-ready", () => {
    loadProfile();
  });
})();

