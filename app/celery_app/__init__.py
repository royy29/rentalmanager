
from celery import Celery

celery_app = Celery(
    "rental_manager",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.update(task_track_started=True, task_time_limit=30)

celery_app.autodiscover_tasks(["app.celery_app"])
