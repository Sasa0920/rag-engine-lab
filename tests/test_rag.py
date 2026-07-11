from qdrant_client.http import models as rest
from src.rag.retriever import create_retriever


class DummyVectorStore:
    def as_retriever(self, search_kwargs):
        return {"search_kwargs": search_kwargs}


def test_create_retriever_applies_document_filter():
    retriever = create_retriever(DummyVectorStore(), document_id=7)

    assert retriever["search_kwargs"]["k"] == 3
    assert isinstance(retriever["search_kwargs"]["filter"], rest.Filter)
    assert retriever["search_kwargs"]["filter"].must[0].key == "document_id"
    assert retriever["search_kwargs"]["filter"].must[0].match.value == 7