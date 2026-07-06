import time

from celery_app import celery_app


@celery_app.task
def hello_task():

    print("Task started...")

    time.sleep(10)

    print("Task completed!")

    return "Finished Successfully"


@celery_app.task
def process_pdf_task(file_paths):

    print(f"Task started: processing PDFs {file_paths}...")

    time.sleep(5)

    print(f"Task completed: processed PDFs {file_paths}!")

    return f"Processed {len(file_paths)} PDFs successfully"