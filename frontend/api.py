import requests

BASE_URL = "http://127.0.0.1:8000"

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

def ask_question(question: str):
 
    response = requests.get(
        f"{BASE_URL}/query",
        params={
            "q": question
        }
    )

    response.raise_for_status()

    return response.json()

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