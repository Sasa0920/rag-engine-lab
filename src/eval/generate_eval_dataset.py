import json

from src.rag.pipeline import initialize_rag
from src.rag.rag_service import rag_query

print("Initializing RAG pipeline...")

qa_chain = initialize_rag()

print("Pipeline ready.")


def load_questions():

    with open("data/questions.json", "r", encoding="utf-8") as f:
        return json.load(f)


def generate_dataset():

    questions = load_questions()

    dataset = []

    for item in questions:

        print(f"Generating answer for: {item['question']}")

        response = rag_query(
            qa_chain,
            item["question"]
        )

        dataset.append({
            "question": item["question"],
            "answer": response["answer"],
            "contexts": response["contexts"],
            "reference": item["reference"]
        })

    with open(
        "data/eval_dataset.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            dataset,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("Evaluation dataset created successfully.")


if __name__ == "__main__":
    generate_dataset()