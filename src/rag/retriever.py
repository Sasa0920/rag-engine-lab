from qdrant_client.http import models as rest


def create_retriever(vectorstore, document_id=None):
    search_kwargs = {"k": 3}
    if document_id is not None:
        search_kwargs["filter"] = rest.Filter(
            must=[
                rest.FieldCondition(
                    key="document_id",
                    match=rest.MatchValue(value=document_id),
                )
            ]
        )

    return vectorstore.as_retriever(
        search_kwargs=search_kwargs
    )