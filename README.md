# Ollama Chat UI

A simple, friendly web interface to chat with **any model** running on your computer via [Ollama](https://ollama.com). No account needed—everything runs locally.

---

## Quick start

1. **Install and run Ollama** (if you haven’t already):  
   [ollama.com](https://ollama.com) → download and install. Then pull a model, e.g.:
   ```bash
   ollama pull llama3.2
   ```

2. **Start this app:**
   ```bash
   pip install -r requirements.txt
   python app.py
   ```

3. **Open your browser** at **http://localhost:5000**

4. **Pick a model** from the dropdown, type a message, and hit Send.

---

## What you need

- **Python 3.8+**
- **Ollama** installed and running (the Ollama app or service must be on; you don’t need to keep `ollama run` open)
- **At least one model** pulled in Ollama. To see your models:
  ```bash
  ollama list
  ```
  To pull a model you don’t have yet:
  ```bash
  ollama pull llama3.2
  ```

---

## Setup (step by step)

### 1. Clone or download this project

### 2. Optional: use a virtual environment (recommended)

**Windows (PowerShell or CMD):**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

You should see something like: `Running on http://0.0.0.0:5000`

### 5. Open in your browser

Go to: **http://localhost:5000**

---

## Using the app

| What to do | How |
|------------|-----|
| **Choose a model** | Use the **Model** dropdown in the header. Models are loaded when the page opens. |
| **Refresh the model list** | Click **Refresh models** (e.g. after you run `ollama pull <model>`). |
| **Send a message** | Type in the box and press **Enter** (or click the send button). Use **Shift+Enter** for a new line. |
| **Set behavior** | Expand **System prompt** and edit the text; it’s sent with every message (e.g. “You are a helpful assistant”, or “Reply in the same language as the user”). |
| **Start over** | Click **Clear chat** to begin a new conversation. |

- **Streaming:** Replies appear as they’re generated.
- **History:** The full conversation is sent to the model so you can have a multi-turn chat.

---

## If something goes wrong

- **“Select a model from the dropdown first”**  
  Pick a model from the **Model** menu. If the list is empty, click **Refresh models**. Make sure Ollama is running and you have at least one model (`ollama list`).

- **“Cannot connect to Ollama”**  
  Start the Ollama app (or ensure the Ollama service is running). The app expects Ollama at `http://localhost:11434` by default.

- **No models in the dropdown**  
  Pull at least one model, e.g. `ollama pull llama3.2`, then click **Refresh models** in the app.

- **Ollama on another machine or port**  
  Set the `OLLAMA_HOST` environment variable before starting the app, e.g.:
  ```bash
  set OLLAMA_HOST=http://192.168.1.10:11434
  python app.py
  ```
  (Use `export OLLAMA_HOST=...` on macOS/Linux.)

---

## Configuration

| Setting | Description |
|--------|--------------|
| **Ollama URL** | Default: `http://localhost:11434`. Override with the `OLLAMA_HOST` environment variable. |
| **System prompt** | Edit the text in the **System prompt** section in the UI; no code change needed. |
| **Model** | Chosen in the UI from the models reported by Ollama; no config file to edit. |

---

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for the full text. You may use, modify, and distribute it freely under the terms of that license.
