const messagesEl = document.getElementById("messages");
const emptyState = document.getElementById("emptyState");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");
const systemPrompt = document.getElementById("systemPrompt");
const statusEl = document.getElementById("status");
const modelSelect = document.getElementById("modelSelect");
const loadModelsBtn = document.getElementById("loadModelsBtn");

let messages = [];
let currentModel = "";

function hideEmptyState() {
  if (emptyState) emptyState.style.display = "none";
}

function showEmptyState() {
  if (emptyState) emptyState.style.display = "flex";
}

function setStatus(text, isError = false) {
  statusEl.textContent = text;
  statusEl.className = "status" + (isError ? " error" : "");
}

function setCurrentModel(name) {
  currentModel = name || "";
  if (modelSelect) modelSelect.value = currentModel;
}

function buildMessagesForApi() {
  return messages.map(({ role, content }) => ({ role, content }));
}

function addMessage(role, content, meta = null) {
  hideEmptyState();
  const div = document.createElement("div");
  div.className = `message ${role}`;
  const avatar = role === "user" ? "You" : "Qwen";
  div.innerHTML = `
    <span class="avatar">${avatar.slice(0, 1)}</span>
    <div class="message-body">
      <div class="bubble">${escapeHtml(content)}</div>
      ${meta ? `<div class="meta">${escapeHtml(meta)}</div>` : ""}
    </div>
  `;
  messagesEl.appendChild(div);
  div.scrollIntoView({ behavior: "smooth", block: "end" });
  return div;
}

function escapeHtml(s) {
  const el = document.createElement("span");
  el.textContent = s;
  return el.innerHTML;
}

function updateBubbleContent(el, content, showCursor = false) {
  const bubble = el.querySelector(".bubble");
  if (!bubble) return;
  bubble.innerHTML = escapeHtml(content) + (showCursor ? '<span class="cursor"></span>' : "");
  el.scrollIntoView({ behavior: "smooth", block: "end" });
}

function appendToBubble(el, chunk) {
  const bubble = el.querySelector(".bubble");
  if (!bubble) return;
  const cursor = bubble.querySelector(".cursor");
  const text = bubble.childNodes[0];
  if (text && text.nodeType === Node.TEXT_NODE) {
    text.textContent = text.textContent + chunk;
  } else {
    bubble.innerHTML = escapeHtml(bubble.textContent || "") + escapeHtml(chunk) + '<span class="cursor"></span>';
  }
  if (cursor) cursor.remove();
  bubble.appendChild(document.createElement("span"));
  bubble.lastChild.className = "cursor";
  el.scrollIntoView({ behavior: "smooth", block: "end" });
}

async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  if (!currentModel) {
    setStatus("Select a model from the dropdown first (or click Refresh models).", true);
    return;
  }

  userInput.value = "";
  userInput.style.height = "auto";

  messages.push({ role: "user", content: text });
  addMessage("user", text);

  const assistantMsg = addMessage("assistant", "");
  const assistantEl = messagesEl.lastElementChild;
  let fullContent = "";
  sendBtn.disabled = true;
  setStatus("Thinking…");

  const apiMessages = buildMessagesForApi();
  const system = (systemPrompt && systemPrompt.value && systemPrompt.value.trim) ? systemPrompt.value.trim() : "";
  if (system) {
    apiMessages.unshift({ role: "system", content: system });
  }

  const body = {
    model: currentModel,
    messages: apiMessages,
    stream: true,
  };
  if (system) {
    body.system = system;
  }

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      let errText = await res.text();
      try {
        const j = JSON.parse(errText);
        if (j.error) errText = j.error;
      } catch (_) {}
      throw new Error(errText || `HTTP ${res.status}`);
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() || "";

      for (const line of lines) {
        if (!line.trim()) continue;
        try {
          const data = JSON.parse(line);
          if (data.error) {
            throw new Error(data.error);
          }
          const chunk = data.message?.content ?? data.response ?? "";
          if (chunk) fullContent += chunk;
          updateBubbleContent(assistantEl, fullContent, !data.done);
          if (data.done) {
            const meta = [];
            if (data.eval_count != null) meta.push(`Tokens: ${data.eval_count}`);
            if (data.eval_duration != null) {
              const sec = (data.eval_duration / 1e9).toFixed(2);
              meta.push(`Time: ${sec}s`);
            }
            if (meta.length) {
              const metaEl = assistantEl.querySelector(".meta");
              if (metaEl) metaEl.textContent = meta.join(" · ");
            }
            updateBubbleContent(assistantEl, fullContent, false);
          }
        } catch (parseErr) {
          if (parseErr instanceof SyntaxError) continue;
          throw parseErr;
        }
      }
    }

    messages.push({ role: "assistant", content: fullContent });
    setStatus("");
  } catch (err) {
    console.error(err);
    const msg = err.message || "Request failed";
    setStatus("Error: " + msg, true);
    updateBubbleContent(assistantEl, "Sorry, something went wrong. " + msg);
    messages.push({ role: "assistant", content: "" });
  } finally {
    sendBtn.disabled = false;
  }
}

userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

userInput.addEventListener("input", () => {
  userInput.style.height = "auto";
  userInput.style.height = Math.min(userInput.scrollHeight, 12 * 24) + "px";
});

sendBtn.addEventListener("click", sendMessage);

clearBtn.addEventListener("click", () => {
  messages = [];
  while (messagesEl.firstChild) messagesEl.removeChild(messagesEl.firstChild);
  messagesEl.appendChild(emptyState);
  showEmptyState();
  setStatus("");
});

function populateModelSelect(models) {
  if (!modelSelect) return;
  modelSelect.innerHTML = "";
  if (!models || models.length === 0) {
    const opt = document.createElement("option");
    opt.value = "";
    opt.textContent = "No models — run: ollama pull <model>";
    modelSelect.appendChild(opt);
    setCurrentModel("");
    return;
  }
  models.forEach((m) => {
    const opt = document.createElement("option");
    opt.value = m.name;
    opt.textContent = m.name;
    modelSelect.appendChild(opt);
  });
  setCurrentModel(models[0].name);
}

async function loadModels() {
  setStatus("Loading models…");
  try {
    const res = await fetch("/api/tags");
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.error || "Failed to load models");
    }
    const data = await res.json();
    const models = data.models || [];
    populateModelSelect(models);
    setStatus(models.length ? "Ready. Select a model and chat." : "No models found. Run: ollama pull <model>");
  } catch (err) {
    setStatus("Could not load models: " + err.message, true);
    if (modelSelect) {
      modelSelect.innerHTML = "";
      const opt = document.createElement("option");
      opt.value = "";
      opt.textContent = "Error — click Refresh models";
      modelSelect.appendChild(opt);
      setCurrentModel("");
    }
  }
}

modelSelect.addEventListener("change", () => {
  setCurrentModel(modelSelect.value);
});

loadModelsBtn.addEventListener("click", loadModels);

// Load available models on page load so users can pick one they have
loadModels();
