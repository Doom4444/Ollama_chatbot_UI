import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

DEFAULT_MODEL = "iKhalid/ALLaM:7b"

CHROMA_DB_PATH = "./db/chroma"

EMBEDDING_MODEL = "nomic-embed-text"