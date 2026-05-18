from sentence_transformers import CrossEncoder

class Reranker:
    def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-2-v2"):
        self.model = CrossEncoder(model_name)

    def rerank(self, query, chunks, top_k=5):
        pairs = [(query, c["text"]) for c in chunks]

        scores = self.model.predict(pairs)

        scored_chunks = list(zip(chunks, scores))
        scored_chunks.sort(key=lambda x: x[1], reverse=True)

        return [c[0] for c in scored_chunks[:top_k]]
    