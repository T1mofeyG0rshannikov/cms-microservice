from typing import Any

from emails.email_service.link_generator.link_generator_interface import (
    LinkGeneratorInterface,
)
from emails.serializers import EmailLogoSerializer
from settings.models import FormLogo
from styles.models.colors.colors import ColorStyles

from .context_processor_interface import EmailContextProcessorInterface


class EmailContextProcessor(EmailContextProcessorInterface):
    def __init__(self, link_generator: LinkGeneratorInterface):
        self.link_generator = link_generator

    @staticmethod
    def get_context() -> dict[Any, Any]:
        logo = FormLogo.objects.only("image", "width", "height").first()
        logo = EmailLogoSerializer(logo).data
        main_color = ColorStyles.objects.values_list("main_color").first()[0]

        return {"logo": logo, "main_color": main_color}

    def confirm_email(self, user) -> dict[Any, Any]:
        context = self.get_context()
        context["link"] = self.link_generator.get_url_to_confirm_email(user.id)

        return context

    def reset_password(self, user) -> dict[Any, Any]:
        context = self.get_context()
        context["link"] = self.link_generator.get_url_to_reset_password(user.id)
        context["user"] = user

        return context


def get_email_context_processor(link_generator: LinkGeneratorInterface) -> EmailContextProcessor:
    return EmailContextProcessor(link_generator)
