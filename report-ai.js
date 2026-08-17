document.addEventListener("DOMContentLoaded", () => {
  async function callAI(endpoint, reportId, panelId, renderFn) {
    const loading = document.getElementById(`loading-${reportId}`);
    const panel = document.getElementById(panelId);
    const body = panel.querySelector(".ai-panel-body");

    loading.style.display = "flex";
    panel.classList.remove("visible");

    try {
      const response = await fetch(endpoint, { method: "POST" });
      const data = await response.json();
      loading.style.display = "none";

      if (!response.ok) {
        body.textContent = data.detail || "Something went wrong.";
      } else {
        renderFn(body, data);
      }
      panel.classList.add("visible");
    } catch (err) {
      loading.style.display = "none";
      body.textContent = "Network error - please try again.";
      panel.classList.add("visible");
    }
  }

  document.querySelectorAll(".ai-summary-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const reportId = btn.dataset.reportId;
      callAI(`/ai/reports/${reportId}/summary`, reportId, `summary-${reportId}`, (body, data) => {
        body.textContent = data.summary;
      });
    });
  });

  document.querySelectorAll(".ai-risk-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const reportId = btn.dataset.reportId;
      callAI(`/ai/reports/${reportId}/risk-alerts`, reportId, `risk-${reportId}`, (body, data) => {
        body.innerHTML = "";
        if (!data.alerts || data.alerts.length === 0) {
          body.textContent = "No risk flags detected in this report.";
        } else {
          data.alerts.forEach((alert) => {
            const chip = document.createElement("span");
            chip.className = "risk-chip";
            chip.textContent = alert;
            body.appendChild(chip);
          });
        }
      });
    });
  });
});
