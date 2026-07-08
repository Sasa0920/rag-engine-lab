from src.rag.ollama_compat import get_ollama_embeddings


def get_embedding_model():
    # Use Ollama embeddings if available; otherwise HuggingFace embeddings.
    try:
        return get_ollama_embeddings(model="nomic-embed-text")
    except Exception:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )