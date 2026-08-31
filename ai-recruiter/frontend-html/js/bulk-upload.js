/**
 * bulk-upload.js — Recruiter Bulk Resume Upload & Batch Parsing Frontend Logic
 */
(function () {
  const dropzone = document.getElementById("bulk-upload-dropzone");
  const fileInput = document.getElementById("bulk-resume-file-input");
  const startBtn = document.getElementById("start-bulk-upload-btn");
  const statusContainer = document.getElementById("bulk-status-container");
  const statusLabel = document.getElementById("bulk-status-label");
  const statusCount = document.getElementById("bulk-status-count");
  const progressBar = document.getElementById("bulk-progress-bar");
  const resultsWrapper = document.getElementById("bulk-results-wrapper");
  const resultsTableBody = document.getElementById("bulk-results-table-body");

  let selectedFiles = [];

  if (!dropzone || !fileInput) return;

  dropzone.addEventListener("click", () => fileInput.click());

  dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("bg-success-subtle");
  });

  dropzone.addEventListener("dragleave", () => {
    dropzone.classList.remove("bg-success-subtle");
  });

  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("bg-success-subtle");
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      selectedFiles = Array.from(e.dataTransfer.files);
      updateDropzoneLabel();
    }
  });

  fileInput.addEventListener("change", () => {
    if (fileInput.files && fileInput.files.length > 0) {
      selectedFiles = Array.from(fileInput.files);
      updateDropzoneLabel();
    }
  });

  function updateDropzoneLabel() {
    const heading = dropzone.querySelector("h6");
    if (heading) {
      heading.textContent = `Selected ${selectedFiles.length} file(s): ${selectedFiles.map(f => f.name).join(", ")}`;
    }
  }

  if (startBtn) {
    startBtn.addEventListener("click", async () => {
      if (selectedFiles.length === 0) {
        alert("Please select at least one PDF/DOCX resume file or ZIP archive.");
        return;
      }

      startBtn.disabled = true;
      statusContainer.classList.remove("d-none");
      statusLabel.textContent = "Uploading & processing batch resumes...";
      progressBar.style.width = "40%";
      statusCount.textContent = `0 / ${selectedFiles.length}`;

      const formData = new FormData();
      selectedFiles.forEach((file) => {
        formData.append("files", file, file.name);
      });

      try {
        const token = Session.getAccessToken();
        const response = await fetch("http://localhost:8000/api/v1/resumes/bulk-upload", {
          method: "POST",
          headers: token ? { Authorization: `Bearer ${token}` } : {},
          body: formData,
        });

        const res = await response.json();
        if (res.success && res.data) {
          progressBar.style.width = "100%";
          statusLabel.textContent = "Processing completed!";
          statusCount.textContent = `${res.data.successful} succeeded, ${res.data.failed} failed`;
          renderResults(res.data.results || []);
        } else {
          alert(res.message || "Bulk upload failed.");
        }
      } catch (err) {
        console.error("Bulk upload error:", err);
        alert("Error connecting to server for bulk upload.");
      } finally {
        startBtn.disabled = false;
      }
    });
  }

  function renderResults(results) {
    if (!resultsWrapper || !resultsTableBody) return;
    resultsWrapper.classList.remove("d-none");

    if (results.length === 0) {
      resultsTableBody.innerHTML = `<tr><td colspan="5" class="text-center text-muted">No files processed.</td></tr>`;
      return;
    }

    resultsTableBody.innerHTML = results.map(r => {
      const data = r.extracted_data || {};
      const statusBadge = r.status === "completed"
        ? `<span class="badge bg-success">Completed</span>`
        : `<span class="badge bg-danger" title="${escapeHtml(r.error || "")}">Failed</span>`;

      return `
        <tr>
          <td class="fw-semibold small">${escapeHtml(r.filename)}</td>
          <td>${statusBadge}</td>
          <td class="small">${escapeHtml(data.name || "—")}</td>
          <td class="small text-muted">${escapeHtml(data.email || "—")}</td>
          <td><span class="badge bg-primary-subtle text-primary border">${data.completeness_score != null ? data.completeness_score + "%" : "—"}</span></td>
        </tr>
      `;
    }).join("");
  }

  function escapeHtml(str) {
    if (!str) return "";
    return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
})();
