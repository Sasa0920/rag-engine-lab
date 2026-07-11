import sqlite3
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "documents.db"

# Ensure folder exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            status TEXT NOT NULL,
            summary TEXT,
            uploaded_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def add_document(filename: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO documents (filename, status, summary, uploaded_at)
        VALUES (?, ?, ?, ?)
    """, (
        filename,
        "Pending",
        None,
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    doc_id = cursor.lastrowid
    conn.close()

    return doc_id

def update_status(doc_id: int, status: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE documents
        SET status = ?
        WHERE id = ?
    """, (status, doc_id))

    conn.commit()
    conn.close()

def save_summary(doc_id: int, summary: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE documents
        SET summary = ?
        WHERE id = ?
    """, (summary, doc_id))

    conn.commit()
    conn.close()

def get_document(doc_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, filename, status, summary, uploaded_at
        FROM documents
        WHERE id = ?
    """, (doc_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "filename": row[1],
        "status": row[2],
        "summary": row[3],
        "uploaded_at": row[4],
    }


def list_documents():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, filename, status, summary, uploaded_at
        FROM documents
        ORDER BY uploaded_at ASC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row[0],
            "filename": row[1],
            "status": row[2],
            "summary": row[3],
            "uploaded_at": row[4],
        }
        for row in rows
    ]


def clear_database():
    """Delete all rows from the documents table. Useful for resetting the DB during testing."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM documents")
    conn.commit()
    conn.close()