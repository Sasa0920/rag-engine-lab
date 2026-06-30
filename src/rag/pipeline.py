from src.ingest.loader import load_document
from src.ingest.ingestion_service import split_documents
from src.rag.embeddings import get_embedding_model
from src.rag.vectorstore import build_vectorstore
from src.rag.retriever import create_retriever
from src.rag.rag_service import build_rag_chain

def initialize_rag():

    documents = load_document("data/document.txt")
    docs = split_documents(documents)

    embeddings = get_embedding_model()

    vectorstore = build_vectorstore(docs, embeddings)

    retriever = create_retriever(vectorstore)

    qa_chain = build_rag_chain(retriever)

    return qa_chain