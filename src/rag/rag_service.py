from langchain_ollama import ChatOllama
from langchain_classic.chains.retrieval_qa.base import RetrievalQA


def build_rag_chain(retriever):

    llm = ChatOllama(
        model="llama3"
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )


def rag_query(qa_chain, question):

    result = qa_chain.invoke(
        {"query": question}
    )

    contexts = [
        doc.page_content
        for doc in result["source_documents"]
    ]

    return {
        "answer": result["result"],
        "contexts": contexts
    }