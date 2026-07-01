import json

from ragas import evaluate
from datasets import Dataset

from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision
)

from langchain_ollama import ChatOllama


# Load dataset
def load_data(path="data/eval_dataset.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_evaluation():

    data = load_data()

    # Convert to HuggingFace Dataset format
    dataset = Dataset.from_dict({
    "question": [d["question"] for d in data],
    "answer": [d["answer"] for d in data],
    "contexts": [d["contexts"] for d in data],
    "reference": [d["reference"] for d in data]
})

    # LLM evaluator (used by RAGAS internally)
    evaluator_llm = ChatOllama(
        model="llama3"
    )

    # Run evaluation
    result = evaluate(
        dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision
        ],
        llm=evaluator_llm
    )

    print("\n📊 RAG Evaluation Results:")
    print(result)


if __name__ == "__main__":
    run_evaluation()