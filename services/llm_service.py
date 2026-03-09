import requests
from config import OLLAMA_HOST
from rag.retriever import retrieve_documents


def stream_chat(payload):

    url = f"{OLLAMA_HOST}/api/chat"
    messages = payload.get("messages", [])

    if messages:
        user_message = messages[-1]["content"]

        # Retrieve documents once
        docs = retrieve_documents(user_message, k=5, mode="mmr")

        context = "\n\n".join(d.page_content for d in docs)

        print("\n" + "="*60)
        print("CONTEXT BUILDING")
        print("="*60)
        
        print("QUESTION:", user_message)

        for d in docs:
            print("SOURCE:", d.metadata.get("source"))
            print("DOC:", d.page_content[:120])
            print("-----")

        rag_prompt = f"""
You are a financial assistant.

Answer the question using ONLY the provided context.

Write a concise answer in 2–3 sentences.
Do not repeat the same idea.
Summarize the information in your own words.

If the answer is not in the context, say you do not know.

Context:
{context}

Question:
{user_message}
"""

        messages[-1]["content"] = rag_prompt
        payload["messages"] = messages

    # Single LLM request
    with requests.post(url, json=payload, stream=True, timeout=120) as r:
        r.raise_for_status()

        for chunk in r.iter_content(chunk_size=None):
            if chunk:
                yield chunk

    print("Retrieved context:", context[:200])
    print("\n" + "="*60)
    print("LLM RESPONSE COMPLETE")
    print("="*60)

def list_models():
    url = f"{OLLAMA_HOST}/api/tags"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()


def build_context(question, k=3):

    docs = retrieve_documents(question, k=k)

    context = "\n\n".join([d.page_content for d in docs])

    return context