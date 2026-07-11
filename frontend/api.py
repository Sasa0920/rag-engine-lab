import os
from pathlib import Path
import requests
import json

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
BACKEND_URL_FILE = WORKSPACE_ROOT / ".backend_url"


def resolve_backend_url():
    if os.getenv("BACKEND_URL"):
        return os.getenv("BACKEND_URL")

    if BACKEND_URL_FILE.exists():
        return BACKEND_URL_FILE.read_text(encoding="utf-8").strip()

    return "http://127.0.0.1:8000"


BASE_URL = resolve_backend_url()

def upload_pdf(file):
 
    files = {
        "files": (
            file.name,
            file.getvalue(),
            "application/pdf"
        )
    }

    response = requests.post(
        f"{BASE_URL}/upload",
        files=files
    )

    response.raise_for_status()

    return response.json()

def ask_question(question: str, document_id: int | None = None):
 
    params = {
        "q": question
    }

    if document_id is not None:
        params["document_id"] = document_id

    response = requests.get(
        f"{BASE_URL}/query",
        params=params
    )

    response.raise_for_status()

    return response.json()


def stream_answer(question: str, document_id: int | None = None):

    try:
        fallback = ask_question(question, document_id=document_id)
        answer = fallback.get("answer", "")
    except Exception:
        answer = "I couldn't generate a response right now."

    if answer:
        yield answer
    else:
        yield "I couldn't generate a response right now."


def list_documents():

    response = requests.get(
        f"{BASE_URL}/documents"
    )

    response.raise_for_status()

    return response.json()["documents"]


def get_document(document_id: int):
   
    response = requests.get(
        f"{BASE_URL}/document/{document_id}"
    )

    response.raise_for_status()

    return response.json()

def check_backend():
   
    try:
        response = requests.get(
            f"{BASE_URL}/",
            timeout=3
        )

        return response.status_code == 200

    except requests.exceptions.RequestException:
        return False