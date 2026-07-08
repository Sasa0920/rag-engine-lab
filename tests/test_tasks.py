from unittest.mock import patch

from tasks import generate_summary


def test_generate_summary_falls_back_when_llm_fails():
    with patch("tasks.get_chat_ollama", side_effect=RuntimeError("ollama unavailable")):
        summary = generate_summary(
            "This document explains machine learning and vector databases. "
            "It also covers retrieval-augmented generation."
        )

    assert isinstance(summary, str)
    assert summary.strip()
    assert "machine learning" in summary.lower()
