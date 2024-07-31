from emails.email_service.email_service_interface import EmailServiceInterface
from emails.email_service.tasks import (
    send_email
)
from django.conf import settings
from emails.email_service.link_generator.link_generator_interface import LinkGeneratorInterface
from django.template import loader
from emails.serializers import EmailLogoSerializer
from settings.models import FormLogo
from styles.models.colors.colors import ColorStyles
from typing import Any


class EmailService(EmailServiceInterface):
    sender: str = f"BankoMag <{settings.EMAIL_HOST_USER}>"

    def __init__(self, template_generator) -> None:
        self.template_generator = template_generator

    def send_mail_to_confirm_email(self, user) -> None:
        template = self.template_generator.generate_confirm_email_template(user)
        send_email.delay(
            "Подтвердите свой email адрес",
            self.sender,
            [user.email],
            template
        )

    def send_mail_to_reset_password(self, user) -> None:
        template = self.template_generator.generate_reset_password_template(user)
        send_email.delay(
            "Восстановление пароля",
            self.sender,
            [user.email],
            template
        )


class EmailTemplateGenerator:
    def __init__(self, context_processor) -> None:
        self.context_processor = context_processor

    def generate_template(template_name: str, context: dict[Any: Any]):
        return loader.render_to_string(
            template_name, context, request=None, using=None
        )

    def generate_confirm_email_template(self, user):
        context = self.context_processor.confirm_email(user)

        return self.generate_template("emails/confirm_email.html", context)

    def generate_reset_password_template(self, user):
        context = self.context_processor.reset_password(user)

        return self.generate_template("emails/reset_password.html", context)


class EmailContextProcessor:
    def __init__(self, link_generator):
        self.link_generator = link_generator

    def get_context() -> dict[Any: Any]:
        logo = FormLogo.objects.only("image", "width", "height").first()
        logo = EmailLogoSerializer(logo).data
        main_color = ColorStyles.objects.values_list("main_color").first()[0]

        return {
            "logo": logo,
            "main_color": main_color
        }

    def confirm_email(self, user):
        context = self.get_context()
        context["link"] = self.link_generator.get_url_to_confirm_email(user.id)

        return context

    def reset_password(self, user):
        context = self.get_context()
        context["link"] = self.link_generator.get_url_to_reset_password(user.id)
        context["user"] = user

        return context

def get_email_service(link_generator: LinkGeneratorInterface) -> EmailService:
    return EmailService(link_generator)
