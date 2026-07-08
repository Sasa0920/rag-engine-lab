"""Compatibility layer for Ollama integrations across LangChain versions."""

try:
    from langchain_ollama import ChatOllama as ChatOllama
    from langchain_ollama import OllamaEmbeddings as OllamaEmbeddings
except Exception:
    from langchain_community.chat_models import ChatOllama as ChatOllama
    from langchain_community.embeddings import OllamaEmbeddings as OllamaEmbeddings


def get_chat_ollama(*args, **kwargs):
    return ChatOllama(*args, **kwargs)


def get_ollama_embeddings(*args, **kwargs):
    return OllamaEmbeddings(*args, **kwargs)
