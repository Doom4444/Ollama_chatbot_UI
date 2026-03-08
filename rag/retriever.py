from rag.vector_store import get_vector_store

def retrieve_documents(query, k=5, threshold=0.50):

    vector_store = get_vector_store()
    results = vector_store.similarity_search_with_score(query, k=8)

    docs = []
    print("\n" + "="*60)
    print("RETRIEVAL RESULTS")
    print("="*60)
    print("\nQUERY:", query)

    for doc, score in results:

        if score < threshold and len(doc.page_content) > 200:

            print("SCORE:", score)
            print("SOURCE:", doc.metadata.get("source"))
            print("DOC:", doc.page_content[:120])
            print("-----")

            docs.append(doc)

    # fallback if nothing passed threshold
    if len(docs) == 0:
        docs = [doc for doc, _ in results[:k]]

    # deduplicate
    seen = set()
    unique_docs = []

    for doc in docs:
        text = doc.page_content.strip()

        if text not in seen:
            unique_docs.append(doc)
            seen.add(text)

    return unique_docs[:k]