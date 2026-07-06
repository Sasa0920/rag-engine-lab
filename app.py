from pathlib import Path
import shutil
from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.openapi.utils import get_openapi
from tasks import process_pdf_task
from src.rag.pipeline import initialize_rag
from src.rag.rag_service import rag_query

app = FastAPI(
    title="DocuMind AI",
    version="1.0",
    docs_url="/docs"
)

UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)

# Safe initialization of RAG pipeline to prevent startup crash if Ollama is not running
qa_chain = None
try:
    qa_chain, _ = initialize_rag()
    print("RAG pipeline initialized successfully.")
except Exception as e:
    print(f"Warning: RAG initialization failed: {e}. /query endpoint will be unavailable.")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )
    
    # Patch the schema to replace contentMediaType with format: binary so Swagger UI shows a file picker
    for component in openapi_schema.get("components", {}).get("schemas", {}).values():
        if "properties" in component:
            for prop in component["properties"].values():
                if prop.get("contentMediaType") == "application/octet-stream":
                    prop["format"] = "binary"
                    prop.pop("contentMediaType", None)
                elif prop.get("type") == "array" and "items" in prop:
                    items = prop["items"]
                    if items.get("contentMediaType") == "application/octet-stream":
                        items["format"] = "binary"
                        items.pop("contentMediaType", None)
                    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


@app.get("/")
def home():
    return {
        "message": "DocuMind AI Backend Running"
    }


@app.post("/upload")
async def upload_files(
    files: List[UploadFile] = File(...)
):
    saved_files = []

    for file in files:
        # Accept only PDFs
        if not file.filename.lower().endswith(".pdf"):
            continue

        destination = UPLOAD_FOLDER / file.filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        saved_files.append(str(destination))

    if not saved_files:
        raise HTTPException(status_code=400, detail="No valid PDF files uploaded")

    # Queue the Celery task
    task = process_pdf_task.delay(saved_files)

    return {
        "task_id": task.id
    }


@app.get("/query")
def query(q: str):
    if qa_chain is None:
        raise HTTPException(
            status_code=503,
            detail="RAG system is not initialized. Please ensure Ollama is running and models are pulled."
        )

    answer = rag_query(qa_chain, q)
    return {"answer": answer}