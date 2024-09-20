from domain.email.repository import SystemRepositoryInterface
from domain.logging.error import ErrorLogRepositoryInterface
from infrastructure.email_services.work_email_service.email_service_interface import (
    WorkEmailServiceInterface,
)


class ErrorLogger:
    def __init__(
        self,
        repository: ErrorLogRepositoryInterface,
        system_repository: SystemRepositoryInterface,
        email_service: WorkEmailServiceInterface,
    ):
        self.repository = repository
        self.system_repository = system_repository
        self.email_service = email_service

    def __call__(self, **kwargs) -> None:
        self.repository.create_error_log(**kwargs)

        emails = self.system_repository.get_system_emails()

        # self.email_service.send_error_emails(emails, **kwargs)
