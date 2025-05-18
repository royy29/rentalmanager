
from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "rental_manager",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)


celery_app.conf.update(
    task_track_started=True,
    task_time_limit=30,
    timezone='Asia/Kolkata',  # Adjust to your timezone
    enable_utc=True,
    beat_schedule={
        "send-return-reminders-every-morning": {
            "task": "app.celery_app.tasks.send_return_reminders",
            # "schedule": crontab(hour=8, minute=0),  # Every day at 8:00 AM
            "schedule": crontab(minute="*/5"),  # Every 5 minutes
        },
    }
)


celery_app.autodiscover_tasks(["app.celery_app"])
import app.celery_app.tasks

