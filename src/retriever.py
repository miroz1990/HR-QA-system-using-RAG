class Retriever:
    def __init__(self, vector_store, embedding_model, top_k):
        self.vector_store = vector_store
        self.embedding_model = embedding_model
        self.top_k = top_k

    def retrieve(self, query, filters=None):
        """
        filters example:
        {
            "role": "employee",
            "doc_type": "leave_policy"
        }
        """

        query_emb = self.embedding_model.encode([query])

        # Step 1: get more candidates first (important!)
        D, I = self.vector_store.index.search(query_emb, k=50)

        results = []
        # for idx in I[0]:
        for score, idx in zip(D[0], I[0]):
            chunk = self.vector_store.metadata[idx]

            if self._match_filters(chunk, filters):
                results.append({
                "text": chunk["text"],
                "source": chunk.get("source"),
                "section": chunk.get("section"),   # ✅ ADD THIS
                "role": chunk.get("role"),         # optional
                "score": float(score)
                })

            if len(results) >= self.top_k:
                break

        return results

    def _match_filters(self, chunk, filters):
        if not filters:
            return True

        for key, value in filters.items():
            if key not in chunk or chunk[key] != value:
                return False

        return True