/**
 * Handles the chat page: sends questions via fetch() to a
 * session-authenticated endpoint, and appends the conversation to
 * the chat window as animated bubbles - no page reload needed.
 */
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("chatForm");
  const input = document.getElementById("chatInput");
  const chatWindow = document.getElementById("chatWindow");

  if (!form) return;

  function scrollToBottom() {
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  function addBubble(text, sender) {
    const bubble = document.createElement("div");
    bubble.className = `chat-bubble ${sender}`;
    bubble.textContent = text;
    chatWindow.appendChild(bubble);
    scrollToBottom();
    return bubble;
  }

  function addTypingIndicator() {
    const typing = document.createElement("div");
    typing.className = "chat-typing";
    typing.id = "typingIndicator";
    typing.innerHTML = "<span></span><span></span><span></span>";
    chatWindow.appendChild(typing);
    scrollToBottom();
  }

  function removeTypingIndicator() {
    const typing = document.getElementById("typingIndicator");
    if (typing) typing.remove();
  }

  // Remove the empty-state placeholder the first time a message is sent
  function clearEmptyState() {
    const empty = chatWindow.querySelector(".chat-empty");
    if (empty) empty.remove();
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const question = input.value.trim();
    if (!question) return;

    clearEmptyState();
    addBubble(question, "user");
    input.value = "";
    input.disabled = true;
    addTypingIndicator();

    try {
      const response = await fetch("/chat/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      removeTypingIndicator();

      if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        addBubble(data.detail || "Something went wrong. Please try again.", "ai");
        return;
      }

      const data = await response.json();
      const aiBubble = addBubble(data.answer, "ai");

      if (data.sources && data.sources.length > 0) {
        const sourcesDiv = document.createElement("div");
        sourcesDiv.className = "chat-sources";
        sourcesDiv.textContent = "Sources: " + data.sources.join(", ");
        aiBubble.appendChild(sourcesDiv);
      }
    } catch (err) {
      removeTypingIndicator();
      addBubble("Network error - please check your connection and try again.", "ai");
    } finally {
      input.disabled = false;
      input.focus();
      scrollToBottom();
    }
  });

  scrollToBottom();
});
