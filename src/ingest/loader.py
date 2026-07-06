from langchain_core.documents import Document
from pathlib import Path
from pypdf import PdfReader

def load_document(file_path):
    path = Path(file_path)
    if path.suffix.lower() == ".pdf":
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return [
            Document(
                page_content=text,
                metadata={"source": str(file_path)}
            )
        ]
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        return [
            Document(
                page_content=text,
                metadata={"source": str(file_path)}
            )
        ]