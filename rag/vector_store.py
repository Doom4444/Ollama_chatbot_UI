from langchain_chroma import Chroma
from rag.embeddings import get_embedding_model

CHROMA_PATH = "./db/chroma"

def get_vector_store():
    embeddings = get_embedding_model()

    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )