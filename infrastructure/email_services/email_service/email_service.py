from django.conf import settings

from application.services.domains.service import get_domain_service
from domain.referrals.referral import UserInterface
from infrastructure.auth.jwt_processor import get_jwt_processor
from infrastructure.email_services.base_email_service import BaseEmailService
from infrastructure.email_services.email_service.context_processor.context_processor import (
    get_email_context_processor,
)
from infrastructure.email_services.email_service.email_service_interface import (
    EmailServiceInterface,
)
from infrastructure.email_services.email_service.link_generator.link_generator import (
    get_link_generator,
)
from infrastructure.email_services.email_service.template_generator.template_generator import (
    get_email_template_generator,
)
from infrastructure.email_services.email_service.template_generator.template_generator_interface import (
    EmailTemplateGeneratorInterface,
)


class EmailService(BaseEmailService, EmailServiceInterface):
    sender: str = f"BankoMag <{settings.EMAIL_HOST_USER}>"

    def __init__(self, template_generator: EmailTemplateGeneratorInterface) -> None:
        self.template_generator = template_generator

    def send_mail_to_confirm_email(self, user: UserInterface) -> None:
        template = self.template_generator.generate_confirm_email_template(user)
        self.send_email("Подтвердите свой email адрес", self.sender, [user.email], template)

    def send_mail_to_confirm_new_email(self, user: UserInterface) -> None:
        template = self.template_generator.generate_confirm_new_email_template(user)
        self.send_email("Подтвердите свой email адрес", self.sender, [user.new_email], template)

    def send_mail_to_reset_password(self, user: UserInterface) -> None:
        template = self.template_generator.generate_reset_password_template(user)
        self.send_email("Восстановление пароля", self.sender, [user.email], template)


def get_email_service() -> EmailServiceInterface:
    domain_service = get_domain_service()

    return EmailService(
        get_email_template_generator(
            get_email_context_processor(get_link_generator(get_jwt_processor(), domain_service.get_domain_string()))
        )
    )
