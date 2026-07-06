from pathlib import Path
import shutil
from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.openapi.utils import get_openapi
from database import init_db, add_document
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

# Initialize database
init_db()
# Initialize RAG pipeline
qa_chain = None

try:
    qa_chain, _ = initialize_rag()
    print("RAG pipeline initialized successfully.")

except Exception as e:
    print(f"Warning: RAG initialization failed: {e}")
    print("The /query endpoint will not work until Ollama is running.")

def custom_openapi():

    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

    components = openapi_schema.get("components", {}).get("schemas", {})

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
        "message": "DocuMind AI Backend Running"
    }

@app.post("/upload")
async def upload_files(
    files: List[UploadFile] = File(...)
):

    tasks = []

    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            continue
        destination = UPLOAD_FOLDER / file.filename
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Save document metadata in SQLite
        document_id = add_document(file.filename)

        # Send task to RabbitMQ
        task = process_pdf_task.delay(
            document_id,
            str(destination)
        )

        tasks.append(
            {
                "document_id": document_id,
                "task_id": task.id,
                "filename": file.filename
            }
        )

    if len(tasks) == 0:
        raise HTTPException(
            status_code=400,
            detail="No valid PDF files uploaded."
        )

    return {

        "message": "Upload successful",
        "tasks": tasks
    }

@app.get("/query")
def query(q: str):

    if qa_chain is None:
        raise HTTPException(
            status_code=503,
            detail="RAG system is not initialized. Please ensure Ollama is running."
        )

    answer = rag_query(
        qa_chain,
        q
    )

    return {
        "answer": answer
    }