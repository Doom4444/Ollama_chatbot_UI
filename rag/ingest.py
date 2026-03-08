import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

from rag.vector_store import get_vector_store


DATA_PATH = "data/documents"


def ingest_documents():

    vector_store = get_vector_store()

    documents = []

    for file in os.listdir(DATA_PATH):

        if file.endswith(".pdf"):

            loader = PyPDFLoader(os.path.join(DATA_PATH, file))
            documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=80
    )

    chunks = splitter.split_documents(documents)

    vector_store.add_documents(chunks)

    print(f"Ingested {len(chunks)} chunks.")