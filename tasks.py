import time
from celery_app import celery_app
from database import update_status
import logging

logger = logging.getLogger(__name__)


@celery_app.task

def process_pdf_task(
    document_id,
    file_path
):

    print()
    print("=" * 50)
    logger.info("Worker started")
    print(file_path)
    print("=" * 50)
    update_status(
        document_id,
        "Processing"
    )

    time.sleep(5)
    update_status(
        document_id,
        "Completed"
    )

    print()
    print("=" * 50)
    logger.info("Worker finished")
    print(file_path)
    print("=" * 50)
    return {

        "document_id": document_id,
        "status": "Completed"

    }