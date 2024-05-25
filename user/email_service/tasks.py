from django.conf import settings
from django.core.mail import send_mail

from core.celery import app


@app.task()
def send_mail_to_confirm_email(url: str, user_email: str) -> None:
    send_mail("Подтвердите почту", url, settings.EMAIL_HOST_USER, [user_email], fail_silently=False)


@app.task()
def send_mail_to_reset_password(url: str, user_email: str) -> None:
    send_mail("Перейдите по ссылке для сброса пароля", url, settings.EMAIL_HOST_USER, [user_email], fail_silently=False)
