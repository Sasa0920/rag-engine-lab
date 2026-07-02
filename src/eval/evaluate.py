import json
import os

from datasets import Dataset
from ragas import evaluate

from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision
)

from langchain_ollama import ChatOllama, OllamaEmbeddings


def load_data(path="data/eval_dataset.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_evaluation():

    #reduce concurrency (prevents Ollama timeout)
    os.environ["RAGAS_MAX_CONCURRENCY"] = "1"

    data = load_data()

    dataset = Dataset.from_dict({
        "question": [d["question"] for d in data],
        "answer": [d["answer"] for d in data],
        "contexts": [d["contexts"] for d in data],
        "reference": [d["reference"] for d in data]
    })

    #LLM judge (must be stable + deterministic)
    evaluator_llm = ChatOllama(
        model="llama3",
        temperature=0,
        num_predict=256
    )

    #Embeddings model (used internally by RAGAS)
    evaluator_embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    print("🚀 Running RAGAS evaluation...")

    result = evaluate(
        dataset,
        metrics=[
            faithfulness,
            #answer_relevancy,
            #context_precision
        ],
        llm=evaluator_llm,
        embeddings=evaluator_embeddings,
        raise_exceptions=False   
    )

    print("\n📊 RAG Evaluation Results:")
    print(result)


if __name__ == "__main__":
    run_evaluation()