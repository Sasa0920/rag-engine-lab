import json
import shutil
from pathlib import Path
from typing import List

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.responses import StreamingResponse

from database import (
    init_db,
    add_document,
    get_document,
    list_documents,
    clear_database,
)

from tasks import process_pdf_task

from src.rag.pipeline import initialize_rag
from src.rag.rag_service import rag_query_stream

from src.agent.agent import run_agent

app = FastAPI(
    title="DocuMind AI",
    version="1.0",
    docs_url="/docs"
)

UPLOAD_FOLDER = Path(__file__).parent / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)

init_db()


def custom_openapi():

    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

    components = openapi_schema.get(
        "components",
        {}
    ).get(
        "schemas",
        {}
    )

    for component in components.values():

        if "properties" not in component:
            continue

        for prop in component["properties"].values():

            if prop.get("contentMediaType") == "application/octet-stream":
                prop["format"] = "binary"
                prop.pop("contentMediaType", None)

            elif prop.get("type") == "array":

                items = prop.get("items", {})

                if items.get("contentMediaType") == "application/octet-stream":

                    items["format"] = "binary"
                    items.pop("contentMediaType", None)

    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/")
def home():

    return {
        "message": "DocuMind AI Backend Running 🚀"
    }


@app.post("/upload")
async def upload_files(
    files: List[UploadFile] = File(...)
):

    tasks = []

    for file in files:

        if not file.filename.lower().endswith(".pdf"):
            continue

        file_path = UPLOAD_FOLDER / file.filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        doc_id = add_document(file.filename)

        task = process_pdf_task.delay(
            doc_id,
            str(file_path)
        )

        tasks.append(
            {
                "document_id": doc_id,
                "task_id": task.id,
                "filename": file.filename,
            }
        )

    if not tasks:

        raise HTTPException(
            status_code=400,
            detail="No valid PDF files uploaded."
        )

    return {
        "message": "Upload successful",
        "tasks": tasks,
    }


@app.get("/query")
def query(
    q: str,
    document_id: int
):

    try:

        qa_chain, _ = initialize_rag(
            document_id=document_id
        )

    except Exception as exc:

        raise HTTPException(
            status_code=503,
            detail=f"Failed to initialize RAG: {exc}"
        )

    document = get_document(document_id)

    summary = None

    if document:
        summary = document["summary"]

    result = run_agent(
        question=q,
        qa_chain=qa_chain,
        summary=summary
    )

    return result


@app.get("/query/stream")
def query_stream(
    q: str,
    document_id: int
):

    try:

        qa_chain, _ = initialize_rag(
            document_id=document_id
        )

    except Exception as exc:

        raise HTTPException(
            status_code=503,
            detail=f"Failed to initialize RAG: {exc}"
        )

    def event_stream():

        for token in rag_query_stream(
            qa_chain,
            q,
            document_id=document_id
        ):

            yield (
                f"data: {json.dumps({'token': token})}\n\n"
            )

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream"
    )


@app.post("/reset-db")
def reset_db():

    clear_database()

    for file_path in UPLOAD_FOLDER.glob("*.pdf"):

        try:
            file_path.unlink()
        except Exception:
            pass

    return {
        "message": "Database cleared and uploads removed"
    }


@app.get("/documents")
def documents():

    return {
        "documents": list_documents()
    }


@app.get("/document/{doc_id}")
def get_doc(doc_id: int):

    doc = get_document(doc_id)

    if not doc:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return doc