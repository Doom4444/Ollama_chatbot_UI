from rag.vector_store import get_vector_store

LOG_SEPARATOR = "=" * 60

def retrieve_documents(query, k=3, mode="similarity", threshold=0.5):

    vector_store = get_vector_store()

    print("\n" + LOG_SEPARATOR)
    print(f"RETRIEVAL MODE: {mode.upper()}")
    print(LOG_SEPARATOR)
    print("QUERY:", query)

    docs = []

    if mode == "mmr":

        docs = vector_store.max_marginal_relevance_search(
            query,
            k=k,
            fetch_k=30,
            lambda_mult=0.5
        )

        for doc in docs:
            print("SOURCE:", doc.metadata.get("source"))
            print("PAGE:", doc.metadata.get("page"))
            print("DOC:", doc.page_content[:120])
            print("-----")

    else:

        results = vector_store.similarity_search_with_score(query, k=8)

        for doc, score in results:

            if score < threshold and len(doc.page_content) > 200:

                print("SCORE:", score)
                print("SOURCE:", doc.metadata.get("source"))
                print("DOC:", doc.page_content[:120])
                print("-----")

                docs.append(doc)

    return docs[:k]