from src.agent.router import classify_intent
from src.rag.rag_service import rag_query, rag_query_stream
from src.rag.ollama_compat import get_chat_ollama


def _iter_answer_tokens(answer: str):
    if not answer:
        return []

    tokens = answer.split()
    return tokens if tokens else [answer]


def _stream_text(answer: str):
    for token in _iter_answer_tokens(answer):
        yield token


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


def run_agent_stream(question, qa_chain, summary=None):
    """
    Stream an answer using the agent's intent routing.
    """

    intent = classify_intent(question)

    if intent == "summary":
        answer = summary or "Summary is not available."
        yield from _stream_text(answer)
        return

    if intent == "rag":
        yield from rag_query_stream(qa_chain, question)
        return

    llm = get_chat_ollama(
        model="llama3"
    )

    from langchain_core.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_template(
        """
            You are a helpful AI assistant.

            Answer the user's question directly.

            Question:
            {question}

            Answer:
            """
    )

    messages = prompt.format_messages(
        question=question
    )

    for chunk in llm.stream(messages):
        text = getattr(chunk, "content", chunk)
        if text:
            yield text
