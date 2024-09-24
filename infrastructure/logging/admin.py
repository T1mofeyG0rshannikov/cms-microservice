from typing import Any

from django.http import HttpRequest

from domain.email.exceptions import CantSendMailError
from domain.logging.admin import AdminLogRepositoryInterface
from infrastructure.email_services.work_email_service.email_service_interface import (
    WorkEmailServiceInterface,
)
from infrastructure.get_ip import get_client_ip


class AdminLoginLogger:
    def __init__(
        self,
        repository: AdminLogRepositoryInterface,
        email_service: WorkEmailServiceInterface,
    ) -> None:
        self.repository = repository
        self.email_service = email_service

    def error(self, request: HttpRequest, fields: dict[str, Any], error: str) -> None:
        ip_address = get_client_ip(request)

        log = self.repository.create_logg(ip_address, **fields)

        self.email_service.send_error_admin_login_message(ip=ip_address, **fields, time=log.date, error=error)

    def success(self, request: HttpRequest, fields: dict[str, Any]) -> None:
        ip_address = get_client_ip(request)

        log = self.repository.create_logg(ip_address, **fields)

        self.email_service.send_success_admin_login_message(ip=ip_address, **fields, time=log.date)

    def fake_admin_panel(self, request: HttpRequest, fields: dict[str, Any]) -> None:
        ip_address = get_client_ip(request)

        log = self.repository.create_logg_fake(ip_address, **fields)

        self.email_service.send_fake_admin_login_message(ip=ip_address, **fields, time=log.date)
