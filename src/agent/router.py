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
        "abstract",
        "key points",
        "takeaway",
        "recap"
    ]

    # Document-related questions
    rag_keywords = [
        "document",
        "pdf",
        "uploaded",
        "file",
        "chapter",
        "section",
        "page",
        "source",
        "filename",
        "document_id",
        "paragraph",
        "report",
        "proposal",
        "agreement",
        "manual",
        "specification",
        "architecture",
        "technology",
        "requirements",
        "objective",
        "project",
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