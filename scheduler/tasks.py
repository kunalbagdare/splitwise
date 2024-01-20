from celery import Celery, schedules
from scheduler.worker import send_email_on_expense
import settings

celery = Celery(
    "tasks",
    broker=settings.CELERY_BORKER_URL,
    backend=settings.CELERY_BACKEND_URL,
    include=["scheduler.tasks"],
    broker_connection_retry_on_startup=True)


@celery.task
def send_email(expense_id: str):
    """
    The function `send_email` sends an email notification for any expense added.
    """
    send_email_on_expense(expense_id)