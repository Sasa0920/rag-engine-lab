from fastapi import FastAPI
from src.rag.pipeline import initialize_rag
from src.rag.rag_service import rag_query

app = FastAPI()

qa_chain = initialize_rag()

@app.get("/query")
def query(q: str):

    answer = rag_query(qa_chain, q)

    return {"answer": answer}