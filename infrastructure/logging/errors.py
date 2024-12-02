from domain.logging.error import ErrorLogRepositoryInterface
from infrastructure.email_services.work_email_service.email_service import (
    get_work_email_service,
)
from infrastructure.email_services.work_email_service.email_service_interface import (
    WorkEmailServiceInterface,
)
from infrastructure.persistence.repositories.errors_repository import (
    get_errors_repository,
)


class ErrorLogger:
    def __init__(
        self,
        repository: ErrorLogRepositoryInterface,
        email_service: WorkEmailServiceInterface,
    ):
        self.repository = repository
        self.email_service = email_service

    def __call__(self, **kwargs) -> None:
        self.repository.create_error_log(**kwargs)

        self.email_service.send_error_emails(**kwargs)


def get_error_logger(
    repository: ErrorLogRepositoryInterface = get_errors_repository(),
    email_service: WorkEmailServiceInterface = get_work_email_service(),
) -> ErrorLogger:
    return ErrorLogger(repository=repository, email_service=email_service)
