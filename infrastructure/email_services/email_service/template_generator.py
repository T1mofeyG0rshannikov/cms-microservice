from typing import Any

from django.template import loader

from application.email_services.user_email_service.context_processor_interface import (
    EmailContextProcessorInterface,
)
from application.email_services.user_email_service.template_generator_interface import (
    EmailTemplateGeneratorInterface,
)
from domain.user.entities import UserInterface
from infrastructure.email_services.email_service.context_processor import (
    get_email_context_processor,
)


class EmailTemplateGenerator(EmailTemplateGeneratorInterface):
    def __init__(self, context_processor: EmailContextProcessorInterface) -> None:
        self.context_processor = context_processor

    @staticmethod
    def generate_template(template_name: str, context: dict[str, Any], app_name: str = "emails") -> str:
        return loader.render_to_string(f"{app_name}/{template_name}", context, request=None, using=None)

    def generate_confirm_email_template(self, user: UserInterface) -> str:
        context = self.context_processor.confirm_email(user)

        return self.generate_template("confirm_email.html", context)

    def generate_confirm_new_email_template(self, user: UserInterface) -> str:
        context = self.context_processor.confirm_new_email(user)

        return self.generate_template("confirm_new_email.html", context)

    def generate_reset_password_template(self, user: UserInterface) -> str:
        context = self.context_processor.reset_password(user)

        return self.generate_template("reset_password.html", context)

    def generate_success_login_in_admin_template(self, **kwargs) -> str:
        return self.generate_template("success_login_in_admin.html", context=kwargs)

    def generate_cant_login_in_admin_template(self, **kwargs) -> str:
        return self.generate_template("error_login_in_admin.html", context=kwargs)


def get_email_template_generator(
    email_context_processor: EmailContextProcessorInterface = get_email_context_processor(),
) -> EmailTemplateGeneratorInterface:
    return EmailTemplateGenerator(context_processor=email_context_processor)
