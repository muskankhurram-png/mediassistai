/**
 * Toast notification system. Reads any elements with [data-toast]
 * (rendered server-side from Jinja2 flash messages) and animates
 * them as floating, auto-dismissing pop-ups instead of static banners.
 */
function createToast(message, type = "success") {
  const container = document.getElementById("toastContainer");
  if (!container) return;

  const icons = { success: "✓", error: "⚠", warning: "!" };

  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <span class="toast-icon">${icons[type] || "•"}</span>
    <span>${message}</span>
    <button class="toast-close" aria-label="Dismiss">&times;</button>
  `;

  toast.querySelector(".toast-close").addEventListener("click", () => dismissToast(toast));
  container.appendChild(toast);

  setTimeout(() => dismissToast(toast), 4500);
}

function dismissToast(toast) {
  toast.classList.add("toast-hide");
  setTimeout(() => toast.remove(), 280);
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-toast]").forEach((el) => {
    createToast(el.dataset.toast, el.dataset.toastType || "success");
    el.remove();
  });
});
