from django.conf import settings
from kombu.exceptions import OperationalError

from domens.domain_service.domain_service import DomainService
from emails.email_service.context_processor.context_processor import (
    get_email_context_processor,
)
from emails.email_service.email_service_interface import EmailServiceInterface
from emails.email_service.link_generator.link_generator import get_link_generator
from emails.email_service.tasks import send_email
from emails.email_service.template_generator.template_generator import (
    get_email_template_generator,
)
from emails.email_service.template_generator.template_generator_interface import (
    EmailTemplateGeneratorInterface,
)
from emails.exceptions import CantSendMailError
from user.auth.jwt_processor import get_jwt_processor
from user.interfaces import UserInterface


class EmailService(EmailServiceInterface):
    sender: str = f"BankoMag <{settings.EMAIL_HOST_USER}>"

    def __init__(self, template_generator: EmailTemplateGeneratorInterface) -> None:
        self.template_generator = template_generator

    @staticmethod
    def send_email(*args, **kwargs):
        try:
            send_email.delay(*args, **kwargs)
        except OperationalError:
            raise CantSendMailError("cant send mail to user")

    def send_mail_to_confirm_email(self, user: UserInterface) -> None:
        template = self.template_generator.generate_confirm_email_template(user)
        self.send_email("Подтвердите свой email адрес", self.sender, [user.email], template)

    def send_mail_to_confirm_new_email(self, user: UserInterface) -> None:
        template = self.template_generator.generate_confirm_new_email_template(user)
        self.send_email("Подтвердите свой email адрес", self.sender, [user.new_email], template)

    def send_mail_to_reset_password(self, user: UserInterface) -> None:
        template = self.template_generator.generate_reset_password_template(user)
        self.send_email("Восстановление пароля", self.sender, [user.email], template)


def get_email_service() -> EmailService:
    return EmailService(
        get_email_template_generator(
            get_email_context_processor(get_link_generator(get_jwt_processor(), DomainService.get_domain_string()))
        )
    )
