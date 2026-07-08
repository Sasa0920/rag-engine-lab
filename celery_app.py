from celery import Celery

celery_app = Celery(
    "documind",
    broker="amqp://guest:guest@localhost:5672//",
    backend="rpc://",
    include=["tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)