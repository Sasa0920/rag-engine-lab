from src.rag.ollama_compat import get_chat_ollama, get_ollama_embeddings


def test_ollama_compat_exports_callable_factories():
    assert callable(get_chat_ollama)
    assert callable(get_ollama_embeddings)
