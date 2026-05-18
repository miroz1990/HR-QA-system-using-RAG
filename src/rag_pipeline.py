from src.ingest import load_documents
from src.chunking import chunk_documents
from src.embedding import EmbeddingModel
from src.vector_store import VectorStore
from src.retriever import Retriever
from src.prompt import build_prompt
from src.llm import generate_answer
from src.config import *
from src.reranker import Reranker
from pathlib import Path

import os

BASE_DIR = Path(__file__).resolve().parent.parent  # go up from src/

index_path = BASE_DIR / "embeddings" / "faiss_index.bin"
metadata_path = BASE_DIR / "embeddings" / "metadata.pkl"

def build_index():

    print("Checking for documents...")  # Add this
    docs = load_documents()
    print(f"Loaded {len(docs)} documents.") # Add this

    chunks = chunk_documents(docs, CHUNK_SIZE, CHUNK_OVERLAP)
    print(f"Created {len(chunks)} chunks.") # Add this

    # if not chunks:
    #     print("Warning: No chunks were created. Check your data source!")
    #     return
    
    # for i, chunk in enumerate(chunks[:3]): # Inspecting first 3
    #     print(f"\n--- Chunk {i} ---")
    #     print(f"Content: {chunk['text'][:1000]}...") # First 200 chars
    #     print(f"Metadata: {chunk.get('source', 'No source')}")


    embedder = EmbeddingModel(EMBEDDING_MODEL)
    embeddings = embedder.encode([c["text"] for c in chunks])

    vector_store = VectorStore(dim=embeddings.shape[1])
    vector_store.add(embeddings, chunks)
    print(vector_store.metadata[0])

    os.makedirs("embeddings", exist_ok=True)
    vector_store.save(str(index_path), str(metadata_path))
    # vector_store.save("embeddings/faiss_index.bin", "embeddings/metadata.pkl")


def load_pipeline():
    embedder = EmbeddingModel(EMBEDDING_MODEL)

    vector_store = VectorStore(dim=384)
    vector_store.load(str(index_path), str(metadata_path))
    # vector_store.load("embeddings/faiss_index.bin", "embeddings/metadata.pkl")

    retriever = Retriever(vector_store, embedder, TOP_K)

    return retriever


def ask(query, retriever, reranker, filters=None):
    # Step 1: retrieve more candidates
    initial_contexts = retriever.retrieve(query, filters)

    # Step 2: re-rank them
    # contexts = reranker.rerank(query, initial_contexts, top_k=5)

    contexts = reranker.rerank(query, initial_contexts, top_k=3)

    prompt = build_prompt(query, contexts)
    answer = generate_answer(prompt)

    return answer, contexts


# if __name__ == "__main__":
#     build_index()