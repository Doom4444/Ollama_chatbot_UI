from rag.vector_store import get_vector_store

def retrieve_documents(query, k=5):

    vector_store = get_vector_store()

    results = vector_store.similarity_search_with_score(query, k=8)

    docs = []

    print("\nQUERY:", query)

    for doc, score in results:

        if len(doc.page_content) > 200:

            print("SCORE:", score)
            print("SOURCE:", doc.metadata.get("source"))
            print("DOC:", doc.page_content[:120])
            print("-----")

            docs.append(doc)

    return docs[:k]