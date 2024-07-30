from django.conf import settings
from django.core.mail import send_mail
from django.template import loader

from core.celery import app


@app.task()
def send_mail_to_confirm_email(url: str, user_email: str) -> None:
    from emails.serializers import EmailLogoSerializer
    from settings.models import FormLogo
    from styles.models.colors.colors import ColorStyles

    logo = FormLogo.objects.only("image", "width", "height").first()
    logo = EmailLogoSerializer(logo).data

    main_color = ColorStyles.objects.values_list("main_color").first()[0]
    email = loader.render_to_string(
        "emails/confirm_email.html", {"logo": logo, "main_color": main_color, "link": url}, request=None, using=None
    )

    send_mail(
        "Подтвердите свой email адрес",
        "",
        f"BankoMag <{settings.EMAIL_HOST_USER}>",
        [user_email],
        html_message=email,
        fail_silently=False,
    )


@app.task()
def send_mail_to_reset_password(url: str, user_email: str) -> None:
    send_mail("Перейдите по ссылке для сброса пароля", url, settings.EMAIL_HOST_USER, [user_email], fail_silently=False)
