from django.conf import settings
from django.core.mail import send_mail
from django.template import loader

from core.celery import app
from domens.models import Domain
from settings.models import FormLogo
from styles.models.colors.colors import ColorStyles


@app.task()
def send_mail_to_confirm_email(url: str, user_email: str) -> None:
    logo = f"http://{Domain.objects.filter(is_partner=False).first().domain}" + FormLogo.objects.first().image.url
    main_color = ColorStyles.objects.first().main_color
    email = loader.render_to_string(
        "user/email_mail.html", {"logo": logo, "main_color": main_color, "link": url}, request=None, using=None
    )

    send_mail("Подтвердите почту", "", settings.EMAIL_HOST_USER, [user_email], html_message=email, fail_silently=False)


@app.task()
def send_mail_to_reset_password(url: str, user_email: str) -> None:
    send_mail("Перейдите по ссылке для сброса пароля", url, settings.EMAIL_HOST_USER, [user_email], fail_silently=False)
