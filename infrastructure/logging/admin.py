from typing import Any

from domain.email.exceptions import CantSendMailError
from domain.logging.admin import AdminLogRepositoryInterface
from infrastructure.email_services.work_email_service.email_service_interface import (
    WorkEmailServiceInterface,
)
from infrastructure.requests.service import RequestService


class AdminLoginLogger:
    def __init__(
        self,
        repository: AdminLogRepositoryInterface,
        email_service: WorkEmailServiceInterface,
        request_service: RequestService,
    ) -> None:
        self.repository = repository
        self.email_service = email_service
        self.request_service = request_service

    def error(self, fields: dict[str, Any], error: str) -> None:
        ip_address = self.request_service.get_client_ip()

        log = self.repository.create_logg(ip_address, **fields)

        self.email_service.send_error_admin_login_message(ip=ip_address, **fields, time=log.date, error=error)

    def success(self, fields: dict[str, Any]) -> None:
        ip_address = self.request_service.get_client_ip()

        log = self.repository.create_logg(ip_address, **fields)

        self.email_service.send_success_admin_login_message(ip=ip_address, **fields, time=log.date)

    def fake_admin_panel(self, fields: dict[str, Any]) -> None:
        ip_address = self.request_service.get_client_ip()

        log = self.repository.create_logg_fake_admin(ip_address, **fields)

        self.email_service.send_fake_admin_login_message(ip=ip_address, **fields, time=log.date)
