def classify_intent(question: str) -> str:
    """
    Classify the user's intent.

    Returns:
        summary
        rag
        general
    """

    q = question.lower()

    # Summary-related questions
    summary_keywords = [
        "summary",
        "summarize",
        "overview",
        "brief",
        "abstract"
    ]

    # Document-related questions
    rag_keywords = [
        "document",
        "pdf",
        "project",
        "chapter",
        "section",
        "page",
        "objective",
        "architecture",
        "technology",
        "requirement",
        "explain",
        "what is",
        "who",
        "where",
        "when",
        "why",
        "how"
    ]

    if any(keyword in q for keyword in summary_keywords):
        return "summary"

    if any(keyword in q for keyword in rag_keywords):
        return "rag"

    return "general"