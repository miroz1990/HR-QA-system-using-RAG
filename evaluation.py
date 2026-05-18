import json
from src.rag_pipeline import load_pipeline, ask
from src.llm_evaluator import evaluate_with_llm
from src.reranker import Reranker

def evaluate():
    retriever = load_pipeline()
    reranker = Reranker()  # Initialize the reranker

    with open("evaluation.json", "r") as f:
        data = json.load(f)

    results = []

    for item in data:
        question = item["question"]
        reference = item["reference_answer"]

        answer, contexts = ask(question, retriever, reranker)

        context_text = "\n".join([c["text"] for c in contexts])

        eval_result = evaluate_with_llm(
            question,
            answer,
            reference,
            context_text
        )

        results.append(eval_result)

        print("\nQuestion:", question)
        print("Answer:", answer)
        print("Evaluation:", eval_result)
        print("-" * 50)

    # Aggregate scores
    avg_correctness = sum(r["correctness"] for r in results) / len(results)
    avg_grounding = sum(r["grounding"] for r in results) / len(results)
    avg_relevance = sum(r["relevance"] for r in results) / len(results)

    print("\n📊 Final Scores:")
    print(f"Correctness: {avg_correctness:.2f}")
    print(f"Grounding: {avg_grounding:.2f}")
    print(f"Relevance: {avg_relevance:.2f}")


if __name__ == "__main__":
    evaluate()