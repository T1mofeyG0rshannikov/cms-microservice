from django.conf import settings

from application.services.domains.service import get_domain_service
from domain.email.repository import SystemRepositoryInterface
from infrastructure.email_services.base_email_service import BaseEmailService
from infrastructure.email_services.work_email_service.context_processor.context_processor import (
    get_work_email_context_processor,
)
from infrastructure.email_services.work_email_service.email_service_interface import (
    WorkEmailServiceInterface,
)
from infrastructure.email_services.work_email_service.template_generator.template_generator import (
    get_work_email_template_generator,
)
from infrastructure.email_services.work_email_service.template_generator.template_generator_interface import (
    WorkEmailTemplateGeneratorInterface,
)
from infrastructure.persistence.repositories.system_repository import (
    get_system_repository,
)


class WorkEmailService(BaseEmailService, WorkEmailServiceInterface):
    sender: str = f"BankoMag <{settings.SYSTEM_EMAIL_HOST_USER}>"

    def __init__(
        self, template_generator: WorkEmailTemplateGeneratorInterface, repository: SystemRepositoryInterface
    ) -> None:
        self.template_generator = template_generator
        self.repository = repository

    def send_email(self, subj: str, sender: str, html_message: str):
        emails = self.repository.get_system_emails()

        return super().send_email(subj, sender, emails, html_message)

    def send_success_admin_login_message(self, **kwargs) -> None:
        template = self.template_generator.generate_success_login_in_admin_template(**kwargs)
        self.send_email("Вход в администраторскую панель", self.sender, template)

    def send_error_admin_login_message(self, **kwargs) -> None:
        template = self.template_generator.generate_cant_login_in_admin_template(**kwargs)
        self.send_email("Ошибка входа в администраторскую панель", self.sender, template)

    def send_fake_admin_login_message(self, **kwargs) -> None:
        template = self.template_generator.generate_login_in_fake_admin(**kwargs)
        self.send_email("Попытка входа в имитацию админки", self.sender, template)

    def send_error_emails(self, **kwargs) -> None:
        template = self.template_generator.generate_errror_message(**kwargs)
        self.send_email("Ошибка на сервере", self.sender, template)


def get_work_email_service() -> WorkEmailServiceInterface:
    domain_service = get_domain_service()

    return WorkEmailService(
        get_work_email_template_generator(get_work_email_context_processor()), get_system_repository()
    )
