from langchain.chains import RetrievalQA
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
    result = qa_chain.invoke({"query": question})

    contexts = [
        doc.page_content for doc in result["source_documents"]
    ]

    return {
        "answer": result["result"],
        "contexts": contexts
    }