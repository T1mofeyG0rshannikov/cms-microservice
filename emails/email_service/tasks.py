from django.core.mail import send_mail
from django.template import loader

from core.celery import app


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

@app.task()
def send_mail_to_confirm_email(url: str, sender: str, user_email: str) -> None:
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
        sender,
        [user_email],
        html_message=email,
        fail_silently=False,
    )


@app.task()
def send_mail_to_reset_password(url: str, sender: str, user_email: str) -> None:
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
        "Восстановление пароля",
        "",
        sender,
        [user_email],
        html_message=email,
        fail_silently=False
    )
