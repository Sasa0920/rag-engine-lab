from src.rag.pipeline import initialize_rag

qa_chain, docs = initialize_rag()
print("RAG ready")
print(f"[INFO] Chunks created: {len(docs)}")