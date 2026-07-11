from langchain.chains import RetrievalQA
from langchain_core.prompts import ChatPromptTemplate
from src.rag.ollama_compat import get_chat_ollama


def build_rag_chain(retriever):

    llm = get_chat_ollama(
        model="llama3"
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )


def rag_query(qa_chain, question: str):

    result = qa_chain.invoke(
        {
            "query": question
        }
    )

    contexts = [
        doc.page_content
        for doc in result["source_documents"]
    ]

    return {
        "answer": result["result"],
        "contexts": contexts
    }


def rag_query_stream(qa_chain, question: str):

    # Retrieve relevant documents
    docs = qa_chain.retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    llm = get_chat_ollama(
        model="llama3"
    )

    prompt = ChatPromptTemplate.from_template(
        """
            You are a helpful AI assistant.

            Answer ONLY using the context below.

            If the answer cannot be found in the context,
            say you don't know.

            Context:
            {context}

            Question:
            {question}

            Answer:
            """
    )

    messages = prompt.format_messages(
        context=context,
        question=question
    )

    # Stream tokens directly from Ollama
    for chunk in llm.stream(messages):

        if hasattr(chunk, "content"):

            text = chunk.content

            if text:
                yield text