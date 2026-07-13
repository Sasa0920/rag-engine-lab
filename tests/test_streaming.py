from src.agent.agent import run_agent_stream
from src.rag.rag_service import rag_query_stream


class FakeChain:
    def invoke(self, payload):
        return {
            "result": "Hello world",
            "source_documents": [],
        }


class StreamingChain:
    def __init__(self, text):
        self.text = text

    def invoke(self, payload):
        return {
            "result": self.text,
            "source_documents": []
        }


class FakeLLM:
    def stream(self, messages):
        for word in ["This", "is", "general"]:
            yield type("Chunk", (), {"content": word})


def test_rag_query_stream_falls_back_to_invoke():
    chunks = list(rag_query_stream(FakeChain(), "What is this?"))

    assert chunks == ["Hello", "world"]


def test_run_agent_stream_summary_intent():
    summary = "This is the stored document summary."
    chunks = list(run_agent_stream("Give me a summary", None, summary=summary))

    assert chunks == summary.split()


# Note: live LLM streaming is not mocked fully in this test environment
# but this ensures the summary branch works and the API can route to stream.
