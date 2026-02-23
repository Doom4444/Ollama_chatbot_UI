# Ollama Chat UI

A small web app to chat with your local **Ollama** model (any model you have). It uses a Python backend to proxy requests to Ollama and a simple frontend with streaming replies.

## Prerequisites

- **Python 3.8+**
- List you available models in Ollama:

```bash
  ollama ls
```

- **Ollama** Replace "YOUR MODEL NAME" with the name of the model you want to run:
  ```bash
  ollama run YOUR MODEL NAME
  ```
  Have Ollama model running in the background after it starts, by pressing on your keyboard:
  ```bash
  CTRL + D
  ```
  the app will call it when you send a message.

## Setup and run

1. Create a virtual environment (optional but recommended):
  ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # source .venv/bin/activate  # macOS/Linux
  ```
2. Install dependencies:
  ```bash
   pip install -r requirements.txt
  ```
3. Start the app:
  ```bash
   python app.py
  ```
4. Open in the browser: **[http://localhost:5000](http://localhost:5000)**

## Features

- **Streaming replies** – tokens appear as they are generated.
- **Conversation history** – full chat is sent to the model so you can have a multi-turn dialogue.
- **Optional system prompt** – expand “System prompt (optional)” and set instructions for the model.
- **Clear chat** – start a new conversation.
- **Refresh models** – reload the list of models from Ollama (model name is shown in the header).

## Configuration

- **Ollama URL**: By default the app uses `http://localhost:11434`. Override with the environment variable:
  ```bash
  set OLLAMA_HOST=http://localhost:11434
  python app.py
  ```
- **Default model**: Edit `DEFAULT_MODEL` in `app.py` if you want another default than `iKhalid/ALLaM:7b`.

