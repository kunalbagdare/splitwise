from celery import Celery, schedules
from scheduler.worker import send_email_on_expense

celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["scheduler.tasks"],
    broker_connection_retry_on_startup=True)


@celery.task
def send_email(expense_id: str):
    send_email_on_expense(expense_id)