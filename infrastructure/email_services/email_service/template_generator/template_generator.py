from typing import Any

from django.template import loader

from domain.user.user import UserInterface
from infrastructure.email_services.email_service.context_processor.context_processor_interface import (
    EmailContextProcessorInterface,
)

from .template_generator_interface import EmailTemplateGeneratorInterface


class EmailTemplateGenerator(EmailTemplateGeneratorInterface):
    def __init__(self, context_processor: EmailContextProcessorInterface) -> None:
        self.context_processor = context_processor

    @staticmethod
    def generate_template(template_name: str, context: dict[Any, Any]) -> str:
        return loader.render_to_string(template_name, context, request=None, using=None)

    def generate_confirm_email_template(self, user: UserInterface) -> str:
        context = self.context_processor.confirm_email(user)

        return self.generate_template("emails/confirm_email.html", context)

    def generate_confirm_new_email_template(self, user: UserInterface) -> str:
        context = self.context_processor.confirm_new_email(user)

        return self.generate_template("emails/confirm_new_email.html", context)

    def generate_reset_password_template(self, user: UserInterface) -> str:
        context = self.context_processor.reset_password(user)

        return self.generate_template("emails/reset_password.html", context)

    def generate_success_login_in_admin_template(self, **kwargs) -> str:
        context = self.context_processor.try_login_in_admin(**kwargs)

        return self.generate_template("emails/success_login_in_admin.html", context)

    def generate_cant_login_in_admin_template(self, **kwargs) -> str:
        context = self.context_processor.try_login_in_admin(**kwargs)

        return self.generate_template("emails/error_login_in_admin.html", context)

    def generate_login_in_fake_admin(self, **kwargs) -> str:
        context = self.context_processor.login_in_fake_admin(**kwargs)

        return self.generate_template("emails/login_in_fake_admin.html", context)


def get_email_template_generator(email_context_processor: EmailContextProcessorInterface) -> EmailTemplateGenerator:
    return EmailTemplateGenerator(email_context_processor)
