/**
 * post-job.js — handles the "Post a Job" form submit.
 */
(function () {
  const form = document.getElementById("post-job-form");
  const alertBox = document.getElementById("post-job-alert");
  const submitBtn = document.getElementById("post-job-submit");
  const submitText = document.getElementById("post-job-submit-text");
  const spinner = document.getElementById("post-job-spinner");

  function showAlert(message, variant) {
    alertBox.textContent = message;
    alertBox.className = `alert alert-${variant} py-2`;
  }

  function parseSkillList(value) {
    const items = value
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);
    return items.length ? items : null; // null -> let the backend auto-extract
  }

  function setLoading(isLoading) {
    submitBtn.disabled = isLoading;
    spinner.classList.toggle("d-none", !isLoading);
    submitText.textContent = isLoading ? "Posting..." : "Post Job";
  }

  const analyzeBtn = document.getElementById("analyze-btn");
  const analyzeBtnText = document.getElementById("analyze-btn-text");
  const analyzeSpinner = document.getElementById("analyze-spinner");

  analyzeBtn.addEventListener("click", async () => {
    const description = document.getElementById("description").value.trim();
    if (description.length < 10) {
      showAlert("Write a description first (at least 10 characters), then analyze it.", "warning");
      return;
    }

    analyzeBtn.disabled = true;
    analyzeSpinner.classList.remove("d-none");
    analyzeBtnText.textContent = "Analyzing...";

    try {
      const res = await jobsAPI.analyze(description);
      const data = res.data;

      if (data.title) document.getElementById("title").value = data.title;
      if (data.required_skills?.length) {
        document.getElementById("required-skills").value = data.required_skills.join(", ");
      }
      if (data.preferred_skills?.length) {
        document.getElementById("preferred-skills").value = data.preferred_skills.join(", ");
      }
      showAlert(`Analyzed (${data.source}). Review the pre-filled fields below before posting.`, "success");
    } catch (err) {
      showAlert(err.message, "danger");
    } finally {
      analyzeBtn.disabled = false;
      analyzeSpinner.classList.add("d-none");
      analyzeBtnText.textContent = "Analyze with AI";
    }
  });

  // Auto-prefill company details from saved recruiter profile if available
  (async function prefillCompanyDetails() {
    try {
      const res = await API.get("/recruiter-profile");
      if (res && res.data) {
        const p = res.data;
        if (p.company_name) document.getElementById("company-name").value = p.company_name;
        if (p.company_logo) document.getElementById("company-logo").value = p.company_logo;
        if (p.company_description) document.getElementById("company-description").value = p.company_description;
        if (p.website) document.getElementById("company-website").value = p.website;
        if (p.location) document.getElementById("company-location").value = p.location;
        if (p.industry) document.getElementById("industry").value = p.industry;
        if (p.company_size) document.getElementById("company-size").value = p.company_size;
        if (p.linkedin_url) document.getElementById("linkedin-profile").value = p.linkedin_url;
        if (p.github_url) document.getElementById("github-profile").value = p.github_url;
        if (p.other_links) document.getElementById("other-links").value = p.other_links;
      }
    } catch (e) {
      // Ignore if profile doesn't exist yet
    }
  })();

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    setLoading(true);

    const experienceRaw = document.getElementById("experience-required").value;

    const payload = {
      title: document.getElementById("title").value.trim(),
      description: document.getElementById("description").value.trim(),
      location: document.getElementById("location").value.trim() || null,
      employment_type: document.getElementById("employment-type").value,
      experience_required: experienceRaw ? Number(experienceRaw) : null,
      salary_range: document.getElementById("salary-range").value.trim() || null,
      status: document.getElementById("status").value,
      required_skills: parseSkillList(document.getElementById("required-skills").value),
      preferred_skills: parseSkillList(document.getElementById("preferred-skills").value) || [],
      // Candidate Screening Settings
      min_ats_score: Number(document.getElementById("min-ats-score").value) || 60,
      min_job_match_score: Number(document.getElementById("min-job-match-score").value) || 60,
      min_experience: Number(document.getElementById("min-experience").value) || 0,
      auto_screening: document.getElementById("auto-screening").value === "true",
      auto_shortlist: document.getElementById("auto-shortlist").value === "true",
      // Company details
      company_name: document.getElementById("company-name").value.trim() || null,
      company_logo: document.getElementById("company-logo").value.trim() || null,
      company_description: document.getElementById("company-description").value.trim() || null,
      company_website: document.getElementById("company-website").value.trim() || null,
      company_location: document.getElementById("company-location").value.trim() || null,
      industry: document.getElementById("industry").value.trim() || null,
      company_size: document.getElementById("company-size").value || null,
      linkedin_profile: document.getElementById("linkedin-profile").value.trim() || null,
      github_profile: document.getElementById("github-profile").value.trim() || null,
      other_links: document.getElementById("other-links").value.trim() || null,
    };

    try {
      const res = await jobsAPI.create(payload);
      if (res.data.fraud_risk_level === "HIGH" || res.data.status === "pending_review") {
        showAlert(
          `Job "${res.data.title}" saved, but AI Fraud Scan detected risk factors (Score: ${res.data.fraud_risk_score}/100). It is currently under Admin Review before publishing.`,
          "warning"
        );
      } else {
        showAlert(`"${res.data.title}" passed AI fraud verification and was published successfully!`, "success");
      }
      form.reset();
      document.getElementById("employment-type").value = "full_time";
      document.getElementById("status").value = "published";
      setTimeout(() => {
        window.location.href = "my-jobs.html";
      }, 1500);
    } catch (err) {
      showAlert(err.message, "danger");
    } finally {
      setLoading(false);
    }

  });
})();
