from src.rag.rag_service import rag_query_stream


class FakeChain:
    def invoke(self, payload):
        return {
            "result": "Hello world",
            "source_documents": [],
        }


def test_rag_query_stream_falls_back_to_invoke():
    chunks = list(rag_query_stream(FakeChain(), "What is this?"))

    assert chunks == ["Hello", "world"]
