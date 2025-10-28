const API_URL = "http://127.0.0.1:8000";
const userId = "user123"; // you can make this dynamic
const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keypress", e => {
  if (e.key === "Enter") sendMessage();
});

async function sendMessage() {
  const text = input.value.trim();
  if (!text) return;
  input.value = "";

  appendMessage(text, "user");

  try {
    const res = await fetch(`${API_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, message: text })
    });

    if (res.status === 429) {
      const data = await res.json();
      appendMessage(data.detail, "bot");
      return;
    }

    const data = await res.json();
    appendMessage(`Got it! (${data.message})`, "bot");
  } catch (err) {
    appendMessage("⚠️ Error connecting to server.", "bot");
  }
}

function appendMessage(text, sender) {
  const msg = document.createElement("div");
  msg.classList.add("message", sender);
  msg.textContent = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}
