from src.rag_pipeline import build_index, load_pipeline, ask
from src.reranker import Reranker
from src.retriever import Retriever
import os

reranker = Reranker()

def auto_filter_query(query):
    query = query.lower()

    if any(word in query for word in ["leave", "vacation", "days off"]):
        return {"role": "employee", "doc_type": "leave_policy"}

    if any(word in query for word in ["security", "data", "password"]):
        return {"doc_type": "it_security_policy"}

    if any(word in query for word in ["harassment", "behavior", "conduct"]):
        return {"doc_type": "code_of_conduct"}

    return None


def run_examples(retriever):
    print("\n--- Employee Question ---")
    answer, _ = ask(
        "How many leave days do I get?",
        retriever,
        reranker,
        filters={"role": "employee", "doc_type": "leave_policy"}
    )
    print(answer)

    print("\n--- Security Question ---")
    answer, _ = ask(
    "What happens if I share company data?",
    retriever,
    reranker,
    filters={"role": "employee", "doc_type": "it_security_policy"}
    )
    print(answer)


def main():
    if not os.path.exists("embeddings/faiss_index.bin"):
        print("🔹 Building index (first time only)...")
        build_index()
    else:
        print("✅ Using existing index...")

    retriever = load_pipeline()

    # Optional: run test queries
    run_examples(retriever)

    print("\n💬 HR Assistant Ready! Type 'exit' to quit.\n")

    while True:
        query = input("You: ")

        if query.lower() == "exit":
            break

        filters = auto_filter_query(query)

        answer, contexts = ask(query, retriever, reranker, filters)

        if not contexts:
            print("\n⚠️ No relevant documents found.")
            continue

        print("\n🤖 Answer:")
        print(answer)

        print("\n📚 Sources:")
        for c in contexts:
            print(f"- {c['source']} (section: {c.get('section', 'N/A')})")

        print("\n" + "-" * 50)


if __name__ == "__main__":
    main()