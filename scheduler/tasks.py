from celery import Celery, schedules
from scheduler.worker import send_email_on_expense, create_and_send_weekly_emails
import settings

celery = Celery(
    "tasks",
    broker=settings.CELERY_BORKER_URL,
    backend=settings.CELERY_BACKEND_URL,
    include=["scheduler.tasks"],
    broker_connection_retry=True)


celery.conf.beat_schedule = {
    'send-weekly-emails': {
        'task': 'tasks.send_weekly_emails',
        'schedule': schedules.crontab(day_of_week='monday', hour=0, minute=0),
    },
}

@celery.task
def send_email(expense_id: str):
    """
    The function `send_email` sends an email notification for any expense added.
    """
    send_email_on_expense(expense_id)



@celery.task
def send_weekly_emails():
    """
    The function `send_weekly_emails` is responsible for creating and sending weekly emails.
    """
    create_and_send_weekly_emails()
    