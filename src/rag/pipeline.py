from pathlib import Path

from database import list_documents
from src.ingest.loader import load_document
from src.ingest.ingestion_service import split_documents
from src.rag.embeddings import get_embedding_model
from src.rag.vectorstore import build_vectorstore
from src.rag.retriever import create_retriever
from src.rag.rag_service import build_rag_chain


def _load_documents_for_rag(document_id=None):
    uploads_dir = Path(__file__).resolve().parents[2] / "uploads"
    documents = []

    known_documents = {doc["filename"]: doc["id"] for doc in list_documents()}

    if uploads_dir.exists():
        for file_path in sorted(uploads_dir.glob("*.pdf")):
            doc_id = known_documents.get(file_path.name)

            if document_id is not None and doc_id != document_id:
                continue

            loaded_docs = load_document(str(file_path))
            for doc in loaded_docs:
                metadata = dict(doc.metadata or {})
                metadata["source"] = str(file_path)
                metadata["filename"] = file_path.name
                metadata["document_id"] = doc_id
                doc.metadata = metadata

            documents.extend(loaded_docs)

    if not documents:
        fallback_docs = load_document("data/document.txt")
        if fallback_docs:
            for doc in fallback_docs:
                metadata = dict(doc.metadata or {})
                metadata["source"] = "data/document.txt"
                metadata["filename"] = "document.txt"
                metadata["document_id"] = None
                doc.metadata = metadata
            documents.extend(fallback_docs)

    return documents


def initialize_rag(document_id=None):
    documents = _load_documents_for_rag(document_id=document_id)

    # chunking
    docs = split_documents(documents)

    # embeddings
    embeddings = get_embedding_model()

    # vector DB
    vectorstore = build_vectorstore(docs, embeddings)

    # retriever
    retriever = create_retriever(vectorstore, document_id=document_id)

    # RAG chain
    qa_chain = build_rag_chain(retriever)

    return qa_chain, docs