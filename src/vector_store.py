import faiss
import numpy as np
import pickle

class VectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

    def add(self, embeddings, chunks):
        self.index.add(np.array(embeddings).astype("float32"))
        self.metadata.extend(chunks)

    def save(self, index_path, metadata_path):
        faiss.write_index(self.index, index_path)
        with open(metadata_path, "wb") as f:
            pickle.dump(self.metadata, f)

    def load(self, index_path, metadata_path):
        self.index = faiss.read_index(index_path)
        with open(metadata_path, "rb") as f:
            self.metadata = pickle.load(f)

    def search(self, query_embedding, top_k):
        D, I = self.index.search(query_embedding, top_k)

        results = []
        for idx in I[0]:
            results.append(self.metadata[idx])

        return results