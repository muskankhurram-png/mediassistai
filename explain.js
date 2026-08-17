document.addEventListener("DOMContentLoaded", () => {
  let mode = "disease";
  const tabs = document.querySelectorAll(".explain-tab");
  const input = document.getElementById("explainInput");
  const btn = document.getElementById("explainBtn");
  const loading = document.getElementById("explainLoading");
  const result = document.getElementById("explainResult");

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      tabs.forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");
      mode = tab.dataset.mode;
      input.placeholder = mode === "disease" ? "e.g. Diabetes" : "e.g. Metformin";
    });
  });

  async function submitExplain() {
    const name = input.value.trim();
    if (!name) return;

    result.classList.remove("visible");
    loading.style.display = "flex";
    btn.disabled = true;

    const endpoint = mode === "disease" ? "/ai/explain/disease" : "/ai/explain/medicine";

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name }),
      });
      const data = await response.json();

      loading.style.display = "none";
      btn.disabled = false;

      if (!response.ok) {
        result.textContent = data.detail || "Something went wrong.";
      } else {
        result.textContent = data.explanation;
      }
      result.classList.add("visible");
    } catch (err) {
      loading.style.display = "none";
      btn.disabled = false;
      result.textContent = "Network error - please try again.";
      result.classList.add("visible");
    }
  }

  btn.addEventListener("click", submitExplain);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") submitExplain();
  });
});
