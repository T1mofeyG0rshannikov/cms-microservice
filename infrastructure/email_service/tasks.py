from django.core.mail import send_mail

from web.core.celery import app


@app.task()
def send_email(subj: str, sender: str, emails: list[str], html_message: str):
    send_mail(
        subj,
        "",
        sender,
        emails,
        html_message=html_message,
        fail_silently=False,
    )
