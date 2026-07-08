import re
from celery_app import celery_app
from database import update_status, save_summary
from src.ingest.loader import load_document
from src.ingest.ingestion_service import split_documents
from src.rag.embeddings import get_embedding_model
from src.rag.vectorstore import build_vectorstore
from src.rag.retriever import create_retriever
from src.rag.ollama_compat import get_chat_ollama


def _fallback_summary(text: str) -> str:
    cleaned = re.sub(r"\s+", " ", text or "").strip()

    if not cleaned:
        return "No text content was available to summarize."

    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", cleaned) if s.strip()]
    if sentences:
        summary = " ".join(sentences[:2])
    else:
        summary = cleaned

    if len(summary) > 400:
        summary = summary[:397].rsplit(" ", 1)[0] + "..."

    return summary


def generate_summary(text: str):
    if not text or not text.strip():
        return "No text content was available to summarize."

    try:
        llm = get_chat_ollama(model="llama3")
        prompt = f"""
        Summarize the following document in a clear and concise way:
        {text}
        """
        response = llm.invoke(prompt)
        if hasattr(response, "content") and response.content:
            return response.content
    except Exception as exc:
        print(f"LLM summary generation failed: {exc}")

    return _fallback_summary(text)

@celery_app.task
def process_pdf_task(document_id, file_path):
    try:
        print("Processing:", file_path)
        update_status(document_id, "Processing")

        # 1. Load
        docs = load_document(file_path)
        # 2. Chunk
        chunks = split_documents(docs)
        # 3. Embeddings
        embeddings = get_embedding_model()
        # 4. Vector DB
        vectorstore = build_vectorstore(chunks, embeddings)
        # 5. Retriever
        retriever = create_retriever(vectorstore)
        # 6. Summary
        full_text = "\n".join([d.page_content for d in docs])
        summary = generate_summary(full_text)
        # 7. Save summary
        save_summary(document_id, summary)
        # 8. Done
        update_status(document_id, "Completed")

        print("Completed:", file_path)

        return {
            "document_id": document_id,
            "status": "Completed"
        }

    except Exception as e:
        update_status(document_id, "Failed")
        return {"error": str(e)}