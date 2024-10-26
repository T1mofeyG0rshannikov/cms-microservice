from typing import Any

from domain.referrals.referral import UserInterface
from infrastructure.email_services.email_service.link_generator.link_generator import (
    get_link_generator,
)
from infrastructure.email_services.email_service.link_generator.link_generator_interface import (
    LinkGeneratorInterface,
)
from infrastructure.persistence.models.settings import FormLogo
from infrastructure.persistence.models.styles.colors.colors import ColorStyles
from web.emails.serializers import EmailLogoSerializer

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

    def confirm_email(self, user: UserInterface) -> dict[Any, Any]:
        context = self.get_context()
        context["link"] = self.link_generator.get_url_to_confirm_email(user.id)

        return context

    def confirm_new_email(self, user: UserInterface) -> dict[Any, Any]:
        context = self.get_context()
        context["link"] = self.link_generator.get_url_to_confirm_new_email(user.id)

        return context

    def reset_password(self, user: UserInterface) -> dict[Any, Any]:
        context = self.get_context()
        context["link"] = self.link_generator.get_url_to_reset_password(user.id)
        context["user"] = user

        return context

    def try_login_in_admin(self, **kwargs) -> dict[str, Any]:
        context = {}
        context["ip"] = kwargs.get("ip")
        context["time"] = kwargs.get("time")
        context["login"] = kwargs.get("login")
        context["error"] = kwargs.get("error")

        return context

    def login_in_fake_admin(self, **kwargs) -> dict[str, Any]:
        context = self.get_context()
        context["ip"] = kwargs.get("ip")
        context["time"] = kwargs.get("time")
        context["login"] = kwargs.get("login")
        user = kwargs.get("user")
        if user and user.is_authenticated:
            user = user.email

        context["user"] = user

        return context


def get_email_context_processor(
    link_generator: LinkGeneratorInterface = get_link_generator(),
) -> EmailContextProcessorInterface:
    return EmailContextProcessor(link_generator=link_generator)
