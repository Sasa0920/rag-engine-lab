from src.agent.router import classify_intent
from src.rag.rag_service import rag_query
from src.rag.ollama_compat import get_chat_ollama


def run_agent(question, qa_chain, summary=None):
    """
    Decide which tool should answer the question.
    """

    intent = classify_intent(question)

    if intent == "summary":

        if summary:
            return {
                "intent": "summary",
                "answer": summary
            }

        return {
            "intent": "summary",
            "answer": "Summary is not available."
        }

    if intent == "rag":

        result = rag_query(
            qa_chain,
            question
        )

        return {
            "intent": "rag",
            "answer": result["answer"]
        }

    llm = get_chat_ollama(
        model="llama3"
    )

    response = llm.invoke(question)

    return {
        "intent": "general",
        "answer": response.content
    }