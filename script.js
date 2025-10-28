const chatBox = document.getElementById("chatBox");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");

// Function to append messages to the chat box
function appendMessage(sender, message) {
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", sender);
  msgDiv.textContent = message;
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight; // auto-scroll to the latest message
}

// Function to send user query and get bot response
async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return; // do nothing if empty

  appendMessage("user", message);
  userInput.value = "";

  // temporary “Thinking…” message
  appendMessage("bot", "Thinking...");

  try {
    const response = await fetch("http://127.0.0.1:5600/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: message }),
    });

    // handle invalid server response
    if (!response.ok) throw new Error(`HTTP error: ${response.status}`);

    const data = await response.json();

    // Replace the “Thinking…” message with the bot’s real response
    chatBox.lastChild.textContent = data.answer || "No response received.";
  } catch (error) {
    console.error("Chatbot error:", error);
    chatBox.lastChild.textContent = "⚠️ Error: Could not reach the server.";
  }
}

// Event listeners
sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});
