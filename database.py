from pathlib import Path
import sqlite3
from datetime import datetime

DB_PATH = Path("database/documents.db")
DB_PATH.parent.mkdir(exist_ok=True)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS documents(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        filename TEXT NOT NULL,

        status TEXT NOT NULL,

        summary TEXT,

        uploaded_at TEXT NOT NULL

    )
    """)

    conn.commit()

    conn.close()


def add_document(filename):

    conn = get_connection()

    cursor = conn.execute(

        """
        INSERT INTO documents
        (filename,status,uploaded_at)

        VALUES(?,?,?)
        """,

        (

            filename,

            "Pending",

            datetime.utcnow().isoformat()

        )

    )

    conn.commit()

    document_id = cursor.lastrowid

    conn.close()

    return document_id


def update_status(document_id, status):

    conn = get_connection()

    conn.execute(

        """

        UPDATE documents

        SET status=?

        WHERE id=?

        """,

        (

            status,

            document_id

        )

    )

    conn.commit()

    conn.close()