from pathlib import Path

from src.ingest.loader import load_document
from src.ingest.ingestion_service import split_documents
from src.rag.embeddings import get_embedding_model
from src.rag.vectorstore import build_vectorstore
from src.rag.retriever import create_retriever
from src.rag.rag_service import build_rag_chain


def initialize_rag():
    uploads_dir = Path("uploads")
    documents = []

    if uploads_dir.exists():
        for file_path in uploads_dir.glob("*.pdf"):
            documents.extend(load_document(str(file_path)))

    if not documents:
        documents = load_document("data/document.txt")

    # chunking
    docs = split_documents(documents)

    # embeddings
    embeddings = get_embedding_model()

    # vector DB
    vectorstore = build_vectorstore(docs, embeddings)

    # retriever
    retriever = create_retriever(vectorstore)

    # RAG chain
    qa_chain = build_rag_chain(retriever)

    return qa_chain, docs