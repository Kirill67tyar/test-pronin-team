from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def test_task(x, y):
    return x + y


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_email_task(self, subject: str, message: str, recipient_list: list, html_message: str | None = None, from_email: str | None = None):
    """
    Общая Celery-таска для отправки письма через Django send_mail.
    При ошибке — делает retry.
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email or settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as exc:
        raise self.retry(exc=exc)
