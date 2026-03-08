# Ollama Chat UI

A simple, friendly web interface to chat with **any model** running on your computer via [Ollama](https://ollama.com). Includes **RAG (Retrieval-Augmented Generation)** so the model can answer questions using **your own documents** (PDFs). No account needed—everything runs locally.

---

## Quick start

1. **Install and run Ollama** (if you haven’t already):  
   [ollama.com](https://ollama.com) → download and install. Then pull a chat model and the embedding model used for RAG:
   ```bash
   ollama pull qwen2.5:3b-instruct-q4_K_M
   ollama pull nomic-embed-text
   ```

2. **Install dependencies and start this app:**
   ```bash
   pip install -r requirements.txt
   python app.py
   ```

3. **Open your browser** at **http://localhost:5000**

4. **Pick a model** from the dropdown, type a message, and hit Send.

5. **Optional — Use your documents:** Put PDFs in `data/documents/`, then run the ingest once (see [Documents & RAG](#documents--rag) below). After that, your chats will use those documents as context.

---

## What you need

- **Python 3.8+**
- **Ollama** installed and running (the Ollama app or service must be on; you don’t need to keep `ollama run` open)
- **At least one chat model** pulled in Ollama (e.g. `qwen2.5:3b-instruct-q4_K_M`). For **RAG**, you also need the embedding model:
  ```bash
  ollama pull nomic-embed-text
  ```
  To see your models:
  ```bash
  ollama list
  ```
  To pull a chat model you don’t have yet:
  ```bash
  ollama pull qwen2.5:3b-instruct-q4_K_M
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

## Documents & RAG

The app can answer questions using **your own PDF documents**. Each time you send a message, the app finds relevant passages from your documents and sends them to the model as context, so answers are grounded in your data (RAG = Retrieval-Augmented Generation).

### 1. Put your documents in place

- Create the folder **`data/documents`** in the project root (if it doesn’t exist).
- Add **PDF files** into `data/documents/`. Only `.pdf` files are loaded.

Example:
```text
Ollama_chatbot_UI/
  data/
    documents/
      report.pdf
      manual.pdf
```

### 2. Pull the embedding model (required for RAG)

RAG uses Ollama to compute embeddings. Pull the embedding model once:

```bash
ollama pull nomic-embed-text
```

### 3. Ingest documents into the vector store

From the **project root**, run the ingest so your PDFs are chunked, embedded, and stored:

```bash
python -c "from rag.ingest import ingest_documents; ingest_documents()"
```

You should see something like: `Ingested 42 chunks.`

- Run this again whenever you **add or change** PDFs in `data/documents/`.
- The vector store is saved under `db/chroma/` (created automatically).

### 4. Chat as usual

- Start the app (`python app.py`), open **http://localhost:5000**, choose a model, and send messages.
- Each message triggers a search over your ingested documents; the model is instructed to answer from that context only and to say it doesn’t know when the answer isn’t in the context.

### RAG summary

| Step | Action |
|------|--------|
| **Documents** | PDFs in `data/documents/` |
| **Embedding model** | `ollama pull nomic-embed-text` |
| **Ingest** | `python -c "from rag.ingest import ingest_documents; ingest_documents()"` |
| **Re-ingest** | Run the same ingest command after adding or updating PDFs |
| **Chat** | Use the UI normally; answers use your documents as context |

---

## If something goes wrong

- **“Select a model from the dropdown first”**  
  Pick a model from the **Model** menu. If the list is empty, click **Refresh models**. Make sure Ollama is running and you have at least one model (`ollama list`).

- **“Cannot connect to Ollama”**  
  Start the Ollama app (or ensure the Ollama service is running). The app expects Ollama at `http://localhost:11434` by default.

- **No models in the dropdown**  
  Pull at least one model, e.g. `ollama pull qwen2.5:3b-instruct-q4_K_M`, then click **Refresh models** in the app.

- **Ollama on another machine or port**  
  Set the `OLLAMA_HOST` environment variable before starting the app, e.g.:
  ```bash
  set OLLAMA_HOST=http://192.168.1.10:11434
  python app.py
  ```
  (Use `export OLLAMA_HOST=...` on macOS/Linux.)

- **RAG: “I don’t know” or answers not using my documents**  
  Ensure you’ve run the ingest after putting PDFs in `data/documents/` (`python -c "from rag.ingest import ingest_documents; ingest_documents()"`). Confirm `nomic-embed-text` is pulled (`ollama list`). If you added or updated PDFs, run the ingest again.

- **Ingest fails or “No module named 'langchain_...'”**  
  Install dependencies: `pip install -r requirements.txt`. Run the ingest from the project root so `rag` and `data/documents` are found.

---

## Configuration

| Setting | Description |
|--------|--------------|
| **Ollama URL** | Default: `http://localhost:11434`. Override with the `OLLAMA_HOST` environment variable. |
| **System prompt** | Edit the text in the **System prompt** section in the UI; no code change needed. |
| **Model** | Chosen in the UI from the models reported by Ollama; no config file to edit. |
| **RAG documents** | PDFs in `data/documents/`; ingest with `python -c "from rag.ingest import ingest_documents; ingest_documents()"`. |
| **RAG vector store** | Stored in `db/chroma/`; embedding model is `nomic-embed-text` (see `config.py` to change). |

---

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for the full text. You may use, modify, and distribute it freely under the terms of that license.
