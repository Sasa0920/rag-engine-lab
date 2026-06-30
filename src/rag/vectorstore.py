from langchain_qdrant import QdrantVectorStore

def build_vectorstore(docs, embeddings):

    return QdrantVectorStore.from_documents(
        documents=docs,
        embedding=embeddings,
        location=":memory:",
        collection_name="demo"
    )